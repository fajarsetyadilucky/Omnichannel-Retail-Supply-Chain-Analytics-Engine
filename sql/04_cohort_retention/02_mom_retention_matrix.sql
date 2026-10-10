-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 02_mom_retention_matrix.sql
-- Module       : 04_cohort_retention
-- Description  : Analisis Retensi Pelanggan Month-over-Month (MoM), Laju Pembusukan Retensi
--                (Retention Decay & Churn Velocity), dan Akumulasi Customer Lifetime Value (LTV).
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS:
-- Biaya akuisisi pelanggan (Customer Acquisition Cost / CAC) di ritel modern sangat mahal.
-- Profitabilitas jangka panjang bertumpu pada kemampuan gerai mempertahankan pelanggan
-- agar melakukan transaksi berulang (Repeat Purchase) di bulan-bulan berikutnya (M1 s/d M11).
-- Melalui modul ini kita mengukur:
-- 1. Berapa persen pelanggan yang kembali aktif belanja di setiap bulan (Retention Rate %)?
-- 2. Berapa order rata-rata yang dihasilkan oleh pelanggan aktif setiap bulannya?
-- 3. Bagaimana kurva akumulasi nilai belanja seumur hidup (Cumulative LTV Trajectory)?
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: RINCIAN GRANULAR RETENSI MONTH-OVER-MONTH & PERFORMA BELANJA ULANG
-- ========================================================================================
-- Menghitung jumlah pelanggan aktif, tingkat retensi, frekuensi order, dan GMV per bulan.
-- ========================================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_timestamp))::date AS cohort_month
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
),
customer_monthly_orders AS (
    SELECT 
        o.customer_id,
        cfp.cohort_month,
        (
            (EXTRACT(YEAR FROM o.order_timestamp) - EXTRACT(YEAR FROM cfp.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_timestamp) - EXTRACT(MONTH FROM cfp.cohort_month))
        )::INT AS cohort_index,
        COUNT(o.order_id) AS orders_in_month,
        SUM(o.total_amount) AS spend_in_month
    FROM raw_orders o
    JOIN customer_first_purchase cfp ON o.customer_id = cfp.customer_id
    WHERE o.order_status = 'COMPLETED'
    GROUP BY 
        o.customer_id, cfp.cohort_month,
        EXTRACT(YEAR FROM o.order_timestamp), EXTRACT(MONTH FROM o.order_timestamp)
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_purchase
    GROUP BY cohort_month
),
aggregated_retention AS (
    SELECT 
        cmo.cohort_month,
        cs.cohort_size,
        cmo.cohort_index,
        COUNT(DISTINCT cmo.customer_id) AS active_customers,
        SUM(cmo.orders_in_month) AS total_orders_placed,
        SUM(cmo.spend_in_month) AS total_monthly_gmv_idr
    FROM customer_monthly_orders cmo
    JOIN cohort_sizes cs ON cmo.cohort_month = cs.cohort_month
    GROUP BY cmo.cohort_month, cs.cohort_size, cmo.cohort_index
)
SELECT 
    cohort_month,
    cohort_size,
    cohort_index,
    active_customers,
    
    -- Retention Rate (%) = (Pelanggan Aktif Bulan Ini / Ukuran Kohort Awal) * 100
    ROUND(active_customers * 100.0 / cohort_size, 2) AS retention_rate_pct,
    
    -- Churn Rate (%) = 100 - Retention Rate (%)
    ROUND(100.0 - (active_customers * 100.0 / cohort_size), 2) AS churn_rate_pct,
    
    total_orders_placed,
    
    -- Frekuensi Transaksi per Pelanggan Aktif
    ROUND(total_orders_placed * 1.0 / active_customers, 2) AS orders_per_active_customer,
    
    total_monthly_gmv_idr,
    
    -- Average Order Value Belanja Ulang
    ROUND(total_monthly_gmv_idr / total_orders_placed, 0) AS monthly_aov_idr
FROM aggregated_retention
ORDER BY cohort_month, cohort_index;


-- ========================================================================================
-- KUERI 2: ANALISIS LAJU PEMBUSUKAN RETENSI (RETENTION DECAY & DROP-OFF AUDIT)
-- ========================================================================================
-- Mengukur titik kritis hilangnya pelanggan: M0 -> M1 Drop (Bulan Pertama) dan M1 -> M3 Drop.
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
retention_summary AS (
    SELECT 
        ca.cohort_month,
        cs.cohort_size,
        COUNT(DISTINCT CASE WHEN ca.cohort_index = 0 THEN ca.customer_id END) AS m0_users,
        COUNT(DISTINCT CASE WHEN ca.cohort_index = 1 THEN ca.customer_id END) AS m1_users,
        COUNT(DISTINCT CASE WHEN ca.cohort_index = 3 THEN ca.customer_id END) AS m3_users,
        COUNT(DISTINCT CASE WHEN ca.cohort_index = 6 THEN ca.customer_id END) AS m6_users
    FROM customer_activities ca
    JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    GROUP BY ca.cohort_month, cs.cohort_size
)
SELECT 
    cohort_month,
    cohort_size,
    m0_users,
    m1_users,
    ROUND(m1_users * 100.0 / cohort_size, 2) AS m1_retention_pct,
    
    -- Penurunan Bulan Pertama (M1 Drop-off Rate)
    ROUND((cohort_size - m1_users) * 100.0 / cohort_size, 2) AS m1_initial_churn_pct,
    
    m3_users,
    ROUND(m3_users * 100.0 / NULLIF(cohort_size, 0), 2) AS m3_retention_pct,
    
    m6_users,
    ROUND(m6_users * 100.0 / NULLIF(cohort_size, 0), 2) AS m6_retention_pct
FROM retention_summary
ORDER BY cohort_month;


-- ========================================================================================
-- KUERI 3: TRAJEKTORI NILAI SEUMUR HIDUP PELANGGAN KUMULATIF (CUMULATIVE LTV PER USER)
-- ========================================================================================
-- Menghitung akumulasi rupiah GMV yang disumbangkan per pelanggan terakuisisi seiring waktu.
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
        SUM(o.total_amount) AS monthly_spend_idr
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
),
running_ltv AS (
    SELECT 
        mcs.cohort_month,
        cs.cohort_size,
        mcs.cohort_index,
        mcs.monthly_spend_idr,
        -- Running Cumulative Spend per Cohort
        SUM(mcs.monthly_spend_idr) OVER (
            PARTITION BY mcs.cohort_month 
            ORDER BY mcs.cohort_index
        ) AS cumulative_cohort_revenue_idr
    FROM monthly_cohort_spend mcs
    JOIN cohort_sizes cs ON mcs.cohort_month = cs.cohort_month
)
SELECT 
    cohort_month,
    cohort_size,
    cohort_index,
    monthly_spend_idr,
    cumulative_cohort_revenue_idr,
    -- Cumulative LTV per Acquired Customer = Running Revenue / Cohort Size
    ROUND(cumulative_cohort_revenue_idr / cohort_size, 0) AS cumulative_ltv_per_acquired_customer_idr
FROM running_ltv
WHERE cohort_month IN ('2024-01-01', '2024-06-01') -- Sampel kohort semester 1 & tengah tahun
ORDER BY cohort_month, cohort_index;
