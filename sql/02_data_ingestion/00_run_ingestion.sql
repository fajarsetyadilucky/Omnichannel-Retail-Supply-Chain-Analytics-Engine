-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 00_run_ingestion.sql
-- Module       : 02_data_ingestion
-- Description  : Master Runner untuk mengeksekusi Bulk Data Ingestion dan
--                menjalankan rangkaian pengujian Data Quality & Reconciliation di Phase 2.
-- Cara Menjalankan:
--   psql -U <username> -d <database_name> -f sql/02_data_ingestion/00_run_ingestion.sql
-- ========================================================================================

\echo '----------------------------------------------------------------------'
\echo '🚀 MEMULAI EKSEKUSI PHASE 2: BULK DATA INGESTION & QUALITY RECONCILIATION'
\echo '----------------------------------------------------------------------'

\echo '[1/2] Menjalankan Bulk Data Loading dari CSV ke 8 Tabel Relasional...'
\i sql/02_data_ingestion/01_copy_from_csv.sql

\echo '[2/2] Menjalankan Pengujian Integritas, Rekonsiliasi, & Storage Footprint...'
\i sql/02_data_ingestion/02_validate_ingestion.sql

\echo '----------------------------------------------------------------------'
\echo '✅ PHASE 2 SELESAI: Seluruh Data Telah Termuat & Terverifikasi 100%!'
\echo '----------------------------------------------------------------------'
