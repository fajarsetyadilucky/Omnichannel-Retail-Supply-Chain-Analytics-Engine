-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 03_cohort_crosstab_pivot.sql
-- Module       : 04_cohort_retention
-- Description  : Transformasi Matriks Segitiga Retensi Pelanggan (Triangular Heatmap Pivot)
--                dalam SQL Murni tanpa ketergantungan library eksternal (Python/Pandas).
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS:
-- Eksekutif ritel (CMO, VP of Growth, CEO) membutuhkan visualisasi ringkas dalam satu layar:
-- Seberapa cepat pelanggan "bocor" (churn) setelah bulan pertama akuisisi?
-- Mengubah tabel fakta vertikal (row-based) menjadi tabel crosstab matriks segitiga
-- (Triangular Heatmap) langsung di level database engine adalah keahlian lanjutan SQL
-- yang sangat bernilai tinggi.
-- Kueri ini menyajikan:
-- 1. Matriks Persentase Retensi Pelanggan (M0% s/d M11%).
-- 2. Matriks Jumlah Pelanggan Aktif Absolut (Headcount M0 s/d M11).
-- 3. Matriks Moneter Omzet Belanja Ulang (Repeat Spend Revenue IDR M0 s/d M11).
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: MATRIKS SEGITIGA PERSENTASE RETENSI PELANGGAN (TRIANGULAR RETENTION RATE %)
-- ========================================================================================
-- Menggunakan teknik ANSI SQL Conditional Aggregation (MAX/CASE WHEN) untuk membentuk pivot.
-- ========================================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_timestamp))::date AS cohort_month
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
),
customer_activities AS (
    SELECT DISTINCT
        o.customer_id,
        cfp.cohort_month,
        (
            (EXTRACT(YEAR FROM o.order_timestamp) - EXTRACT(YEAR FROM cfp.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_timestamp) - EXTRACT(MONTH FROM cfp.cohort_month))
        )::INT AS cohort_index
    FROM raw_orders o
    JOIN customer_first_purchase cfp ON o.customer_id = cfp.customer_id
    WHERE o.order_status = 'COMPLETED'
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_purchase
    GROUP BY cohort_month
),
cohort_activity_counts AS (
    SELECT 
        ca.cohort_month,
        cs.cohort_size,
        ca.cohort_index,
        COUNT(DISTINCT ca.customer_id) AS active_customers
    FROM customer_activities ca
    JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    GROUP BY ca.cohort_month, cs.cohort_size, ca.cohort_index
)
SELECT 
    cohort_month,
    cohort_size,
    ROUND(MAX(CASE WHEN cohort_index = 0 THEN active_customers END) * 100.0 / cohort_size, 1) AS m0_pct,
    ROUND(MAX(CASE WHEN cohort_index = 1 THEN active_customers END) * 100.0 / cohort_size, 1) AS m1_pct,
    ROUND(MAX(CASE WHEN cohort_index = 2 THEN active_customers END) * 100.0 / cohort_size, 1) AS m2_pct,
    ROUND(MAX(CASE WHEN cohort_index = 3 THEN active_customers END) * 100.0 / cohort_size, 1) AS m3_pct,
    ROUND(MAX(CASE WHEN cohort_index = 4 THEN active_customers END) * 100.0 / cohort_size, 1) AS m4_pct,
    ROUND(MAX(CASE WHEN cohort_index = 5 THEN active_customers END) * 100.0 / cohort_size, 1) AS m5_pct,
    ROUND(MAX(CASE WHEN cohort_index = 6 THEN active_customers END) * 100.0 / cohort_size, 1) AS m6_pct,
    ROUND(MAX(CASE WHEN cohort_index = 7 THEN active_customers END) * 100.0 / cohort_size, 1) AS m7_pct,
    ROUND(MAX(CASE WHEN cohort_index = 8 THEN active_customers END) * 100.0 / cohort_size, 1) AS m8_pct,
    ROUND(MAX(CASE WHEN cohort_index = 9 THEN active_customers END) * 100.0 / cohort_size, 1) AS m9_pct,
    ROUND(MAX(CASE WHEN cohort_index = 10 THEN active_customers END) * 100.0 / cohort_size, 1) AS m10_pct,
    ROUND(MAX(CASE WHEN cohort_index = 11 THEN active_customers END) * 100.0 / cohort_size, 1) AS m11_pct
FROM cohort_activity_counts
GROUP BY cohort_month, cohort_size
ORDER BY cohort_month;


