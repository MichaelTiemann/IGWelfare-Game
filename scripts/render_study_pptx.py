#!/usr/bin/env python3
"""
Foils & Founders: 46-Slide Google Slides (.pptx) Exporter with Verified TeX Math
================================================================================
Renders every equation using Computer Modern ('cm') math typography into a crisp
360-DPI transparent PNG (with zero raw text overlays) and verifies that all 46
equations compile through the TeX math parser with 0 fallbacks.

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations
import io
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser

# Force authentic Computer Modern (LaTeX) math typography
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.family"] = "serif"

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
CARDS_YAML = ROOT / "decks" / "cards.yaml"
STUDY_YAML = ROOT / "decks" / "study_cards.yaml"
OUT_DIR = ROOT / "output"
OUT_PPTX = OUT_DIR / "foils_and_founders_study_slides.pptx"

MATH_PARSER = MathTextParser("agg")
import argparse

THEMES: Dict[str, Dict[str, Any]] = {
    "hydrofoil": {
        "label": "Up on Foils (Deep Pacific Navy)",
        "suffix": "",
        "bg_dark": RGBColor(0x07, 0x13, 0x24),
        "panel_play": RGBColor(0x0B, 0x1F, 0x36),
        "panel_study": RGBColor(0x10, 0x1D, 0x30),
        "eq_bg": RGBColor(0x05, 0x0E, 0x1A),
        "text_main": RGBColor(0xFF, 0xFF, 0xFF),
        "text_muted": RGBColor(0xA8, 0xDA, 0xDC),
        "gold": RGBColor(0xF4, 0xC9, 0x7E),
        "green": RGBColor(0x80, 0xED, 0x99),
        "cyan": RGBColor(0x00, 0xB4, 0xD8),
        "eq_hex_1": "#FFFFFF",
        "eq_hex_2": "#F4C97E",
    },
    "waka": {
        "label": "Te Waka Hourua (Kauri, Pounamu & Kokowai)",
        "suffix": "_waka",
        "bg_dark": RGBColor(0x14, 0x0E, 0x0B),
        "panel_play": RGBColor(0x1F, 0x16, 0x12),
        "panel_study": RGBColor(0x12, 0x21, 0x1D),
        "eq_bg": RGBColor(0x0D, 0x09, 0x07),
        "text_main": RGBColor(0xF9, 0xF4, 0xEC),
        "text_muted": RGBColor(0xD8, 0xC3, 0xA5),
        "gold": RGBColor(0xE9, 0xB8, 0x62),
        "green": RGBColor(0x52, 0xB7, 0x88),
        "cyan": RGBColor(0xE7, 0x6F, 0x51),
        "eq_hex_1": "#FFF8EE",
        "eq_hex_2": "#E9B862",
    },
    "academic": {
        "label": "Academic Monograph & Print (Daylight Ivory)",
        "suffix": "_academic",
        "bg_dark": RGBColor(0xF7, 0xF4, 0xED),
        "panel_play": RGBColor(0xFF, 0xFF, 0xFF),
        "panel_study": RGBColor(0xF0, 0xF4, 0xF8),
        "eq_bg": RGBColor(0xFF, 0xFD, 0xF9),
        "text_main": RGBColor(0x14, 0x21, 0x3D),
        "text_muted": RGBColor(0x4A, 0x55, 0x68),
        "gold": RGBColor(0x8C, 0x2D, 0x19),
        "green": RGBColor(0x1B, 0x5E, 0x20),
        "cyan": RGBColor(0x00, 0x5F, 0x73),
        "eq_hex_1": "#0B1F36",
        "eq_hex_2": "#8C2D19",
        "deck_overrides": {
            "B": RGBColor(0x1B, 0x6B, 0x5D),
            "T": RGBColor(0xB8, 0x1D, 0x24),
            "C": RGBColor(0x00, 0x66, 0x99),
            "K": RGBColor(0x9A, 0x67, 0x00),
            "N": RGBColor(0x6B, 0x3F, 0x7D),
            "H": RGBColor(0xC8, 0x5A, 0x00),
            "E": RGBColor(0x1E, 0x70, 0x3A),
        },
    },
    "blueprint": {
        "label": "1925 Quantum Blueprint ( Naval & Systems Grid )",
        "suffix": "_blueprint",
        "bg_dark": RGBColor(0x06, 0x1A, 0x38),
        "panel_play": RGBColor(0x0A, 0x27, 0x52),
        "panel_study": RGBColor(0x08, 0x21, 0x45),
        "eq_bg": RGBColor(0x04, 0x12, 0x28),
        "text_main": RGBColor(0xEC, 0xF8, 0xF8),
        "text_muted": RGBColor(0x90, 0xE0, 0xEF),
        "gold": RGBColor(0xFF, 0xD1, 0x66),
        "green": RGBColor(0x72, 0xEF, 0xDD),
        "cyan": RGBColor(0x48, 0xCA, 0xE4),
        "eq_hex_1": "#ECF8F8",
        "eq_hex_2": "#FFD166",
    },
}

EQ_HEX_1 = "#FFFFFF"
EQ_HEX_2 = "#F4C97E"
CURRENT_DECK_OVERRIDES: Dict[str, RGBColor] = {}

def apply_theme_globals(theme_name: str) -> Dict[str, Any]:
    global C_BG_DARK, C_PANEL_PLAY, C_PANEL_STUDY, C_EQ_BG
    global C_WHITE, C_MUTED, C_GOLD, C_GREEN, C_CYAN
    global EQ_HEX_1, EQ_HEX_2, CURRENT_DECK_OVERRIDES
    t = THEMES[theme_name]
    C_BG_DARK = t["bg_dark"]
    C_PANEL_PLAY = t["panel_play"]
    C_PANEL_STUDY = t["panel_study"]
    C_EQ_BG = t["eq_bg"]
    C_WHITE = t["text_main"]
    C_MUTED = t["text_muted"]
    C_GOLD = t["gold"]
    C_GREEN = t["green"]
    C_CYAN = t["cyan"]
    EQ_HEX_1 = t["eq_hex_1"]
    EQ_HEX_2 = t["eq_hex_2"]
    CURRENT_DECK_OVERRIDES = t.get("deck_overrides", {})
    return t

TIER_1_HUBS = {"B:00", "B:01", "B:02", "B:05", "E:01", "N:01", "N:02"}
TIER_2_BRIDGES = {
    "B:03", "B:04", "B:07", "C:01", "C:02", "C:03", "C:05",
    "N:03", "N:04", "N:05", "K:01", "K:02", "K:03", "K:04", "K:05",
}
TIER_3_CAPSTONES = {
    "B:06", "B:08", "B:09", "C:04", "C:06", "E:02", "E:03", "N:06", "K:06", "K:07",
}

C_BG_DARK = RGBColor(0x07, 0x13, 0x24)
C_PANEL_PLAY = RGBColor(0x0B, 0x1F, 0x36)
C_PANEL_STUDY = RGBColor(0x10, 0x1D, 0x30)
C_EQ_BG = RGBColor(0x05, 0x0E, 0x1A)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_MUTED = RGBColor(0xA8, 0xDA, 0xDC)
C_GOLD = RGBColor(0xF4, 0xC9, 0x7E)
C_GREEN = RGBColor(0x80, 0xED, 0x99)
C_CYAN = RGBColor(0x00, 0xB4, 0xD8)

DECK_THEMES: Dict[str, Tuple[str, RGBColor]] = {
    "B": ("Module 1: Base Lifecycle & Fiscal Gate", RGBColor(0x2A, 0x9D, 0x8F)),
    "T": ("Module 1B: Cautionary Trap & Spoiler", RGBColor(0xFF, 0x59, 0x5E)),
    "C": ("Module 2: Climate, Cohesion & Resilience", RGBColor(0x00, 0xB4, 0xD8)),
    "K": ("Module 3: Wayfinder Kaupapa Persona", RGBColor(0xF4, 0xC9, 0x7E)),
    "N": ("Module 4: Nobel & Institutional Archive", RGBColor(0xB5, 0x83, 0x8D)),
    "H": ("Module 5: Orthodoxy Boss Hazard", RGBColor(0xF7, 0x7F, 0x00)),
    "E": ("Module 6: Clean Energy & Grid Endowment", RGBColor(0x80, 0xED, 0x99)),
}


THEMES_DIR = ROOT / "themes"


def find_theme_yaml(theme_name: str) -> Path | None:
    if not THEMES_DIR.exists():
        return None
    candidates = sorted(list(THEMES_DIR.rglob("*.yaml")) + list(THEMES_DIR.rglob("*.yml")))
    aliases = {
        "waka": ["waka_hourua", "waka", "hourua"],
        "hydrofoil": ["hydrofoil", "foils", "up_on_foils"],
        "academic": ["academic", "monograph"],
        "blueprint": ["blueprint", "quantum"],
    }
    for term in aliases.get(theme_name, [theme_name]):
        for f in candidates:
            if term in f"{f.parent.name}/{f.stem}".lower():
                return f
    return None


def apply_lexicon(text: Any, lexicon: List[Tuple[str, str]]) -> Any:
    if not isinstance(text, str) or not text or not lexicon:
        return text
    out = text
    for src, dst in lexicon:
        if src in out:
            out = out.replace(src, dst)
    return out


def apply_theme_yaml_overrides(
    cards: List[Dict[str, Any]], theme_name: str
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    theme_file = find_theme_yaml(theme_name)
    if not theme_file:
        print(f"  [INFO] No theme YAML in themes/ for '{theme_name}'; using base card text.")
        return [dict(c) for c in cards], {}

    raw = yaml.safe_load(theme_file.read_text(encoding="utf-8")) or {}
    print(f"  [THEME YAML] Loaded '{raw.get('theme_name', theme_name)}' from {theme_file.relative_to(ROOT)}")

    lex_dict = raw.get("lexicon_replacements") or {}
    lexicon: List[Tuple[str, str]] = sorted(
        [(str(k), str(v)) for k, v in lex_dict.items() if k and v],
        key=lambda kv: len(kv[0]),
        reverse=True,
    )

    overrides_by_id: Dict[str, Dict[str, Any]] = {}
    card_ov = raw.get("card_overrides") or {}
    if isinstance(card_ov, dict):
        for cid, ov_dict in card_ov.items():
            if isinstance(ov_dict, dict):
                overrides_by_id[str(cid).strip()] = ov_dict

    for k, v in raw.items():
        if isinstance(k, str) and ":" in k and isinstance(v, dict):
            overrides_by_id[k.strip()] = {**overrides_by_id.get(k.strip(), {}), **v}

    print(f"  [THEME YAML] Matched {len(overrides_by_id)} card_overrides + {len(lexicon)} lexicon rules")

    themed_cards: List[Dict[str, Any]] = []
    for base_c in cards:
        cid = str(base_c.get("id", "")).strip()
        ov = overrides_by_id.get(cid, {})
        merged = dict(base_c)

        for k, v in ov.items():
            if v in (None, "", [], {}):
                continue
            merged[k] = v

        if lexicon:
            for str_field in ("name", "type", "gate_or_phase", "cost_or_requirement", "flavor_text", "proof_bridge"):
                if str_field not in ov and str_field in merged:
                    merged[str_field] = apply_lexicon(merged[str_field], lexicon)
            if "effects" not in ov and isinstance(merged.get("effects"), list):
                merged["effects"] = [
                    {
                        "label": apply_lexicon(e.get("label", ""), lexicon),
                        "rule": apply_lexicon(e.get("rule", ""), lexicon),
                    }
                    if isinstance(e, dict) else e
                    for e in merged["effects"]
                ]

        themed_cards.append(merged)

    return themed_cards, raw


def load_joined_cards() -> List[Dict[str, Any]]:
    cards_data = yaml.safe_load(CARDS_YAML.read_text(encoding="utf-8"))
    study_data = yaml.safe_load(STUDY_YAML.read_text(encoding="utf-8"))

    play_list: List[Dict[str, Any]] = cards_data.get("cards", [])
    study_list: List[Dict[str, Any]] = study_data.get("study_cards", [])

    play_by_id = {str(c["id"]): c for c in play_list if "id" in c}
    study_by_id = {str(s["id"]): s for s in study_list if "id" in s}

    all_ids = [str(s["id"]) for s in study_list if "id" in s]
    for c in play_list:
        cid = str(c.get("id", ""))
        if cid and cid not in all_ids:
            all_ids.append(cid)

    return [{**play_by_id.get(cid, {}), **study_by_id.get(cid, {})} for cid in all_ids]


def get_mana_badge(card_id: str) -> str:
    prefix = card_id.split(":")[0]
    if prefix in ("T", "H"):
        return "Hazard / Spoiler (-2M if Countered)"
    if card_id in TIER_1_HUBS:
        return "Tier 1 Hub • Base: 1 Mana (Royalty Engine)"
    if card_id in TIER_2_BRIDGES:
        return "Tier 2 Bridge • Base: 2 Mana"
    if card_id in TIER_3_CAPSTONES:
        return "Tier 3 Capstone • Base: 4-5 Mana (2x/3x)"
    return "Wayfinder Asset • Base: 2 Mana"


def clean_prose_text(text: Any) -> str:
    if not text:
        return ""
    s = str(text)
    for sz in (r"\left", r"\right", r"\middle", r"\big", r"\Big", r"\bigg", r"\Bigg"):
        s = s.replace(sz, "")
    replacements = [
        (r"\times", "×"), (r"\longrightarrow", "⟶"), (r"\rightarrow", "→"), (r"\to", "→"),
        (r"\Longrightarrow", "⟹"), (r"\implies", "⇒"), (r"\iff", "⇔"),
        (r"\ge", "≥"), (r"\le", "≤"), (r"\gg", "≫"), (r"\ll", "≪"), (r"\approx", "≈"),
        (r"\neq", "≠"), (r"\pm", "±"), (r"\cdot", "·"), (r"\partial", "∂"),
        (r"\Delta", "Δ"), (r"\Sigma", "Σ"), (r"\Gamma", "Γ"), (r"\mu^\star", "μ*"),
        (r"\mu", "μ"), (r"\pi", "π"), (r"\tau_a", "τ_a"), (r"\tau_k", "τ_k"),
        (r"\tau_y", "τ_y"), (r"\tau_c", "τ_c"), (r"\tau", "τ"), (r"\sigma", "σ"),
        (r"\phi_1", "φ₁"), (r"\phi_2", "φ₂"), (r"\phi", "φ"), (r"\gamma", "γ"),
        (r"\kappa", "κ"), (r"\omega", "ω"), (r"\rho", "ρ"), (r"\delta", "δ"),
        (r"\epsilon", "ε"), (r"\theta", "θ"), (r"\alpha", "α"), (r"\beta", "β"),
        (r"\psi", "ψ"), (r"\ell", "l"), (r"\star", "*"), (r"\%", "%"),
        (r"\infty", "∞"), (r"\int", "∫"), (r"\sum", "∑"), (r"\prod", "∏"),
        (r"\in", "∈"), (r"\forall", "∀"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathcal\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathbb\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathbf\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\bar\{([^}]*)\}", r"\1̄", s)
    s = s.replace("$$", "").replace("$", "")
    return s.strip()


def extract_braced(s: str, start_idx: int) -> Tuple[str, int]:
    depth = 0
    for i in range(start_idx, len(s)):
        if s[i] == "{" and (i == 0 or s[i - 1] != "\\"):
            depth += 1
        elif s[i] == "}" and (i == 0 or s[i - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return s[start_idx + 1 : i], i + 1
    return s[start_idx + 1 :], len(s)


def replace_underbrace_balanced(s: str) -> str:
    token = r"\underbrace"
    while token in s:
        idx = s.find(token)
        i = idx + len(token)
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s) or s[i] != "{":
            s = s[:idx] + s[idx + len(token) :]
            continue
        expr, next_i = extract_braced(s, i)
        while next_i < len(s) and s[next_i].isspace():
            next_i += 1
        if next_i < len(s) and s[next_i] == "_":
            next_i += 1
            while next_i < len(s) and s[next_i].isspace():
                next_i += 1
            if next_i < len(s) and s[next_i] == "{":
                lbl, end_i = extract_braced(s, next_i)
                s = s[:idx] + f"\\left[{expr}\\right]_{{{lbl}}}" + s[end_i:]
                continue
        s = s[:idx] + f"\\left[{expr}\\right]" + s[next_i:]
    return s


def _replace_text_macros(s: str) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        inner = inner.replace(r"\&", "+").replace("&", "+")
        inner = inner.replace("%", r"\%").replace("–", "-").replace("—", "-")
        inner = inner.replace(" ", r"\ ")
        return r"\mathrm{" + inner + "}"

    return re.sub(r"\\(?:text|textbf|operatorname)\{([^{}]*)\}", repl, s)


def _replace_substack(s: str) -> str:
    pattern = re.compile(r"\\substack\{([^{}]*)\}")
    return pattern.sub(lambda m: m.group(1).replace(r"\\", ", "), s)


def to_mathtext_lines(latex_str: str) -> List[str]:
    s = " ".join(latex_str.strip().strip("$").splitlines()).strip()
    parts: List[str] = [s]
    if len(s) > 115:
        if r"\qquad" in s:
            parts = [p.strip() for p in s.split(r"\qquad", 1)]
        elif r"\quad" in s:
            parts = [p.strip() for p in s.split(r"\quad", 1)]
        elif r"\Longrightarrow" in s and len(s) > 155:
            idx = s.find(r"\Longrightarrow")
            parts = [s[:idx].strip(), r"\Longrightarrow " + s[idx + len(r"\Longrightarrow") :].strip()]

    cleaned_lines: List[str] = []
    for p in parts:
        line = p
        line = re.sub(
            r"\\xrightarrow\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
            lambda m: f"\\overset{{{m.group(1)}}}{{\\longrightarrow}}",
            line,
        )
        line = re.sub(
            r"\\stackrel\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}",
            lambda m: f"\\overset{{{m.group(1)}}}{{{m.group(2)}}}",
            line,
        )
        line = replace_underbrace_balanced(line)
        line = _replace_substack(line)
        for _ in range(3):
            line = _replace_text_macros(line)

        line = re.sub(r"\\mathbb\{([A-Z])\}", lambda m: f"\\mathbf{{{m.group(1)}}}", line)
        line = line.replace(r"\middle|", r"\,|\,")
        line = line.replace(r"\implies", r"\Rightarrow").replace(r"\iff", r"\Leftrightarrow")
        line = re.sub(r"\\le(?![a-zA-Z])", lambda _: r"\leq", line)
        line = re.sub(r"\\ge(?![a-zA-Z])", lambda _: r"\geq", line)
        line = re.sub(r"\\ne(?![a-zA-Z])", lambda _: r"\neq", line)
        line = line.replace(r"\land", r"\wedge").replace(r"\lor", r"\vee")
        line = line.replace(r"\big", "").replace(r"\Big", "").replace(r"\bigg", "").replace(r"\Bigg", "")
        line = line.replace(r"\qquad", r"\ \ \ ").replace(r"\quad", r"\ \ ")
        line = line.replace("–", "-").replace("—", "-")

        if len(re.findall(r"\\left\b", line)) != len(re.findall(r"\\right\b", line)):
            line = re.sub(r"\\left\b", "", line)
            line = re.sub(r"\\right\b", "", line)

        cleaned_lines.append(line.strip())

    return [ln for ln in cleaned_lines if ln]


def render_equation_png(latex_str: str, cid: str = "") -> io.BytesIO:
    lines = to_mathtext_lines(latex_str)
    max_len = max((len(ln) for ln in lines), default=50)

    if len(lines) == 1:
        fontsize = 28 if max_len < 80 else (24 if max_len < 115 else (20.5 if max_len < 150 else 17.5))
    else:
        fontsize = 23.5 if max_len < 100 else (20.0 if max_len < 135 else 17.0)

    fig = plt.figure(figsize=(12.4, 1.85), dpi=360)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.patch.set_alpha(0.0)

    if len(lines) == 1:
        ax.text(0.5, 0.5, f"${lines[0]}$", color=EQ_HEX_1, fontsize=fontsize, ha="center", va="center")
    else:
        ax.text(0.5, 0.74, f"${lines[0]}$", color=EQ_HEX_1, fontsize=fontsize, ha="center", va="center")
        ax.text(0.5, 0.24, f"${lines[1]}$", color=EQ_HEX_2, fontsize=fontsize - 0.5, ha="center", va="center")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=360, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf


def add_rounded_box(
    slide: Any, left: float, top: float, width: float, height: float,
    fill_rgb: RGBColor, line_rgb: RGBColor, line_pt: float = 1.5
) -> Any:
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.adjustments[0] = 0.02
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    shape.line.color.rgb = line_rgb
    shape.line.width = Pt(line_pt)
    return shape


def add_para(
    tf: Any, text: str, size_pt: float, color: RGBColor,
    bold: bool = False, italic: bool = False, space_after: float = 3.0
) -> Any:
    p = tf.paragraphs[0] if (len(tf.paragraphs) == 1 and tf.paragraphs[0].text == "") else tf.add_paragraph()
    p.text = str(text)
    p.font.size = Pt(size_pt)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = "Arial"
    p.space_after = Pt(space_after)
    return p


def build_slide_base(prs: Presentation) -> Any:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG_DARK
    return slide


MASTER_EQ = (
    r"\mathcal{W}(\mu^\star) = \int_{\mathcal{S}} V_1(s)\,d\mu^\star(s) \xrightarrow{\text{SS0}\to\text{SS2}} +20.49\%\text{ CE Welfare}"
    r"\qquad"
    r"\Sigma_{\text{Aotearoa}} = \left(\sum_{i=1}^{P}\mathcal{M}_i + \sum_{i=1}^{P}\mathcal{W}_i\right)\times\Gamma_{\text{Regime}} \;\; (\bar{\Sigma} \ge 135\text{ pts})"
)


def populate_title_slide(prs: Presentation, total_slides: int) -> None:
    slide = build_slide_base(prs)

    hdr = add_rounded_box(slide, 0.25, 0.18, 12.833, 0.88, C_PANEL_PLAY, C_GOLD, 2.0)
    tf = hdr.text_frame
    tf.word_wrap = True
    p1 = add_para(tf, f"SLIDE 01 / {total_slides:02d}  •  BEYOND THE MAGIC MONEY TREE — FOILS & FOUNDERS: THE AOTEAROA STUDY DECK", 14.5, C_GOLD, bold=True, space_after=2)
    p1.alignment = PP_ALIGN.CENTER
    p2 = add_para(tf, 'Rule Zero (B:00 — The Rawlsian D20 Test): "Not all lives are easy, but none should be impossible."', 11.5, C_MUTED, italic=True, space_after=0)
    p2.alignment = PP_ALIGN.CENTER

    left_box = add_rounded_box(slide, 0.25, 1.14, 6.32, 3.82, C_PANEL_PLAY, C_CYAN, 2.0)
    ltf = left_box.text_frame
    ltf.word_wrap = True
    ltf.vertical_anchor = MSO_ANCHOR.TOP
    add_para(ltf, "LEFT VERTICAL PANEL • TABLETOP GAMEPLAY ARCHITECTURE", 10.5, C_CYAN, bold=True, space_after=5)
    add_para(ltf, "⛵ Hull A — Up on Foils (Systems & Hydrofoil Engineering):", 10.5, C_GOLD, bold=True, space_after=2)
    add_para(ltf, "Lift Aotearoa from high-drag SS0 Displacement Mode (81.0 Cohesion, 22%-30% child hardship corner, approaching 200% Debt/GDP) onto SS1 (2x Mana) and SS2 Hydrofoils (3x Mana, 126.0 Cohesion, 18.5% PAYE, Super @ 65) by interlocking 3 Subsystems: 1. Front Foil (B:01+B:02), 2. Wing-Sail (B:05+B:03+E:02), and 3. Rear T-Foil (B:07+B:06).", 9.5, C_WHITE, space_after=6)
    add_para(ltf, "🛶 Hull B — Te Waka Hourua (Double-Hulled Voyaging & Mana):", 10.5, C_GOLD, bold=True, space_after=2)
    add_para(ltf, "Steward multi-generational characters across Being (Tamariki, 0-17), Becoming (Pakeke, 18-62), and Crossing Over (Kaumātua, 63-89 → Rebirth at J=0 via the Rawlsian D20). Expose cards to The River (+1 Generosity), collect persistent Variant B Royalties, and stake Contingent Mana at risk.", 9.5, C_WHITE, space_after=6)
    add_para(ltf, "🏆 Three-Pillar Scrabble Scoring & Dual Ruleset:", 10.5, C_GREEN, bold=True, space_after=2)
    add_para(ltf, "Compete for 1) Mana Laureate (Toa Takitini) and 2) Wealth Laureate (Pou Rawa) while maximizing 3) Combined National Score (Σ_Aotearoa) and out-sailing Finland (88.0 → 107.2) in Abundance Mode or Feral Spoiler Mode.", 9.5, C_WHITE, space_after=0)

    right_box = add_rounded_box(slide, 6.76, 1.14, 6.32, 3.82, C_PANEL_STUDY, C_GOLD, 2.0)
    rtf = right_box.text_frame
    rtf.word_wrap = True
    rtf.vertical_anchor = MSO_ANCHOR.TOP
    add_para(rtf, "RIGHT VERTICAL PANEL • EMPIRICAL & OLG MODEL ARCHITECTURE", 10.5, C_GOLD, bold=True, space_after=5)
    add_para(rtf, "🔬 8-PType × 4-Region General Equilibrium GPU Engine:", 10.5, C_CYAN, bold=True, space_after=2)
    add_para(rtf, "Every card in this deck compiles a formal theorem and calibrated parameter from the companion IGWelfare MATLAB/Python codebase (NZ_4Region_Master.m, PolicyExperiment_LeeSeshadri_4Region.m, QEA_2026.m).", 9.5, C_WHITE, space_after=6)
    add_para(rtf, "📚 Core Empirical Anchors Across the Cards:", 10.5, C_GREEN, bold=True, space_after=3)
    add_para(rtf, "• Dunedin Study (Poulton et al. 2015) & GUiNZ (Morton et al. 2023): 22% (d20: 1-4) to 30% (d20: 1-6) early subsistence corner & 80/20 concentration of $50.5B/yr fiscal drag.", 9.2, C_GOLD, space_after=3)
    add_para(rtf, "• Cunha, Heckman, & Schennach (2010) & Lee & Seshadri (2019): Multi-stage CES dynamic complementarity (φ₁ = -0.50) proving 6.8:1 ROI on Gate 1-2 vs. late remediation collapse.", 9.2, C_GOLD, space_after=3)
    add_para(rtf, "• Guvenen et al. (2023) & Murphy, Shleifer, & Vishny (1991): Use-It-Or-Lose-It wealth/estate tax shift rotating capital from passive land (z_l) to active builders (z_h, 20:01-20:19).", 9.2, C_GOLD, space_after=3)
    add_para(rtf, "• Williamson (2009), Ostrom (2010), & Romer (1990): Polycentric governance, ACC Year-5 actuarial breakeven (3.84x), and non-rival knowledge spillovers.", 9.2, C_GOLD, space_after=0)

    eq_box = add_rounded_box(slide, 0.25, 5.04, 12.833, 2.28, C_EQ_BG, C_GOLD, 2.2)
    etf = eq_box.text_frame
    etf.word_wrap = True
    etf.vertical_anchor = MSO_ANCHOR.TOP
    add_para(etf, f"MASTER THREE-PILLAR SCRABBLE & RAWLSIAN SOCIAL WELFARE OBJECTIVE FUNCTION  (Slide 1 of {total_slides})", 9.5, C_GOLD, bold=True, space_after=0)

    png_buf = render_equation_png(MASTER_EQ, cid="SLIDE_01")
    slide.shapes.add_picture(png_buf, Inches(0.42), Inches(5.34), width=Inches(12.48))


def populate_card_slide(prs: Presentation, card: Dict[str, Any], slide_idx: int, total_slides: int) -> None:
    cid = str(card.get("id", "X:00"))
    prefix = cid.split(":")[0]
    deck_name, accent_rgb = DECK_THEMES.get(prefix, DECK_THEMES["B"])
    accent_rgb = CURRENT_DECK_OVERRIDES.get(prefix, accent_rgb)

    slide = build_slide_base(prs)

    name = clean_prose_text(card.get("name") or card.get("equation_title") or cid)
    card_type = clean_prose_text(card.get("type", ""))
    gate_or_phase = clean_prose_text(card.get("gate_or_phase", ""))
    cost_or_req = clean_prose_text(card.get("cost_or_requirement", ""))
    synergy_links = ", ".join(str(x) for x in (card.get("synergy_links") or [])) or "None"
    effects_list: List[Dict[str, Any]] = card.get("effects") or []
    flavor_text = clean_prose_text(card.get("flavor_text", ""))
    empirical_anchor = clean_prose_text(card.get("empirical_anchor", ""))
    mana_info = get_mana_badge(cid)

    monograph_ref = clean_prose_text(card.get("monograph_ref", ""))
    equation_title = clean_prose_text(card.get("equation_title", ""))
    latex_eq = str(card.get("latex_equation", "")).strip()
    parameters = clean_prose_text(card.get("parameters", ""))
    proof_bridge = clean_prose_text(card.get("proof_bridge", ""))
    citations: List[str] = card.get("citations") or []

    # 1. TOP HEADER BAR
    hdr = add_rounded_box(slide, 0.25, 0.16, 12.833, 0.90, C_PANEL_PLAY, accent_rgb, 2.0)
    htf = hdr.text_frame
    htf.word_wrap = True
    p_top = add_para(htf, f"[{cid}]  {name}   —   {deck_name.upper()}", 13.0, C_WHITE, bold=True, space_after=2)
    p_top.alignment = PP_ALIGN.LEFT
    p_sub = add_para(htf, f"{card_type}  •  Phase: {gate_or_phase}  •  Cost/Req: {cost_or_req}  •  {mana_info}", 9.5, C_GOLD, italic=True, space_after=0)
    p_sub.alignment = PP_ALIGN.LEFT

    # 2. LEFT VERTICAL PANEL: PLAY TEXT
    left_box = add_rounded_box(slide, 0.25, 1.14, 6.32, 3.82, C_PANEL_PLAY, accent_rgb, 1.8)
    ltf = left_box.text_frame
    ltf.word_wrap = True
    ltf.vertical_anchor = MSO_ANCHOR.TOP

    add_para(ltf, "PLAY SIDE (FRONT) • RULES, EFFECTS, SYNERGIES & FLAVOR", 9.5, accent_rgb, bold=True, space_after=4)

    eff_font = 8.4 if len(effects_list) >= 4 else (9.0 if len(effects_list) == 3 else 9.4)
    for eff in effects_list:
        lbl = clean_prose_text(eff.get("label", "Effect"))
        rule = clean_prose_text(eff.get("rule", ""))
        add_para(ltf, f"▸ {lbl}:", eff_font + 0.3, C_CYAN, bold=True, space_after=0.5)
        add_para(ltf, f"   {rule}", eff_font, C_WHITE, space_after=3.0)

    if flavor_text:
        add_para(ltf, f'💬 "{flavor_text}"', 8.8, C_GOLD, italic=True, space_after=3.5)

    add_para(ltf, f"🔗 River Synergy Links: {synergy_links}", 9.0, C_GREEN, bold=True, space_after=0)

    # 3. RIGHT VERTICAL PANEL: STUDY TEXT
    right_box = add_rounded_box(slide, 6.76, 1.14, 6.32, 3.82, C_PANEL_STUDY, C_GOLD, 1.8)
    rtf = right_box.text_frame
    rtf.word_wrap = True
    rtf.vertical_anchor = MSO_ANCHOR.TOP

    add_para(rtf, "STUDY SIDE (FOLD-OVER BACK) • PARAMETERS, PROOF BRIDGE & CITATIONS", 9.5, C_GOLD, bold=True, space_after=4)
    if equation_title:
        add_para(rtf, f"📐 Formal Operator: {equation_title}", 9.6, C_CYAN, bold=True, space_after=3.5)
    if parameters:
        add_para(rtf, "📊 Calibrated OLG Parameters & Metrics:", 9.4, C_GOLD, bold=True, space_after=1)
        add_para(rtf, parameters, 8.8, C_WHITE, space_after=4)
    if proof_bridge:
        add_para(rtf, "🌉 Theorem-to-Tabletop Proof Bridge ('Why the Rule Works'):", 9.4, C_GREEN, bold=True, space_after=1)
        add_para(rtf, proof_bridge, 8.8, C_WHITE, space_after=4)
    if citations:
        add_para(rtf, "📚 Primary Academic & Empirical Citations:", 9.4, C_GOLD, bold=True, space_after=1)
        for c in citations[:4]:
            add_para(rtf, f"• {clean_prose_text(c)}", 8.4, C_WHITE, space_after=2)
    if empirical_anchor:
        add_para(rtf, f"🏛️ Empirical Anchor: {empirical_anchor}", 8.4, C_MUTED, italic=True, space_after=2)
    if monograph_ref:
        add_para(rtf, f"💻 Monograph & Code Hook: {monograph_ref}", 8.5, C_CYAN, bold=True, space_after=0)

    # 4. FULL-WIDTH BOTTOM EQUATION STAGE
    eq_box = add_rounded_box(slide, 0.25, 5.04, 12.833, 2.28, C_EQ_BG, C_GOLD, 2.2)
    etf = eq_box.text_frame
    etf.word_wrap = True
    etf.vertical_anchor = MSO_ANCHOR.TOP
    add_para(etf, f"MATHEMATICAL SPECIFICATION — {cid}: {equation_title}   (Slide {slide_idx} of {total_slides})", 9.0, C_GOLD, bold=True, space_after=0)

    if latex_eq:
        png_buf = render_equation_png(latex_eq, cid=cid)
        slide.shapes.add_picture(png_buf, Inches(0.42), Inches(5.34), width=Inches(12.48))

    notes_tf = slide.notes_slide.notes_text_frame
    notes_tf.text = (
        f"[{cid}] {name} — {equation_title}\n"
        f"Monograph Ref: {monograph_ref}\n"
        f"Parameters: {parameters}\n"
        f"Raw LaTeX Equation:\n$$\n{latex_eq}\n$$"
    )


def build_themed_deck(base_cards: List[Dict[str, Any]], theme_name: str) -> Path:
    t = apply_theme_globals(theme_name)
    cards, theme_meta = apply_theme_yaml_overrides(base_cards, theme_name)
    if cards:
        print(f"  [VERIFY {theme_name.upper()}] B:00 Title -> {cards[0].get('name')}")
    total_slides = len(cards) + 1
    out_path = OUT_DIR / f"foils_and_founders_study_slides{t['suffix']}.pptx"

    print(f"[INFO] Rendering '{theme_name}' theme ({t['label']}) -> {out_path.name}...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    populate_title_slide(prs, total_slides)
    for idx, card in enumerate(cards, start=2):
        populate_card_slide(prs, card, idx, total_slides)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"[OK] Saved {len(prs.slides)} slides -> {out_path.relative_to(ROOT)}")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Render themed Foils & Founders Study Decks (.pptx)")
    ap.add_argument(
        "-t", "--theme",
        choices=["hydrofoil", "waka", "academic", "blueprint", "all"],
        default="hydrofoil",
        help="Visual theme to render (default: hydrofoil, or 'all' for all 4 themes)",
    )
    args = ap.parse_args()

    cards = load_joined_cards()
    all_tests = [("SLIDE_01", MASTER_EQ)] + [(str(c["id"]), str(c.get("latex_equation", ""))) for c in cards]
    failures = 0
    for cid, eq in all_tests:
        for ln in to_mathtext_lines(eq):
            try:
                MATH_PARSER.parse(f"${ln}$", dpi=72)
            except Exception as exc:
                failures += 1
                print(f"[FAIL] {cid}: {ln}\n       {exc}")

    print(f"[AUDIT] Verified {len(all_tests)} slide equations -> {failures} failures!")
    if failures > 0:
        raise RuntimeError(f"Aborting: {failures} equation(s) failed mathtext parsing.")

    themes_to_build = ["hydrofoil", "waka", "academic", "blueprint"] if args.theme == "all" else [args.theme]
    for th in themes_to_build:
        build_themed_deck(cards, th)


if __name__ == "__main__":
    main()
