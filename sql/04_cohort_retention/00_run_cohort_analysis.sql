-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 00_run_cohort_analysis.sql
-- Module       : 04_cohort_retention
-- Description  : Master Runner untuk mengeksekusi seluruh rangkaian analisis kohort retensi:
--                1. Penentuan Inisiasi Kohort & Atribusi Kanal Pembelian Pertama
--                2. Rincian Granular Retensi MoM, Churn Velocity, & LTV Kumulatif
--                3. Triangular Heatmap Matrix Pivot (Persentase, Headcount, dan GMV)
-- Cara Menjalankan:
--   psql -U <username> -d <database_name> -f sql/04_cohort_retention/00_run_cohort_analysis.sql
-- ========================================================================================

\timing on

\echo '--------------------------------------------------------------------------------'
\echo '🚀 MEMULAI EKSEKUSI PHASE 4: CUSTOMER LIFECYCLE & COHORT RETENTION ENGINE'
\echo '--------------------------------------------------------------------------------'

\echo ''
\echo '[1/3] Menjalankan Penentuan Kohort Akuisisi Pertama & Atribusi Kanal...'
\echo '--------------------------------------------------------------------------------'
\i sql/04_cohort_retention/01_cohort_first_purchase.sql

\echo ''
\echo '[2/3] Menjalankan Analisis Retensi MoM, Churn Velocity, & LTV Trajectory...'
\echo '--------------------------------------------------------------------------------'
\i sql/04_cohort_retention/02_mom_retention_matrix.sql

\echo ''
\echo '[3/3] Menjalankan Triangular Heatmap Matrix Pivot (ANSI SQL Crosstab)...'
\echo '--------------------------------------------------------------------------------'
\i sql/04_cohort_retention/03_cohort_crosstab_pivot.sql

\echo ''
\echo '--------------------------------------------------------------------------------'
\echo '✅ PHASE 4 SELESAI: Analisis Kohort Retensi Berhasil Dieksekusi 100%!'
\echo '--------------------------------------------------------------------------------'
