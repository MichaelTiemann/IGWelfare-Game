#!/usr/bin/env python3
"""
Foils & Founders: Focused Card-Balance, Pillar-Starvation & Tuning Guardrail Suite
==================================================================================
Fast (~15s on 17 cores at 6,000 CRN games) ongoing diagnostic harness measuring:
  1. Suite N (N:01-N:09) Constructive Spread & Automated Outlier Guardrails
  2. Capture Pillar Parity Check across all 22 Capture Cards (T:00-T:10, H:01-H:10, P:06)
  3. Pillar Starvation Curves (Removing k = 1, 2, 3, 4 cards from Pillars 1, 2, 3, & 4)
  4. 12 High-Signal Structural Pairs (or `--all-th-pairs` for all 231 Capture pairs)

Exports `output/focused_tuning_audit.csv`.

Usage:
  python3 scripts/audit_pillar_curves_and_pairs.py --games 6000
  python3 scripts/audit_pillar_curves_and_pairs.py --games 10000 --all-th-pairs
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
from itertools import combinations
import os
from pathlib import Path
import sys
import time
from typing import Dict, List, Tuple
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from simulate_foils_and_founders_balance import (  # noqa: E402
    BOSS_TRAP_META,
    NOBEL_IDS,
    SimConfig,
    load_deck_counts_from_yaml,
    simulate_single_game,
)

try:
    import yaml
except ImportError:
    yaml = None


STRAT_4P = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]

PILLAR_ROSTERS: Dict[int, List[str]] = {
    1: ["T:01", "T:07", "T:04", "H:01", "H:02", "T:00"],
    2: ["H:08", "H:07", "T:05", "T:10", "T:08"],
    3: ["H:03", "H:05", "H:06", "T:03", "T:02", "T:09"],
    4: ["H:04", "H:09", "P:06", "T:06", "H:10"],
}

FOCUSED_PAIRS: List[Tuple[str, str]] = [
    ("N:05", "N:07"), ("N:07", "N:08"), ("N:04", "N:07"), ("N:02", "N:05"),
    ("T:01", "T:07"), ("T:04", "T:07"), ("H:07", "H:08"), ("T:05", "T:10"),
    ("H:04", "T:06"), ("H:04", "P:06"), ("H:09", "P:06"), ("H:03", "H:05"),
]


def load_card_titles() -> Dict[str, str]:
    cards_yaml = ROOT / "decks" / "cards.yaml"
    if yaml is not None and cards_yaml.exists():
        data = yaml.safe_load(cards_yaml.read_text(encoding="utf-8")) or {}
        return {str(c["id"]): str(c["name"]).split(":")[0].split("(")[0].strip()[:32] for c in data.get("cards", [])}
    return {}


def _worker(task: Tuple[str, Tuple[str, ...], int, int, Dict[str, int]]) -> Tuple[str, Tuple[str, ...], np.ndarray]:
    tag, excl_tuple, n_games, seed, counts = task
    cfg = SimConfig(n_games=n_games, excluded_cards=frozenset(excl_tuple), rng_seed=seed)
    out = np.empty((n_games, 6), dtype=np.float64)
    for g in range(n_games):
        r = simulate_single_game(None, cfg, STRAT_4P, deck_counts=counts, game_seed=seed + g)
        out[g, 0] = r["ss2_reached"] * 100.0
        out[g, 1] = r["ss2_turn"]
        out[g, 2] = r["moon_shot"] * 100.0
        out[g, 3] = r["crew_score"]
        out[g, 4] = r["player_wealth"][3]
        out[g, 5] = r["beat_finland"] * 100.0
    return tag, excl_tuple, out


def paired_delta(base_arr: np.ndarray, without_arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    diff = base_arr - without_arr
    return diff.mean(axis=0), diff.std(axis=0, ddof=1) / np.sqrt(diff.shape[0])


def main() -> None:
    ap = argparse.ArgumentParser(description="Focused T/H/N/P:06 Balance & Pillar Starvation Diagnostic Suite.")
    ap.add_argument("-n", "--games", type=int, default=6_000, help="CRN games per config (default: 6000)")
    ap.add_argument("-w", "--workers", type=int, default=max(1, (os.cpu_count() or 8) - 1), help="CPU worker processes")
    ap.add_argument("--all-th-pairs", action="store_true", help="Also run all 231 Capture-card pairs (incl. P:06)")
    ap.add_argument("--seed", type=int, default=20261126, help="Base SeedSequence integer")
    args = ap.parse_args()

    t0 = time.perf_counter()
    titles = load_card_titles()
    base_counts = load_deck_counts_from_yaml(singleton_override=False)
    capture_ids = sorted(BOSS_TRAP_META.keys())
    all_singles = list(NOBEL_IDS) + capture_ids

    tasks: List[Tuple[str, Tuple[str, ...], int, int, Dict[str, int]]] = [
        ("BASE", (), args.games, args.seed, base_counts)
    ]
    seen = {()}
    for cid in all_singles:
        k = (cid,)
        seen.add(k)
        tasks.append((f"1:{cid}", k, args.games, args.seed, base_counts))

    # Pillar starvation curves: remove top k = 2, 3, 4 cards from each Pillar 1..4
    for pil_num, roster in PILLAR_ROSTERS.items():
        for k_rem in (2, 3, 4):
            sub_k = tuple(sorted(roster[:k_rem]))
            if sub_k not in seen:
                seen.add(sub_k)
                tasks.append((f"STARVE_P{pil_num}_k{k_rem}", sub_k, args.games, args.seed, base_counts))

    pair_list = FOCUSED_PAIRS + (list(combinations(capture_ids, 2)) if args.all_th_pairs else [])
    for a, b in pair_list:
        pk = tuple(sorted((a, b)))
        if pk not in seen:
            seen.add(pk)
            tasks.append((f"PAIR:{a}+{b}", pk, args.games, args.seed, base_counts))

    print(
        f"Running {len(tasks)} focused configs x {args.games:,} CRN games = {len(tasks)*args.games:,} games "
        f"on {args.workers} workers..."
    )
    results: Dict[Tuple[str, ...], np.ndarray] = {}
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for idx, (_, k_tup, arr) in enumerate(pool.map(_worker, tasks, chunksize=1), 1):
            results[k_tup] = arr
            if idx % 20 == 0 or idx == len(tasks):
                dt = time.perf_counter() - t0
                print(f"  [{idx:3d}/{len(tasks)}] {dt:5.1f}s ({idx * args.games / dt:,.0f} games/sec)")

    base = results[()]
    bm = base.mean(axis=0)
    print(
        f"\nBASELINE: SS2={bm[0]:5.2f}% (Turn {bm[1]:4.2f}) | SpoilerMoon={bm[2]:5.2f}% | "
        f"CrewScore={bm[3]:6.2f} | SpoilerWealth={bm[4]:5.2f} | BeatFinland={bm[5]:5.2f}%"
    )

    s_deltas = {cid: paired_delta(base, results[(cid,)]) for cid in all_singles}

    # --- 1. SUITE N SPREAD & GUARDRAIL CHECK ---
    print("\n=== 1. SUITE N CONSTRUCTIVE BALANCE & GUARDRAILS (Full - Without) ===")
    n_pts = [s_deltas[c][0][3] for c in NOBEL_IDS]
    n_med = float(np.median(n_pts))
    for cid in sorted(NOBEL_IDS, key=lambda c: s_deltas[c][0][3], reverse=True):
        m, se = s_deltas[cid]
        flag = " [WATCH: >2.8x median]" if m[3] > max(28.0, 2.8 * max(4.0, n_med)) else ""
        print(
            f"  {cid} {titles.get(cid, ''):<32s} | dCrew={m[3]:+6.2f} ({se[3]:4.2f}) | "
            f"dSS2={m[0]:+5.2f}% | dTurn={m[1]:+5.2f} | dMoon={m[2]:+5.2f}%{flag}"
        )

    # --- 2. PILLAR PARITY SUMMARY ACROSS ALL 22 CAPTURE CARDS ---
    print("\n=== 2. CAPTURE PILLAR MEAN SINGLE-CARD MEANS (Checking Dilution Parity) ===")
    for pil_num in (1, 2, 3, 4):
        cids = PILLAR_ROSTERS[pil_num]
        vecs = np.array([s_deltas[c][0] for c in cids])
        mu = vecs.mean(axis=0)
        print(
            f"  Pillar {pil_num} ({len(cids)} cards: {', '.join(cids):<34s}) -> "
            f"Mean dMoon={mu[2]:+5.2f}% | Mean dSpWlth={mu[4]:+5.2f} | Mean dCrew={mu[3]:+6.2f}"
        )

    # --- 3. PILLAR STARVATION CURVES (k = 1..4 REMOVED FROM EACH PILLAR) ---
    print("\n=== 3. PILLAR STARVATION CURVES: SPOILER MOON% WHEN k CARDS REMOVED FROM ONE PILLAR ===")
    print(f"  {'Pillar':<10s} | {'Full (k=0)':>10s} | {'k=1 Out':>10s} | {'k=2 Out':>10s} | {'k=3 Out':>10s} | {'k=4 Out':>10s}")
    print("  " + "-" * 68)
    for pil_num, roster in PILLAR_ROSTERS.items():
        vals = [bm[2]]
        for k_rem in (1, 2, 3, 4):
            sub_k = tuple(sorted(roster[:k_rem]))
            vals.append(float(results[sub_k][:, 2].mean()))
        print(
            f"  Pillar {pil_num:<3d} | {vals[0]:9.2f}% | {vals[1]:9.2f}% | {vals[2]:9.2f}% | "
            f"{vals[3]:9.2f}% | {vals[4]:9.2f}%"
        )

    # --- 4. HIGH-SIGNAL PAIRS & SYNERGY WEDGES ---
    print("\n=== 4. FOCUSED PAIRWISE INTERACTIONS (Joint = Full - Without_AB | Syn = Joint - Sum_Singles) ===")
    pair_keys = [k for k in results if len(k) == 2]
    scored_pairs = []
    for a, b in pair_keys:
        m_ab, se_ab = paired_delta(base, results[(a, b)])
        syn = m_ab - (s_deltas[a][0] + s_deltas[b][0])
        scored_pairs.append((abs(m_ab[2]) + 0.25 * abs(m_ab[3]), a, b, m_ab, se_ab, syn))
    scored_pairs.sort(reverse=True)
    for _, a, b, m_ab, se_ab, syn in scored_pairs[:16]:
        print(
            f"  {a}+{b:<6s} | Joint dCrew={m_ab[3]:+7.2f} (Syn {syn[3]:+6.2f}) | "
            f"Joint dMoon={m_ab[2]:+6.2f}% (Syn {syn[2]:+6.2f}%) | Joint dSS2={m_ab[0]:+5.2f}%"
        )

    out_csv = ROOT / "output" / "focused_tuning_audit.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["excluded_cards", "n_excluded", "mean_ss2_pct", "mean_ss2_turn", "mean_moon_pct", "mean_crew_pts", "mean_spoiler_w", "mean_beat_fin_pct"])
        for k_tup in sorted(results.keys(), key=lambda x: (len(x), x)):
            rm = results[k_tup].mean(axis=0)
            w.writerow(["+".join(k_tup) or "BASELINE", len(k_tup), *[round(float(v), 4) for v in rm]])
    print(f"\n[OK] Saved {len(results)} summary rows -> {out_csv.relative_to(ROOT)}")


if __name__ == "__main__":
    main()