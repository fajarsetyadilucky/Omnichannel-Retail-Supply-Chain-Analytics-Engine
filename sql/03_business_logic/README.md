# 🧠 Module 03: Core Business Logic & Omnichannel Supply Chain Analytics
## Omnichannel Retail & Supply Chain Performance Engine

**Author:** Fajar Setyadi  
**Role:** Data Analyst & Business Intelligence  
**Target Environment:** PostgreSQL 15+ Enterprise  

---

## 🎯 Gambaran Modul

Modul ini adalah **inti analitik (*analytical powerhouse*)** dari portofolio Omnichannel Retail & Supply Chain Engine. Di sini, data granular operasional (100.000 pesanan, 228.177 detail item, 263.520 log inventori harian, dan 8.000 pesanan pengadaan B2B) ditransformasikan menjadi kecerdasan bisnis (*actionable business intelligence*) tingkat manajemen melalui formulasi SQL tingkat lanjut.

Modul ini berfokus pada 3 pilar masalah bisnis utama di industri ritel modern:
1. **Deteksi Kebocoran Stok Siluman (*Ghost Stockout Detection*)**: Mengidentifikasi stok fiktif di rak menggunakan teknik *Gaps-and-Islands* dan menghitung kerugian omzet (*lost sales opportunity*).
2. **Tata Kelola SLA Vendor & Rekonsiliasi Denda Penalti (*Supplier SLA & Penalty Receivables*)**: Mengukur kepatuhan kontrak prinsipal FMCG dan mengekstraksi hak piutang denda keterlambatan pengiriman.
3. **Ekonomi Unit Lintas Kanal (*Omnichannel Unit Economics*) & Produktivitas Spasial**: Membedah margin kontribusi riil per kanal belanja, efisiensi throughput per meter persegi gudang (*Revenue per SQM*), serta kepatuhan garansi pengantaran instan 30 menit.

---

## 📂 Struktur File Script SQL

