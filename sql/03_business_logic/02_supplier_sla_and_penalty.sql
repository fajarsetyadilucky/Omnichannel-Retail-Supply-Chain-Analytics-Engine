-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 02_supplier_sla_and_penalty.sql
-- Module       : 03_business_logic
-- Description  : Analisis Kepatuhan Service Level Agreement (SLA) Vendor FMCG Prinsipal,
--                Rekonsiliasi Hari Keterlambatan, dan Akumulasi Piutang Denda Penalti (IDR).
-- ========================================================================================

-- ----------------------------------------------------------------------------------------
-- DEFINISI MASALAH BISNIS:
-- Keterlambatan pasokan barang dari vendor (Inbound Supply Chain) menyebabkan stok di hub
-- kosong (*stockout*) dan menurunkan kepuasan pelanggan omnichannel.
-- Dalam kontrak pengadaan B2B, terdapat klausul SLA pengiriman (Target 94% - 98%).
-- Jika vendor terlambat, ritel berhak menagihkan denda penalti harian (1.5% - 3.0% per hari)
-- dari total nilai PO.
-- Masalah riil: Seringkali departemen Finance & Procurement tidak memiliki rekonsiliasi
-- otomatis sehingga denda penalti senilai miliaran rupiah tidak tertagih (revenue leakage).
-- ----------------------------------------------------------------------------------------


-- ========================================================================================
-- KUERI 1: SCORECARD KOMPREHENSIF KINERJA VENDOR & REKONSILIASI DENDA PENALTI
-- ========================================================================================
-- Mengukur realisasi SLA vs komitmen kontrak serta menghitung denda yang harus ditagihkan.
-- ========================================================================================

WITH supplier_po_metrics AS (
    SELECT 
        po.supplier_id,
        sup.supplier_name,
        sup.category_specialty,
        sup.sla_target_pct AS contracted_sla_target,
        sup.penalty_rate_pct_per_day,
        
        -- Volume & Nilai Pengadaan
        COUNT(*) AS total_pos_issued,
        SUM(po.po_value) AS total_procurement_value_idr,
        
        -- Breakdown Status Pengiriman
        COUNT(CASE WHEN po.delivery_status = 'ON_TIME' THEN 1 END) AS on_time_deliveries,
        COUNT(CASE WHEN po.delivery_status = 'LATE' THEN 1 END) AS late_deliveries,
        COUNT(CASE WHEN po.delivery_status = 'CRITICAL_DELAY' THEN 1 END) AS critical_delay_deliveries,
        
        -- Lead Time & Keterlambatan
        ROUND(AVG(po.promised_lead_time_days), 1) AS avg_promised_lead_days,
        ROUND(AVG(po.actual_lead_time_days), 1) AS avg_actual_lead_days,
        SUM(po.delay_days) AS total_delay_days_accrued,
        
        -- Total Denda Penalti yang Dikenakan
        SUM(po.penalty_amount) AS total_penalty_receivable_idr
    FROM raw_purchase_orders po
    JOIN seed_suppliers sup ON po.supplier_id = sup.supplier_id
    GROUP BY 
        po.supplier_id, sup.supplier_name, sup.category_specialty, 
        sup.sla_target_pct, sup.penalty_rate_pct_per_day
),
scored_suppliers AS (
    SELECT 
        *,
        -- Realisasi Kepatuhan SLA Aktual (%) = (On Time POs / Total POs) * 100
        ROUND(on_time_deliveries * 100.0 / total_pos_issued, 2) AS actual_sla_pct,

        -- Gap Kepatuhan SLA = Realisasi SLA - Target Kontrak
        ROUND((on_time_deliveries * 100.0 / total_pos_issued) - contracted_sla_target, 2) AS sla_performance_gap,

        -- Rasio Denda terhadap Nilai Pengadaan (%)
        ROUND(total_penalty_receivable_idr * 100.0 / total_procurement_value_idr, 2) AS penalty_to_po_value_pct,

        -- Klasifikasi Risiko Vendor (Vendor Governance Classification)
        CASE 
            WHEN (on_time_deliveries * 100.0 / total_pos_issued) >= contracted_sla_target 
            THEN 'COMPLIANT (Meets SLA)'
            WHEN (on_time_deliveries * 100.0 / total_pos_issued) >= (contracted_sla_target - 2.50) 
            THEN 'MODERATE RISK (Minor Breach)'
            ELSE 'CRITICAL BREACH (Contract Violation)'
        END AS vendor_compliance_tier
    FROM supplier_po_metrics
)
SELECT 
    supplier_id,
    supplier_name,
    category_specialty,
    total_pos_issued,
    total_procurement_value_idr,
    contracted_sla_target,
    actual_sla_pct,
    sla_performance_gap,
    on_time_deliveries,
    late_deliveries,
    critical_delay_deliveries,
    total_delay_days_accrued,
    total_penalty_receivable_idr,
    penalty_to_po_value_pct,
    vendor_compliance_tier
