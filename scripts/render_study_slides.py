#!/usr/bin/env python3
"""
Foils & Founders: 81-Slide Widescreen Study Deck Renderer (16:9 HTML + Print PDF)
=================================================================================
Joins `decks/cards.yaml` + `decks/study_cards.yaml` (80 cards) and prepends Slide 1 (Title & Rule Zero
Architecture) to generate a 81-slide interactive HTML5/MathJax presentation:
  - Layout per Card Slide (1920x1080 16:9 aspect ratio):
      * Top Banner: Card ID, Deck Badge, Title, Subtitle, Cost, & Mana Tier
      * Upper-Left Vertical Panel: Tabletop Play Text (Dual Narratives, Effect,
        Impact Metrics, Synergy & Counter Badges)
      * Upper-Right Vertical Panel: Empirical Study Text (Primary Citations,
        Empirical Evidence, Proof Bridge, & MATLAB/Python Codebase Hooks)
      * Full-Width Bottom Stage (Left-to-Right): High-visibility MathJax LaTeX
        Display Equation spanning the entire horizontal width of the slide.
  - Controls: Left/Right Arrow keys, Spacebar, Slide Picker, or Cmd+P to export
    all 81 slides as a widescreen Landscape PDF.

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations
import html
import re
from pathlib import Path
from typing import Any, Dict, List
import yaml

ROOT = Path(__file__).resolve().parent.parent
CARDS_YAML = ROOT / "decks" / "cards.yaml"
DECK_YAML = ROOT / "decks" / "study_cards.yaml"
OUT_DIR = ROOT / "output"
OUT_HTML = OUT_DIR / "foils_and_founders_study_slides.html"


# Inverse-Hub Base Mana mapping from Foils & Founders Gameplay Rules
TIER_1_HUBS = {"B:00", "B:01", "B:02", "B:05", "E:01", "N:01", "N:02"}
TIER_2_BRIDGES = {
    "B:03", "B:04", "B:07", "C:01", "C:02", "C:03", "C:05",
    "N:03", "N:04", "N:05", "K:01", "K:02", "K:03", "K:04", "K:05",
}
TIER_3_CAPSTONES = {
    "B:06", "B:08", "B:09", "C:04", "C:06", "E:02", "E:03", "N:06", "K:06", "K:07",
}

DECK_COLORS: Dict[str, Dict[str, str]] = {
    "B": {"name": "Base Lifecycle & Fiscal Gate", "accent": "#2A9D8F", "bg": "#0A2229", "badge": "#14453D"},
    "T": {"name": "Cautionary Trap & Spoiler", "accent": "#FF595E", "bg": "#2B0F18", "badge": "#591623"},
    "C": {"name": "Climate, Cohesion & Resilience", "accent": "#00B4D8", "bg": "#0B2135", "badge": "#123C5E"},
    "K": {"name": "Wayfinder Kaupapa Persona", "accent": "#F4C97E", "bg": "#241B0B", "badge": "#4A3512"},
    "N": {"name": "Nobel & Institutional Archive", "accent": "#B5838D", "bg": "#1F162B", "badge": "#3D2652"},
    "H": {"name": "Orthodoxy Boss Hazard", "accent": "#F77F00", "bg": "#2B1808", "badge": "#572F0D"},
    "E": {"name": "Energy & Epistemic Operators", "accent": "#80ED99", "bg": "#0B261C", "badge": "#164A36"},
    "P": {"name": "Open-Source Wildcards & Sockets", "accent": "#94A3B8", "bg": "#111827", "badge": "#334155"},
}



from render_math import (
    get_mathjax_svg_fit_css,
    pick_eq_size_class,
    resolve_card_latex,
)


def get_mana_badge(card: Dict[str, Any]) -> str:
    cid = str(card.get("id", "X:00"))
    prefix = cid.split(":")[0]
    kickback = card.get("feral_kickback_wealth")
    if prefix in ("T", "H"):
        kb = f" • Mode B: +{kickback}W" if kickback is not None else ""
        return f"Hazard / Orthodoxy Boss{kb}"
    mtier = card.get("mana_tier")
    bmana = card.get("base_mana")
    if mtier is not None and bmana is not None:
        return f"Tier {mtier} • Base: {bmana} Mana (2x SS1 / 3x SS2)"
    return "Wayfinder / Policy Asset • Base: 2 Mana"


def esc(text: Any) -> str:
    return "" if text is None else html.escape(str(text), quote=True)


def format_inline_text(text: Any) -> str:
    return "" if not text else html.escape(str(text), quote=False)


def build_title_slide_html(total_slides: int) -> str:
    return f"""
    <section class="slide active" data-slide="1" style="--accent: #F4C97E; --panel-bg: #0D2238; --badge-bg: #18395A;">
      <header class="slide-header">
        <div class="header-left">
          <span class="card-id-pill">SLIDE 01 / {total_slides:02d}</span>
          <span class="deck-pill">FOILS &amp; FOUNDERS: THE AOTEAROA STUDY DECK</span>
        </div>
        <div class="header-titles">
          <h1>Beyond the Magic Money Tree — Foils &amp; Founders</h1>
          <p class="subtitle">Rule Zero (B:00): &ldquo;Not all lives are easy, but none should be impossible.&rdquo;</p>
        </div>
        <div class="header-right">
          <div class="cost-box">20 Turns • &Delta;t = 3 Yrs/Turn</div>
          <div class="mana-box">Coopetitive OLG Tabletop &amp; Study Deck</div>
        </div>
      </header>

      <div class="columns-container">
        <!-- LEFT VERTICAL: PLAY & MECHANICS -->
        <div class="col-panel play-panel">
          <div class="panel-tag">LEFT VERTICAL PANEL • TABLETOP GAMEPLAY ARCHITECTURE</div>
          <div class="lens-box foil-lens">
            <div class="lens-title">&#9973; Hull A — Up on Foils (Systems &amp; Hydrofoil Engineering)</div>
            <p>Lift Aotearoa from high-drag <strong>SS0 Displacement Mode</strong> (81.0 Cohesion, 22%–30% child hardship corner, approaching 200% Debt/GDP) onto <strong>SS1</strong> (2x Mana) and <strong>SS2 Hydrofoils</strong> (3x Mana, 126.0 Cohesion, 18.25% PAYE, Super @ Age 64) by interlocking three Subsystems: <strong>1. Front Foil (B:01+B:03)</strong>, <strong>2. Wing-Sail (B:08+B:05/B:06+C:09+E:01/E:02)</strong>, and <strong>3. Rear T-Foil (B:09+B:14/B:15)</strong>.</p>
          </div>
          <div class="lens-box waka-lens">
            <div class="lens-title">&#128758; Hull B — Te Waka Hourua (Double-Hulled Voyaging &amp; Mana)</div>
            <p>Players steward multi-generational characters across <strong>Being</strong> (<em>Tamariki</em>, ages 0–17), <strong>Becoming</strong> (<em>Pakeke</em>, ages 18–62), and <strong>Crossing Over</strong> (<em>Kaumātua</em>, ages 63–89 &rarr; Rebirth at $J=0$ via the Rawlsian D20). Expose cards to <strong>The River</strong> (+1 Generosity), collect persistent <strong>Variant B Royalties</strong>, and stake <strong>Contingent Mana</strong> at risk.</p>
          </div>
          <div class="mechanic-box">
            <div class="box-label">THREE-PILLAR "SCRABBLE" VICTORY &amp; DUAL RULESET</div>
            <p>Compete for <strong>1) Mana Laureate (<em>Toa Takitini</em>)</strong> and <strong>2) Wealth Laureate (<em>Pou Rawa</em>)</strong> while maximizing <strong>3) The Combined National Score ($\\Sigma_{{\\text{{Aotearoa}}}}$)</strong> and out-sailing <strong>Finland (88.0 &rarr; 107.2)</strong>. Play in <em>Abundance Mode</em> (clearing D20 reefs 1–6 &amp; 19–20) or <em>Feral Spoiler Mode</em> (Judo-countering rent-seekers).</p>
          </div>
        </div>

        <!-- RIGHT VERTICAL: EMPIRICAL & OLG ENGINE -->
        <div class="col-panel study-panel">
          <div class="panel-tag">RIGHT VERTICAL PANEL • EMPIRICAL &amp; OLG MODEL ARCHITECTURE</div>
          <div class="study-block">
            <div class="box-label">8-PTYPE &times; 4-REGION GENERAL EQUILIBRIUM GPU ENGINE</div>
            <p>Every card in this 81-slide deck compiles a formal theorem and calibrated parameter from the companion <strong>IGWelfare</strong> MATLAB/Python codebase (<code>NZ_4Region_Master.m</code>, <code>PolicyExperiment_LeeSeshadri_4Region.m</code>, <code>QEA_2026.m</code>) and empirical longitudinal microdata.</p>
          </div>
          <div class="study-block">
            <div class="box-label">CORE EMPIRICAL ANCHORS ACROSS ALL 80 CARDS</div>
            <ul class="cite-list">
              <li><strong>Dunedin Multidisciplinary Study (Poulton et al. 2015) &amp; GUiNZ (Morton et al. 2023):</strong> 22% ($d20: 1\\text{{--}}4$) to 30% ($d20: 1\\text{{--}}6$) early subsistence corner ($\\Pr(i_c=0)$) &amp; 80/20 concentration of $50.5B/yr fiscal drag.</li>
              <li><strong>Cunha, Heckman, &amp; Schennach (2010) &amp; Lee &amp; Seshadri (2019):</strong> Multi-stage CES dynamic complementarity ($\\phi_1 = -0.50$) proving 6.8:1 ROI on Gate 1–2 vs. late remediation collapse.</li>
              <li><strong>Guvenen et al. (2023) &amp; Murphy, Shleifer, &amp; Vishny (1991):</strong> Use-It-Or-Lose-It wealth/estate tax shift rotating capital from passive land ($z_\\ell$) to high-return builders ($z_h$, <code>20:01</code>–<code>20:19</code>).</li>
              <li><strong>Williamson (2009), Ostrom (2010), &amp; Romer (1990):</strong> Polycentric governance, ACC Year-5 actuarial breakeven ($3.84\\times$), and non-rival knowledge spillovers.</li>
            </ul>
          </div>
          <div class="code-hook-bar">
            <span><strong>Navigation:</strong> Use <code>&larr;</code> / <code>&rarr;</code> keys, click the bottom controls, or press <code>Cmd+P</code> to save all 81 slides to PDF.</span>
          </div>
        </div>
      </div>

      <!-- FULL-WIDTH BOTTOM EQUATION STAGE -->
      <footer class="equation-stage">
        <div class="eq-header">
          <span class="eq-tag">MASTER THREE-PILLAR SCRABBLE &amp; RAWLSIAN SOCIAL WELFARE OBJECTIVE FUNCTION (OLG STATIONARY DISTRIBUTION $\\mu^\\star$)</span>
          <span class="slide-num-badge">Slide 1 of {total_slides}</span>
        </div>
        <div class="eq-display">
          $$\\mathcal{{W}}(\\mu^\\star) = \\int_{{\\mathcal{{S}}}} V_1(s) \\, d\\mu^\\star(s) \\xrightarrow{{\\text{{SS0}} \\to \\text{{SS2}}}} +20.49\\% \\text{{ CE Welfare}}, \\qquad \\Sigma_{{\\text{{Aotearoa}}}} = \\left( \\sum_{{i=1}}^{{P}} \\mathcal{{M}}_i + \\sum_{{i=1}}^{{P}} \\mathcal{{W}}_i \\right) \\times \\Gamma_{{\\text{{Regime}}}} \\;\\; \\Big(\\bar{{\\Sigma}}_{{\\text{{Target}}}} \\ge 135\\text{{ pts/player}}\\Big)$$
        </div>
      </footer>
    </section>
    """


def build_card_slide_html(card: Dict[str, Any], slide_idx: int, total_slides: int) -> str:
    cid = str(card.get("id", "X:00"))
    deck_code = cid.split(":")[0] if ":" in cid else "B"
    theme = DECK_COLORS.get(deck_code, DECK_COLORS["B"])

    title = format_inline_text(card.get("name") or card.get("title") or cid)
    subtitle = format_inline_text(card.get("type") or card.get("subtitle") or "")
    cost = format_inline_text(card.get("cost_or_requirement") or card.get("cost") or "")
    mana_info = get_mana_badge(card)

    effects = card.get("effects") or []
    eff_1 = f"<strong>{esc(effects[0].get('label',''))}:</strong> {format_inline_text(effects[0].get('rule',''))}" if len(effects) >= 1 else ""
    eff_2 = f"<strong>{esc(effects[1].get('label',''))}:</strong> {format_inline_text(effects[1].get('rule',''))}" if len(effects) >= 2 else ""
    flavor = format_inline_text(card.get("flavor_text", ""))

    synergies: List[str] = card.get("synergy_links") or card.get("synergy_cards") or []
    key_params: List[str] = card.get("key_parameters") or []
    citations: List[str] = card.get("references") or []
    evidence = format_inline_text(card.get("empirical_evidence") or card.get("empirical_anchor") or "")
    proof_bridge = format_inline_text(card.get("tabletop_bridge", ""))
    vfi_mod = str(card.get("vfi_module", ""))
    latex_eq = resolve_card_latex(card, cid)

    impact_html = "".join(
        f'<div class="impact-item"><span class="imp-k">▸ </span><span class="imp-v">{format_inline_text(p)}</span></div>'
        for p in key_params[:4]
    )
    syn_pills = "".join(f'<span class="syn-pill">{esc(s)}</span>' for s in synergies) or '<span class="none-pill">None</span>'
    cite_items = "".join(f"<li>{format_inline_text(c)}</li>" for c in citations[:5])
    code_pills = f'<code class="code-pill">{esc(vfi_mod)}</code>' if vfi_mod else ""

    eq_size_class = pick_eq_size_class(latex_eq)

    return f"""
    <section class="slide" data-slide="{slide_idx}" data-card-id="{esc(cid)}"
             style="--accent: {theme['accent']}; --panel-bg: {theme['bg']}; --badge-bg: {theme['badge']};">
      <header class="slide-header">
        <div class="header-left">
          <span class="card-id-pill">{esc(cid)}</span>
          <span class="deck-pill">{esc(deck_code)} SUITE • {esc(theme['name'].upper())}</span>
        </div>
        <div class="header-titles">
          <h1>{title}</h1>
          <p class="subtitle">{subtitle}</p>
        </div>
        <div class="header-right">
          <div class="cost-box"><strong>Cost / Req:</strong> {cost}</div>
          <div class="mana-box">{esc(mana_info)}</div>
        </div>
      </header>

      <div class="columns-container">
        <div class="col-panel play-panel">
          <div class="panel-tag">PLAY SIDE (FRONT) • MECHANICS, CALIBRATED PARAMETERS &amp; SYNERGIES</div>
          <div class="lens-box foil-lens">
            <div class="lens-title">&#9973; Primary Mechanic</div>
            <p>{eff_1}</p>
          </div>
          <div class="lens-box waka-lens">
            <div class="lens-title">&#128758; Coupled / Second-Order Mechanic</div>
            <p>{eff_2 or flavor}</p>
          </div>
          <div class="mechanic-box">
            <div class="box-label">FLAVOR &amp; POLITICAL-ECONOMY INSIGHT</div>
            <p>&ldquo;{flavor}&rdquo;</p>
          </div>
          <div class="impact-grid">{impact_html}</div>
          <div class="badges-footer">
            <div class="badge-group">
              <span class="badge-group-title">SYNERGY LINKS (RIVER COMBOS):</span>
              {syn_pills}
            </div>
          </div>
        </div>

        <div class="col-panel study-panel">
          <div class="panel-tag">STUDY SIDE (FOLD-OVER BACK) • EMPIRICAL EVIDENCE &amp; PROOF BRIDGE</div>
          <div class="study-block">
            <div class="box-label">PRIMARY ACADEMIC &amp; EMPIRICAL CITATIONS</div>
            <ul class="cite-list">{cite_items}</ul>
          </div>
          <div class="study-block evidence-block">
            <div class="box-label">CALIBRATED EMPIRICAL EVIDENCE ({esc(card.get('economic_concept', ''))})</div>
            <p>{evidence}</p>
          </div>
          <div class="study-block bridge-block">
            <div class="box-label">THEOREM-TO-TABLETOP PROOF BRIDGE</div>
            <p>{proof_bridge}</p>
          </div>
          <div class="code-hook-bar">
            <span class="code-hook-label">24-File GPU Solver Module:</span>
            {code_pills}
          </div>
        </div>
      </div>

      <footer class="equation-stage">
        <div class="eq-header">
          <span class="eq-tag">FORMAL MATHEMATICAL / ECONOMETRIC SPECIFICATION ({esc(cid)})</span>
          <span class="slide-num-badge">Slide {slide_idx} of {total_slides}</span>
        </div>
        <div class="eq-display {eq_size_class}">
          $${latex_eq}$$
        </div>
      </footer>
    </section>
    """


def build_deck_html(cards: List[Dict[str, Any]]) -> str:
    total_slides = len(cards) + 1  # Slide 1 (Title/Legend) + 44 Cards = 45 Slides
    slides_html = [build_title_slide_html(total_slides)]

    options_html = ['<option value="1">01 — Title &amp; Rule Zero Architecture</option>']
    for idx, card in enumerate(cards, start=2):
        slides_html.append(build_card_slide_html(card, idx, total_slides))
        cid = esc(card.get("id", ""))
        ctitle = esc(card.get("name") or card.get("title") or "")
        options_html.append(f'<option value="{idx}">{idx:02d} — [{cid}] {ctitle}</option>')

    all_slides_str = "\n".join(slides_html)
    all_options_str = "\n".join(options_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Foils &amp; Founders — 81-Slide Study Deck (Play Left | Study Right | Full-Width Equations)</title>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    :root {{
      --bg-dark: #050C16;
      --text-main: #F1FAEE;
      --text-muted: #A8DADC;
      --gold: #F4C97E;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}

    /* 16:9 Widescreen Viewport Stage (Balanced Container-Proportional Midpoint) */
    #deck-viewport {{
      width: min(96vw, calc((100vh - 52px) * 16 / 9));
      aspect-ratio: 16 / 9;
      position: relative;
      container-type: size;
    }}

    .slide {{
      display: none;
      width: 100%;
      height: 100%;
      background: linear-gradient(145deg, #071324 0%, #0B1D33 55%, #081C24 100%);
      border: 2.5px solid var(--accent, #00B4D8);
      border-radius: 12px;
      padding: 0.95% 1.3%;
      flex-direction: column;
      gap: 0.8%;
      justify-content: space-between;
      box-shadow: 0 18px 50px rgba(0,0,0,0.75);
      overflow: hidden;
    }}
    .slide.active {{
      display: flex;
    }}

    /* TOP SLIDE HEADER (Centered vertically, expands gently if title wraps to 2 lines) */
    .slide-header {{
      display: grid;
      grid-template-columns: 22% 52% 26%;
      align-items: center;
      background: rgba(8, 22, 38, 0.9);
      border-bottom: 2px solid var(--accent);
      border-radius: 8px;
      padding: 0.48% 1.1%;
      min-height: 11.8%;
      max-height: 14.5%;
      flex-shrink: 0;
    }}
    .header-left {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      align-items: flex-start;
    }}
    .card-id-pill {{
      background: var(--accent);
      color: #04101E;
      font-weight: 900;
      font-size: clamp(10px, 1.38cqw, 24px);
      padding: 2px 11px;
      border-radius: 6px;
      letter-spacing: 1px;
    }}
    .deck-pill {{
      font-size: clamp(7.5px, 0.74cqw, 13px);
      color: var(--gold);
      font-weight: 700;
      letter-spacing: 0.6px;
    }}
    .header-titles {{
      text-align: center;
      padding: 0 8px;
    }}
    .header-titles h1 {{
      font-size: clamp(12px, 1.54cqw, 28px);
      color: #FFFFFF;
      line-height: 1.12;
    }}
    .header-titles .subtitle {{
      font-size: clamp(8.5px, 0.90cqw, 16px);
      color: var(--gold);
      font-family: Georgia, serif;
      font-style: italic;
      margin-top: 2px;
      line-height: 1.15;
    }}
    .header-right {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 3px;
      text-align: right;
    }}
    .cost-box {{
      background: var(--badge-bg);
      border: 1px solid var(--accent);
      color: #FFFFFF;
      font-size: clamp(8px, 0.78cqw, 14px);
      padding: 2.5px 9px;
      border-radius: 5px;
      line-height: 1.18;
    }}
    .mana-box {{
      font-size: clamp(7.5px, 0.74cqw, 13px);
      color: #80ED99;
      font-weight: 700;
    }}

    /* MIDDLE SPLIT VERTICAL COLUMNS: PLAY LEFT | STUDY RIGHT */
    .columns-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.15%;
      flex: 1 1 auto;
      min-height: 0;
      margin: 0;
    }}
    .col-panel {{
      background: rgba(11, 29, 51, 0.78);
      border: 1.5px solid rgba(168, 218, 220, 0.28);
      border-radius: 10px;
      padding: 1.3% 1.7%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }}
    .play-panel {{
      border-left: 5px solid var(--accent);
    }}
    .study-panel {{
      border-left: 5px solid var(--gold);
      background: rgba(15, 25, 42, 0.84);
    }}
    .panel-tag {{
      font-size: clamp(7.5px, 0.75cqw, 13px);
      font-weight: 800;
      letter-spacing: 1px;
      color: var(--accent);
      border-bottom: 1px solid rgba(255,255,255,0.14);
      padding-bottom: 3px;
      margin-bottom: 3px;
    }}
    .study-panel .panel-tag {{
      color: var(--gold);
    }}

    .lens-box {{
      background: rgba(6, 17, 30, 0.75);
      border-radius: 7px;
      padding: 1.05% 1.55%;
      border-left: 3px solid #00B4D8;
    }}
    .waka-lens {{
      border-left-color: var(--gold);
    }}
    .lens-title {{
      font-size: clamp(8px, 0.82cqw, 14.5px);
      font-weight: 800;
      color: #8ECAE6;
      margin-bottom: 2px;
    }}
    .waka-lens .lens-title {{
      color: var(--gold);
    }}
    .lens-box p, .mechanic-box p, .study-block p {{
      font-size: clamp(8px, 0.82cqw, 14.5px);
      line-height: 1.34;
      color: #E8F1F5;
    }}

    .mechanic-box {{
      background: rgba(20, 55, 65, 0.48);
      border: 1px solid var(--accent);
      border-radius: 7px;
      padding: 1.05% 1.55%;
    }}
    .box-label {{
      font-size: clamp(7px, 0.71cqw, 12.5px);
      font-weight: 800;
      color: #80ED99;
      letter-spacing: 0.6px;
      margin-bottom: 2px;
    }}

    .impact-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px 10px;
      background: rgba(5, 14, 24, 0.85);
      padding: 0.95% 1.45%;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.1);
    }}
    .impact-item {{
      font-size: clamp(7px, 0.70cqw, 12.5px);
      line-height: 1.25;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .imp-k {{ color: var(--gold); font-weight: 700; }}
    .imp-v {{ color: #FFFFFF; }}

    .badges-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      padding-top: 2px;
    }}
    .badge-group {{
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
    }}
    .badge-group-title {{
      font-size: clamp(6.5px, 0.66cqw, 11.5px);
      color: var(--text-muted);
      font-weight: 700;
    }}
    .syn-pill, .cnt-pill, .none-pill {{
      font-size: clamp(7px, 0.69cqw, 12px);
      font-weight: 800;
      padding: 1px 7px;
      border-radius: 4px;
    }}
    .syn-pill {{ background: #14453D; color: #80ED99; border: 1px solid #2A9D8F; }}
    .cnt-pill {{ background: #4A151B; color: #FF8080; border: 1px solid #FF595E; }}
    .none-pill {{ color: #6C757D; font-size: clamp(6.5px, 0.64cqw, 11px); }}

    /* RIGHT COLUMN STUDY BLOCKS */
    .study-block {{
      background: rgba(7, 16, 29, 0.8);
      border-radius: 7px;
      padding: 1.15% 1.55%;
      border-left: 3px solid #A8DADC;
    }}
    .evidence-block {{ border-left-color: #00B4D8; }}
    .bridge-block {{
      border-left-color: #80ED99;
      background: rgba(16, 42, 38, 0.55);
    }}
    .cite-list {{
      padding-left: 16px;
      font-size: clamp(7.5px, 0.77cqw, 13.5px);
      line-height: 1.32;
      color: #F4C97E;
    }}
    .cite-list li {{ margin-bottom: 2px; }}

    .code-hook-bar {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      background: rgba(4, 10, 18, 0.9);
      padding: 0.75% 1.35%;
      border-radius: 6px;
      border: 1px solid rgba(0, 180, 216, 0.35);
    }}
    .code-hook-label {{
      font-size: clamp(7px, 0.69cqw, 12px);
      font-weight: 700;
      color: #00B4D8;
    }}
    .code-pill {{
      background: #102A42;
      color: #E0FBFC;
      font-family: "SFMono-Regular", Consolas, Menlo, monospace;
      font-size: clamp(6.5px, 0.67cqw, 11.5px);
      padding: 1px 6px;
      border-radius: 4px;
    }}

    /* FULL-WIDTH BOTTOM EQUATION STAGE (21.8% height) */
    .equation-stage {{
      height: 21.8%;
      flex-shrink: 0;
      width: 100%;
      background: linear-gradient(90deg, #040D1A 0%, #091E32 50%, #040D1A 100%);
      border: 2.5px solid var(--gold);
      border-radius: 10px;
      padding: 0.6% 1.6%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }}
    .eq-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: absolute;
      top: 6px;
      left: 16px;
      right: 16px;
    }}
    .eq-tag {{
      font-size: clamp(7px, 0.70cqw, 12.5px);
      font-weight: 800;
      letter-spacing: 1.1px;
      color: var(--gold);
    }}
    .slide-num-badge {{
      font-size: clamp(7px, 0.70cqw, 12.5px);
      color: var(--text-muted);
      font-weight: 700;
    }}
    .eq-display {{
      width: 100%;
      text-align: center;
      color: #FFFFFF;
      margin-top: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .eq-size-lg {{ font-size: clamp(11px, 1.7cqw, 27px); }}
    .eq-size-md {{ font-size: clamp(9.5px, 1.5cqw, 23px); }}
    .eq-size-sm {{ font-size: clamp(8.5px, 1.3cqw, 19.5px); }}
    {get_mathjax_svg_fit_css('.eq-display', '13.5cqh', '1.15in')}

    /* BOTTOM NAVIGATION TOOLBAR */
    #nav-bar {{
      margin-top: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: #0B1D33;
      padding: 6px 16px;
      border-radius: 8px;
      border: 1px solid #2A9D8F;
    }}
    .nav-btn {{
      background: #133B5C;
      color: #F4C97E;
      border: 1px solid #00B4D8;
      padding: 5px 14px;
      border-radius: 5px;
      cursor: pointer;
      font-weight: 700;
      font-size: 13px;
    }}
    .nav-btn:hover {{ background: #1D5582; }}
    #slide-select {{
      background: #071324;
      color: #FFFFFF;
      border: 1px solid #F4C97E;
      padding: 5px 10px;
      border-radius: 5px;
      font-size: 13px;
      max-width: 420px;
    }}

    /* PRINT / PDF EXPORT MEDIA QUERY (45 Widescreen Landscape Pages) */
    @media print {{
      @page {{
        size: 16in 9in;
        margin: 0;
      }}
      body {{
        overflow: visible !important;
        height: auto !important;
        width: auto !important;
        display: block !important;
        background: #050C16 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      #nav-bar {{ display: none !important; }}
      #deck-viewport {{
        width: 100% !important;
        height: auto !important;
        max-width: none !important;
        max-height: none !important;
      }}
      .slide {{
        display: flex !important;
        width: 16in !important;
        height: 9in !important;
        container-type: size !important;
        page-break-after: always !important;
        break-after: page !important;
        border-radius: 0 !important;
        box-shadow: none !important;
      }}
    }}
  </style>
</head>
<body>

  <div id="deck-viewport">
    {all_slides_str}
  </div>

  <nav id="nav-bar">
    <button class="nav-btn" onclick="prevSlide()">&#9664; Prev (&larr;)</button>
    <select id="slide-select" onchange="jumpToSlide(this.value)">
      {all_options_str}
    </select>
    <button class="nav-btn" onclick="nextSlide()">Next (&rarr;) &#9654;</button>
    <button class="nav-btn" onclick="toggleFullScreen()">&#9974; Fullscreen (F)</button>
    <button class="nav-btn" onclick="window.print()">&#128424; Print / Save 81-Slide PDF</button>
  </nav>

  <script>
    let currentSlide = 1;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const selectEl = document.getElementById('slide-select');

    function showSlide(n) {{
      if (n < 1) n = totalSlides;
      if (n > totalSlides) n = 1;
      currentSlide = n;
      slides.forEach((s, idx) => {{
        s.classList.toggle('active', idx + 1 === currentSlide);
      }});
      selectEl.value = String(currentSlide);
      window.location.hash = 'slide-' + currentSlide;
    }}

    function nextSlide() {{ showSlide(currentSlide + 1); }}
    function prevSlide() {{ showSlide(currentSlide - 1); }}
    function jumpToSlide(val) {{ showSlide(parseInt(val, 10)); }}

    function toggleFullScreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen();
      }} else {{
        document.exitFullscreen();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        prevSlide();
      }} else if (e.key === 'Home') {{
        showSlide(1);
      }} else if (e.key === 'End') {{
        showSlide(totalSlides);
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullScreen();
      }}
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      const hash = window.location.hash;
      if (hash && hash.startsWith('#slide-')) {{
        const num = parseInt(hash.replace('#slide-', ''), 10);
        if (!isNaN(num)) showSlide(num);
      }}
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    if not DECK_YAML.exists():
        raise FileNotFoundError(f"Cannot find {DECK_YAML}")

    g_data = yaml.safe_load(CARDS_YAML.read_text(encoding="utf-8"))
    s_data = yaml.safe_load(DECK_YAML.read_text(encoding="utf-8"))
    g_by_id = {str(c["id"]): c for c in g_data.get("cards", [])}
    s_by_id = {str(s["id"]): s for s in s_data.get("study_cards", [])}
    cards = [{**g_by_id.get(cid, {}), **s_by_id.get(cid, {})} for cid in g_by_id]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_out = build_deck_html(cards)
    OUT_HTML.write_text(html_out, encoding="utf-8")

    print(f"[OK] Rendered {len(cards) + 1}-slide widescreen deck ({len(cards)} cards + 1 Title Slide)")
    print(f"     -> {OUT_HTML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
