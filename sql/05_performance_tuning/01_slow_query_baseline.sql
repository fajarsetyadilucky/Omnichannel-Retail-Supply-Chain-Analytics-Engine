-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 01_slow_query_baseline.sql
-- Module       : 05_performance_tuning
-- Description  : Baseline Audit Rencana Eksekusi (Query Execution Plans) sebelum Tuning:
--                Mengidentifikasi bottleneck I/O, Sequential Scans, dan Buffer Read Spikes
--                menggunakan EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS).
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH & ARSITEKTUR KINERJA:
-- Dalam sistem ritel skala enterprise dengan jutaan transaksi, kueri analitik tanpa
-- indeks yang tepat memicu Sequential Table Scan (Seq Scan) ke seluruh blok data disk.
-- Dampaknya:
-- 1. Lonjakan I/O Disk (Buffer Read Spikes) yang membebani memori RAM server.
-- 2. Kueri dashboard analitik melambat dari milidetik menjadi hitungan detik.
-- 3. Terjadi "Table Contention" di mana kueri baca mengganggu transaksi kasir real-time.
--
-- File ini menangkap "Kondisi Sebelum Tuning" (Baseline State) untuk 3 kueri analitik berat:
--   - Kueri 1: Multi-Filter Pesanan Kanal (Store ID, Date Range, Status) di raw_orders.
--   - Kueri 2: Window Function Perputaran Inventori di raw_inventory_daily (263k baris).
--   - Kueri 3: Filter Keterlambatan Vendor FMCG di raw_purchase_orders.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: BASELINE FILTER RENTANG TANGGAL & KANAL TOKO (TABLE: raw_orders)
-- ========================================================================================
-- Kasus Penggunaan: Laporan omzet kuartalan per cabang gerai toko offline / hub.
-- Bottleneck yang Diantisipasi: Seq Scan 100.000 baris, memindai seluruh block pages.
-- ========================================================================================

EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS)
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


-- ========================================================================================
-- KUERI 2: BASELINE ROLLING WINDOW FUNCTION INVENTORI (TABLE: raw_inventory_daily)
-- ========================================================================================
-- Kasus Penggunaan: Deteksi laju permintaan moving average 14 hari per SKU per Toko.
-- Bottleneck yang Diantisipasi: Seq Scan 263.520 baris + In-Memory/Disk Sort Spikes.
-- ========================================================================================

EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS)
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


-- ========================================================================================
-- KUERI 3: BASELINE FILTER ANOMALI VENDOR TERLAMBAT (TABLE: raw_purchase_orders)
-- ========================================================================================
-- Kasus Penggunaan: Audit harian PO bermasalah yang terkena denda penalti keterlambatan.
-- Bottleneck yang Diantisipasi: Seq Scan 8.000 baris untuk mencari fraksi kecil (~5%) data.
-- ========================================================================================

EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS)
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
