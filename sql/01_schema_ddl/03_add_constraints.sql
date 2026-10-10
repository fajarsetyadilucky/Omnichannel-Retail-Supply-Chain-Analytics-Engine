-- ========================================================================================
-- 🛒 Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
-- ========================================================================================
-- Author       : Fajar Setyadi
-- Role         : Data Analyst & Business Intelligence
-- File         : 03_add_constraints.sql
-- Module       : 01_schema_ddl
-- Description  : Menambahkan Business Integrity CHECK Constraints pada 8 tabel
--                untuk menjaga validitas kalkulasi finansial, rasio SLA, & inventori.
-- ========================================================================================

-- ========================================================================================
-- 1. CONSTRAINTS PADA MASTER SEED TABLES
-- ========================================================================================

-- Tabel: seed_stores
ALTER TABLE seed_stores
    DROP CONSTRAINT IF EXISTS chk_stores_capacity,
    ADD CONSTRAINT chk_stores_capacity 
        CHECK (sqm_capacity > 0);


-- Tabel: seed_suppliers
ALTER TABLE seed_suppliers
    DROP CONSTRAINT IF EXISTS chk_suppliers_lead_time,
    DROP CONSTRAINT IF EXISTS chk_suppliers_sla_target,
    DROP CONSTRAINT IF EXISTS chk_suppliers_penalty_rate,
    ADD CONSTRAINT chk_suppliers_lead_time 
        CHECK (promised_lead_time_days >= 1),
    ADD CONSTRAINT chk_suppliers_sla_target 
        CHECK (sla_target_pct >= 0.00 AND sla_target_pct <= 100.00),
    ADD CONSTRAINT chk_suppliers_penalty_rate 
        CHECK (penalty_rate_pct_per_day >= 0.00 AND penalty_rate_pct_per_day <= 10.00);


-- Tabel: seed_products
ALTER TABLE seed_products
    DROP CONSTRAINT IF EXISTS chk_products_cost_price,
    DROP CONSTRAINT IF EXISTS chk_products_selling_price,
    DROP CONSTRAINT IF EXISTS chk_products_reorder_point,
    ADD CONSTRAINT chk_products_cost_price 
        CHECK (cost_price > 0),
    ADD CONSTRAINT chk_products_selling_price 
        CHECK (selling_price >= cost_price),
    ADD CONSTRAINT chk_products_reorder_point 
        CHECK (min_reorder_point >= 0);


-- ========================================================================================
-- 2. CONSTRAINTS PADA OPERATIONAL & TRANSACTIONAL TABLES
-- ========================================================================================

-- Tabel: raw_orders
-- Memastikan integritas kalkulasi: Total = Subtotal + Ongkir - Diskon
ALTER TABLE raw_orders
    DROP CONSTRAINT IF EXISTS chk_orders_subtotal,
    DROP CONSTRAINT IF EXISTS chk_orders_shipping_fee,
    DROP CONSTRAINT IF EXISTS chk_orders_discount_amount,
    DROP CONSTRAINT IF EXISTS chk_orders_total_calc,
    DROP CONSTRAINT IF EXISTS chk_orders_delivery_duration,
    ADD CONSTRAINT chk_orders_subtotal 
        CHECK (subtotal >= 0.00),
    ADD CONSTRAINT chk_orders_shipping_fee 
        CHECK (shipping_fee >= 0.00),
    ADD CONSTRAINT chk_orders_discount_amount 
        CHECK (discount_amount >= 0.00),
    ADD CONSTRAINT chk_orders_total_calc 
        CHECK (total_amount = (subtotal + shipping_fee - discount_amount)),
    ADD CONSTRAINT chk_orders_delivery_duration 
        CHECK (delivery_duration_minutes >= 0);


-- Tabel: raw_order_items
-- Memastikan integritas kalkulasi baris item: line_total = quantity * unit_price
ALTER TABLE raw_order_items
    DROP CONSTRAINT IF EXISTS chk_order_items_qty,
    DROP CONSTRAINT IF EXISTS chk_order_items_unit_price,
    DROP CONSTRAINT IF EXISTS chk_order_items_unit_cost,
    DROP CONSTRAINT IF EXISTS chk_order_items_line_total_calc,
    ADD CONSTRAINT chk_order_items_qty 
        CHECK (quantity > 0),
    ADD CONSTRAINT chk_order_items_unit_price 
        CHECK (unit_price > 0.00),
    ADD CONSTRAINT chk_order_items_unit_cost 
        CHECK (unit_cost > 0.00),
    ADD CONSTRAINT chk_order_items_line_total_calc 
        CHECK (line_total = (quantity * unit_price));


-- Tabel: raw_inventory_daily
-- Memastikan integritas stok gudang: stock_available = stock_on_hand - stock_reserved
ALTER TABLE raw_inventory_daily
    DROP CONSTRAINT IF EXISTS chk_inventory_on_hand,
    DROP CONSTRAINT IF EXISTS chk_inventory_reserved,
    DROP CONSTRAINT IF EXISTS chk_inventory_available_calc,
    DROP CONSTRAINT IF EXISTS chk_inventory_sold_today,
    ADD CONSTRAINT chk_inventory_on_hand 
        CHECK (stock_on_hand >= 0),
    ADD CONSTRAINT chk_inventory_reserved 
        CHECK (stock_reserved >= 0),
    ADD CONSTRAINT chk_inventory_available_calc 
        CHECK (stock_available = (stock_on_hand - stock_reserved)),
    ADD CONSTRAINT chk_inventory_sold_today 
        CHECK (units_sold_today >= 0);


-- Tabel: raw_purchase_orders
-- Memastikan integritas PO vendor: actual delivery >= po_date, delay >= 0, denda >= 0
ALTER TABLE raw_purchase_orders
    DROP CONSTRAINT IF EXISTS chk_po_dates,
    DROP CONSTRAINT IF EXISTS chk_po_value,
    DROP CONSTRAINT IF EXISTS chk_po_delay_days,
    DROP CONSTRAINT IF EXISTS chk_po_penalty_amount,
    ADD CONSTRAINT chk_po_dates 
        CHECK (actual_delivery_date >= po_date AND expected_delivery_date >= po_date),
    ADD CONSTRAINT chk_po_value 
        CHECK (po_value > 0.00),
    ADD CONSTRAINT chk_po_delay_days 
        CHECK (delay_days >= 0),
    ADD CONSTRAINT chk_po_penalty_amount 
        CHECK (penalty_amount >= 0.00);
