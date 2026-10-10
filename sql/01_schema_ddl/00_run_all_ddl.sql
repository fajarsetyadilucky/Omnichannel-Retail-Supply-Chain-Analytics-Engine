-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 00_run_all_ddl.sql
-- Module       : 01_schema_ddl
-- Description  : Master Orchestrator script untuk mengeksekusi seluruh tahapan Phase 1
--                secara berurutan via psql command-line.
-- Cara Menjalankan:
--   psql -U <username> -d <database_name> -f sql/01_schema_ddl/00_run_all_ddl.sql
-- ========================================================================================

\echo '----------------------------------------------------------------------'
\echo '🚀 MEMULAI EKSEKUSI PHASE 1: RELATIONAL SCHEMA ARCHITECTURE & DDL'
\echo '----------------------------------------------------------------------'

\echo '[1/4] Membuat Custom ENUM & Domain Types...'
\i sql/01_schema_ddl/01_create_enums_and_domains.sql

\echo '[2/4] Membuat 8 Tabel Relasional (3NF) Master & Transaksional...'
\i sql/01_schema_ddl/02_create_tables.sql

\echo '[3/4] Menambahkan Business Integrity CHECK Constraints...'
\i sql/01_schema_ddl/03_add_constraints.sql

\echo '[4/4] Menjalankan Audit & Verifikasi Skema Database...'
\i sql/01_schema_ddl/04_verify_schema.sql

\echo '----------------------------------------------------------------------'
\echo '✅ PHASE 1 SELESAI: Skema Relasional 3NF Berhasil Dibangun 100%!'
\echo '----------------------------------------------------------------------'
