#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — A3 Fold-Over Study Card Renderer
======================================================================
Compiles `decks/study_cards.yaml` + `decks/cards.yaml` into A3 Landscape
(420mm x 297mm) sheets with 5 fold-over cards per sheet (5 columns x 2 rows):
  - Top Row (Back Face): 138mm x 79mm Landscape (rotated -90deg in the 79x138mm
    top slot) featuring MathJax 3 SVG equations, calibrated parameters, proof
    bridge, and peer-reviewed citations.
  - Bottom Row (Front Face): Standard 79mm x 138mm Portrait game card.

By default, renders ONLY the cards present in `decks/study_cards.yaml` (padded
to a multiple of 5 with write-in Study Wildcards) so you can preview 1 sheet
immediately. Pass `--all-cards` to render all 43 canonical cards.

Usage:
  python3 scripts/render_study_cards.py --theme generic --out build/study_generic.html
  python3 scripts/render_study_cards.py --theme waka_hourua --co2-pos bottom-right --out build/study_waka.html
  python3 scripts/render_study_cards.py --theme foils_pakeha --out build/study_foils.html
"""

import argparse
import html
from pathlib import Path
from typing import Any, Dict, List

from render_cards import (
    DECK_ORDER,
    build_wildcard_html,
    find_card_asset,
    get_co2e_badge_html,
)
from render_common import (
    COPYRIGHT_CARD_HTML,
    DEFAULT_THEME_CONFIG,
    build_sheet_footer_html,
    build_theme_search_order,
    get_base_a3_css,
    load_yaml,
    resolve_theme_config,
)


def build_front_card_html(
    raw_card: Dict[str, Any],
    palettes: Dict[str, Dict[str, str]],
    card_overrides: Dict[str, Any],
    themes_dir: Path,
    search_order: List[str],
    co2_pos: str,
    out_path: Path,
) -> str:
    """Renders the standard 79mm x 138mm Portrait front card for the bottom row."""
    card = dict(raw_card)
    cid = str(card.get("id", "")).strip()
    prefix = cid.split(":")[0] if ":" in cid else "B"
    palette = palettes.get(prefix, palettes["B"])

    if cid in card_overrides:
        ov = card_overrides[cid]
        for k in ("name", "type", "flavor_text"):
            if k in ov:
                card[k] = ov[k]

    border_col = palette.get("border", "#0284c7")
    header_bg = palette.get("header_bg", "#e0f2fe")
    badge_bg = palette.get("badge_bg", "#0369a1")
    badge_txt = palette.get("badge_text", "#ffffff")

    co2_html = get_co2e_badge_html(card)
    gate_phase = html.escape(str(card.get("gate_or_phase", "")))
    gate_span = f'<span class="gate-tag">{gate_phase}</span>' if gate_phase else ""

    if co2_pos == "top-right":
        top_right_slot = co2_html or gate_span
        bottom_right_slot = gate_span if co2_html else ""
    else:
        top_right_slot = gate_span
        bottom_right_slot = co2_html

    asset_path = find_card_asset(themes_dir, search_order, cid)
    art_html = ""
    if asset_path is not None:
        try:
            rel_asset = asset_path.resolve().relative_to(out_path.resolve().parent)
        except ValueError:
            rel_asset = asset_path
        art_html = f'<div class="card-art"><img src="{rel_asset.as_posix()}" alt="{html.escape(cid)}" /></div>'

    effects_html = [
        f'<div class="effect-block"><span class="effect-label">{html.escape(str(eff.get("label", "")))}:</span> '
        f'<span class="effect-rule">{html.escape(str(eff.get("rule", "")))}</span></div>'
        for eff in card.get("effects", [])
    ]

    synergies = ", ".join(card.get("synergy_links", []))
    flavor = html.escape(str(card.get("flavor_text", "")))
    anchor = html.escape(str(card.get("empirical_anchor", "")))
    cost_req = html.escape(str(card.get("cost_or_requirement", "")))

    return f"""
    <article class="card front-card" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <header class="card-header">
        <div class="header-top">
          <span class="pdd-badge">{html.escape(cid)}</span>
          <div class="header-right">{top_right_slot}</div>
        </div>
        <h2 class="card-title">{html.escape(str(card.get("name", "")))}</h2>
        <div class="card-type">{html.escape(str(card.get("type", "")))}</div>
      </header>
      <div class="card-cost"><strong>Cost / Req:</strong> {cost_req}</div>
      {art_html}
      <div class="card-body">{''.join(effects_html)}</div>
      <div class="card-flavor">&ldquo;{flavor}&rdquo;</div>
      <div class="card-anchor"><strong>Anchor:</strong> {anchor}</div>
      <footer class="card-footer">
        <div class="synergy-bar">🔗 <strong>Synergies:</strong> {html.escape(synergies)}</div>
        <div class="footer-right">{bottom_right_slot}</div>
      </footer>
      <div class="card-copyright">{COPYRIGHT_CARD_HTML}</div>
    </article>
    """


def build_study_back_html(
    card_front: Dict[str, Any],
    study_entry: Dict[str, Any],
    palettes: Dict[str, Dict[str, str]],
    orient: str,
) -> str:
    """
    Renders the top-row Back Face (79mm x 138mm slot containing a 138mm x 79mm
    rotated Landscape blackboard with MathJax equation, parameters, proof bridge,
    and academic citations).
    """
    cid = str(card_front.get("id", study_entry.get("id", "B:??"))).strip()
    cname = str(card_front.get("name", "Write-In Study Card")).strip()
    prefix = cid.split(":")[0] if ":" in cid else "B"
    palette = palettes.get(prefix, palettes["B"])

    border_col = palette.get("border", "#0284c7")
    header_bg = palette.get("header_bg", "#e0f2fe")
    badge_bg = palette.get("badge_bg", "#0369a1")
    badge_txt = palette.get("badge_text", "#ffffff")

    mono_ref = html.escape(str(study_entry.get("monograph_ref", "Doc 1B • Doc 2 GPU Solver")))
    eq_title = html.escape(str(study_entry.get("equation_title", "General-Equilibrium Specification")))
    latex_raw = str(study_entry.get("latex_equation", "")).strip()
    params_txt = html.escape(str(study_entry.get("parameters", "")))
    bridge_txt = html.escape(str(study_entry.get("proof_bridge", "")))
    citations = study_entry.get("citations", [])

    cites_html = "".join(
        f"<li>{html.escape(str(c))}</li>" for c in citations
    )

    rot_class = "rot-ccw" if orient == "landscape-ccw" else (
        "rot-cw" if orient == "landscape-cw" else "rot-180"
    )

    return f"""
    <div class="study-back-slot" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <div class="study-landscape-canvas {rot_class}">
        <header class="sb-header">
          <div class="sb-header-left">
            <span class="pdd-badge">{html.escape(cid)}</span>
            <span class="sb-card-name">{html.escape(cname)}</span>
          </div>
          <span class="sb-mono-ref">📐 {mono_ref}</span>
        </header>

        <div class="sb-eq-frame">
          <div class="sb-eq-title">{eq_title}</div>
          <div class="sb-eq-math">\\[ {latex_raw} \\]</div>
        </div>

        <div class="sb-params">
          <strong>Calibration:</strong> {params_txt}
        </div>

        <div class="sb-bridge">
          <strong>Tabletop Proof Bridge:</strong> {bridge_txt}
        </div>

        <div class="sb-citations">
          <div class="sb-cite-heading">Primary Econometric &amp; Empirical Citations:</div>
          <ul class="sb-cite-list">{cites_html}</ul>
        </div>

        <footer class="sb-footer">
          <span>Fold along bottom crease &bull; Foils &amp; Founders Study Deck</span>
          <span>{COPYRIGHT_CARD_HTML}</span>
        </footer>
      </div>
    </div>
    """


def build_wildcard_study_back_html(
    prefix: str,
    palette: Dict[str, str],
    orient: str,
) -> str:
    border_col = palette.get("border", "#334155")
    header_bg = palette.get("header_bg", "#f1f5f9")
    badge_bg = palette.get("badge_bg", "#1e293b")
    badge_txt = palette.get("badge_text", "#ffffff")
    rot_class = "rot-ccw" if orient == "landscape-ccw" else (
        "rot-cw" if orient == "landscape-cw" else "rot-180"
    )

    return f"""
    <div class="study-back-slot" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <div class="study-landscape-canvas {rot_class}">
        <header class="sb-header">
          <div class="sb-header-left">
            <span class="pdd-badge">{html.escape(prefix)}:??</span>
            <span class="sb-card-name">Write-In Study Card (Track 2 Challenge Mode PR)</span>
          </div>
          <span class="sb-mono-ref">📐 Doc 1B §____ • Doc 2: ____________.m</span>
        </header>

        <div class="sb-eq-frame">
          <div class="sb-eq-title">Bellman / Kolmogorov Forward / Stationary Distribution Specification:</div>
          <div class="sb-eq-math" style="color:#94a3b8; font-family:var(--font-mono); font-size:7pt;">
            [ Write or typeset your formal OLG / CES / KFE equation here: &Delta;&mu;*(s) = ... ]
          </div>
        </div>

        <div class="sb-params">
          <strong>Calibration &amp; Parameters:</strong> ________________________________________________________________________________________
        </div>

        <div class="sb-bridge">
          <strong>Tabletop Proof Bridge:</strong> ___________________________________________________________________________________________
        </div>

        <div class="sb-citations">
          <div class="sb-cite-heading">Primary Econometric &amp; Empirical Citations:</div>
          <ul class="sb-cite-list">
            <li>1. _____________________________________________________________________________________________________________</li>
            <li>2. _____________________________________________________________________________________________________________</li>
          </ul>
        </div>

        <footer class="sb-footer">
          <span>Fold along bottom crease &bull; Foils &amp; Founders Study Deck</span>
          <span>{COPYRIGHT_CARD_HTML}</span>
        </footer>
      </div>
    </div>
    """


def render_study_deck_html(
    cards_data: Dict[str, Any],
    study_data: Dict[str, Any],
    theme_cfg: Dict[str, Any],
    themes_dir: Path,
    theme_id: str,
    co2_pos: str,
    orient: str,
    all_cards: bool,
    out_path: Path,
) -> str:
    all_front_cards: List[Dict[str, Any]] = cards_data.get("cards", [])
    front_by_id: Dict[str, Dict[str, Any]] = {
        str(c.get("id", "")).strip(): c for c in all_front_cards
    }
    study_list: List[Dict[str, Any]] = study_data.get("study_cards", [])
    study_by_id: Dict[str, Dict[str, Any]] = {
        str(s.get("id", "")).strip(): s for s in study_list
    }

    active_theme_name = theme_cfg.get("theme_name", theme_id)
    typo = theme_cfg.get("typography", {})
    font_heading = typo.get("heading_font", "'Inter', system-ui, sans-serif")
    font_body = typo.get("body_font", "'Inter', system-ui, sans-serif")
    font_mono = typo.get("mono_font", "'JetBrains Mono', monospace")

    palettes = dict(DEFAULT_THEME_CONFIG["deck_palettes"])
    palettes.update(theme_cfg.get("deck_palettes", {}))
    card_overrides = theme_cfg.get("card_overrides", {})
    search_order = build_theme_search_order(themes_dir, theme_id, theme_cfg)

    # Determine which cards to render (default: only those in study_cards.yaml)
    target_ids: List[str] = (
        [str(c.get("id", "")).strip() for c in all_front_cards]
        if all_cards
        else [str(s.get("id", "")).strip() for s in study_list]
    )

    pairs: List[tuple[str, str]] = []  # (top_back_html, bottom_front_html)
    for cid in target_ids:
        front_card = front_by_id.get(cid, {"id": cid, "name": cid})
        study_entry = study_by_id.get(cid, {"id": cid})
        back_html = build_study_back_html(front_card, study_entry, palettes, orient)
        front_html = build_front_card_html(
            front_card, palettes, card_overrides, themes_dir, search_order, co2_pos, out_path
        )
        pairs.append((back_html, front_html))

    # Pad to a multiple of 5 (5 fold-over cards per A3 sheet)
    cards_per_sheet = 5
    rem = len(pairs) % cards_per_sheet
    pad_count = (cards_per_sheet - rem) if rem != 0 else 0
    for i in range(pad_count):
        pfx = DECK_ORDER[i % len(DECK_ORDER)]
        pal = palettes.get(pfx, palettes["B"])
        pairs.append(
            (
                build_wildcard_study_back_html(pfx, pal, orient),
                build_wildcard_html(pfx, pal, co2_pos),
            )
        )

    total_sheets = len(pairs) // cards_per_sheet
    sheet_blocks: List[str] = []
    for s in range(total_sheets):
        batch = pairs[s * cards_per_sheet : (s + 1) * cards_per_sheet]
        top_row_html = "".join(b[0] for b in batch)
        bottom_row_html = "".join(b[1] for b in batch)
        footer_html = build_sheet_footer_html(
            f"Foils &amp; Founders Study Deck ({html.escape(active_theme_name)}) &mdash; "
            f"A3 Sheet {s + 1} of {total_sheets} (5 Fold-Over Study Cards: Cut 5 Vertical Strips &amp; Fold Top Back Behind Bottom Front)"
        )
        sheet_blocks.append(f"""
        <section class="a3-sheet">
          <div class="card-grid study-grid">
            {top_row_html}
            {bottom_row_html}
          </div>
          {footer_html}
        </section>
        """)

    base_css = get_base_a3_css(font_heading, font_body, font_mono)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Foils &amp; Founders — Fold-Over Study Cards ({html.escape(active_theme_name)})</title>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{
        fontCache: 'global',
        scale: 0.92
      }},
      startup: {{
        pageReady: () => {{
          return MathJax.startup.defaultPageReady().then(() => {{
            // Auto-fit any wide equations inside their 130mm container
            document.querySelectorAll('.sb-eq-math').forEach(box => {{
              const svg = box.querySelector('svg');
              if (svg) {{
                svg.style.maxWidth = '100%';
                svg.style.height = 'auto';
              }}
            }});
          }});
        }}
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    {base_css}
    .a3-sheet {{
      padding: 8mm 12.5mm 5mm 12.5mm;
    }}
    .card-grid.study-grid {{
      display: grid;
      grid-template-columns: repeat(5, 79mm);
      grid-template-rows: 138mm 138mm;
      gap: 0;
      border: 0.4mm dashed #475569;
      margin: 0 auto;
    }}

    /* Standard Front Card (Bottom Row: 79mm x 138mm Portrait) */
    .card {{
      width: 79mm;
      height: 138mm;
      border: 0.25mm dashed #94a3b8;
      border-top: 0.6mm solid #0f172a; /* Bold Horizontal Crease Line */
      background: #ffffff;
      padding: 2.2mm 2.5mm 1.5mm 2.5mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }}
    .card-header {{
      background: var(--header-bg);
      padding: 1.5mm 1.8mm;
      border-radius: 1.2mm;
      border-left: 1.2mm solid var(--card-border);
      margin-bottom: 1.2mm;
      flex-shrink: 0;
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.8mm;
      gap: 1mm;
    }}
    .pdd-badge {{
      font-family: var(--font-mono);
      font-size: 7.5pt;
      font-weight: 800;
      background: var(--badge-bg);
      color: var(--badge-txt);
      padding: 0.4mm 1.6mm;
      border-radius: 1mm;
      letter-spacing: 0.03em;
      flex-shrink: 0;
    }}
    .co2-badge {{
      font-family: var(--font-mono);
      font-size: 5.6pt;
      font-weight: 700;
      padding: 0.4mm 1.3mm;
      border-radius: 1mm;
      white-space: nowrap;
    }}
    .co2-computed {{ background: #dcfce7; color: #166534; border: 0.3mm solid #86efac; }}
    .co2-indirect {{ background: #e0f2fe; color: #075985; border: 0.3mm solid #7dd3fc; }}
    .co2-hazard {{ background: #fee2e2; color: #991b1b; border: 0.3mm solid #fca5a5; }}
    .gate-tag {{ font-family: var(--font-mono); font-size: 5.4pt; color: #475569; font-weight: 600; }}
    .card-title {{ font-family: var(--font-heading); font-size: 8.2pt; font-weight: 800; color: #0f172a; line-height: 1.15; margin-bottom: 0.4mm; }}
    .card-type {{ font-size: 5.8pt; font-weight: 600; color: #334155; }}
    .card-cost {{ font-size: 5.9pt; background: #f8fafc; border: 0.25mm solid #cbd5e1; padding: 0.9mm 1.4mm; border-radius: 0.8mm; margin-bottom: 1.2mm; line-height: 1.2; flex-shrink: 0; }}
    .card-art {{ height: 22mm; margin-bottom: 1.2mm; border-radius: 1mm; overflow: hidden; background: #f1f5f9; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
    .card-art img {{ width: 100%; height: 100%; object-fit: cover; }}
    .card-body {{ flex: 1; display: flex; flex-direction: column; gap: 1.1mm; overflow: hidden; }}
    .effect-block {{ font-size: 6.0pt; line-height: 1.24; background: #ffffff; border-left: 0.8mm solid #cbd5e1; padding-left: 1.4mm; }}
    .effect-label {{ font-weight: 800; color: #0f172a; }}
    .effect-rule {{ color: #1e293b; }}
    .card-flavor {{ font-size: 5.7pt; font-style: italic; color: #334155; background: #f8fafc; padding: 1mm 1.4mm; border-radius: 0.8mm; margin-top: 1mm; line-height: 1.2; flex-shrink: 0; }}
    .card-anchor {{ font-size: 5.0pt; color: #64748b; margin-top: 0.8mm; line-height: 1.15; flex-shrink: 0; }}
    .card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 0.25mm solid #e2e8f0; padding-top: 0.8mm; margin-top: 0.8mm; font-size: 5.4pt; flex-shrink: 0; }}
    .synergy-bar {{ font-family: var(--font-mono); color: #0f172a; }}
    .card-copyright {{ font-family: var(--font-mono); font-size: 4.5pt; color: #94a3b8; text-align: center; margin-top: 0.4mm; line-height: 1; flex-shrink: 0; }}

    /* Top Row: Study Back Slot (79mm x 138mm outer slot holding rotated 138mm x 79mm Landscape Canvas) */
    .study-back-slot {{
      width: 79mm;
      height: 138mm;
      border: 0.25mm dashed #94a3b8;
      border-bottom: 0.6mm solid #0f172a; /* Fold Crease Line */
      position: relative;
      overflow: hidden;
      background: #ffffff;
    }}
    .study-landscape-canvas {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 138mm;
      height: 79mm;
      padding: 2.6mm 3.2mm 2mm 3.2mm;
      border-top: 2.2mm solid var(--card-border);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #ffffff;
    }}
    .rot-ccw {{ transform: translate(-50%, -50%) rotate(-90deg); }}
    .rot-cw  {{ transform: translate(-50%, -50%) rotate(90deg); }}
    .rot-180 {{
      width: 79mm;
      height: 138mm;
      transform: translate(-50%, -50%) rotate(180deg);
    }}

    /* Landscape Study Card Interior Elements */
    .sb-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--header-bg);
      padding: 1.2mm 2mm;
      border-radius: 1.2mm;
      border-left: 1.4mm solid var(--card-border);
      gap: 2mm;
      flex-shrink: 0;
    }}
    .sb-header-left {{
      display: flex;
      align-items: center;
      gap: 1.8mm;
      min-width: 0;
    }}
    .sb-card-name {{
      font-family: var(--font-heading);
      font-size: 8.2pt;
      font-weight: 800;
      color: #0f172a;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .sb-mono-ref {{
      font-family: var(--font-mono);
      font-size: 5.8pt;
      font-weight: 700;
      color: #334155;
      background: #ffffff;
      padding: 0.5mm 1.5mm;
      border-radius: 0.8mm;
      border: 0.25mm solid #cbd5e1;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .sb-eq-frame {{
      background: #f8fafc;
      border: 0.35mm solid #94a3b8;
      border-left: 1.2mm solid var(--card-border);
      border-radius: 1.2mm;
      padding: 1.2mm 2mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
      flex-shrink: 0;
    }}
    .sb-eq-title {{
      font-family: var(--font-mono);
      font-size: 6pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--badge-bg);
      margin-bottom: 0.5mm;
    }}
    .sb-eq-math {{
      font-size: 7.4pt;
      line-height: 1.1;
      text-align: center;
      overflow: hidden;
      padding: 0.4mm 0;
    }}
    .sb-eq-math mjx-container {{
      margin: 0 !important;
      max-width: 100% !important;
    }}
    .sb-params {{
      font-family: var(--font-mono);
      font-size: 5.9pt;
      line-height: 1.22;
      background: #eff6ff;
      border: 0.25mm solid #bfdbfe;
      padding: 1mm 1.6mm;
      border-radius: 0.8mm;
      color: #1e3a8a;
      flex-shrink: 0;
    }}
    .sb-bridge {{
      font-size: 6.2pt;
      line-height: 1.24;
      color: #0f172a;
      background: #f0fdf4;
      border-left: 1mm solid #16a34a;
      padding: 1mm 1.6mm;
      border-radius: 0.8mm;
      flex-shrink: 0;
    }}
    .sb-citations {{
      border-top: 0.25mm solid #cbd5e1;
      padding-top: 0.8mm;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      overflow: hidden;
    }}
    .sb-cite-heading {{
      font-family: var(--font-mono);
      font-size: 5.5pt;
      font-weight: 800;
      color: #475569;
      text-transform: uppercase;
      margin-bottom: 0.4mm;
    }}
    .sb-cite-list {{
      list-style: disc;
      padding-left: 3.2mm;
      font-size: 5.5pt;
      line-height: 1.2;
      color: #334155;
    }}
    .sb-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 4.8pt;
      color: #94a3b8;
      border-top: 0.2mm solid #e2e8f0;
      padding-top: 0.5mm;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>
  {''.join(sheet_blocks)}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Foils & Founders A3 Fold-Over Study Cards (Equations & Citations on Back)."
    )
    parser.add_argument(
        "--cards-yaml",
        type=Path,
        default=Path("decks/cards.yaml"),
        help="Path to cards.yaml (default: decks/cards.yaml)",
    )
    parser.add_argument(
        "--study-yaml",
        type=Path,
        default=Path("decks/study_cards.yaml"),
        help="Path to study_cards.yaml (default: decks/study_cards.yaml)",
    )
    parser.add_argument(
        "--themes-dir",
        type=Path,
        default=Path("themes"),
        help="Directory containing theme folders (default: themes)",
    )
    parser.add_argument(
        "--theme",
        type=str,
        default="generic",
        help="Theme ID to render: generic | waka_hourua | foils_pakeha",
    )
    parser.add_argument(
        "--co2-pos",
        type=str,
        choices=["top-right", "bottom-right"],
        default="top-right",
        help="Position of the CO2e impact badge on the front card (default: top-right)",
    )
    parser.add_argument(
        "--back-orient",
        type=str,
        choices=["landscape-ccw", "landscape-cw", "portrait-180"],
        default="landscape-ccw",
        help="Orientation of the top fold-over back face (default: landscape-ccw)",
    )
    parser.add_argument(
        "--all-cards",
        action="store_true",
        help="Render all 43 cards in cards.yaml instead of only the entries in study_cards.yaml",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("build/study_generic.html"),
        help="Output HTML file path (default: build/study_generic.html)",
    )
    args = parser.parse_args()

    cards_data = load_yaml(args.cards_yaml, required=True)
    study_data = load_yaml(args.study_yaml, required=True)
    theme_cfg = resolve_theme_config(args.themes_dir, args.theme)

    html_out = render_study_deck_html(
        cards_data,
        study_data,
        theme_cfg,
        args.themes_dir,
        args.theme,
        args.co2_pos,
        args.back_orient,
        args.all_cards,
        args.out,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")
    study_count = len(study_data.get("study_cards", []))
    print(
        f"[OK] Rendered {study_count} study cards + {(5 - study_count % 5) % 5} study wildcards "
        f"(theme='{args.theme}', back_orient='{args.back_orient}') -> {args.out}"
    )


if __name__ == "__main__":
    main()
