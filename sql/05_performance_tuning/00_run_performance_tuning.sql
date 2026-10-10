-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 00_run_performance_tuning.sql
-- Module       : 05_performance_tuning
-- Description  : Master Runner untuk mengeksekusi seluruh tahapan Database Performance Tuning:
--                1. Slow Query Profiling & Baseline Execution Plan Capture
--                2. Strategic Indexing (Composite B-Tree, Partial Index, BRIN Time-Series)
--                3. Declarative Range Table Partitioning & Partition Pruning Demonstration
--                4. Enterprise Materialized Views & Non-Blocking Concurrent Refresh
-- Cara Menjalankan:
--   psql -U <username> -d <database_name> -f sql/05_performance_tuning/00_run_performance_tuning.sql
-- ========================================================================================

\timing on

\echo '--------------------------------------------------------------------------------'
\echo '🚀 MEMULAI EKSEKUSI PHASE 5: DATABASE PERFORMANCE TUNING & BENCHMARKING'
\echo '--------------------------------------------------------------------------------'

\echo ''
\echo '[1/4] Menjalankan Profiling Slow Query Baseline (EXPLAIN ANALYZE BUFFERS)...'
\echo '--------------------------------------------------------------------------------'
\i sql/05_performance_tuning/01_slow_query_baseline.sql

\echo ''
\echo '[2/4] Menerapkan Strategi Pengindeksan (Composite, Partial, & BRIN)...'
\echo '--------------------------------------------------------------------------------'
\i sql/05_performance_tuning/02_indexing_strategy.sql

\echo ''
\echo '[3/4] Menerapkan Declarative Range Partitioning & Menguji Partition Pruning...'
\echo '--------------------------------------------------------------------------------'
\i sql/05_performance_tuning/03_table_partitioning.sql

\echo ''
\echo '[4/4] Membangun Materialized Views & Menguji REFRESH CONCURRENTLY Non-blocking...'
\echo '--------------------------------------------------------------------------------'
\i sql/05_performance_tuning/04_materialized_views.sql

\echo ''
\echo '--------------------------------------------------------------------------------'
\echo '✅ PHASE 5 SELESAI: Seluruh Optimasi Kinerja Database Telah Diterapkan 100%!'
\echo '--------------------------------------------------------------------------------'
