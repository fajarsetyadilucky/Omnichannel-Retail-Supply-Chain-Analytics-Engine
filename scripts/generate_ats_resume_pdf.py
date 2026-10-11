import subprocess
import shutil
from pathlib import Path

# Paths
base_dir = Path(r"d:\BOOTCAMP BUSSINESS INTELEGENCE & DATA ANALYST\project\Portfolio Project 2 SQL\Omnichannel-Retail-Supply-Chain-Analytics-Engine")
resume_dir = base_dir / "resume"
resume_dir.mkdir(parents=True, exist_ok=True)
project_parent_dir = Path(r"d:\BOOTCAMP BUSSINESS INTELEGENCE & DATA ANALYST\project")

chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Precision CSS: Guarantees EXACTLY 2 Pages for both EN & ID with zero spillage
css_style = """
    @page {
        size: A4 portrait;
        margin: 12mm 15mm 12mm 15mm;
    }
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    body {
        font-family: 'Calibri', 'Arial', 'Helvetica', sans-serif;
        color: #111827;
        background-color: #ffffff;
        line-height: 1.4;
        font-size: 10pt;
    }
    a {
        color: #0369a1;
        text-decoration: none;
        font-weight: 600;
    }
    a:hover {
        text-decoration: underline;
    }
    .header-container {
        text-align: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .candidate-name {
        font-size: 20pt;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 3px;
    }
    .candidate-title {
        font-size: 11.5pt;
        font-weight: 600;
        color: #0369a1;
        margin-bottom: 5px;
        letter-spacing: 0.3px;
    }
    .contact-info {
        font-size: 9.3pt;
        color: #334155;
    }
    .contact-info span {
        margin: 0 4px;
        color: #94a3b8;
    }
    .section-title {
        font-size: 11pt;
        font-weight: 700;
        text-transform: uppercase;
        color: #0f172a;
        border-bottom: 1px solid #94a3b8;
        padding-bottom: 3px;
        margin-top: 14px;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    .summary-text {
        font-size: 9.8pt;
        color: #1e293b;
        text-align: justify;
        line-height: 1.44;
    }
    .skills-category {
        margin-bottom: 5px;
        font-size: 9.6pt;
        line-height: 1.4;
    }
    .skills-category strong {
        color: #0f172a;
        font-weight: 700;
    }
    .experience-item {
        margin-bottom: 8px;
    }
    .item-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2px;
    }
    .company-name {
        font-size: 10.5pt;
        font-weight: 700;
        color: #0f172a;
    }
    .date-location {
        font-size: 9.2pt;
        font-weight: 600;
        color: #475569;
        white-space: nowrap;
    }
    .job-title {
        font-size: 10pt;
        font-weight: 600;
        color: #0369a1;
        font-style: italic;
        margin-bottom: 4px;
    }
    ul.bullet-list {
        padding-left: 18px;
        margin-top: 2px;
    }
    ul.bullet-list li {
        font-size: 9.6pt;
        color: #1e293b;
        margin-bottom: 5px;
        line-height: 1.42;
        text-align: justify;
    }
    ul.bullet-list li strong {
        color: #0f172a;
    }

    /* PAGE 2 STYLES (Engineered for tight, elegant 3-project fit) */
    .page-break-projects {
        page-break-before: always;
        margin-top: 0 !important;
    }
    .project-item {
        margin-bottom: 7px;
    }
    .project-header-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 1px;
    }
    .project-title {
        font-size: 10.2pt;
        font-weight: 700;
        color: #0f172a;
    }
    .project-link-badge {
        font-size: 8.8pt;
        white-space: nowrap;
    }
    .project-tech {
        font-size: 8.9pt;
        font-weight: 600;
        color: #475569;
        margin-bottom: 2px;
    }
    ul.project-bullet-list {
        padding-left: 17px;
        margin-top: 1px;
    }
    ul.project-bullet-list li {
        font-size: 9.1pt;
        color: #1e293b;
        margin-bottom: 2.5px;
        line-height: 1.34;
        text-align: justify;
    }
    ul.project-bullet-list li strong {
        color: #0f172a;
    }
    .edu-degree {
        font-size: 9.8pt;
        font-weight: 700;
        color: #0f172a;
    }
    .edu-inst {
        font-size: 9.2pt;
        color: #334155;
    }
"""

