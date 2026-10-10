-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 02_validate_ingestion.sql
-- Module       : 02_data_ingestion
-- Description  : Suite Pengujian Kualitas Data (Enterprise Data Quality & Reconciliation Test)
--                untuk memverifikasi kelengkapan baris, referential integrity (orphan records),
--                serta rekonsiliasi silang POS vs Inventori pasca pemuatan data.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- 1. UJI REKONSILIASI JUMLAH BARIS (ROW COUNT MATCHING)
-- ----------------------------------------------------------------------------------------
WITH actual_counts AS (
    SELECT 'seed_stores' AS table_name, COUNT(*) AS actual_rows FROM seed_stores
    UNION ALL
    SELECT 'seed_suppliers', COUNT(*) FROM seed_suppliers
    UNION ALL
    SELECT 'seed_products', COUNT(*) FROM seed_products
    UNION ALL
    SELECT 'seed_customers', COUNT(*) FROM seed_customers
    UNION ALL
    SELECT 'raw_orders', COUNT(*) FROM raw_orders
    UNION ALL
    SELECT 'raw_order_items', COUNT(*) FROM raw_order_items
    UNION ALL
    SELECT 'raw_inventory_daily', COUNT(*) FROM raw_inventory_daily
    UNION ALL
    SELECT 'raw_purchase_orders', COUNT(*) FROM raw_purchase_orders
),
expected_benchmarks AS (
    SELECT 'seed_stores' AS table_name, 12 AS expected_rows
    UNION ALL
    SELECT 'seed_suppliers', 15
    UNION ALL
    SELECT 'seed_products', 60
    UNION ALL
    SELECT 'seed_customers', 10000
    UNION ALL
    SELECT 'raw_orders', 100000
    UNION ALL
    SELECT 'raw_order_items', 228177
    UNION ALL
    SELECT 'raw_inventory_daily', 263520
    UNION ALL
    SELECT 'raw_purchase_orders', 8000
)
SELECT 
    a.table_name,
    a.actual_rows,
    e.expected_rows,
    CASE 
        WHEN a.actual_rows = e.expected_rows THEN '✅ 100% MATCH'
        ELSE '❌ MISMATCH'
    END AS reconciliation_status
FROM actual_counts a
JOIN expected_benchmarks e ON a.table_name = e.table_name
ORDER BY a.table_name;


-- ----------------------------------------------------------------------------------------
-- 2. UJI INTEGRITAS REFERENSIAL & DETEKSI DATA YATIM (ORPHAN RECORDS CHECK)
-- ----------------------------------------------------------------------------------------
-- Menguji apakah terdapat relasi Foreign Key yang bocor / tidak memiliki induk.
SELECT 
    'Orders -> Customers' AS relationship,
    COUNT(*) AS orphan_count,
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END AS test_status
FROM raw_orders o
LEFT JOIN seed_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL

UNION ALL

SELECT 
    'Orders -> Stores',
    COUNT(*),
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END
FROM raw_orders o
LEFT JOIN seed_stores s ON o.store_id = s.store_id
WHERE s.store_id IS NULL

UNION ALL

SELECT 
    'Order Items -> Orders',
    COUNT(*),
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END
FROM raw_order_items oi
LEFT JOIN raw_orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL

UNION ALL

SELECT 
    'Order Items -> Products',
    COUNT(*),
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END
FROM raw_order_items oi
LEFT JOIN seed_products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL

UNION ALL

SELECT 
    'Inventory -> Stores & Products',
    COUNT(*),
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END
FROM raw_inventory_daily inv
LEFT JOIN seed_stores s ON inv.store_id = s.store_id
LEFT JOIN seed_products p ON inv.product_id = p.product_id
WHERE s.store_id IS NULL OR p.product_id IS NULL

UNION ALL

SELECT 
    'Purchase Orders -> Suppliers & Stores',
    COUNT(*),
    CASE WHEN COUNT(*) = 0 THEN '✅ PASS (No Orphans)' ELSE '❌ FAIL' END
FROM raw_purchase_orders po
LEFT JOIN seed_suppliers sup ON po.supplier_id = sup.supplier_id
LEFT JOIN seed_stores st ON po.store_id = st.store_id
WHERE sup.supplier_id IS NULL OR st.store_id IS NULL;


-- ----------------------------------------------------------------------------------------
-- 3. UJI REKONSILIASI KASIR POS VS INVENTORI (GHOST STOCKOUT BULLETPROOF TEST)
-- ----------------------------------------------------------------------------------------
-- Memastikan tidak ada perbedaan antara units_sold_today di inventori dengan penjualan riil POS.
WITH pos_daily_sales AS (
    SELECT 
        o.order_timestamp::date AS transaction_date,
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS actual_pos_sold
    FROM raw_orders o
    JOIN raw_order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_timestamp::date, o.store_id, oi.product_id
),
comparison AS (
    SELECT 
        inv.snapshot_date,
        inv.store_id,
        inv.product_id,
        inv.units_sold_today AS inventory_sales,
        COALESCE(pos.actual_pos_sold, 0) AS pos_sales,
        inv.is_ghost_stockout
    FROM raw_inventory_daily inv
    LEFT JOIN pos_daily_sales pos 
      ON inv.snapshot_date = pos.transaction_date 
     AND inv.store_id = pos.store_id 
     AND inv.product_id = pos.product_id
)
SELECT 
    COUNT(*) AS total_snapshots_audited,
    SUM(CASE WHEN inventory_sales != pos_sales THEN 1 ELSE 0 END) AS total_sales_discrepancies,
    SUM(CASE WHEN is_ghost_stockout = TRUE AND pos_sales > 0 THEN 1 ELSE 0 END) AS ghost_stockout_contradictions,
    CASE 
        WHEN SUM(CASE WHEN inventory_sales != pos_sales THEN 1 ELSE 0 END) = 0 
         AND SUM(CASE WHEN is_ghost_stockout = TRUE AND pos_sales > 0 THEN 1 ELSE 0 END) = 0 
        THEN '✅ 100% BULLETPROOF SYNCHRONIZED'
        ELSE '❌ RECONCILIATION FAILED'
    END AS audit_verdict
FROM comparison;


-- ----------------------------------------------------------------------------------------
-- 4. AUDIT UKURAN PENYIMPANAN FISIK DATABASE (STORAGE FOOTPRINT AUDIT)
-- ----------------------------------------------------------------------------------------
SELECT 
    relname AS table_name,
    pg_size_pretty(pg_relation_size(c.oid)) AS data_size,
    pg_size_pretty(pg_indexes_size(c.oid)) AS index_size,
    pg_size_pretty(pg_total_relation_size(c.oid)) AS total_storage_size
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' 
  AND c.relkind = 'r'
  AND relname IN (
      'seed_stores', 'seed_suppliers', 'seed_products', 'seed_customers',
      'raw_orders', 'raw_order_items', 'raw_inventory_daily', 'raw_purchase_orders'
  )
ORDER BY pg_total_relation_size(c.oid) DESC;
