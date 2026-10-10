# 📚 Kamus Data (Data Dictionary) - Enterprise Grade
## Omnichannel Retail & Supply Chain Performance Engine

**Author:** Fajar Setyadi  
**Target Database:** PostgreSQL Enterprise  
**Versi Skema:** 2.0 (Hyper-Realistic Production Schema)  

---

## 📑 Daftar Entitas & Tabel

### A. Master Seed Tables (`data/seed/`)

#### 1. `seed_stores`
Menyimpan data master toko fisik dan fulfillment hub/dark store di seluruh wilayah Jabodetabek.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `store_id` | `VARCHAR(10)` | `PRIMARY KEY` | Kode unik fasilitas (contoh: `STR-001`). |
| `store_name` | `VARCHAR(100)` | `NOT NULL` | Nama resmi cabang/hub (contoh: `Hub Senayan City`). |
| `city` | `VARCHAR(50)` | `NOT NULL` | Kota administratif di Jabodetabek. |
| `district` | `VARCHAR(50)` | `NOT NULL` | Kecamatan / kawasan spesifik (contoh: `Tanah Abang / Gelora`). |
| `address` | `VARCHAR(255)` | `NOT NULL` | Alamat fisik lengkap hub/toko ritel. |
| `store_type` | `VARCHAR(50)` | `NOT NULL` | Tipe fasilitas: `Flagship Store`, `Dark Store / Fulfillment Hub`, `Express Hub`. |
| `sqm_capacity` | `INTEGER` | `CHECK (> 0)` | Luas kapasitas area penyimpanan gudang dalam meter persegi (m²). |
| `manager_name` | `VARCHAR(100)` | `NOT NULL` | Nama lengkap PIC Manager yang bertanggung jawab atas hub. |
| `contact_phone` | `VARCHAR(25)` | `NOT NULL` | Nomor telepon operasional hub. |
| `opened_date` | `DATE` | `NOT NULL` | Tanggal resmi fasilitas mulai beroperasi. |

---

#### 2. `seed_suppliers`
Menyimpan profil vendor FMCG prinsipal serta klausul perjanjian *Service Level Agreement* (SLA) pengiriman.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `supplier_id` | `VARCHAR(10)` | `PRIMARY KEY` | Kode unik vendor/supplier (contoh: `SUP-001`). |
| `supplier_name` | `VARCHAR(150)` | `NOT NULL` | Nama perseroan vendor (contoh: `PT Indofood CBP Sukses Makmur Tbk`). |
| `category_specialty` | `VARCHAR(50)` | `NOT NULL` | Kategori utama produk yang disuplai (contoh: `Packaged Food`). |
| `promised_lead_time_days` | `INTEGER` | `CHECK (>= 1)` | Komitmen waktu tunggu pengiriman barang sejak PO terbit (hari). |
| `sla_target_pct` | `NUMERIC(5,2)` | `CHECK (0-100)` | Target minimum ketepatan waktu pengiriman dalam kontrak (% SLA). |
| `penalty_rate_pct_per_day` | `NUMERIC(4,2)`| `NOT NULL` | Persentase denda keterlambatan per hari dari total nilai PO (%). |
| `pic_name` | `VARCHAR(100)` | `NOT NULL` | Nama PIC Account Manager dari pihak vendor. |
| `contact_email` | `VARCHAR(100)` | `NOT NULL` | Email korporat B2B pemesanan barang. |
| `phone` | `VARCHAR(25)` | `NOT NULL` | Nomor telepon kontak vendor. |
| `city` | `VARCHAR(50)` | `NOT NULL` | Lokasi kantor/gudang pusat vendor. |

---

