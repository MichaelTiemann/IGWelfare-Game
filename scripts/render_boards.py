#!/usr/bin/env python3
"""
Foils & Founders: The Aotearoa Deck — A3 Landscape Playmat & Token Renderer
============================================================================
Compiles `decks/boards_and_tokens.yaml` + a visual theme (`generic`, `waka_hourua`,
or `foils_pakeha`) into a 2-Sheet A3 Landscape (420mm x 297mm) HTML/PDF document:
  - Sheet 1: The National Hydrofoil & Te Waka Hourua Board (5 Gates, 4 Exits,
             4 Obligations, and 7 Forms of Capital Dashboard)
  - Sheet 2: Two Player "Whānau & Wayfinder" Mats + Double-Sided Cut-Out Tokens

Usage:
  python3 scripts/render_boards.py --theme generic --out build/boards_generic.html
  python3 scripts/render_boards.py --theme waka_hourua --out build/boards_waka.html
  python3 scripts/render_boards.py --theme foils_pakeha --out build/boards_foils.html
"""

import argparse
import html
from pathlib import Path

from render_common import (
    THEME_ACCENTS,
    build_sheet_footer_html,
    get_base_a3_css,
    load_yaml,
    resolve_theme_config,
)


def fmt(text: str) -> str:
    """Escapes HTML, converts newlines to <br/>, and replaces ASCII '->' with right arrows."""
    return (
        html.escape(str(text))
        .replace("\n", "<br/>")
        .replace(" -&gt; ", " &rarr; ")
        .replace("-&gt;", "&rarr;")
    )


