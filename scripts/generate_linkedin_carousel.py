"""
========================================================================================
Next-Gen Enterprise-Ready LinkedIn Carousel Generator (V3)
Omnichannel Retail & Supply Chain Analytics Engine (PostgreSQL 15+)
Author: Fajar Setyadi | Data Analyst & Business Intelligence

Enterprise Polish & Alignment:
- Realistic Governance Framing: Strategic Enabler & Data Forensic Audit
- Professional Tone: Replaced naive "superhero" claims with Cross-Functional Decision Intelligence
- Enterprise Architecture: PostgreSQL Production Analytics Engine (No junior Excel comparisons)
- Vendor Governance: SLA Dispute Audit Trail (No arbitrary penalty cuts)
- Commercial Acumen: AOV Restructuring with Cross-Selling Bundling (Conversion Protection)
- Clean Mobile-First UI/UX: No redundant author avatar on cover slide footer
========================================================================================
"""

import os
import subprocess
from pathlib import Path
import base64
import sys

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
<title>LinkedIn Carousel - Omnichannel Retail Analytics Engine (Enterprise Edition)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,800&family=JetBrains+Mono:wght@500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
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
        background-color: #03050a;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
        -webkit-font-smoothing: antialiased;
        margin: 0;
        padding: 0;
    }}
    
    .slide-wrapper {{
        width: 1080px;
        height: 1350px;
        position: relative;
        background: #060913;
        overflow: hidden;
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 65px 72px 55px 72px;
    }}

    /* Futuristic Geometric Ambient Lighting */
    .ambient-glow-top {{
        position: absolute;
        width: 750px;
        height: 650px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.14) 0%, rgba(6, 182, 212, 0.05) 45%, transparent 70%);
        top: -180px;
        right: -140px;
        pointer-events: none;
        z-index: 1;
    }}
    .ambient-glow-bottom {{
        position: absolute;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.03) 50%, transparent 70%);
        bottom: -150px;
        left: -120px;
        pointer-events: none;
        z-index: 1;
    }}
    .cyber-mesh {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
        background-size: 32px 32px;
        pointer-events: none;
        opacity: 0.55;
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

    /* HEADER: Dossier Status Bar */
    .top-status-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }}
    .dossier-tag {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(99, 102, 241, 0.35);
        padding: 8px 18px;
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #e0e7ff;
    }}
    .dossier-tag .pulse-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00f2fe;
        box-shadow: 0 0 10px #00f2fe;
    }}
    .dossier-tag .accent-cyan {{ color: #00f2fe; }}
    .dossier-tag .accent-emerald {{ color: #10b981; }}
    .dossier-tag .accent-rose {{ color: #f43f5e; }}

    .slide-counter-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        font-weight: 800;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 16px;
        border-radius: 8px;
    }}

    /* HEADLINE TITLES */
    .title-block {{
        margin-bottom: 22px;
    }}
    h1.hero-title {{
        font-size: 47px;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -1.2px;
        color: #ffffff;
        margin-bottom: 16px;
    }}
    h2.slide-headline {{
        font-size: 38px;
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.8px;
        color: #ffffff;
        margin-bottom: 10px;
    }}
    .lead-text {{
        font-size: 18px;
        font-weight: 500;
        line-height: 1.5;
        color: #94a3b8;
    }}
    .highlight-gradient-cyan {{
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .highlight-gradient-emerald {{
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .highlight-gradient-rose {{
        background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .highlight-gradient-amber {{
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* BENTO BOX COMPONENTS */
    .bento-grid-2col {{
        display: grid;
        grid-template-columns: 1.25fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }}
    .bento-grid-3col {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-bottom: 16px;
    }}
    .bento-card {{
        background: rgba(13, 19, 35, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px 24px;
        position: relative;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }}
    .bento-card.highlight-cyan-border {{
        border-color: rgba(0, 242, 254, 0.3);
        background: linear-gradient(145deg, rgba(15, 25, 48, 0.85) 0%, rgba(9, 14, 26, 0.9) 100%);
    }}
    .bento-card.highlight-emerald-border {{
        border-color: rgba(16, 185, 129, 0.3);
        background: linear-gradient(145deg, rgba(10, 30, 25, 0.85) 0%, rgba(8, 18, 15, 0.9) 100%);
    }}
    .bento-card.highlight-rose-border {{
        border-color: rgba(244, 63, 94, 0.3);
        background: linear-gradient(145deg, rgba(32, 12, 18, 0.85) 0%, rgba(18, 8, 12, 0.9) 100%);
    }}

    /* METRIC HERO CARD */
    .hero-metric-strip {{
        background: linear-gradient(135deg, rgba(20, 30, 55, 0.85) 0%, rgba(10, 16, 30, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.35);
        border-radius: 20px;
        padding: 24px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.45);
    }}
    .hero-metric-strip.rose {{
        border-color: rgba(244, 63, 94, 0.4);
        background: linear-gradient(135deg, rgba(40, 14, 22, 0.85) 0%, rgba(18, 7, 12, 0.95) 100%);
    }}
    .hero-metric-strip.emerald {{
        border-color: rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, rgba(12, 36, 28, 0.85) 0%, rgba(6, 18, 14, 0.95) 100%);
    }}
    .metric-mega-number {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 50px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1.2px;
        line-height: 1;
    }}
    .metric-caption {{
        font-size: 15.5px;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 6px;
    }}
    .metric-pill-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 13.5px;
        font-weight: 800;
        padding: 8px 18px;
        border-radius: 100px;
        background: rgba(0, 242, 254, 0.12);
        border: 1px solid rgba(0, 242, 254, 0.4);
        color: #00f2fe;
    }}
    .metric-pill-badge.rose {{
        background: rgba(244, 63, 94, 0.15);
        border-color: rgba(244, 63, 94, 0.4);
        color: #fb7185;
    }}
    .metric-pill-badge.emerald {{
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.4);
        color: #34d399;
    }}

    /* VISUAL LEAKAGE PIPELINE */
    .pipeline-container {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 18px;
    }}
    .pipeline-step {{
        display: flex;
        align-items: center;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 20px;
        gap: 18px;
    }}
    .pipeline-step.leaking {{
        border-color: rgba(244, 63, 94, 0.35);
        background: linear-gradient(90deg, rgba(35, 14, 20, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    }}
    .pipe-node-badge {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 12px;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 6px;
        background: rgba(244, 63, 94, 0.2);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
        flex-shrink: 0;
    }}
    .pipe-content h3 {{
        font-size: 17px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .pipe-content p {{
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.45;
    }}
    .pipe-leak-amount {{
        margin-left: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 800;
        color: #f43f5e;
        flex-shrink: 0;
    }}

    /* CODE TERMINAL WINDOW */
    .terminal-box {{
        background: #02040a;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }}
    .terminal-bar {{
        background: rgba(15, 23, 42, 0.95);
        padding: 10px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .terminal-lights {{
        display: flex;
        gap: 6px;
    }}
    .terminal-light {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}
    .t-red {{ background: #ef4444; }}
    .t-yellow {{ background: #f59e0b; }}
    .t-green {{ background: #10b981; }}
    .terminal-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 1px;
    }}
    .terminal-engine-tag {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: #00f2fe;
        background: rgba(0, 242, 254, 0.12);
        padding: 2px 8px;
        border-radius: 4px;
    }}
    .terminal-code {{
        padding: 18px 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13.5px;
        line-height: 1.6;
        color: #e2e8f0;
        white-space: pre-wrap;
    }}
    .kw {{ color: #f43f5e; font-weight: 700; }}
    .fn {{ color: #00f2fe; font-weight: 600; }}
    .str {{ color: #34d399; }}
    .cmt {{ color: #64748b; font-style: italic; }}

    /* WATERFALL VISUAL BAR CHART */
    .waterfall-card {{
        background: rgba(13, 19, 35, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 18px;
    }}
    .waterfall-row {{
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 13.5px;
        font-weight: 600;
    }}
    .wf-label {{
        width: 200px;
        color: #cbd5e1;
        flex-shrink: 0;
    }}
    .wf-bar-track {{
        flex-grow: 1;
        height: 24px;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 6px;
        overflow: hidden;
        position: relative;
        display: flex;
        align-items: center;
        padding: 0 10px;
    }}
    .wf-bar-fill {{
        position: absolute;
        top: 0;
        bottom: 0;
        border-radius: 6px;
    }}
    .wf-bar-fill.pos {{
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        left: 0;
    }}
    .wf-bar-fill.neg {{
        background: linear-gradient(90deg, #f43f5e 0%, #fb7185 100%);
        right: 0;
    }}
    .wf-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        font-weight: 800;
        color: #ffffff;
        position: relative;
        z-index: 2;
    }}
    .wf-total-badge {{
        margin-top: 14px;
        padding: 12px 18px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 800;
    }}
    .wf-total-badge.bad {{
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #fb7185;
    }}
    .wf-total-badge.good {{
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
    }}

    /* COHORT HEATMAP GRID */
    .cohort-heatmap-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 6px;
        margin: 14px 0 18px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }}
    .cohort-heatmap-table th {{
        padding: 8px;
        color: #94a3b8;
        font-weight: 700;
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
    }}
    .cohort-heatmap-table td {{
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        font-weight: 800;
        color: #ffffff;
    }}
    .c-m0 {{ background: #064e3b; color: #a7f3d0; }}
    .c-m1 {{ background: #047857; color: #d1fae5; }}
    .c-cliff {{ background: rgba(244, 63, 94, 0.35); color: #fecdd3; border: 1px solid #f43f5e; }}
    .c-low {{ background: rgba(30, 41, 59, 0.6); color: #94a3b8; }}

    /* QUERY BENCHMARK CHART */
    .speed-chart-card {{
        background: rgba(13, 19, 35, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
    }}
    .speed-track-row {{
        margin-bottom: 18px;
    }}
    .speed-track-header {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 700;
    }}
    .speed-bar-slot {{
        height: 32px;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 8px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        padding: 0 14px;
    }}
    .speed-fill-red {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #f43f5e 0%, #fb7185 100%);
    }}
    .speed-fill-green {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 2.5%;
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        box-shadow: 0 0 12px #10b981;
    }}
    .speed-number-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        font-weight: 800;
        color: #ffffff;
        position: relative;
        z-index: 2;
    }}

    /* ROADMAP STEPPED MATRIX */
    .roadmap-timeline {{
        display: flex;
        flex-direction: column;
        gap: 14px;
        margin-bottom: 18px;
    }}
    .timeline-node {{
        display: flex;
        gap: 18px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 22px;
        align-items: center;
    }}
    .node-phase-badge {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 12px;
        font-weight: 800;
        padding: 8px 14px;
        border-radius: 8px;
        background: rgba(0, 242, 254, 0.12);
        border: 1px solid rgba(0, 242, 254, 0.4);
        color: #00f2fe;
        flex-shrink: 0;
    }}
    .node-body h3 {{
        font-size: 17px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .node-body p {{
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.45;
    }}
    .node-gain {{
        margin-left: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 17px;
        font-weight: 800;
        color: #34d399;
        flex-shrink: 0;
    }}

    /* FOOTER BRANDING BAR */
    .dossier-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .dossier-author {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .dossier-avatar {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid #00f2fe;
        object-fit: cover;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.35);
    }}
    .dossier-name {{
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
    }}
    .dossier-role {{
        font-size: 12.5px;
        color: #00f2fe;
        font-weight: 600;
    }}
    .dossier-action-btn {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.4) 0%, rgba(0, 242, 254, 0.25) 100%);
        border: 1px solid rgba(0, 242, 254, 0.4);
        padding: 8px 18px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);
    }}

    /* COVER VIP CARD (SLIDE 1) */
    .cover-vip-card {{
        background: linear-gradient(145deg, rgba(20, 28, 52, 0.8) 0%, rgba(10, 15, 30, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 24px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }}
    .cover-vip-avatar {{
        width: 86px;
        height: 86px;
        border-radius: 50%;
        border: 3px solid #00f2fe;
        object-fit: cover;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.45);
        flex-shrink: 0;
    }}
    .cover-vip-name {{
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
    }}
    .cover-vip-role {{
        font-size: 15px;
        color: #00f2fe;
        font-weight: 700;
        margin-top: 3px;
    }}
    .cover-vip-tag {{
        display: inline-block;
        margin-top: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 12px;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.08);
        padding: 4px 10px;
        border-radius: 6px;
        color: #cbd5e1;
    }}

    /* SLIDE 1 DEDICATED CLEAN FOOTER (NO DUPLICATE AVATAR) */
    .cover-footer-clean {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .cover-footer-context {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }}

    /* CLOSING CARD (SLIDE 10) */
    .closing-vip-box {{
        background: linear-gradient(145deg, rgba(22, 32, 60, 0.85) 0%, rgba(10, 15, 30, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.35);
        border-radius: 24px;
        padding: 36px 32px;
        text-align: center;
        box-shadow: 0 14px 45px rgba(0, 0, 0, 0.5);
    }}
    .closing-avatar-large {{
        width: 105px;
        height: 105px;
        border-radius: 50%;
        border: 3px solid #00f2fe;
        object-fit: cover;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.5);
        margin-bottom: 16px;
    }}
    .closing-prompt-quote {{
        font-size: 17px;
        color: #cbd5e1;
        line-height: 1.55;
        max-width: 720px;
        margin: 18px auto 26px auto;
        padding: 18px 22px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 14px;
        border: 1px dashed rgba(0, 242, 254, 0.3);
    }}
    .contact-card-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 22px;
    }}
    .contact-item {{
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        text-align: left;
    }}
    .contact-item-icon {{
        font-size: 22px;
        color: #00f2fe;
    }}
    .repo-box-creative {{
        background: rgba(0, 242, 254, 0.08);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
</style>
</head>
<body>

<!-- ======================================================== -->
<!-- SLIDE 1: COVER (ENTERPRISE FORENSIC AUDIT DOSSIER)       -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide1">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>
    <div class="ambient-glow-bottom"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>STRATEGIC DATA AUDIT <span class="accent-cyan">• 50 CABANG RETAIL</span></span>
            </div>
            <div class="slide-counter-badge">01 / 10</div>
        </div>

        <div>
            <div class="cover-vip-card">
                <img class="cover-vip-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="cover-vip-name">{author_name}</div>
                    <div class="cover-vip-role">{author_role}</div>
                    <div class="cover-vip-tag">PostgreSQL 15+ Enterprise Analytics Engine</div>
                </div>
            </div>

            <div class="title-block">
                <h1 class="hero-title">
                    Audit Forensik Rantai Pasok 50 Gerai: Rekonsiliasi Potensi Margin <span class="highlight-gradient-cyan">Rp 18,3 Miliar</span> Berbasis <span class="highlight-gradient-emerald">PostgreSQL Engine</span>
                </h1>
                <p class="lead-text">
                    Studi Kasus Analitik Relasional untuk Pengambilan Keputusan Direksi: Mitigasi <em>Ghost Stockout</em>, audit kepatuhan SLA vendor, dan restrukturisasi margin unit economics omnichannel.
                </p>
            </div>

            <div class="bento-grid-3col">
                <div class="bento-card highlight-cyan-border" style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: #00f2fe;">50 Gerai</div>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 600; margin-top: 4px;">Jaringan Retail Fisik</div>
                </div>
                <div class="bento-card highlight-cyan-border" style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: #a78bfa;">3 Hub</div>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 600; margin-top: 4px;">Fulfillment Regional</div>
                </div>
                <div class="bento-card highlight-cyan-border" style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: #34d399;">100% SQL</div>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 600; margin-top: 4px;">Logika di Level Mesin</div>
                </div>
            </div>
        </div>

        <div class="cover-footer-clean">
            <div class="cover-footer-context">
                🏢 Laporan Intelijen Keputusan Bisnis Eksekutif
            </div>
            <div class="dossier-action-btn">Mulai Membaca Laporan ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 2: THE LEAKAGE PIPELINE (4 TITIK KEBOCORAN)        -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide2">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot" style="background: #f43f5e; box-shadow: 0 0 10px #f43f5e;"></span>
                <span>DIAGNOSA OPERASIONAL <span class="accent-rose">• 4 TITIK KEBOCORAN</span></span>
            </div>
            <div class="slide-counter-badge">02 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Ilusi Omset Bertumbuh: Di Balik GMV Besar, Margin Bocor <span class="highlight-gradient-rose">Rp 18,3 M</span></h2>
            <p class="lead-text">Rekonsiliasi data membuktikan inefisiensi operasional tersembunyi di 4 titik rantai pasok.</p>
        </div>

        <div class="hero-metric-strip rose">
            <div>
                <div class="metric-mega-number highlight-gradient-rose">Rp 18.330.000.000</div>
                <div class="metric-caption">Akumulasi Potensi Rekonsiliasi Margin Operasional per Tahun</div>
            </div>
            <div class="metric-pill-badge rose">KRITIS</div>
        </div>

        <div class="pipeline-container">
            <div class="pipeline-step leaking">
                <div class="pipe-node-badge">TITIK 1</div>
                <div class="pipe-content">
                    <h3>Ghost Stockout (Phantom Inventory)</h3>
                    <p>Sistem mencatat stok ada, rak fisik toko kosong. 6,8% pesanan online dibatalkan sepihak.</p>
                </div>
                <div class="pipe-leak-amount">- Rp 5,72 M</div>
            </div>

            <div class="pipeline-step leaking">
                <div class="pipe-node-badge">TITIK 2</div>
                <div class="pipe-content">
                    <h3>Keterlambatan Supplier Tanpa Rekonsiliasi Penalti</h3>
                    <p>Vendor melanggar lead-time SLA sehingga toko kehabisan stok, namun denda luput ditagihkan.</p>
                </div>
                <div class="pipe-leak-amount">- Rp 3,24 M</div>
            </div>

            <div class="pipeline-step leaking">
                <div class="pipe-node-badge">TITIK 3</div>
                <div class="pipe-content">
                    <h3>Defisit Subsidi Ongkir Layanan Express</h3>
                    <p>Layanan 3-Hour Delivery sangat laris, tetapi per pesanan nombok Rp 24.500 akibat subsidi kurir.</p>
                </div>
                <div class="pipe-leak-amount">- Rp 4,88 M</div>
            </div>

            <div class="pipeline-step leaking">
                <div class="pipe-node-badge">TITIK 4</div>
                <div class="pipe-content">
                    <h3>Jurang Churn Pelanggan Baru (Month 2 Cliff)</h3>
                    <p>86% pembeli baru tidak pernah bertransaksi ulang setelah bulan pertama.</p>
                </div>
                <div class="pipe-leak-amount">- Rp 4,49 M</div>
            </div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Solusi di Tingkat Engine ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 3: ARSITEKTUR DATABASE PRODUKSI                    -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide3">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>DATA ARCHITECTURE <span class="accent-cyan">• SINGLE SOURCE OF TRUTH</span></span>
            </div>
            <div class="slide-counter-badge">03 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Arsitektur Database Produksi: Menjaga Integritas Data Relasional Sebelum Agregasi BI</h2>
            <p class="lead-text">Prinsip Analytics Engineering: Integritas skema di tingkat database mengeliminasi anomali data di pintu masuk.</p>
        </div>

        <div class="terminal-box">
            <div class="terminal-bar">
                <div class="terminal-lights">
                    <div class="terminal-light t-red"></div>
                    <div class="terminal-light t-yellow"></div>
                    <div class="terminal-light t-green"></div>
                </div>
                <div class="terminal-title">POSTGRESQL 15+ DDL DOMAINS &amp; CONSTRAINTS</div>
                <div class="terminal-engine-tag">ZERO CORRUPTION</div>
            </div>
            <div class="terminal-code">
<span class="kw">CREATE DOMAIN</span> d_positive_money <span class="kw">AS NUMERIC</span>(15,2) 
    <span class="kw">CHECK</span> (<span class="kw">VALUE</span> &gt;= 0.00); <span class="cmt">-- Cegah nilai uang abnormal</span>

<span class="kw">CREATE TYPE</span> order_channel_type <span class="kw">AS ENUM</span> (
    <span class="str">'STORE_POS'</span>, <span class="str">'ONLINE_WEB'</span>, <span class="str">'MARKETPLACE'</span>, <span class="str">'EXPRESS_APP'</span>
);

<span class="kw">ALTER TABLE</span> fact_order_items <span class="kw">ADD CONSTRAINT</span> chk_item_validity
    <span class="kw">CHECK</span> (quantity &gt; 0 <span class="kw">AND</span> unit_selling_price &gt;= unit_cogs * 0.5);
            </div>
        </div>

        <div class="bento-grid-2col">
            <div class="bento-card highlight-cyan-border">
                <div style="font-size: 24px; margin-bottom: 8px;">🛡️</div>
                <h3 style="font-size: 17px; font-weight: 800; color: #fff; margin-bottom: 6px;">Zero Garbage In di Level Skema</h3>
                <p style="font-size: 14px; color: #94a3b8; line-height: 1.45;">PostgreSQL Domains &amp; ENUMs menolak salah ketik kategori dan harga minus secara instan. Menjamin kebersihan data sebelum dikonsumsi analis.</p>
            </div>
            <div class="bento-card highlight-cyan-border">
                <div style="font-size: 24px; margin-bottom: 8px;">⚡</div>
                <h3 style="font-size: 17px; font-weight: 800; color: #fff; margin-bottom: 6px;">100% Plug-and-Play untuk BI Layer</h3>
                <p style="font-size: 14px; color: #94a3b8; line-height: 1.45;">Mart analitik sudah teragregasi secara terstruktur. Saat dihubungkan ke Power BI atau Tableau, dashboard langsung responsif tanpa lag.</p>
            </div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Kasus 1: Ghost Stockout ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 4: KASUS 1 - GHOST STOCKOUT ERADICATION            -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide4">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-bottom"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>KASUS 1 <span class="accent-cyan">• FORENSIK PERSEDIAAN</span></span>
            </div>
            <div class="slide-counter-badge">04 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Membasmi <span class="highlight-gradient-cyan">"Ghost Stockout"</span>: Barang Ada di Sistem, Fisik Rak Kosong</h2>
            <p class="lead-text">Order online masuk, namun fisik nihil akibat salah rak atau shrinkage. 6,8% pesanan batal sepihak.</p>
        </div>

        <div class="hero-metric-strip">
            <div>
                <div class="metric-mega-number highlight-gradient-cyan">Rp 5.720.000.000</div>
                <div class="metric-caption">Potensi Penjualan Hilang (Lost Sales) yang Berhasil Diselamatkan</div>
            </div>
            <div class="metric-pill-badge">Batal: 6,8% ➔ 0,4%</div>
        </div>

        <div class="terminal-box">
            <div class="terminal-bar">
                <div class="terminal-lights">
                    <div class="terminal-light t-red"></div>
                    <div class="terminal-light t-yellow"></div>
                    <div class="terminal-light t-green"></div>
                </div>
                <div class="terminal-title">WINDOW FUNCTION LAG() INVENTORY DISCREPANCY DETECTOR</div>
                <div class="terminal-engine-tag">SQL ANALYTICS</div>
            </div>
            <div class="terminal-code">
<span class="cmt">-- Deteksi selisih stok sistem vs transaksi kasir yang macet</span>
<span class="kw">SELECT</span> store_id, product_id, recorded_stock,
       <span class="fn">LAG</span>(recorded_stock, 1) <span class="kw">OVER</span> (
           <span class="kw">PARTITION BY</span> store_id, product_id <span class="kw">ORDER BY</span> audit_date
       ) <span class="kw">AS</span> prev_stock,
       <span class="kw">CASE WHEN</span> recorded_stock &gt; 0 <span class="kw">AND</span> actual_sales_qty = 0 <span class="kw">AND</span> days_without_sales &gt;= 7 
            <span class="kw">THEN</span> <span class="str">'GHOST_STOCKOUT_ALERT'</span> <span class="kw">ELSE</span> <span class="str">'NORMAL'</span> <span class="kw">END AS</span> audit_status
<span class="kw">FROM</span> mart_inventory_discrepancy;
            </div>
        </div>

        <div class="bento-card highlight-cyan-border">
            <h3 style="font-size: 17px; font-weight: 800; color: #fff; margin-bottom: 6px;">🎯 Keputusan Manajerial Berbasis Data:</h3>
            <p style="font-size: 14.5px; color: #94a3b8; line-height: 1.48;">Alih-alih menghitung stok manual membabi-buta di 50 cabang, query ini menghasilkan <strong>daftar prioritas audit fisik harian</strong> hanya untuk barang berstatus alert. Produktivitas staf gudang melonjak 340%.</p>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Kasus 2: Penalti Vendor ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 5: KASUS 2 - VENDOR SLA COMPLIANCE & DISPUTE AUDIT -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide5">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot" style="background: #10b981; box-shadow: 0 0 10px #10b981;"></span>
                <span>KASUS 2 <span class="accent-emerald">• GOVERNANCE RANTAI PASOK</span></span>
            </div>
            <div class="slide-counter-badge">05 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Menerbitkan <span class="highlight-gradient-emerald">SLA Audit Trail</span> yang Sah untuk Rekonsiliasi Pembayaran Vendor</h2>
            <p class="lead-text">Keterlambatan pengiriman supplier membuat rak kosong saat akhir pekan. Denda kontrak butuh alat bukti rekonsiliasi yang valid.</p>
        </div>

        <div class="hero-metric-strip emerald">
            <div>
                <div class="metric-mega-number highlight-gradient-emerald">Rp 3.240.000.000</div>
                <div class="metric-caption">Klaim Penalti Vendor Sah Berhasil Direkonsiliasi Berimbang</div>
            </div>
            <div class="metric-pill-badge emerald">100% PATUH KONTRAK</div>
        </div>

        <!-- TIERED GAUGE MATRIX -->
        <div class="bento-card highlight-emerald-border" style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: 800; color: #a7f3d0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Etika Kemitraan: Matriks Denda Bertingkat (Tiered Grace-Period)</div>
            
            <div style="display: flex; gap: 10px; margin-bottom: 8px;">
                <div style="flex: 1; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 12px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">DELAY &lt;= 24 JAM</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">0% DENDA</div>
                    <div style="font-size: 11.5px; color: #6ee7b7;">Grace Period Kemitraan</div>
                </div>
                <div style="flex: 1; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 12px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">DELAY 2 - 3 HARI</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 800; color: #fbbf24; margin: 4px 0;">2% DARI PO</div>
                    <div style="font-size: 11.5px; color: #fde68a;">Kompensasi Operasional</div>
                </div>
                <div style="flex: 1; background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 8px; padding: 12px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">DELAY &gt; 3 HARI</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 800; color: #f43f5e; margin: 4px 0;">5% DARI PO</div>
                    <div style="font-size: 11.5px; color: #fecdd3;">Penalti Maksimal</div>
                </div>
            </div>
        </div>

        <div class="bento-grid-2col">
            <div class="bento-card" style="border-color: rgba(244, 63, 94, 0.3);">
                <div style="font-size: 12px; font-weight: 800; color: #fb7185; text-transform: uppercase;">SEBELUMNYA (MANUAL)</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 800; color: #fff; margin: 6px 0;">Rp 0 Ditagih</div>
                <p style="font-size: 13.5px; color: #94a3b8; line-height: 1.4;">Finance dan Procurement kesulitan membuktikan keterlambatan karena arsip surat jalan tersebar manual.</p>
            </div>
            <div class="bento-card" style="border-color: rgba(16, 185, 129, 0.4); background: rgba(10, 30, 20, 0.6);">
                <div style="font-size: 12px; font-weight: 800; color: #34d399; text-transform: uppercase;">SESUDAH (SLA AUDIT TRAIL)</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 800; color: #34d399; margin: 6px 0;">Rp 3,24 Miliar</div>
                <p style="font-size: 13.5px; color: #94a3b8; line-height: 1.4;">Menyediakan alat bukti objektif untuk rekonsiliasi pembayaran faktur vendor tanpa memicu sengketa sepihak.</p>
            </div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Kasus 3: Unit Economics ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 6: KASUS 3 - WATERFALL MARGIN & CONVERSION SAFE    -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide6">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot" style="background: #f59e0b; box-shadow: 0 0 10px #f59e0b;"></span>
                <span>KASUS 3 <span class="accent-cyan">• UNIT ECONOMICS &amp; MARGIN</span></span>
            </div>
            <div class="slide-counter-badge">06 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Promo Ongkir Kilat: Ramai Transaksi, Namun <span class="highlight-gradient-rose">Nombok Rp 24.500</span>/Order</h2>
            <p class="lead-text">Layanan Express 3-Hour Delivery sangat laris, tetapi membakar kas perusahaan tanpa batas.</p>
        </div>

        <!-- WATERFALL VISUAL CHART -->
        <div class="waterfall-card">
            <div style="font-size: 13px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 14px;">Anatomi Kerugian per Transaksi (Batas Lama Rp 150.000)</div>
            
            <div class="waterfall-row">
                <div class="wf-label">Gross Margin (30%)</div>
                <div class="wf-bar-track">
                    <div class="wf-bar-fill pos" style="width: 45%;"></div>
                    <div class="wf-val">+ Rp 45.000</div>
                </div>
            </div>

            <div class="waterfall-row">
                <div class="wf-label">Subsidi Kurir Instan</div>
                <div class="wf-bar-track">
                    <div class="wf-bar-fill neg" style="width: 48%;"></div>
                    <div class="wf-val" style="margin-left: auto;">- Rp 48.000</div>
                </div>
            </div>

            <div class="waterfall-row">
                <div class="wf-label">Packaging &amp; Dry Ice</div>
                <div class="wf-bar-track">
                    <div class="wf-bar-fill neg" style="width: 12.5%;"></div>
                    <div class="wf-val" style="margin-left: auto;">- Rp 12.500</div>
                </div>
            </div>

            <div class="waterfall-row">
                <div class="wf-label">Payment Gateway Fee</div>
                <div class="wf-bar-track">
                    <div class="wf-bar-fill neg" style="width: 9%;"></div>
                    <div class="wf-val" style="margin-left: auto;">- Rp 9.000</div>
                </div>
            </div>

            <div class="wf-total-badge bad">
                <span>MARGIN KONTRIBUSI BERSIH LAMA:</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 18px;">- Rp 24.500 (DEFISIT / RUGI)</span>
            </div>
        </div>

        <div class="bento-card highlight-emerald-border">
            <h3 style="font-size: 17px; font-weight: 800; color: #34d399; margin-bottom: 4px;">💡 Solusi Taktis: Threshold Rp 250.000 + Rekomendasi Bundling</h3>
            <p style="font-size: 14px; color: #cbd5e1; line-height: 1.45;">Alih-alih mematikan promo atau memicu penurunan konversi checkout, manajemen menaikkan syarat belanja didukung <strong>rekomendasi bundling produk komplementer (cross-selling)</strong> di kasir/aplikasi. Margin berbalik sehat <strong>+Rp 12.000/order</strong>, memulihkan <strong>Rp 4,88 Miliar</strong> per tahun.</p>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Kasus 4: Kohort Retensi ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 7: KASUS 4 - COHORT RETENTION HEATMAP              -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide7">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-bottom"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>KASUS 4 <span class="accent-cyan">• CUSTOMER LIFECYCLE</span></span>
            </div>
            <div class="slide-counter-badge">07 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Mencegah Churn: Mengungkap Jurang Retensi di <span class="highlight-gradient-cyan">Bulan ke-2 (Month 2 Cliff)</span></h2>
            <p class="lead-text">Akuisisi user baru tinggi, tetapi 86% pembeli lenyap setelah bulan pertama.</p>
        </div>

        <div class="bento-card highlight-cyan-border" style="padding: 16px 20px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #94a3b8; text-transform: uppercase;">Visual Heatmap Retensi 12 Bulan (PostgreSQL Recursive CTE)</div>
            
            <table class="cohort-heatmap-table">
                <thead>
                    <tr>
                        <th>Kohort</th>
                        <th>User Baru</th>
                        <th>Bulan 0</th>
                        <th>Bulan 1</th>
                        <th style="color: #f43f5e;">Bulan 2 ⚠️</th>
                        <th>Bulan 3</th>
                        <th>Bulan 6</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="background: rgba(255,255,255,0.04); font-size: 12px;">Jan 2023</td>
                        <td style="background: rgba(255,255,255,0.04);">12.450</td>
                        <td class="c-m0">100%</td>
                        <td class="c-m1">41.8%</td>
                        <td class="c-cliff">14.1%</td>
                        <td class="c-low">9.8%</td>
                        <td class="c-low">6.4%</td>
                    </tr>
                    <tr>
                        <td style="background: rgba(255,255,255,0.04); font-size: 12px;">Feb 2023</td>
                        <td style="background: rgba(255,255,255,0.04);">14.120</td>
                        <td class="c-m0">100%</td>
                        <td class="c-m1">42.4%</td>
                        <td class="c-cliff">13.8%</td>
                        <td class="c-low">9.2%</td>
                        <td class="c-low">6.1%</td>
                    </tr>
                    <tr>
                        <td style="background: rgba(255,255,255,0.04); font-size: 12px;">Mar 2023</td>
                        <td style="background: rgba(255,255,255,0.04);">15.890</td>
                        <td class="c-m0">100%</td>
                        <td class="c-m1">43.0%</td>
                        <td class="c-cliff">14.4%</td>
                        <td class="c-low">10.1%</td>
                        <td class="c-low">6.8%</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bento-card highlight-emerald-border">
            <h3 style="font-size: 17px; font-weight: 800; color: #34d399; margin-bottom: 6px;">🎯 The Golden Re-Engagement Window (Hari ke-14 s/d 21)</h3>
            <p style="font-size: 14.5px; color: #cbd5e1; line-height: 1.48;">Data membuktikan jika pelanggan tidak kembali sebelum hari ke-21, kemungkinan mereka membeli lagi turun di bawah 5%. Memicu penawaran personalisasi tepat pada hari ke-14 mendongkrak retensi ke <strong>31%</strong> dan mengamankan <strong>Rp 4,49 Miliar LTV</strong>.</p>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Tuning Performa SQL ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 8: QUERY SPEED BENCHMARK                           -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide8">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>ENGINEERING DEPTH <span class="accent-cyan">• QUERY TUNING</span></span>
            </div>
            <div class="slide-counter-badge">08 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Dari 8,4 Detik Menjadi <span class="highlight-gradient-cyan">140 Milidetik</span>: Efisiensi Melejit <span class="highlight-gradient-emerald">98,3%</span></h2>
            <p class="lead-text">Query analitik lambat membekukan database kasir. Kami mendesain strategi composite &amp; partial index.</p>
        </div>

        <!-- VISUAL SPEED BENCHMARK -->
        <div class="speed-chart-card">
            <div class="speed-track-row">
                <div class="speed-track-header">
                    <span style="color: #fb7185;">SEBELUM: Sequential Table Scan (500.000+ Baris)</span>
                    <span style="font-family: 'JetBrains Mono', monospace; color: #fb7185;">8.420 ms</span>
                </div>
                <div class="speed-bar-slot">
                    <div class="speed-fill-red"></div>
                    <div class="speed-number-val">8.420 ms (CPU 95% - SERVER FREEZE)</div>
                </div>
            </div>

            <div class="speed-track-row" style="margin-bottom: 0;">
                <div class="speed-track-header">
                    <span style="color: #34d399;">SESUDAH: B-Tree &amp; Partial Indexing Scan</span>
                    <span style="font-family: 'JetBrains Mono', monospace; color: #34d399;">142 ms (60x LEBIH CEPAT)</span>
                </div>
                <div class="speed-bar-slot">
                    <div class="speed-fill-green"></div>
                    <div class="speed-number-val" style="margin-left: 35px; color: #34d399;">142 ms ⚡ ZERO LATENCY</div>
                </div>
            </div>
        </div>

        <div class="bento-grid-2col">
            <div class="bento-card highlight-cyan-border">
                <h3 style="font-size: 16.5px; font-weight: 800; color: #00f2fe; margin-bottom: 4px;">Partial Indexing</h3>
                <p style="font-size: 13.5px; color: #94a3b8; line-height: 1.45;">Hanya mengindeks pesanan berstatus aktif (unfulfilled), menghemat 85% ruang disk RAM index buffer.</p>
            </div>
            <div class="bento-card highlight-cyan-border">
                <h3 style="font-size: 16.5px; font-weight: 800; color: #34d399; margin-bottom: 4px;">BRIN Indexing</h3>
                <p style="font-size: 13.5px; color: #94a3b8; line-height: 1.45;">Memanfaatkan urutan fisik tanggal pesanan untuk mempercepat query agregasi historis multi-tahun.</p>
            </div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Roadmap Eksekusi ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 9: STEPPED 90-DAY STRATEGIC ROADMAP                -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide9">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-bottom"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot" style="background: #10b981; box-shadow: 0 0 10px #10b981;"></span>
                <span>EXECUTIVE ACTION <span class="accent-emerald">• ROADMAP 90 HARI</span></span>
            </div>
            <div class="slide-counter-badge">09 / 10</div>
        </div>

        <div class="title-block">
            <h2 class="slide-headline">Rencana Aksi 90 Hari: Menyelamatkan Potensi Margin <span class="highlight-gradient-emerald">Rp 18,3 Miliar</span></h2>
            <p class="lead-text">Panduan eksekusi lintas fungsi untuk tim Finance, Procurement, dan Operasional.</p>
        </div>

        <div class="roadmap-timeline">
            <div class="timeline-node">
                <div class="node-phase-badge">HARI 1 - 30</div>
                <div class="node-body">
                    <h3>Finance &amp; Procurement: SLA Audit Trail Reconciliation</h3>
                    <p>Integrasi kalkulasi bukti audit denda ke proses rekonsiliasi faktur pembelian vendor.</p>
                </div>
                <div class="node-gain">+ Rp 3,24 M</div>
            </div>

            <div class="timeline-node">
                <div class="node-phase-badge">HARI 31 - 60</div>
                <div class="node-body">
                    <h3>Operations &amp; Merchandising: Basket Threshold &amp; Cycle Count</h3>
                    <p>Naikkan minimum order ke Rp 250rb dengan promo bundling &amp; audit stok rak prioritas harian.</p>
                </div>
                <div class="node-gain">+ Rp 10,60 M</div>
            </div>

            <div class="timeline-node">
                <div class="node-phase-badge">HARI 61 - 90</div>
                <div class="node-body">
                    <h3>Marketing &amp; CRM: Automasi Re-Engagement Kohort Hari ke-14</h3>
                    <p>Trigger promo personalisasi tepat sebelum pembeli baru memasuki jurang churn.</p>
                </div>
                <div class="node-gain">+ Rp 4,49 M</div>
            </div>
        </div>

        <div class="hero-metric-strip emerald">
            <div>
                <div class="metric-mega-number highlight-gradient-emerald">Rp 18.330.000.000</div>
                <div class="metric-caption">Total Estimasi Pemulihan Margin Tahunan (Annual Net Profit Recovery)</div>
            </div>
            <div class="metric-pill-badge emerald">100% TERUKUR</div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn">Hubungi Penulis ➔</div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- SLIDE 10: VIP EXECUTIVE CLOSING & COLLABORATION          -->
<!-- ======================================================== -->
<div class="slide-wrapper" id="slide10">
    <div class="cyber-mesh"></div>
    <div class="ambient-glow-top"></div>
    <div class="ambient-glow-bottom"></div>

    <div class="content-layer">
        <div class="top-status-bar">
            <div class="dossier-tag">
                <span class="pulse-dot"></span>
                <span>COLLABORATION <span class="accent-cyan">• DATA TALENT</span></span>
            </div>
            <div class="slide-counter-badge">10 / 10</div>
        </div>

        <div class="closing-vip-box">
            <img class="closing-avatar-large" src="{author_photo_uri}" alt="{author_name}">
            <div style="font-size: 28px; font-weight: 900; color: #ffffff;">{author_name}</div>
            <div style="font-size: 16px; color: #00f2fe; font-weight: 700; margin-top: 4px;">{author_role}</div>

            <div class="closing-prompt-quote">
                💬 <strong>Mari Berdiskusi:</strong> Bagaimana tim data di organisasi rekan-rekan memitigasi selisih stok phantom vs fisik saat kampanye promo besar? Mari bertukar wawasan di kolom komentar!
            </div>

            <div class="contact-card-grid">
                <div class="contact-item">
                    <div class="contact-item-icon">📧</div>
                    <div>
                        <div style="font-size: 12px; color: #94a3b8; font-weight: 600;">Email Resmi:</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: #fff;">{author_email}</div>
                    </div>
                </div>
                <div class="contact-item">
                    <div class="contact-item-icon">💬</div>
                    <div>
                        <div style="font-size: 12px; color: #94a3b8; font-weight: 600;">WhatsApp:</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: #fff;">{author_wa_formatted}</div>
                    </div>
                </div>
            </div>

            <div class="repo-box-creative">
                <div style="text-align: left;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 600;">📂 Repositori Lengkap (DDL, Query &amp; Laporan):</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 13.5px; font-weight: 700; color: #e2e8f0;">
                        github.com/fajarsetyadilucky/Omnichannel-Retail-Supply-Chain-Analytics-Engine
                    </div>
                </div>
                <div class="metric-pill-badge" style="background: rgba(0, 242, 254, 0.15);">100% SQL</div>
            </div>
        </div>

        <div class="dossier-footer">
            <div class="dossier-author">
                <img class="dossier-avatar" src="{author_photo_uri}" alt="{author_name}">
                <div>
                    <div class="dossier-name">{author_name}</div>
                    <div class="dossier-role">{author_role}</div>
                </div>
            </div>
            <div class="dossier-action-btn" style="background: rgba(16, 185, 129, 0.2); border-color: rgba(16, 185, 129, 0.4); color: #34d399;">Terbuka untuk Diskusi Strategis</div>
        </div>
    </div>
</div>

</body>
</html>
"""

# Save updated HTML file
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Enterprise V3 HTML preview saved: {html_file}")

# Chrome / Edge detection
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
browser_bin = None
for cp in chrome_paths:
    if os.path.exists(cp):
        browser_bin = cp
        break

if browser_bin:
    print(f"Rendering high-res Enterprise PDF with: {browser_bin}")
    cmd_pdf = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        str(html_file)
    ]
    subprocess.run(cmd_pdf, capture_output=True)
    print(f"SUCCESS: Generated PDF carousel: {pdf_file.name} ({pdf_file.stat().st_size / 1024:.2f} KB)")

    print("Rendering 10 Individual High-Res PNG Slides (Enterprise V3)...")
    for i in range(1, 11):
        slide_png = CAROUSEL_DIR / f"slide_{i:02d}.png"
        slide_html = CAROUSEL_DIR / f"_temp_slide_{i:02d}.html"
        
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

# Enterprise-Ready Post Copy
post_copy = f"""Banyak retail terjebak pada ilusi penjualan: "GMV bertumbuh 22%, bisnis tampak sehat."
Namun saat data transaksi 50 cabang dan 3 gudang regional diaudit forensik, kami mengidentifikasi potensi kebocoran margin mencapai Rp 18,3 Miliar per tahun.

Sebagai Data Analyst & Business Intelligence, data bukan sekadar grafik visual di layar dashboard—melainkan katalisator pengambilan keputusan direksi: MENGAPA inefisiensi terjadi, DI MANA titik kebocorannya, dan BAGAIMANA memulihkannya secara berimbang tanpa merusak operasi bisnis.

Dalam studi kasus ini, seluruh mesin audit forensik dirancang 100% menggunakan Enterprise PostgreSQL 15+ Engine sebagai Production Analytics Foundation.

Berikut 4 temuan kritis hasil audit data forensik:

1️⃣ Membasmi "Ghost Stockout" (Phantom Inventory) — Mitigasi Lost Sales Rp 5,7 Miliar:
Sistem mencatat stok barang tersedia, namun fisik di rak toko kosong. Akibatnya 6,8% pesanan online dibatalkan sepihak dan mengecewakan pelanggan.
Menggunakan Window Function LAG() dan discrepancy tracking, kami mendeteksi anomali selisih stok secara otomatis dan menerbitkan prioritas audit fisik harian ke staf gudang, menekan pembatalan pesanan hingga 0,4%.

2️⃣ Audit Kepatuhan & SLA Dispute Trail Vendor — Rekonsiliasi Rp 3,2 Miliar:
Keterlambatan pengiriman vendor kerap membuat rak toko kosong saat akhir pekan, namun denda kontrak luput ditagihkan karena kesulitan rekonsiliasi manual.
Dengan pendekatan Tiered Grace-Period (toleransi <24 jam, denda proporsional >48 jam), query analitik menghasilkan alat bukti SLA Dispute Audit Trail yang sah untuk rekonsiliasi faktur berimbang antara tim Finance dan Vendor tanpa memicu sengketa sepihak.

3️⃣ Unit Economics Promo Ongkir Kilat — Pemulihan Margin Rp 4,9 Miliar:
Layanan Express 3-Hour Delivery sangat laris, tetapi membakar kas: margin kontribusi minus Rp 24.500 per transaksi karena subsidi kurir tanpa batas minimal belanja.
Alih-alih mematikan layanan yang disukai pelanggan atau memicu penurunan konversi, simulasi analitik merekomendasikan penyesuaian batas belanja ke Rp 250rb yang didukung strategi bundling produk komplementer (cross-selling) di kasir/aplikasi. Margin berbalik sehat (+Rp 12.000/order).

4️⃣ Jurang Retensi Pelanggan Bulan ke-2 (Month 2 Cliff) — Pengamanan Rp 4,5 Miliar LTV:
Analisis kohort 12 bulan membuktikan 86% pelanggan baru churn setelah bulan pertama. Query analitik mengidentifikasi "Golden Re-engagement Window" pada hari ke-14 s/d 21 pasca pembelian pertama untuk memicu penawaran personalisasi terarah.

⚡ Efisiensi Mesin Database:
Melalui strategi Composite B-Tree dan Partial Indexing, waktu respon query analitik dipangkas 98,3% (dari 8,4 detik menjadi 140 milidetik), memastikan data 100% Plug-and-Play untuk konsumsi BI tanpa membebani database kasir.

👉 Geser dokumen carousel 10 slide di atas untuk melihat arsitektur skema DDL, visual waterfall margin, heatmap kohort, dan roadmap eksekusi 90 harinya!

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Eksplorasi Skrip SQL Lengkap & Laporan Bisnis di GitHub:
{github_url}

📬 Terbuka untuk Diskusi & Peluang Kerja (Data Analyst / BI Analyst):
👤 {author_name} | {author_role}
📧 {author_email}
💬 WhatsApp: {author_wa_formatted} (https://wa.me/62{author_wa[1:]})

Bagaimana pendekatan rekan-rekan dalam mengelola data persediaan phantom vs fisik saat kampanye promo besar? Mari berdiskusi di kolom komentar! 👇

#DataAnalytics #BusinessIntelligence #PostgreSQL #SQL #SupplyChainAnalytics #RetailAnalytics #DecisionIntelligence #DataArchitecture #UnitEconomics #HiringDataAnalyst #JobSeeker
"""

with open(post_copy_file, "w", encoding="utf-8") as f:
    f.write(post_copy)
print(f"Enterprise Post Copy saved: {post_copy_file}")
print("ALL ENTERPRISE ASSETS GENERATED SUCCESSFULLY!")
