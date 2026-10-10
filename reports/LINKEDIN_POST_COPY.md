GMV naik 22%, tapi mengapa kas perusahaan justru bocor Rp 18,3 Miliar?

Audit forensik data transaksi ritel (50 cabang & 3 gudang) menggunakan PostgreSQL CTEs & Window Functions mengungkap The Omnichannel Paradox: di balik omzet ratusan miliar, margin bocor di 4 titik kritis.

4 Temuan Utama & Solusi Bisnis:
🔴 Ghost Stockout (Lost Sales Rp 5,7 M): Rak fisik kosong walau sistem tercatat ada ➔ Dimatangkan via Window Function LAG() (Slide 4).
🔴 Penalti SLA Vendor (Rp 3,2 M): Denda telat kirim FMCG luput ditagih ➔ Ditertibkan via skema Tiered Grace-Period (Slide 5).
🔴 Subsidi Ongkir Kilat (Minus Rp 4,9 M): Pengiriman 3 jam membakar kas ➔ Dibalikkan profit via batas belanja Rp 250rb (Slide 6).
🔴 Retention Cliff (Rp 4,5 M LTV): 86% user churn di bulan ke-2 ➔ Diselamatkan di Golden Window hari ke-14 (Slide 7).

⚡ Efisiensi Database:
Arsitektur Composite & Partial Index memangkas kecepatan query 98,3% (8,4 detik ➔ 140 milidetik), memastikan data plug-and-play tanpa membebani kasir (Slide 8).

━━━━━━━━━━━━━━━━━━━━━━━━━━━
👉 Geser 10 slide Carousel PDF di atas untuk melihat visualisasi margin waterfall, heatmap kohort, dan roadmap eksekusinya.

📂 Source Code SQL & Laporan Bisnis Lengkap di GitHub:
https://github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📬 Open for Opportunities:
Sedang mencari Data Analyst / BI Analyst yang mampu menghubungkan eksekusi SQL teknis dengan profitabilitas bisnis? Mari terhubung!

👤 Fajar Setyadi | Data Analyst & Business Intelligence
📧 Fajarsetyadilucky@gmail.com | 💬 WA: 0896-3052-7099

#DataAnalytics #BusinessIntelligence #PostgreSQL #SQL #SupplyChain #RetailAnalytics #HiringDataAnalyst
