#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — Multi-Theme Card Renderer (v2.0)
Supports Theme Dictionaries (card_overrides + lexicon_replacements) & CO2e Badges
License: CC-BY-SA-4.0 / GPL-3.0-or-later
"""

import argparse
import copy
import html
from pathlib import Path
import yaml

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

IMAGE_EXTENSIONS = [".svg", ".png", ".webp", ".jpg", ".jpeg"]

# Default computed/indirect CO2e badges if not explicitly set on a card in cards.yaml
DEFAULT_CO2E_BADGES = {
    "B:00": ("Fair Transition", "indirect_enabler"),
    "B:01": ("Low-Carbon Care", "indirect_enabler"),
    "B:02": ("Active Transport", "indirect_enabler"),
    "B:03": ("Clean-Tech Talent", "indirect_enabler"),
    "B:04": ("-75% Waste Drag", "indirect_enabler"),
    "B:05": ("Green CapEx Shift", "indirect_enabler"),
    "B:06": ("-4.2 MtCO2e / yr", "computed"),
    "B:07": ("2% Real Climate PV", "indirect_enabler"),
    "B:08": ("Full-System Audit", "indirect_enabler"),
    "B:09": ("Net-Zero Aotearoa", "computed"),
    "T:00": ("+0.4 tCO2e / limo", "hazard_increase"),
    "T:01": ("Stalled Retrofit", "hazard_increase"),
    "T:02": ("Sprawl Bubble", "hazard_increase"),
    "T:03": ("Urban Heat Trap", "hazard_increase"),
    "C:01": ("USD 1,200 / tCO2e", "computed"),
    "C:02": ("-2.5 MtCO2e / yr", "computed"),
    "C:03": ("Kaitiaki Resilience", "indirect_enabler"),
    "C:04": ("-4.2 MtCO2e / yr", "computed"),
    "C:05": ("-5.9 MtCO2e / yr", "computed"),
    "C:06": ("High-Trust Action", "indirect_enabler"),
    "K:01": ("Marae/School Solar", "indirect_enabler"),
    "K:02": ("Clean-Tech VC", "indirect_enabler"),
    "K:03": ("Green Bond -60bps", "indirect_enabler"),
    "K:04": ("QEA-2026 Solver", "indirect_enabler"),
    "K:05": ("Kaitiaki Story", "indirect_enabler"),
    "K:06": ("Solar Bequest", "indirect_enabler"),
    "K:07": ("Unified Climate Waka", "indirect_enabler"),
    "N:01": ("Zero-Friction Grid", "indirect_enabler"),
    "N:02": ("Adaptive Workforce", "indirect_enabler"),
    "N:03": ("Forward Carbon Audit", "indirect_enabler"),
    "N:04": ("Community Microgrids", "indirect_enabler"),
    "N:05": ("Clean R&D Compounding", "indirect_enabler"),
    "N:06": ("Sustainable Quality", "computed"),
    "H:01": ("Cancels LNG Trap", "indirect_enabler"),
    "H:02": ("Local Microgrid Trust", "indirect_enabler"),
    "H:03": ("Retains Green Engineers", "indirect_enabler"),
    "H:04": ("Intergen Solar Asset", "indirect_enabler"),
    "H:05": ("Armors Coast & Grid", "computed"),
    "E:01": ("-10.0 MtCO2e / yr", "computed"),
    "E:02": ("-14.8 MtCO2e / yr", "computed"),
    "E:03": ("-3.2 MtCO2e (No LNG)", "computed"),
}


def normalize_card_id(card_id: str) -> str:
    return card_id.strip().replace(":", "_")


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_theme_chain(themes_dir: Path, theme_name: str) -> list[Path]:
    visited = []
    queue = [theme_name]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.append(current)
        manifest = load_yaml(themes_dir / current / "theme.yaml")
        for fb in manifest.get("fallback_chain", []):
            if fb not in visited:
                queue.append(fb)
    if "generic" not in visited:
        visited.append("generic")
    return [themes_dir / t for t in visited]


def apply_lexicon(text: str, lexicon: dict) -> str:
    if not text or not lexicon:
        return text
    out = text
    for src, dst in lexicon.items():
        out = out.replace(src, dst)
    return out


def localize_card_for_theme(card: dict, theme_manifests: list[dict]) -> dict:
    """Apply theme card_overrides and lexicon_replacements (from most specific theme first)."""
    localized = copy.deepcopy(card)
    cid = localized["id"]

    # Apply from fallback up to active theme so active theme wins
    for manifest in reversed(theme_manifests):
        overrides = manifest.get("card_overrides", {}).get(cid, {})
        for k, v in overrides.items():
            localized[k] = copy.deepcopy(v)

        lexicon = manifest.get("lexicon_replacements", {})
        if lexicon:
            for field in ["name", "type", "gate_or_phase", "cost_or_requirement", "flavor_text"]:
                if field in localized and isinstance(localized[field], str):
                    localized[field] = apply_lexicon(localized[field], lexicon)
            for eff in localized.get("effects", []):
                eff["label"] = apply_lexicon(eff.get("label", ""), lexicon)
                eff["rule"] = apply_lexicon(eff.get("rule", ""), lexicon)

    return localized


def resolve_card_asset(card_id: str, theme_chain: list[Path]) -> tuple[str, Path | None, str]:
    stem = normalize_card_id(card_id)
    for theme_dir in theme_chain:
        assets_dir = theme_dir / "assets"
        if assets_dir.exists():
            for ext in IMAGE_EXTENSIONS:
                candidate = assets_dir / f"{stem}{ext}"
                if candidate.exists():
                    return ("image", candidate, theme_dir.name)
        md_candidate = theme_dir / "cards" / f"{stem}.md"
        if md_candidate.exists():
            return ("markdown_file", md_candidate, theme_dir.name)
    return ("generic_yaml", None, theme_chain[0].name)


def generate_card_markdown(card: dict) -> str:
    lines = [
        f"## {card['name']}",
        f"*{card['type']} — {', '.join(card.get('lens', []))}*",
        "",
        f"**Cost / Requirement:** {card.get('cost_or_requirement', 'None')}",
        "",
        "### Effects & Mechanics",
    ]
    for eff in card.get("effects", []):
        lines.append(f"* **{eff['label']}:** {eff['rule']}")
    lines.extend([
        "",
        f"> *\"{card.get('flavor_text', '')}\"*",
        "",
        f"**Empirical Anchor:** {card.get('empirical_anchor', '')}",
    ])
    return "\n".join(lines)


def md_to_html(md_text: str) -> str:
    if HAS_MARKDOWN:
        return markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    out = []
    for line in md_text.splitlines():
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("* "):
            out.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line.strip():
            out.append(f"<p>{html.escape(line)}</p>")
    return "\n".join(out)


def render_deck_html(
    cards_data: dict,
    theme_chain: list[Path],
    co2_pos: str = "top-right",
    populate_generic_md: bool = True,
) -> str:
    active_theme_name = theme_chain[0].name
    theme_manifests = [load_yaml(t / "theme.yaml") for t in theme_chain]

    generic_cards_dir = theme_chain[-1] / "cards"
    if populate_generic_md:
        generic_cards_dir.mkdir(parents=True, exist_ok=True)

    card_blocks = []
    for raw_card in cards_data.get("cards", []):
        cid = raw_card["id"]
        deck_prefix = cid.split(":")[0]
        stem = normalize_card_id(cid)

        if populate_generic_md:
            (generic_cards_dir / f"{stem}.md").write_text(
                generate_card_markdown(raw_card), encoding="utf-8"
            )

        # Localize card text using theme dictionary (card_overrides + lexicon_replacements)
        card = localize_card_for_theme(raw_card, theme_manifests)
        localized_md_text = generate_card_markdown(card)

        asset_type, asset_path, resolved_theme = resolve_card_asset(cid, theme_chain)

        co2_obj = card.get("co2e_impact", {})
        default_badge, default_status = DEFAULT_CO2E_BADGES.get(cid, ("CO2e: N/A", "na"))
        co2_badge = co2_obj.get("display", default_badge)
        co2_status = co2_obj.get("status", default_status)

        if asset_type == "image" and asset_path is not None:
            rel_img = asset_path.as_posix()
            body_html = (
                f'<div class="card-art"><img src="{rel_img}" alt="{html.escape(card["name"])}"/></div>'
                f'<div class="card-md-body compact">{md_to_html(localized_md_text)}</div>'
            )
        elif asset_type == "markdown_file" and asset_path is not None and resolved_theme == active_theme_name:
            custom_md = asset_path.read_text(encoding="utf-8")
            body_html = f'<div class="card-md-body">{md_to_html(custom_md)}</div>'
        else:
            body_html = f'<div class="card-md-body">{md_to_html(localized_md_text)}</div>'

        synergies = ", ".join(card.get("synergy_links", []))
        co2_badge_html = (
            f'<div class="co2e-badge status-{co2_status}" title="Anticipated CO2e Impact">'
            f'🌱 {html.escape(co2_badge)}</div>'
        )

        # Fixed header slots: never duplicate gate_or_phase!
        if co2_pos == "top-right":
            top_center_slot = html.escape(card.get("gate_or_phase", ""))
            top_right_slot = co2_badge_html
            bottom_right_slot = f'<span class="theme-tag">Theme: {html.escape(active_theme_name)}</span>'
        else:
            top_center_slot = f'<span class="theme-tag">Theme: {html.escape(active_theme_name)}</span>'
            top_right_slot = f'<span class="gate-label">{html.escape(card.get("gate_or_phase", ""))}</span>'
            bottom_right_slot = co2_badge_html

        card_blocks.append(f"""
        <article class="game-card deck-{deck_prefix}" id="card-{stem}">
          <header class="card-header">
            <div class="pdd-corner" title="Canonical Card ID">{html.escape(cid)}</div>
            <div class="header-center">{top_center_slot}</div>
            <div class="header-right">{top_right_slot}</div>
          </header>
          <main class="card-content">
            {body_html}
          </main>
          <footer class="card-footer">
            <div class="synergy-bar">🔗 <strong>Synergies:</strong> {html.escape(synergies)}</div>
            <div class="footer-right">{bottom_right_slot}</div>
          </footer>
        </article>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(cards_data['metadata']['game_title'])} ({html.escape(active_theme_name)})</title>
  <style>
    :root {{
      --card-w: 340px; --card-h: 500px;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
    }}
    body {{ font-family: var(--font-sans); background: #f4f6f8; margin: 24px; color: #1a202c; }}
    .deck-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(var(--card-w), 1fr)); gap: 20px; }}
    .game-card {{
      background: #ffffff; border: 4px solid #2d3748; border-radius: 14px;
      display: flex; flex-direction: column; justify-content: space-between;
      min-height: var(--card-h); padding: 12px 14px; box-sizing: border-box;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08); page-break-inside: avoid;
    }}
    .deck-B {{ border-color: #1B4F72; }} .deck-T {{ border-color: #922B21; }}
    .deck-C {{ border-color: #117864; }} .deck-K {{ border-color: #B7950B; }}
    .deck-N {{ border-color: #512E5F; }} .deck-H {{ border-color: #424949; }}
    .deck-E {{ border-color: #196F3D; }}
    .card-header {{
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
      border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 8px;
    }}
    .pdd-corner {{
      font-family: var(--font-mono); font-size: 1.25rem; font-weight: 800;
      background: #1a202c; color: #fff; padding: 3px 9px; border-radius: 6px;
    }}
    .header-center {{ font-size: 0.70rem; font-weight: 600; color: #4a5568; text-transform: uppercase; }}
    .gate-label {{ font-size: 0.72rem; font-weight: 700; color: #2d3748; text-transform: uppercase; }}
    .theme-tag {{ font-size: 0.68rem; color: #718096; font-weight: 600; }}
    .co2e-badge {{
      font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
      background: #e6fffa; color: #065f46; border: 1px solid #38b2ac;
      padding: 3px 7px; border-radius: 6px; white-space: nowrap;
    }}
    .co2e-badge.status-hazard_increase {{ background: #fff5f5; color: #9b2c2c; border-color: #feb2b2; }}
    .card-content {{ flex: 1; overflow: hidden; font-size: 0.80rem; line-height: 1.32; }}
    .card-content h2 {{ font-size: 1.02rem; margin: 2px 0 4px 0; color: #1a202c; }}
    .card-content h3 {{ font-size: 0.82rem; margin: 6px 0 3px 0; text-transform: uppercase; color: #2d3748; }}
    .card-content ul {{ padding-left: 16px; margin: 4px 0; }}
    .card-content li {{ margin-bottom: 4px; }}
    .card-content blockquote {{
      margin: 8px 0 4px 0; padding: 5px 8px; background: #f7fafc;
      border-left: 3px solid #cbd5e0; font-size: 0.75rem; color: #4a5568;
    }}
    .card-art img {{ width: 100%; max-height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 6px; }}
    .card-footer {{
      display: flex; align-items: center; justify-content: space-between;
      border-top: 1px solid #e2e8f0; padding-top: 6px; margin-top: 8px; font-size: 0.70rem; color: #4a5568;
    }}
    @media print {{
      body {{ background: #fff; margin: 0; }}
      .deck-grid {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    }}
  </style>
</head>
<body>
  <div class="deck-grid">
    {''.join(card_blocks)}
  </div>
</body>
</html>"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render Foils & Founders cards with theme dictionaries.")
    parser.add_argument("--cards", default="decks/cards.yaml", help="Path to master cards.yaml")
    parser.add_argument("--themes-dir", default="themes", help="Directory containing theme folders")
    parser.add_argument("--theme", default="generic", help="Active theme name (e.g., generic, waka_hourua, foils_pakeha)")
    parser.add_argument("--co2-pos", choices=["top-right", "bottom-right"], default="top-right")
    parser.add_argument("--export-generic-md", action="store_true", help="Export raw .md files to themes/generic/cards/")
    parser.add_argument("--out", default="build/deck_preview.html", help="Output HTML path")
    args = parser.parse_args()

    cards_data = load_yaml(Path(args.cards))
    chain = build_theme_chain(Path(args.themes_dir), args.theme)
    html_out = render_deck_html(
        cards_data, chain, co2_pos=args.co2_pos, populate_generic_md=args.export_generic_md
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Rendered {len(cards_data.get('cards', []))} cards using theme chain {[p.name for p in chain]} -> {out_path}")
