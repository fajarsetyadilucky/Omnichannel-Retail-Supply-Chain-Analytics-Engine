-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 00_run_business_logic.sql
-- Module       : 03_business_logic
-- Description  : Master Runner untuk mengeksekusi seluruh kueri analitik bisnis & rantai pasok:
--                1. Deteksi Ghost Stockout & Estimasi Lost Sales (Gaps-and-Islands)
--                2. Scorecard Vendor SLA & Akumulasi Denda Penalti Keterlambatan
--                3. Unit Economics Kanal Omnichannel, Delivery SLA, & Revenue per SQM
-- Cara Menjalankan:
--   psql -U <username> -d <database_name> -f sql/03_business_logic/00_run_business_logic.sql
-- ========================================================================================

\timing on

\echo '--------------------------------------------------------------------------------'
-- 🚀 MEMULAI EKSEKUSI PHASE 3: CORE BUSINESS LOGIC & SUPPLY CHAIN ANALYTICS
\echo '--------------------------------------------------------------------------------'

\echo ''
\echo '[1/3] Menjalankan Analisis Ghost Stockout & Estimasi Kebocoran Omzet...'
\echo '--------------------------------------------------------------------------------'
\i sql/03_business_logic/01_ghost_stockout_detection.sql

\echo ''
\echo '[2/3] Menjalankan Scorecard Kinerja Vendor SLA & Rekonsiliasi Denda Penalti...'
\echo '--------------------------------------------------------------------------------'
\i sql/03_business_logic/02_supplier_sla_and_penalty.sql

\echo ''
\echo '[3/3] Menjalankan Analisis Omnichannel Unit Economics & Produktivitas Spasial Hub...'
\echo '--------------------------------------------------------------------------------'
\i sql/03_business_logic/03_omnichannel_unit_economics.sql

\echo ''
\echo '--------------------------------------------------------------------------------'
\echo '✅ PHASE 3 SELESAI: Seluruh Kueri Analitik Bisnis Sukses Dijalankan!'
\echo '--------------------------------------------------------------------------------'
