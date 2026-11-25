#!/usr/bin/env python3
"""
Foils & Founders: Multi-Core T, H, & N Card Power & Pairwise Synergy Auditor
=============================================================================
Uses Common Random Numbers (CRN) across multi-core worker processes to measure:
  1. Leave-One-Out Marginal Card Power across all 30 T, H, & N cards:
       - Suite N (N:01-N:09): Constructive contribution when PRESENT (`Full - Without`)
       - Suites T (T:00-T:10) & H (H:01-H:10): Threat / Spoiler / Drag power when PRESENT (`Full - Without`)
  2. Leave-Two-Out Pairwise Interactions (`Delta_AB = Full - Without(A, B)` and Pure Synergy Wedge
     `I_AB = Delta_AB - (Delta_A + Delta_B)`):
       - All 36 Nobel-Pair combinations (`N:xx + N:yy`)
       - 24 High-Leverage Intra-Pillar & Macro-Coupled Boss/Trap pairs (`T/H + T/H`)
       - 12 Canonical Nobel-Shield vs. Boss/Trap Counter pairs (`N + H/T`)
     (Pass `--all-th-pairs` to also sweep all 210 `T/H x T/H` pairs!)

Outputs ranked console tables + `output/thn_card_power_and_pairs.csv`.

Usage:
  python3 scripts/audit_thn_card_power.py --games 6000
  python3 scripts/audit_thn_card_power.py --games 12000 --all-th-pairs
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
from typing import Dict, List, Sequence, Tuple
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from simulate_foils_and_founders_balance import (  # noqa: E402
    BOSS_IDS,
    BOSS_TRAP_META,
    NOBEL_IDS,
    TRAP_IDS,
    SimConfig,
    load_deck_counts_from_yaml,
    simulate_single_game,
)

try:
    import yaml
except ImportError:
    yaml = None


STRAT_4P = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]

# Curated high-interest Boss/Trap pairs (same-Pillar bottlenecks + coupled macro sinkholes)
CURATED_TH_PAIRS: List[Tuple[str, str]] = [
    # Pillar 4 (Bay-Immune Offshore & Shock Bottleneck!)
    ("H:04", "H:09"), ("H:04", "T:06"), ("H:09", "H:10"), ("T:06", "H:10"),
    # Pillar 2 (Land Hoarding, Bubbles, & Cartels)
    ("H:07", "H:08"), ("T:05", "T:10"), ("T:05", "H:07"), ("T:10", "H:08"), ("T:08", "H:07"),
    # Pillar 1 (Cash-Book Myopia, Silos, Surge, & Election Scissor-Blade)
    ("H:01", "T:07"), ("H:01", "H:02"), ("T:04", "T:07"), ("T:01", "T:07"), ("T:00", "H:02"),
    # Pillar 3 (GUiNZ Hardship, Sandwich Care, Rent Squeeze, & Austerity)
    ("H:03", "H:05"), ("H:03", "H:06"), ("T:02", "T:03"), ("T:03", "H:05"), ("T:09", "H:06"),
    # Cross-Pillar Coupled Sinkholes
    ("H:03", "H:04"), ("T:04", "H:10"), ("H:01", "T:03"), ("H:06", "H:07"), ("H:08", "H:09"),
]

# Canonical Nobel Counter vs. Boss/Trap Equilibrium Pairs
COUNTER_NH_PAIRS: List[Tuple[str, str]] = [
    ("N:04", "H:01"), ("N:02", "H:02"), ("N:05", "H:02"), ("N:01", "T:04"),
    ("N:03", "H:03"), ("N:03", "H:10"), ("N:06", "T:05"), ("N:07", "T:06"),
    ("N:07", "H:08"), ("N:07", "H:09"), ("N:07", "T:07"), ("N:08", "H:05"),
]


def load_card_titles() -> Dict[str, str]:
    cards_yaml = ROOT / "decks" / "cards.yaml"
    if yaml is not None and cards_yaml.exists():
        data = yaml.safe_load(cards_yaml.read_text(encoding="utf-8")) or {}
        return {str(c["id"]): str(c["name"]).split(":")[0].split("(")[0].strip()[:34] for c in data.get("cards", [])}
    return {}


def _run_ablation_worker(task: Tuple[str, Tuple[str, ...], int, int, Dict[str, int]]) -> Tuple[str, Tuple[str, ...], np.ndarray]:
    """
    Top-level picklable worker for macOS `spawn` multiprocessing.
    Returns per-game array of shape (n_games, 6):
      col 0: ss2_reached (0/1)
      col 1: ss2_turn
      col 2: moon_shot (0/1)
      col 3: crew_score (constructive per-capita score)
      col 4: spoiler_wealth (P4 final wealth)
      col 5: beat_finland (0/1)
    """
    label, excluded_tuple, n_games, base_seed, base_counts = task
    cfg = SimConfig(n_games=n_games, excluded_cards=frozenset(excluded_tuple), rng_seed=base_seed)
    out = np.empty((n_games, 6), dtype=np.float64)
    for g in range(n_games):
        r = simulate_single_game(None, cfg, STRAT_4P, deck_counts=base_counts, game_seed=base_seed + g)
        out[g, 0] = r["ss2_reached"] * 100.0
        out[g, 1] = r["ss2_turn"]
        out[g, 2] = r["moon_shot"] * 100.0
        out[g, 3] = r["crew_score"]
        out[g, 4] = r["player_wealth"][3]
        out[g, 5] = r["beat_finland"] * 100.0
    return label, excluded_tuple, out


def paired_delta(base_arr: np.ndarray, without_arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes `Effect of Card(s) Being PRESENT = Full_Deck - Without_Card(s)` across CRN-paired games,
    returning (mean_vec, stderr_vec) across the 6 telemetry columns.
    """
    diff = base_arr - without_arr
    n = diff.shape[0]
    return diff.mean(axis=0), diff.std(axis=0, ddof=1) / np.sqrt(n)


