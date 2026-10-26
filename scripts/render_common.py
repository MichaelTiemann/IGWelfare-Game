#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — Shared Rendering Utilities
================================================================
Common YAML loading, resilient theme resolution (with built-in defaults
if `themes/generic/theme.yaml` is absent), copyright constants, and base
A3 Landscape (420mm x 297mm) print CSS shared by `render_cards.py` and
`render_boards.py`.
"""

import html
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("Error: PyYAML is required. Install with: pip install pyyaml\n")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent

COPYRIGHT_SHEET_HTML = (
    "&copy; 2026 Michael Tiemann. Licensed under Creative Commons "
    "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)."
)
COPYRIGHT_CARD_HTML = "&copy; 2026 Michael Tiemann &bull; CC BY-SA 4.0"

DEFAULT_THEME_CONFIG = {
    "theme_id": "generic",
    "theme_name": "Generic Typographic Theme (Markdown Root)",
    "fallback_chain": [],
    "typography": {
        "heading_font": "'Inter', 'Helvetica Neue', Arial, sans-serif",
        "body_font": "'Inter', system-ui, -apple-system, sans-serif",
        "mono_font": "'JetBrains Mono', 'Fira Code', monospace",
    },
    "deck_palettes": {
        "B": {"name": "Base Game — Up on Foils", "border": "#0284c7", "header_bg": "#e0f2fe", "badge_bg": "#0369a1", "badge_text": "#ffffff"},
        "T": {"name": "Cautionary Traps", "border": "#d97706", "header_bg": "#fef3c7", "badge_bg": "#b45309", "badge_text": "#ffffff"},
        "C": {"name": "Climate & Resilience", "border": "#059669", "header_bg": "#d1fae5", "badge_bg": "#047857", "badge_text": "#ffffff"},
        "K": {"name": "Wayfinders & Kaupapa", "border": "#7c3aed", "header_bg": "#ede9fe", "badge_bg": "#6d28d9", "badge_text": "#ffffff"},
        "N": {"name": "Nobel Laureate Archive", "border": "#ca8a04", "header_bg": "#fef9c3", "badge_bg": "#a16207", "badge_text": "#ffffff"},
        "H": {"name": "Orthodoxy Boss Deck", "border": "#dc2626", "header_bg": "#fee2e2", "badge_bg": "#b91c1c", "badge_text": "#ffffff"},
        "E": {"name": "Electrification & Grid", "border": "#0d9488", "header_bg": "#ccfbf1", "badge_bg": "#0f766e", "badge_text": "#ffffff"},
    },
}

THEME_ACCENTS = {
    "generic": "#1e293b",
    "waka_hourua": "#0f766e",
    "foils_pakeha": "#0284c7",
}


def load_yaml(path: Path, required: bool = True) -> dict:
    """Loads a YAML file, returning {} if optional and missing."""
    if not path.exists():
        if required:
            sys.stderr.write(f"Error: Required YAML file not found: {path}\n")
            sys.exit(1)
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merges override dict into a copy of base dict."""
    merged = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = v
    return merged


def resolve_theme_config(themes_dir: Path, theme_name: str) -> dict:
    """
    Resolves theme configuration with automatic fallback to DEFAULT_THEME_CONFIG
    so rendering succeeds even if `themes/generic/theme.yaml` is not on disk.
    """
    cfg = dict(DEFAULT_THEME_CONFIG)

    generic_yaml = themes_dir / "generic" / "theme.yaml"
    if generic_yaml.exists():
        cfg = deep_merge(cfg, load_yaml(generic_yaml, required=False))

    if theme_name != "generic":
        theme_yaml = themes_dir / theme_name / "theme.yaml"
        if theme_yaml.exists():
            active_cfg = load_yaml(theme_yaml, required=False)
            # Apply any intermediate fallback themes first
            for fb in reversed(active_cfg.get("fallback_chain", [])):
                if fb != "generic":
                    fb_yaml = themes_dir / fb / "theme.yaml"
                    if fb_yaml.exists():
                        cfg = deep_merge(cfg, load_yaml(fb_yaml, required=False))
            cfg = deep_merge(cfg, active_cfg)
        else:
            # Sensible display name even if theme folder isn't created yet
            friendly_names = {
                "waka_hourua": "Te Waka Hourua — Māori & Pasifika Pūrākau Theme",
                "foils_pakeha": "Up on Foils — America's Cup Systems Engineering Theme",
            }
            cfg["theme_id"] = theme_name
            cfg["theme_name"] = friendly_names.get(theme_name, theme_name)

    return cfg


def build_theme_search_order(themes_dir: Path, theme_name: str, theme_cfg: dict) -> list[str]:
    """Returns ordered list of theme folder names to search for overrides/assets."""
    chain = [theme_name]
    for fb in theme_cfg.get("fallback_chain", []):
        if fb not in chain:
            chain.append(fb)
    if "generic" not in chain:
        chain.append("generic")
    return chain


def get_base_a3_css(font_heading: str, font_body: str, font_mono: str, accent: str = "#1e293b") -> str:
    """Returns the shared A3 Landscape (@page, .a3-sheet, .sheet-footer) CSS rules."""
    return f"""
    :root {{
      --font-heading: {font_heading};
      --font-body: {font_body};
      --font-mono: {font_mono};
      --accent: {accent};
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: var(--font-body);
      background: #e2e8f0;
      color: #0f172a;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    @page {{
      size: A3 landscape;
      margin: 0;
    }}
    .a3-sheet {{
      width: 420mm;
      height: 297mm;
      background: #ffffff;
      margin: 8mm auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
      overflow: hidden;
    }}
    @media print {{
      body {{
        background: #ffffff;
      }}
      .a3-sheet {{
        margin: 0;
        box-shadow: none;
      }}
    }}
    .sheet-footer {{
      font-family: var(--font-mono);
      font-size: 7pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 3mm;
    }}
    """


def build_sheet_footer_html(right_label: str) -> str:
    """Returns the standardized A3 sheet footer with CC BY-SA 4.0 left & sheet label right."""
    return f"""
    <div class="sheet-footer">
      <span>{COPYRIGHT_SHEET_HTML}</span>
      <span>{right_label}</span>
    </div>
    """
  
