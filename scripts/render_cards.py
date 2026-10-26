#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — Multi-Theme Card Renderer (v3.1)
Supports Theme Dictionaries (card_overrides + lexicon_replacements), CO2e Badges,
T:04 Lavoisier Syndrome, and 7+1 Open-Source Extensibility Wildcards (50/50 A3 Slots).
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
DECK_ORDER = ["B", "T", "C", "K", "N", "H", "E"]

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
    "T:04": ("Stalls Clean-Tech R&D", "hazard_increase"),
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

WILDCARD_SPEC = {
    "B": (
        "B:??",
        "Base Foil Wildcard (Design a Lifecycle Lever)",
        "Cohort Identity or Structural Foil — Lenses 1, 2, or 3",
        "Propose a new developmental gate, housing lever, or actuarial rule within the NZD 9.19B SS1 envelope.",
    ),
    "T": (
        "T:??",
        "Cautionary Trap Wildcard (Spot a Policy Pitfall)",
        "Single-Lens Pitch-Pole or Rent-Seeking Trap",
        "Document a real-world domestic or international policy trap where solving one lens in isolation backfires.",
    ),
    "C": (
        "C:??",
        "Climate & Resilience Wildcard (Armor the Waka)",
        "Adaptation, Biodiversity, or Regional Just-Transition Card",
        "Propose a community microgrid, catchment restoration, or spatial resilience buffer anchored to C:01–C:06.",
    ),
    "K": (
        "K:??",
        "Wayfinder & Kaupapa Wildcard (Bring Your Mandate)",
        "Companion Persona — Innate Kaupapa + Two Dual-Class Synergies",
        "Add a new community, iwi, union, local-government, or youth persona who brings a vital lens to the Big Table.",
    ),
    "N": (
        "N:??",
        "Theoretical Milestone Wildcard (Stand on Giants)",
        "Economic / Systems Theory Proof — Open-Source Archive",
        "Cite a peer-reviewed theorem or natural experiment that unlocks a non-rival multiplier across the board.",
    ),
    "H": (
        "H:??",
        "Orthodoxy Boss Wildcard (Name theBlocker & Counter)",
        "Institutional Hazard -> Coupled Combo Counter-Play",
        "Write an entrenched status-quo objection at the top, and the exact multi-card combo that defeats it below.",
    ),
    "E": (
        "E:??",
        "Game-Changer Wildcard (Fork the VFI GPU Engine)",
        "Track 2 Stationary-Distribution Shift — Challenge Mode",
        "Modify a state variable or shock in VFI Toolkit (like QEA-2026) to unlock trapped precautionary capital.",
    ),
}


def normalize_card_id(card_id: str) -> str:
    return card_id.strip().replace(":", "_").replace("?", "X")


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
    localized = copy.deepcopy(card)
    cid = localized["id"]
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


def build_wildcard_html(
    deck_prefix: str,
    cid: str,
    title: str,
    subtitle: str,
    prompt_text: str,
    active_theme_name: str,
    co2_pos: str,
) -> str:
    """Render an interactive/write-in Open-Source Extensibility Card for each deck."""
    co2_badge_html = '<div class="co2e-badge status-na">🌱 CO2e: ______</div>'
    if co2_pos == "top-right":
        top_center = "OPEN-SOURCE PR SLOT"
        top_right = co2_badge_html
        bottom_right = f'<span class="theme-tag">Theme: {html.escape(active_theme_name)}</span>'
    else:
        top_center = f'<span class="theme-tag">Theme: {html.escape(active_theme_name)}</span>'
        top_right = '<span class="gate-label">OPEN-SOURCE PR SLOT</span>'
        bottom_right = co2_badge_html

    return f"""
    <article class="game-card wildcard-card deck-{deck_prefix}" id="card-{normalize_card_id(cid)}">
      <header class="card-header">
        <div class="pdd-corner wildcard-pdd">{html.escape(cid)}</div>
        <div class="header-center">{top_center}</div>
        <div class="header-right">{top_right}</div>
      </header>
      <main class="card-content">
        <h2>{html.escape(title)}</h2>
        <p><em>{html.escape(subtitle)}</em></p>
        <p class="wildcard-prompt">{html.escape(prompt_text)}</p>
        <h3>Write-In Card Draft (Or Submit via GitHub PR)</h3>
        <div class="write-in-lines">
          <div class="write-line"><span>Card Name &amp; Gate:</span></div>
          <div class="write-line"><span>Cost / Requirement:</span></div>
          <div class="write-line"><span>Mechanic 1 (Effect):</span></div>
          <div class="write-line"></div>
          <div class="write-line"><span>Mechanic 2 (Synergy / Crowd-Out Check):</span></div>
          <div class="write-line"></div>
          <div class="write-line"><span>Empirical Anchor / Citation:</span></div>
        </div>
        <blockquote>
          <em>"This game is licensed under CC-BY-SA-4.0. Copy metadata/card_template.yaml and submit a Pull Request to github.com/MichaelTiemann/IGWelfare-Game!"</em>
        </blockquote>
      </main>
      <footer class="card-footer">
        <div class="synergy-bar">🔗 <strong>Synergies:</strong> ____, ____, ____</div>
        <div class="footer-right">{bottom_right}</div>
      </footer>
    </article>
    """


