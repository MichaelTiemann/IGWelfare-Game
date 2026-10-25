#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — Multi-Theme Card Renderer
License: CC-BY-SA-4.0 / GPL-3.0-or-later
Author: Michael Tiemann (https://github.com/MichaelTiemann/IGWelfare)

Usage:
  python3 scripts/render_cards.py --theme generic --co2-pos top-right
  python3 scripts/render_cards.py --theme waka_hourua --co2-pos bottom-right
"""

import argparse
import html
from pathlib import Path
import yaml

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

IMAGE_EXTENSIONS = [".svg", ".png", ".webp", ".jpg", ".jpeg"]


def normalize_card_id(card_id: str) -> str:
    """Convert 'B:01' -> 'B_01' for filesystem-safe canonical asset lookup."""
    return card_id.strip().replace(":", "_")


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_theme_chain(themes_dir: Path, theme_name: str) -> list[Path]:
    """Resolve the recursive fallback_chain ending at 'generic'."""
    visited = []
    queue = [theme_name]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.append(current)
        manifest_path = themes_dir / current / "theme.yaml"
        if manifest_path.exists():
            manifest = load_yaml(manifest_path)
            for fb in manifest.get("fallback_chain", []):
                if fb not in visited:
                    queue.append(fb)
    if "generic" not in visited:
        visited.append("generic")
    return [themes_dir / t for t in visited]


def resolve_card_asset(card_id: str, theme_chain: list[Path]) -> tuple[str, Path | None, str]:
    """
    Search theme_chain for canonical artwork or Markdown override.
    Returns: (asset_type, asset_path, resolved_theme_name)
      where asset_type is 'image', 'markdown_file', or 'generic_yaml'.
    """
    stem = normalize_card_id(card_id)
    for theme_dir in theme_chain:
        # 1. Check for visual artwork in assets/
        assets_dir = theme_dir / "assets"
        if assets_dir.exists():
            for ext in IMAGE_EXTENSIONS:
                candidate = assets_dir / f"{stem}{ext}"
                if candidate.exists():
                    return ("image", candidate, theme_dir.name)
        # 2. Check for custom Markdown layout in cards/
        md_candidate = theme_dir / "cards" / f"{stem}.md"
        if md_candidate.exists():
            return ("markdown_file", md_candidate, theme_dir.name)

    return ("generic_yaml", None, "generic")


def generate_generic_markdown(card: dict) -> str:
    """Generate the canonical Generic Markdown representation of a card."""
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
    """Convert Markdown text to HTML (uses python-markdown if installed, else clean fallback)."""
    if HAS_MARKDOWN:
        return markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    # Lightweight zero-dependency fallback
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
    """Render all cards into a responsive HTML/CSS print-and-play sheet."""
    generic_cards_dir = theme_chain[-1] / "cards"
    if populate_generic_md:
        generic_cards_dir.mkdir(parents=True, exist_ok=True)

    card_blocks = []
    for card in cards_data.get("cards", []):
        cid = card["id"]
        deck_prefix = cid.split(":")[0]
        stem = normalize_card_id(cid)

        # Populate themes/generic/cards/{P_DD}.md so artists/writers can inspect/fork it
        generic_md_text = generate_generic_markdown(card)
        if populate_generic_md:
            (generic_cards_dir / f"{stem}.md").write_text(generic_md_text, encoding="utf-8")

        asset_type, asset_path, resolved_theme = resolve_card_asset(cid, theme_chain)

        # Extract CO2e badge (or default placeholder slot)
        co2_obj = card.get("co2e_impact", {})
        co2_badge = co2_obj.get("display", "CO2e: N/A")
        co2_status = co2_obj.get("status", "na")

        # Render body according to resolved asset_type
        if asset_type == "image" and asset_path is not None:
            rel_img = asset_path.as_posix()
            body_html = (
                f'<div class="card-art"><img src="{rel_img}" alt="{html.escape(card["name"])}"/></div>'
                f'<div class="card-md-body compact">{md_to_html(generic_md_text)}</div>'
            )
        elif asset_type == "markdown_file" and asset_path is not None:
            custom_md = asset_path.read_text(encoding="utf-8")
            body_html = f'<div class="card-md-body">{md_to_html(custom_md)}</div>'
        else:
            body_html = f'<div class="card-md-body">{md_to_html(generic_md_text)}</div>'

        synergies = ", ".join(card.get("synergy_links", []))
        co2_badge_html = (
            f'<div class="co2e-badge status-{co2_status}" title="Anticipated CO2e Impact">'
            f'🌱 {html.escape(co2_badge)}</div>'
        )

        top_right_slot = (
            co2_badge_html
            if co2_pos == "top-right"
            else f'<span class="gate-label">{html.escape(card.get("gate_or_phase", ""))}</span>'
        )
        bottom_right_slot = (
            co2_badge_html
            if co2_pos == "bottom-right"
            else f'<span class="theme-tag">Theme: {resolved_theme}</span>'
        )

        card_blocks.append(f"""
        <article class="game-card deck-{deck_prefix}" id="card-{stem}">
          <header class="card-header">
            <div class="pdd-corner" title="Canonical Card ID">{html.escape(cid)}</div>
            <div class="header-center">{html.escape(card.get("gate_or_phase", ""))}</div>
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
  <title>{html.escape(cards_data['metadata']['game_title'])}</title>
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
      display: flex; align-items: center; justify-content: space-between;
      border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 8px;
    }}
    .pdd-corner {{
      font-family: var(--font-mono); font-size: 1.25rem; font-weight: 800;
      background: #1a202c; color: #fff; padding: 3px 9px; border-radius: 6px;
    }}
    .header-center {{ font-size: 0.72rem; font-weight: 600; color: #4a5568; text-transform: uppercase; }}
    .co2e-badge {{
      font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
      background: #e6fffa; color: #065f46; border: 1px solid #38b2ac;
      padding: 3px 7px; border-radius: 6px; white-space: nowrap;
    }}
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
    parser = argparse.ArgumentParser(description="Render Foils & Founders cards with theme fallbacks.")
    parser.add_argument("--cards", default="decks/cards.yaml", help="Path to master cards.yaml")
    parser.add_argument("--themes-dir", default="themes", help="Directory containing theme folders")
    parser.add_argument("--theme", default="generic", help="Active theme name (falls back to generic)")
    parser.add_argument("--co2-pos", choices=["top-right", "bottom-right"], default="top-right")
    parser.add_argument("--out", default="build/deck_preview.html", help="Output HTML path")
    args = parser.parse_args()

    cards_data = load_yaml(Path(args.cards))
    chain = build_theme_chain(Path(args.themes_dir), args.theme)
    html_out = render_deck_html(cards_data, chain, co2_pos=args.co2_pos)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Rendered {len(cards_data.get('cards', []))} cards using theme chain {[p.name for p in chain]} -> {out_path}")
