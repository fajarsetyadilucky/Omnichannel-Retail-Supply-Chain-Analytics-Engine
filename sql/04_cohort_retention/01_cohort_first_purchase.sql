-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 01_cohort_first_purchase.sql
-- Module       : 04_cohort_retention
-- Description  : Penentuan Kohort Bulan Pertama Belanja (Customer First Purchase Cohort),
--                Atribusi Kanal Akuisisi Pertama (First-Touch Channel), dan Nilai Transaksi Awal.
--                Menggunakan Deterministic Order Sequence Tie-Breaker untuk menjamin 0 duplikasi.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS & ARSITEKTUR ANALITIK:
-- Analisis siklus hidup pelanggan (Customer Lifecycle) dimulai dari momen transaksi pertama
-- (Inception Date / Day Zero).
-- Dalam ritel omnichannel, memahami bulan akuisisi dan kanal belanja pertama sangat krusial:
-- 1. Apakah pelanggan yang diakuisisi via Quick Commerce memiliki nilai keranjang awal
--    yang berbeda dibanding pelanggan toko fisik (In-Store POS)?
-- 2. Berapa laju pertumbuhan basis pelanggan baru setiap bulan di sepanjang tahun 2024?
-- 3. Bagaimana profil segmentasi (Loyalty Tier & Wilayah Kota) dari setiap kohort?
--
-- ⚠️ ARSITEKTUR TIE-BREAKER (PENGHINDARAN BLUNDER ATRIBUSI):
-- Jika pelanggan melakukan 2 transaksi di jam/menit yang sama pada hari pertama, joining
-- menggunakan MIN(timestamp) akan memicu duplikasi relasi 1-ke-banyak.
-- Solusi Arsitek: Gunakan ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY timestamp, order_id)
-- dengan filter `order_seq = 1` guna menjamin tepat 1 first-touch attribution per pelanggan.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: DISTRIBUSI BULAN AKUISISI KOHORT PERTAMA & FINANCIAL BASKET AOV
-- ========================================================================================
-- Menentukan bulan pertama transaksi tiap pelanggan (Completed Orders Only)
-- dan mengukur rata-rata nilai transaksi awal (Initial Basket Size / AOV).
-- ========================================================================================

WITH customer_ranked_orders AS (
    SELECT 
        customer_id,
        order_id AS initial_order_id,
        order_timestamp AS first_order_timestamp,
        sales_channel AS acquisition_channel,
        total_amount AS initial_spend_idr,
        DATE_TRUNC('month', order_timestamp)::date AS cohort_month,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_timestamp ASC, order_id ASC
        ) AS order_sequence_num
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
),
first_order_details AS (
    -- Ambil tepat 1 transaksi pertama per pelanggan (Deterministic First-Touch Attribution)
    SELECT 
        customer_id,
        cohort_month,
        first_order_timestamp,
        initial_order_id,
        acquisition_channel,
        initial_spend_idr
    FROM customer_ranked_orders
    WHERE order_sequence_num = 1
)
SELECT 
    cohort_month,
    COUNT(customer_id) AS new_customers_acquired,
    
    -- Pangsa Akuisisi Pelanggan Baru (%)
    ROUND(
        COUNT(customer_id) * 100.0 / 
        SUM(COUNT(customer_id)) OVER (), 
        2
    ) AS pct_share_of_total_acquired,
    
    -- Akumulasi Nilai Transaksi Pertama (First-Day GMV Riil)
    SUM(initial_spend_idr) AS initial_cohort_gmv_idr,
    
    -- Rata-rata Keranjang Belanja Transaksi Pertama (First-Order AOV)
    ROUND(AVG(initial_spend_idr), 0) AS first_order_aov_idr,
    
    -- Nilai Transaksi Minimum & Maksimum
    MIN(initial_spend_idr) AS min_first_order_spend_idr,
    MAX(initial_spend_idr) AS max_first_order_spend_idr
FROM first_order_details
GROUP BY cohort_month
ORDER BY cohort_month;


-- ========================================================================================
-- KUERI 2: ATRIBUSI KANAL AKUISISI PERTAMA (FIRST-TOUCH CHANNEL ATTRIBUTION)
-- ========================================================================================
-- Membedah kanal mana yang paling efektif mendatangkan pelanggan baru per kohort.
-- ========================================================================================

WITH customer_ranked_orders AS (
    SELECT 
        customer_id,
        order_id AS initial_order_id,
        order_timestamp AS first_order_timestamp,
        sales_channel AS acquisition_channel,
        total_amount AS initial_spend_idr,
        DATE_TRUNC('month', order_timestamp)::date AS cohort_month,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_timestamp ASC, order_id ASC
        ) AS order_sequence_num
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
),
first_orders_deduped AS (
    SELECT * FROM customer_ranked_orders WHERE order_sequence_num = 1
),
first_order_channel AS (
    SELECT 
        cohort_month,
        acquisition_channel,
        COUNT(customer_id) AS customers_count,
        SUM(initial_spend_idr) AS total_initial_revenue_idr
    FROM first_orders_deduped
    GROUP BY cohort_month, acquisition_channel
)
SELECT 
    cohort_month,
    acquisition_channel,
    customers_count,
    ROUND(
        customers_count * 100.0 / 
        SUM(customers_count) OVER (PARTITION BY cohort_month), 
        2
    ) AS channel_acquisition_share_pct,
    total_initial_revenue_idr,
    ROUND(total_initial_revenue_idr / customers_count, 0) AS channel_first_aov_idr
FROM first_order_channel
ORDER BY cohort_month, customers_count DESC;


-- ========================================================================================
-- KUERI 3: PROFIL LOYALTY TIER & DOMISILI KOTA PELANGGAN PER BULAN AKUISISI
-- ========================================================================================
-- Memetakan distribusi tier loyalitas (Platinum, Gold, Silver, Bronze) serta sebaran
-- kota domisili dari pelanggan yang terakuisisi pada setiap gelombang kohort.
-- ========================================================================================

WITH customer_first_orders AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_timestamp))::date AS cohort_month
    FROM raw_orders
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
)
SELECT 
    cfo.cohort_month,
    c.city,
    c.loyalty_tier,
    COUNT(cfo.customer_id) AS customer_count,
    ROUND(
        COUNT(cfo.customer_id) * 100.0 / 
        SUM(COUNT(cfo.customer_id)) OVER (PARTITION BY cfo.cohort_month), 
        2
    ) AS segment_share_pct
FROM customer_first_orders cfo
JOIN seed_customers c ON cfo.customer_id = c.customer_id
GROUP BY cfo.cohort_month, c.city, c.loyalty_tier
ORDER BY cfo.cohort_month, customer_count DESC;
