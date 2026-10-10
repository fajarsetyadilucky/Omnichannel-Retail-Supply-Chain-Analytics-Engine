# 📐 Entity Relationship Diagram (ERD) & Relational Architecture
## Omnichannel Retail & Supply Chain Performance Engine

**Author:** Fajar Setyadi  
**Role:** Data Analyst & Business Intelligence  
**Environment:** PostgreSQL 15+ Enterprise Edition  
**Schema Normalization:** Strict Third Normal Form (3NF)  

---

## 🏛️ Skema Visual Mermaid ERD (8 Relational Tables)

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
        product_category_enum category
        varchar sub_category
        numeric cost_price
        numeric base_price
        boolean is_perishable
        varchar supplier_id FK
        velocity_class_enum velocity_class
    }

    seed_customers {
        varchar customer_id PK
        varchar customer_name
        varchar email UK
        varchar phone_number
        varchar city
        varchar district
        channel_enum acquisition_channel
        timestamp registration_timestamp
    }

    raw_orders {
        varchar order_id PK
        varchar customer_id FK
        varchar store_id FK
        channel_enum channel
        order_status_enum order_status
        timestamp order_timestamp
        numeric subtotal
        numeric discount_amount
        numeric delivery_fee
        numeric total_amount
        payment_method_enum payment_method
        integer delivery_time_minutes
    }

    raw_order_items {
        varchar item_id PK
        varchar order_id FK
        varchar product_id FK
        integer quantity
        numeric unit_price
        numeric unit_cost
        numeric subtotal_amount
    }

    raw_inventory_daily {
        varchar snapshot_id PK
        date snapshot_date
        varchar store_id FK
        varchar product_id FK
        integer stock_on_hand
        integer safety_stock_level
        integer units_received
        integer units_sold
        boolean is_stockout_flagged
    }

    raw_purchase_orders {
        varchar po_id PK
        varchar supplier_id FK
        varchar destination_store_id FK
        timestamp po_timestamp
        date expected_delivery_date
        date actual_delivery_date
        po_status_enum po_status
        numeric total_po_value
        numeric penalty_fee_charged
    }
```

---

## 🔗 Matriks Relasi Antar Tabel (Relational Integrity Matrix)

| Primary Table (1) | Foreign Key Table (N) | Foreign Key Column | Constraint & Cascade Rule | Deskripsi Relasi Bisnis |
| :--- | :--- | :--- | :--- | :--- |
| `seed_suppliers` | `seed_products` | `supplier_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu vendor memasok banyak SKU produk. |
| `seed_suppliers` | `raw_purchase_orders` | `supplier_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu vendor menerima banyak pesanan pengadaan B2B (PO). |
| `seed_stores` | `raw_orders` | `store_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu toko/hub melayani banyak pesanan online dan offline. |
| `seed_stores` | `raw_inventory_daily` | `store_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu toko memiliki log rekam stok harian per produk. |
| `seed_stores` | `raw_purchase_orders` | `destination_store_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu toko menjadi tujuan pengantaran barang dari vendor. |
| `seed_customers` | `raw_orders` | `customer_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu pelanggan dapat bertransaksi berulang kali (*Repeat Orders*). |
| `raw_orders` | `raw_order_items` | `order_id` | `ON UPDATE CASCADE ON DELETE CASCADE` | Satu nota pesanan berisi 1 atau lebih varian item barang (*Cart Line Items*). |
| `seed_products` | `raw_order_items` | `product_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu produk dapat dibeli di banyak transaksi berbeda. |
| `seed_products` | `raw_inventory_daily` | `product_id` | `ON UPDATE CASCADE ON DELETE RESTRICT` | Satu produk dicatat posisi stoknya setiap hari di setiap toko. |

---

## 🛡️ Aturan Integritas Relasional & Constraints
* **Natural/Business Primary Keys:** Semua tabel menggunakan ID terstruktur yang bermakna (`STR-xxx`, `SUP-xxx`, `PRD-xxx`, `CUST-xxx`, `ORD-xxx`, `ITM-xxx`, `INV-xxx`, `PO-xxx`).
* **Foreign Key Constraints:** Menjamin *Zero Orphan Records* pada seluruh 609.769 baris data.
* **Positive Financial Constraints:** Validasi `CHECK (cost_price > 0)`, `CHECK (quantity > 0)`, dan `CHECK (total_amount >= 0)` untuk menjamin realisme finansial.
