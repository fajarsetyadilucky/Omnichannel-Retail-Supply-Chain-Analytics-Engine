-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 01_ghost_stockout_detection.sql
-- Module       : 03_business_logic
-- Description  : Deteksi Anomali Kehabisan Stok Tersembunyi (Ghost Stockout Detection)
--                dan Estimasi Potensi Kerugian Omzet Penjualan (Lost Sales Opportunity)
--                menggunakan metode Gaps-and-Islands & Rolling Window Functions.
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS:
-- "Ghost Stockout" (Phantom Inventory) terjadi ketika sistem komputer ERP mencatat stok
-- masih tersedia di toko/hub (misal: 45 unit), namun secara fisik di rak barang tersebut
-- rusak, hilang, salah penempatan, atau dicuri.
-- Akibatnya: Konsumen tidak bisa membeli (penjualan kasir = 0 unit) selama berhari-hari.
-- Dampak finansial: Terjadi kebocoran omzet riil tanpa disadari oleh Store Manager.
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: DETEKSI INSIDEN GHOST STOCKOUT VIA GAPS-AND-ISLANDS WINDOW FUNCTION
-- ========================================================================================
-- Mengidentifikasi rentang hari berturut-turut (>= 3 hari) di mana produk FAST/MEDIUM
-- memiliki stok buku > 10 unit namun penjualan harian = 0.
-- ========================================================================================

WITH daily_demand_baseline AS (
    SELECT 
        inv.snapshot_date,
        inv.store_id,
        st.store_name,
        st.city AS store_city,
        inv.product_id,
        p.product_name,
        p.category,
        p.velocity_tier,
        p.selling_price,
        inv.stock_on_hand,
        inv.units_sold_today,
        inv.is_ghost_stockout,

        -- 1. Hitung baseline permintaan normal: rata-rata bergerak penjualan 14 hari ke belakang
        COALESCE(ROUND(AVG(inv.units_sold_today) OVER (
            PARTITION BY inv.store_id, inv.product_id 
            ORDER BY inv.snapshot_date 
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ), 2), 0.00) AS baseline_daily_velocity,

        -- 2. Flag anomali: Stok sistem positif (> 10 unit), produk FAST/MEDIUM, tapi penjualan 0
        CASE 
            WHEN inv.units_sold_today = 0 
             AND inv.stock_on_hand >= 10 
             AND p.velocity_tier IN ('FAST', 'MEDIUM') 
            THEN 1 
            ELSE 0 
        END AS is_zero_sales_anomaly
    FROM raw_inventory_daily inv
    JOIN seed_products p ON inv.product_id = p.product_id
    JOIN seed_stores st ON inv.store_id = st.store_id
),
island_segmentation AS (
    SELECT 
        *,
        -- 3. Gaps-and-Islands identifier: Mengelompokkan hari berturut-turut menjadi satu pulau (island)
        snapshot_date - (ROW_NUMBER() OVER (
            PARTITION BY store_id, product_id, is_zero_sales_anomaly 
            ORDER BY snapshot_date
        ) * INTERVAL '1 day') AS streak_island_group
    FROM daily_demand_baseline
),
ghost_stockout_incidents AS (
    SELECT 
        store_id,
        store_name,
        store_city,
        product_id,
        product_name,
        category,
        velocity_tier,
        selling_price,
        MIN(snapshot_date) AS incident_start_date,
        MAX(snapshot_date) AS incident_end_date,
        COUNT(*) AS duration_days,
        ROUND(AVG(stock_on_hand), 0) AS avg_phantom_stock_on_hand,
        ROUND(AVG(baseline_daily_velocity), 2) AS normal_daily_demand,

        -- 4. Estimasi Unit Gagal Jual = Durasi Hari x Baseline Permintaan Normal Harian
        ROUND(COUNT(*) * AVG(baseline_daily_velocity), 0) AS estimated_lost_units,

        -- 5. Estimasi Kerugian Penjualan (Rupiah) = Estimasi Unit Gagal Jual x Harga Jual Produk
        ROUND(COUNT(*) * AVG(baseline_daily_velocity) * selling_price, 0) AS estimated_lost_revenue_idr,

        -- 6. Triage Urgensi: Klasifikasi Tingkat Keparahan Anomali
        CASE 
            WHEN AVG(baseline_daily_velocity) >= 2.0 AND COUNT(*) >= 5 
            THEN 'CRITICAL PHANTOM OUTAGE (High Velocity Lost Sales)'
            WHEN AVG(baseline_daily_velocity) >= 1.0 
            THEN 'HIGH RISK GHOST STOCKOUT'
            ELSE 'MODERATE STAGNATION'
        END AS incident_severity_tier
    FROM island_segmentation
    WHERE is_zero_sales_anomaly = 1
    GROUP BY 
        store_id, store_name, store_city, product_id, product_name, category, 
        velocity_tier, selling_price, streak_island_group
    HAVING COUNT(*) >= 3 -- Ambang batas enterprise: minimal 3 hari berturut-turut macet
)
SELECT 
    incident_start_date,
    incident_end_date,
    duration_days,
    store_id,
    store_name,
    product_id,
    product_name,
    category,
    velocity_tier,
    avg_phantom_stock_on_hand,
    normal_daily_demand,
    estimated_lost_units,
    estimated_lost_revenue_idr,
    incident_severity_tier
