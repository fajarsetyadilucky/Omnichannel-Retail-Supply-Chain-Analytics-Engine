-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 03_table_partitioning.sql
-- Module       : 05_performance_tuning
-- Description  : Implementasi Partisi Tabel Deklaratif Rentang Waktu (Range Partitioning),
--                Mitigasi Blunder Primary Key Partisi, dan Pembuktian Partition Pruning.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH & ARSITEKTUR PARTISI POSTGRESQL:
-- Pada sistem ritel omnichannel dengan volume transaksi yang tumbuh ratusan ribu per bulan,
-- tabel monolithic (tunggal) akan membengkak menjadi puluhan gigabyte.
-- Dampak: Kueri yang hanya membutuhkan data 1 bulan tetap harus menelusuri indeks raksasa.
--
-- SOLUSI: Declarative Range Partitioning berdasarkan rentang bulanan `order_timestamp`.
--
-- ⚠️ DETEKSI & PENGHINDARAN BLUNDER LEVEL ARSITEK:
-- Blunder Arsitektur 1 (Partitioning Primary Key Violation):
--   Di PostgreSQL, membuat Primary Key tunggal pada tabel terpartisi:
--     `CREATE TABLE orders_partitioned (order_id VARCHAR PRIMARY KEY, ...)`
--   Akan menghasilkan FATAL ERROR:
--     "ERROR: unique constraint on partitioned table must include all partitioning columns"
--   Solusi Profesional:
--     Primary Key WAJIB berbentuk Composite Key yang menyertakan kolom partisi:
--     `PRIMARY KEY (order_id, order_timestamp)`
--
-- Blunder Arsitektur 2 (Pruning Deactivation):
--   Memastikan parameter engine `enable_partition_pruning` aktif (ON) agar planner
--   mengabaikan partisi yang tidak relevan secara otomatis.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- TAHAP 1: PEMBUATAN TABEL MASTER TERPARTISI (DECLARATIVE RANGE PARTITIONING)
-- ========================================================================================

CREATE TABLE IF NOT EXISTS orders_partitioned (
    order_id                    VARCHAR(20)         NOT NULL,
    customer_id                 VARCHAR(15)         NOT NULL,
    order_timestamp             TIMESTAMP           NOT NULL,
    sales_channel               sales_channel_enum  NOT NULL,
    store_id                    VARCHAR(10)         NOT NULL,
    payment_method              VARCHAR(50)         NOT NULL,
    order_status                order_status_enum   NOT NULL,
    subtotal                    NUMERIC(14,2)       NOT NULL,
    shipping_fee                NUMERIC(10,2)       NOT NULL DEFAULT 0.00,
    discount_amount             NUMERIC(10,2)       NOT NULL DEFAULT 0.00,
    total_amount                NUMERIC(14,2)       NOT NULL,
    delivery_duration_minutes   INTEGER             NOT NULL DEFAULT 0,
    
    -- MITIGASI BLUNDER: Primary Key wajib menyertakan kolom partisi (order_timestamp)
    CONSTRAINT pk_orders_partitioned PRIMARY KEY (order_id, order_timestamp)
) PARTITION BY RANGE (order_timestamp);


-- ========================================================================================
-- TAHAP 2: PEMBUATAN 12 CHILD PARTITIONS UNTUK TAHUN PENUH 2024
-- ========================================================================================

CREATE TABLE IF NOT EXISTS orders_2024_01 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01 00:00:00') TO ('2024-02-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_02 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-02-01 00:00:00') TO ('2024-03-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_03 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-03-01 00:00:00') TO ('2024-04-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_04 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-04-01 00:00:00') TO ('2024-05-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_05 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-05-01 00:00:00') TO ('2024-06-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_06 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-06-01 00:00:00') TO ('2024-07-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_07 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-07-01 00:00:00') TO ('2024-08-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_08 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-08-01 00:00:00') TO ('2024-09-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_09 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-09-01 00:00:00') TO ('2024-10-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_10 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-10-01 00:00:00') TO ('2024-11-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_11 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-11-01 00:00:00') TO ('2024-12-01 00:00:00');

CREATE TABLE IF NOT EXISTS orders_2024_12 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-12-01 00:00:00') TO ('2025-01-01 00:00:00');


-- ========================================================================================
-- TAHAP 3: MIGRASI DATA DARI TABEL NON-PARTISI (ETL MIGRATION)
-- ========================================================================================

INSERT INTO orders_partitioned (
    order_id, customer_id, order_timestamp, sales_channel, store_id,
    payment_method, order_status, subtotal, shipping_fee, discount_amount,
    total_amount, delivery_duration_minutes
)
SELECT 
    order_id, customer_id, order_timestamp, sales_channel, store_id,
    payment_method, order_status, subtotal, shipping_fee, discount_amount,
    total_amount, delivery_duration_minutes
FROM raw_orders
ON CONFLICT (order_id, order_timestamp) DO NOTHING;


-- ========================================================================================
-- TAHAP 4: PEMBUATAN INDEKS LOKAL OTOMATIS PADA SELURUH PARTISI
-- ========================================================================================

CREATE INDEX IF NOT EXISTS idx_orders_part_store_timestamp 
ON orders_partitioned (store_id, order_timestamp);


-- ========================================================================================
-- TAHAP 5: AUDIT DISTRIBUSI BARIS & UKURAN SETIAP PARTISI BULANAN
-- ========================================================================================

SELECT 
    nmsp_parent.nspname AS parent_schema,
    parent.relname      AS parent_table,
    child.relname       AS partition_name,
    pg_size_pretty(pg_relation_size(child.oid)) AS partition_data_size,
    pg_size_pretty(pg_total_relation_size(child.oid)) AS partition_total_size,
    c.reltuples::bigint AS estimated_row_count
FROM pg_inherits
JOIN pg_class parent        ON pg_inherits.inhparent = parent.oid
JOIN pg_class child         ON pg_inherits.inhrelid   = child.oid
JOIN pg_namespace nmsp_parent ON nmsp_parent.oid = parent.relnamespace
JOIN pg_class c             ON c.oid = child.oid
WHERE parent.relname = 'orders_partitioned'
ORDER BY child.relname;


-- ========================================================================================
-- TAHAP 6: PEMBUKTIAN PARTITION PRUNING VIA EXPLAIN (ANALYZE, BUFFERS)
-- ========================================================================================
-- Kueri di bawah ini hanya menargetkan bulan Maret 2024.
-- Bukti Arsitektural: Engine HANYA memindai partisi `orders_2024_03`.
-- 11 partisi lainnya (Jan, Feb, Apr-Des) DIABAIKAN SEPENUHNYA (Never Scanned),
-- menghemat lebih dari 91.6% I/O Disk!
-- ========================================================================================

SET enable_partition_pruning = on;

EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT 
    store_id,
    sales_channel,
    COUNT(order_id) AS march_orders,
    SUM(total_amount) AS march_gmv_idr
FROM orders_partitioned
WHERE order_timestamp >= '2024-03-01 00:00:00'
  AND order_timestamp <  '2024-04-01 00:00:00'
  AND order_status = 'COMPLETED'
GROUP BY store_id, sales_channel
ORDER BY march_gmv_idr DESC;
