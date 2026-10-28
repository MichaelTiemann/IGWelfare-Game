#!/usr/bin/env python3
"""
Foils & Founders: Printable Cohort Command Mat (Player Board) SVG Renderer
==========================================================================
Generates a print-ready A4-Landscape SVG (297mm x 210mm aspect ratio: 1485x1050 px)
and an HTML preview wrapper in output/ with exact inner-margin geometry:
  - Outer Track Box: x=30 to x=1455 (width=1425)
  - 15 Lifecycle Boxes: start_x=42, box_w=82, gap_x=5 -> x=42..1347
  - 16th Status/Rebirth Column: x=1347, width=96 -> right edge at x=1443 (12px inner margin)

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "output"


def build_character_track_svg(y_top: int, char_label: str, sub_label: str) -> list[str]:
    lines = [
        f'<rect x="30" y="{y_top}" width="1425" height="260" rx="10" fill="#0B1F36" stroke="#00B4D8" stroke-width="2"/>',
        f'<text x="42" y="{y_top + 24}" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="15.5" font-weight="bold">'
        f'{char_label}</text>',
        f'<text x="1443" y="{y_top + 24}" text-anchor="end" fill="#A8DADC" font-family="Georgia, serif" font-size="12.5" font-style="italic">'
        f'{sub_label}</text>',
        f'<text x="42" y="{y_top + 44}" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="11.2" font-weight="bold">'
        f'STAGE 1 — BEING (TAMARIKI: j=0..5 / Ages 0-17) | STAGE 2 — BECOMING (PAKEKE: j=6..20 / Ages 18-62) | '
        f'STAGE 3 — CROSSING OVER (KAUMATUA: j=21..29 / Ages 63-89)</text>',
    ]

    # Exact grid geometry: 42 + 15*(82 + 5) + 96 = 1443 (12px inside x=1455 right border)
    start_x = 42
    box_w = 82
    box_h = 82
    gap_x = 5
    status_w = 96

    # Render Row 1: j = 0 to 14 (15 boxes)
    ry1 = y_top + 54
    for j in range(15):
        bx = start_x + j * (box_w + gap_x)
        age_lo = j * 3
        age_hi = age_lo + 2

        if j <= 5:
            fill = "#123524" if j in (0, 1, 4) else "#0F292A"
            stroke = "#80ED99" if j in (0, 1, 4) else "#2A9D8F"
            stage_tag = "B:01 GATE" if j <= 1 else ("B:02 GATE" if j == 4 else "TAMARIKI")
        else:
            fill = "#4A151B" if j == 7 else "#102E4A"
            stroke = "#FF4D4D" if j == 7 else "#00B4D8"
            stage_tag = "H:03 CHECK!" if j == 7 else ("B:03 GRANT" if j == 6 else "EARNING")

        lines.append(f'<rect x="{bx}" y="{ry1}" width="{box_w}" height="{box_h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry1 + 18}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">j={j}</text>'
        )
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry1 + 35}" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5">Age {age_lo}-{age_hi}</text>'
        )
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry1 + 54}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="9.2" font-weight="bold">{stage_tag}</text>'
        )
        if j == 0:
            lines.append(
                f'<text x="{bx + box_w/2}" y="{ry1 + 71}" text-anchor="middle" fill="#FF8080" '
                f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">Roll D20 (B:00)</text>'
            )
        elif j == 4:
            lines.append(
                f'<text x="{bx + box_w/2}" y="{ry1 + 71}" text-anchor="middle" fill="#80ED99" '
                f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">Mentoring 12-14</text>'
            )
        elif j == 6:
            lines.append(
                f'<text x="{bx + box_w/2}" y="{ry1 + 71}" text-anchor="middle" fill="#80ED99" '
                f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">Unlock Kaupapa!</text>'
            )
        elif j == 7:
            lines.append(
                f'<text x="{bx + box_w/2}" y="{ry1 + 71}" text-anchor="middle" fill="#FFD6D6" '
                f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">1d6: 1-2 Sydney</text>'
            )

    # Column 16 (Row 1): Birth Vigintile & Trajectory Token Box
    sx = start_x + 15 * (box_w + gap_x)
    lines.append(f'<rect x="{sx}" y="{ry1}" width="{status_w}" height="{box_h}" rx="6" fill="#24080D" stroke="#F4C97E" stroke-width="2"/>')
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry1 + 22}" text-anchor="middle" fill="#F4C97E" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">BIRTH D20</text>'
    )
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry1 + 43}" text-anchor="middle" fill="#FFFFFF" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="10">Vigintile (1-20)</text>'
    )
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry1 + 64}" text-anchor="middle" fill="#80ED99" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="9.5">Stunt / Thrive</text>'
    )

    # Render Row 2: j = 15 to 29 (15 boxes)
    ry2 = y_top + 148
    for idx, j in enumerate(range(15, 30)):
        bx = start_x + idx * (box_w + gap_x)
        age_lo = j * 3
        age_hi = age_lo + 2

        if j <= 20:
            fill = "#102E4A"
            stroke = "#00B4D8"
            stage_tag = "FOUNDING"
            sub_note = "+Wealth/Turn"
        else:
            fill = "#3D2B08"
            stroke = "#F4C97E"
            stage_tag = "ELDER (K:06)"
            sub_note = "+1 Exp Token!" if j < 28 else "Succession!"

        lines.append(f'<rect x="{bx}" y="{ry2}" width="{box_w}" height="{box_h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry2 + 18}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">j={j}</text>'
        )
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry2 + 35}" text-anchor="middle" fill="#E0FBFC" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10.5">Age {age_lo}-{age_hi}</text>'
        )
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry2 + 54}" text-anchor="middle" fill="#F4C97E" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="9.2" font-weight="bold">{stage_tag}</text>'
        )
        lines.append(
            f'<text x="{bx + box_w/2}" y="{ry2 + 71}" text-anchor="middle" fill="#80ED99" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">{sub_note}</text>'
        )

    # Column 16 (Row 2): Box 30 — Passing Over & Piketty-Saez Rebirth at J=0
    lines.append(f'<rect x="{sx}" y="{ry2}" width="{status_w}" height="{box_h}" rx="6" fill="#521924" stroke="#FF8080" stroke-width="2"/>')
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry2 + 20}" text-anchor="middle" fill="#FF8080" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">j=30 (90y)</text>'
    )
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry2 + 38}" text-anchor="middle" fill="#FFFFFF" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold">REBIRTH J=0</text>'
    )
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry2 + 55}" text-anchor="middle" fill="#F4C97E" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="9">Roll D20 Raw</text>'
    )
    lines.append(
        f'<text x="{sx + status_w/2}" y="{ry2 + 71}" text-anchor="middle" fill="#80ED99" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="8.5">B:02 Bequest</text>'
    )

    return lines


def build_cohort_svg() -> str:
    width, height = 1485, 1050
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<defs>',
        '  <linearGradient id="cohortBg" x1="0%" y1="0%" x2="100%" y2="100%">',
        '    <stop offset="0%" stop-color="#061220"/>',
        '    <stop offset="60%" stop-color="#0B1D33"/>',
        '    <stop offset="100%" stop-color="#0A242E"/>',
        '  </linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#cohortBg)"/>',
        f'<rect x="12" y="12" width="{width-24}" height="{height-24}" rx="14" fill="none" stroke="#D4A359" stroke-width="3"/>',
        '<text x="742" y="44" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" '
        'font-size="22" font-weight="bold" letter-spacing="1.2">'
        'FOILS &amp; FOUNDERS — MULTI-GENERATIONAL COHORT COMMAND MAT (PLAYER BOARD)</text>',
        '<text x="742" y="68" text-anchor="middle" fill="#A8DADC" font-family="Georgia, serif" '
        'font-size="15" font-style="italic">'
        '"Not all lives are easy, but none should be impossible." — Each Turn = 3 Years across Being, Becoming, &amp; Crossing Over</text>',
    ]

    svg.extend(
        build_character_track_svg(
            84,
            "CHARACTER SLOT A (GENERATION 1 — E.G., START AT AGE 36 [j=12] OR AGE 66 [j=22])",
            "Full Agency at j=6..29 | Unlocks K:06 Experience Token/Turn at j=21 (Age 63+)",
        )
    )
    svg.extend(
        build_character_track_svg(
            358,
            "CHARACTER SLOT B (GENERATION 2 — E.G., START AT AGE 3 [j=1] OR AGE 21 [j=7])",
            "Absorbs B:01/B:02 Buffs at j=0..5 | Watch Age-21 Sydney Brain-Drain Check at j=7!",
        )
    )

    # ==========================================================================
    # BOTTOM COMMAND BAYS (y = 632 to 1018)
    # ==========================================================================
    svg.append('<rect x="30" y="632" width="465" height="386" rx="10" fill="#0E273C" stroke="#2A9D8F" stroke-width="2.5"/>')
    svg.append(
        '<text x="48" y="658" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">'
        'KAUPAPA PERSONA COMMAND ZONE (K:01-K:07)</text>'
    )
    svg.append(
        '<text x="48" y="678" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        'Tap once/turn for Innate Kaupapa or Wildcard Synergy Link!</text>'
    )
    svg.append('<rect x="48" y="692" width="205" height="255" rx="8" fill="#081726" stroke="#F4C97E" stroke-width="2" stroke-dasharray="6,4"/>')
    svg.append(
        '<text x="150" y="795" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">'
        'PRIMARY KAUPAPA</text>'
    )
    svg.append(
        '<text x="150" y="818" text-anchor="middle" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '(Character A: K:01-K:06)</text>'
    )
    svg.append(
        '<text x="150" y="842" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="10">'
        'Passes over at j=30 unless</text>'
    )
    svg.append(
        '<text x="150" y="856" text-anchor="middle" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="10">'
        'B:02 Succession is active!</text>'
    )

    svg.append('<rect x="272" y="692" width="205" height="255" rx="8" fill="#081726" stroke="#00B4D8" stroke-width="2" stroke-dasharray="6,4"/>')
    svg.append(
        '<text x="374" y="795" text-anchor="middle" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">'
        'SECONDARY / KOTAHITANGA</text>'
    )
    svg.append(
        '<text x="374" y="818" text-anchor="middle" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '(Char B / Dual-Class Overlay)</text>'
    )
    svg.append(
        '<text x="374" y="842" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="10">'
        'Unlocks at Age 18 (j=6) or</text>'
    )
    svg.append(
        '<text x="374" y="856" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="10">'
        'Age 12 (j=4) with B:02!</text>'
    )
    svg.append(
        '<text x="262" y="972" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">'
        'K:06 Elder Dividend (j=21..29): +1 Free Lifetime Experience Token/Turn!</text>'
    )
    svg.append(
        '<text x="262" y="992" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="10.5">'
        '(Cuts N:01-N:05, B:04, or B:08 deployment cost by 100%)</text>'
    )

    # Bay 2: Available Mana Pool & Contingent Liability Reference
    svg.append('<rect x="510" y="632" width="465" height="386" rx="10" fill="#0E273C" stroke="#F4C97E" stroke-width="2.5"/>')
    svg.append(
        '<text x="528" y="658" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">'
        'MANA POOL (M_i) — RANGATIRATANGA &amp; STANDING</text>'
    )
    svg.append(
        '<text x="528" y="678" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        'Start with 3 Seed Mana/Adult | Floor = 0 Mana ("None Impossible")</text>'
    )
    svg.append('<rect x="528" y="692" width="429" height="150" rx="8" fill="#081726" stroke="#D4A359" stroke-width="1.8"/>')
    svg.append(
        '<text x="742" y="755" text-anchor="middle" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="bold">'
        'AVAILABLE (UNSTAKED) MANA TOKENS</text>'
    )
    svg.append(
        '<text x="742" y="782" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="12">'
        'Initiator Payout = mu * Sum(m_k) | River Royalty = mu * m_j</text>'
    )
    svg.append(
        '<text x="742" y="804" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11.5">'
        'Multipliers: Base = 1x | Complete SS1 = 2x! | Complete SS2 = 3x!</text>'
    )

    svg.append('<rect x="528" y="854" width="429" height="146" rx="8" fill="#2B1219" stroke="#FF8080" stroke-width="1.5"/>')
    svg.append(
        '<text x="542" y="876" fill="#FF8080" font-family="Helvetica, Arial, sans-serif" font-size="12.5" font-weight="bold">'
        'CONTINGENT LIABILITY RULES (SKIN IN THE WAKA):</text>'
    )
    svg.append(
        '<text x="542" y="898" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '1. Goal Succeeds w/ Stake: Stake returned + full mu*Mana dividend!</text>'
    )
    svg.append(
        '<text x="542" y="918" fill="#FFD6D6" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '2. Bystander Forfeit (0 Staked): Lose -2 Mana (SS1) / -3 Mana (SS2)!</text>'
    )
    svg.append(
        '<text x="542" y="938" fill="#FFD6D6" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '3. Unsaved Trap / Elder Dies: Staked Mana on failed goal is forfeited!</text>'
    )
    svg.append(
        '<text x="542" y="958" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '4. Abolishing Impossible Corner (Bay 1): +5 Legacy Mana Bonus!</text>'
    )
    svg.append(
        '<text x="542" y="978" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '5. At 0 Mana: Fund B:01 care or co-tap K:07 to restore +1 Mana.</text>'
    )

    # Bay 3: Liquid Wealth, Generosity, & Dynasty Endowment Treasury
    svg.append('<rect x="990" y="632" width="465" height="386" rx="10" fill="#0E273C" stroke="#00B4D8" stroke-width="2.5"/>')
    svg.append(
        '<text x="1008" y="658" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">'
        'WEALTH &amp; GENEROSITY TREASURY (W_i)</text>'
    )
    svg.append(
        '<text x="1008" y="678" fill="#E0FBFC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        'Earned at Phase I (by Age/Tier) + Phase II (+1 Generosity/River Card)</text>'
    )
    svg.append('<rect x="1008" y="692" width="429" height="150" rx="8" fill="#081726" stroke="#00B4D8" stroke-width="1.8"/>')
    svg.append(
        '<text x="1222" y="755" text-anchor="middle" fill="#00B4D8" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="bold">'
        'LIQUID WEALTH &amp; GENEROSITY TOKENS</text>'
    )
    svg.append(
        '<text x="1222" y="782" text-anchor="middle" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="12">'
        'Spend to: Pay Subsystem Political Drag | Shield Tamariki (2W)</text>'
    )
    svg.append(
        '<text x="1222" y="804" text-anchor="middle" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11.5">'
        'Emergency Bailout (4W) | Repatriate Exiled Sydney Graduate (3W)</text>'
    )

    svg.append('<rect x="1008" y="854" width="429" height="146" rx="8" fill="#102A2E" stroke="#2A9D8F" stroke-width="1.5"/>')
    svg.append(
        '<text x="1022" y="876" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="12.5" font-weight="bold">'
        'THREE-PILLAR SCRABBLE SCORING (TURN 20 / SS2):</text>'
    )
    svg.append(
        '<text x="1022" y="898" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '• Pillar I (Toa Takitini): Individual/Cohort Mana Laureate (M_i)</text>'
    )
    svg.append(
        '<text x="1022" y="918" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '• Pillar II (Pou Rawa): Individual/Cohort Wealth Laureate (W_i)</text>'
    )
    svg.append(
        '<text x="1022" y="938" fill="#80ED99" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">'
        '• Pillar III (Te Waka Hourua): Sum(M_i + W_i) * Gamma_Regime</text>'
    )
    svg.append(
        '<text x="1022" y="958" fill="#A8DADC" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '  SS0 = 0.5x (No Laureates!) | SS1 = 1.0x | SS2 = 1.5x (+0.05x/Early Turn)</text>'
    )
    svg.append(
        '<text x="1022" y="978" fill="#F4C97E" font-family="Helvetica, Arial, sans-serif" font-size="11">'
        '  Championship Standard: >= 135 Per-Capita Pts &amp; Beat Finland (126.0)!</text>'
    )

    svg.append('</svg>')
    return "\n".join(svg)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_content = build_cohort_svg()
    svg_path = OUT_DIR / "foils_and_founders_cohort_mat.svg"
    svg_path.write_text(svg_content, encoding="utf-8")

    html_path = OUT_DIR / "foils_and_founders_cohort_mat.html"
    html_content = (
        "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='utf-8'/>\n"
        "<title>Foils & Founders — Cohort Command Mat (Player Board)</title>\n"
        "<style>body{margin:0;padding:16px;background:#050C16;color:#F4C97E;font-family:sans-serif;}"
        ".wrap{max-width:1485px;margin:0 auto;}</style>\n</head>\n<body>\n"
        f"<div class='wrap'>{svg_content}</div>\n</body>\n</html>\n"
    )
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[OK] Rendered SVG Cohort Mat  -> {svg_path.relative_to(ROOT)}")
    print(f"[OK] Rendered HTML Preview    -> {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