FROM ghost_stockout_incidents
ORDER BY estimated_lost_revenue_idr DESC, duration_days DESC
LIMIT 20;


-- ========================================================================================
-- KUERI 2: AGREGASI KEBOCORAN MODAL PER CABANG TOKO / HUB (EXECUTIVE SUMMARY)
-- ========================================================================================
-- Membantu VP of Retail & Head of Logistics mengidentifikasi hub paling bermasalah.
-- ========================================================================================

WITH daily_demand_baseline AS (
    SELECT 
        inv.snapshot_date,
        inv.store_id,
        st.store_name,
        inv.product_id,
        p.selling_price,
        inv.stock_on_hand,
        inv.units_sold_today,
        COALESCE(AVG(inv.units_sold_today) OVER (
            PARTITION BY inv.store_id, inv.product_id 
            ORDER BY inv.snapshot_date 
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ), 0.00) AS baseline_daily_velocity,
        CASE 
            WHEN inv.units_sold_today = 0 AND inv.stock_on_hand >= 10 AND p.velocity_tier IN ('FAST', 'MEDIUM') 
            THEN 1 ELSE 0 
        END AS is_zero_sales_anomaly
    FROM raw_inventory_daily inv
    JOIN seed_products p ON inv.product_id = p.product_id
    JOIN seed_stores st ON inv.store_id = st.store_id
),
island_segmentation AS (
    SELECT 
        *,
        snapshot_date - (ROW_NUMBER() OVER (
            PARTITION BY store_id, product_id, is_zero_sales_anomaly 
            ORDER BY snapshot_date
        ) * INTERVAL '1 day') AS streak_island_group
    FROM daily_demand_baseline
),
incidents AS (
    SELECT 
        store_id,
        store_name,
        COUNT(*) AS duration_days,
        ROUND(COUNT(*) * AVG(baseline_daily_velocity), 0) AS estimated_lost_units,
        ROUND(COUNT(*) * AVG(baseline_daily_velocity) * selling_price, 0) AS estimated_lost_revenue_idr
    FROM island_segmentation
    WHERE is_zero_sales_anomaly = 1
    GROUP BY store_id, store_name, product_id, selling_price, streak_island_group
    HAVING COUNT(*) >= 3
)
SELECT 
    store_id,
    store_name,
    COUNT(*) AS total_ghost_incidents,
    SUM(duration_days) AS total_lost_shelf_days,
    SUM(estimated_lost_units) AS total_lost_units,
    SUM(estimated_lost_revenue_idr) AS total_lost_revenue_idr,
    ROUND(AVG(estimated_lost_revenue_idr), 0) AS avg_revenue_loss_per_incident
FROM incidents
GROUP BY store_id, store_name
ORDER BY total_lost_revenue_idr DESC;


-- ========================================================================================
-- KUERI 3: KATEGORI PRODUK PALING RENTAN MENGALAMI GHOST STOCKOUT
-- ========================================================================================

WITH daily_demand_baseline AS (
    SELECT 
        inv.snapshot_date,
        inv.store_id,
        inv.product_id,
        p.category,
        p.selling_price,
        inv.stock_on_hand,
        inv.units_sold_today,
        COALESCE(AVG(inv.units_sold_today) OVER (
            PARTITION BY inv.store_id, inv.product_id 
            ORDER BY inv.snapshot_date 
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ), 0.00) AS baseline_daily_velocity,
        CASE 
            WHEN inv.units_sold_today = 0 AND inv.stock_on_hand >= 10 AND p.velocity_tier IN ('FAST', 'MEDIUM') 
            THEN 1 ELSE 0 
        END AS is_zero_sales_anomaly
    FROM raw_inventory_daily inv
    JOIN seed_products p ON inv.product_id = p.product_id
),
island_segmentation AS (
    SELECT 
        *,
        snapshot_date - (ROW_NUMBER() OVER (
            PARTITION BY store_id, product_id, is_zero_sales_anomaly 
            ORDER BY snapshot_date
        ) * INTERVAL '1 day') AS streak_island_group
    FROM daily_demand_baseline
),
incidents AS (
    SELECT 
        category,
        COUNT(*) AS duration_days,
        ROUND(COUNT(*) * AVG(baseline_daily_velocity), 0) AS estimated_lost_units,
        ROUND(COUNT(*) * AVG(baseline_daily_velocity) * selling_price, 0) AS estimated_lost_revenue_idr
    FROM island_segmentation
    WHERE is_zero_sales_anomaly = 1
    GROUP BY category, product_id, selling_price, streak_island_group
    HAVING COUNT(*) >= 3
)
SELECT 
    category,
    COUNT(*) AS total_incidents,
    SUM(duration_days) AS total_anomaly_days,
    SUM(estimated_lost_units) AS total_lost_units,
    SUM(estimated_lost_revenue_idr) AS total_lost_revenue_idr,
    ROUND(SUM(estimated_lost_revenue_idr) * 100.0 / SUM(SUM(estimated_lost_revenue_idr)) OVER (), 2) AS pct_share_of_total_loss
FROM incidents
GROUP BY category
ORDER BY total_lost_revenue_idr DESC;
