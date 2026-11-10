#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — A3 Landscape 5x2 Stacked-Bond Card Renderer
==================================================================================
Compiles `decks/cards.yaml` + a visual theme (`generic`, `waka_hourua`, or
`foils_pakeha`) into an 8-Sheet A3 Landscape (420mm x 297mm) HTML/PDF document
with 10 cards per sheet (5 columns x 2 rows = 80 slots: 100% A3 utilization
across Suites B, T, C, K, N, H, E, and P).

Usage:
  python3 scripts/render_cards.py --theme generic --co2-pos top-right --out build/generic.html
  python3 scripts/render_cards.py --theme waka_hourua --co2-pos bottom-right --out build/waka_preview.html
  python3 scripts/render_cards.py --theme foils_pakeha --co2-pos top-right --out build/foils_preview.html
"""

import argparse
import html
from pathlib import Path
from typing import Any, Dict, List, Optional

from render_common import (
    COPYRIGHT_CARD_HTML,
    DEFAULT_THEME_CONFIG,
    build_sheet_footer_html,
    build_theme_search_order,
    get_base_a3_css,
    load_yaml,
    resolve_theme_config,
)

DECK_ORDER = ["B", "T", "C", "K", "N", "H", "E", "P"]


def find_card_asset(themes_dir: Path, search_order: List[str], card_id: str) -> Optional[Path]:
    """Searches theme asset folders for an optional illustration matching card_id (e.g. B_01.svg)."""
    stem = card_id.replace(":", "_")
    for theme_name in search_order:
        assets_dir = themes_dir / theme_name / "assets"
        if not assets_dir.exists():
            continue
        for ext in (".svg", ".png", ".webp", ".jpg", ".jpeg"):
            candidate = assets_dir / f"{stem}{ext}"
            if candidate.exists():
                return candidate
    return None


DEFAULT_PILLAR_SHORT_LABELS: Dict[int, str] = {
    1: "Pillar I · Narrative",
    2: "Pillar II · Land/Cartel",
    3: "Pillar III · Squeeze",
    4: "Pillar IV · Offshore",
}


def get_co2e_badge_html(card: Dict[str, Any], theme_cfg: Optional[Dict[str, Any]] = None) -> str:
    """Renders explicit CO2e badge if present on a Climate Extension card, else Pillar/Kickback or Mana pill."""
    co2_obj = card.get("co2e_impact") or {}
    display = co2_obj.get("display", "")
    status = co2_obj.get("status", "na")
    if display and status != "na":
        css_mod = "co2-hazard" if status == "hazard_increase" else (
            "co2-indirect" if status == "indirect_enabler" else "co2-computed"
        )
        return f'<span class="co2-badge {css_mod}">🌱 {html.escape(str(display))}</span>'

    kickback = card.get("feral_kickback_wealth")
    pillar_raw = card.get("capture_pillar")
    if kickback is not None and pillar_raw is not None:
        p_idx = int(pillar_raw)
        theme_pillars = (theme_cfg or {}).get("capture_pillars", {})
        p_short = (
            theme_pillars.get(p_idx)
            or theme_pillars.get(str(p_idx))
            or DEFAULT_PILLAR_SHORT_LABELS.get(p_idx, f"Pillar {p_idx}")
        )
        return (
            f'<span class="co2-badge pillar-badge pillar-p{p_idx}">'
            f'{html.escape(str(p_short))} &bull; +{kickback}W</span>'
        )

    cid = str(card.get("id", "")).strip()
    pfx = cid.split(":")[0] if ":" in cid else "B"
    if pfx in ("T", "H") and kickback is not None:
        return f'<span class="co2-badge co2-hazard">⚡ Mode B: +{kickback}W</span>'
    mtier = card.get("mana_tier")
    bmana = card.get("base_mana")
    if mtier is not None and bmana is not None:
        return f'<span class="co2-badge co2-indirect">✦ Tier {mtier} • {bmana}M</span>'
    return ""


def build_wildcard_html(
    prefix: str,
    palette: Dict[str, str],
    co2_pos: str,
) -> str:
    deck_label = palette.get("name", f"Deck {prefix}")
    border_col = palette.get("border", "#334155")
    header_bg = palette.get("header_bg", "#f1f5f9")
    badge_bg = palette.get("badge_bg", "#1e293b")
    badge_txt = palette.get("badge_text", "#ffffff")

    co2_placeholder = '<span class="co2-badge co2-indirect">🌱 ____ MtCO2e</span>'
    top_right = co2_placeholder if co2_pos == "top-right" else '<span class="gate-tag">Gate / Phase: ____</span>'
    bottom_right = co2_placeholder if co2_pos == "bottom-right" else '<span class="gate-tag">PR Track 1 / Track 2</span>'

    return f"""
    <article class="card wildcard-card" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <header class="card-header">
        <div class="header-top">
          <span class="pdd-badge">{html.escape(prefix)}:??</span>
          <div class="header-right">{top_right}</div>
        </div>
        <h2 class="card-title">Write-In Game Changer: ____________________</h2>
        <div class="card-type">Player-Authored Wildcard &bull; {html.escape(deck_label)}</div>
      </header>
      <div class="card-cost">
        <strong>Cost / Requirement:</strong> __________________________________________________
      </div>
      <div class="card-body">
        <div class="effect-block">
          <span class="effect-label">First-Order Effect (Easy Mode):</span>
          <span class="effect-rule">____________________________________________________________________________________________________________________</span>
        </div>
        <div class="effect-block">
          <span class="effect-label">Crowd-Out / Second-Order Check (Challenge Mode):</span>
          <span class="effect-rule">____________________________________________________________________________________________________________________</span>
        </div>
      </div>
      <div class="card-flavor">&ldquo;When a card doesn&rsquo;t exist yet, author a Game Changer and prove it at the Big Table.&rdquo;</div>
      <div class="card-anchor"><strong>Empirical Anchor:</strong> ______________________________________________</div>
      <footer class="card-footer">
        <div class="synergy-bar">🔗 <strong>Synergies:</strong> ____, ____, ____</div>
        <div class="footer-right">{bottom_right}</div>
      </footer>
      <div class="card-copyright">{COPYRIGHT_CARD_HTML}</div>
    </article>
    """


def render_deck_html(
    deck_data: Dict[str, Any],
    theme_cfg: Dict[str, Any],
    themes_dir: Path,
    theme_id: str,
    co2_pos: str,
    out_path: Path,
) -> str:
    cards: List[Dict[str, Any]] = sorted(
        deck_data.get("cards", []),
        key=lambda c: (int(c.get("a3_game_sheet", 99)), int(c.get("a3_slot", 99))),
    )
    active_theme_name = theme_cfg.get("theme_name", theme_id)
    typo = theme_cfg.get("typography", {})
    font_heading = typo.get("heading_font", "'Inter', system-ui, sans-serif")
    font_body = typo.get("body_font", "'Inter', system-ui, sans-serif")
    font_mono = typo.get("mono_font", "'JetBrains Mono', monospace")

    palettes = dict(DEFAULT_THEME_CONFIG["deck_palettes"])
    palettes.update(theme_cfg.get("deck_palettes", {}))
    card_overrides = theme_cfg.get("card_overrides", {})
    search_order = build_theme_search_order(themes_dir, theme_id, theme_cfg)

    rendered_cards: List[str] = []
    for raw_card in cards:
        card = dict(raw_card)
        cid = str(card.get("id", "")).strip()
        prefix = cid.split(":")[0] if ":" in cid else "B"
        palette = palettes.get(prefix, palettes["B"])

        # Apply theme-specific text overrides (e.g., Te Waka Hourua titles/flavor)
        if cid in card_overrides:
            ov = card_overrides[cid]
            if "name" in ov:
                card["name"] = ov["name"]
            if "type" in ov:
                card["type"] = ov["type"]
            if "flavor_text" in ov:
                card["flavor_text"] = ov["flavor_text"]

        border_col = palette.get("border", "#0284c7")
        header_bg = palette.get("header_bg", "#e0f2fe")
        badge_bg = palette.get("badge_bg", "#0369a1")
        badge_txt = palette.get("badge_text", "#ffffff")

        border_col = palette.get("border", "#0284c7")
        header_bg = palette.get("header_bg", "#e0f2fe")
        badge_bg = palette.get("badge_bg", "#0369a1")
        badge_txt = palette.get("badge_text", "#ffffff")

        co2_html = get_co2e_badge_html(card, theme_cfg)
        gate_phase = html.escape(str(card.get("gate_or_phase", "")))
        gate_span = f'<span class="gate-tag">{gate_phase}</span>' if gate_phase else ""
        if co2_pos == "top-right":
            top_right_slot = co2_html or gate_span
            bottom_right_slot = gate_span if co2_html else ""
        else:
            top_right_slot = gate_span
            bottom_right_slot = co2_html

        # Optional illustration asset
        asset_path = find_card_asset(themes_dir, search_order, cid)
        art_html = ""
        if asset_path is not None:
            try:
                rel_asset = asset_path.resolve().relative_to(out_path.resolve().parent)
            except ValueError:
                rel_asset = asset_path
            art_html = f'<div class="card-art"><img src="{rel_asset.as_posix()}" alt="{html.escape(cid)}" /></div>'

        effects_html = []
        for eff in card.get("effects", []):
            lbl = html.escape(str(eff.get("label", "")))
            rule = html.escape(str(eff.get("rule", "")))
            effects_html.append(
                f'<div class="effect-block"><span class="effect-label">{lbl}:</span> <span class="effect-rule">{rule}</span></div>'
            )

        synergies = ", ".join(card.get("synergy_links", []))
        flavor = html.escape(str(card.get("flavor_text", "")))
        anchor = html.escape(str(card.get("empirical_anchor", "")))
        cost_req = html.escape(str(card.get("cost_or_requirement", "")))

        rendered_cards.append(f"""
        <article class="card" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
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
          <div class="card-body">
            {''.join(effects_html)}
          </div>
          <div class="card-flavor">&ldquo;{flavor}&rdquo;</div>
          <div class="card-anchor"><strong>Anchor:</strong> {anchor}</div>
          <footer class="card-footer">
            <div class="synergy-bar">🔗 <strong>Synergies:</strong> {html.escape(synergies)}</div>
            <div class="footer-right">{bottom_right_slot}</div>
          </footer>
          <div class="card-copyright">{COPYRIGHT_CARD_HTML}</div>
        </article>
        """)

    # Pad to a multiple of 10 with write-in P:?? deck wildcards (7 wildcards -> 50 slots)
    cards_per_sheet = 10
    rem = len(rendered_cards) % cards_per_sheet
    pad_count = (cards_per_sheet - rem) if rem != 0 else 0
    for i in range(pad_count):
        pfx = DECK_ORDER[i % len(DECK_ORDER)]
        rendered_cards.append(build_wildcard_html(pfx, palettes.get(pfx, palettes["B"]), co2_pos))

    total_sheets = len(rendered_cards) // cards_per_sheet
    sheet_blocks = []
    for s in range(total_sheets):
        batch = rendered_cards[s * cards_per_sheet : (s + 1) * cards_per_sheet]
        footer_html = build_sheet_footer_html(
            f"Foils &amp; Founders: The Aotearoa Deck ({html.escape(active_theme_name)}) &mdash; "
            f"A3 Landscape Sheet {s + 1} of {total_sheets} (5&times;2 Stacked Bond &mdash; Cut along dashed lines)"
        )
        sheet_blocks.append(f"""
        <section class="a3-sheet">
          <div class="card-grid">
            {''.join(batch)}
          </div>
          {footer_html}
        </section>
        """)

    base_css = get_base_a3_css(font_heading, font_body, font_mono)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Foils &amp; Founders: The Aotearoa Deck ({html.escape(active_theme_name)})</title>
  <style>
    {base_css}
    .a3-sheet {{
      padding: 8mm 12.5mm 5mm 12.5mm;
    }}
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(5, 79mm);
      grid-template-rows: repeat(2, 138mm);
      gap: 0;
      border: 0.4mm dashed #64748b;
      margin: 0 auto;
    }}
    .card {{
      width: 79mm;
      height: 138mm;
      border: 0.25mm dashed #94a3b8;
      border-top: 2.2mm solid var(--card-border);
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
    .pillar-badge {{ font-size: 5.3pt; letter-spacing: 0.01em; }}
    .pillar-p1 {{ background: #f3e8ff; color: #581c87; border: 0.3mm solid #d8b4fe; }}
    .pillar-p2 {{ background: #fef3c7; color: #92400e; border: 0.3mm solid #fcd34d; }}
    .pillar-p3 {{ background: #ffe4e6; color: #9f1239; border: 0.3mm solid #fda4af; }}
    .pillar-p4 {{ background: #e0e7ff; color: #3730a3; border: 0.3mm solid #a5b4fc; }}    .gate-tag {{
      font-family: var(--font-mono);
      font-size: 5.4pt;
      color: #475569;
      font-weight: 600;
    }}
    .card-title {{
      font-family: var(--font-heading);
      font-size: 8.2pt;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.15;
      margin-bottom: 0.4mm;
    }}
    .card-type {{
      font-size: 5.8pt;
      font-weight: 600;
      color: #334155;
    }}
    .card-cost {{
      font-size: 5.9pt;
      background: #f8fafc;
      border: 0.25mm solid #cbd5e1;
      padding: 0.9mm 1.4mm;
      border-radius: 0.8mm;
      margin-bottom: 1.2mm;
      line-height: 1.2;
      flex-shrink: 0;
    }}
    .card-art {{
      height: 22mm;
      margin-bottom: 1.2mm;
      border-radius: 1mm;
      overflow: hidden;
      background: #f1f5f9;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .card-art img {{ width: 100%; height: 100%; object-fit: cover; }}
    .card-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 1.1mm;
      overflow: hidden;
    }}
    .effect-block {{
      font-size: 6.0pt;
      line-height: 1.24;
      background: #ffffff;
      border-left: 0.8mm solid #cbd5e1;
      padding-left: 1.4mm;
    }}
    .effect-label {{ font-weight: 800; color: #0f172a; }}
    .effect-rule {{ color: #1e293b; }}
    .card-flavor {{
      font-size: 5.7pt;
      font-style: italic;
      color: #334155;
      background: #f8fafc;
      padding: 1mm 1.4mm;
      border-radius: 0.8mm;
      margin-top: 1mm;
      line-height: 1.2;
      flex-shrink: 0;
    }}
    .card-anchor {{
      font-size: 5.0pt;
      color: #64748b;
      margin-top: 0.8mm;
      line-height: 1.15;
      flex-shrink: 0;
    }}
    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 0.25mm solid #e2e8f0;
      padding-top: 0.8mm;
      margin-top: 0.8mm;
      font-size: 5.4pt;
      flex-shrink: 0;
    }}
    .synergy-bar {{ font-family: var(--font-mono); color: #0f172a; }}
    .card-copyright {{
      font-family: var(--font-mono);
      font-size: 4.5pt;
      color: #94a3b8;
      text-align: center;
      margin-top: 0.4mm;
      line-height: 1;
      letter-spacing: 0.02em;
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
        description="Render Foils & Founders 5x2 Stacked-Bond A3 Landscape Card Sheets."
    )
    parser.add_argument(
        "--cards-yaml",
        type=Path,
        default=Path("decks/cards.yaml"),
        help="Path to cards.yaml (default: decks/cards.yaml)",
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
        help="Position of the CO2e impact badge on each card (default: top-right)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("build/generic.html"),
        help="Output HTML file path (default: build/generic.html)",
    )
    args = parser.parse_args()

    deck_data = load_yaml(args.cards_yaml, required=True)
    theme_cfg = resolve_theme_config(args.themes_dir, args.theme)
    html_out = render_deck_html(
        deck_data, theme_cfg, args.themes_dir, args.theme, args.co2_pos, args.out
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")
    total_cards = len(deck_data.get("cards", []))
    print(
        f"[OK] Rendered {total_cards} canonical cards + {(10 - total_cards % 10) % 10} wildcards "
        f"(theme='{args.theme}', co2_pos='{args.co2_pos}') -> {args.out}"
    )


if __name__ == "__main__":
    main()