| File Script | Peran & Tanggung Jawab Analitik |
| :--- | :--- |
| [`00_run_business_logic.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/03_business_logic/00_run_business_logic.sql) | Master runner psql untuk mengeksekusi ketiga rangkaian kueri analitik secara berurutan. |
| [`01_ghost_stockout_detection.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/03_business_logic/01_ghost_stockout_detection.sql) | Algoritma *Gaps-and-Islands*, moving average 14 hari, agregasi kebocoran per cabang toko dan kategori produk. |
| [`02_supplier_sla_and_penalty.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/03_business_logic/02_supplier_sla_and_penalty.sql) | Vendor SLA Scorecard, klasifikasi risiko kontrak, Pareto ranking 80/20 denda finansial, dan tren bulanan. |
| [`03_omnichannel_unit_economics.sql`](file:///d:/BOOTCAMP%20BUSSINESS%20INTELEGENCE%20&%20DATA%20ANALYST/project/Portfolio%20Project%202%20SQL/Omnichannel-Retail-Supply-Chain-Analytics-Engine/sql/03_business_logic/03_omnichannel_unit_economics.sql) | Net Contribution Margin, diskon & ongkir, Revenue / SQM per hub, serta analisis persentil SLA pengiriman instan. |

---

## 🔬 Metodologi, Formulasi Matematis, & Bedah Kueri

### 1. Deteksi Ghost Stockout & Estimasi Lost Sales (`01_ghost_stockout_detection.sql`)

#### Definisi Masalah:
Stok buku pada sistem komputer ERP mencatat barang tersedia ($\text{Stock on Hand} \ge 10$ unit), namun secara fisik di rak barang tersebut raib, salah penempatan, rusak, atau dicuri (*shrinkage*). Akibatnya, pada produk fast-moving terjadi kekosongan penjualan ($\text{Units Sold} = 0$) selama berhari-hari berturut-turut.

#### Algoritma SQL & Formulasi Matematis:
1. **Baseline Permintaan Normal (Moving Window):**
   $$\text{Baseline Velocity}_{s, p, t} = \frac{1}{14} \sum_{i=1}^{14} \text{Units Sold}_{s, p, t-i}$$
   Dihitung dengan klausa: `AVG(inv.units_sold_today) OVER (PARTITION BY store_id, product_id ORDER BY snapshot_date ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING)`.
2. **Flag Anomali Bisnis:**
   $$\text{Anomaly} = 1 \iff (\text{Units Sold} = 0) \land (\text{Stock on Hand} \ge 10) \land (\text{Velocity Tier} \in \{\text{'FAST'}, \text{'MEDIUM'}\})$$
3. **Pengelompokan Hari Beruntun (Gaps-and-Islands):**
   $$\text{Island Group} = \text{snapshot\_date} - (\text{ROW\_NUMBER}() \times 1\text{ hari})$$
   Jika tanggal berurutan dan status anomali bernilai sama, selisih tanggal dengan deret integer menghasilkan nilai anchor date yang konstan.
4. **Estimasi Kerugian Omzet Penjualan (Lost Revenue):**
   $$\text{Estimated Lost Revenue} = \text{Durasi Hari} \times \text{Baseline Velocity} \times \text{Harga Jual SKU}$$
   Ambang batas enterprise yang diselidiki adalah insiden dengan $\text{Durasi Hari} \ge 3$ hari berturut-turut.

---

### 2. Kinerja SLA Vendor & Piutang Denda Penalti (`02_supplier_sla_and_penalty.sql`)

#### Definisi Masalah:
Keterlambatan pasokan barang dari prinsipal (*Inbound Inefficiency*) memicu *stockout* di jaringan gerai ritel. Kontrak B2B mengatur SLA kedatangan (94% – 98%) dengan klausul denda penalti harian (1.5% – 3.0% per hari keterlambatan) dari nilai Purchase Order (PO). Seringkali denda ini luput ditagih oleh Finance karena ketiadaan audit otomatis.

#### Algoritma SQL & Formulasi Matematis:
1. **Realisasi Kepatuhan SLA (%):**
   $$\text{Actual SLA \%} = \frac{\sum \text{On-Time POs}}{\sum \text{Total POs Issued}} \times 100$$
2. **Kalkulasi Denda Penalti Harian:**
   $$\text{Penalty Amount} = \text{Delay Days} \times \text{Penalty Rate \%} \times \text{PO Value}$$
3. **Analisis Pareto 80/20 Denda Finansial:**
   Menggunakan window function `SUM(...) OVER (ORDER BY penalty DESC)` untuk menemukan kelompok vendor kecil yang menyumbang 80% kebocoran penalti finansial terbesar.

---

### 3. Omnichannel Unit Economics & Produktivitas Spasial Hub (`03_omnichannel_unit_economics.sql`)

#### Definisi Masalah:
Ekspansi ke kanal digital (Mobile App, Web, Quick Commerce Instant) kerap kali menurunkan margin laba akibat subsidi ongkir dan promosi diskon. Kueri ini mengukur apakah setiap pesanan digital memberikan kontribusi laba bersih positif dan seberapa efisien pemanfaatan fisik ruang toko per meter persegi.

#### Formulasi Laba Kontribusi Bersih (Net Contribution Margin):
$$\text{Gross Profit} = \sum (\text{Line Total}) - \sum (\text{Qty} \times \text{Unit Cost})$$
$$\text{Net Contribution Margin} = \text{Gross Profit} + \text{Shipping Fee Collected} - \text{Discount Amount}$$
$$\text{Net Contribution Margin \%} = \frac{\text{Net Contribution Margin}}{\text{Total Net Sales (GMV)}} \times 100$$

#### Produktivitas Spasial Ritel (Spatial Efficiency):
$$\text{Revenue per SQM} = \frac{\text{Total Completed Revenue (IDR)}}{\text{Store SQM Capacity}}$$
$$\text{Throughput per SQM} = \frac{\text{Total Completed Orders}}{\text{Store SQM Capacity}}$$

#### Pengukuran SLA Pengantaran Instan:
Menggunakan fungsi persentil kontinu PostgreSQL:
- `PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY delivery_duration_minutes)` (Median)
- `PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY delivery_duration_minutes)` (P95 Tail Latency)

---

## 📈 Rangkuman Temuan Eksekutif (Empirical Findings dari 609.769 Baris Data)

Berdasarkan pengujian terhadap dataset riil tahun penuh 2024:

### 1. Temuan Ghost Stockout
- **Total Kebocoran Omzet Ritel:** **Rp 2.216.373.573 (~ Rp 2,22 Miliar)** hilang di seluruh jaringan dari 14.514 insiden rak macet (total 117.617 hari rak anomali).
- **Kategori Paling Terdampak:** **Fresh Produce (29,23% / Rp 647,87 Juta)** dan **Personal Care (19,10% / Rp 423,40 Juta)** menyumbang hampir 50% dari total kerugian nasional akibat sensitivitas kerusakan fisik dan susut barang (*spoilage/shrinkage*).
- **Cabang Paling Rawan:** Hub logistik besar (*Cakung Mega Distribution Hub* & *Bekasi Retail Hub*) menampung kerugian rupiah terbesar karena volume unit stok di rak yang sangat masif.

### 2. Temuan Inbound Vendor SLA & Piutang Denda
- **Total Nilai Pengadaan (PO):** **Rp 113.879.400.000 (~ Rp 113,88 Miliar)** di sepanjang 366 hari tahun 2024.
- **Akumulasi Piutang Denda Keterlambatan:** **Rp 1.316.149.000 (~ Rp 1,316 Miliar)** dari total 1.153 hari keterlambatan kumulatif yang sah ditagihkan ke pihak vendor FMCG.
- **Pareto Drivers (80/20 Rule):** 5 Vendor teratas menyumbang porsi denda terbesar:
  1. *PT Wings Surya (Wings Group)*: Rp 132,69 Juta (124 hari terlambat)
  2. *PT Unilever Indonesia Tbk*: Rp 121,44 Juta (96 hari terlambat)
  3. *PT Orang Tua Group (OT)*: Rp 108,03 Juta (106 hari terlambat)
  4. *PT Garudafood Putra Putri Jaya Tbk*: Rp 105,69 Juta (96 hari terlambat)
  5. *PT Mayora Indah Tbk*: Rp 104,85 Juta (96 hari terlambat)

### 3. Temuan Unit Economics & Throughput Hub
- **Volume Kanal Belanja:** **Mobile App** mendominasi dengan 51.689 pesanan (AOV Rp 90.136), disusul **In-Store POS** 18.647 pesanan (AOV Rp 80.525), **Website** 14.251 pesanan, dan **Quick Commerce Instant** 9.482 pesanan.
- **Gross Profit Margin:** Relatif seragam di angka **23,23% – 23,25%**, membuktikan konsistensi penetapan harga katalog produk lintas kanal.
- **SLA Pengantaran 30 Menit:** 82% – 88% pesanan instan berhasil tiba di bawah 30 menit, dengan Median waktu antar berkisar antara 23 – 25 menit.
- **Throughput Spasial Tertinggi:** Format *Dark Store* (misal: *Jakarta Selatan Dark Store*) mencetak efisiensi omzet per meter persegi tertinggi (**Rp 31,8 Juta / m²**), membuktikan densitas modal yang jauh lebih efisien dibandingkan format hypermarket konvensional.

---

## 🚀 Panduan Menjalankan Script

Jalankan master runner via psql terminal:

```bash
# Jalankan seluruh Phase 3 secara otomatis
psql -U postgres -d omnichannel_retail_db -f sql/03_business_logic/00_run_business_logic.sql
```

Atau jalankan kueri individual untuk analisis interaktif:
```bash
psql -U postgres -d omnichannel_retail_db -f sql/03_business_logic/01_ghost_stockout_detection.sql
psql -U postgres -d omnichannel_retail_db -f sql/03_business_logic/02_supplier_sla_and_penalty.sql
psql -U postgres -d omnichannel_retail_db -f sql/03_business_logic/03_omnichannel_unit_economics.sql
```
