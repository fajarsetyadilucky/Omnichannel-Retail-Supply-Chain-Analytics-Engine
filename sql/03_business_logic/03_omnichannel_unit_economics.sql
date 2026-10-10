-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 03_omnichannel_unit_economics.sql
-- Module       : 03_business_logic
-- Description  : Analisis Unit Economics per Kanal Belanja, Profitabilitas Kontribusi Bersih
--                (Net Contribution Margin), dan Efisiensi Throughput Cabang per Meter Persegi.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS:
-- Model bisnis omnichannel menggabungkan kanal offline (In-Store POS) dan digital
-- (Mobile App, Website, Quick Commerce Instant).
-- Tantangan: Kanal online seringkali membakar uang (*burn rate*) karena diskon promosi
-- dan subsidi ongkos kirim logistik pengantaran.
-- Melalui kueri ini, kita membedah:
-- 1. Apakah Quick Commerce menguntungkan secara unit margin atau menjadi loss-leader?
-- 2. Berapa omzet yang dihasilkan per meter persegi gudang (Revenue per SQM)?
-- 3. Bagaimana performa pemenuhan waktu antar (Delivery SLA percentiles)?
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: UNIT ECONOMICS & PROFITABILITAS PER KANAL PENJUALAN OMNICHANNEL
-- ========================================================================================
-- Membedah GMV, COGS, Gross Margin, Diskon, Ongkir, dan Net Contribution Margin.
-- ========================================================================================

WITH order_cogs AS (
    -- Agregasi HPP (Cost of Goods Sold) riil per order dari detail item
    SELECT 
        order_id,
        SUM(quantity * unit_cost) AS total_cogs_idr,
        SUM(line_total) AS total_items_gross_idr
    FROM raw_order_items
    GROUP BY order_id
),
channel_summary AS (
    SELECT 
        o.sales_channel,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS unique_transacting_customers,
        
        -- Finansial Top-Line (Gross Merchandise Value / Revenue)
        SUM(o.subtotal) AS total_subtotal_idr,
        SUM(o.discount_amount) AS total_discounts_given_idr,
        SUM(o.shipping_fee) AS total_shipping_revenue_idr,
        SUM(o.total_amount) AS total_net_sales_gmv_idr,
        
        -- Finansial Bottom-Line (COGS & Margins)
        SUM(cogs.total_cogs_idr) AS total_cogs_idr,
        SUM(cogs.total_items_gross_idr - cogs.total_cogs_idr) AS gross_profit_idr,
        
        -- Net Contribution Margin = Gross Profit + Shipping Collected - Discounts Given
        SUM(
            (cogs.total_items_gross_idr - cogs.total_cogs_idr) 
            + o.shipping_fee 
            - o.discount_amount
        ) AS net_contribution_margin_idr,
        
        -- Metrik Waktu Pengantaran (Khusus Delivery Channels)
        ROUND(AVG(CASE WHEN o.sales_channel != 'In-Store POS' THEN o.delivery_duration_minutes END), 1) AS avg_delivery_minutes,
        PERCENTILE_CONT(0.50) WITHIN GROUP (
            ORDER BY CASE WHEN o.sales_channel != 'In-Store POS' THEN o.delivery_duration_minutes END
        ) AS median_delivery_minutes,
        PERCENTILE_CONT(0.95) WITHIN GROUP (
            ORDER BY CASE WHEN o.sales_channel != 'In-Store POS' THEN o.delivery_duration_minutes END
        ) AS p95_delivery_minutes
    FROM raw_orders o
    JOIN order_cogs cogs ON o.order_id = cogs.order_id
    WHERE o.order_status = 'COMPLETED' -- Standar audit enterprise: hanya pesanan sukses terealisasi
    GROUP BY o.sales_channel
)
SELECT 
    sales_channel,
    total_orders,
    unique_transacting_customers,
    
    -- Average Order Value (AOV)
    ROUND(total_net_sales_gmv_idr / total_orders, 0) AS aov_idr,
    
    total_net_sales_gmv_idr,
    gross_profit_idr,
    
    -- Gross Margin % = Gross Profit / Subtotal * 100
    ROUND(gross_profit_idr * 100.0 / total_subtotal_idr, 2) AS gross_margin_pct,
    
    total_discounts_given_idr,
    ROUND(total_discounts_given_idr * 100.0 / total_subtotal_idr, 2) AS discount_rate_pct,
    
    total_shipping_revenue_idr,
    net_contribution_margin_idr,
    
    -- Contribution Margin % = Net Margin / Total Sales * 100
    ROUND(net_contribution_margin_idr * 100.0 / total_net_sales_gmv_idr, 2) AS net_contribution_margin_pct,
    
    avg_delivery_minutes,
    median_delivery_minutes,
    p95_delivery_minutes