#### 3. `seed_products`
Menyimpan katalog produk retail FMCG dengan struktur margin dan atribut rantai pasok.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `product_id` | `VARCHAR(10)` | `PRIMARY KEY` | Kode SKU produk (contoh: `PRD-001`). |
| `product_name` | `VARCHAR(150)` | `NOT NULL` | Nama lengkap produk dan kemasan (contoh: `Indomie Goreng Spesial 85g`). |
| `category` | `VARCHAR(50)` | `NOT NULL` | Kategori besar (Packaged Food, Beverages, Dairy, dll). |
| `subcategory` | `VARCHAR(50)` | `NOT NULL` | Subkategori produk (Instant Noodles, UHT Milk, dll). |
| `cost_price` | `NUMERIC(12,2)` | `CHECK (> 0)` | Harga Pokok Penjualan (HPP / Beli dari supplier). |
| `selling_price` | `NUMERIC(12,2)` | `CHECK (> cost)` | Harga jual ritel ke konsumen. |
| `supplier_id` | `VARCHAR(10)` | `REFERENCES seed_suppliers` | Vendor pemasok utama barang. |
| `is_perishable` | `BOOLEAN` | `DEFAULT FALSE` | Status produk rantai dingin/mudah rusak (True/False). |
| `velocity_tier` | `VARCHAR(10)` | `IN ('FAST','MEDIUM','SLOW')` | Kecepatan perputaran produk di pasar. |
| `min_reorder_point`| `INTEGER` | `NOT NULL` | Batas minimum stok untuk memicu pemesanan ulang (*safety stock*). |

---

#### 4. `seed_customers`
Menyimpan basis data pelanggan omnichannel Jabodetabek yang alami (1-3 kata, email riil, no ponsel GSM, domisili kecamatan).

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(15)` | `PRIMARY KEY` | Kode unik pelanggan (contoh: `CUST-00001`). |
| `customer_name` | `VARCHAR(100)` | `NOT NULL` | Nama lengkap pelanggan (natural 1, 2, atau 3 kata). |
| `gender` | `VARCHAR(10)` | `IN ('Male','Female')` | Jenis kelamin. |
| `email` | `VARCHAR(100)` | `UNIQUE` | Alamat email pelanggan (Gmail, Yahoo, Outlook, dll). |
| `phone_number` | `VARCHAR(20)` | `NOT NULL` | Nomor ponsel GSM Indonesia (format `0812-xxxx-xxxx`). |
| `city` | `VARCHAR(50)` | `NOT NULL` | Kota tempat tinggal di Jabodetabek. |
| `district` | `VARCHAR(50)` | `NOT NULL` | Kecamatan domisili pelanggan (contoh: `Kebayoran Baru`, `Serpong`). |
| `registration_date` | `DATE` | `NOT NULL` | Tanggal pendaftaran akun (basis penentuan kohor awal). |
| `acquisition_channel`| `VARCHAR(50)` | `NOT NULL` | Saluran pemasaran tempat pelanggan diakuisisi. |
| `loyalty_tier` | `VARCHAR(20)` | `NOT NULL` | Tingkat loyalitas: `Bronze`, `Silver`, `Gold`, `Platinum`. |

---

### B. Operational & Transactional Tables (`data/raw/`)

#### 5. `raw_orders`
Header transaksi ritel omnichannel di wilayah Jabodetabek sepanjang tahun 2024.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR(20)` | `PRIMARY KEY` | Nomor resi transaksi (contoh: `ORD-2024-000001`). |
| `customer_id` | `VARCHAR(15)` | `REFERENCES seed_customers` | ID pelanggan yang melakukan pemesanan. |
| `order_timestamp` | `TIMESTAMP` | `NOT NULL` | Waktu transaksi dibuat (mengikuti kurva jam sibuk alami). |
| `sales_channel` | `VARCHAR(50)` | `NOT NULL` | Kanal: `Mobile App`, `Website`, `In-Store POS`, `Quick Commerce Instant`. |
| `store_id` | `VARCHAR(10)` | `REFERENCES seed_stores` | Hub/toko pemenuh (*fulfillment center*). |
| `payment_method` | `VARCHAR(50)` | `NOT NULL` | Metode pembayaran (GoPay, BCA VA, Kartu Kredit, COD, dll). |
| `order_status` | `VARCHAR(20)` | `NOT NULL` | Status order: `COMPLETED`, `CANCELLED`, `RETURNED`. |
| `subtotal` | `NUMERIC(14,2)` | `CHECK (>= 0)` | Total nilai barang sebelum diskon dan ongkir. |
| `shipping_fee` | `NUMERIC(10,2)` | `DEFAULT 0` | Biaya pengantaran pesanan ke konsumen. |
| `discount_amount` | `NUMERIC(10,2)` | `DEFAULT 0` | Total potongan diskon yang diaplikasikan. |
| `total_amount` | `NUMERIC(14,2)` | `NOT NULL` | Nilai bersih yang dibayar konsumen (`subtotal + shipping - discount`). |
| `delivery_duration_minutes` | `INTEGER` | `NOT NULL` | Durasi pengiriman pesanan sampai ke tujuan (menit). |

