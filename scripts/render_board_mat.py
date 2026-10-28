#!/usr/bin/env python3
"""
Foils & Founders: Printable SVG & HTML Board Mat Renderer
=========================================================
Generates a print-ready SVG (900mm x 600mm aspect ratio: 1800x1220 px)
and an HTML preview wrapper in output/ showing:
  - Zone 1: The Rawlsian D20 Reef & Vigintile Compass (B:00)
  - Zone 2: The 3 Interlocking Subsystem Bays (Sub-Zones A, B, and C)
  - Zone 3: The 8-Slot Texas Hold'em River (Variant B Persistent Royalties)
  - Zone 4: The 20-Turn OLG Clock & Chasing Finland Cohesion Race Track

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
        '<text x="48" y="108" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="bold">'
        'ZONE 1: THE RAWLSIAN D20 BIRTH &amp; ENDOGENOUS HAZARD COMPASS (20 WEALTH VIGINTILES)</text>'
    )
    svg.append(
        '<text x="1750" y="108" text-anchor="end" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="13">'
        'Cover Red/Amber Reefs by Locking Subsystems 1, 2, &amp; 3 Below ("Make Your Own Luck")</text>'
    )

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
            f'font-family="Helvetica, Arial, sans-serif" font-size="20" font-weight="bold">d20: {d}</text>'
        )
        svg.append(
            f'<text x="{cx + cell_w/2}" y="{cy + 46}" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">{label}</text>'
        )

    svg.append(
        '<text x="295" y="194" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
        'BOTTOM REEF (1-6): Triggers T:00/T:01/T:05 | Closed by BAY 1 (B:01+B:02)</text>'
    )
    svg.append(
        '<text x="950" y="194" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
        'ELECTION AUDIT (1-8 on Turns 3,6,9,12,15,18): Triggers H:01/H:02 | Closed by BAY 3 (B:07)</text>'
    )
    svg.append(
        '<text x="1605" y="194" text-anchor="middle" fill="#FFB703" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
        'TOP REEF (19-20): T:02/T:04 | Closed by BAY 2 (B:05)</text>'
    )

    # ==========================================================================
    # ZONE 2: THE THREE INTERLOCKING SUBSYSTEM BAYS (y = 222 to 707)
    # ==========================================================================
    bays = [
        {
            "x": 30,
            "title": "BAY 1: FRONT LIFTING FOIL",
            "maori": "Te Korowai Mokopuna (Human Capability)",
            "recipe": "REQUIRED: B:01 (First 2000 Days) + B:02 (Tuakana-Teina) + 1 Amplifier (N:01, N:02, C:02, C:03)",
            "judo": "JUDO COUNTERS: Play B:01+N:02 vs. T:00/T:01 | Play C:02 or K:05 vs. T:05 Outrage",
            "lock": "LOCKED REWARD: Covers D20 Reef 1-6 (No Life Impossible!) + Awards +5 Legacy Mana Bonus",
            "color": "#2A9D8F",
        },
        {
            "x": 625,
            "title": "BAY 2: WING-SAIL POWER PLANT",
            "maori": "Te Aka Matua (Capital &amp; Clean Energy Rotation)",
            "recipe": "REQUIRED: B:05 (Use-It-Or-Lose-It) + B:03 (Youth Grant) + 1 Engine (E:01, E:02, C:05)",
            "judo": "JUDO COUNTERS: Play B:05+N:05 or K:02 vs. T:02/T:04/H:05 | Play B:03 vs. H:03 Exile",
            "lock": "LOCKED REWARD: Covers D20 Reef 19-20 + Stops Sydney Brain Drain + Adults Earn +1 Wealth/Turn",
            "color": "#00B4D8",
        },
        {
            "x": 1220,
            "title": "BAY 3: REAR T-FOIL STABILIZER",
            "maori": "Nga Kete o te Wananga (Actuarial &amp; Fiscal Governance)",
            "recipe": "REQUIRED: B:07 (ACC Time-Bend) + B:06 (2050 50/50 Rule) + 1 Proof (N:03, N:04, B:04, B:08)",
            "judo": "JUDO COUNTERS: Play B:07+N:03 vs. H:01 Cash Myopia | Play N:01/N:04 vs. H:02 Silos",
            "lock": "LOCKED REWARD: Cancels Election Audits + PAYE Cut to 18.5% (+1W/Turn) + Super @ 65 (K:06)",
            "color": "#D4A359",
        },
    ]

    for b in bays:
        bx = b["x"]
        bw = 550
        svg.append(f'<rect x="{bx}" y="222" width="{bw}" height="485" rx="12" fill="#0B1F36" stroke="{b["color"]}" stroke-width="3"/>')
        svg.append(
            f'<text x="{bx + 18}" y="248" fill="{b["color"]}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="bold">'
            f'{b["title"]}</text>'
        )
        svg.append(
            f'<text x="{bx + bw - 18}" y="248" text-anchor="end" fill="#F4C97E" font-family="Georgia, serif" font-size="14" font-style="italic">'
            f'{b["maori"]}</text>'
        )
        svg.append(
            f'<text x="{bx + 18}" y="268" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="11.5" font-weight="bold">'
            f'{b["recipe"]}</text>'
        )
        svg.append(
            f'<text x="{bx + 18}" y="286" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
            f'Political Drag Cost: [2P: 1.5 Wealth] | [3-4P: 2.0 Wealth] | [5-6P: 3.0 Wealth + 3 Co-Stakers (unless K:07)]</text>'
        )

        # Sub-Zone A: Staking & Incubation
        svg.append(f'<rect x="{bx+16}" y="298" width="{bw-32}" height="135" rx="8" fill="#102E4A" stroke="#00B4D8" stroke-width="1.5"/>')
        svg.append(
            f'<text x="{bx+28}" y="318" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">'
            f'SUB-ZONE A: CONTINGENT MANA STAKING &amp; INCUBATION (UPRIGHT 0-DEG TOKENS)</text>'
        )
        for slot_i in range(3):
            sx = bx + 32 + slot_i * 165
            svg.append(f'<rect x="{sx}" y="328" width="150" height="94" rx="6" fill="#0A1E32" stroke="#457B9D" stroke-dasharray="5,4"/>')
            svg.append(
                f'<text x="{sx+75}" y="375" text-anchor="middle" fill="#8ECAE6" font-family="Helvetica, Arial, sans-serif" font-size="11">'
                f'Card / Upright Mana #{slot_i+1}</text>'
            )

        # Sub-Zone B: 1-Turn Emergency / Jeopardy Box
        svg.append(
            f'<rect x="{bx+16}" y="444" width="{bw-32}" height="135" rx="8" fill="#3B1018" stroke="#FF4D4D" stroke-width="2" stroke-dasharray="8,5"/>'
        )
        svg.append(
            f'<text x="{bx+28}" y="466" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">'
            f'SUB-ZONE B: 1-TURN EMERGENCY / JEOPARDY BOX (TIP MANA 90-DEG SIDEWAYS!)</text>'
        )
        svg.append(
            f'<text x="{bx+28}" y="485" fill="#FFD6D6" font-family="Helvetica, Arial, sans-serif" font-size="11">'
            f'If D20 Reef Roll or Feral Spoiler hits: Place T/H Trap here. Save within 1 Turn or Forfeit Staked Mana!</text>'
        )
        svg.append(f'<rect x="{bx+28}" y="495" width="160" height="72" rx="6" fill="#24080D" stroke="#FF4D4D"/>')
        svg.append(
            f'<text x="{bx+108}" y="535" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">'
            f'TRAP / BOSS SLOT</text>'
        )
        svg.append(f'<rect x="{bx+204}" y="495" width="318" height="72" rx="6" fill="#182B3A" stroke="#2A9D8F"/>')
        svg.append(
            f'<text x="{bx+363}" y="523" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">'
            f'EMPIRICAL SHIELD / JUDO COUNTER SLOT</text>'
        )
        svg.append(
            f'<text x="{bx+363}" y="543" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="10.5">'
            f'{b["judo"]}</text>'
        )
        svg.append(
            f'<text x="{bx+363}" y="560" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="10">'
            f'Feral Backfire: Countering Spoiler = +1 Mana to Crew &amp; -2 Mana Whakama to Spoiler!</text>'
        )

        # Sub-Zone C: Locked Foil Plinth
        svg.append(f'<rect x="{bx+16}" y="590" width="{bw-32}" height="104" rx="8" fill="#123524" stroke="#80ED99" stroke-width="2"/>')
        svg.append(
            f'<text x="{bx+28}" y="614" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="bold">'
            f'SUB-ZONE C: LOCKED HYDROFOIL / KIATO PLINTH (REEF CLEARED!)</text>'
        )
        svg.append(
            f'<text x="{bx+28}" y="638" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">'
            f'{b["lock"]}</text>'
        )
        svg.append(
            f'<text x="{bx+28}" y="662" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="11.5">'
            f'Bystander Forfeit Check: Any player with 0 Mana staked when locked forfeits -2 Mana (SS1) / -3 Mana (SS2)!</text>'
        )
        svg.append(
            f'<text x="{bx+28}" y="682" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
            f'Multiplier Status: [Any 2 Bays Locked = SS1 (2x Mana!)] | [All 3 Bays + Capstone = SS2 (3x Mana!)]</text>'
        )

    # ==========================================================================
    # ZONE 3: THE TEXAS HOLD'EM RIVER & PERSISTENT COMMONS (y = 724 to 968)
    # ==========================================================================
    svg.append('<rect x="30" y="724" width="1740" height="244" rx="12" fill="#0D233A" stroke="#F4C97E" stroke-width="2.5"/>')
    svg.append(
        '<text x="48" y="750" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="bold">'
        'ZONE 3: THE TEXAS HOLD\'EM RIVER — PERSISTENT INSTITUTIONAL INFRASTRUCTURE (VARIANT B / ROMER N:05)</text>'
    )
    svg.append(
        '<text x="1750" y="750" text-anchor="end" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">'
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
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5" font-weight="bold">'
            f'VARIANT B ROYALTY CAP / TURN</text>'
        )
        svg.append(
            f'<text x="{rx + r_w/2}" y="{ry + 170}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="11">'
            f'[ Roy 1 ]   [ Roy 2 ]   [ N:05 ]</text>'
        )

    # ==========================================================================
    # ZONE 4: 20-TURN OLG CLOCK & CHASING FINLAND TRACK (y = 984 to 1190)
    # ==========================================================================
    svg.append('<rect x="30" y="984" width="1740" height="206" rx="12" fill="#0F2942" stroke="#2A9D8F" stroke-width="2"/>')
    svg.append(
        '<text x="48" y="1008" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">'
        'ZONE 4A: 20-TURN OLG LIFECYCLE CLOCK (dt = 3 YEARS/TURN: 2026 TO 2086) — RED TURNS = PARLIAMENTARY ELECTION AUDIT (H:01)</text>'
    )

    t_w = 81
    for t in range(1, 21):
        tx = 46 + (t - 1) * (t_w + 4.5)
        ty = 1018
        yr = 2026 + (t - 1) * 3
        is_elec = (t % 3 == 0)
        is_2050 = (t == 8)
        t_fill = "#5C1620" if is_elec else ("#5C4408" if is_2050 else "#091A2B")
        t_stroke = "#FF4D4D" if is_elec else ("#F4C97E" if is_2050 else "#00B4D8")
        tag = "ELECTION!" if is_elec else ("2050 RULE" if is_2050 else f"Age +{t*3}y")

        svg.append(f'<rect x="{tx}" y="{ty}" width="{t_w}" height="58" rx="6" fill="{t_fill}" stroke="{t_stroke}" stroke-width="1.8"/>')
        svg.append(
            f'<text x="{tx + t_w/2}" y="{ty + 20}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12.5" font-weight="bold">T{t} ({yr})</text>'
        )
        svg.append(
            f'<text x="{tx + t_w/2}" y="{ty + 42}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">{tag}</text>'
        )

    svg.append(
        '<text x="48" y="1102" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">'
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
            f'font-family="Helvetica, Arial, sans-serif" font-size="12.5" font-weight="bold">{mtitle}</text>'
        )
        svg.append(
            f'<text x="{mx + mw/2}" y="1161" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5">{msub}</text>'
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