-- ========================================================================================
-- KUERI 2: MATRIKS SEGITIGA JUMLAH PELANGGAN AKTIF ABSOLUT (HEADCOUNT VOLUME)
-- ========================================================================================
-- Memperlihatkan jumlah kepala pelanggan bertransaksi per bulan kalender.
-- ========================================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_timestamp))::date AS cohort_month
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
),
customer_activities AS (
    SELECT DISTINCT
        o.customer_id,
        cfp.cohort_month,
        (
            (EXTRACT(YEAR FROM o.order_timestamp) - EXTRACT(YEAR FROM cfp.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_timestamp) - EXTRACT(MONTH FROM cfp.cohort_month))
        )::INT AS cohort_index
    FROM raw_orders o
    JOIN customer_first_purchase cfp ON o.customer_id = cfp.customer_id
    WHERE o.order_status = 'COMPLETED'
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_purchase
    GROUP BY cohort_month
),
cohort_activity_counts AS (
    SELECT 
        ca.cohort_month,
        cs.cohort_size,
        ca.cohort_index,
        COUNT(DISTINCT ca.customer_id) AS active_customers
    FROM customer_activities ca
    JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    GROUP BY ca.cohort_month, cs.cohort_size, ca.cohort_index
)
SELECT 
    cohort_month,
    cohort_size,
    MAX(CASE WHEN cohort_index = 0 THEN active_customers END) AS m0_users,
    MAX(CASE WHEN cohort_index = 1 THEN active_customers END) AS m1_users,
    MAX(CASE WHEN cohort_index = 2 THEN active_customers END) AS m2_users,
    MAX(CASE WHEN cohort_index = 3 THEN active_customers END) AS m3_users,
    MAX(CASE WHEN cohort_index = 4 THEN active_customers END) AS m4_users,
    MAX(CASE WHEN cohort_index = 5 THEN active_customers END) AS m5_users,
    MAX(CASE WHEN cohort_index = 6 THEN active_customers END) AS m6_users,
    MAX(CASE WHEN cohort_index = 7 THEN active_customers END) AS m7_users,
    MAX(CASE WHEN cohort_index = 8 THEN active_customers END) AS m8_users,
    MAX(CASE WHEN cohort_index = 9 THEN active_customers END) AS m9_users,
    MAX(CASE WHEN cohort_index = 10 THEN active_customers END) AS m10_users,
    MAX(CASE WHEN cohort_index = 11 THEN active_customers END) AS m11_users
FROM cohort_activity_counts
GROUP BY cohort_month, cohort_size
ORDER BY cohort_month;


-- ========================================================================================
-- KUERI 3: MATRIKS SEGITIGA OMZET BELANJA ULANG MONETER (REPEAT SPEND REVENUE IDR)
-- ========================================================================================
-- Memperlihatkan kontribusi rupiah GMV riil yang masuk ke perusahaan per bulan indeks.
-- ========================================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_timestamp))::date AS cohort_month
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
),
monthly_cohort_spend AS (
    SELECT 
        cfp.cohort_month,
        (
            (EXTRACT(YEAR FROM o.order_timestamp) - EXTRACT(YEAR FROM cfp.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_timestamp) - EXTRACT(MONTH FROM cfp.cohort_month))
        )::INT AS cohort_index,
        SUM(o.total_amount) AS spend_in_month_idr
    FROM raw_orders o
    JOIN customer_first_purchase cfp ON o.customer_id = cfp.customer_id
    WHERE o.order_status = 'COMPLETED'
    GROUP BY 
        cfp.cohort_month,
        (
            (EXTRACT(YEAR FROM o.order_timestamp) - EXTRACT(YEAR FROM cfp.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_timestamp) - EXTRACT(MONTH FROM cfp.cohort_month))
        )::INT
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_purchase
    GROUP BY cohort_month
)
SELECT 
    mcs.cohort_month,
    cs.cohort_size,
    MAX(CASE WHEN mcs.cohort_index = 0 THEN mcs.spend_in_month_idr END) AS m0_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 1 THEN mcs.spend_in_month_idr END) AS m1_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 2 THEN mcs.spend_in_month_idr END) AS m2_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 3 THEN mcs.spend_in_month_idr END) AS m3_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 4 THEN mcs.spend_in_month_idr END) AS m4_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 5 THEN mcs.spend_in_month_idr END) AS m5_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 6 THEN mcs.spend_in_month_idr END) AS m6_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 7 THEN mcs.spend_in_month_idr END) AS m7_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 8 THEN mcs.spend_in_month_idr END) AS m8_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 9 THEN mcs.spend_in_month_idr END) AS m9_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 10 THEN mcs.spend_in_month_idr END) AS m10_spend_idr,
    MAX(CASE WHEN mcs.cohort_index = 11 THEN mcs.spend_in_month_idr END) AS m11_spend_idr
FROM monthly_cohort_spend mcs
JOIN cohort_sizes cs ON mcs.cohort_month = cs.cohort_month
GROUP BY mcs.cohort_month, cs.cohort_size
ORDER BY mcs.cohort_month;