def render_deck_html(
    cards_data: dict,
    theme_chain: list[Path],
    co2_pos: str = "top-right",
    populate_generic_md: bool = False,
    include_wildcards: bool = True,
) -> str:
    active_theme_name = theme_chain[0].name
    theme_manifests = [load_yaml(t / "theme.yaml") for t in theme_chain]

    if populate_generic_md:
        generic_cards_dir = theme_chain[-1] / "cards"
        generic_cards_dir.mkdir(parents=True, exist_ok=True)

    # Group cards by deck prefix so T:04 sits right after T:03 and each deck can end with its P:?? wildcard
    grouped_cards: dict[str, list[dict]] = {p: [] for p in DECK_ORDER}
    for raw_card in cards_data.get("cards", []):
        prefix = raw_card["id"].split(":")[0]
        grouped_cards.setdefault(prefix, []).append(raw_card)

    for prefix in grouped_cards:
        grouped_cards[prefix].sort(key=lambda c: c["id"])

    card_blocks = []
    for deck_prefix in DECK_ORDER:
        for raw_card in grouped_cards.get(deck_prefix, []):
            cid = raw_card["id"]
            stem = normalize_card_id(cid)

            if populate_generic_md:
                (generic_cards_dir / f"{stem}.md").write_text(
                    generate_card_markdown(raw_card), encoding="utf-8"
                )

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
                    f'<div class="card-md-body">{md_to_html(localized_md_text)}</div>'
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
                <div class="pdd-corner">{html.escape(cid)}</div>
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

        # Append the Deck-Specific Extensibility Wildcard (B:??, T:??, C:??, K:??, N:??, H:??, E:??)
        if include_wildcards and deck_prefix in WILDCARD_SPEC:
            w_cid, w_title, w_sub, w_prompt = WILDCARD_SPEC[deck_prefix]
            card_blocks.append(
                build_wildcard_html(
                    deck_prefix, w_cid, w_title, w_sub, w_prompt, active_theme_name, co2_pos
                )
            )

    # If 42 cards + 7 wildcards = 49 cards, add the 50th Master Open-Source Contributor Card to fill Sheet 5!
    if include_wildcards and len(card_blocks) % 10 == 9:
        card_blocks.append(
            build_wildcard_html(
                "B",
                "*:50",
                "Fork the Deck: How to Contribute a Pull Request",
                "Tracks 1–4 Open-Source Contribution Guide (CC-BY-SA-4.0)",
                "Track 1: First-Order Card | Track 2: VFI GPU Shift | Track 3: Demographic CSVs | Track 4: Art Theme.",
                active_theme_name,
                co2_pos,
            )
        )

    # Build strict 5-column x 2-row Stacked-Bond A3 Landscape sheets (10 cards per sheet)
    cols = 5
    rows_per_sheet = 2
    cards_per_sheet = cols * rows_per_sheet
    total_sheets = (len(card_blocks) + cards_per_sheet - 1) // cards_per_sheet
    sheet_blocks = []

    for s in range(total_sheets):
        sheet_cards = card_blocks[s * cards_per_sheet : (s + 1) * cards_per_sheet]
        row_htmls = []
        for r in range(rows_per_sheet):
            row_cards = sheet_cards[r * cols : (r + 1) * cols]
            if not row_cards:
                continue
            while len(row_cards) < cols:
                row_cards.append('<div class="game-card empty-slot"></div>')
            cells = "".join(f"<td>{c}</td>" for c in row_cards)
            row_htmls.append(f"<tr>{cells}</tr>")

        sheet_blocks.append(f"""
        <section class="a3-sheet">
          <table class="stacked-bond-table">
            <tbody>
              {''.join(row_htmls)}
            </tbody>
          </table>
          <div class="sheet-footer">
            Foils &amp; Founders: The Aotearoa Deck ({html.escape(active_theme_name)}) — A3 Landscape Sheet {s + 1} of {total_sheets} (5&times;2 Stacked Bond — Cut along dashed lines)
          </div>
        </section>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(cards_data['metadata']['game_title'])} ({html.escape(active_theme_name)})</title>
  <style>
    @page {{
      size: A3 landscape;
      margin: 6mm;
    }}
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
    }}
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    body {{
      font-family: var(--font-sans);
      background: #cbd5e1;
      margin: 0;
      padding: 16px;
      color: #1a202c;
    }}
    .a3-sheet {{
      width: 408mm;
      height: 285mm;
      background: #ffffff;
      margin: 0 auto 24px auto;
      padding: 4mm 5mm 3mm 5mm;
      box-shadow: 0 8px 24px rgba(0,0,0,0.18);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    .stacked-bond-table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 3mm;
      table-layout: fixed;
      margin: 0 auto;
    }}
    .stacked-bond-table td {{
      width: 76.8mm;
      height: 133mm;
      padding: 0;
      vertical-align: top;
    }}
    .sheet-footer {{
      font-family: var(--font-mono);
      font-size: 7pt;
      color: #64748b;
      text-align: right;
      padding-right: 3mm;
    }}
    .game-card {{
      width: 76.8mm;
      height: 133mm;
      background: #ffffff;
      border: 1.2mm solid #2d3748;
      outline: 0.25mm dashed #94a3b8;
      outline-offset: 1.2mm;
      border-radius: 3.5mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 2.2mm 2.8mm;
      overflow: hidden;
    }}
    .game-card.wildcard-card {{
      background: #fcfcfd;
      border-style: dashed;
    }}
    .wildcard-pdd {{
      background: #475569 !important;
    }}
    .wildcard-prompt {{
      font-size: 6.2pt;
      color: #334155;
      background: #f1f5f9;
      padding: 1.2mm 1.6mm;
      border-radius: 1mm;
    }}
    .write-in-lines {{
      display: flex;
      flex-direction: column;
      gap: 2.8mm;
      margin: 1.8mm 0;
    }}
    .write-line {{
      border-bottom: 0.35mm dotted #94a3b8;
      height: 4.8mm;
      font-size: 5.6pt;
      font-weight: 700;
      color: #64748b;
      display: flex;
      align-items: flex-end;
      padding-bottom: 0.4mm;
    }}
    .game-card.empty-slot {{
      border: 0.3mm dashed #e2e8f0;
      outline: none;
      background: transparent;
    }}
    .deck-B {{ border-color: #1B4F72; }}
    .deck-T {{ border-color: #922B21; }}
    .deck-C {{ border-color: #117864; }}
    .deck-K {{ border-color: #B7950B; }}
    .deck-N {{ border-color: #512E5F; }}
    .deck-H {{ border-color: #424949; }}
    .deck-E {{ border-color: #196F3D; }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1.2mm;
      border-bottom: 0.4mm solid #cbd5e1;
      padding-bottom: 1mm;
      margin-bottom: 1.2mm;
      flex-shrink: 0;
    }}
    .pdd-corner {{
      font-family: var(--font-mono);
      font-size: 9pt;
      font-weight: 800;
      background: #1a202c;
      color: #ffffff;
      padding: 0.5mm 1.8mm;
      border-radius: 1mm;
      flex-shrink: 0;
    }}
    .header-center, .gate-label {{
      font-size: 5.3pt;
      font-weight: 700;
      color: #475569;
      text-transform: uppercase;
      text-align: center;
      line-height: 1.1;
    }}
    .theme-tag {{
      font-size: 5.3pt;
      color: #64748b;
      font-weight: 600;
      white-space: nowrap;
    }}
    .co2e-badge {{
      font-family: var(--font-mono);
      font-size: 5.5pt;
      font-weight: 700;
      background: #e6fffa;
      color: #065f46;
      border: 0.3mm solid #38b2ac;
      padding: 0.4mm 1.4mm;
      border-radius: 1mm;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .co2e-badge.status-hazard_increase {{
      background: #fff5f5;
      color: #9b2c2c;
      border-color: #feb2b2;
    }}
    .co2e-badge.status-na {{
      background: #f8fafc;
      color: #475569;
      border-color: #cbd5e1;
    }}
    .card-content {{
      flex: 1 1 auto;
      overflow: hidden;
      font-size: 6.8pt;
      line-height: 1.24;
    }}
    .card-content h2 {{
      font-size: 8.2pt;
      line-height: 1.14;
      margin: 0.4mm 0 0.8mm 0;
      color: #0f172a;
    }}
    .card-content h3 {{
      font-size: 6.2pt;
      margin: 1.2mm 0 0.5mm 0;
      text-transform: uppercase;
      color: #334155;
      letter-spacing: 0.02em;
    }}
    .card-content p {{
      margin: 0.7mm 0;
    }}
    .card-content ul {{
      padding-left: 3.2mm;
      margin: 0.7mm 0;
    }}
    .card-content li {{
      margin-bottom: 0.7mm;
    }}
    .card-content blockquote {{
      margin: 1mm 0 0.7mm 0;
      padding: 0.9mm 1.6mm;
      background: #f8fafc;
      border-left: 0.7mm solid #94a3b8;
      font-size: 0.92em;
      color: #334155;
    }}
    .card-art img {{
      width: 100%;
      max-height: 34mm;
      object-fit: cover;
      border-radius: 1.5mm;
      margin-bottom: 1mm;
    }}
    .card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1mm;
      border-top: 0.3mm solid #cbd5e1;
      padding-top: 0.9mm;
      margin-top: 0.9mm;
      font-size: 5.5pt;
      color: #475569;
      flex-shrink: 0;
    }}
    @media print {{
      body {{
        background: #ffffff;
        padding: 0;
        margin: 0;
      }}
      .a3-sheet {{
        margin: 0;
        box-shadow: none;
        page-break-after: always;
        break-after: page;
      }}
    }}
  </style>
</head>
<body>
  {''.join(sheet_blocks)}
  <script>
    function fitAllCards() {{
      document.querySelectorAll('.game-card:not(.empty-slot)').forEach(card => {{
        const content = card.querySelector('.card-content');
        if (!content) return;
        let sizePt = 6.8;
        content.style.fontSize = sizePt + 'pt';
        while (content.scrollHeight > content.clientHeight + 1 && sizePt > 4.6) {{
          sizePt -= 0.15;
          content.style.fontSize = sizePt.toFixed(2) + 'pt';
          content.style.lineHeight = '1.16';
        }}
      }});
    }}
    window.addEventListener('load', fitAllCards);
    window.addEventListener('beforeprint', fitAllCards);
  </script>
</body>
</html>"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render Foils & Founders cards in 5x2 Stacked-Bond A3 sheets.")
    parser.add_argument("--cards", default="decks/cards.yaml", help="Path to master cards.yaml")
    parser.add_argument("--themes-dir", default="themes", help="Directory containing theme folders")
    parser.add_argument("--theme", default="generic", help="Active theme name (e.g., generic, waka_hourua, foils_pakeha)")
    parser.add_argument("--co2-pos", choices=["top-right", "bottom-right"], default="top-right")
    parser.add_argument("--no-wildcards", action="store_true", help="Omit the 7+1 open-source write-in wildcard cards")
    parser.add_argument("--export-generic-md", action="store_true", help="Export raw .md files to themes/generic/cards/")
    parser.add_argument("--out", default="build/deck_preview.html", help="Output HTML path")
    args = parser.parse_args()

    cards_data = load_yaml(Path(args.cards))
    chain = build_theme_chain(Path(args.themes_dir), args.theme)
    html_out = render_deck_html(
        cards_data,
        chain,
        co2_pos=args.co2_pos,
        populate_generic_md=args.export_generic_md,
        include_wildcards=not args.no_wildcards,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Rendered deck (wildcards={not args.no_wildcards}) in 5x2 Stacked-Bond A3 sheets -> {out_path}")
