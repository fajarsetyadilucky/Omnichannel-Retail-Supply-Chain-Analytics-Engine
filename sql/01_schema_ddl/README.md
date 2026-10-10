# 🏗️ Module 01: Relational Schema Architecture & DDL (3NF)
## Omnichannel Retail & Supply Chain Performance Engine

**Author:** Fajar Setyadi  
**Role:** Data Analyst & Business Intelligence  
**Target Environment:** PostgreSQL 15+ Enterprise  

---

## 🎯 Gambaran Modul
Modul ini bertanggung jawab membangun pondasi arsitektur database relasional **Third Normal Form (3NF)** yang kokoh, konsisten, dan mematuhi standar integritas data level enterprise. 

Arsitektur database dibagi menjadi dua layer utama:
1. **Master Seed Layer:** Menyimpan data referensi entitas inti ritel (cabang toko/hub, vendor FMCG, katalog produk, dan profil pelanggan).
2. **Transactional & Operational Raw Layer:** Menyimpan data lalu lintas transaksi pesanan, rincian keranjang belanja, pergerakan inventori harian, serta kontrak pengadaan barang vendor (*Purchase Orders*).

---

## 📐 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    seed_suppliers ||--o{ seed_products : "supplies (1:N)"
    seed_suppliers ||--o{ raw_purchase_orders : "fulfills (1:N)"
    seed_stores ||--o{ raw_orders : "fulfills_from (1:N)"
    seed_stores ||--o{ raw_inventory_daily : "tracks_stock (1:N)"
    seed_stores ||--o{ raw_purchase_orders : "receives_at (1:N)"
    seed_customers ||--o{ raw_orders : "places (1:N)"
    raw_orders ||--|{ raw_order_items : "contains (1:N)"
    seed_products ||--o{ raw_order_items : "ordered_in (1:N)"
    seed_products ||--o{ raw_inventory_daily : "snapshotted (1:N)"

    seed_stores {
        varchar store_id PK
        varchar store_name
        varchar city
        varchar district
        varchar address
        store_type_enum store_type
        integer sqm_capacity
        varchar manager_name
        varchar contact_phone
        date opened_date
    }

    seed_suppliers {
        varchar supplier_id PK
        varchar supplier_name
        varchar category_specialty
        integer promised_lead_time_days
        numeric sla_target_pct
        numeric penalty_rate_pct_per_day
        varchar pic_name
        varchar contact_email
        varchar phone
        varchar city
    }

    seed_products {
        varchar product_id PK
        varchar product_name
        varchar category
        varchar subcategory
        numeric cost_price
        numeric selling_price
        varchar supplier_id FK
        boolean is_perishable
        velocity_tier_enum velocity_tier
        integer min_reorder_point
    }

    seed_customers {
        varchar customer_id PK
        varchar customer_name
        gender_enum gender
        varchar email UK
        varchar phone_number
        varchar city
        varchar district
        date registration_date
        varchar acquisition_channel
        loyalty_tier_enum loyalty_tier
    }

    raw_orders {
        varchar order_id PK
        varchar customer_id FK
        timestamp order_timestamp
        sales_channel_enum sales_channel
        varchar store_id FK
        varchar payment_method
        order_status_enum order_status
        numeric subtotal
        numeric shipping_fee
        numeric discount_amount
        numeric total_amount
        integer delivery_duration_minutes
    }

    raw_order_items {
        bigint order_item_id PK
        varchar order_id FK
        varchar product_id FK
        integer quantity
        numeric unit_price
        numeric unit_cost
        numeric line_total
    }

    raw_inventory_daily {
        date snapshot_date PK
        varchar store_id PK, FK
        varchar product_id PK, FK
        integer stock_on_hand
        integer stock_reserved
        integer stock_available
        integer units_sold_today
        boolean is_ghost_stockout
    }

    raw_purchase_orders {
        varchar po_id PK
        varchar supplier_id FK
        varchar store_id FK
        date po_date
        date expected_delivery_date
        date actual_delivery_date
        numeric po_value
        integer promised_lead_time_days
        integer actual_lead_time_days
        integer delay_days
        delivery_status_enum delivery_status
        numeric penalty_amount
    }
```

---

## 📂 Struktur File Script SQL

| File Script | Peran & Tanggung Jawab |
| :--- | :--- |
| [`00_run_all_ddl.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/01_schema_ddl/00_run_all_ddl.sql) | Master orchestrator psql untuk menjalankan seluruh DDL secara otomatis. |
| [`01_create_enums_and_domains.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/01_schema_ddl/01_create_enums_and_domains.sql) | Definisi tipe data kustom ENUM (`order_status`, `sales_channel`, `delivery_status`, dll). |
| [`02_create_tables.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/01_schema_ddl/02_create_tables.sql) | DDL 8 tabel relasional 3NF beserta Primary Key & Foreign Key. |
| [`03_add_constraints.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/01_schema_ddl/03_add_constraints.sql) | Business Integrity CHECK Constraints (validasi harga, stok gudang, kalkulasi total). |
| [`04_verify_schema.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/01_schema_ddl/04_verify_schema.sql) | Script diagnostik untuk mengaudit keberadaan tabel, constraints, dan tipe kolom. |

---

## 💻 Panduan Eksekusi

### Opsi A: Menggunakan PostgreSQL CLI (`psql`)
Buka terminal dan jalankan:
```bash
psql -U postgres -d omnichannel_retail_db -f sql/01_schema_ddl/00_run_all_ddl.sql
```

### Opsi B: Menggunakan GUI Client (DBeaver / pgAdmin / DataGrip)
Buka file secara berurutan dan jalankan:
1. `01_create_enums_and_domains.sql`
2. `02_create_tables.sql`
3. `03_add_constraints.sql`
4. `04_verify_schema.sql` (Verifikasi hasil)
