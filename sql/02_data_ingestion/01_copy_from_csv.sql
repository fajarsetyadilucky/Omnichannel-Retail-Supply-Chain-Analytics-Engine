-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 01_copy_from_csv.sql
-- Module       : 02_data_ingestion
-- Description  : Script Bulk Loading data dari 8 file CSV ke tabel PostgreSQL
--                menggunakan perintah \copy (Client-side psql) yang aman & berkinerja tinggi.
-- ========================================================================================

-- Catatan Eksekusi:
-- Perintah \copy dijalankan melalui psql dari root direktori proyek:
-- psql -U <user> -d <database> -f sql/02_data_ingestion/01_copy_from_csv.sql

\echo '----------------------------------------------------------------------'
\echo '🚀 MEMULAI PROSES BULK INGESTION DARI CSV KE POSTGRESQL'
\echo '----------------------------------------------------------------------'

-- ========================================================================================
-- LAYER 1: INGESTION MASTER SEED TABLES (URUTAN RELASI DEPENDENSI)
-- ========================================================================================

\echo '[1/8] Memuat Master Cabang Toko & Hub (seed_stores)...'
\copy seed_stores (store_id, store_name, city, district, address, store_type, sqm_capacity, manager_name, contact_phone, opened_date) FROM 'data/seed/seed_stores.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[2/8] Memuat Master Vendor Prinsipal FMCG (seed_suppliers)...'
\copy seed_suppliers (supplier_id, supplier_name, category_specialty, promised_lead_time_days, sla_target_pct, penalty_rate_pct_per_day, pic_name, contact_email, phone, city) FROM 'data/seed/seed_suppliers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[3/8] Memuat Master Katalog Produk FMCG (seed_products)...'
\copy seed_products (product_id, product_name, category, subcategory, cost_price, selling_price, supplier_id, is_perishable, velocity_tier, min_reorder_point) FROM 'data/seed/seed_products.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[4/8] Memuat Master Profil Pelanggan Jabodetabek (seed_customers)...'
\copy seed_customers (customer_id, customer_name, gender, email, phone_number, city, district, registration_date, acquisition_channel, loyalty_tier) FROM 'data/seed/seed_customers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');


-- ========================================================================================
-- LAYER 2: INGESTION TRANSACTIONAL & OPERATIONAL TABLES
-- ========================================================================================

\echo '[5/8] Memuat 100.000 Transaksi Header Pesanan (raw_orders)...'
\copy raw_orders (order_id, customer_id, order_timestamp, sales_channel, store_id, payment_method, order_status, subtotal, shipping_fee, discount_amount, total_amount, delivery_duration_minutes) FROM 'data/raw/raw_orders.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[6/8] Memuat 227.000+ Baris Keranjang Belanja (raw_order_items)...'
\copy raw_order_items (order_item_id, order_id, product_id, quantity, unit_price, unit_cost, line_total) FROM 'data/raw/raw_order_items.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[7/8] Memuat 263.520 Snapshot Inventori Harian 366 Hari Tersinkron (raw_inventory_daily)...'
\copy raw_inventory_daily (snapshot_date, store_id, product_id, stock_on_hand, stock_reserved, stock_available, units_sold_today, is_ghost_stockout) FROM 'data/raw/raw_inventory_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '[8/8] Memuat 8.000 Purchase Orders & Denda SLA (raw_purchase_orders)...'
\copy raw_purchase_orders (po_id, supplier_id, store_id, po_date, expected_delivery_date, actual_delivery_date, po_value, promised_lead_time_days, actual_lead_time_days, delay_days, delivery_status, penalty_amount) FROM 'data/raw/raw_purchase_orders.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo '----------------------------------------------------------------------'
\echo '✅ BULK INGESTION SELESAI: 8 Tabel Berhasil Dimuat Penuh!'
\echo '----------------------------------------------------------------------'
