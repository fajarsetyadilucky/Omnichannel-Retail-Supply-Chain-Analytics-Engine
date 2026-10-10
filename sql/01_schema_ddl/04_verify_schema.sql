-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 04_verify_schema.sql
-- Module       : 01_schema_ddl
-- Description  : Script audit & verifikasi integritas skema tabel, tipe kolom,
--                Primary Key, Foreign Key, dan CHECK constraints yang telah terpasang.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- 1. AUDIT DAFTAR TABEL & JUMLAH KOLOM
-- ----------------------------------------------------------------------------------------
SELECT 
    table_name,
    COUNT(column_name) AS total_columns,
    'OK - CREATED' AS status
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name IN (
      'seed_stores', 'seed_suppliers', 'seed_products', 'seed_customers',
      'raw_orders', 'raw_order_items', 'raw_inventory_daily', 'raw_purchase_orders'
  )
GROUP BY table_name
ORDER BY table_name;


-- ----------------------------------------------------------------------------------------
-- 2. AUDIT PRIMARY KEY & FOREIGN KEY CONSTRAINTS
-- ----------------------------------------------------------------------------------------
SELECT
    tc.table_name,
    tc.constraint_type,
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
LEFT JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.table_schema = 'public'
  AND tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
ORDER BY tc.table_name, tc.constraint_type DESC, kcu.column_name;


-- ----------------------------------------------------------------------------------------
-- 3. AUDIT BUSINESS INTEGRITY CHECK CONSTRAINTS
-- ----------------------------------------------------------------------------------------
SELECT
    r.relname AS table_name,
    con.conname AS check_constraint_name,
    pg_get_constraintdef(con.oid) AS constraint_definition
FROM pg_constraint con
JOIN pg_class r ON con.conrelid = r.oid
JOIN pg_namespace n ON n.oid = r.relnamespace
WHERE n.nspname = 'public'
  AND con.contype = 'c'
  AND r.relname IN (
      'seed_stores', 'seed_suppliers', 'seed_products', 'seed_customers',
      'raw_orders', 'raw_order_items', 'raw_inventory_daily', 'raw_purchase_orders'
  )
ORDER BY r.relname, con.conname;