---

#### 6. `raw_order_items`
Detail baris barang (*line items*) dari setiap transaksi order.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `order_item_id` | `BIGINT` | `PRIMARY KEY` | Nomor identitas baris item. |
| `order_id` | `VARCHAR(20)` | `REFERENCES raw_orders` | Relasi ke nomor resi pesanan. |
| `product_id` | `VARCHAR(10)` | `REFERENCES seed_products` | Relasi ke master produk. |
| `quantity` | `INTEGER` | `CHECK (> 0)` | Kuantitas unit yang dibeli. |
| `unit_price` | `NUMERIC(12,2)` | `NOT NULL` | Harga satuan saat transaksi terjadi. |
| `unit_cost` | `NUMERIC(12,2)` | `NOT NULL` | HPP satuan saat transaksi terjadi. |
| `line_total` | `NUMERIC(14,2)` | `NOT NULL` | Total harga kotor baris (`quantity * unit_price`). |

---

#### 7. `raw_inventory_daily`
Snapshot posisi inventori harian per toko dan produk untuk analisis pergerakan stok dan *Ghost Stockout*.

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `snapshot_date` | `DATE` | `NOT NULL` | Tanggal pencatatan posisi stok. |
| `store_id` | `VARCHAR(10)` | `REFERENCES seed_stores` | Lokasi toko/gudang hub. |
| `product_id` | `VARCHAR(10)` | `REFERENCES seed_products` | SKU produk yang dicatat. |
| `stock_on_hand` | `INTEGER` | `CHECK (>= 0)` | Stok fisik total yang tercatat di sistem ERP gudang. |
| `stock_reserved` | `INTEGER` | `CHECK (>= 0)` | Stok yang sedang dialokasikan untuk pesanan berjalan. |
| `stock_available` | `INTEGER` | `NOT NULL` | Stok bersih siap jual (`stock_on_hand - stock_reserved`). |
| `units_sold_today` | `INTEGER` | `DEFAULT 0` | Realisasi unit yang terjual pada tanggal tersebut. |
| `is_ghost_stockout` | `BOOLEAN` | `DEFAULT FALSE` | **Ground Truth Flag:** Penanda stok fiktif di rak (stok sistem > 0 tapi penjualan 0). |

---

#### 8. `raw_purchase_orders`
Data transaksi pemesanan pasokan barang ke vendor prinsipal (*Procurement & Inbound Supply Chain*).

| Nama Kolom | Tipe Data SQL | Constraints | Deskripsi & Kegunaan Bisnis |
| :--- | :--- | :--- | :--- |
| `po_id` | `VARCHAR(35)` | `PRIMARY KEY` | Nomor resi PO korporat (contoh: `PO-V001-20240416-0001`). |
| `supplier_id` | `VARCHAR(10)` | `REFERENCES seed_suppliers` | Vendor yang menerima PO. |
| `store_id` | `VARCHAR(10)` | `REFERENCES seed_stores` | Gudang tujuan penerimaan pasokan. |
| `po_date` | `DATE` | `NOT NULL` | Tanggal diterbitkannya PO. |
| `expected_delivery_date` | `DATE` | `NOT NULL` | Tanggal estimasi tiba sesuai janji SLA. |
| `actual_delivery_date` | `DATE` | `NOT NULL` | Tanggal kedatangan riil barang di gudang. |
| `po_value` | `NUMERIC(16,2)` | `CHECK (> 0)` | Nilai moneter PO (dalam Rupiah). |
| `promised_lead_time_days`| `INTEGER` | `NOT NULL` | Komitmen hari pengiriman vendor. |
| `actual_lead_time_days` | `INTEGER` | `NOT NULL` | Realisasi hari pengiriman (`actual - po_date`). |
| `delay_days` | `INTEGER` | `CHECK (>= 0)` | Selisih hari keterlambatan (`GREATEST(0, actual - expected)`). |
| `delivery_status` | `VARCHAR(20)` | `NOT NULL` | Status: `ON_TIME`, `LATE`, `CRITICAL_DELAY`. |
| `penalty_amount` | `NUMERIC(14,2)` | `DEFAULT 0` | Besaran denda penalti keterlambatan berdasarkan klausul kontrak. |
