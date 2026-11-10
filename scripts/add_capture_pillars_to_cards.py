#!/usr/bin/env python3
"""
Surgically stamps the 22 `feral_kickback_wealth` cards (T:00-T:10, H:01-H:10, P:06)
in `cards.yaml` with `capture_pillar` (1..4) and `capture_pillar_label` without
reformatting comments, quotes, or multi-line blocks.

Idempotent: safe to run multiple times (updates in place if fields already exist).
"""

from __future__ import annotations
from pathlib import Path
import re
import sys
from typing import Dict, Tuple

PILLAR_LABELS: Dict[int, str] = {
    1: "Pillar 1: Narrative & Short-Termism",
    2: "Pillar 2: Land Hoarding & Cartels",
    3: "Pillar 3: Family & Wage Squeeze",
    4: "Pillar 4: Offshore Escape & External Shocks",
}

# Balanced 6 / 5 / 6 / 5 split across all 22 feral_kickback_wealth cards
CARD_TO_PILLAR: Dict[str, int] = {
    # Pillar 1: Narrative & Short-Termism (6 cards — cleared by Rear T-Foil)
    "T:00": 1,
    "T:01": 1,
    "T:04": 1,
    "T:07": 1,
    "H:01": 1,
    "H:02": 1,
    # Pillar 2: Land Hoarding & Cartels (5 cards — cleared by Wing-Sail)
    "T:05": 2,
    "T:08": 2,
    "T:10": 2,
    "H:07": 2,
    "H:08": 2,
    # Pillar 3: Family & Wage Squeeze (6 cards — cleared by Front Lifting Foil)
    "T:02": 3,
    "T:03": 3,
    "T:09": 3,
    "H:03": 3,
    "H:05": 3,
    "H:06": 3,
    # Pillar 4: Offshore Escape & External Shocks (5 cards — cleared by Judo or Davos D20)
    "T:06": 4,
    "H:04": 4,
    "H:09": 4,
    "H:10": 4,
    "P:06": 4,
}


def resolve_cards_path(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
        if p.is_file():
            return p
        raise FileNotFoundError(f"Cannot find specified file: {p}")
    for candidate in (Path("cards.yaml"), Path("decks/cards.yaml"), Path("data/cards.yaml")):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Could not auto-locate cards.yaml; pass path as argv[1].")


def update_cards_yaml(path: Path) -> Tuple[int, Dict[int, int]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out_lines: list[str] = []

    current_id: str | None = None
    stamped_ids: set[str] = set()
    counts: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}

    id_re = re.compile(r"^- id:\s*(\S+)\s*$")
    kickback_re = re.compile(r"^(\s*)feral_kickback_wealth:\s*\d+\s*$")
    existing_pillar_re = re.compile(r"^\s*capture_pillar(_label)?:\s*")

    for line in lines:
        m_id = id_re.match(line)
        if m_id:
            current_id = m_id.group(1).strip("'\"")

        # Strip any prior capture_pillar / capture_pillar_label lines so re-runs stay clean
        if existing_pillar_re.match(line):
            continue

        out_lines.append(line)

        m_kb = kickback_re.match(line)
        if m_kb and current_id in CARD_TO_PILLAR:
            indent = m_kb.group(1)
            p_num = CARD_TO_PILLAR[current_id]
            p_label = PILLAR_LABELS[p_num]
            out_lines.append(f"{indent}capture_pillar: {p_num}\n")
            out_lines.append(f"{indent}capture_pillar_label: '{p_label}'\n")
            stamped_ids.add(current_id)
            counts[p_num] += 1

    missing = set(CARD_TO_PILLAR.keys()) - stamped_ids
    if missing:
        raise RuntimeError(f"Expected feral_kickback_wealth on cards not found: {sorted(missing)}")

    path.write_text("".join(out_lines), encoding="utf-8")
    return len(stamped_ids), counts


def main() -> None:
    target = resolve_cards_path(sys.argv[1] if len(sys.argv) > 1 else None)
    total, counts = update_cards_yaml(target)
    print(f"Updated {total} cards in {target}:")
    for p_num, label in PILLAR_LABELS.items():
        print(f"  {label:46s} -> {counts[p_num]} cards")


if __name__ == "__main__":
    main()