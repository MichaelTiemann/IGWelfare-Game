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

    # 1. Build 5 Lifecycle Gates HTML
    gate_cards_html = []
    for g in gates:
        gid = html.escape(g.get("id", ""))
        gname = html.escape(g.get("name", ""))
        foils_t = html.escape(g.get("foils_title", ""))
        waka_t = html.escape(g.get("waka_title", ""))
        kcards = ", ".join(g.get("key_cards", []))
        ss0_out = html.escape(g.get("ss0_outcome", ""))
        ss2_out = html.escape(g.get("ss2_outcome", ""))
        subtitle = waka_t if theme_id == "waka_hourua" else f"{foils_t} • {waka_t}"

        gate_cards_html.append(f"""
        <div class="gate-box">
          <div class="gate-header">
            <span class="badge-id">{gid}</span>
            <span class="gate-keys">🔗 {html.escape(kcards)}</span>
          </div>
          <div class="gate-title">{gname}</div>
          <div class="gate-subtitle">{subtitle}</div>
          <div class="state-row state-ss0"><strong>🔴 SS0:</strong> {ss0_out}</div>
          <div class="state-row state-ss2"><strong>🟢 SS2:</strong> {ss2_out}</div>
          <div class="meeple-slot">Place Cohort Meeples (TOK:01) Here</div>
        </div>
        """)

    # 2. Build 4 Exits HTML
    exit_rows_html = [
        f"""
        <tr>
          <td><strong>{html.escape(ex.get("name", ""))}</strong></td>
          <td class="cell-ss0">🩸 {html.escape(ex.get("ss0_drain", ""))}</td>
          <td class="cell-ss2">🛡️ {html.escape(ex.get("ss2_target", ""))}</td>
        </tr>
        """
        for ex in exits
    ]

    # 3. Build 4 Obligations HTML
    ob_rows_html = [
        f"""
        <tr>
          <td><strong>{html.escape(ob.get("creditor", ""))}</strong></td>
          <td class="cell-ss0">🔴 {html.escape(ob.get("ss0_breach", ""))}</td>
          <td class="cell-ss2">✨ {html.escape(ob.get("ss2_fulfillment", ""))}</td>
        </tr>
        """
        for ob in obligations
    ]

    # 4. Build 7 Capitals Dashboard HTML
    cap_cards_html = [
        f"""
        <div class="cap-box">
          <div class="cap-top">
            <span class="cap-name">{html.escape(c.get("name", ""))}</span>
            <span class="cap-links">{html.escape(", ".join(c.get("primary_cards", [])))}</span>
          </div>
          <div class="cap-track">
            <div class="cap-step step-ss0"><strong>SS0:</strong> {html.escape(c.get("ss0_baseline", ""))}</div>
            <div class="cap-step step-ss1"><strong>SS1:</strong> {html.escape(c.get("ss1_milestone", ""))}</div>
            <div class="cap-step step-ss2"><strong>SS2:</strong> {html.escape(c.get("ss2_victory", ""))}</div>
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
              <div class="slot-title">GATE 1 TAMARIKI (Ages 0–5)</div>
              <div class="slot-desc">Attach B:01 (NZD 13k In-Kind) + N:02 Readiness to flip 🔴 &rarr; 🟢 &amp; spawn +15.3k Care</div>
              <div class="token-drop">Drop TOK:01 Meeple</div>
            </div>
            <div class="care-slot">
              <div class="slot-title">GATE 2 RANGATAHI (Ages 12–14)</div>
              <div class="slot-desc">Pair Tuakana + Teina (B:02 / C:03) + C:02 Monilukutaito to block Job Shocks &amp; T:05</div>
              <div class="token-drop">Drop Paired TOK:01</div>
            </div>
            <div class="care-slot">
              <div class="slot-title">GATE 3 LAUNCH (Ages 20–35)</div>
              <div class="slot-desc">Seed with NZD 62k+ Youth Grant (B:03) + Cooled Rents (B:05) to block Exit 3 Abroad</div>
              <div class="token-drop">Drop TOK:01 + ⚡ TOK:02</div>
            </div>
          </div>

          <div class="mat-grid-2">
            <div class="ledger-panel">
              <div class="panel-heading">OBLIGATIONS LEDGER (TO WHOM &amp; HOW MUCH)</div>
              <ul class="ledger-list">
                <li><strong>To Mokopuna (0–20):</strong> [ ] Stunted (i_c=0) <em>vs.</em> [ ] Thriving + NZD 62k Seed + Solar</li>
                <li><strong>To Kaumātua (65+):</strong> [ ] H:04 Age-70 Cut <em>vs.</em> [ ] NZ Super at 65 (B:06) + K:06 Wisdom</li>
                <li><strong>To Working Whānau:</strong> [ ] 3.1x Rent / 28% PAYE <em>vs.</em> [ ] Rents -10.5% / 18.5% PAYE</li>
                <li><strong>My Capital Track (B:05):</strong> [ ] Passive Dirt (z_l) <em>vs.</em> [ ] Active Builder (z_h: 19/20 Win!)</li>
              </ul>
            </div>
            <div class="ledger-panel">
              <div class="panel-heading">MANA &amp; PASSING OVER INHERITANCE (END OF TURN)</div>
              <div class="mana-boxes">
                <div class="mana-col mana-bad">🌪️ <strong>Mana Eroded (T:05 / Drag)</strong><br/><span>Track unbuffered Exits 1–4</span></div>
                <div class="mana-col mana-good">✨ <strong>Mana Created (Ako / K:07)</strong><br/><span>Lifts Cohesion 100 &rarr; 126.0</span></div>
              </div>
              <div class="passing-over-box">
                <strong>Passing Over Ritual (Gate 5 &rarr; Next Gen):</strong> Recycle NZD 1.6T Estate Wave (B:05 &rarr; B:03 NZD 62k Seeds), leave paid-off Solar (pv=5, E:02), &amp; pass 🧺 <strong>Ngā Kete Tokens (1.75x Skill Multiplier)</strong> to your rising Mokopuna!
              </div>
            </div>
          </div>
        </div>
        """

    # 6. Build Double-Sided Cut-Out Token Sheet HTML (Bottom of Sheet 2)
    token_strips_html = []
    for t in tokens:
        tid = html.escape(t.get("id", ""))
        tname = html.escape(t.get("name", ""))
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
              <div class="side-desc side-a"><strong>{sa.get('icon','')} Side A (SS0): {html.escape(sa.get('label',''))}</strong> — {html.escape(sa.get('mechanic',''))}</div>
              <div class="side-desc side-b"><strong>{sb.get('icon','')} Side B (SS2): {html.escape(sb.get('label',''))}</strong> — {html.escape(sb.get('mechanic',''))}</div>
            </div>
          </div>
          <div class="punch-strip">{badges_html}</div>
        </div>
        """)

    footer_1 = build_sheet_footer_html(
        f"Foils &amp; Founders ({html.escape(active_theme_name)}) &mdash; A3 Playmat 1 of 2: National Hydrofoil &amp; Te Waka Hourua Board"
    )
    footer_2 = build_sheet_footer_html(
        f"Foils &amp; Founders ({html.escape(active_theme_name)}) &mdash; A3 Playmat 2 of 2: Whānau Ledgers &amp; Double-Sided Tokens"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Foils &amp; Founders — A3 Playmats &amp; Tokens ({html.escape(active_theme_name)})</title>
  <style>
    {base_css}
    .a3-sheet {{
      padding: 8mm 10mm 6mm 10mm;
    }}
    .board-banner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.5px solid var(--accent);
      padding-bottom: 2mm;
      margin-bottom: 2.5mm;
    }}
    .banner-title {{
      font-family: var(--font-heading);
      font-size: 14pt;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: -0.02em;
    }}
    .banner-sub {{ font-size: 8.5pt; color: #475569; font-weight: 600; }}
    .banner-right {{
      font-family: var(--font-mono);
      font-size: 7.5pt;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 1.5mm 3mm;
      border-radius: 1.5mm;
      text-align: right;
    }}
    .section-label {{
      font-family: var(--font-mono);
      font-size: 7.5pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      margin-bottom: 1.2mm;
    }}
    .gates-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 2.5mm;
      margin-bottom: 2.5mm;
    }}
    .gate-box {{
      border: 1.5px solid #94a3b8;
      border-top: 3.5px solid var(--accent);
      border-radius: 2mm;
      padding: 2mm;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .gate-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1mm; }}
    .badge-id {{
      font-family: var(--font-mono);
      font-size: 6.5pt;
      font-weight: 800;
      background: var(--accent);
      color: #ffffff;
      padding: 0.4mm 1.5mm;
      border-radius: 1mm;
    }}
    .gate-keys {{ font-family: var(--font-mono); font-size: 6pt; color: #334155; font-weight: 600; }}
    .gate-title {{ font-family: var(--font-heading); font-size: 8.5pt; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .gate-subtitle {{ font-size: 6.5pt; font-style: italic; color: #0f766e; margin-bottom: 1.2mm; }}
    .state-row {{ font-size: 6.2pt; line-height: 1.22; padding: 1mm 1.2mm; border-radius: 1mm; margin-bottom: 1mm; }}
    .state-ss0 {{ background: #fef2f2; border-left: 2px solid #dc2626; }}
    .state-ss2 {{ background: #f0fdf4; border-left: 2px solid #16a34a; }}
    .meeple-slot {{
      border: 1px dashed #94a3b8;
      background: #ffffff;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 5.8pt;
      color: #64748b;
      padding: 1.2mm;
      border-radius: 1mm;
      margin-top: auto;
    }}
    .mid-split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin-bottom: 2.5mm; }}
    .board-table {{ width: 100%; border-collapse: collapse; font-size: 6.3pt; }}
    .board-table th {{
      background: #1e293b;
      color: #ffffff;
      text-align: left;
      padding: 1.2mm 1.8mm;
      font-family: var(--font-mono);
      font-size: 6.2pt;
    }}
    .board-table td {{ border: 1px solid #cbd5e1; padding: 1.1mm 1.6mm; line-height: 1.2; }}
    .cell-ss0 {{ background: #fff1f2; color: #881337; }}
    .cell-ss2 {{ background: #f0fdf4; color: #14532d; }}
    .capitals-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 2mm; }}
    .cap-box {{
      border: 1.2px solid #cbd5e1;
      border-radius: 1.5mm;
      padding: 1.6mm;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .cap-top {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 1mm; margin-bottom: 1mm; }}
    .cap-name {{ display: block; font-family: var(--font-heading); font-size: 6.8pt; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .cap-links {{ font-family: var(--font-mono); font-size: 5.5pt; color: #0284c7; font-weight: 700; }}
    .cap-step {{ font-size: 5.8pt; line-height: 1.2; padding: 0.8mm 1mm; border-radius: 0.8mm; margin-bottom: 0.8mm; }}
    .step-ss0 {{ background: #f8fafc; border-left: 2px solid #64748b; }}
    .step-ss1 {{ background: #eff6ff; border-left: 2px solid #0284c7; }}
    .step-ss2 {{ background: #ecfdf5; border-left: 2px solid #059669; font-weight: 600; }}
    .mats-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-bottom: 2.5mm; }}
    .player-mat {{ border: 2px solid var(--accent); border-radius: 2.5mm; padding: 2.5mm; background: #f8fafc; }}
    .mat-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 1.5mm;
      margin-bottom: 2mm;
    }}
    .mat-title {{ font-family: var(--font-heading); font-size: 9.5pt; font-weight: 800; color: var(--accent); }}
    .mat-sub {{ font-size: 6.2pt; color: #475569; }}
    .d20-box {{ border: 1.5px solid var(--accent); background: #ffffff; border-radius: 1.5mm; padding: 1mm 2mm; text-align: center; }}
    .d20-label {{ font-family: var(--font-mono); font-size: 5.5pt; font-weight: 700; }}
    .d20-circle {{ font-family: var(--font-mono); font-size: 9pt; font-weight: 800; color: var(--accent); }}
    .d20-sub {{ font-size: 5pt; color: #64748b; }}
    .mat-grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm; margin-bottom: 2mm; }}
    .care-slot {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 1.5mm; padding: 1.5mm; }}
    .slot-title {{ font-family: var(--font-mono); font-size: 6.2pt; font-weight: 800; color: #0f172a; }}
    .slot-desc {{ font-size: 5.6pt; color: #475569; line-height: 1.2; margin: 0.8mm 0; }}
    .token-drop {{
      border: 1px dashed #94a3b8;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 5.5pt;
      padding: 1.5mm;
      border-radius: 1mm;
      color: #64748b;
      background: #f8fafc;
    }}
    .mat-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }}
    .ledger-panel {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 1.5mm; padding: 1.5mm; }}
    .panel-heading {{ font-family: var(--font-mono); font-size: 6pt; font-weight: 800; color: var(--accent); margin-bottom: 1mm; }}
    .ledger-list {{ list-style: none; font-size: 5.7pt; line-height: 1.35; }}
    .mana-boxes {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm; margin-bottom: 1.2mm; font-size: 5.6pt; }}
    .mana-col {{ padding: 1mm; border-radius: 1mm; text-align: center; }}
    .mana-bad {{ background: #fef2f2; border: 1px solid #fca5a5; }}
    .mana-good {{ background: #f0fdf4; border: 1px solid #86efac; }}
    .passing-over-box {{
      font-size: 5.6pt;
      line-height: 1.22;
      background: #f5f3ff;
      border: 1px solid #c4b5fd;
      padding: 1mm 1.2mm;
      border-radius: 1mm;
    }}
    .tokens-container {{ display: flex; flex-direction: column; gap: 1.5mm; }}
    .token-row-card {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border: 1px solid #cbd5e1;
      border-radius: 1.5mm;
      padding: 1.2mm 2mm;
      background: #ffffff;
    }}
    .token-meta {{ flex: 1; padding-right: 3mm; }}
    .token-title {{ font-family: var(--font-heading); font-size: 7.2pt; font-weight: 800; margin-bottom: 0.6mm; }}
    .token-sides {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; font-size: 5.8pt; line-height: 1.2; }}
    .side-a {{ color: #991b1b; }}
    .side-b {{ color: #065f46; }}
    .punch-strip {{ display: flex; gap: 2mm; }}
    .punch-pair {{ display: flex; border: 1.2px dashed #475569; border-radius: 1.5mm; padding: 0.6mm; background: #f8fafc; }}
    .punch-half {{
      width: 15mm;
      height: 12mm;
      border: 1.5px solid #000;
      border-radius: 1mm;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 0 0.4mm;
    }}
    .punch-icon {{ font-size: 8.5pt; line-height: 1; }}
    .punch-tag {{ font-family: var(--font-mono); font-size: 4.8pt; font-weight: 800; margin-top: 0.5mm; }}
    .sheet-footer {{ padding: 1mm 0 0 0; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>

  <!-- ==================== A3 SHEET 1: NATIONAL BOARD ==================== -->
  <section class="a3-sheet">
    <div>
      <header class="board-banner">
        <div>
          <div class="banner-title">FOILS &amp; FOUNDERS: THE AOTEAROA DECK — NATIONAL TABLETOP BOARD</div>
          <div class="banner-sub">{html.escape(sub_banner)}</div>
        </div>
        <div class="banner-right">
          <div><strong>Phase Track:</strong> [ ] SS0 Status Quo &rarr; [ ] SS1 Year-5 Audit (3.84x) &rarr; [ ] SS2 2050 50/50 Harvest</div>
          <div><strong>Victory (B:09 / N:06):</strong> Stunting &le; 1.5% &bull; Cohesion 126.0 &bull; Super @ 65 &bull; PAYE 18.5% (+20.49% CE)</div>
        </div>
      </header>

      <div class="section-label">ZONE A: THE LIFECYCLE RIVER — 5 GATES OF BECOMING &amp; INTERGENERATIONAL CROSSING OVER</div>
      <div class="gates-grid">{''.join(gate_cards_html)}</div>

      <div class="mid-split">
        <div>
          <div class="section-label">ZONE B1: THE 4 FISCAL &amp; DEMOGRAPHIC EXITS (SS0 HULL DRAG VS. SS2 RECOVERY)</div>
          <table class="board-table">
            <thead>
              <tr>
                <th style="width:28%;">Exit / Funnel</th>
                <th style="width:38%;">SS0 Displacement Drain</th>
                <th style="width:34%;">SS1 &rarr; SS2 Foil-Borne Target</th>
              </tr>
            </thead>
            <tbody>{''.join(exit_rows_html)}</tbody>
          </table>
        </div>
        <div>
          <div class="section-label">ZONE B2: NATIONAL OBLIGATIONS LEDGER (TO WHOM &amp; HOW MUCH)</div>
          <table class="board-table">
            <thead>
              <tr>
                <th style="width:28%;">Obligation To Whom</th>
                <th style="width:36%;">SS0 Breach of Compact</th>
                <th style="width:36%;">SS2 Fulfillment of Compact</th>
              </tr>
            </thead>
            <tbody>{''.join(ob_rows_html)}</tbody>
          </table>
        </div>
      </div>

      <div class="section-label">ZONE C: THE SEVEN FORMS OF CAPITAL DASHBOARD (TRACK MARKERS FROM SS0 &rarr; SS1 &rarr; SS2)</div>
      <div class="capitals-grid">{''.join(cap_cards_html)}</div>
    </div>
    {footer_1}
  </section>

  <!-- ============== A3 SHEET 2: PLAYER MATS & CUT-OUT TOKENS ============== -->
  <section class="a3-sheet">
    <div>
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

      <div class="section-label">PART 1: INDIVIDUAL WHĀNAU &amp; WAYFINDER LEDGERS (2 PLAYER MATS PER SHEET)</div>
      <div class="mats-row">
        {build_player_mat(1)}
        {build_player_mat(2)}
      </div>

      <div class="section-label">PART 2: FIVE DOUBLE-SIDED TOKEN TYPES (CUT ALONG DASHED BOXES &amp; FOLD IN HALF: SS0 LIABILITY &harr; SS2 ENDOWMENT)</div>
      <div class="tokens-container">{''.join(token_strips_html)}</div>
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
  
