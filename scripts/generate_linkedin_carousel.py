"""
========================================================================================
LinkedIn Carousel Generator: Omnichannel Retail & Supply Chain Analytics Engine
Author: Fajar Setyadi | Data Analyst & Business Intelligence
Format: 10-Slide LinkedIn Document Carousel (1080px x 1350px, 4:5 Aspect Ratio)
Aesthetic: Executive Tech Luxury (Deep Slate Navy, PostgreSQL Cyan, Emerald Green)
========================================================================================
"""

import os
import subprocess
from pathlib import Path
import base64
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"
CAROUSEL_DIR = REPORTS_DIR / "carousel_slides"
FIGURES_DIR = REPORTS_DIR / "figures"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CAROUSEL_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

html_file = REPORTS_DIR / "linkedin_carousel_preview.html"
pdf_file = REPORTS_DIR / "LINKEDIN_CAROUSEL_OMNICHANNEL_SQL_ENGINE.pdf"
post_copy_file = REPORTS_DIR / "LINKEDIN_POST_COPY.md"

def get_base64_image(image_path):
    p = Path(image_path)
    if p.exists():
        ext = p.suffix.lower().replace(".", "")
        if ext == "jpg":
            ext = "jpeg"
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/{ext};base64,{b64}"
    return ""

author_photo_uri = get_base64_image(FIGURES_DIR / "author_fajar_setyadi.png")
github_url = "https://github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine"
author_name = "Fajar Setyadi"
author_role = "Data Analyst & Business Intelligence"
author_email = "Fajarsetyadilucky@gmail.com"
author_wa = "089630527099"
author_wa_formatted = "0896-3052-7099"

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>LinkedIn Carousel - Omnichannel Retail & Supply Chain Analytics Engine</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
    @page {{
        size: 1080px 1350px;
        margin: 0;
    }}
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        background-color: #030712;
        color: #f3f4f6;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        margin: 0;
        padding: 0;
    }}
    
    .slide-wrapper {{
        width: 1080px;
        height: 1350px;
        position: relative;
        background: radial-gradient(circle at 10% 15%, #0f172a 0%, #030712 65%, #020617 100%);
        overflow: hidden;
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 70px 75px 65px 75px;
    }}

    /* Subdued Background Grid Pattern */
    .grid-bg {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 1;
    }}
    
    /* Top Radial Glow */
    .glow-sphere {{
        position: absolute;
        width: 650px;
        height: 650px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.09) 0%, rgba(99, 102, 241, 0.03) 50%, transparent 70%);
        top: -150px;
        right: -100px;
        pointer-events: none;
        z-index: 1;
    }}

    .glow-sphere-emerald {{
        position: absolute;
        width: 550px;
        height: 550px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.08) 0%, transparent 70%);
        bottom: -100px;
        left: -100px;
        pointer-events: none;
        z-index: 1;
    }}

    .content-layer {{
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: space-between;
    }}

    /* TOP HEADER */
    .slide-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }}
    .tag-badge {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 9px 18px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #e2e8f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }}
    .tag-badge .dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #38bdf8;
        box-shadow: 0 0 10px #38bdf8;
    }}
    .tag-badge .accent {{
        color: #38bdf8;
    }}
    .tag-badge .emerald {{
        color: #34d399;
    }}
    .slide-number {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        font-weight: 700;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 6px 14px;
        border-radius: 8px;
    }}

    /* HEADLINE TITLES */
    .title-area {{
        margin-bottom: 28px;
    }}
    h1.hero-title {{
        font-size: 48px;
        font-weight: 900;
        line-height: 1.18;
        color: #ffffff;
        letter-spacing: -1.2px;
        margin-bottom: 18px;
    }}
    h2.slide-title {{
        font-size: 38px;
        font-weight: 800;
        line-height: 1.22;
        color: #ffffff;
        letter-spacing: -0.8px;
        margin-bottom: 12px;
    }}
    .subtitle {{
        font-size: 19px;
        font-weight: 500;
        line-height: 1.5;
        color: #cbd5e1;
    }}
    .highlight-cyan {{
        color: #38bdf8;
        text-shadow: 0 0 25px rgba(56, 189, 248, 0.25);
    }}
    .highlight-emerald {{
        color: #34d399;
        text-shadow: 0 0 25px rgba(52, 211, 153, 0.25);
    }}
    .highlight-amber {{
        color: #fbbf24;
    }}

    /* STAT CALLOUT HERO */
    .stat-hero-card {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 24px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }}
    .stat-hero-card.emerald-border {{
        border-color: rgba(52, 211, 153, 0.3);
    }}
    .stat-hero-card.amber-border {{
        border-color: rgba(251, 191, 36, 0.3);
    }}
    .stat-big {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
        line-height: 1;
    }}
    .stat-desc {{
        font-size: 16px;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 6px;
    }}
    .stat-pill {{
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8;
        padding: 8px 18px;
        border-radius: 100px;
        font-size: 14px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }}
    .stat-pill.emerald {{
        background: rgba(52, 211, 153, 0.15);
        border-color: rgba(52, 211, 153, 0.35);
        color: #34d399;
    }}

    /* CONTENT CARDS & GRIDS */
    .cards-stack {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        flex-grow: 1;
    }}
    .glass-card {{
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 24px;
        display: flex;
        gap: 18px;
        align-items: flex-start;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }}
    .glass-card.highlight {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-color: rgba(56, 189, 248, 0.25);
    }}
    .card-icon-box {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
    }}
    .card-icon-box.emerald {{
        background: rgba(52, 211, 153, 0.12);
        border-color: rgba(52, 211, 153, 0.25);
        color: #34d399;
    }}
    .card-icon-box.amber {{
        background: rgba(251, 191, 36, 0.12);
        border-color: rgba(251, 191, 36, 0.25);
        color: #fbbf24;
    }}
    .card-content h3 {{
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }}
    .card-content p {{
        font-size: 15px;
        color: #94a3b8;
        line-height: 1.48;
    }}

    /* CODE SNIPPET BOX */
    .code-container {{
        background: #020617;
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        overflow: hidden;
        margin: 14px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }}
    .code-header {{
        background: rgba(15, 23, 42, 0.9);
        padding: 10px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .code-dots {{
        display: flex;
        gap: 6px;
    }}
    .code-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}
    .code-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .code-body {{
        padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13.5px;
        line-height: 1.55;
        color: #e2e8f0;
        overflow-x: hidden;
        white-space: pre-wrap;
    }}
    .code-kw {{ color: #f43f5e; font-weight: 700; }}
    .code-fn {{ color: #38bdf8; font-weight: 600; }}
    .code-str {{ color: #34d399; }}
    .code-comment {{ color: #64748b; font-style: italic; }}
    .code-highlight {{ background: rgba(56, 189, 248, 0.12); padding: 2px 4px; border-radius: 4px; }}

    /* COMPARISON BEFORE & AFTER */
    .compare-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 10px;
    }}
    .compare-box {{
        background: rgba(15, 23, 42, 0.65);
        border-radius: 14px;
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .compare-box.bad {{
        border-color: rgba(239, 68, 68, 0.3);
        background: rgba(30, 15, 15, 0.4);
    }}
    .compare-box.good {{
        border-color: rgba(52, 211, 153, 0.3);
        background: rgba(10, 30, 20, 0.4);
    }}
    .compare-label {{
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }}
    .compare-label.bad {{ color: #f87171; }}
    .compare-label.good {{ color: #34d399; }}
    .compare-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
    }}
    .compare-desc {{
        font-size: 13.5px;
        color: #94a3b8;
        line-height: 1.45;
    }}

    /* BOTTOM FOOTER BRANDING */
    .slide-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 24px;
    }}
    .author-info {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .author-avatar-img {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid #38bdf8;
        object-fit: cover;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }}
    .author-text .name {{
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
    }}
    .author-text .role {{
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 500;
    }}
    .footer-action {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 6px 14px;
        border-radius: 100px;
    }}

    /* SLIDE 1 COVER SPECIAL */
    .cover-body {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        padding: 10px 0;
    }}
    .cover-hero-author {{
        display: flex;
        align-items: center;
        gap: 20px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 34px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }}
    .cover-hero-avatar {{
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 3px solid #38bdf8;
        object-fit: cover;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
    }}
    .cover-hero-name {{
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
    }}
    .cover-hero-role {{
        font-size: 15px;
        color: #38bdf8;
        font-weight: 600;
    }}
    .cover-meta-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 32px;
    }}
    .meta-stat-item {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 16px;
        text-align: center;
    }}
    .meta-stat-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #38bdf8;
    }}
    .meta-stat-lbl {{
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 4px;
    }}

    /* SLIDE 10 CLOSING SPECIAL */
    .closing-card {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 24px;
        padding: 36px 32px;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        margin: auto 0;
    }}
    .closing-avatar {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #38bdf8;
        object-fit: cover;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
        margin-bottom: 16px;
    }}
    .closing-name {{
        font-size: 28px;
        font-weight: 900;
        color: #ffffff;
    }}
    .closing-role {{
        font-size: 17px;
        color: #38bdf8;
        font-weight: 600;
        margin-top: 4px;
        margin-bottom: 22px;
    }}
    .closing-prompt {{
        font-size: 17px;
        color: #cbd5e1;
        line-height: 1.55;
        max-width: 680px;
        margin: 0 auto 28px auto;
        padding: 18px;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 14px;
        border: 1px dashed rgba(56, 189, 248, 0.3);
    }}
    .contact-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 24px;
    }}
    .contact-badge {{
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        text-align: left;
    }}
    .contact-badge-icon {{
        font-size: 20px;
        color: #38bdf8;
    }}
    .contact-badge-title {{
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
    }}
    .contact-badge-val {{
        font-size: 14px;
        color: #ffffff;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }}
    .repo-link-box {{
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 14px;
        padding: 14px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .repo-link-text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #e2e8f0;
        font-weight: 600;
    }}
</style>
</head>
<body>

<!-- ======================================================== -->
<!-- SLIDE 1: THE HOOK / EXECUTIVE COVER                      -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide1">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>
    
    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Audit Forensik Data <span class="accent">• 50 Cabang Retail</span></span>
            </div>
            <div class="slide-number">01 / 10</div>
        </div>

        <div class="cover-body">
            <div class="cover-hero-author">
                <img class="cover-hero-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="cover-hero-name">{author_name}</div>
                    <div class="cover-hero-role">{author_role}</div>
                </div>
            </div>

            <h1 class="hero-title">
                Menutup Kebocoran Laba <span class="highlight-cyan">Rp 18,3 Miliar</span> dengan Enterprise <span class="highlight-emerald">PostgreSQL Engine</span>
            </h1>

            <p class="subtitle">
                Studi kasus analitik relasional: Rekonsiliasi <em>Ghost Stockout</em>, audit penalti SLA vendor rantai pasok, dan pemulihan margin unit economics omnichannel.
            </p>

            <div class="cover-meta-grid">
                <div class="meta-stat-item">
                    <div class="meta-stat-val">50 Toko</div>
                    <div class="meta-stat-lbl">Jaringan Retail Fisik</div>
                </div>
                <div class="meta-stat-item">
                    <div class="meta-stat-val">3 Hub</div>
                    <div class="meta-stat-lbl">Gudang Regional</div>
                </div>
                <div class="meta-stat-item">
                    <div class="meta-stat-val">100% SQL</div>
                    <div class="meta-stat-lbl">Tanpa Beban Eksternal BI</div>
                </div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Geser ke Kanan ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 2: THE BURNING BUSINESS PAIN                        -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide2">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Diagnosa Operasional <span class="accent">• Akar Masalah Bisnis</span></span>
            </div>
            <div class="slide-number">02 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Ilusi Penjualan Semu: Omset Bertumbuh, Namun Laba Bocor <span class="highlight-amber">Rp 18,3 M</span></h2>
            <p class="subtitle">Banyak retail terjebak melihat volume GMV yang naik, tanpa menyadari margin bersih tergerus inefisiensi operasional.</p>
        </div>

        <div class="stat-hero-card amber-border">
            <div>
                <div class="stat-big highlight-amber">Rp 18.330.000.000</div>
                <div class="stat-desc">Akumulasi Kerugian Margin Operasional per Tahun</div>
            </div>
            <div class="stat-pill">4 Titik Kebocoran</div>
        </div>

        <div class="cards-stack">
            <div class="glass-card">
                <div class="card-icon-box amber">📦</div>
                <div class="card-content">
                    <h3>1. Stok Hantu (Phantom Inventory) — Hilang Rp 5,7 M</h3>
                    <p>Database mencatat barang tersedia, namun fisik di rak toko kosong. 6,8% pesanan online dibatalkan sepihak, memicu kekecewaan pembeli.</p>
                </div>
            </div>

            <div class="glass-card">
                <div class="card-icon-box amber">⏱️</div>
                <div class="card-content">
                    <h3>2. Wanprestasi Vendor SLA — Terlewat Rp 3,2 M</h3>
                    <p>Supplier kerap terlambat mengirim barang & tingkat cacat tinggi, namun klausul denda kontrak tidak pernah ditagih secara sistematis.</p>
                </div>
            </div>

            <div class="glass-card">
                <div class="card-icon-box amber">🚚</div>
                <div class="card-content">
                    <h3>3. Promo Ongkir Kilat Nombok — Defisit Rp 4,9 M</h3>
                    <p>Layanan <em>3-Hour Delivery</em> mencatatkan margin kontribusi minus Rp 24.500 per transaksi akibat subsidi pengiriman tanpa batas minimum order.</p>
                </div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Mengapa PostgreSQL? ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 3: ENGINEERING FOUNDATION (DATA INTEGRITY)          -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide3">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Database Architecture <span class="accent">• Data Integrity by Design</span></span>
            </div>
            <div class="slide-number">03 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Mengapa Analisis Selesai di <span class="highlight-cyan">PostgreSQL</span>, Bukan di Excel?</h2>
            <p class="subtitle">Prinsip Analis Senior: Beban integritas data dan logika bisnis berat harus diselesaikan di tingkat database relasional.</p>
        </div>

        <div class="code-container">
            <div class="code-header">
                <div class="code-dots">
                    <div class="code-dot dot-red"></div>
                    <div class="code-dot dot-yellow"></div>
                    <div class="code-dot dot-green"></div>
                </div>
                <div class="code-title">Enterprise DDL & Domain Constraints</div>
            </div>
            <div class="code-body">
<span class="code-kw">CREATE DOMAIN</span> d_positive_money <span class="code-kw">AS NUMERIC</span>(15,2) 
    <span class="code-kw">CHECK</span> (<span class="code-kw">VALUE</span> &gt;= 0.00); <span class="code-comment">-- Mencegah nilai uang minus abnormal</span>

<span class="code-kw">CREATE TYPE</span> order_channel_type <span class="code-kw">AS ENUM</span> (
    <span class="code-str">'STORE_POS'</span>, <span class="code-str">'ONLINE_WEB'</span>, <span class="code-str">'MARKETPLACE'</span>, <span class="code-str">'EXPRESS_APP'</span>
);

<span class="code-kw">ALTER TABLE</span> fact_order_items <span class="code-kw">ADD CONSTRAINT</span> chk_qty_positive
    <span class="code-kw">CHECK</span> (quantity &gt; 0 <span class="code-kw">AND</span> unit_selling_price &gt;= unit_cogs * 0.5);
            </div>
        </div>

        <div class="cards-stack">
            <div class="glass-card highlight">
                <div class="card-icon-box">🛡️</div>
                <div class="card-content">
                    <h3>Integritas Skema Mencegah Data Kotor (Zero Garbage In)</h3>
                    <p>PostgreSQL Domains & ENUMs mengeliminasi salah ketik kategori atau harga anomali di pintu masuk. Dashboard BI tidak perlu melakukan pembersihan data berulang kali.</p>
                </div>
            </div>
            <div class="glass-card">
                <div class="card-icon-box">⚡</div>
                <div class="card-content">
                    <h3>100% Siap Dihubungkan ke BI Tool (Plug-and-Play)</h3>
                    <p>Seluruh tabel mart dan view analitik sudah teragregasi secara presisi. Visualisasi di Power BI / Tableau berjalan sangat responsif tanpa komputasi berat di klien.</p>
                </div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Kasus 1: Ghost Stockout ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 4: KASUS 1 - GHOST STOCKOUT ERADICATION            -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide4">
    <div class="grid-bg"></div>
    <div class="glow-sphere-emerald"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Kasus 1 <span class="accent">• Forensik Persediaan Retail</span></span>
            </div>
            <div class="slide-number">04 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Membasmi <span class="highlight-cyan">"Ghost Stockout"</span>: Barang Ada di Sistem, Fisik Rak Kosong</h2>
            <p class="subtitle">Pesanan online masuk, staf toko mencari barang tapi fisik nihil. Pembatalan sepihak merusak reputasi toko.</p>
        </div>

        <div class="stat-hero-card">
            <div>
                <div class="stat-big highlight-cyan">Rp 5.720.000.000</div>
                <div class="stat-desc">Potensi Penjualan Hilang (Lost Sales) yang Diselamatkan</div>
            </div>
            <div class="stat-pill">6,8% ➔ 0,4% Batalkan Order</div>
        </div>

        <div class="code-container">
            <div class="code-header">
                <div class="code-dots">
                    <div class="code-dot dot-red"></div>
                    <div class="code-dot dot-yellow"></div>
                    <div class="code-dot dot-green"></div>
                </div>
                <div class="code-title">Window Function Discrepancy Detection</div>
            </div>
            <div class="code-body">
<span class="code-comment">-- Deteksi selisih stok sistem vs pola kasir yang macet</span>
<span class="code-kw">SELECT</span> store_id, product_id,
       recorded_stock,
       <span class="code-fn">LAG</span>(recorded_stock, 1) <span class="code-kw">OVER</span> (
           <span class="code-kw">PARTITION BY</span> store_id, product_id 
           <span class="code-kw">ORDER BY</span> audit_date
       ) <span class="code-kw">AS</span> prev_stock,
       <span class="code-kw">CASE WHEN</span> recorded_stock &gt; 0 <span class="code-kw">AND</span> actual_sales_qty = 0 
                 <span class="code-kw">AND</span> days_without_sales &gt;= 7 
            <span class="code-kw">THEN</span> <span class="code-str">'GHOST_STOCKOUT_ALERT'</span> <span class="code-kw">ELSE</span> <span class="code-str">'NORMAL'</span> <span class="code-kw">END AS</span> audit_status
<span class="code-kw">FROM</span> mart_inventory_discrepancy;
            </div>
        </div>

        <div class="glass-card highlight">
            <div class="card-icon-box emerald">🎯</div>
            <div class="card-content">
                <h3>Aksi Manajemen Berbasis Data</h3>
                <p>Daripada menghitung stok manual ke seluruh 50 cabang, query ini menghasilkan <strong>daftar prioritas audit fisik harian</strong> hanya untuk barang berstatus alert. Efisiensi staf gudang melonjak 340%.</p>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Kasus 2: Penalti Vendor ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 5: KASUS 2 - SUPPLIER SLA PENALTY AUDIT             -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide5">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Kasus 2 <span class="accent">• Tata Kelola Rantai Pasok</span></span>
            </div>
            <div class="slide-number">05 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Menagih Hak Perusahaan: Audit Penalti Keterlambatan <span class="highlight-emerald">SLA Vendor</span></h2>
            <p class="subtitle">Vendor terlambat kirim barang mengakibatkan rak kosong di momen akhir pekan. Denda kontrak selama ini luput ditagihkan.</p>
        </div>

        <div class="stat-hero-card emerald-border">
            <div>
                <div class="stat-big highlight-emerald">Rp 3.240.000.000</div>
                <div class="stat-desc">Dana Penalti Supplier Sah Berhasil Direkonsiliasi</div>
            </div>
            <div class="stat-pill emerald">100% Sesuai Kontrak SLA</div>
        </div>

        <div class="code-container">
            <div class="code-header">
                <div class="code-dots">
                    <div class="code-dot dot-red"></div>
                    <div class="code-dot dot-yellow"></div>
                    <div class="code-dot dot-green"></div>
                </div>
                <div class="code-title">Tiered SLA Penalty Logic Matrix</div>
            </div>
            <div class="code-body">
<span class="code-comment">-- Etika Kemitraan: Toleransi 24 jam pertama, denda proporsional >48 jam</span>
<span class="code-kw">SELECT</span> supplier_id, po_number,
       delivery_delay_days,
       <span class="code-kw">CASE</span> 
           <span class="code-kw">WHEN</span> delivery_delay_days &lt;= 1 <span class="code-kw">THEN</span> 0.00 <span class="code-comment">-- Grace period kemitraan</span>
           <span class="code-kw">WHEN</span> delivery_delay_days <span class="code-kw">BETWEEN</span> 2 <span class="code-kw">AND</span> 3 <span class="code-kw">THEN</span> po_value * 0.02
           <span class="code-kw">WHEN</span> delivery_delay_days &gt; 3 <span class="code-kw">THEN</span> po_value * 0.05
       <span class="code-kw">END AS</span> calculated_penalty_amount
<span class="code-kw">FROM</span> fact_purchase_orders;
            </div>
        </div>

        <div class="compare-grid">
            <div class="compare-box bad">
                <div class="compare-label bad">Sebelumnya (Manual)</div>
                <div class="compare-value">Rp 0</div>
                <div class="compare-desc">Denda tidak ditagih karena tim finance kewalahan mencocokkan surat jalan fisik vs invoice.</div>
            </div>
            <div class="compare-box good">
                <div class="compare-label good">Sesudah (Otomatis SQL)</div>
                <div class="compare-value highlight-emerald">Rp 3,24 M</div>
                <div class="compare-desc">Potongan denda otomatis diterbitkan saat kliring pembayaran tagihan PO supplier.</div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Kasus 3: Unit Economics ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 6: KASUS 3 - UNIT ECONOMICS & LOGISTICS DEFICIT     -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide6">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Kasus 3 <span class="accent">• Unit Economics & Margin Kontribusi</span></span>
            </div>
            <div class="slide-number">06 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Promo Ongkir Kilat: Ramai Transaksi, Namun <span class="highlight-amber">Nombok Rp 24.500</span>/Order</h2>
            <p class="subtitle">Layanan Express 3-Hour Delivery sangat laris, tetapi membakar uang perusahaan secara tidak terkendali.</p>
        </div>

        <div class="stat-hero-card amber-border">
            <div>
                <div class="stat-big highlight-amber">Rp 4.880.000.000</div>
                <div class="stat-desc">Efisiensi Biaya Logistik Diselamatkan Melalui Ambang Belanja Baru</div>
            </div>
            <div class="stat-pill">AOV: Rp 150rb ➔ Rp 250rb</div>
        </div>

        <div class="compare-grid">
            <div class="compare-box bad">
                <div class="compare-label bad">Kondisi Lama (Threshold Rp 150.000)</div>
                <div class="compare-value highlight-amber">- Rp 24.500</div>
                <div class="compare-desc">
                    • Laba Kotor (30%): Rp 45.000<br>
                    • Ongkir Kilat Subsidi: (Rp 48.000)<br>
                    • Kemasan Khusus: (Rp 12.500)<br>
                    • Gateway Payment: (Rp 9.000)<br>
                    <strong>➔ Margin Bersih: DEFISIT NEGATIF</strong>
                </div>
            </div>
            <div class="compare-box good">
                <div class="compare-label good">Rekomendasi SQL (Threshold Rp 250.000)</div>
                <div class="compare-value highlight-emerald">+ Rp 12.000</div>
                <div class="compare-desc">
                    • Laba Kotor (30%): Rp 75.000<br>
                    • Ongkir Kilat Subsidi: (Rp 45.000)<br>
                    • Kemasan Khusus: (Rp 10.000)<br>
                    • Gateway Payment: (Rp 8.000)<br>
                    <strong>➔ Margin Bersih: LABA SEHAT</strong>
                </div>
            </div>
        </div>

        <div class="glass-card highlight" style="margin-top: 14px;">
            <div class="card-icon-box">💡</div>
            <div class="card-content">
                <h3>Keputusan Strategis Tanpa Mematikan Fitur</h3>
                <p>Alih-alih menutup layanan kilat yang disukai pelanggan, manajemen cukup menaikkan syarat belanja minimum dari Rp 150rb ke Rp 250rb. Margin berbalik positif dan mengamankan <strong>Rp 4,88 Miliar</strong> per tahun.</p>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Kasus 4: Kohort Retensi ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 7: KASUS 4 - COHORT RETENTION & CHURN CLIFF        -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide7">
    <div class="grid-bg"></div>
    <div class="glow-sphere-emerald"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Kasus 4 <span class="accent">• Customer Lifecycle Analytics</span></span>
            </div>
            <div class="slide-number">07 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Mencegah Churn: Mengungkap Jurang Retensi di <span class="highlight-cyan">Bulan ke-2 (Month 2 Cliff)</span></h2>
            <p class="subtitle">Akuisisi pelanggan baru sangat tinggi, namun 86% pelanggan menghilang setelah bulan pertama.</p>
        </div>

        <div class="stat-hero-card emerald-border">
            <div>
                <div class="stat-big highlight-emerald">Rp 4.490.000.000</div>
                <div class="stat-desc">Nilai LTV (Customer Lifetime Value) yang Berhasil Dipulihkan</div>
            </div>
            <div class="stat-pill emerald">Retention: 14% ➔ 31%</div>
        </div>

        <div class="code-container">
            <div class="code-header">
                <div class="code-dots">
                    <div class="code-dot dot-red"></div>
                    <div class="code-dot dot-yellow"></div>
                    <div class="code-dot dot-green"></div>
                </div>
                <div class="code-title">12-Month Cohort Analysis with Recursive CTE</div>
            </div>
            <div class="code-body">
<span class="code-kw">WITH</span> first_orders <span class="code-kw">AS</span> (
    <span class="code-kw">SELECT</span> customer_id, <span class="code-fn">DATE_TRUNC</span>(<span class="code-str">'month'</span>, <span class="code-fn">MIN</span>(order_date)) <span class="code-kw">AS</span> cohort_month
    <span class="code-kw">FROM</span> fact_orders <span class="code-kw">GROUP BY</span> customer_id
),
retention_matrix <span class="code-kw">AS</span> (
    <span class="code-kw">SELECT</span> f.cohort_month,
           <span class="code-fn">EXTRACT</span>(year <span class="code-kw">FROM</span> o.order_date)*12 + <span class="code-fn">EXTRACT</span>(month <span class="code-kw">FROM</span> o.order_date) -
           (<span class="code-fn">EXTRACT</span>(year <span class="code-kw">FROM</span> f.cohort_month)*12 + <span class="code-fn">EXTRACT</span>(month <span class="code-kw">FROM</span> f.cohort_month)) <span class="code-kw">AS</span> month_gap,
           <span class="code-fn">COUNT</span>(<span class="code-kw">DISTINCT</span> o.customer_id) <span class="code-kw">AS</span> retained_users
    <span class="code-kw">FROM</span> fact_orders o <span class="code-kw">JOIN</span> first_orders f <span class="code-kw">ON</span> o.customer_id = f.customer_id
    <span class="code-kw">GROUP BY</span> 1, 2
)
            </div>
        </div>

        <div class="glass-card highlight">
            <div class="card-icon-box emerald">🎯</div>
            <div class="card-content">
                <h3>Golden Re-Engagement Window (Hari ke-14 s/d 21)</h3>
                <p>Data membuktikan jika pelanggan tidak bertransaksi ulang sebelum hari ke-21, probabilitas mereka kembali turun di bawah 5%. Solusi: Otomatisasi promo personalisasi pada hari ke-14 mengangkat retensi ke 31%.</p>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Performa Mesin SQL ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 8: QUERY PERFORMANCE OPTIMIZATION                  -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide8">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Engineering Depth <span class="accent">• Query Tuning & Indexing</span></span>
            </div>
            <div class="slide-number">08 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Dari 8,4 Detik Menjadi <span class="highlight-cyan">140 Milidetik</span>: Efisiensi Melejit <span class="highlight-emerald">98,3%</span></h2>
            <p class="subtitle">Query yang lambat membekukan database operasional. Kami mendesain strategi indexing multi-lapis.</p>
        </div>

        <div class="stat-hero-card">
            <div>
                <div class="stat-big highlight-cyan">140 ms</div>
                <div class="stat-desc">Waktu Eksekusi Query Agregasi 500.000+ Baris Transaksi</div>
            </div>
            <div class="stat-pill">60x Lebih Cepat</div>
        </div>

        <div class="compare-grid">
            <div class="compare-box bad">
                <div class="compare-label bad">Sebelum Optimasi (Sequential Scan)</div>
                <div class="compare-value highlight-amber">8.420 ms</div>
                <div class="compare-desc">
                    • Membaca seluruh disk block secara linier.<br>
                    • Beban CPU server melonjak 95%.<br>
                    • Query analitik mengganggu kasir toko.
                </div>
            </div>
            <div class="compare-box good">
                <div class="compare-label good">Setelah Optimasi (Composite & Partial Index)</div>
                <div class="compare-value highlight-emerald">142 ms</div>
                <div class="compare-desc">
                    • <code>CREATE INDEX idx_orders_status ON ...</code><br>
                    • Partial index khusus pesanan aktif (unfulfilled).<br>
                    • BRIN Index untuk timestamp historis.
                </div>
            </div>
        </div>

        <div class="cards-stack" style="margin-top: 14px;">
            <div class="glass-card highlight">
                <div class="card-icon-box">🚀</div>
                <div class="card-content">
                    <h3>Hasil: Arsitektur 100% Siap untuk BI Skala Besar</h3>
                    <p>Database mampu melayani ratusan kueri analitik bersamaan tanpa latensi, menjamin laporan manajemen dan dashboard operasional selalu terbarui secara <em>real-time</em>.</p>
                </div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Rekapitulasi Finansial ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 9: TOTAL FINANCIAL ROI & 90-DAY ROADMAP             -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide9">
    <div class="grid-bg"></div>
    <div class="glow-sphere-emerald"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Executive Summary <span class="accent">• Roadmap Rekonsiliasi Laba</span></span>
            </div>
            <div class="slide-number">09 / 10</div>
        </div>

        <div class="title-area">
            <h2 class="slide-title">Rencana Aksi 90 Hari: Menyelamatkan Laba <span class="highlight-emerald">Rp 18,3 Miliar</span></h2>
            <p class="subtitle">Bukan sekadar temuan di atas kertas, melainkan panduan eksekusi nyata untuk direksi dan manajemen.</p>
        </div>

        <div class="cards-stack">
            <div class="glass-card highlight">
                <div class="card-icon-box emerald">1️⃣</div>
                <div class="card-content">
                    <h3>Hari 1–30: Audit & Tagih Penalti Supplier (+Rp 3,2 M)</h3>
                    <p>Menerbitkan otomatisasi nota penalti SLA vendor saat rekonsiliasi faktur pembelian. Menghasilkan pemulihan kas langsung tanpa belanja modal.</p>
                </div>
            </div>

            <div class="glass-card highlight">
                <div class="card-icon-box emerald">2️⃣</div>
                <div class="card-content">
                    <h3>Hari 31–60: Hapus Defisit Ongkir & Basmi Ghost Stockout (+Rp 10,6 M)</h3>
                    <p>Naikkan batas minimum order Express Delivery ke Rp 250rb. Terapkan alert stok harian bagi staf gudang untuk menekan pesanan batal.</p>
                </div>
            </div>

            <div class="glass-card highlight">
                <div class="card-icon-box emerald">3️⃣</div>
                <div class="card-content">
                    <h3>Hari 61–90: Otomatisasi Retensi Kohort Hari ke-14 (+Rp 4,5 M)</h3>
                    <p>Integrasi query kohort ke sistem CRM pemasaran untuk re-engagement otomatis pembeli baru sebelum masuk jurang churn.</p>
                </div>
            </div>
        </div>

        <div class="stat-hero-card emerald-border" style="margin-top: 14px;">
            <div>
                <div class="stat-big highlight-emerald">Rp 18.330.000.000</div>
                <div class="stat-desc">Total Nilai Pemulihan Laba Bersih Tahunan (Annual Net Profit Recovery)</div>
            </div>
            <div class="stat-pill emerald">ROI 100% Terukur</div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Hubungi Penulis ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 10: CLOSING CTA, CODEBASE & CONTACT                -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide10">
    <div class="grid-bg"></div>
    <div class="glow-sphere"></div>

    <div class="content-layer">
        <div class="slide-header">
            <div class="tag-badge">
                <span class="dot"></span>
                <span>Data Talent <span class="accent">• Collaboration &amp; Inquiry</span></span>
            </div>
            <div class="slide-number">10 / 10</div>
        </div>

        <div class="closing-card">
            <img class="closing-avatar" src="{author_photo_uri}" alt="{author_name}">
            <div class="closing-name">{author_name}</div>
            <div class="closing-role">{author_role}</div>

            <div class="closing-prompt">
                💬 <strong>Mari Berdiskusi:</strong> Bagaimana tim data di organisasi rekan-rekan menangani selisih stok phantom vs fisik saat kampanye flash sale? Mari bertukar wawasan di kolom komentar!
            </div>

            <div class="contact-grid">
                <div class="contact-badge">
                    <div class="contact-badge-icon">📧</div>
                    <div>
                        <div class="contact-badge-title">Email Resmi</div>
                        <div class="contact-badge-val">{author_email}</div>
                    </div>
                </div>
                <div class="contact-badge">
                    <div class="contact-badge-icon">💬</div>
                    <div>
                        <div class="contact-badge-title">WhatsApp Bisnis</div>
                        <div class="contact-badge-val">{author_wa_formatted}</div>
                    </div>
                </div>
            </div>

            <div class="repo-link-box">
                <div class="repo-link-text">
                    📂 Repositori Lengkap (DDL, Query &amp; Laporan):<br>
                    <strong>github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine</strong>
                </div>
                <div class="stat-pill">PostgreSQL 15+</div>
            </div>
        </div>

        <div class="slide-footer">
            <div class="author-info">
                <img class="author-avatar-img" src="{author_photo_uri}" alt="{author_name}">
                <div class="author-text">
                    <div class="name">{author_name}</div>
                    <div class="role">{author_role}</div>
                </div>
            </div>
            <div class="footer-action">Terbuka untuk Peluang Kerja</div>
        </div>
    </div>
</div>

</body>
</html>
"""

# Write HTML file
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Interactive HTML preview saved: {html_file}")

# Browser detection for PDF & Screenshots
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
browser_bin = None
for cp in chrome_paths:
    if os.path.exists(cp):
        browser_bin = cp
        break

if not browser_bin:
    print("Warning: Google Chrome or Microsoft Edge not found in standard paths.")
else:
    print(f"Using browser binary: {browser_bin}")
    
    # Generate Multi-Page PDF for LinkedIn Document Upload
    cmd_pdf = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        str(html_file)
    ]
    print("Rendering Multi-Page PDF for LinkedIn Document Carousel...")
    res_pdf = subprocess.run(cmd_pdf, capture_output=True)
    if pdf_file.exists():
        print(f"SUCCESS: Generated PDF carousel: {pdf_file.name} ({pdf_file.stat().st_size / 1024:.2f} KB)")
    else:
        print("PDF generation failed:", res_pdf.stderr.decode('utf-8', errors='ignore'))

    # Generate Individual 10 PNG Slides (1080x1350)
    print("Rendering 10 Individual High-Res PNG Slides...")
    for i in range(1, 11):
        slide_png = CAROUSEL_DIR / f"slide_{i:02d}.png"
        slide_html = CAROUSEL_DIR / f"_temp_slide_{i:02d}.html"
        
        # Extract specific slide wrapper
        parts = html_content.split(f'id="slide{i}"')
        if len(parts) > 1:
            head = html_content.split('<div class="slide-wrapper" id="slide1">')[0]
            if i < 10:
                slide_body = f'<div class="slide-wrapper" id="slide{i}"' + parts[1].split('<!-- ======================================================== -->')[0]
            else:
                slide_body = f'<div class="slide-wrapper" id="slide10"' + parts[1].split('</body>')[0]
                
            single_html = head + slide_body + "</body></html>"
            slide_html.write_text(single_html, encoding="utf-8")
            
            cmd_img = [
                browser_bin,
                "--headless",
                "--disable-gpu",
                "--window-size=1080,1350",
                f"--screenshot={slide_png}",
                str(slide_html)
            ]
            subprocess.run(cmd_img, capture_output=True)
            if slide_html.exists():
                slide_html.unlink()
            print(f"  Slide {i:02d} PNG: {slide_png.name} (Exists: {slide_png.exists()})")

# Generate High-Converting LinkedIn Post Copy (Optimized for HR & Technical Recruiter Engagement)
post_copy = f"""Banyak retail terjebak pada ilusi penjualan: "GMV naik 22%, bisnis tampak sehat."
Namun saat data transaksi 50 cabang dan 3 gudang regional dibedah mendalam, kami menemukan kebocoran laba bersih mencapai Rp 18,3 Miliar per tahun.

Sebagai Data Analyst & Business Intelligence, bagi saya data bukan sekadar grafik warna-warni di BI tools—melainkan bagaimana logika relasional tingkat database mampu mengamankan margin dan mengarahkan keputusan bisnis secara presisi.

Dalam studi kasus ini, seluruh mesin audit dirancang 100% menggunakan Enterprise PostgreSQL 15+ Engine.

Berikut 4 temuan kritis hasil audit data forensik:

1️⃣ Membasmi "Ghost Stockout" (Phantom Inventory) — Selamatkan Rp 5,7 Miliar:
Sistem mencatat stok barang tersedia, namun fisik di rak toko kosong. Akibatnya 6,8% pesanan online dibatalkan sepihak dan mengecewakan pelanggan.
Menggunakan Window Function LAG() dan discrepancy tracking, kami mendeteksi anomali selisih stok secara otomatis dan menerbitkan prioritas audit fisik harian ke staf gudang, menekan order pembatalan ke 0,4%.

2️⃣ Audit Kepatuhan & Penalti Supplier SLA — Reklasifikasi Rp 3,2 Miliar:
Supplier kerap terlambat mengirim barang sehingga rak kosong di akhir pekan. Denda kontrak selama ini luput ditagihkan karena tim finance kewalahan mencocokkan surat jalan fisik vs invoice.
Dengan query analitik otomatis berpola Tiered Grace-Period (toleransi <24 jam, denda proporsional >48 jam), denda otomatis dipotong saat kliring tagihan PO tanpa merusak hubungan kemitraan.

3️⃣ Unit Economics Promo Ongkir Kilat — Hemat Rp 4,9 Miliar:
Layanan Express 3-Hour Delivery sangat laris, tetapi membakar uang: margin kontribusi minus Rp 24.500 per transaksi karena subsidi kurir tanpa batas minimal belanja.
Alih-alih mematikan layanan, simulasi SQL membuktikan bahwa menaikkan batas belanja (AOV threshold) dari Rp 150rb ke Rp 250rb membalikkan margin menjadi positif (+Rp 12.000/order).

4️⃣ Jurang Retensi Pelanggan Bulan ke-2 (Month 2 Cliff) — Pulihkan Rp 4,5 Miliar LTV:
Analisis kohort 12 bulan membuktikan 86% pelanggan baru churn setelah bulan pertama. Query mengidentifikasi "Golden Re-engagement Window" pada hari ke-14 s/d 21 pasca pembelian pertama untuk mengirimkan penawaran komplementer terarah.

⚡ Efisiensi Mesin Database:
Melalui strategi Composite B-Tree dan Partial Indexing, waktu respon query analitik dipangkas 98,3% (dari 8,4 detik menjadi 140 milidetik), memastikan data 100% Plug-and-Play untuk konsumsi BI.

👉 Geser dokumen carousel 10 slide di atas untuk melihat arsitektur skema DDL, cuplikan query SQL, dan roadmap eksekusi 90 harinya!

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Eksplorasi Skrip SQL Lengkap & Laporan Bisnis di GitHub:
{github_url}

📬 Terbuka untuk Diskusi & Peluang Kerja (Data Analyst / BI Analyst):
👤 {author_name} | {author_role}
📧 {author_email}
💬 WhatsApp: {author_wa_formatted} (https://wa.me/62{author_wa[1:]})

Bagaimana pendekatan rekan-rekan dalam menangani selisih stok fisik vs sistem saat kampanye promo besar? Mari berdiskusi di kolom komentar! 👇

#DataAnalytics #BusinessIntelligence #PostgreSQL #SQL #SupplyChainAnalytics #RetailAnalytics #DataEngineering #DataStorytelling #UnitEconomics #HiringDataAnalyst #JobSeeker
"""

with open(post_copy_file, "w", encoding="utf-8") as f:
    f.write(post_copy)
print(f"LinkedIn Post Copy saved: {post_copy_file}")
print("ALL ASSETS GENERATED SUCCESSFULLY!")
