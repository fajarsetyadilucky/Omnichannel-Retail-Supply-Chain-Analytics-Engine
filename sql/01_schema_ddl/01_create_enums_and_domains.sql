-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 01_create_enums_and_domains.sql
-- Module       : 01_schema_ddl
-- Description  : Mendefinisikan Custom Data Types (ENUMs) PostgreSQL untuk menjamin
--                integritas domain data ritel omnichannel, supply chain SLA, & status pesanan.
-- ========================================================================================

-- Pastikan eksekusi bersifat idempoten (bisa dijalankan ulang tanpa error)
DROP TYPE IF EXISTS order_status_enum CASCADE;
DROP TYPE IF EXISTS sales_channel_enum CASCADE;
DROP TYPE IF EXISTS delivery_status_enum CASCADE;
DROP TYPE IF EXISTS loyalty_tier_enum CASCADE;
DROP TYPE IF EXISTS velocity_tier_enum CASCADE;
DROP TYPE IF EXISTS store_type_enum CASCADE;
DROP TYPE IF EXISTS gender_enum CASCADE;

-- ----------------------------------------------------------------------------------------
-- 1. ENUM: STATUS PESANAN (ORDER LIFECYCLE)
-- ----------------------------------------------------------------------------------------
-- Mendefinisikan status transaksi ritel omnichannel:
-- - COMPLETED : Transaksi berhasil, barang diterima oleh pelanggan.
-- - CANCELLED : Pesanan dibatalkan sebelum pengiriman / gagal bayar.
-- - RETURNED  : Barang dikembalikan pelanggan (retur logistik).
CREATE TYPE order_status_enum AS ENUM (
    'COMPLETED',
    'CANCELLED',
    'RETURNED'
);
COMMENT ON TYPE order_status_enum IS 'Status siklus hidup transaksi pelanggan ritel omnichannel.';

-- ----------------------------------------------------------------------------------------
-- 2. ENUM: KANAL PENJUALAN OMNICHANNEL (SALES CHANNELS)
-- ----------------------------------------------------------------------------------------
-- Mendefinisikan 4 touchpoint belanja omnichannel modern:
-- - Mobile App             : Belanja via aplikasi native Android/iOS (termasuk kurir ekspedisi).
-- - Website                : Belanja via web e-commerce desktop/mobile browser.
-- - In-Store POS           : Transaksi langsung di kasir toko fisik/flagship store.
-- - Quick Commerce Instant : Layanan belanja cepat instan sampai dalam 15-45 menit.
CREATE TYPE sales_channel_enum AS ENUM (
    'Mobile App',
    'Website',
    'In-Store POS',
    'Quick Commerce Instant'
);
COMMENT ON TYPE sales_channel_enum IS 'Kanal penjualan omnichannel tempat transaksi diinisiasi.';

-- ----------------------------------------------------------------------------------------
-- 3. ENUM: STATUS KETEPATAN SLA PENGIRIMAN VENDOR (SUPPLY CHAIN SLA)
-- ----------------------------------------------------------------------------------------
-- Mengukur kinerja pengiriman Purchase Order (PO) dari vendor prinsipal FMCG:
-- - ON_TIME        : Tiba tepat waktu atau lebih awal dari promised lead time.
-- - LATE           : Terlambat wajar (1-3 hari kerja), dikenakan denda penalti standar.
-- - CRITICAL_DELAY : Terlambat berat (> 3 hari), membahayakan kontinuitas stok hub.
CREATE TYPE delivery_status_enum AS ENUM (
    'ON_TIME',
    'LATE',
    'CRITICAL_DELAY'
);
COMMENT ON TYPE delivery_status_enum IS 'Status evaluasi ketepatan pengiriman supplier terhadap janji SLA.';

-- ----------------------------------------------------------------------------------------
-- 4. ENUM: TIER LOYALITAS PELANGGAN (CRM LOYALTY TIERS)
-- ----------------------------------------------------------------------------------------
-- Segmentasi pelanggan berbasis Power-Law / Pareto aktivitas belanja:
-- - Platinum : Pelanggan VIP Whale dengan frekuensi belanja tertinggi.
-- - Gold     : Pelanggan loyal aktif belanja berkala.
-- - Silver   : Pelanggan reguler dengan frekuensi belanja moderat.
-- - Bronze   : Pelanggan baru atau pembeli sporadis / one-time.
CREATE TYPE loyalty_tier_enum AS ENUM (
    'Platinum',
    'Gold',
    'Silver',
    'Bronze'
);
COMMENT ON TYPE loyalty_tier_enum IS 'Tingkat loyalitas pelanggan untuk analisis kohor dan segmentasi LTV.';

-- ----------------------------------------------------------------------------------------
-- 5. ENUM: KECEPATAN PERPUTARAN BARANG (INVENTORY VELOCITY TIER)
-- ----------------------------------------------------------------------------------------
-- Klasifikasi perputaran inventori FMCG untuk mitigasi Ghost Stockout:
-- - FAST   : Fast-Moving Consumer Goods (perputaran harian tinggi, misal: Mie, Susu, Air Mineral).
-- - MEDIUM : Perputaran menengah (misal: Sabun Mandi, Biskuit, Bumbu Dapur).
-- - SLOW   : Perputaran lambat (misal: Pembersih Lantai kemasan besar, Gula Stevia).
CREATE TYPE velocity_tier_enum AS ENUM (
    'FAST',
    'MEDIUM',
    'SLOW'
);
COMMENT ON TYPE velocity_tier_enum IS 'Klasifikasi laju perputaran SKU barang di gudang dan rak toko.';

-- ----------------------------------------------------------------------------------------
-- 6. ENUM: TIPE FASILITAS TOKO & HUB (STORE & FULFILLMENT TYPES)
-- ----------------------------------------------------------------------------------------
CREATE TYPE store_type_enum AS ENUM (
    'Flagship Store',
    'Dark Store / Fulfillment Hub',
    'Express Hub'
);
COMMENT ON TYPE store_type_enum IS 'Format fasilitas toko fisik dan hub logistik ritel.';

-- ----------------------------------------------------------------------------------------
-- 7. ENUM: DEMOGRAFI GENDER
-- ----------------------------------------------------------------------------------------
CREATE TYPE gender_enum AS ENUM (
    'Male',
    'Female'
);
COMMENT ON TYPE gender_enum IS 'Jenis kelamin pelanggan untuk analisis demografi preferensi produk.';