FROM channel_summary
ORDER BY total_net_sales_gmv_idr DESC;


-- ========================================================================================
-- KUERI 2: PRODUKTIVITAS SPASIAL & THROUGHPUT HUB PER METER PERSEGI (REVENUE PER SQM)
-- ========================================================================================
-- Membandingkan efisiensi ruang gudang: Dark Store vs Flagship vs Express Hub.
-- ========================================================================================

SELECT 
    st.store_id,
    st.store_name,
    st.city,
    st.store_type,
    st.sqm_capacity,
    COUNT(o.order_id) AS total_orders_fulfilled,
    SUM(o.total_amount) AS total_revenue_idr,
    
    -- Metrik Efisiensi Ritel Spasial
    ROUND(SUM(o.total_amount) / st.sqm_capacity, 0) AS revenue_per_sqm_idr,
    ROUND(COUNT(o.order_id) * 1.0 / st.sqm_capacity, 2) AS orders_throughput_per_sqm,
    
    -- Rata-rata Nilai Keranjang Belanja Cabang (AOV)
    ROUND(AVG(o.total_amount), 0) AS store_aov_idr
FROM seed_stores st
LEFT JOIN raw_orders o ON st.store_id = o.store_id AND o.order_status = 'COMPLETED'
GROUP BY st.store_id, st.store_name, st.city, st.store_type, st.sqm_capacity
ORDER BY revenue_per_sqm_idr DESC;


-- ========================================================================================
-- KUERI 3: SLA KEPATUHAN PENGANTARAN INSTANT QUICK COMMERCE (< 30 MENIT)
-- ========================================================================================
-- Mengukur persentase pemenuhan komitmen "Sampai Dalam 30 Menit" di setiap Hub.
-- ========================================================================================

WITH instant_orders AS (
    SELECT 
        o.store_id,
        st.store_name,
        st.city,
        o.order_id,
        o.delivery_duration_minutes,
        CASE WHEN o.delivery_duration_minutes <= 30 THEN 1 ELSE 0 END AS is_under_30_mins,
        CASE WHEN o.delivery_duration_minutes > 40 THEN 1 ELSE 0 END AS is_critical_late
    FROM raw_orders o
    JOIN seed_stores st ON o.store_id = st.store_id
    WHERE o.sales_channel = 'Quick Commerce Instant'
      AND o.order_status = 'COMPLETED'
)
SELECT 
    store_id,
    store_name,
    city,
    COUNT(*) AS total_instant_orders,
    ROUND(AVG(delivery_duration_minutes), 1) AS avg_duration_mins,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY delivery_duration_minutes) AS median_duration_mins,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY delivery_duration_minutes) AS p90_duration_mins,
    SUM(is_under_30_mins) AS fulfilled_under_30_mins,
    ROUND(SUM(is_under_30_mins) * 100.0 / COUNT(*), 2) AS sla_compliance_pct,
    SUM(is_critical_late) AS orders_exceeding_40_mins
FROM instant_orders
GROUP BY store_id, store_name, city
ORDER BY sla_compliance_pct DESC;