def main() -> None:
    ap = argparse.ArgumentParser(description="Multi-core Leave-One-Out & Leave-Pair-Out Power Audit for T, H, & N Cards.")
    ap.add_argument("-n", "--games", type=int, default=6_000, help="CRN-paired games per configuration (default: 6000)")
    ap.add_argument("-w", "--workers", type=int, default=max(1, (os.cpu_count() or 8) - 1), help="Worker processes")
    ap.add_argument("--all-th-pairs", action="store_true", help="Also run all 210 T/H x T/H pairs (301 configs total)")
    ap.add_argument("--seed", type=int, default=20261126, help="Base SeedSequence integer")
    args = ap.parse_args()

    t0 = time.perf_counter()
    titles = load_card_titles()
    base_counts = load_deck_counts_from_yaml(singleton_override=False)

    single_cards: List[str] = list(NOBEL_IDS) + list(TRAP_IDS) + list(BOSS_IDS)
    nobel_pairs: List[Tuple[str, str]] = list(combinations(NOBEL_IDS, 2))
    th_all: List[str] = list(TRAP_IDS) + list(BOSS_IDS)
    th_pairs: List[Tuple[str, str]] = list(combinations(th_all, 2)) if args.all_th_pairs else CURATED_TH_PAIRS

    tasks: List[Tuple[str, Tuple[str, ...], int, int, Dict[str, int]]] = [
        ("BASELINE", (), args.games, args.seed, base_counts)
    ]
    for cid in single_cards:
        tasks.append((f"1:{cid}", (cid,), args.games, args.seed, base_counts))

    seen_pairs = set()
    for grp, plist in [("NN", nobel_pairs), ("TH", th_pairs), ("NH", COUNTER_NH_PAIRS)]:
        for a, b in plist:
            key = tuple(sorted((a, b)))
            if key not in seen_pairs:
                seen_pairs.add(key)
                tasks.append((f"2:{grp}:{a}+{b}", (a, b), args.games, args.seed, base_counts))

    total_sims = len(tasks) * args.games
    print(
        f"Launching {len(tasks)} configurations x {args.games:,} CRN games = {total_sims:,} total 20-turn games "
        f"across {args.workers} CPU workers..."
    )

    results: Dict[Tuple[str, ...], np.ndarray] = {}
    tags: Dict[Tuple[str, ...], str] = {}
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for done_i, (lbl, excl_t, arr) in enumerate(pool.map(_run_ablation_worker, tasks, chunksize=1), 1):
            key = tuple(sorted(excl_t))
            results[key] = arr
            tags[key] = lbl
            if done_i % 15 == 0 or done_i == len(tasks):
                elapsed = time.perf_counter() - t0
                print(f"  [{done_i:3d}/{len(tasks)}] completed in {elapsed:5.1f}s ({done_i * args.games / elapsed:,.0f} games/sec)")

    base = results[()]
    b_mean = base.mean(axis=0)
    print(
        f"\nBASELINE FULL DECK ({args.games:,} games): "
        f"SS2={b_mean[0]:5.2f}% | SS2_Turn={b_mean[1]:5.2f} | SpoilerMoon={b_mean[2]:5.2f}% | "
        f"CrewScore={b_mean[3]:6.2f} | SpoilerWealth={b_mean[4]:5.2f} | BeatFinland={b_mean[5]:5.2f}%"
    )

    single_deltas: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
    for cid in single_cards:
        single_deltas[cid] = paired_delta(base, results[(cid,)])

    # --- TABLE 1: SUITE N (CONSTRUCTIVE POWER WHEN PRESENT = FULL - WITHOUT) ---
    print("\n=== 1. SUITE N (N:01-N:09) MARGINAL CONSTRUCTIVE POWER (Effect of Card Being PRESENT) ===")
    print(
        f"{'Card':<6s} {'Title':<34s} | {'dCrewPts':>9s} {'(SE)':>6s} | {'dSS2%':>7s} | {'dTurn':>6s} | "
        f"{'dMoon%':>7s} | {'dSpWlth':>8s} | {'PowerIdx':>8s}"
    )
    print("-" * 110)
    n_rows = []
    for cid in NOBEL_IDS:
        m, se = single_deltas[cid]
        # Constructive Power Index: +CrewScore + 1.5*dSS2% - 1.2*dMoon% - 2.0*dTurn
        p_idx = m[3] + 1.5 * m[0] - 1.2 * m[2] - 2.0 * m[1]
        n_rows.append((p_idx, cid, m, se))
    n_rows.sort(reverse=True)
    for p_idx, cid, m, se in n_rows:
        print(
            f"{cid:<6s} {titles.get(cid, ''):<34s} | {m[3]:+9.2f} ({se[3]:4.2f}) | {m[0]:+6.2f}% | {m[1]:+6.2f} | "
            f"{m[2]:+6.2f}% | {m[4]:+8.2f} | {p_idx:+8.2f}"
        )

    # --- TABLE 2: SUITES T & H (DESTRUCTIVE / CAPTURE POWER WHEN PRESENT = FULL - WITHOUT) ---
    print("\n=== 2. SUITES T & H (21 CARDS) MARGINAL THREAT & CAPTURE POWER (Effect of Card Being PRESENT) ===")
    print(
        f"{'Card':<6s} {'Pil':<3s} {'KB':<3s} {'Title':<32s} | {'dMoon%':>7s} | {'dSpWlth':>8s} | "
        f"{'dCrewPts':>9s} {'(SE)':>6s} | {'dSS2%':>7s} | {'ThreatIdx':>9s}"
    )
    print("-" * 116)
    th_rows = []
    for cid in list(TRAP_IDS) + list(BOSS_IDS):
        m, se = single_deltas[cid]
        pil, kb, _ = BOSS_TRAP_META[cid]
        # Threat Index: how strongly this Trap/Boss hurts the Crew & boosts Spoiler Moon/Wealth when in the game
        threat_idx = -m[3] + 2.0 * m[2] + 0.8 * m[4] - 1.5 * m[0]
        th_rows.append((threat_idx, cid, pil + 1, kb, m, se))
    th_rows.sort(reverse=True)
    for t_idx, cid, pil_num, kb, m, se in th_rows:
        print(
            f"{cid:<6s} P{pil_num:<2d} {kb:2.0f}W {titles.get(cid, ''):<32s} | {m[2]:+6.2f}% | {m[4]:+8.2f} | "
            f"{m[3]:+9.2f} ({se[3]:4.2f}) | {m[0]:+6.2f}% | {t_idx:+9.2f}"
        )

    # --- TABLE 3: PAIRWISE INTERACTIONS (`I_AB = Delta_AB - (Delta_A + Delta_B)`) ---
    csv_rows: List[Dict[str, object]] = []
    for cid in single_cards:
        m, se = single_deltas[cid]
        csv_rows.append({
            "kind": "SINGLE",
            "cards": cid,
            "d_ss2_pct": round(float(m[0]), 4),
            "d_ss2_turn": round(float(m[1]), 4),
            "d_moon_pct": round(float(m[2]), 4),
            "d_crew_pts": round(float(m[3]), 4),
            "se_crew_pts": round(float(se[3]), 4),
            "d_spoiler_w": round(float(m[4]), 4),
            "syn_crew_pts": 0.0,
            "syn_moon_pct": 0.0,
        })

    pair_records = []
    for key, arr in results.items():
        if len(key) != 2:
            continue
        a, b = key
        m_ab, se_ab = paired_delta(base, arr)
        m_a, _ = single_deltas[a]
        m_b, _ = single_deltas[b]
        # Pure Non-Additive Interaction I_AB = (Full - Without_AB) - [(Full - Without_A) + (Full - Without_B)]
        syn_vec = m_ab - (m_a + m_b)
        grp = tags[key].split(":")[1]
        pair_records.append((grp, a, b, m_ab, se_ab, syn_vec))
        csv_rows.append({
            "kind": f"PAIR_{grp}",
            "cards": f"{a}+{b}",
            "d_ss2_pct": round(float(m_ab[0]), 4),
            "d_ss2_turn": round(float(m_ab[1]), 4),
            "d_moon_pct": round(float(m_ab[2]), 4),
            "d_crew_pts": round(float(m_ab[3]), 4),
            "se_crew_pts": round(float(se_ab[3]), 4),
            "d_spoiler_w": round(float(m_ab[4]), 4),
            "syn_crew_pts": round(float(syn_vec[3]), 4),
            "syn_moon_pct": round(float(syn_vec[2]), 4),
        })

    print("\n=== 3A. TOP 12 NOBEL x NOBEL PAIRS BY JOINT IMPACT & NON-ADDITIVE SYNERGY (Full - Without Both) ===")
    print(f"{'Pair':<13s} | {'Joint dCrew':>11s} {'(SE)':>6s} | {'AddSum':>8s} | {'Synergy I_AB':>12s} | {'Joint dSS2%':>11s} | {'Joint dMoon%':>12s}")
    print("-" * 88)
    nn_recs = [r for r in pair_records if r[0] == "NN"]
    nn_recs.sort(key=lambda r: abs(r[3][3]) + abs(r[5][3]), reverse=True)
    for _, a, b, m_ab, se_ab, syn_v in nn_recs[:12]:
        add_sum = m_ab[3] - syn_v[3]
        print(
            f"{a}+{b:<8s} | {m_ab[3]:+11.2f} ({se_ab[3]:4.2f}) | {add_sum:+8.2f} | {syn_v[3]:+12.2f} | "
            f"{m_ab[0]:+10.2f}% | {m_ab[2]:+11.2f}%"
        )

    print("\n=== 3B. TOP 12 BOSS/TRAP x BOSS/TRAP PAIRS (Pillar Bottlenecks & Compound Sinkholes) ===")
    print(f"{'Pair':<13s} | {'Joint dMoon%':>12s} | {'Syn dMoon%':>10s} | {'Joint dCrew':>11s} {'(SE)':>6s} | {'Syn dCrew':>10s} | {'Joint dSS2%':>11s}")
    print("-" * 88)
    th_recs = [r for r in pair_records if r[0] == "TH"]
    th_recs.sort(key=lambda r: abs(r[3][2]) + 0.35 * abs(r[3][3]), reverse=True)
    for _, a, b, m_ab, se_ab, syn_v in th_recs[:12]:
        print(
            f"{a}+{b:<8s} | {m_ab[2]:+11.2f}% | {syn_v[2]:+9.2f}% | {m_ab[3]:+11.2f} ({se_ab[3]:4.2f}) | "
            f"{syn_v[3]:+10.2f} | {m_ab[0]:+10.2f}%"
        )

    print("\n=== 3C. SHIELD vs. BOSS COUNTER PAIRS (Removing Both Nobel Shield & Target Boss Together) ===")
    print(f"{'Pair':<13s} | {'Net dCrewPts':>12s} {'(SE)':>6s} | {'Net dMoon%':>10s} | {'Net dSS2%':>9s} | {'Interaction I_AB':>16s}")
    print("-" * 78)
    nh_recs = [r for r in pair_records if r[0] == "NH"]
    for _, a, b, m_ab, se_ab, syn_v in nh_recs:
        print(
            f"{a}+{b:<8s} | {m_ab[3]:+12.2f} ({se_ab[3]:4.2f}) | {m_ab[2]:+9.2f}% | {m_ab[0]:+8.2f}% | "
            f"{syn_v[3]:+16.2f}"
        )

    out_csv = ROOT / "output" / "thn_card_power_and_pairs.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\n[OK] Exported {len(csv_rows)} single & pairwise ablation rows -> {out_csv.relative_to(ROOT)}")


if __name__ == "__main__":
    main()