FROM scored_suppliers
ORDER BY total_penalty_receivable_idr DESC;


-- ========================================================================================
-- KUERI 2: PARETO ANALYSIS VENDOR PELANGGAR SLA (TOP CONTRIBUTORS TO FINANCIAL PENALTY)
-- ========================================================================================
-- Menghitung kontribusi kumulatif denda penalti untuk memprioritaskan re-negosiasi kontrak.
-- ========================================================================================

WITH supplier_penalties AS (
    SELECT 
        po.supplier_id,
        sup.supplier_name,
        sup.category_specialty,
        COUNT(CASE WHEN po.delay_days > 0 THEN 1 END) AS delayed_po_count,
        SUM(po.delay_days) AS total_days_delayed,
        SUM(po.penalty_amount) AS total_penalty_idr
    FROM raw_purchase_orders po
    JOIN seed_suppliers sup ON po.supplier_id = sup.supplier_id
    GROUP BY po.supplier_id, sup.supplier_name, sup.category_specialty
),
pareto_ranking AS (
    SELECT 
        supplier_id,
        supplier_name,
        category_specialty,
        delayed_po_count,
        total_days_delayed,
        total_penalty_idr,
        -- Running Total Penalti Kumulatif
        SUM(total_penalty_idr) OVER (ORDER BY total_penalty_idr DESC) AS cumulative_penalty_idr,
        -- Persentase Kumulatif Penalti (% Pareto)
        ROUND(
            SUM(total_penalty_idr) OVER (ORDER BY total_penalty_idr DESC) * 100.0 / 
            SUM(total_penalty_idr) OVER (), 
            2
        ) AS cumulative_penalty_pct
    FROM supplier_penalties
)
SELECT 
    supplier_id,
    supplier_name,
    category_specialty,
    delayed_po_count,
    total_days_delayed,
    total_penalty_idr,
    cumulative_penalty_idr,
    cumulative_penalty_pct,
    CASE 
        WHEN cumulative_penalty_pct <= 80.00 THEN 'Top 80% Penalty Driver (Immediate Audit)'
        ELSE 'Long-tail Variance'
    END AS pareto_action_group
FROM pareto_ranking
ORDER BY total_penalty_idr DESC;


-- ========================================================================================
-- KUERI 3: TREN KINERJA KETEPATAN SLA BULANAN (MONTH-OVER-MONTH SLA VOLATILITY)
-- ========================================================================================
-- Memantau tren bulanan ketepatan waktu pengiriman vendor di sepanjang tahun 2024.
-- ========================================================================================

SELECT 
    DATE_TRUNC('month', po.po_date)::date AS po_month,
    COUNT(*) AS total_pos,
    SUM(po.po_value) AS monthly_po_value_idr,
    COUNT(CASE WHEN po.delivery_status = 'ON_TIME' THEN 1 END) AS on_time_pos,
    COUNT(CASE WHEN po.delivery_status != 'ON_TIME' THEN 1 END) AS delayed_pos,
    ROUND(
        COUNT(CASE WHEN po.delivery_status = 'ON_TIME' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) AS monthly_on_time_pct,
    SUM(po.delay_days) AS total_delay_days,
    SUM(po.penalty_amount) AS total_monthly_penalty_idr
FROM raw_purchase_orders po
GROUP BY DATE_TRUNC('month', po.po_date)::date
ORDER BY po_month;