def render_boards_html(board_data: dict, theme_cfg: dict, theme_id: str) -> str:
    tokens = board_data.get("tokens", [])
    gates = board_data.get("lifecycle_gates", [])
    exits = board_data.get("exits_and_drains", [])
    capitals = board_data.get("capital_tracks", [])
    obligations = board_data.get("obligations_matrix", [])

    active_theme_name = theme_cfg.get("theme_name", theme_id)
    typo = theme_cfg.get("typography", {})
    font_heading = typo.get("heading_font", "'Inter', system-ui, sans-serif")
    font_body = typo.get("body_font", "'Inter', system-ui, sans-serif")
    font_mono = typo.get("mono_font", "'JetBrains Mono', monospace")

    accent = THEME_ACCENTS.get(theme_id, "#1e293b")
    base_css = get_base_a3_css(font_heading, font_body, font_mono, accent)

    sub_banner = (
        "Te Waka Hourua — Being, Becoming, & Crossing Over (Ngā Kete o te Wānanga)"
        if theme_id == "waka_hourua"
        else "Coupled Hydrofoil & Te Waka Hourua — 5 Gates, 4 Exits, & 7 Forms of Capital"
    )

    # 1. Build 5 Lifecycle Gates HTML (Full-width colored header pill, no duplicate title)
    gate_cards_html = []
    for g in gates:
        gname = fmt(g.get("name", ""))
        foils_t = fmt(g.get("foils_title", ""))
        waka_t = fmt(g.get("waka_title", ""))
        kcards = ", ".join(g.get("key_cards", []))
        ss0_out = fmt(g.get("ss0_outcome", ""))
        ss2_out = fmt(g.get("ss2_outcome", ""))
        subtitle = waka_t if theme_id == "waka_hourua" else f"{foils_t} &bull; {waka_t}"

        gate_cards_html.append(f"""
        <div class="gate-box">
          <div class="gate-top">
            <div class="gate-pill-bar">
              <span class="gate-pill-title">{gname}</span>
              <span class="gate-pill-keys">🔗 {fmt(kcards)}</span>
            </div>
            <div class="gate-subtitle">{subtitle}</div>
          </div>
          <div class="gate-states">
            <div class="state-row state-ss0"><strong>🔴 SS0:</strong> {ss0_out}</div>
            <div class="state-row state-ss2"><strong>🟢 SS2:</strong> {ss2_out}</div>
          </div>
          <div class="meeple-slot">🎯 Place Cohort Meeples (TOK:01) Here</div>
        </div>
        """)

    # 2. Build 4 Exits HTML (Colored box filling left cell + rich right cells)
    exit_rows_html = []
    for ex in exits:
        ex_name = fmt(ex.get("name", ""))
        ex_sub = fmt(ex.get("subtitle", ""))
        ex_ss0 = fmt(ex.get("ss0_drain", ""))
        ex_ss2 = fmt(ex.get("ss2_target", ""))
        sub_html = f'<span class="pill-sub">{ex_sub}</span>' if ex_sub else ""
        exit_rows_html.append(f"""
        <tr>
          <td class="cell-pill-col">
            <div class="row-pill pill-exit">
              <span class="pill-main">{ex_name}</span>
              {sub_html}
            </div>
          </td>
          <td class="cell-ss0">🩸 {ex_ss0}</td>
          <td class="cell-ss2">🛡️ {ex_ss2}</td>
        </tr>
        """)

    # 3. Build 4 Obligations HTML (Colored box filling left cell + rich right cells)
    ob_rows_html = []
    for ob in obligations:
        cred = fmt(ob.get("creditor", ""))
        ob_sub = fmt(ob.get("subtitle", ""))
        breach = fmt(ob.get("ss0_breach", ""))
        fulfill = fmt(ob.get("ss2_fulfillment", ""))
        sub_html = f'<span class="pill-sub">{ob_sub}</span>' if ob_sub else ""
        ob_rows_html.append(f"""
        <tr>
          <td class="cell-pill-col">
            <div class="row-pill pill-ob">
              <span class="pill-main">{cred}</span>
              {sub_html}
            </div>
          </td>
          <td class="cell-ss0">🔴 {breach}</td>
          <td class="cell-ss2">✨ {fulfill}</td>
        </tr>
        """)

    # 4. Build 7 Capitals Dashboard HTML
    cap_cards_html = [
        f"""
        <div class="cap-box">
          <div class="cap-top">
            <span class="cap-name">{fmt(c.get("name", ""))}</span>
            <span class="cap-links">🔗 {fmt(", ".join(c.get("primary_cards", [])))}</span>
          </div>
          <div class="cap-track">
            <div class="cap-step step-ss0"><strong>SS0:</strong> {fmt(c.get("ss0_baseline", ""))}</div>
            <div class="cap-step step-ss1"><strong>SS1:</strong> {fmt(c.get("ss1_milestone", ""))}</div>
            <div class="cap-step step-ss2"><strong>SS2:</strong> {fmt(c.get("ss2_victory", ""))}</div>
          </div>
        </div>
        """
        for c in capitals
    ]

    # 5. Build Player Mat Template (Rendered 2x Side-by-Side on Sheet 2)
    def build_player_mat(player_num: int) -> str:
        return f"""
        <div class="player-mat">
          <div class="mat-header">
            <div>
              <div class="mat-title">WHĀNAU &amp; WAYFINDER LEDGER — PLAYER {player_num}</div>
              <div class="mat-sub">Connect Your Macro Persona (K:01–K:06) to Your Rawlsian D20 Birth Cohort (B:00)</div>
            </div>
            <div class="d20-box">
              <div class="d20-label">B:00 D20 ROLL</div>
              <div class="d20-circle">1–20</div>
              <div class="d20-sub">Sub-Roll: 01:XX / 20:XX</div>
            </div>
          </div>

          <div class="mat-grid-3">
            <div class="care-slot">
              <div class="slot-pill">GATE 1 • TAMARIKI (0–5)</div>
              <div class="slot-desc">Attach B:01 (NZD 13k In-Kind) + N:02 Readiness to flip 🔴 &rarr; 🟢 &amp; spawn +15.3k Care</div>
              <div class="token-drop">🎯 Drop TOK:01 Meeple</div>
            </div>
            <div class="care-slot">
              <div class="slot-pill">GATE 2 • RANGATAHI (12–14)</div>
              <div class="slot-desc">Pair Tuakana + Teina (B:02 / C:03) + C:02 Monilukutaito to block Job Shocks &amp; T:05</div>
              <div class="token-drop">🎯 Drop Paired TOK:01</div>
            </div>
            <div class="care-slot">
              <div class="slot-pill">GATE 3 • LAUNCH (20–35)</div>
              <div class="slot-desc">Seed with NZD 62k+ Youth Grant (B:03) + Cooled Rents (B:05) to block Exit 3 Abroad</div>
              <div class="token-drop">🎯 Drop TOK:01 + ⚡ TOK:02</div>
            </div>
          </div>

          <div class="mat-grid-2">
            <div class="ledger-panel">
              <div class="panel-heading">OBLIGATIONS LEDGER (TO WHOM &amp; HOW MUCH)</div>
              <ul class="ledger-list">
                <li><strong>To Mokopuna (0–20):</strong> &#9744; Stunted (i_c=0) <em>vs.</em> &#9744; Thriving + NZD 62k Seed + Solar</li>
                <li><strong>To Kaumātua (65+):</strong> &#9744; H:04 Age-70 Cut <em>vs.</em> &#9744; NZ Super at 65 (B:06) + K:06 Wisdom</li>
                <li><strong>To Working Whānau:</strong> &#9744; 3.1x Rent / 28.2% PAYE <em>vs.</em> &#9744; Rents -10.5% / 18.5% PAYE</li>
                <li><strong>My Capital Track (B:05):</strong> &#9744; Passive Dirt (z_l) <em>vs.</em> &#9744; Active Builder (z_h: 19/20 Win!)</li>
              </ul>
            </div>
            <div class="ledger-panel">
              <div class="panel-heading">MANA &amp; PASSING OVER INHERITANCE (END OF TURN)</div>
              <div class="mana-boxes">
                <div class="mana-col mana-bad">🌪️ <strong>Mana Eroded (T:05 / Drag)</strong><br/><span>Track unbuffered Exits 1–4</span></div>
                <div class="mana-col mana-good">✨ <strong>Mana Created (Ako / K:07)</strong><br/><span>Lifts Cohesion 100.0 &rarr; 126.0</span></div>
              </div>
              <div class="passing-over-box">
                <strong>Passing Over Ritual (Gate 5 &rarr; Next Gen):</strong> Recycle NZD 1.6T Estate Wave (B:05 &rarr; B:03 NZD 62k Seeds), leave paid-off Solar (pv=5, E:02), &amp; pass 🧺 <strong>Ngā Kete Tokens (1.8x Skill Multiplier)</strong> to your rising Mokopuna!
              </div>
            </div>
          </div>
        </div>
        """

    # 6. Build Double-Sided Cut-Out Token Sheet HTML (Bottom of Sheet 2)
    token_strips_html = []
    for t in tokens:
        tid = fmt(t.get("id", ""))
        tname = fmt(t.get("name", ""))
        sa = t.get("side_a_ss0", {})
        sb = t.get("side_b_ss2", {})

        badges_html = "".join(
            f"""
            <div class="punch-pair" title="Cut around dashed box &amp; fold in half for double-sided token">
              <div class="punch-half" style="border-color:{sa.get('color','#dc2626')}; background:#fef2f2;">
                <span class="punch-icon">{sa.get('icon','🔴')}</span>
                <span class="punch-tag">{tid} SS0</span>
              </div>
              <div class="punch-half" style="border-color:{sb.get('color','#16a34a')}; background:#f0fdf4;">
                <span class="punch-icon">{sb.get('icon','🟢')}</span>
                <span class="punch-tag">{tid} SS2</span>
              </div>
            </div>
            """
            for _ in range(3)
        )

        token_strips_html.append(f"""
        <div class="token-row-card">
          <div class="token-meta">
            <div class="token-title"><span class="badge-id">{tid}</span> {tname}</div>
            <div class="token-sides">
              <div class="side-desc side-a"><strong>{sa.get('icon','')} Side A (SS0): {fmt(sa.get('label',''))}</strong> — {fmt(sa.get('mechanic',''))}</div>
              <div class="side-desc side-b"><strong>{sb.get('icon','')} Side B (SS2): {fmt(sb.get('label',''))}</strong> — {fmt(sb.get('mechanic',''))}</div>
            </div>
          </div>
          <div class="punch-strip">{badges_html}</div>
        </div>
        """)

    footer_1 = build_sheet_footer_html(
        f"Foils &amp; Founders ({fmt(active_theme_name)}) &mdash; A3 Playmat 1 of 2: National Hydrofoil &amp; Te Waka Hourua Board"
    )
    footer_2 = build_sheet_footer_html(
        f"Foils &amp; Founders ({fmt(active_theme_name)}) &mdash; A3 Playmat 2 of 2: Whānau Ledgers &amp; Double-Sided Tokens"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Foils &amp; Founders — A3 Playmats &amp; Tokens ({fmt(active_theme_name)})</title>
  <style>
    {base_css}
    .a3-sheet {{
      padding: 6mm 8mm 5mm 8mm;
    }}
    .sheet-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 2.8mm;
      min-height: 0;
    }}
    .zone-block {{
      display: flex;
      flex-direction: column;
      min-height: 0;
    }}
    .zone-grow-gates {{ flex: 1.18; }}
    .zone-grow-mid {{ flex: 1.02; }}
    .zone-grow-caps {{ flex: 1.18; }}
    .zone-grow-mats {{ flex: 1.12; }}
    .zone-grow-tokens {{ flex: 1.22; }}

    /* Top Banner (Single-Line Guaranteed) */
    .board-banner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 4mm;
      border-bottom: 3px solid var(--accent);
      padding-bottom: 1.8mm;
      flex-shrink: 0;
    }}
    .banner-title {{
      font-family: var(--font-heading);
      font-size: 22pt;
      font-weight: 900;
      color: var(--accent);
      letter-spacing: -0.02em;
      white-space: nowrap;
      line-height: 1.15;
    }}
    .banner-sub {{
      font-size: 9.8pt;
      color: #334155;
      font-weight: 700;
      margin-top: 0.4mm;
      white-space: nowrap;
    }}
    .banner-right {{
      font-family: var(--font-mono);
      font-size: 8.2pt;
      line-height: 1.35;
      background: #f1f5f9;
      border: 1.5px solid #94a3b8;
      padding: 1.5mm 3mm;
      border-radius: 2mm;
      text-align: right;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .section-label {{
      font-family: var(--font-mono);
      font-size: 8.8pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      margin-bottom: 1.2mm;
      flex-shrink: 0;
    }}

    /* Zone A: 5 Lifecycle Gates with Full-Width Colored Header Pill */
    .gates-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 2.8mm;
    }}
    .gate-box {{
      border: 1.8px solid #64748b;
      border-radius: 2.5mm;
      padding: 2mm;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .gate-pill-bar {{
      background: var(--accent);
      color: #ffffff;
      padding: 1.6mm 2mm;
      border-radius: 1.6mm;
      display: flex;
      flex-direction: column;
      gap: 0.6mm;
    }}
    .gate-pill-title {{
      font-family: var(--font-heading);
      font-size: 8.8pt;
      font-weight: 900;
      letter-spacing: 0.01em;
      white-space: nowrap;
      line-height: 1.1;
    }}
    .gate-pill-keys {{
      font-family: var(--font-mono);
      font-size: 7.2pt;
      color: #e2e8f0;
      font-weight: 700;
      white-space: nowrap;
    }}
    .gate-subtitle {{
      font-size: 10pt;
      font-style: italic;
      font-weight: 700;
      color: #0f766e;
      margin-top: 1.2mm;
      line-height: 1.2;
    }}
    .gate-states {{
      display: flex;
      flex-direction: column;
      gap: 1.4mm;
      margin: 1.4mm 0;
    }}
    .state-row {{
      font-size: 8pt;
      line-height: 1.25;
      padding: 1.3mm 1.6mm;
      border-radius: 1.2mm;
    }}
    .state-ss0 {{ background: #fef2f2; border-left: 3px solid #dc2626; }}
    .state-ss2 {{ background: #f0fdf4; border-left: 3px solid #16a34a; }}
    /* 2x Taller Meeple Token Drop Lane */
    .meeple-slot {{
      min-height: 12.5mm;
      border: 1.8px dashed #475569;
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 7.8pt;
      font-weight: 800;
      color: #1e293b;
      padding: 2mm;
      border-radius: 1.8mm;
    }}

    /* Zone B: Exits & Obligations Split with Colored Left Box */
    .mid-split {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3.5mm;
    }}
    .mid-col {{
      display: flex;
      flex-direction: column;
    }}
    .board-table {{
      flex: 1;
      width: 100%;
      height: 100%;
      border-collapse: collapse;
      font-size: 8.4pt;
    }}
    .board-table th {{
      background: #1e293b;
      color: #ffffff;
      text-align: left;
      padding: 1.4mm 2mm;
      font-family: var(--font-mono);
      font-size: 8pt;
    }}
    .board-table td {{
      border: 1.2px solid #94a3b8;
      padding: 1.4mm 2mm;
      line-height: 1.24;
      vertical-align: middle;
    }}
    .cell-pill-col {{
      padding: 1mm !important;
      background: #f1f5f9;
      width: 31%;
    }}
    .row-pill {{
      height: 100%;
      min-height: 11.5mm;
      border-radius: 1.5mm;
      padding: 1.4mm 2mm;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .pill-exit {{ background: #991b1b; border-left: 4px solid #dc2626; }}
    .pill-ob {{ background: var(--accent); border-left: 4px solid #0284c7; }}
    .pill-main {{
      font-family: var(--font-heading);
      font-size: 8.2pt;
      font-weight: 900;
      letter-spacing: 0.01em;
      line-height: 1.15;
    }}
    .pill-sub {{
      font-size: 6.8pt;
      color: #e2e8f0;
      font-weight: 600;
      margin-top: 0.3mm;
    }}
    .cell-ss0 {{ background: #fff1f2; color: #881337; width: 35%; }}
    .cell-ss2 {{ background: #f0fdf4; color: #14532d; font-weight: 600; width: 34%; }}

    /* Zone C: 7 Capitals Dashboard */
    .capitals-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 2.4mm;
    }}
    .cap-box {{
      border: 1.5px solid #64748b;
      border-top: 3.5px solid var(--accent);
      border-radius: 2mm;
      padding: 1.8mm;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .cap-top {{
      border-bottom: 1.2px solid #cbd5e1;
      padding-bottom: 1mm;
      margin-bottom: 1mm;
    }}
    .cap-name {{
      display: block;
      font-family: var(--font-heading);
      font-size: 8.6pt;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.15;
      margin-bottom: 0.5mm;
    }}
    .cap-links {{
      font-family: var(--font-mono);
      font-size: 7pt;
      color: #0369a1;
      font-weight: 800;
    }}
    .cap-track {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 1.2mm;
    }}
    .cap-step {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      font-size: 7.5pt;
      line-height: 1.22;
      padding: 1.1mm 1.4mm;
      border-radius: 1.2mm;
    }}
    .step-ss0 {{ background: #f8fafc; border-left: 3px solid #64748b; }}
    .step-ss1 {{ background: #eff6ff; border-left: 3px solid #0284c7; }}
    .step-ss2 {{ background: #ecfdf5; border-left: 3px solid #059669; font-weight: 700; }}

    /* Sheet 2: Player Mats & Tokens */
    .mats-row {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4mm;
    }}
    .player-mat {{
      border: 2.5px solid var(--accent);
      border-radius: 3mm;
      padding: 2.8mm;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 2mm;
    }}
    .mat-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #cbd5e1;
      padding-bottom: 1.5mm;
    }}
    .mat-title {{
      font-family: var(--font-heading);
      font-size: 12pt;
      font-weight: 900;
      color: var(--accent);
    }}
    .mat-sub {{ font-size: 8pt; color: #334155; font-weight: 600; margin-top: 0.3mm; }}
    .d20-box {{
      border: 2px solid var(--accent);
      background: #ffffff;
      border-radius: 2mm;
      padding: 1mm 2.8mm;
      text-align: center;
      flex-shrink: 0;
    }}
    .d20-label {{ font-family: var(--font-mono); font-size: 6.8pt; font-weight: 800; }}
    .d20-circle {{ font-family: var(--font-mono); font-size: 12.5pt; font-weight: 900; color: var(--accent); line-height: 1.1; }}
    .d20-sub {{ font-size: 6.5pt; color: #475569; font-weight: 600; }}
    .mat-grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.2mm;
    }}
    .care-slot {{
      background: #ffffff;
      border: 1.5px solid #94a3b8;
      border-radius: 2mm;
      padding: 1.8mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .slot-pill {{
      background: var(--accent);
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 7.4pt;
      font-weight: 800;
      padding: 1mm 1.5mm;
      border-radius: 1.2mm;
      white-space: nowrap;
    }}
    .slot-desc {{ font-size: 7.4pt; color: #334155; line-height: 1.22; margin: 1mm 0; }}
    /* 2x Taller Token Drop Lane on Player Mat */
    .token-drop {{
      min-height: 11mm;
      border: 1.6px dashed #475569;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 7.4pt;
      font-weight: 800;
      padding: 1.8mm;
      border-radius: 1.5mm;
      color: #1e293b;
      background: #f1f5f9;
    }}
    .mat-grid-2 {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2.2mm;
    }}
    .ledger-panel {{
      background: #ffffff;
      border: 1.5px solid #94a3b8;
      border-radius: 2mm;
      padding: 2mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .panel-heading {{
      font-family: var(--font-mono);
      font-size: 7.8pt;
      font-weight: 800;
      color: var(--accent);
      margin-bottom: 0.8mm;
    }}
    .ledger-list {{
      list-style: none;
      font-size: 7.6pt;
      line-height: 1.45;
    }}
    .mana-boxes {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.8mm;
      font-size: 7.4pt;
      line-height: 1.22;
    }}
    .mana-col {{ padding: 1.4mm; border-radius: 1.5mm; text-align: center; }}
    .mana-bad {{ background: #fef2f2; border: 1.5px solid #fca5a5; }}
    .mana-good {{ background: #f0fdf4; border: 1.5px solid #86efac; }}
    .passing-over-box {{
      font-size: 7.4pt;
      line-height: 1.25;
      background: #f5f3ff;
      border: 1.5px solid #c4b5fd;
      padding: 1.4mm 1.6mm;
      border-radius: 1.5mm;
    }}

    /* Cut-Out Tokens Section */
    .tokens-container {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 1.8mm;
    }}
    .token-row-card {{
      flex: 1;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border: 1.5px solid #94a3b8;
      border-radius: 2mm;
      padding: 1.4mm 2.5mm;
      background: #ffffff;
    }}
    .badge-id {{
      font-family: var(--font-mono);
      font-size: 8pt;
      font-weight: 800;
      background: var(--accent);
      color: #ffffff;
      padding: 0.4mm 1.8mm;
      border-radius: 1.2mm;
      margin-right: 1.5mm;
    }}
    .token-meta {{ flex: 1; padding-right: 4mm; }}
    .token-title {{
      font-family: var(--font-heading);
      font-size: 9.5pt;
      font-weight: 800;
      margin-bottom: 0.8mm;
      color: #0f172a;
    }}
    .token-sides {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3mm;
      font-size: 7.6pt;
      line-height: 1.24;
    }}
    .side-a {{ color: #991b1b; background: #fff1f2; padding: 1mm 1.5mm; border-radius: 1mm; }}
    .side-b {{ color: #065f46; background: #ecfdf5; padding: 1mm 1.5mm; border-radius: 1mm; }}
    .punch-strip {{ display: flex; gap: 2.5mm; flex-shrink: 0; }}
    .punch-pair {{
      display: flex;
      border: 1.6px dashed #334155;
      border-radius: 2mm;
      padding: 0.8mm;
      background: #f8fafc;
    }}
    .punch-half {{
      width: 22mm;
      height: 16.5mm;
      border: 1.8px solid #000;
      border-radius: 1.5mm;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 0 0.5mm;
    }}
    .punch-icon {{ font-size: 12.5pt; line-height: 1; }}
    .punch-tag {{ font-family: var(--font-mono); font-size: 6.8pt; font-weight: 800; margin-top: 0.8mm; }}
    .sheet-footer {{ padding: 1.5mm 0 0 0; border-top: 1.5px solid #cbd5e1; margin-top: 1.5mm; flex-shrink: 0; }}
  </style>
</head>
<body>

  <!-- ==================== A3 SHEET 1: NATIONAL BOARD ==================== -->
  <section class="a3-sheet">
    <div class="sheet-body">
      <header class="board-banner">
        <div>
          <div class="banner-title">FOILS &amp; FOUNDERS: THE AOTEAROA DECK — NATIONAL TABLETOP BOARD</div>
          <div class="banner-sub">{fmt(sub_banner)}</div>
        </div>
        <div class="banner-right">
          <div><strong>Phase Track:</strong> &#9744; SS0 Status Quo &rarr; &#9744; SS1 Year-5 Audit (3.8x) &rarr; &#9744; SS2 2050 50/50 Harvest</div>
          <div><strong>Victory (B:09 / N:06):</strong> Stunting &le; 1.5% &bull; Cohesion 126.0 &bull; Super @ 65 &bull; PAYE 18.5% (+20.5% CE)</div>
        </div>
      </header>

      <div class="zone-block zone-grow-gates">
        <div class="section-label">ZONE A: THE LIFECYCLE RIVER — 5 GATES OF BECOMING &amp; INTERGENERATIONAL CROSSING OVER</div>
        <div class="gates-grid">{''.join(gate_cards_html)}</div>
      </div>

      <div class="zone-block zone-grow-mid">
        <div class="mid-split">
          <div class="mid-col">
            <div class="section-label">ZONE B1: THE 4 FISCAL &amp; DEMOGRAPHIC EXITS (SS0 HULL DRAG VS. SS2 RECOVERY)</div>
            <table class="board-table">
              <thead>
                <tr>
                  <th style="width:31%;">Exit / Funnel</th>
                  <th style="width:35%;">SS0 Displacement Drain</th>
                  <th style="width:34%;">SS1 &rarr; SS2 Foil-Borne Target</th>
                </tr>
              </thead>
              <tbody>{''.join(exit_rows_html)}</tbody>
            </table>
          </div>
          <div class="mid-col">
            <div class="section-label">ZONE B2: NATIONAL OBLIGATIONS LEDGER (TO WHOM &amp; HOW MUCH)</div>
            <table class="board-table">
              <thead>
                <tr>
                  <th style="width:31%;">Obligation To Whom</th>
                  <th style="width:35%;">SS0 Breach of Compact</th>
                  <th style="width:34%;">SS2 Fulfillment of Compact</th>
                </tr>
              </thead>
              <tbody>{''.join(ob_rows_html)}</tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="zone-block zone-grow-caps">
        <div class="section-label">ZONE C: THE SEVEN FORMS OF CAPITAL DASHBOARD (TRACK MARKERS FROM SS0 &rarr; SS1 &rarr; SS2)</div>
        <div class="capitals-grid">{''.join(cap_cards_html)}</div>
      </div>
    </div>
    {footer_1}
  </section>

  <!-- ============== A3 SHEET 2: PLAYER MATS & CUT-OUT TOKENS ============== -->
  <section class="a3-sheet">
    <div class="sheet-body">
      <header class="board-banner">
        <div>
          <div class="banner-title">WHĀNAU &amp; WAYFINDER PLAYER MATS + DOUBLE-SIDED CUT-OUT TOKENS</div>
          <div class="banner-sub">Track Your B:00 Rawlsian Birth Roll, Tamariki in Care, Mana Balance, &amp; Passing Over Inheritance</div>
        </div>
        <div class="banner-right">
          <div><strong>Tabletop Setup:</strong> Print on A3 Cardstock &bull; Cut Player Mats &amp; Fold-Over Tokens Along Dashed Lines</div>
          <div><strong>Full Rules &amp; Sub-Rolls:</strong> rules/boards_and_tokens.md &bull; decks/nat_1.md &bull; decks/nat_20.md</div>
        </div>
      </header>

      <div class="zone-block zone-grow-mats">
        <div class="section-label">PART 1: INDIVIDUAL WHĀNAU &amp; WAYFINDER LEDGERS (2 PLAYER MATS PER SHEET)</div>
        <div class="mats-row">
          {build_player_mat(1)}
          {build_player_mat(2)}
        </div>
      </div>

      <div class="zone-block zone-grow-tokens">
        <div class="section-label">PART 2: FIVE DOUBLE-SIDED TOKEN TYPES (CUT ALONG DASHED BOXES &amp; FOLD IN HALF: SS0 LIABILITY &harr; SS2 ENDOWMENT)</div>
        <div class="tokens-container">{''.join(token_strips_html)}</div>
      </div>
    </div>
    {footer_2}
  </section>

</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Foils & Founders A3 Landscape Playmats and Token Sheets."
    )
    parser.add_argument(
        "--board-yaml",
        type=Path,
        default=Path("decks/boards_and_tokens.yaml"),
        help="Path to boards_and_tokens.yaml (default: decks/boards_and_tokens.yaml)",
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
        "--out",
        type=Path,
        default=Path("build/boards_generic.html"),
        help="Output HTML file path (default: build/boards_generic.html)",
    )
    args = parser.parse_args()

    board_data = load_yaml(args.board_yaml, required=True)
    theme_cfg = resolve_theme_config(args.themes_dir, args.theme)
    html_out = render_boards_html(board_data, theme_cfg, args.theme)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")
    print(
        f"[OK] Rendered 2 A3 Landscape Playmat & Token sheets (theme='{args.theme}') -> {args.out}"
    )


if __name__ == "__main__":
    main()
