#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — A3 Fold-Over Study Card Renderer
======================================================================
Compiles `decks/study_cards.yaml` + `decks/cards.yaml` into A3 Landscape
(420mm x 297mm) sheets with 5 fold-over cards per sheet (5 columns x 2 rows):
  - Top Row (Back Face): 138mm x 79mm Landscape (rotated -90deg in the 79x138mm
    top slot) featuring MathJax 3 SVG equations, calibrated parameters, proof
    bridge, peer-reviewed citations, and right-justified Doc 1B/2 reference.
  - Bottom Row (Front Face): Standard 79mm x 138mm Portrait game card.

By default, renders ONLY the cards present in `decks/study_cards.yaml` (padded
to a multiple of 5 with write-in Study Wildcards) so you can preview 1 sheet
immediately. Renders all 80 canonical cards across 16 A3 fold-over study sheets (5 per sheet).

Usage:
  python3 scripts/render_study_cards.py --theme generic --out build/study_generic.html
  python3 scripts/render_study_cards.py --theme waka_hourua --co2-pos bottom-right --out build/study_waka.html
  python3 scripts/render_study_cards.py --theme foils_pakeha --out build/study_foils.html
"""

import argparse
import html
import re
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
from render_math import (
    get_mathjax_svg_fit_css,
    resolve_card_latex,
)


def clip_at_sentence_or_word(text: str, limit: int) -> str:
    """Clips text cleanly at a sentence or word boundary without mid-word cuts."""
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    window = cleaned[:limit]
    dot_pos = max(window.rfind(". "), window.rfind("! "), window.rfind("? "))
    if dot_pos >= int(limit * 0.55):
        return window[: dot_pos + 1]
    word_cut = window.rsplit(" ", 1)[0].rstrip(",;:-")
    return f"{word_cut}…"


def build_front_card_html(
    raw_card: Dict[str, Any],
    palettes: Dict[str, Dict[str, str]],
    card_overrides: Dict[str, Any],
    theme_cfg: Dict[str, Any],
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

    try:
        co2_html = get_co2e_badge_html(card, theme_cfg)
    except TypeError:
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


def get_fold_instruction(orient: str) -> str:
    if orient == "landscape-ccw":
        return "Fold along left crease &bull; Foils &amp; Founders Study Deck"
    if orient == "landscape-cw":
        return "Fold along right crease &bull; Foils &amp; Founders Study Deck"
    return "Fold along bottom crease &bull; Foils &amp; Founders Study Deck"


def build_study_back_html(
    card_front: Dict[str, Any],
    study_entry: Dict[str, Any],
    palettes: Dict[str, Dict[str, str]],
    card_overrides: Dict[str, Any],
    orient: str,
    standalone_copyright: bool,
) -> str:
    """
    Renders the top-row Back Face (79mm x 138mm slot containing a 138mm x 79mm
    rotated Landscape blackboard with MathJax equation, parameters, proof bridge,
    academic citations, and full multi-line Doc 1B/2 program list in the footer).
    """
    cid = str(card_front.get("id", study_entry.get("id", "B:??"))).strip()
    cname = str(card_front.get("name", "Write-In Study Card")).strip()
    if cid in card_overrides and "name" in card_overrides[cid]:
        cname = str(card_overrides[cid]["name"]).strip()

    prefix = cid.split(":")[0] if ":" in cid else "B"
    palette = palettes.get(prefix, palettes["B"])

    border_col = palette.get("border", "#0284c7")
    header_bg = palette.get("header_bg", "#e0f2fe")
    badge_bg = palette.get("badge_bg", "#0369a1")
    badge_txt = palette.get("badge_text", "#ffffff")

    mono_raw = str(
        study_entry.get("vfi_module") or study_entry.get("monograph_ref") or "Docs 2A/2B • 24-File GPU Solver"
    ).strip()
    mono_ref = html.escape(mono_raw)

    eq_title = html.escape(str(
        study_entry.get("economic_concept") or study_entry.get("equation_title") or "General-Equilibrium Specification"
    ))
    latex_raw = resolve_card_latex(study_entry, cid)
    eq_multiline_cls = " sb-eq-2line" if r"\\" in latex_raw else ""

    raw_params = study_entry.get("key_parameters") or study_entry.get("parameters") or ""
    if isinstance(raw_params, list):
        params_plain = " • ".join(str(x) for x in raw_params)
        params_txt = " &bull; ".join(html.escape(str(x)) for x in raw_params)
    else:
        params_plain = str(raw_params).strip()
        params_txt = html.escape(params_plain)

    bridge_raw = str(study_entry.get("tabletop_bridge") or study_entry.get("proof_bridge") or "").strip()
    ev_raw = str(study_entry.get("empirical_evidence", "")).strip()
    citations = study_entry.get("references") or study_entry.get("citations") or []
    cites_plain_len = sum(len(str(c)) for c in citations)

    # Check total text pressure before deciding whether to append Evidence or ditch fold instructions
    base_char_load = len(params_plain) + len(bridge_raw) + cites_plain_len + len(mono_raw)
    is_overfull_footer = len(mono_raw) > 54
    is_dense_card = base_char_load > 520 or (is_overfull_footer and base_char_load > 430)

    bridge_txt = html.escape(bridge_raw)
    if ev_raw and len(bridge_raw) < 165 and not is_dense_card:
        ev_budget = max(90, 320 - len(bridge_raw))
        ev_clean = html.escape(clip_at_sentence_or_word(ev_raw, ev_budget))
        bridge_txt = f"{bridge_txt} <br/><em>Evidence:</em> {ev_clean}"

    cites_html = "".join(
        f"<li>{html.escape(str(c))}</li>" for c in citations
    )

    rot_class = "rot-ccw" if orient == "landscape-ccw" else (
        "rot-cw" if orient == "landscape-cw" else "rot-180"
    )
    dense_cls = " sb-dense" if is_dense_card else ""

    # Ditch folding instructions on cards with over-full program lists or dense text!
    omit_fold = is_overfull_footer or is_dense_card
    if omit_fold:
        fold_span = (
            f'<span class="sb-fold-note">{COPYRIGHT_CARD_HTML}</span>'
            if standalone_copyright
            else ""
        )
        footer_cls = "sb-footer sb-footer-full"
    else:
        fold_txt = get_fold_instruction(orient)
        if standalone_copyright:
            fold_txt = f"{fold_txt} &bull; {COPYRIGHT_CARD_HTML}"
        fold_span = f'<span class="sb-fold-note">{fold_txt}</span>'
        footer_cls = "sb-footer"

    return f"""
    <div class="study-back-slot" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <div class="study-landscape-canvas {rot_class}{dense_cls}">
        <header class="sb-header">
          <span class="pdd-badge">{html.escape(cid)}</span>
          <span class="sb-card-name">{html.escape(cname)}</span>
        </header>

        <div class="sb-eq-frame">
          <div class="sb-eq-title">{eq_title}</div>
          <div class="sb-eq-math{eq_multiline_cls}">\\[ {latex_raw} \\]</div>
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

        <footer class="{footer_cls}">
          {fold_span}
          <span class="sb-mono-ref">📐 {mono_ref}</span>
        </footer>
      </div>
    </div>
    """


def build_wildcard_study_back_html(
    prefix: str,
    palette: Dict[str, str],
    orient: str,
    standalone_copyright: bool,
) -> str:
    border_col = palette.get("border", "#334155")
    header_bg = palette.get("header_bg", "#f1f5f9")
    badge_bg = palette.get("badge_bg", "#1e293b")
    badge_txt = palette.get("badge_text", "#ffffff")
    rot_class = "rot-ccw" if orient == "landscape-ccw" else (
        "rot-cw" if orient == "landscape-cw" else "rot-180"
    )
    fold_txt = get_fold_instruction(orient)
    if standalone_copyright:
        fold_txt = f"{fold_txt} &bull; {COPYRIGHT_CARD_HTML}"

    return f"""
    <div class="study-back-slot" style="--card-border: {border_col}; --header-bg: {header_bg}; --badge-bg: {badge_bg}; --badge-txt: {badge_txt};">
      <div class="study-landscape-canvas {rot_class}">
        <header class="sb-header">
          <span class="pdd-badge">{html.escape(prefix)}:??</span>
          <span class="sb-card-name">Write-In Study Card (Track 2 Challenge Mode PR)</span>
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
          <span class="sb-fold-note">{fold_txt}</span>
          <span class="sb-mono-ref">📐 Doc 1B §____ • Doc 2: ____________.m</span>
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
    standalone_copyright: bool,
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

    raw_ids: List[str] = (
        [str(c.get("id", "")).strip() for c in all_front_cards]
        if all_cards
        else [str(s.get("id", "")).strip() for s in study_list]
    )

    full_packs: List[tuple[str, List[str]]] = []
    if study_list and all("a3_study_sheet" in s for s in study_list):
        ordered_ids = [
            str(s["id"]).strip()
            for s in sorted(
                study_list,
                key=lambda x: (int(x.get("a3_study_sheet", 99)), int(x.get("a3_study_slot", 99))),
            )
            if str(s["id"]).strip() in set(raw_ids)
        ]
        for sh_idx in range(0, len(ordered_ids), 5):
            chunk = ordered_ids[sh_idx : sh_idx + 5]
            sh_num = (sh_idx // 5) + 1
            full_packs.append((f"Study Sheet {sh_num} ({chunk[0]}&ndash;{chunk[-1]})", chunk))
    else:
        by_prefix: Dict[str, List[str]] = {p: [] for p in DECK_ORDER}
        for cid in raw_ids:
            pfx = cid.split(":")[0] if ":" in cid else "B"
            by_prefix.setdefault(pfx, []).append(cid)
        overflow_ids: List[str] = []
        for pfx in DECK_ORDER:
            cids = by_prefix.get(pfx, [])
            num_full = len(cids) // 5
            for p_idx in range(num_full):
                chunk = cids[p_idx * 5 : (p_idx + 1) * 5]
                full_packs.append((f"Pack {pfx}{p_idx + 1} ({chunk[0]}&ndash;{chunk[-1]})", chunk))
            overflow_ids.extend(cids[num_full * 5 :])
        for ov_idx in range(0, len(overflow_ids), 5):
            chunk = overflow_ids[ov_idx : ov_idx + 5]
            full_packs.append((f"Overflow Pack {(ov_idx // 5) + 1} ({', '.join(chunk)})", chunk))

    total_sheets = len(full_packs)
    sheet_blocks: List[str] = []
    wildcard_counter = 0

    for s_idx, (pack_label, chunk_ids) in enumerate(full_packs):
        batch: List[tuple[str, str]] = []
        for cid in chunk_ids:
            front_card = front_by_id.get(cid, {"id": cid, "name": cid})
            study_entry = study_by_id.get(cid, {"id": cid})
            back_html = build_study_back_html(
                front_card, study_entry, palettes, card_overrides, orient, standalone_copyright
            )
            front_html = build_front_card_html(
                front_card, palettes, card_overrides, theme_cfg, themes_dir, search_order, co2_pos, out_path
            )
            batch.append((back_html, front_html))

        # Pad any partial overflow sheet to 5 cards with Write-In Study Wildcards
        while len(batch) < 5:
            pfx = DECK_ORDER[wildcard_counter % len(DECK_ORDER)]
            wildcard_counter += 1
            pal = palettes.get(pfx, palettes["B"])
            batch.append(
                (
                    build_wildcard_study_back_html(pfx, pal, orient, standalone_copyright),
                    build_wildcard_html(pfx, pal, co2_pos),
                )
            )

        top_row_html = "".join(b[0] for b in batch)
        bottom_row_html = "".join(b[1] for b in batch)
        footer_html = build_sheet_footer_html(
            f"Foils &amp; Founders Study Deck ({html.escape(active_theme_name)}) &mdash; "
            f"A3 Sheet {s_idx + 1} of {total_sheets}: {pack_label}"
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
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      svg: {{
        fontCache: 'global',
        scale: 0.92
      }},
      startup: {{
        pageReady: () => {{
          return MathJax.startup.defaultPageReady().then(() => {{
            document.querySelectorAll('.sb-eq-math').forEach(box => {{
              const svg = box.querySelector('svg');
              if (svg) {{
                svg.style.maxWidth = '100%';
                svg.style.height = 'auto';
              }}
            }});
            // Post-MathJax overflow guard: drop fold instructions first, then compact if needed
            document.querySelectorAll('.study-landscape-canvas').forEach(canvas => {{
              const cites = canvas.querySelector('.sb-citations');
              const isOverflowing = () => (
                canvas.scrollHeight > canvas.clientHeight + 1 ||
                (cites && cites.scrollHeight > cites.clientHeight + 1)
              );
              if (isOverflowing()) {{
                const foldNote = canvas.querySelector('.sb-fold-note');
                const footer = canvas.querySelector('.sb-footer');
                if (foldNote && !foldNote.textContent.includes('©')) {{
                  foldNote.style.display = 'none';
                  if (footer) footer.classList.add('sb-footer-full');
                }}
              }}
              if (isOverflowing()) {{
                canvas.classList.add('sb-dense');
              }}
              if (isOverflowing()) {{
                canvas.classList.add('sb-ultra-dense');
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
    .pillar-badge {{ font-size: 5.3pt; letter-spacing: 0.01em; }}
    .pillar-p1 {{ background: #f3e8ff; color: #581c87; border: 0.3mm solid #d8b4fe; }}
    .pillar-p2 {{ background: #fef3c7; color: #92400e; border: 0.3mm solid #fcd34d; }}
    .pillar-p3 {{ background: #ffe4e6; color: #9f1239; border: 0.3mm solid #fda4af; }}
    .pillar-p4 {{ background: #e0e7ff; color: #3730a3; border: 0.3mm solid #a5b4fc; }}
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
      padding: 2.2mm 3.0mm 1.6mm 3.0mm;
      border-top: 2.2mm solid var(--card-border);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.8mm;
      background: #ffffff;
      box-sizing: border-box;
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
      align-items: center;
      background: var(--header-bg);
      padding: 1.0mm 1.8mm;
      border-radius: 1.1mm;
      border-left: 1.4mm solid var(--card-border);
      gap: 1.8mm;
      flex-shrink: 0;
    }}
    .sb-card-name {{
      font-family: var(--font-heading);
      font-size: 8.3pt;
      font-weight: 800;
      color: #0f172a;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
    }}
    .sb-eq-frame {{
      background: #f8fafc;
      border: 0.35mm solid #94a3b8;
      border-left: 1.2mm solid var(--card-border);
      border-radius: 1.1mm;
      padding: 0.9mm 1.8mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
      flex-shrink: 0;
    }}
    .sb-eq-title {{
      font-family: var(--font-mono);
      font-size: 5.7pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--badge-bg);
      margin-bottom: 0.3mm;
    }}
    .sb-eq-math {{
      font-size: 7.2pt;
      line-height: 1.08;
      text-align: center;
      overflow: hidden;
      padding: 0.2mm 0;
    }}
    .sb-eq-math.sb-eq-2line {{
      font-size: 6.2pt;
    }}
    {get_mathjax_svg_fit_css('.sb-eq-math', '13.5mm')}
    .sb-params {{
      font-family: var(--font-mono);
      font-size: 5.6pt;
      line-height: 1.18;
      background: #eff6ff;
      border: 0.25mm solid #bfdbfe;
      padding: 0.8mm 1.4mm;
      border-radius: 0.8mm;
      color: #1e3a8a;
      flex-shrink: 0;
    }}
    .sb-bridge {{
      font-size: 5.9pt;
      line-height: 1.20;
      color: #0f172a;
      background: #f0fdf4;
      border-left: 1mm solid #16a34a;
      padding: 0.8mm 1.4mm;
      border-radius: 0.8mm;
      flex-shrink: 0;
    }}
    .sb-citations {{
      border-top: 0.25mm solid #cbd5e1;
      padding-top: 0.6mm;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      overflow: hidden;
      min-height: 9mm;
    }}
    .sb-cite-heading {{
      font-family: var(--font-mono);
      font-size: 5.3pt;
      font-weight: 800;
      color: #475569;
      text-transform: uppercase;
      margin-bottom: 0.3mm;
      flex-shrink: 0;
    }}
    .sb-cite-list {{
      list-style: disc;
      padding-left: 3.0mm;
      margin: 0;
      font-size: 5.3pt;
      line-height: 1.16;
      color: #334155;
    }}
    .sb-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 2mm;
      font-family: var(--font-mono);
      border-top: 0.25mm solid #cbd5e1;
      padding-top: 0.5mm;
      flex-shrink: 0;
      min-width: 0;
    }}
    .sb-footer.sb-footer-full {{
      justify-content: flex-end;
    }}
    .sb-fold-note {{
      font-size: 4.9pt;
      color: #64748b;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    /* Allows multi-line wrapping & automatic height expansion for over-full .m program lists! */
    .sb-mono-ref {{
      font-family: var(--font-mono);
      font-size: 5.1pt;
      font-weight: 700;
      line-height: 1.18;
      color: #1e293b;
      background: #f1f5f9;
      padding: 0.3mm 1.3mm;
      border-radius: 0.8mm;
      border: 0.25mm solid #cbd5e1;
      white-space: normal;
      overflow-wrap: anywhere;
      word-break: break-word;
      text-align: right;
      max-width: 100%;
    }}
    .sb-footer.sb-footer-full .sb-mono-ref {{
      width: 100%;
      text-align: left;
    }}

    /* Tier 1 Auto-Compact for dense cards (e.g. K:07) */
    .study-landscape-canvas.sb-dense {{
      padding: 1.8mm 2.6mm 1.3mm 2.6mm;
      gap: 0.55mm;
    }}
    .study-landscape-canvas.sb-dense .sb-eq-frame {{
      padding: 0.7mm 1.5mm;
    }}
    .study-landscape-canvas.sb-dense .sb-eq-math svg {{
      max-height: 11.0mm !important;
    }}
    .study-landscape-canvas.sb-dense .sb-params {{
      font-size: 5.2pt;
      line-height: 1.14;
      padding: 0.65mm 1.2mm;
    }}
    .study-landscape-canvas.sb-dense .sb-bridge {{
      font-size: 5.4pt;
      line-height: 1.14;
      padding: 0.65mm 1.2mm;
    }}
    .study-landscape-canvas.sb-dense .sb-cite-list {{
      font-size: 5.0pt;
      line-height: 1.12;
    }}
    .study-landscape-canvas.sb-dense .sb-mono-ref {{
      font-size: 4.8pt;
      line-height: 1.14;
    }}

    /* Tier 2 Ultra-Dense Safety Net (triggered by JS if MathJax equation + citations still push height) */
    .study-landscape-canvas.sb-ultra-dense .sb-eq-math svg {{
      max-height: 9.2mm !important;
    }}
    .study-landscape-canvas.sb-ultra-dense .sb-params,
    .study-landscape-canvas.sb-ultra-dense .sb-bridge {{
      font-size: 4.9pt;
      line-height: 1.10;
      padding: 0.5mm 1.0mm;
    }}
    .study-landscape-canvas.sb-ultra-dense .sb-cite-list {{
      font-size: 4.75pt;
      line-height: 1.08;
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
        help="Render all 80 cards in cards.yaml instead of only the entries in study_cards.yaml",
    )
    parser.add_argument(
        "--standalone-copyright",
        action="store_true",
        help="Include copyright notice on the study card back as well (for standalone printing)",
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
        args.standalone_copyright,
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