# ==========================================
# 1. ENGLISH RESUME HTML
# ==========================================
html_en = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Fajar Setyadi - Data Analyst &amp; Business Intelligence Resume</title>
<style>{css_style}</style>
</head>
<body>

    <!-- HEADER -->
    <div class="header-container">
        <h1 class="candidate-name">FAJAR SETYADI</h1>
        <div class="candidate-title">Data Analyst | Business Intelligence Analyst</div>
        <div class="contact-info">
            Jakarta Selatan, Indonesia <span>•</span>
            <a href="tel:+6289630527099">+62 896-3052-7099</a> <span>•</span>
            <a href="mailto:fajarsetyadilucky@gmail.com">fajarsetyadilucky@gmail.com</a> <span>•</span>
            <a href="https://linkedin.com/in/fajar-setyadi">linkedin.com/in/fajar-setyadi</a> <span>•</span>
            <a href="https://github.com/fajarsetyadilucky">github.com/fajarsetyadilucky</a>
        </div>
    </div>

    <!-- PROFESSIONAL SUMMARY -->
    <div class="section-title">PROFESSIONAL SUMMARY</div>
    <p class="summary-text">
        <strong>Data Analyst &amp; Business Intelligence Analyst</strong> with <strong>5+ years of experience</strong> transforming complex fiscal and multi-channel transactional datasets into high-impact executive dashboards and automated analytical engines. Proven track record in regional government financial authority (<strong>BPKAD</strong>), consolidating multi-source budgetary records across <strong>26 regional units</strong> and optimizing fiscal reporting turnaround by <strong>75%</strong>. Technical mastery across <strong>PostgreSQL 15+</strong> (advanced SQL, declarative partitioning, composite indexing, and 98.3% query optimization), <strong>Power BI</strong> (Star Schema modeling, advanced DAX, and executive storytelling), and <strong>Python</strong> (Pandas, SciPy Monte Carlo simulation, statistical hypothesis testing). Adept at bridging technical data engineering with executive leadership strategy to identify revenue leakages, optimize unit economics, and drive data-backed decision-making.
    </p>

    <!-- CORE TECHNICAL SKILLS -->
    <div class="section-title">CORE TECHNICAL SKILLS</div>
    <div class="skills-category">
        <strong>Databases &amp; Query Engines:</strong> PostgreSQL 15+, SQL (Advanced CTEs, Window Functions, Declarative Partitioning, Composite &amp; Partial Indexing, Query Plan Optimization / EXPLAIN ANALYZE, DDL/DML, Constraints, Foreign Keys)
    </div>
    <div class="skills-category">
        <strong>Business Intelligence &amp; Modeling:</strong> Power BI (Desktop PBIP), DAX (Time Intelligence, Iterators, Custom Measures, Cumulative Aggregations), Star Schema &amp; Dimensional Modeling (Kimball), Power Query (M), Interactive Dashboards, KPI Tracking
    </div>
    <div class="skills-category">
        <strong>Programming &amp; Analytics:</strong> Python (Pandas, NumPy, SciPy, Matplotlib, Seaborn), Advanced Microsoft Excel / Google Sheets (PivotTables, XLOOKUP, Dynamic Arrays, Power Pivot), Statistical Hypothesis Testing (Z-Score, A/B Testing), Monte Carlo Simulation
    </div>
    <div class="skills-category">
        <strong>Domain &amp; Methodologies:</strong> Financial Reconciliation, Unit Economics (LTV, CAC, Payback), Margin Variance Analysis, Supply Chain &amp; Inventory Analytics, SLA Dispute Auditing, Data Governance &amp; Pipeline Automation
    </div>

    <!-- PROFESSIONAL EXPERIENCE -->
    <div class="section-title">PROFESSIONAL EXPERIENCE</div>
    <div class="experience-item">
        <div class="item-header">
            <span class="company-name">Badan Pengelola Keuangan dan Aset Daerah (BPKAD) Kabupaten Lampung Tengah</span>
            <span class="date-location">2020 – 2025</span>
        </div>
        <div class="job-title">Data &amp; Financial Reporting Analyst <span style="font-weight: normal; font-size: 8.8pt; color: #64748b;">(Regional Government Financial &amp; Asset Authority)</span></div>
        <ul class="bullet-list">
            <li><strong>Financial Data Consolidation:</strong> Consolidated, cleaned, and audited multi-source budgetary and asset valuation data across <strong>26 regional operational units (OPD)</strong>, maintaining 100% data integrity and regulatory compliance for regional budget (APBD) governance.</li>
            <li><strong>Reporting Pipeline Automation:</strong> Architected automated reporting workflows and interactive dashboards using <strong>Power BI</strong> and advanced <strong>Excel</strong>, reducing monthly reporting cycle times by <strong>75%</strong> (from 5 business days to under 4 hours) while eliminating manual data entry bottlenecks.</li>
            <li><strong>Budgetary Discrepancy Auditing:</strong> Executed forensic variance analysis and discrepancy tracking across <strong>IDR 2.8+ Trillion</strong> in annual regional budget (APBD) expenditures, identifying fiscal anomalies and safeguarding public resource allocation.</li>
            <li><strong>Data Quality &amp; Validation Frameworks:</strong> Engineered automated validation routines and multi-table reconciliation checks, driving down cross-departmental reporting errors and discrepancies by <strong>90%</strong>.</li>
            <li><strong>Executive Stakeholder Communication:</strong> Authored and presented executive fiscal summary reports to department directors and cross-functional teams, translating complex multi-table financial data into clear, actionable policy and resource allocation recommendations.</li>
        </ul>
    </div>

    <!-- PAGE 2: FEATURED PROJECTS & EDUCATION -->
    <div class="section-title page-break-projects">FEATURED ENGINEERING &amp; ANALYTICS PROJECTS</div>

    <!-- Project 1 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">1. Omnichannel Retail Supply Chain Analytics Engine</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine">[GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gmUye2pV">[LinkedIn Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Tech Stack: PostgreSQL 15+, Database Architecture, Partitioning, Composite Indexing, Query Optimization, Financial Forensics</div>
        <ul class="project-bullet-list">
            <li><strong>Database Architecture &amp; Partitioning:</strong> Engineered an enterprise relational database schema on <strong>609,769 transaction rows</strong> across 50 retail branches and 3 regional distribution centers, utilizing declarative range partitioning and relational integrity constraints.</li>
            <li><strong>Query Optimization (98.3% Latency Drop):</strong> Designed composite B-Tree indexes, partial indexes, and optimized query execution plans, slashing query latency from <strong>8,420 ms down to 140 ms (98.3% speedup)</strong> to eliminate lock contention on POS transaction servers.</li>
            <li><strong>Forensic Margin Recovery (Rp 18.3B Impact):</strong> Formulated advanced SQL models resolving critical profit leakages: mitigated <strong>Rp 5.7B</strong> lost sales via automated <em>Ghost Stockout</em> detection using Window Function <code>LAG()</code>, reconciled <strong>Rp 3.2B</strong> in overdue vendor penalties via <em>Tiered Grace-Period</em> SLA audit trails, and recovered <strong>Rp 4.9B</strong> in delivery margins by restructuring express 3-hour unit economics.</li>
            <li><strong>Customer Lifecycle Analytics:</strong> Built a 12-month cohort retention matrix identifying an 86% Month-2 drop-off, establishing a "Golden Re-engagement Window" on Days 14–21 to safeguard <strong>Rp 4.5B</strong> in customer lifetime value (LTV).</li>
        </ul>
    </div>

    <!-- Project 2 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">2. Multi-Branch Retail F&amp;B Profitability &amp; Root-Cause Optimization</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Retail-Branch-Profitability-Analysis">[GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gqEzfWWs">[LinkedIn Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Tech Stack: Power BI (Desktop PBIP), Python (Pandas, NumPy, SciPy), Statistical Z-Score Root-Cause, Executive Dashboard</div>
        <ul class="project-bullet-list">
            <li><strong>End-to-End Operational Analysis:</strong> Conducted comprehensive operational profitability audits across 18 retail restaurant branches, combining Python ETL pipelines with interactive Power BI dashboards to diagnose margin erosion across store tiers.</li>
            <li><strong>Statistical Root-Cause Modeling:</strong> Implemented statistical anomaly detection (Z-score distribution analysis) on food waste, labor cost ratios, and promo discounting, isolating the root drivers behind branch-level margin variances.</li>
            <li><strong>Power BI Enterprise Modeling (PBIP):</strong> Architected a Star Schema model with 30+ custom DAX measures for dynamic branch P&amp;L comparisons, store clustering, and SKU-level contribution margins, delivering an estimated financial impact of <strong>IDR 254M/year</strong>.</li>
        </ul>
    </div>

    <!-- Project 3 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">3. Predictive Investment Feasibility &amp; SaaS Unit Economics Modeling</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Portfolio_Feasibility_EventPhoto_SaaS">[GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gkzRp5ky">[LinkedIn Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Tech Stack: Python (SciPy Monte Carlo 1,000 Runs), Streamlit App Simulator, Power BI, SaaS Unit Economics</div>
        <ul class="project-bullet-list">
            <li><strong>SaaS Unit Economics Architecture:</strong> Formulated predictive financial and commercial models evaluating Customer Acquisition Cost (CAC), Lifetime Value (LTV), Payback Period, Net Churn, and Cash Burn rates for an event-tech SaaS platform.</li>
            <li><strong>Stochastic Risk Simulation (Monte Carlo):</strong> Developed a Python simulation engine utilizing <strong>SciPy</strong> executing <strong>1,000 Monte Carlo runs</strong>, stress-testing revenue variability and quantifying 95% confidence intervals for investor break-even timelines.</li>
            <li><strong>Dual-Layer Analytics UI:</strong> Deployed an interactive Streamlit web simulator for scenario stress-testing and an executive Power BI investment scorecard, delivering institutional-grade decision support for venture capital stakeholders.</li>
        </ul>
    </div>

    <!-- EDUCATION & CERTIFICATIONS -->
    <div class="section-title">EDUCATION &amp; CERTIFICATIONS</div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
        <div>
            <span class="edu-degree">Bachelor of Informatics Engineering (S.Kom / Teknik Informatika)</span><br>
            <span class="edu-inst">Institut Informatika &amp; Bisnis (IIB) Darmajaya, Lampung</span>
        </div>
        <div class="date-location">
            2015 – 2020
        </div>
    </div>
    <div style="font-size: 9.1pt; color: #475569; margin-bottom: 5px;">
        Relevant Coursework: Database Systems, Algorithms &amp; Data Structures, Software Engineering, Object-Oriented Programming, Statistical Analysis
    </div>

    <div style="font-size: 9.2pt; color: #1e293b; line-height: 1.35;">
        <strong>Professional Credentials:</strong> 
        Business Intelligence &amp; Data Analytics Specialist (Digital Skola) <span>•</span> 
        Advanced Excel for Business &amp; Data Analysis (Digital Skola) <span>•</span> 
        MTA: Software &amp; Application Development Fundamentals (Microsoft)
    </div>

</body>
</html>
"""

# ==========================================
# 2. INDONESIAN RESUME HTML
# ==========================================
html_id = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Fajar Setyadi - Resume Data Analyst &amp; Business Intelligence</title>
<style>{css_style}</style>
</head>
<body>

    <!-- HEADER -->
    <div class="header-container">
        <h1 class="candidate-name">FAJAR SETYADI</h1>
        <div class="candidate-title">Data Analyst | Business Intelligence Analyst</div>
        <div class="contact-info">
            Jakarta Selatan, Indonesia <span>•</span>
            <a href="tel:+6289630527099">+62 896-3052-7099</a> <span>•</span>
            <a href="mailto:fajarsetyadilucky@gmail.com">fajarsetyadilucky@gmail.com</a> <span>•</span>
            <a href="https://linkedin.com/in/fajar-setyadi">linkedin.com/in/fajar-setyadi</a> <span>•</span>
            <a href="https://github.com/fajarsetyadilucky">github.com/fajarsetyadilucky</a>
        </div>
    </div>

    <!-- RINGKASAN PROFESIONAL -->
    <div class="section-title">RINGKASAN PROFESIONAL</div>
    <p class="summary-text">
        <strong>Data Analyst &amp; Business Intelligence Analyst</strong> dengan <strong>5+ tahun pengalaman kerja profesional</strong> dalam mengolah data fiskal dan transaksional skala besar menjadi mesin analitik otomatis dan dasbor eksekutif strategis. Memiliki rekam jejak teruji pada instansi pengelola keuangan daerah (<strong>BPKAD</strong>), mengonsolidasikan data anggaran dan aset lintas <strong>26 unit kerja operasional (OPD)</strong> serta mempercepat efisiensi siklus pelaporan hingga <strong>75%</strong>. Memiliki keahlian mendalam pada <strong>PostgreSQL 15+</strong> (SQL tingkat lanjut, <em>declarative partitioning</em>, <em>composite indexing</em>, dan optimasi kueri 98,3%), <strong>Power BI</strong> (<em>Star Schema modeling</em>, formula DAX lanjutan, dan <em>executive storytelling</em>), serta <strong>Python</strong> (Pandas, simulasi Monte Carlo SciPy, dan pengujian hipotesis statistik). Terbukti piawai menjembatani rekayasa teknis database dengan strategi kepemimpinan eksekutif untuk mengidentifikasi kebocoran margin, mengoptimalkan <em>unit economics</em>, dan mendorong pengambilan keputusan berbasis data.
    </p>

    <!-- KEAHLIAN TEKNIS UTAMA -->
    <div class="section-title">KEAHLIAN TEKNIS UTAMA</div>
    <div class="skills-category">
        <strong>Database &amp; Mesin Kueri:</strong> PostgreSQL 15+, SQL (CTEs Lanjutan, Window Functions, Declarative Partitioning, Composite &amp; Partial Indexing, Optimasi Eksekusi Kueri / EXPLAIN ANALYZE, DDL/DML, Integritas Relasional &amp; Constraints)
    </div>
    <div class="skills-category">
        <strong>Business Intelligence &amp; Pemodelan:</strong> Power BI (Desktop PBIP), DAX (Time Intelligence, Iterators, Custom Measures, Cumulative Aggregations), Star Schema &amp; Dimensional Modeling (Kimball), Power Query (M), Dasbor Interaktif, Pelacakan KPI
    </div>
    <div class="skills-category">
        <strong>Pemrograman &amp; Analitika Statistik:</strong> Python (Pandas, NumPy, SciPy, Matplotlib, Seaborn), Advanced Microsoft Excel / Google Sheets (PivotTables, XLOOKUP, Dynamic Arrays, Power Pivot), Pengujian Hipotesis Statistik (Z-Score, A/B Testing), Simulasi Stokastik Monte Carlo
    </div>
    <div class="skills-category">
        <strong>Domain Bisnis &amp; Metodologi:</strong> Rekonsiliasi Finansial, Unit Economics (LTV, CAC, Payback Period), Analisis Varians Margin, Supply Chain &amp; Inventory Analytics, Audit Sengketa SLA Vendor, Tata Kelola Data &amp; Otomatisasi Alur Kerja
    </div>

    <!-- PENGALAMAN KERJA PROFESIONAL -->
    <div class="section-title">PENGALAMAN KERJA PROFESIONAL</div>
    <div class="experience-item">
        <div class="item-header">
            <span class="company-name">Badan Pengelola Keuangan dan Aset Daerah (BPKAD) Kabupaten Lampung Tengah</span>
            <span class="date-location">2020 – 2025</span>
        </div>
        <div class="job-title">Data &amp; Financial Reporting Analyst <span style="font-weight: normal; font-size: 8.8pt; color: #64748b;">(Instansi Pengelola Keuangan dan Aset Pemerintah Daerah)</span></div>
        <ul class="bullet-list">
            <li><strong>Konsolidasi Data Finansial:</strong> Mengonsolidasi, membersihkan, dan mengaudit data multi-sumber anggaran dan penilaian aset lintas <strong>26 Unit Pelaksana Daerah (OPD)</strong>, menjaga 100% integritas data dan kepatuhan regulasi tata kelola APBD.</li>
            <li><strong>Otomatisasi Alur Pelaporan:</strong> Merancang alur kerja pelaporan otomatis dan dasbor interaktif menggunakan <strong>Power BI</strong> dan <strong>Excel Lanjutan</strong>, memangkas siklus pelaporan bulanan sebesar <strong>75%</strong> (dari 5 hari kerja menjadi di bawah 4 jam) sekaligus mengeliminasi bottleneck input manual.</li>
            <li><strong>Audit Forensik Selisih Anggaran:</strong> Menjalankan analisis varians dan pelacakan diskrepansi atas realisasi belanja APBD tahunan senilai <strong>Rp 2,8+ Triliun</strong>, mengidentifikasi anomali fiskal dan mengamankan alokasi anggaran daerah.</li>
            <li><strong>Standarisasi Kualitas Data:</strong> Membangun rutinitas validasi otomatis dan rekonsiliasi data multi-tabel, menekan tingkat kesalahan dan diskrepansi pelaporan lintas instansi sebesar <strong>90%</strong>.</li>
            <li><strong>Komunikasi Pemangku Kepentingan:</strong> Menyusun dan mempresentasikan laporan ringkasan eksekutif fiskal kepada jajaran pimpinan dinas dan tim teknis, menerjemahkan data keuangan multi-tabel yang kompleks menjadi rekomendasi kebijakan dan alokasi sumber daya yang konkret.</li>
        </ul>
    </div>

    <!-- HALAMAN 2: PROYEK UNGGULAN & PENDIDIKAN -->
    <div class="section-title page-break-projects">PROYEK UNGGULAN REKAYASA DATA &amp; ANALITIKA BISNIS</div>

    <!-- Proyek 1 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">1. Omnichannel Retail Supply Chain Analytics Engine</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine">[Kode GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gmUye2pV">[Slide Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Teknologi: PostgreSQL 15+, Arsitektur Database, Partisi Tabel, Composite Indexing, Optimasi Kueri, Audit Forensik Finansial</div>
        <ul class="project-bullet-list">
            <li><strong>Arsitektur Database &amp; Partisi:</strong> Merancang skema database relasional skala korporat pada <strong>609.769 baris transaksi</strong> dari 50 gerai ritel dan 3 gudang distribusi, menerapkan <em>declarative range partitioning</em> dan integritas referensial data.</li>
            <li><strong>Optimasi Performa Kueri (Lonjakan 98,3%):</strong> Mendesain strategi <em>composite B-Tree index</em> dan <em>partial index</em>, memangkas latensi eksekusi kueri analitik dari <strong>8.420 ms menjadi 140 ms (efisiensi 98,3%)</strong> untuk meniadakan perebutan kunci memori pada database kasir POS toko.</li>
            <li><strong>Pemulihan Margin Finansial (Dampak Rp 18,3 Miliar):</strong> Merumuskan kueri SQL lanjutan untuk memetakan kebocoran laba operasional: memitigasi <strong>Rp 5,7 Miliar</strong> potensi kehilangan omzet akibat <em>Ghost Stockout</em> menggunakan Window Function <code>LAG()</code>, merekonsiliasi piutang denda keterlambatan vendor FMCG sebesar <strong>Rp 3,2 Miliar</strong> via audit trail SLA berimbang, dan memulihkan margin layanan kilat sebesar <strong>Rp 4,9 Miliar</strong> melalui kenaikan batas belanja Rp 250rb yang dipadu strategi <em>cross-selling</em>.</li>
            <li><strong>Analisis Retensi Siklus Hidup Pelanggan:</strong> Membangun matriks retensi kohort 12 bulan yang mendeteksi penurunan retensi 86% di bulan kedua, mengidentifikasi <em>Golden Re-engagement Window</em> pada hari ke-14 s/d 21 untuk mengamankan <strong>Rp 4,5 Miliar</strong> nilai <em>Customer Lifetime Value</em> (LTV).</li>
        </ul>
    </div>

    <!-- Proyek 2 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">2. Multi-Branch Retail F&amp;B Profitability &amp; Root-Cause Optimization</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Retail-Branch-Profitability-Analysis">[Kode GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gqEzfWWs">[Slide Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Teknologi: Power BI (Desktop PBIP), Python (Pandas, NumPy, SciPy), Statistik Root-Cause Z-Score, Dasbor Eksekutif</div>
        <ul class="project-bullet-list">
            <li><strong>Audit Profitabilitas Multi-Cabang:</strong> Menjalankan audit performa operasional menyeluruh pada 18 cabang restoran ritel F&amp;B, mengintegrasikan alur ETL Python dengan dasbor analitik Power BI untuk mendiagnosis erosi margin laba antar-cabang.</li>
            <li><strong>Pemodelan Akar Masalah Statistik:</strong> Menerapkan uji statistik deteksi anomali (<em>Z-score distribution analysis</em>) pada metrik <em>food waste</em>, rasio beban tenaga kerja, dan potongan diskon promo untuk mengisolasi akar pemicu penurunan laba bersih cabang.</li>
            <li><strong>Arsitektur Pemodelan Power BI (PBIP):</strong> Membangun model <em>Star Schema</em> dengan 30+ ukuran DAX dinamis untuk komparasi P&amp;L cabang, klasterisasi toko, dan kontribusi margin per SKU produk, menghasilkan estimasi pemulihan laba <strong>Rp 254 Juta per tahun</strong>.</li>
        </ul>
    </div>

    <!-- Proyek 3 -->
    <div class="project-item">
        <div class="project-header-row">
            <span class="project-title">3. Predictive Investment Feasibility &amp; SaaS Unit Economics Modeling</span>
            <span class="project-link-badge"><a href="https://github.com/fajarsetyadilucky/Portfolio_Feasibility_EventPhoto_SaaS">[Kode GitHub ↗]</a> <span>•</span> <a href="https://lnkd.in/p/gkzRp5ky">[Slide Carousel ↗]</a></span>
        </div>
        <div class="project-tech">Teknologi: Python (SciPy Monte Carlo 1.000 Iterasi), Streamlit Web App, Power BI, SaaS Unit Economics</div>
        <ul class="project-bullet-list">
            <li><strong>Arsitektur Pemodelan Finansial SaaS:</strong> Merumuskan model proyeksi komersial untuk mengevaluasi <em>Customer Acquisition Cost</em> (CAC), <em>Lifetime Value</em> (LTV), <em>Payback Period</em>, <em>Net Churn</em>, dan tingkat pembakaran kas (<em>burn rate</em>) platform SaaS event-tech.</li>
            <li><strong>Simulasi Risiko Stokastik Monte Carlo:</strong> Membangun mesin simulasi berbasis Python (<strong>SciPy</strong>) dengan <strong>1.000 iterasi Monte Carlo</strong>, menguji ketahanan variabilitas pendapatan dan mengukur selang kepercayaan 95% untuk titik impas (<em>break-even</em>) investor.</li>
            <li><strong>Antarmuka Dasbor Dua Lapisan:</strong> Mengembangkan simulator skenario web interaktif via Streamlit dan <em>scorecard</em> investasi Power BI, menyajikan instrumen pendukung keputusan risiko-pengembalian tingkat institusional bagi pemodal ventura.</li>
        </ul>
    </div>

    <!-- PENDIDIKAN & SERTIFIKASI -->
    <div class="section-title">PENDIDIKAN &amp; SERTIFIKASI</div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
        <div>
            <span class="edu-degree">Sarjana Komputer (S.Kom) — Teknik Informatika</span><br>
            <span class="edu-inst">Institut Informatika &amp; Bisnis (IIB) Darmajaya, Lampung</span>
        </div>
        <div class="date-location">
            2015 – 2020
        </div>
    </div>
    <div style="font-size: 9.1pt; color: #475569; margin-bottom: 5px;">
        Mata Kuliah Relevan: Sistem Basis Data, Algoritma &amp; Struktur Data, Rekayasa Perangkat Lunak, Pemrograman Berorientasi Objek, Analisis Statistik
    </div>

    <div style="font-size: 9.2pt; color: #1e293b; line-height: 1.35;">
        <strong>Sertifikasi Profesional:</strong> 
        Business Intelligence &amp; Data Analytics Specialist (Digital Skola) <span>•</span> 
        Advanced Excel Mastery for Business &amp; Data Analysis (Digital Skola) <span>•</span> 
        MTA: Software &amp; Application Development Fundamentals (Microsoft)
    </div>

</body>
</html>
"""

# Save HTML files
html_en_path = resume_dir / "fajar_setyadi_resume_en.html"
html_id_path = resume_dir / "fajar_setyadi_resume_id.html"

html_en_path.write_text(html_en, encoding="utf-8")
html_id_path.write_text(html_id, encoding="utf-8")
print(f"Saved: {html_en_path}")
print(f"Saved: {html_id_path}")

# PDF output paths
pdf_en_path = resume_dir / "FAJAR_SETYADI_RESUME_EN.pdf"
pdf_id_path = resume_dir / "FAJAR_SETYADI_RESUME_ID.pdf"

project_resume_dir = project_parent_dir / "Resume"
project_resume_dir.mkdir(parents=True, exist_ok=True)

parent_en_path = project_resume_dir / "Fajar_Setyadi_Resume_EN.pdf"
parent_id_path = project_resume_dir / "Fajar_Setyadi_Resume_ID.pdf"

# Render EN PDF
print("Rendering English PDF...")
subprocess.run([
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_en_path}",
    str(html_en_path)
], check=True)
shutil.copy2(pdf_en_path, parent_en_path)
shutil.copy2(html_en_path, project_resume_dir / "fajar_setyadi_resume_en.html")
if (resume_dir / "FAJAR_SETYADI_RESUME_EN.md").exists():
    shutil.copy2(resume_dir / "FAJAR_SETYADI_RESUME_EN.md", project_resume_dir / "Fajar_Setyadi_Resume_EN.md")
print(f"SUCCESS: {pdf_en_path.name} -> Copied to {parent_en_path}")

# Render ID PDF
print("Rendering Indonesian PDF...")
subprocess.run([
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_id_path}",
    str(html_id_path)
], check=True)
shutil.copy2(pdf_id_path, parent_id_path)
shutil.copy2(html_id_path, project_resume_dir / "fajar_setyadi_resume_id.html")
if (resume_dir / "FAJAR_SETYADI_RESUME_ID.md").exists():
    shutil.copy2(resume_dir / "FAJAR_SETYADI_RESUME_ID.md", project_resume_dir / "Fajar_Setyadi_Resume_ID.md")
print(f"SUCCESS: {pdf_id_path.name} -> Copied to {parent_id_path}")

print("ALL BALANCED RESUME EDITIONS GENERATED SUCCESSFULLY IN PROJECT RESUME FOLDER!")
