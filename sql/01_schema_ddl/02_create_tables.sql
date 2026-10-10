-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 02_create_tables.sql
-- Module       : 01_schema_ddl
-- Description  : Mendefinisikan DDL 8 Tabel Relasional (3NF) berskala enterprise:
--                - 4 Master Seed Tables (Stores, Suppliers, Products, Customers)
--                - 4 Transactional & Operational Tables (Orders, Order Items, Inventory, PO)
-- ========================================================================================

-- Drop tabel secara berurutan sesuai relasi Foreign Key (reverse dependency)
DROP TABLE IF EXISTS raw_order_items CASCADE;
DROP TABLE IF EXISTS raw_orders CASCADE;
DROP TABLE IF EXISTS raw_inventory_daily CASCADE;
DROP TABLE IF EXISTS raw_purchase_orders CASCADE;
DROP TABLE IF EXISTS seed_products CASCADE;
DROP TABLE IF EXISTS seed_customers CASCADE;
DROP TABLE IF EXISTS seed_suppliers CASCADE;
DROP TABLE IF EXISTS seed_stores CASCADE;


-- ========================================================================================
-- LAYER 1: MASTER SEED TABLES (ENTITAS UTAMA BISNIS)
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- 1. TABEL: seed_stores
-- ----------------------------------------------------------------------------------------
-- Menyimpan profil 12 toko fisik, flagship store, & fulfillment dark store di Jabodetabek.
CREATE TABLE seed_stores (
    store_id        VARCHAR(10)     NOT NULL,
    store_name      VARCHAR(100)    NOT NULL,
    city            VARCHAR(50)     NOT NULL,
    district        VARCHAR(50)     NOT NULL,
    address         VARCHAR(255)    NOT NULL,
    store_type      store_type_enum NOT NULL,
    sqm_capacity    INTEGER         NOT NULL,
    manager_name    VARCHAR(100)    NOT NULL,
    contact_phone   VARCHAR(25)     NOT NULL,
    opened_date     DATE            NOT NULL,

    CONSTRAINT pk_seed_stores PRIMARY KEY (store_id)
);

COMMENT ON TABLE seed_stores IS 'Data master cabang toko fisik, flagship, dan fulfillment hub ritel Jabodetabek.';
COMMENT ON COLUMN seed_stores.store_id IS 'Identifier unik cabang (contoh: STR-001).';
COMMENT ON COLUMN seed_stores.sqm_capacity IS 'Kapasitas area penyimpanan gudang dalam satuan meter persegi (sqm).';


-- ----------------------------------------------------------------------------------------
-- 2. TABEL: seed_suppliers
-- ----------------------------------------------------------------------------------------
-- Menyimpan profil 15 vendor prinsipal FMCG beserta klausul kontrak SLA & denda keterlambatan.
CREATE TABLE seed_suppliers (
    supplier_id                 VARCHAR(10)     NOT NULL,
    supplier_name               VARCHAR(150)    NOT NULL,
    category_specialty          VARCHAR(50)     NOT NULL,
    promised_lead_time_days     INTEGER         NOT NULL,
    sla_target_pct              NUMERIC(5,2)    NOT NULL,
    penalty_rate_pct_per_day    NUMERIC(4,2)    NOT NULL,
    pic_name                    VARCHAR(100)    NOT NULL,
    contact_email               VARCHAR(100)    NOT NULL,
    phone                       VARCHAR(25)     NOT NULL,
    city                        VARCHAR(50)     NOT NULL,

    CONSTRAINT pk_seed_suppliers PRIMARY KEY (supplier_id)
);

COMMENT ON TABLE seed_suppliers IS 'Master vendor FMCG dengan klausul perjanjian SLA pengiriman & rate denda penalti.';
COMMENT ON COLUMN seed_suppliers.promised_lead_time_days IS 'Komitmen batas waktu tunggu pengiriman pasokan barang (hari).';
COMMENT ON COLUMN seed_suppliers.sla_target_pct IS 'Target minimum kepatuhan SLA ketepatan waktu pengiriman vendor (%).';
COMMENT ON COLUMN seed_suppliers.penalty_rate_pct_per_day IS 'Tarif denda keterlambatan per hari dari nilai PO (%).';


