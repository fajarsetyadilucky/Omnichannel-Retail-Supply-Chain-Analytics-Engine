-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 04_materialized_views.sql
-- Module       : 05_performance_tuning
-- Description  : Desain & Implementasi Materialized Views untuk Agregasi Dashboard Manajemen,
--                Mitigasi Blunder Kunci Eksklusif (Lock Outage), dan Refresh Concurrently.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH & ARSITEKTUR MATERIALIZED VIEWS:
-- Dashboard eksekutif (Power BI, Metabase, Tableau, Looker) sering kali mengirimkan query
-- agregasi berat (SUM, AVG, COUNT DISTINCT) ke jutaan baris data setiap kali halaman dibuka.
-- Menjalankan kalkulasi on-the-fly untuk data historis statis adalah pemborosan resource CPU.
--
-- SOLUSI: Pre-computing hasil agregasi ke dalam Materialized Views terindeks.
--
-- ⚠️ DETEKSI & PENGHINDARAN BLUNDER LEVEL ARSITEK:
-- Blunder Arsitektur 1 (Table Exclusive Lock Outage):
--   Menjalankan perintah standar: `REFRESH MATERIALIZED VIEW my_mv;`
--   Perintah ini mengakuisisi ACCESS EXCLUSIVE LOCK yang MEMBLOKIR seluruh kueri SELECT
--   dari user / dashboard selama proses refresh berlangsung!
-- Solusi Profesional:
--   Gunakan klausa non-blocking: `REFRESH MATERIALIZED VIEW CONCURRENTLY my_mv;`
--
-- Blunder Arsitektur 2 (Prasyarat Unique Index untuk Refresh Concurrently):
--   PostgreSQL SECARA KETAT mewajibkan adanya UNIQUE INDEX tanpa nilai NULL pada
--   Materialized View sebelum perintah `CONCURRENTLY` dapat dieksekusi.
--   Jika indeks unik tidak ada, PostgreSQL akan melempar FATAL ERROR:
--     "ERROR: cannot refresh materialized view concurrently without a unique index"
--   Solusi Profesional:
--     Wajib membuat UNIQUE INDEX pada kolom kunci komposit view segera setelah view dibuat.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- TAHAP 1: MATERIALIZED VIEW 1 - REKAP OMZET HARIAN CABANG (DAILY STORE REVENUE)
-- ========================================================================================

DROP MATERIALIZED VIEW IF EXISTS mv_daily_store_revenue_summary CASCADE;

CREATE MATERIALIZED VIEW mv_daily_store_revenue_summary AS
SELECT 
    o.store_id,
    st.store_name,
    st.city AS store_city,
    st.store_type,
    DATE_TRUNC('day', o.order_timestamp)::date AS summary_date,
    COUNT(o.order_id) AS total_completed_orders,
    COUNT(DISTINCT o.customer_id) AS unique_transacting_customers,
    SUM(o.subtotal) AS gross_subtotal_idr,
    SUM(o.discount_amount) AS total_discounts_idr,
    SUM(o.shipping_fee) AS total_shipping_revenue_idr,
    SUM(o.total_amount) AS net_revenue_idr,
    ROUND(SUM(o.total_amount) / NULLIF(COUNT(o.order_id), 0), 0) AS daily_aov_idr
FROM raw_orders o
JOIN seed_stores st ON o.store_id = st.store_id
WHERE o.order_status = 'COMPLETED'
GROUP BY 
    o.store_id, st.store_name, st.city, st.store_type, 
    DATE_TRUNC('day', o.order_timestamp)::date
WITH DATA;

-- MITIGASI BLUNDER: Wajib membuat UNIQUE INDEX agar dapat di-refresh CONCURRENTLY
CREATE UNIQUE INDEX uidx_mv_store_daily_revenue 
ON mv_daily_store_revenue_summary (store_id, summary_date);


-- ========================================================================================
-- TAHAP 2: MATERIALIZED VIEW 2 - SCORECARD KINERJA VENDOR FMCG
-- ========================================================================================

DROP MATERIALIZED VIEW IF EXISTS mv_supplier_performance_scorecard CASCADE;

CREATE MATERIALIZED VIEW mv_supplier_performance_scorecard AS
SELECT 
    sup.supplier_id,
    sup.supplier_name,
    sup.category_specialty,
    sup.sla_target_pct AS contracted_sla_pct,
    COUNT(po.po_id) AS total_pos_handled,
    SUM(po.po_value) AS total_procurement_value_idr,
    COUNT(CASE WHEN po.delivery_status = 'ON_TIME' THEN 1 END) AS on_time_deliveries,
    COUNT(CASE WHEN po.delivery_status != 'ON_TIME' THEN 1 END) AS late_deliveries,
    ROUND(
        COUNT(CASE WHEN po.delivery_status = 'ON_TIME' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(po.po_id), 0), 
        2
    ) AS realized_sla_pct,
    SUM(po.delay_days) AS total_days_delayed,
    SUM(po.penalty_amount) AS total_penalty_receivable_idr
FROM seed_suppliers sup
LEFT JOIN raw_purchase_orders po ON sup.supplier_id = po.supplier_id
GROUP BY 
    sup.supplier_id, sup.supplier_name, sup.category_specialty, sup.sla_target_pct
WITH DATA;

-- MITIGASI BLUNDER: Wajib membuat UNIQUE INDEX pada supplier_id
CREATE UNIQUE INDEX uidx_mv_supplier_scorecard 
ON mv_supplier_performance_scorecard (supplier_id);


-- ========================================================================================
-- TAHAP 3: DEMONSTRASI ZERO-DOWNTIME REFRESH (CONCURRENT REFRESH DEMO)
-- ========================================================================================
-- Kueri SELECT dari dashboard TIDAK AKAN PERNAH TERKUNCI (Non-blocking updates).
-- ========================================================================================

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_store_revenue_summary;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_supplier_performance_scorecard;


-- ========================================================================================
-- TAHAP 4: PEMBUKTIAN KECEPATAN (BENCHMARKING MV VS ON-THE-FLY AGGREGATION)
-- ========================================================================================

-- Kueri Langsung ke Materialized View: Sub-milidetik (< 1-2 ms) dengan Index Scan
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT 
    store_name,
    summary_date,
    total_completed_orders,
    net_revenue_idr,
    daily_aov_idr
FROM mv_daily_store_revenue_summary
WHERE store_id = 'STR-001'
  AND summary_date BETWEEN '2024-06-01' AND '2024-06-30'
ORDER BY summary_date;
