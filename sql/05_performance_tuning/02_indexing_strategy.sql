-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 02_indexing_strategy.sql
-- Module       : 05_performance_tuning
-- Description  : Implementasi Arsitektur Pengindeksan Tingkat Lanjut:
--                1. Composite B-Tree Indexes (Equality Precedes Range)
--                2. Partial Indexes (Menghemat 85%-95% Index Size untuk Kasus Anomali)
--                3. BRIN (Block Range Index) untuk Append-Only Time-Series Logs
--                4. Validasi Pemangkasan I/O dan Peningkatan Kecepatan via EXPLAIN ANALYZE
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- PRINSIP ARSITEKTUR INDEXING & PENGHINDARAN BLUNDER:
-- Blunder Umum 1 (Over-Indexing):
--   Membuat indeks pada setiap kolom tunggal. Setiap indeks B-Tree memperlambat operasi
--   INSERT/UPDATE dan memakan memori cache RAM.
-- Solusi Arsitektural:
--   1. Composite Index: Urutkan kolom filter kesetaraan (Equality: store_id) sebelum
--      kolom rentang waktu (Range: order_timestamp).
--   2. Partial Index: Hanya indeks baris data yang relevan secara operasional
--      (misal: WHERE delivery_status != 'ON_TIME'). Menghemat 95% ruang disk!
--   3. BRIN Index: Untuk tabel time-series raksasa yang tersusun urut secara fisik di disk,
--      BRIN menyimpan rentang nilai (min/max) per 128 halaman, menghasilkan ukuran indeks
--      hingga 90% lebih kecil daripada B-Tree konvensional.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- TAHAP 1: PEMBUATAN INDEKS STRATEGIS (ENTERPRISE INDEX CREATION)
-- ========================================================================================

-- 1. Composite B-Tree Index untuk Filter Pesanan Toko & Rentang Tanggal
-- Aturan E-R: Equality (store_id) diletakkan sebelum Range (order_timestamp)
CREATE INDEX IF NOT EXISTS idx_orders_composite_store_timestamp 
ON raw_orders (store_id, order_timestamp);

-- 2. Composite B-Tree Index untuk Window Function Inventori
-- Mengoptimalkan PARTITION BY (store_id, product_id) dan ORDER BY (snapshot_date)
CREATE INDEX IF NOT EXISTS idx_inventory_composite_store_prod_date 
ON raw_inventory_daily (store_id, product_id, snapshot_date);

-- 3. Partial B-Tree Index untuk Pesanan Berstatus COMPLETED
-- Hanya mengindeks pesanan sukses, mengabaikan pesanan batal/retur
CREATE INDEX IF NOT EXISTS idx_orders_partial_completed 
ON raw_orders (sales_channel, total_amount) 
WHERE order_status = 'COMPLETED';

-- 4. Partial B-Tree Index untuk Pelanggaran SLA Vendor Keterlambatan
-- Dari 8.000 PO, hanya ~5% yang terlambat. Indeks ini sangat ramping dan cepat!
CREATE INDEX IF NOT EXISTS idx_po_partial_delayed 
ON raw_purchase_orders (supplier_id, delay_days, penalty_amount) 
WHERE delivery_status != 'ON_TIME';

-- 5. BRIN Index (Block Range Index) untuk Jejak Waktu Pesanan
-- Mengelompokkan 128 disk pages per range untuk menghemat RAM & disk footprint
CREATE INDEX IF NOT EXISTS idx_orders_brin_timestamp 
ON raw_orders USING brin (order_timestamp) 
WITH (pages_per_range = 128);


-- ========================================================================================
-- TAHAP 2: AUDIT FOOTPRINT UKURAN PENYIMPANAN INDEKS (STORAGE FOOTPRINT AUDIT)
-- ========================================================================================
-- Membandingkan efisiensi ruang disk antara B-Tree, Partial Index, dan BRIN.
-- ========================================================================================

SELECT 
    c.relname AS index_name,
    t.relname AS table_name,
    am.amname AS index_type,
    pg_size_pretty(pg_relation_size(c.oid)) AS index_size,
    pg_relation_size(c.oid) AS index_size_bytes,
    pg_size_pretty(pg_relation_size(t.oid)) AS table_size
FROM pg_class c
JOIN pg_index i ON c.oid = i.indexrelid
JOIN pg_class t ON i.indrelid = t.oid
JOIN pg_am am ON c.relam = am.oid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relname LIKE 'idx_%'
ORDER BY pg_relation_size(c.oid) DESC;


-- ========================================================================================
-- TAHAP 3: BUKTI EFISIENSI EKSEKUSI PASCA-INDEXING (EXPLAIN ANALYZE BENCHMARK)
-- ========================================================================================

-- Validasi 1: Kueri Pesanan Toko Pasca Composite Indexing
-- Membuktikan transisi dari "Seq Scan" menjadi "Bitmap Index Scan / Index Scan"
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT 
    store_id,
    sales_channel,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue_idr,
    ROUND(AVG(total_amount), 0) AS aov_idr
FROM raw_orders
WHERE store_id = 'STR-001'
  AND order_timestamp >= '2024-06-01 00:00:00'
  AND order_timestamp <  '2024-09-01 00:00:00'
  AND order_status = 'COMPLETED'
GROUP BY store_id, sales_channel
ORDER BY total_revenue_idr DESC;

-- Validasi 2: Kueri Inventori Pasca Composite Indexing
-- Membuktikan penghilangan operasi Sort eksternal berkat indeks terurut (snapshot_date)
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT 
    snapshot_date,
    store_id,
    product_id,
    stock_on_hand,
    units_sold_today,
    ROUND(AVG(units_sold_today) OVER (
        PARTITION BY store_id, product_id 
        ORDER BY snapshot_date 
        ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
    ), 2) AS rolling_14d_avg_sold
FROM raw_inventory_daily
WHERE store_id = 'STR-001'
  AND product_id = 'PRD-001'
ORDER BY snapshot_date DESC;

-- Validasi 3: Kueri Vendor Terlambat Pasca Partial Indexing
-- Membuktikan pemindaian instan hanya pada subset kecil data anomali
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT 
    supplier_id,
    delivery_status,
    COUNT(po_id) AS delayed_po_count,
    SUM(delay_days) AS total_delay_days,
    SUM(penalty_amount) AS total_penalty_idr
FROM raw_purchase_orders
WHERE delivery_status != 'ON_TIME'
GROUP BY supplier_id, delivery_status
ORDER BY total_penalty_idr DESC;