-- ----------------------------------------------------------------------------------------
-- 3. TABEL: seed_products
-- ----------------------------------------------------------------------------------------
-- Menyimpan 60 SKU produk ritel FMCG lintas 6 kategori dengan HPP, Harga Jual, & Velocity.
CREATE TABLE seed_products (
    product_id          VARCHAR(10)         NOT NULL,
    product_name        VARCHAR(150)        NOT NULL,
    category            VARCHAR(50)         NOT NULL,
    subcategory         VARCHAR(50)         NOT NULL,
    cost_price          NUMERIC(12,2)       NOT NULL,
    selling_price       NUMERIC(12,2)       NOT NULL,
    supplier_id         VARCHAR(10)         NOT NULL,
    is_perishable       BOOLEAN             NOT NULL DEFAULT FALSE,
    velocity_tier       velocity_tier_enum  NOT NULL,
    min_reorder_point   INTEGER             NOT NULL,

    CONSTRAINT pk_seed_products PRIMARY KEY (product_id),
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id)
        REFERENCES seed_suppliers (supplier_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE seed_products IS 'Katalog master 60 SKU produk ritel FMCG dengan batas aman reorder dan HPP.';
COMMENT ON COLUMN seed_products.cost_price IS 'Harga Pokok Penjualan (HPP beli dari vendor supplier).';
COMMENT ON COLUMN seed_products.selling_price IS 'Harga jual eceran ritel ke konsumen akhir.';
COMMENT ON COLUMN seed_products.velocity_tier IS 'Klasifikasi perputaran produk (FAST, MEDIUM, SLOW).';
COMMENT ON COLUMN seed_products.min_reorder_point IS 'Batas minimum stok untuk menerbitkan Purchase Order baru.';


-- ----------------------------------------------------------------------------------------
-- 4. TABEL: seed_customers
-- ----------------------------------------------------------------------------------------
-- Menyimpan 10.000 profil pelanggan nyata Jabodetabek lengkap dengan gender, email, HP, & tier.
CREATE TABLE seed_customers (
    customer_id         VARCHAR(15)         NOT NULL,
    customer_name       VARCHAR(100)        NOT NULL,
    gender              gender_enum         NOT NULL,
    email               VARCHAR(120)        NOT NULL,
    phone_number        VARCHAR(20)         NOT NULL,
    city                VARCHAR(50)         NOT NULL,
    district            VARCHAR(50)         NOT NULL,
    registration_date   DATE                NOT NULL,
    acquisition_channel VARCHAR(50)         NOT NULL,
    loyalty_tier        loyalty_tier_enum   NOT NULL,

    CONSTRAINT pk_seed_customers PRIMARY KEY (customer_id),
    CONSTRAINT uq_customers_email UNIQUE (email)
);

COMMENT ON TABLE seed_customers IS 'Basis data 10.000 pelanggan Jabodetabek untuk cohort retention & customer lifetime value.';
COMMENT ON COLUMN seed_customers.registration_date IS 'Tanggal registrasi akun pelanggan (baseline analisa kohor).';
COMMENT ON COLUMN seed_customers.loyalty_tier IS 'Tingkat loyalitas pelanggan (Platinum, Gold, Silver, Bronze).';


-- ========================================================================================
-- LAYER 2: TRANSACTIONAL & OPERATIONAL TABLES (DATA RAW TRANSAKSI)
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- 5. TABEL: raw_orders
-- ----------------------------------------------------------------------------------------
-- Menyimpan 100.000 header transaksi ritel omnichannel tahun 2024.
CREATE TABLE raw_orders (
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

    CONSTRAINT pk_raw_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES seed_customers (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_orders_store FOREIGN KEY (store_id)
        REFERENCES seed_stores (store_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE raw_orders IS 'Header transaksi pesanan ritel omnichannel (App, Web, POS, Quick Commerce).';
COMMENT ON COLUMN raw_orders.order_timestamp IS 'Waktu transaksi dibuat (mengikuti kurva jam sibuk biologis manusia).';
COMMENT ON COLUMN raw_orders.delivery_duration_minutes IS 'Durasi waktu pengantaran barang ke konsumen (menit).';


-- ----------------------------------------------------------------------------------------
-- 6. TABEL: raw_order_items
-- ----------------------------------------------------------------------------------------
-- Menyimpan 228.000+ baris detail keranjang belanja setiap transaksi pesanan.
CREATE TABLE raw_order_items (
    order_item_id   BIGINT          NOT NULL,
    order_id        VARCHAR(20)     NOT NULL,
    product_id      VARCHAR(10)     NOT NULL,
    quantity        INTEGER         NOT NULL,
    unit_price      NUMERIC(12,2)   NOT NULL,
    unit_cost       NUMERIC(12,2)   NOT NULL,
    line_total      NUMERIC(14,2)   NOT NULL,

    CONSTRAINT pk_raw_order_items PRIMARY KEY (order_item_id),
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id)
        REFERENCES raw_orders (order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id)
        REFERENCES seed_products (product_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE raw_order_items IS 'Detail baris produk dalam setiap keranjang transaksi belanja.';
COMMENT ON COLUMN raw_order_items.line_total IS 'Nilai kotor baris belanja = quantity * unit_price.';


-- ----------------------------------------------------------------------------------------
-- 7. TABEL: raw_inventory_daily
-- ----------------------------------------------------------------------------------------
-- Menyimpan 108.000 snapshot stok harian per toko dan produk (injeksi anomali Ghost Stockout).
CREATE TABLE raw_inventory_daily (
    snapshot_date       DATE            NOT NULL,
    store_id            VARCHAR(10)     NOT NULL,
    product_id          VARCHAR(10)     NOT NULL,
    stock_on_hand       INTEGER         NOT NULL,
    stock_reserved      INTEGER         NOT NULL,
    stock_available     INTEGER         NOT NULL,
    units_sold_today    INTEGER         NOT NULL DEFAULT 0,
    is_ghost_stockout   BOOLEAN         NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_raw_inventory_daily PRIMARY KEY (snapshot_date, store_id, product_id),
    CONSTRAINT fk_inventory_store FOREIGN KEY (store_id)
        REFERENCES seed_stores (store_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id)
        REFERENCES seed_products (product_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE raw_inventory_daily IS 'Snapshot posisi inventori harian 180 hari untuk evaluasi Ghost Stockout.';
COMMENT ON COLUMN raw_inventory_daily.is_ghost_stockout IS 'Ground Truth Flag: Penanda stok fiktif di rak fisik (stok > 0 tapi penjualan 0).';


-- ----------------------------------------------------------------------------------------
-- 8. TABEL: raw_purchase_orders
-- ----------------------------------------------------------------------------------------
-- Menyimpan 8.000 pesanan pasokan ke vendor prinsipal FMCG dengan evaluasi denda SLA.
CREATE TABLE raw_purchase_orders (
    po_id                   VARCHAR(35)             NOT NULL,
    supplier_id             VARCHAR(10)             NOT NULL,
    store_id                VARCHAR(10)             NOT NULL,
    po_date                 DATE                    NOT NULL,
    expected_delivery_date  DATE                    NOT NULL,
    actual_delivery_date    DATE                    NOT NULL,
    po_value                NUMERIC(15,2)           NOT NULL,
    promised_lead_time_days INTEGER                 NOT NULL,
    actual_lead_time_days   INTEGER                 NOT NULL,
    delay_days              INTEGER                 NOT NULL DEFAULT 0,
    delivery_status         delivery_status_enum    NOT NULL,
    penalty_amount          NUMERIC(15,2)           NOT NULL DEFAULT 0.00,

    CONSTRAINT pk_raw_purchase_orders PRIMARY KEY (po_id),
    CONSTRAINT fk_po_supplier FOREIGN KEY (supplier_id)
        REFERENCES seed_suppliers (supplier_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_po_store FOREIGN KEY (store_id)
        REFERENCES seed_stores (store_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE raw_purchase_orders IS 'Transaksi Purchase Order ke vendor dengan kalkulasi denda penalti keterlambatan.';
COMMENT ON COLUMN raw_purchase_orders.penalty_amount IS 'Total denda penalti keterlambatan yang harus ditagih ke vendor (Rp).';
