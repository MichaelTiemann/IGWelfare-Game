#!/usr/bin/env python3
"""
Foils & Founders: Printable SVG & HTML Board Mat Renderer (Overflow-Fixed)
==========================================================================
Generates a print-ready SVG (900mm x 600mm aspect ratio: 1800x1220 px)
and an HTML preview wrapper in output/ with:
  - Stacked Bay Titles + Maori Subtitles (zero horizontal collision)
  - Strictly bounded Sub-Zone A, B, and C text lines
  - 3-Year/Turn OLG Clock where every turn = 1 NZ Parliamentary Term (no redundant red election boxes)

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "output"


def build_board_svg() -> str:
    width, height = 1800, 1220
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<defs>',
        '  <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '    <stop offset="0%" stop-color="#071324"/>',
        '    <stop offset="50%" stop-color="#0B1D33"/>',
        '    <stop offset="100%" stop-color="#09222C"/>',
        '  </linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#bgGrad)"/>',
        f'<rect x="14" y="14" width="{width-28}" height="{height-28}" rx="16" fill="none" stroke="#D4A359" stroke-width="3"/>',
    ]

    # --- TITLE & RULE ZERO BANNER ---
    svg.append(
        '<text x="900" y="46" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" '
        'font-size="24" font-weight="bold" letter-spacing="1.5">'
        'FOILS &amp; FOUNDERS: THE AOTEAROA DECK — MACRO HYDROFOIL &amp; TE WAKA HOURUA MAT</text>'
    )
    svg.append(
        '<text x="900" y="72" text-anchor="middle" fill="#A8DADC" font-family="Georgia, serif" '
        'font-size="17" font-style="italic">'
        'Rule Zero (B:00 — The Rawlsian D20 Test): "Not all lives are easy, but none should be impossible."</text>'
    )

    # ==========================================================================
    # ZONE 1: THE RAWLSIAN D20 REEF & VIGINTILE COMPASS (y = 86 to 208)
    # ==========================================================================
    svg.append('<rect x="30" y="86" width="1740" height="122" rx="10" fill="#0F2942" stroke="#00B4D8" stroke-width="2"/>')
    svg.append(
        '<text x="45" y="108" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="13.5" font-weight="bold">'
        'ZONE 1: THE RAWLSIAN D20 BIRTH &amp; ENDOGENOUS HAZARD COMPASS (20 WEALTH VIGINTILES)</text>'
    )
    svg.append(
        '<text x="1755" y="108" text-anchor="end" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="12.5">'
        'Cover Red/Amber Reefs by Locking Subsystems 1, 2, &amp; 3 Below ("Make Your Own Luck")</text>'
    )

    # 20 D20 cells: 45 + 20*83 + 19*2 = 45 + 1660 + 38 = 1743 (12px inside x=1770 right border)
    cell_w = 83
    start_x = 45
    for d in range(1, 21):
        cx = start_x + (d - 1) * (cell_w + 2)
        cy = 118
        if d <= 4:
            fill, stroke, label = "#6B111B", "#FF4D4D", "SS0 STUNT"
        elif d <= 6:
            fill, stroke, label = "#521924", "#FF8080", "H:06 DRIFT"
        elif d >= 19:
            fill, stroke, label = "#5C3A08", "#F77F00", "T:02/T:04"
        else:
            fill, stroke, label = "#113F48", "#2A9D8F", "CLEAR"

        svg.append(f'<rect x="{cx}" y="{cy}" width="{cell_w}" height="56" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        svg.append(
            f'<text x="{cx + cell_w/2}" y="{cy + 26}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="19" font-weight="bold">d20: {d}</text>'
        )
        svg.append(
            f'<text x="{cx + cell_w/2}" y="{cy + 46}" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">{label}</text>'
        )

    svg.append(
        '<text x="310" y="194" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
        'BOTTOM REEF (1-6): T:00/T:01/T:05 | Closed by BAY 1 (B:01+B:02)</text>'
    )
    svg.append(
        '<text x="955" y="194" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
        '3-YR TERM AUDIT (1-8): Triggers H:01/H:02 on Unshielded Stakes | Closed by BAY 3 (B:07)</text>'
    )
    svg.append(
        '<text x="1585" y="194" text-anchor="middle" fill="#FFB703" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
        'TOP REEF (19-20): T:02/T:04 | Closed by BAY 2 (B:05)</text>'
    )

    # ==========================================================================
    # ZONE 2: THE THREE INTERLOCKING SUBSYSTEM BAYS (y = 220 to 710)
    # ==========================================================================
    bays = [
        {
            "x": 30,
            "title": "BAY 1: FRONT LIFTING FOIL",
            "maori": "Te Korowai Mokopuna — Early Human Capability",
            "recipe": "RECIPE: B:01 (First 2000 Days) + B:02 (Tuakana-Teina) + 1 Amp (N:01, N:02, C:02, C:03)",
            "judo1": "Play B:01+N:02 (or K:01) vs. T:00/T:01",
            "judo2": "Play C:02 or K:05 vs. T:05 Outrage Mill",
            "lock1": "LOCKED REWARD: Covers D20 Reef 1-6 (No Life Impossible!)",
            "lock2": "+ Awards +5 Legacy Mana Bonus to Enacting Coalition!",
            "color": "#2A9D8F",
        },
        {
            "x": 625,
            "title": "BAY 2: WING-SAIL POWER PLANT",
            "maori": "Te Aka Matua — Capital &amp; Clean Energy Rotation",
            "recipe": "RECIPE: B:05 (Use-It-Or-Lose-It) + B:03 (Youth Grant) + 1 Engine (E:01, E:02, C:05)",
            "judo1": "Play B:05+N:05 (or K:02) vs. T:02/T:04/H:05",
            "judo2": "Play B:03 vs. H:03 Sydney Brain Drain",
            "lock1": "LOCKED REWARD: Covers D20 Reef 19-20 + Ends Brain Drain",
            "lock2": "+ Working Adults Earn +1 Wealth Every Turn!",
            "color": "#00B4D8",
        },
        {
            "x": 1220,
            "title": "BAY 3: REAR T-FOIL STABILIZER",
            "maori": "Nga Kete o te Wananga — Actuarial &amp; Fiscal Governance",
            "recipe": "RECIPE: B:07 (ACC Time-Bend) + B:06 (2050 50/50 Rule) + 1 Proof (N:03, N:04, B:04, B:08)",
            "judo1": "Play B:07+N:03 (or K:03/K:04) vs. H:01 Myopia",
            "judo2": "Play N:01/N:04 vs. H:02 Agency Silos",
            "lock1": "LOCKED REWARD: Cancels H:01 Cash-Myopia Audits Forever",
            "lock2": "+ PAYE Cut to 18.5% (+1W/Turn) &amp; Super @ 65 (K:06)!",
            "color": "#D4A359",
        },
    ]

    for b in bays:
        bx = b["x"]
        bw = 550
        svg.append(f'<rect x="{bx}" y="220" width="{bw}" height="490" rx="12" fill="#0B1F36" stroke="{b["color"]}" stroke-width="3"/>')

        # Stacked Title (y=243) and Maori Subtitle (y=261) -> Zero Horizontal Collision!
        svg.append(
            f'<text x="{bx + 18}" y="243" fill="{b["color"]}" font-family="Helvetica, Arial, sans-serif" font-size="16.5" font-weight="bold">'
            f'{b["title"]}</text>'
        )
        svg.append(
            f'<text x="{bx + 18}" y="259" fill="#F4C97E" font-family="Georgia, serif" font-size="12.5" font-style="italic">'
            f'{b["maori"]}</text>'
        )
        svg.append(
            f'<text x="{bx + 18}" y="276" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="10.8" font-weight="bold">'
            f'{b["recipe"]}</text>'
        )
        svg.append(
            f'<text x="{bx + 18}" y="291" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="10.2">'
            f'Political Drag: [2P: 1.5W] • [3-4P: 2.0W] • [5-6P: 3.0W + 3 Co-Stakers (unless K:07)]</text>'
        )

        # Sub-Zone A: Staking & Incubation (y=292, height=132, width=518)
        svg.append(f'<rect x="{bx+16}" y="300" width="{bw-32}" height="124" rx="8" fill="#102E4A" stroke="#00B4D8" stroke-width="1.5"/>')
        svg.append(
            f'<text x="{bx+26}" y="317" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
            f'SUB-ZONE A: CONTINGENT MANA STAKING (UPRIGHT 0-DEG TOKENS)</text>'
        )
        for slot_i in range(3):
            sx = bx + 30 + slot_i * 166
            svg.append(f'<rect x="{sx}" y="325" width="152" height="89" rx="6" fill="#0A1E32" stroke="#457B9D" stroke-dasharray="5,4"/>')
            svg.append(
                f'<text x="{sx+76}" y="370" text-anchor="middle" fill="#8ECAE6" font-family="Helvetica, Arial, sans-serif" font-size="10.5">'
                f'Card / Upright Mana #{slot_i+1}</text>'
            )

        # Sub-Zone B: 1-Turn Emergency / Jeopardy Box (y=434, height=142, width=518)
        svg.append(
            f'<rect x="{bx+16}" y="434" width="{bw-32}" height="142" rx="8" fill="#3B1018" stroke="#FF4D4D" stroke-width="2" stroke-dasharray="8,5"/>'
        )
        svg.append(
            f'<text x="{bx+26}" y="454" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
            f'SUB-ZONE B: 1-TURN EMERGENCY BOX (TIP MANA 90-DEG SIDEWAYS!)</text>'
        )
        svg.append(
            f'<text x="{bx+26}" y="471" fill="#FFD6D6" font-family="Helvetica, Arial, sans-serif" font-size="10">'
            f'If D20 Reef or Feral Spoiler hits: Place T/H Trap below. Save in 1 Turn or Forfeit Stake!</text>'
        )

        # Left Box: Trap/Boss Slot (x = bx+26, width = 140)
        svg.append(f'<rect x="{bx+26}" y="480" width="140" height="84" rx="6" fill="#24080D" stroke="#FF4D4D"/>')
        svg.append(
            f'<text x="{bx+96}" y="518" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="10.5" font-weight="bold">'
            f'TRAP / BOSS SLOT</text>'
        )
        svg.append(
            f'<text x="{bx+96}" y="536" text-anchor="middle" fill="#FFD6D6" font-family="Helvetica, Arial, sans-serif" font-size="9.5">'
            f'(T:00-T:05 / H:01-H:06)</text>'
        )

        # Right Box: Empirical Shield / Judo Counter Slot (x = bx+176, width = 346)
        svg.append(f'<rect x="{bx+176}" y="480" width="346" height="84" rx="6" fill="#182B3A" stroke="#2A9D8F"/>')
        svg.append(
            f'<text x="{bx+349}" y="498" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="10.5" font-weight="bold">'
            f'EMPIRICAL SHIELD / JUDO COUNTER SLOT</text>'
        )
        svg.append(
            f'<text x="{bx+349}" y="515" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="9.8">'
            f'• {b["judo1"]}</text>'
        )
        svg.append(
            f'<text x="{bx+349}" y="531" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="9.8">'
            f'• {b["judo2"]}</text>'
        )
        svg.append(
            f'<text x="{bx+349}" y="550" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="9.2">'
            f'Feral Backfire: Countering = +1M to Crew &amp; -2M Whakama to Spoiler!</text>'
        )

        # Sub-Zone C: Locked Foil Plinth (y=586, height=110, width=518)
        svg.append(f'<rect x="{bx+16}" y="586" width="{bw-32}" height="110" rx="8" fill="#123524" stroke="#80ED99" stroke-width="2"/>')
        svg.append(
            f'<text x="{bx+26}" y="607" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
            f'SUB-ZONE C: LOCKED HYDROFOIL / KIATO PLINTH (REEF CLEARED!)</text>'
        )
        svg.append(
            f'<text x="{bx+26}" y="627" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="10.8" font-weight="bold">'
            f'{b["lock1"]}</text>'
        )
        svg.append(
            f'<text x="{bx+26}" y="644" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="10.8" font-weight="bold">'
            f'{b["lock2"]}</text>'
        )
        svg.append(
            f'<text x="{bx+26}" y="664" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="10">'
            f'Bystander Forfeit: 0 Mana staked when locked = -2 Mana (SS1) / -3 Mana (SS2)!</text>'
        )
        svg.append(
            f'<text x="{bx+26}" y="682" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="9.8">'
            f'Regime Multipliers: [Any 2 Bays = SS1 (2x Mana!)] • [All 3 Bays + Cap = SS2 (3x Mana!)]</text>'
        )

    # ==========================================================================
    # ZONE 3: THE TEXAS HOLD'EM RIVER & PERSISTENT COMMONS (y = 724 to 968)
    # ==========================================================================
    svg.append('<rect x="30" y="724" width="1740" height="244" rx="12" fill="#0D233A" stroke="#F4C97E" stroke-width="2.5"/>')
    svg.append(
        '<text x="46" y="750" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="15.5" font-weight="bold">'
        'ZONE 3: THE TEXAS HOLD\'EM RIVER — PERSISTENT INSTITUTIONAL INFRASTRUCTURE (VARIANT B / ROMER N:05)</text>'
    )
    svg.append(
        '<text x="1754" y="750" text-anchor="end" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="12.5" font-weight="bold">'
        'Expose Card to River = Collect +1 Generosity (Wealth) Immediately! | Enacted Cards Stay &amp; Earn Royalties</text>'
    )

    r_w = 202
    for r_i in range(8):
        rx = 46 + r_i * (r_w + 13)
        ry = 764
        svg.append(f'<rect x="{rx}" y="{ry}" width="{r_w}" height="190" rx="8" fill="#081726" stroke="#00B4D8" stroke-width="1.5"/>')
        svg.append(f'<rect x="{rx}" y="{ry}" width="{r_w}" height="26" rx="6" fill="#133B5C"/>')
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 18}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
            f'RIVER SLOT {r_i+1} (+1 WEALTH)</text>'
        )
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 78}" text-anchor="middle" fill="#8ECAE6" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
            f'FACE-UP POLICY CARD</text>'
        )
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 100}" text-anchor="middle" fill="#A8DADC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5">'
            f'Tier 1: 1M | Tier 2: 2M | Tier 3: 4-5M</text>'
        )
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 120}" text-anchor="middle" fill="#80ED99" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10">'
            f'Slide Down When Enacted</text>'
        )
        svg.append(f'<rect x="{rx+10}" y="{ry+134}" width="{r_w-20}" height="46" rx="5" fill="#0F2C3F" stroke="#2A9D8F"/>')
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 151}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">'
            f'VARIANT B ROYALTY CAP / TURN</text>'
        )
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 170}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5">'
            f'[ Roy 1 ]   [ Roy 2 ]   [ N:05 ]</text>'
        )

    # ==========================================================================
    # ZONE 4: 20-TURN OLG CLOCK & CHASING FINLAND TRACK (y = 984 to 1190)
    # ==========================================================================
    svg.append('<rect x="30" y="984" width="1740" height="206" rx="12" fill="#0F2942" stroke="#2A9D8F" stroke-width="2"/>')
    svg.append(
        '<text x="46" y="1008" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="14.5" font-weight="bold">'
        'ZONE 4A: 20-TURN OLG LIFECYCLE CLOCK (dt = 3 YEARS / 1 PARLIAMENTARY TERM PER TURN: 2026 TO 2086)</text>'
    )

    t_w = 81
    for t in range(1, 21):
        tx = 46 + (t - 1) * (t_w + 4.5)
        ty = 1018
        yr = 2026 + (t - 1) * 3
        is_2050 = (t == 9)  # Turn 9 = 2050 (2026 + 8*3 = 2050)
        t_fill = "#5C4408" if is_2050 else "#091A2B"
        t_stroke = "#F4C97E" if is_2050 else "#00B4D8"
        tag = "2050 TARGET!" if is_2050 else f"Age +{t*3}y"

        svg.append(f'<rect x="{tx}" y="{ty}" width="{t_w}" height="58" rx="6" fill="{t_fill}" stroke="{t_stroke}" stroke-width="1.8"/>')
        svg.append(
            f'<text x="{tx + t_w/2}" y="{ty + 22}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">T{t} ({yr})</text>'
        )
        svg.append(
            f'<text x="{tx + t_w/2}" y="{ty + 43}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">{tag}</text>'
        )

    svg.append(
        '<text x="46" y="1102" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="14.5" font-weight="bold">'
        'ZONE 4B: "CHASING FINLAND" SOCIAL COHESION MATCH RACE (C:06) &amp; THREE-PILLAR SCRABBLE MULTIPLIER</text>'
    )

    milestones = [
        (46, 250, "#4A151B", "#FF4D4D", "81.0: AOTEAROA SS0 START", "Hull Drag 0.5x | +0.25/turn"),
        (308, 250, "#1E3A5F", "#8ECAE6", "83.0 -> 96.0: SCOTLAND", "Stalls at 96.0 (No B:05 Land Tax)"),
        (570, 270, "#163E47", "#00B4D8", "88.0 -> 107.2: FINLAND BOAT", "D20 Roll: 1-5(-0.5) 6-15(+1) 16-20(+2)"),
        (852, 260, "#4F3708", "#FFB703", "90.0 -> 105: 1989 JAPAN", "Turn 7 Land Bubble Crash (-3/turn)"),
        (1124, 290, "#134035", "#2A9D8F", "114.8: AOTEAROA SS1 FOILS", "Scrabble Gamma = 1.0x | +2.60/turn"),
        (1426, 328, "#1A4D2E", "#80ED99", "126.0: SS2 HYDROFOIL VICTORY!", "Gamma = 1.5x (+0.05x/Early Turn) #1 OECD"),
    ]
    for mx, mw, mfill, mstroke, mtitle, msub in milestones:
        svg.append(f'<rect x="{mx}" y="1114" width="{mw}" height="62" rx="7" fill="{mfill}" stroke="{mstroke}" stroke-width="2"/>')
        svg.append(
            f'<text x="{mx + mw/2}" y="1139" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">{mtitle}</text>'
        )
        svg.append(
            f'<text x="{mx + mw/2}" y="1161" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.2">{msub}</text>'
        )

    svg.append('</svg>')
    return "\n".join(svg)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_content = build_board_svg()
    svg_path = OUT_DIR / "foils_and_founders_board_mat.svg"
    svg_path.write_text(svg_content, encoding="utf-8")

    html_path = OUT_DIR / "foils_and_founders_board_mat.html"
    html_content = (
        "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='utf-8'/>\n"
        "<title>Foils & Founders — Printable Macro Board Mat</title>\n"
        "<style>body{margin:0;padding:16px;background:#050C16;color:#F4C97E;font-family:sans-serif;}"
        ".wrap{max-width:1800px;margin:0 auto;}</style>\n</head>\n<body>\n"
        f"<div class='wrap'>{svg_content}</div>\n</body>\n</html>\n"
    )
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[OK] Rendered SVG Board Mat -> {svg_path.relative_to(ROOT)}")
    print(f"[OK] Rendered HTML Preview  -> {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
