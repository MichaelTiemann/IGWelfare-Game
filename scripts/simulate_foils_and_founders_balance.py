#!/usr/bin/env python3
"""
Foils & Founders: 20-Turn Coopetitive Monte Carlo Balance Simulator (v2026.11e)
================================================================================
Evaluates:
  1. +3 Mana Inverse-Hub Royalty + Waka Mataika Pioneer Bonus for Hub Builders
  2. 2-Turn "Use-It-Or-Lose-It" Manaaki Decay (0 staked & 0 earned for 2 turns -> -1 Mana)
  3. "Shooting the Moon" Plutocrat Gambit driven by actual drawn T:00-T:10, H:01-H:10, & P:06 cards:
       - Exact Capture Pillars (1..4), feral_kickback_wealth (2W..4W), & synergy_links Judo-Counters
       - Strategic Ambiguity (Turns 1-5 seed-capital skim vs. Turn 6-8 reformer pivot)
       - Global Market D20 Contagion (Davos tail-risk margin calls on concentrated wealth)
  4. 100-Card Tranche Play Shoe (6x B:01, 3x B:02, 7x B:03, 3x B:04, 3x B:05, 4x B:06) + Coasian Trading
  5. Full Suite N (N:01-N:09), Suite T (T:00-T:10), & Suite H (H:01-H:10) card-level operators,
     including N:07 (Milgrom-Wilson 2020 Combinatorial Package Clearinghouse & Amber Shock Core)
     and `excluded_cards` + Common Random Numbers (CRN) support for leave-k-out power ablations.

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Set, Tuple
import numpy as np

try:
    import yaml
except ImportError:
    yaml = None


TRANCHE_SCHEDULE: Tuple[float, float, float] = (0.50, 0.25, 0.25)
CARD_TO_SLOT: Dict[str, str] = {
    "B:01": "G12_TAMARIKI",
    "B:02": "G12_TAMARIKI",
    "B:03": "G3_MENTOR",
    "B:04": "G4_LAUNCH",
    "B:05": "G4_LAUNCH",
    "B:06": "G5_GRANT",
}
LIFECYCLE_SLOTS: Tuple[str, ...] = ("G12_TAMARIKI", "G3_MENTOR", "G4_LAUNCH", "G5_GRANT")
DEFAULT_TRANCHE_COPIES: Dict[str, int] = {
    "B:01": 6,
    "B:02": 3,
    "B:03": 7,
    "B:04": 3,
    "B:05": 3,
    "B:06": 4,
}

NOBEL_IDS: Tuple[str, ...] = tuple(f"N:0{i}" for i in range(1, 10))
TRAP_IDS: Tuple[str, ...] = tuple(f"T:{i:02d}" for i in range(0, 11))
BOSS_IDS: Tuple[str, ...] = tuple(f"H:{i:02d}" for i in range(1, 11))

# Exact Capture Pillar (0-indexed 0..3 matching Pillars 1..4 in plutocrats_crown_and_davos.md),
# feral_kickback_wealth (2W..4W), and Nobel/River Judo-counter links:
BOSS_TRAP_META: Dict[str, Tuple[int, float, Tuple[str, ...]]] = {
    # Pillar 1 (idx 0): Narrative & Short-Termism — cleared by Bay 3 (Rear T-Foil)
    "T:00": (0, 2.0, ("N:02", "B:09")),
    "T:01": (0, 3.0, ("C:05", "N:04")),
    "T:04": (0, 4.0, ("N:01", "N:07", "B:09")),
    "T:07": (0, 4.0, ("B:09", "N:04", "N:07")),
    "H:01": (0, 3.0, ("B:09", "N:04")),
    "H:02": (0, 3.0, ("N:02", "N:05")),
    # Pillar 2 (idx 1): Land Hoarding & Cartels — cleared by Bay 2 (Wing-Sail)
    "T:05": (1, 4.0, ("B:08", "N:06")),
    "T:08": (1, 3.0, ("B:08", "N:05")),
    "T:10": (1, 4.0, ("B:08", "N:04")),
    "H:07": (1, 4.0, ("B:08", "N:07")),
    "H:08": (1, 4.0, ("C:08", "E:01", "N:07")),
    # Pillar 3 (idx 2): Family & Wage Squeeze — cleared by Bay 1 (Front Lifting Foil)
    "T:02": (2, 3.0, ("B:01", "N:03", "N:08")),
    "T:03": (2, 3.0, ("B:10", "N:04", "N:07")),
    "T:09": (2, 3.0, ("B:01", "B:08", "N:08")),
    "H:03": (2, 3.0, ("B:01", "N:03")),
    "H:05": (2, 3.0, ("B:15", "N:08")),
    "H:06": (2, 3.0, ("B:08", "N:02", "N:07")),
    # Pillar 4 (idx 3): Offshore Escape & External Shocks — NEVER cleared by a single Bay!
    "T:06": (3, 3.0, ("C:06", "N:07")),
    "H:04": (3, 4.0, ("B:06", "B:08")),
    "H:09": (3, 4.0, ("E:03", "N:07")),
    "H:10": (3, 3.0, ("B:03", "N:03", "N:07")),
    "P:06": (3, 4.0, ("E:03", "N:05")),
}

CONSTRUCTIVE_TRACKED: Set[str] = (
    set(DEFAULT_TRANCHE_COPIES)
    | set(NOBEL_IDS)
    | {"B:08", "B:09", "B:10", "B:15", "C:05", "C:06", "C:08", "E:01", "E:02", "E:03"}
)


@dataclass
class SimConfig:
    n_games: int = 5_000
    n_turns: int = 20
    n_players: int = 4
    normalized_scaling: bool = True
    tranche_deck_enabled: bool = True
    coasian_trading_enabled: bool = True
    era_backlog: float = 1.0        # psi_backlog: 1/16 (1972) -> 1/4 (1995) -> 1.0 (2026 Master)
    excluded_cards: FrozenSet[str] = frozenset()
    seed_mana: float = 3.0
    hub_royalty_mana: float = 3.0
    bridge_royalty_mana: float = 2.5
    idle_mana_limit: int = 2
    idle_mana_decay: float = 1.0
    abolish_impossible_bonus: float = 5.0
    bystander_forfeit_ss1: float = 2.0
    bystander_forfeit_ss2: float = 3.0
    feral_backfire_forfeit: float = 2.0
    watchdog_block_mana: float = 1.0
    tier_mana: Tuple[float, float, float] = (1.0, 2.1, 4.6)
    pillar_attempt_probs: Tuple[float, float, float, float] = (0.52, 0.44, 0.62, 0.80)
    pillar_passive_rents: Tuple[float, float, float, float, float] = (0.0, 0.55, 1.45, 3.10, 5.20)
    crew_base_shield: float = 0.76
    governance_erosion_per_pillar: float = 0.16
    global_wealth_threshold: float = 26.0
    finland_start: float = 88.0
    nz_start: float = 81.0
    rng_seed: int = 20261028


@dataclass
class PlayerState:
    strategy: str
    mana: float
    wealth: float
    kickback_wealth: float = 0.0
    capture_pillars: Set[int] = field(default_factory=set)
    vault_cards: List[str] = field(default_factory=list)
    boss_hand: List[str] = field(default_factory=list)
    idle_mana_turns: int = 0
    init_mana: float = 0.0
    royalty_mana: float = 0.0
    legacy_mana: float = 0.0
    forfeit_mana: float = 0.0
    decay_mana_lost: float = 0.0
    contagion_hits: int = 0
    river_tiers_enacted: List[int] = field(default_factory=list)
    ages: List[int] = field(default_factory=lambda: [12, 1])
    struggling_flags: List[bool] = field(default_factory=lambda: [False, False])
    exiled_flags: List[bool] = field(default_factory=lambda: [False, False])
    hand: List[str] = field(default_factory=list)
    slot_stacks: Dict[str, int] = field(default_factory=lambda: {s: 0 for s in LIFECYCLE_SLOTS})
    had_turn1_tamariki: bool = False
    got_gate12_in_time: bool = False
    compass_peeks: int = 0
    pdsa_bonus: float = 0.0
    exergy_unlocked: bool = False
    slot3_unlocked: bool = False
    trades_made: int = 0


def load_deck_counts_from_yaml(repo_root: Optional[Path] = None, singleton_override: bool = False) -> Dict[str, int]:
    """Loads Play-Shoe multiplicities (excluding T & H Boss/Trap cards, which populate boss_shoe)."""
    if singleton_override:
        base = {cid: 1 for cid in CONSTRUCTIVE_TRACKED}
        base["OTHER"] = 33
        return base

    root = repo_root or Path(__file__).resolve().parents[1]
    cards_yaml = root / "decks" / "cards.yaml"
    if yaml is not None and cards_yaml.exists():
        data = yaml.safe_load(cards_yaml.read_text(encoding="utf-8")) or {}
        cards = data.get("cards", [])
        if cards:
            counts: Dict[str, int] = {"OTHER": 0}
            for c in cards:
                cid = str(c.get("id", "")).strip()
                if cid in BOSS_TRAP_META or cid in ("B:00", "B:16", "K:10"):
                    continue  # T/H/P:06 go to Boss/Trap shoe; B:00 is D20; B:16/K:10 sit on board
                n_cop = max(1, int(c.get("copies", 1)))
                if cid in CONSTRUCTIVE_TRACKED:
                    counts[cid] = counts.get(cid, 0) + n_cop
                else:
                    counts["OTHER"] += n_cop
            return counts

    fallback = {cid: 1 for cid in CONSTRUCTIVE_TRACKED}
    fallback.update(DEFAULT_TRANCHE_COPIES)
    fallback["OTHER"] = 33
    return fallback


def slot_coverage(stacks: int, singleton_mode: bool) -> float:
    if stacks <= 0:
        return 0.0
    if singleton_mode:
        return 1.0
    return float(sum(TRANCHE_SCHEDULE[: min(3, stacks)]))


def slot_marginal_gain(stacks: int, singleton_mode: bool) -> float:
    if singleton_mode:
        return 1.0 if stacks == 0 else 0.0
    return TRANCHE_SCHEDULE[stacks] if stacks < 3 else 0.0


def draw_from_shoe(rng: np.random.Generator, shoe: List[str], discard: List[str], n: int) -> List[str]:
    out: List[str] = []
    for _ in range(n):
        if not shoe and discard:
            shoe.extend(discard)
            discard.clear()
            rng.shuffle(shoe)
        if shoe:
            out.append(shoe.pop())
    return out


def roll_d20_birth(
    rng: np.random.Generator,
    front_foil_active: bool,
    guinz_drift: bool = True,
    era_backlog: float = 1.0,
) -> Tuple[float, bool]:
    roll = int(rng.integers(1, 21))
    base_cut = 6 if guinz_drift else 4
    corner_cutoff = max(1, int(round(base_cut * (0.25 + 0.75 * era_backlog))))
    if roll <= corner_cutoff:
        if not front_foil_active:
            return 0.5, True
        return 1.5, False
    elif roll <= 12:
        return 2.0 if front_foil_active else 1.0, False
    elif roll <= 18:
        return 3.0 if front_foil_active else 2.0, False
    else:
        return 4.0 if front_foil_active else 2.5, False


def compute_lead_dynamics(traj: np.ndarray) -> Dict[str, float | List[float]]:
    n_t, _ = traj.shape
    leaders = np.argmax(traj, axis=1)
    sorted_scores = np.sort(traj, axis=1)
    margins = sorted_scores[:, -1] - sorted_scores[:, -2]
    denom = np.maximum(1.0, np.mean(np.maximum(0.0, traj), axis=1))
    gap_integral = float(np.mean(margins / denom))

    lead_changes = 0
    swing_integral = 0.0
    reigns: List[int] = []
    cur_reign = 1

    for t in range(1, n_t):
        prev_l, curr_l = int(leaders[t - 1]), int(leaders[t])
        if curr_l != prev_l:
            lead_changes += 1
            reigns.append(cur_reign)
            cur_reign = 1
            deficit_closed = max(0.0, float(traj[t - 1, prev_l] - traj[t - 1, curr_l]))
            new_margin = max(0.0, float(traj[t, curr_l] - traj[t, prev_l]))
            swing_integral += deficit_closed + new_margin
        else:
            cur_reign += 1
    reigns.append(cur_reign)

    mid_idx = min(9, n_t - 1)
    turn10_holds = float(leaders[mid_idx] == leaders[-1])
    era_slices = [leaders[:6], leaders[6:13], leaders[13:]]
    era_leaders = [int(np.bincount(es, minlength=traj.shape[1]).argmax()) for es in era_slices]

    return {
        "gap_integral": gap_integral,
        "swing_integral": swing_integral,
        "raw_margin_integral": float(np.sum(margins)),
        "lead_changes": float(lead_changes),
        "mean_reign": float(np.mean(reigns)),
        "turn10_holds": turn10_holds,
        "era_leaders": era_leaders,
    }


def simulate_single_game(
    rng: Optional[np.random.Generator],
    cfg: SimConfig,
    strategies: List[str],
    table_mode: str = "mixed",
    deck_counts: Optional[Dict[str, int]] = None,
    game_seed: Optional[int] = None,
) -> Dict[str, float | List[float]]:
    """
    Runs a single 20-turn game. When `game_seed` is supplied, separates `rng_deals` (card shuffles)
    from `rng_rolls` (D20 births, macro shocks, and AI rolls) for low-variance CRN ablations.
    """
    if game_seed is not None:
        ss = np.random.SeedSequence(game_seed)
        s_deals, s_rolls = ss.spawn(2)
        rng_deals = np.random.default_rng(s_deals)
        rng_rolls = np.random.default_rng(s_rolls)
    else:
        assert rng is not None
        rng_deals = rng
        rng_rolls = rng

    n_p = len(strategies)
    singleton_mode = not cfg.tranche_deck_enabled
    excl = cfg.excluded_cards
    psi = cfg.era_backlog

    raw_counts = deck_counts or load_deck_counts_from_yaml(singleton_override=singleton_mode)
    counts = {cid: cnt for cid, cnt in raw_counts.items() if cid not in excl}

    shoe = [cid for cid, cnt in counts.items() for _ in range(cnt)]
    rng_deals.shuffle(shoe)
    discard: List[str] = []

    # Build Boss & Trap Shoe (`T:00-T:10`, `H:03-H:10`, `P:06`), while `H:01` & `H:02` start in Orthodoxy Row
    active_hazards: Set[str] = set()
    orthodoxy_row_avail: Set[str] = set()
    for start_h in ("H:01", "H:02"):
        if start_h not in excl:
            active_hazards.add(start_h)
            orthodoxy_row_avail.add(start_h)
    # H:03 GUiNZ modern hardship baseline active unless excluded or playing 1972 low-backlog mode
    guinz_active = ("H:03" not in excl) and (psi >= 0.5)

    boss_shoe = [cid for cid in BOSS_TRAP_META if cid not in excl and cid not in ("H:01", "H:02")]
    rng_deals.shuffle(boss_shoe)
    boss_discard: List[str] = []

    # Enacted persistent River commons (`N:01-N:09`, `B:08`, `B:09`, `C:05`, `C:06`, `C:08`, `E:01-E:03`, etc.)
    enacted_river: Set[str] = set()
    amber_saves = 0
    h09_survived = False

    players: List[PlayerState] = []
    for s in strategies:
        w0, struggling = roll_d20_birth(rng_rolls, front_foil_active=False, guinz_drift=guinz_active, era_backlog=psi)
        p_init = PlayerState(strategy=s, mana=cfg.seed_mana, wealth=w0 * 2.0, struggling_flags=[False, struggling])
        p_init.hand.extend(draw_from_shoe(rng_deals, shoe, discard, 5))
        p_init.had_turn1_tamariki = any(c in ("B:01", "B:02", "B:03") for c in p_init.hand)
        if s == "feral_spoiler":
            p_init.boss_hand.extend(draw_from_shoe(rng_deals, boss_shoe, boss_discard, 3))
        players.append(p_init)

    river_cards = draw_from_shoe(rng_deals, shoe, discard, 4)

    subsystems_done = [False, False, False]  # [Bay 1 Front Foil, Bay 2 Wing-Sail, Bay 3 Rear T-Foil]
    ss_regime = 0
    ss2_turn = cfg.n_turns + 1
    total_trades = 0

    finland_cohesion = cfg.finland_start
    nz_cohesion = cfg.nz_start + (8.0 * (1.0 - psi))

    if cfg.normalized_scaling:
        base_drag_cost = 1.5 if n_p == 2 else (2.0 if n_p <= 4 else 3.0)
        self_combo_allowed = (n_p == 2)
        river_visibility_boost = 1.15 if n_p == 2 else (0.90 if n_p >= 5 else 1.0)
    else:
        base_drag_cost = 2.0
        self_combo_allowed = False
        river_visibility_boost = 0.72 if n_p == 2 else (1.28 if n_p >= 5 else 1.0)

    mana_traj: List[List[float]] = []
    wealth_traj: List[List[float]] = []

    for turn in range(1, cfg.n_turns + 1):
        front_foil, wing_sail, rear_foil = subsystems_done
        mana_active_this_turn = [False] * n_p
        mean_wealth = float(np.mean([x.wealth for x in players]))

        # Dynamic Nobel River modifiers
        n02_coase = "N:02" in enacted_river
        n03_heckman = "N:03" in enacted_river
        n04_williamson = "N:04" in enacted_river
        n05_ostrom = "N:05" in enacted_river
        n06_romer = "N:06" in enacted_river
        n07_milgrom = "N:07" in enacted_river
        n08_doepke = "N:08" in enacted_river
        n09_medallion = "N:09" in enacted_river

        royalty_cap = 3 if n06_romer else 2
        h02_drag = 0.35 * psi if ("H:02" in active_hazards and not (n02_coase or n05_ostrom)) else 0.0
        drag_cost = max(0.8, base_drag_cost + h02_drag - (0.50 if n02_coase else 0.0))

        # --- BOARD HEADWIND DRAW (Mode A / Shared Macro Environment) ---
        if turn % 2 == 1 and boss_shoe:
            drawn_h = draw_from_shoe(rng_deals, boss_shoe, boss_discard, 1)[0]
            active_hazards.add(drawn_h)
            # Immediate board shock pulses for specific T/H cards (scaled by psi_backlog)
            if drawn_h == "T:01" and "C:05" not in enacted_river:
                nz_cohesion = max(60.0, nz_cohesion - 2.4 * psi)
            elif drawn_h == "T:03" and not ("B:10" in enacted_river or n04_williamson):
                nz_cohesion = max(60.0, nz_cohesion - 1.5 * psi)
                for px in players:
                    if px.strategy != "feral_spoiler":
                        loss_m = min(px.mana, 1.0 * psi)
                        px.mana -= loss_m
                        px.forfeit_mana += loss_m
            elif drawn_h == "H:09":
                if ss_regime == 2 or ("E:03" in enacted_river and n07_milgrom):
                    h09_survived = True
                else:
                    nz_cohesion = max(60.0, nz_cohesion - 2.2 * psi)
                    for px in players:
                        px.wealth = max(0.0, px.wealth - 0.85 * psi)
            # Recycle drawn card back into boss_discard so Spoiler can also encounter it later
            boss_discard.append(drawn_h)

        # --- PHASE 0: Shoe Draw, River Turnover, & Coasian / Milgrom Tranche Clearing ---
        for p in players:
            p.hand.extend(draw_from_shoe(rng_deals, shoe, discard, 1))
            if p.strategy == "feral_spoiler":
                p.boss_hand.extend(draw_from_shoe(rng_deals, boss_shoe, boss_discard, 1))

        t00_stall = ("T:00" in active_hazards) and not (n02_coase or rear_foil)
        if river_cards and not (t00_stall and turn % 2 == 0):
            discard.append(river_cards.pop(0))
            river_cards.extend(draw_from_shoe(rng_deals, shoe, discard, 1))

        # Constructive River Draft (prioritizes needed Gate tranches, N:07, N:01-N:08, B:09, B:08, E:01)
        for p in players:
            if p.strategy in ("bystander", "feral_spoiler"):
                continue
            best_rc, best_val = None, 0.0
            for rc in river_cards:
                sl = CARD_TO_SLOT.get(rc)
                if sl is not None:
                    val = slot_marginal_gain(p.slot_stacks[sl], singleton_mode)
                elif rc in NOBEL_IDS and rc not in enacted_river:
                    val = 0.48 if rc in ("N:07", "N:03", "N:04", "N:06") else 0.42
                elif rc == "B:09" and "B:09" not in enacted_river and turn <= 8:
                    val = 0.47
                elif rc in ("B:08", "E:01", "C:06", "C:08") and rc not in enacted_river:
                    val = 0.38
                else:
                    val = 0.0
                if val > best_val:
                    best_rc, best_val = rc, val
            if best_rc is not None and best_val >= 0.25:
                river_cards.remove(best_rc)
                p.hand.append(best_rc)
                river_cards.extend(draw_from_shoe(rng_deals, shoe, discard, 1))

        # Endogenous Coasian Trading + N:07 Combinatorial Clearing (1.0W ransom cap + 3-way clearing)
        if cfg.coasian_trading_enabled and not singleton_mode:
            spoiler_price = 1.0 if n07_milgrom else 1.8
            for a_i, sa in enumerate(players):
                if sa.strategy == "bystander":
                    continue
                for b_i, sb in enumerate(players):
                    if a_i == b_i or sb.strategy in ("bystander", "feral_spoiler"):
                        continue
                    for c_a in list(sa.hand):
                        sla = CARD_TO_SLOT.get(c_a)
                        if sla is None:
                            continue
                        a_is_spoiler = sa.strategy == "feral_spoiler"
                        a_surplus = (
                            a_is_spoiler
                            or sa.slot_stacks[sla] >= 1
                            or sum(CARD_TO_SLOT.get(x) == sla for x in sa.hand) >= 2
                        )
                        b_empty = (sb.slot_stacks[sla] == 0) and not any(CARD_TO_SLOT.get(x) == sla for x in sb.hand)
                        if not (a_surplus and b_empty):
                            continue

                        swapped = False
                        if not a_is_spoiler:
                            for c_b in list(sb.hand):
                                slb = CARD_TO_SLOT.get(c_b)
                                if slb is not None and slb != sla:
                                    b_surp = sb.slot_stacks[slb] >= 1 or sum(CARD_TO_SLOT.get(x) == slb for x in sb.hand) >= 2
                                    a_emp = (sa.slot_stacks[slb] == 0) and not any(CARD_TO_SLOT.get(x) == slb for x in sa.hand)
                                    if b_surp and a_emp:
                                        sa.hand.remove(c_a)
                                        sb.hand.remove(c_b)
                                        sa.hand.append(c_b)
                                        sb.hand.append(c_a)
                                        swap_m = 0.65 if n07_milgrom else 0.50
                                        sa.mana += swap_m
                                        sb.mana += swap_m
                                        sa.royalty_mana += swap_m
                                        sb.royalty_mana += swap_m
                                        mana_active_this_turn[a_i] = True
                                        mana_active_this_turn[b_i] = True
                                        sa.trades_made += 1
                                        sb.trades_made += 1
                                        total_trades += 1
                                        swapped = True
                                        break
                        price = spoiler_price if a_is_spoiler else (0.95 if n07_milgrom else 1.1)
                        if not swapped and sb.wealth >= price + 1.0:
                            sa.hand.remove(c_a)
                            sb.hand.append(c_a)
                            sb.wealth -= price
                            sa.wealth += price
                            if a_is_spoiler:
                                if not n07_milgrom:
                                    sa.kickback_wealth += 0.8
                            else:
                                sa.mana += 0.7
                                sa.royalty_mana += 0.7
                                mana_active_this_turn[a_i] = True
                            sa.trades_made += 1
                            sb.trades_made += 1
                            total_trades += 1
                        break

        # --- N:08 DOEPKE-KINDERMANN 3RD WHĀNAU SLOT UNLOCK ---
        t09_delay = 2 if ("T:09" in active_hazards and not wing_sail) else 0
        if n08_doepke and ("B:15" in enacted_river or ss_regime == 2) and turn >= (6 + t09_delay):
            for px in players:
                if px.strategy != "feral_spoiler" and not px.slot3_unlocked:
                    px.slot3_unlocked = True
                    px.ages.append(0)
                    px.struggling_flags.append(False)
                    px.exiled_flags.append(False)
                    px.mana += 1.5
                    px.legacy_mana += 1.5

        # --- PHASE I: Aging, H:04 Brain-Drain Check, Rebirth, & Ongoing T/H/N Earnings ---
        for p in players:
            g12_cov = slot_coverage(p.slot_stacks["G12_TAMARIKI"], singleton_mode)
            g3_cov = slot_coverage(p.slot_stacks["G3_MENTOR"], singleton_mode)
            g4_cov = slot_coverage(p.slot_stacks["G4_LAUNCH"], singleton_mode)
            g5_cov = slot_coverage(p.slot_stacks["G5_GRANT"], singleton_mode)

            for c_idx in range(len(p.ages)):
                p.ages[c_idx] += 1
                # Repatriate exiled Sydney graduate once Wing-Sail (B:06 + B:08) locks
                if p.exiled_flags[c_idx] and (wing_sail or ("B:08" in enacted_river and g5_cov >= 0.50)):
                    p.exiled_flags[c_idx] = False

                # Age 21 (age == 7): H:04 Brain-Drain Vortex & H:10 LVR/Unmentored Cliff
                if p.ages[c_idx] == 7 and not wing_sail:
                    if "H:04" in active_hazards and g5_cov < 0.50 and "B:08" not in enacted_river:
                        if int(rng_rolls.integers(1, 21)) <= max(1, int(round(5 * psi))):
                            p.exiled_flags[c_idx] = True
                    cliff_shield = min(1.0, 0.5 * (g3_cov + g5_cov))
                    if rng_rolls.random() < 0.22 * psi * (1.0 - 0.75 * cliff_shield):
                        p.wealth = max(0.0, p.wealth - 1.4)

                if p.ages[c_idx] >= 30:
                    p.ages[c_idx] = 0
                    p.exiled_flags[c_idx] = False
                    _, is_st = roll_d20_birth(
                        rng_rolls,
                        front_foil_active=(front_foil or g12_cov >= 0.50),
                        guinz_drift=guinz_active,
                        era_backlog=psi,
                    )
                    p.struggling_flags[c_idx] = is_st

            adult_count = sum(1 for a, ex in zip(p.ages, p.exiled_flags) if a >= 6 and not ex)
            if p.strategy == "feral_spoiler":
                z_mult = 0.55 if (wing_sail and len(p.capture_pillars) < 3) else 1.15
                # Active rentier siphons from T:05, T:06, T:10, H:07, H:08 before Bay 2 / counters lock
                if not wing_sail:
                    if "T:05" in active_hazards:
                        p.wealth += 0.35 * psi
                    if "H:07" in active_hazards and "B:08" not in enacted_river:
                        p.wealth += 0.40 * psi
                    if "T:10" in active_hazards:
                        p.wealth += 0.45 * psi
                if "H:08" in active_hazards and "C:08" not in enacted_river and not n07_milgrom:
                    p.wealth += 0.35 * psi
                if "T:06" in active_hazards and "C:06" not in enacted_river and not n07_milgrom:
                    p.wealth += 0.35 * psi
            else:
                tranche_lift = 0.12 * (g4_cov + g5_cov)
                romer_lift = 0.16 if n06_romer else 0.0
                t05_drag = 0.09 * psi if ("T:05" in active_hazards and not wing_sail) else 0.0
                z_mult = max(0.5, 1.0 + (0.45 if wing_sail else 0.0) + (0.45 if rear_foil else 0.0) + tranche_lift + romer_lift - t05_drag)
                hardship_penalty = (0.5 + 0.5 * g12_cov) if (any(p.struggling_flags) and not front_foil) else 1.0
                exergy_div = 0.38 if p.exergy_unlocked else 0.0
                p.wealth += adult_count * 1.25 * z_mult * hardship_penalty + exergy_div

                # Ongoing T/H structural headwind drags when uncountered
                if "H:05" in active_hazards and "B:15" not in enacted_river and not rear_foil:
                    p.wealth = max(0.0, p.wealth - 0.30 * psi)
                if "H:07" in active_hazards and not wing_sail and "B:08" not in enacted_river:
                    p.wealth = max(0.0, p.wealth - 0.25 * psi)
                if "H:08" in active_hazards and "C:08" not in enacted_river and not p.exergy_unlocked:
                    p.wealth = max(0.0, p.wealth - 0.25 * psi)
                if "T:06" in active_hazards and "C:06" not in enacted_river and not n07_milgrom:
                    p.wealth = max(0.0, p.wealth - 0.22 * psi)
                if "T:09" in active_hazards and not wing_sail and not n08_doepke:
                    p.wealth = max(0.0, p.wealth - 0.20 * psi)
                if "T:02" in active_hazards and p.strategy == "finisher" and not front_foil:
                    p.wealth = max(0.0, p.wealth - 0.30 * psi)

        # --- PHASE II: Card Execution (Incl. N:07 Atomic 2-Card Package Play!) & Domino Capture ---
        for p_i, p in enumerate(players):
            k = len(p.capture_pillars)

            # 1. Strategic Ambiguity (Turns 1-5): Skim 1 available Pillar 1/2 card if present
            if (
                k == 0
                and turn <= 5
                and p.strategy in ("finisher", "shielded_arb", "feral_spoiler")
                and rng_rolls.random() < (cfg.pillar_attempt_probs[0] if p.strategy == "feral_spoiler" else 0.26)
            ):
                skim_pool = (p.boss_hand + sorted(orthodoxy_row_avail)) if p.strategy == "feral_spoiler" else (boss_shoe + sorted(orthodoxy_row_avail))
                cand = [c for c in skim_pool if BOSS_TRAP_META[c][0] in (0, 1)]
                if cand:
                    chosen_c = cand[0]
                    if chosen_c in orthodoxy_row_avail:
                        orthodoxy_row_avail.discard(chosen_c)
                    elif p.strategy == "feral_spoiler":
                        p.boss_hand.remove(chosen_c)
                    else:
                        boss_shoe.remove(chosen_c)
                    pil_idx, kb_w, _ = BOSS_TRAP_META[chosen_c]
                    p.capture_pillars.add(pil_idx)
                    p.vault_cards.append(chosen_c)
                    active_hazards.add(chosen_c)
                    p.wealth += 2.0
                    if p.strategy == "feral_spoiler":
                        p.kickback_wealth += kb_w * 0.5
                        p.wealth += cfg.pillar_passive_rents[len(p.capture_pillars)]
                        continue

            # 2. Reformer Mid-Game Pivot (Turns 6-8)
            if k == 1 and turn in (6, 7, 8) and p.strategy in ("finisher", "shielded_arb"):
                p.capture_pillars.clear()
                p.vault_cards.clear()
                p.wealth += 1.5
                p.mana += 1.5
                p.init_mana += 1.5
                mana_active_this_turn[p_i] = True

            # 3. Constructive Hand/River Execution (1 action normally; UP TO 2 atomic package plays if N:07 is live!)
            if p.strategy in ("hub_builder", "shielded_arb", "constructive") or (p.strategy == "finisher" and turn >= 5):
                max_plays = 2 if (n07_milgrom and p.wealth >= 1.6) else 1
                played_any = False

                for play_step in range(max_plays):
                    pkg_disc = 0.25 if play_step == 1 else 0.0
                    has_kaumatua = any(a >= 21 for a in p.ages)
                    nobel_cost = 0.0 if (p.strategy == "hub_builder" and has_kaumatua) else max(0.0, 0.55 - pkg_disc)

                    # Priority A: Needed Lifecycle Gate Tranches
                    best_card, best_gain = None, 0.0
                    for hc in p.hand:
                        sl = CARD_TO_SLOT.get(hc)
                        if sl is not None:
                            urg = 1.35 if (sl in ("G12_TAMARIKI", "G3_MENTOR") and turn <= 5) else 1.0
                            g = slot_marginal_gain(p.slot_stacks[sl], singleton_mode) * urg
                            if g > best_gain:
                                best_card, best_gain = hc, g

                    if best_card is not None and best_gain > 0 and p.wealth >= (0.6 - pkg_disc):
                        sl = CARD_TO_SLOT[best_card]
                        mg = slot_marginal_gain(p.slot_stacks[sl], singleton_mode)
                        p.hand.remove(best_card)
                        p.slot_stacks[sl] += 1
                        # H:06 Kaiako Urban Rent Squeeze dampens uncooled early tranche Mana slightly
                        h06_mult = 0.82 if ("H:06" in active_hazards and not wing_sail and "B:08" not in enacted_river) else 1.0
                        # H:10 Unmentored Grant Commutator Hazard if G5_GRANT > G3_MENTOR
                        if (
                            sl == "G5_GRANT"
                            and "H:10" in active_hazards
                            and p.slot_stacks["G5_GRANT"] > p.slot_stacks["G3_MENTOR"]
                            and not n03_heckman
                        ):
                            p.wealth = max(0.0, p.wealth - 1.2 * psi)
                            p.mana = max(0.0, p.mana - 0.8 * psi)
                        if sl in ("G12_TAMARIKI", "G3_MENTOR") and turn <= 5:
                            p.got_gate12_in_time = True
                            p.struggling_flags = [False] * len(p.ages)
                        tier_exposed = 0 if sl in ("G12_TAMARIKI", "G3_MENTOR") else 1
                        p.river_tiers_enacted.append(tier_exposed)
                        pioneer_bonus = 0.9 if (p.strategy == "hub_builder" and sl in ("G12_TAMARIKI", "G3_MENTOR")) else 0.0
                        p.mana += (1.8 * mg + pioneer_bonus) * h06_mult
                        p.init_mana += (1.8 * mg + pioneer_bonus) * h06_mult
                        p.wealth += 0.35
                        mana_active_this_turn[p_i] = True
                        played_any = True
                        continue

                    # Priority B: Enact Nobel Engine (N:01-N:09) or Key Structural Card (B:09, B:08, E:01-E:03, C:05-C:08)
                    special_candidates = [
                        hc for hc in p.hand
                        if (hc in NOBEL_IDS or hc in ("B:09", "B:08", "B:10", "B:15", "C:05", "C:06", "C:08", "E:01", "E:02", "E:03"))
                        and hc not in enacted_river
                        and (hc != "N:09" or (ss_regime >= 1 and sum(1 for nx in NOBEL_IDS[:8] if nx in enacted_river) >= 2))
                        and (hc != "B:15" or ss_regime >= 1)
                    ]
                    if special_candidates and p.wealth >= nobel_cost:
                        sc_id = special_candidates[0]
                        p.hand.remove(sc_id)
                        enacted_river.add(sc_id)
                        p.wealth = max(0.0, p.wealth - nobel_cost)
                        mana_active_this_turn[p_i] = True
                        played_any = True

                        if sc_id == "B:09":
                            active_hazards.discard("H:01")
                            orthodoxy_row_avail.discard("H:01")
                            if turn <= 8:
                                p.compass_peeks += 1
                                p.mana += 2.8
                                p.init_mana += 2.8
                            else:
                                p.mana += 2.5
                                p.init_mana += 2.5
                                p.exergy_unlocked = True
                        elif sc_id == "N:01":
                            p.pdsa_bonus = min(0.18, p.pdsa_bonus + 0.09)
                            p.mana += 1.6
                            p.init_mana += 1.6
                        elif sc_id == "N:02":
                            active_hazards.discard("H:02")
                            orthodoxy_row_avail.discard("H:02")
                            p.mana += 1.6
                            p.init_mana += 1.6
                        elif sc_id == "N:03":
                            p.mana += 1.9
                            p.init_mana += 1.9
                        elif sc_id == "N:04":
                            active_hazards.discard("H:01")
                            orthodoxy_row_avail.discard("H:01")
                            p.compass_peeks += 1
                            p.mana += 1.8
                            p.init_mana += 1.8
                        elif sc_id == "N:05":
                            active_hazards.discard("H:02")
                            orthodoxy_row_avail.discard("H:02")
                            p.mana += 1.9
                            p.init_mana += 1.9
                        elif sc_id == "N:06":
                            p.mana += 2.0
                            p.init_mana += 2.0
                        elif sc_id == "N:07":
                            n07_milgrom = True
                            p.mana += 2.2
                            p.init_mana += 2.2
                        elif sc_id == "N:08":
                            n08_doepke = True
                            p.mana += 1.8
                            p.init_mana += 1.8
                        elif sc_id == "N:09":
                            n09_medallion = True
                            p.mana += 4.5
                            p.legacy_mana += 4.5
                        elif sc_id in ("E:01", "E:02", "E:03"):
                            p.exergy_unlocked = True
                            p.wealth += 1.0
                            p.mana += 1.4
                            p.init_mana += 1.4
                        else:
                            # B:08, B:10, B:15, C:05, C:06, C:08
                            p.river_tiers_enacted.append(1)
                            p.mana += 1.6
                            p.init_mana += 1.6
                        continue
                    break

                if not played_any and rng_rolls.random() < (0.62 + p.pdsa_bonus):
                    if p.hand:
                        discard.append(p.hand.pop(0))
                    p.wealth += 1.0
                    tier_exposed = 0 if p.strategy == "hub_builder" and turn <= 8 else (1 if turn <= 12 else 2)
                    p.river_tiers_enacted.append(tier_exposed)
                    mana_active_this_turn[p_i] = True

            elif p.strategy == "feral_spoiler":
                if len(p.hand) > 5:
                    for hc in list(p.hand):
                        if hc not in CARD_TO_SLOT:
                            p.hand.remove(hc)
                            discard.append(hc)
                            break

                # Spoiler can ONLY capture missing Pillars for which they actually hold (or can draw) a matching T/H/P:06 card!
                avail_cards = [
                    c for c in (p.boss_hand + sorted(orthodoxy_row_avail))
                    if BOSS_TRAP_META[c][0] not in p.capture_pillars
                ]
                k_now = len(p.capture_pillars)
                lobby_cost = 1.15 * k_now
                if avail_cards and p.wealth >= lobby_cost:
                    attempt_p = cfg.pillar_attempt_probs[k_now]
                    if p.wealth > 1.20 * mean_wealth:
                        attempt_p = min(0.92, attempt_p + 0.06)

                    if rng_rolls.random() < attempt_p:
                        avail_cards.sort(key=lambda cx: (BOSS_TRAP_META[cx][0] == 3, BOSS_TRAP_META[cx][1]), reverse=True)
                        chosen_boss = avail_cards[0]
                        target_pillar, kb_val, counters = BOSS_TRAP_META[chosen_boss]
                        if chosen_boss in orthodoxy_row_avail:
                            orthodoxy_row_avail.discard(chosen_boss)
                        else:
                            p.boss_hand.remove(chosen_boss)
                        p.wealth -= lobby_cost

                        if k_now == 0:
                            p.capture_pillars.add(target_pillar)
                            p.vault_cards.append(chosen_boss)
                            active_hazards.add(chosen_boss)
                            p.wealth += 2.0
                            p.kickback_wealth += 2.0
                        else:
                            arb_indices = [
                                idx_x for idx_x, x in enumerate(players)
                                if x.strategy == "shielded_arb" and x.wealth >= 1.0 * k_now
                            ]
                            has_counter_on_river = any(cnt_c in enacted_river for cnt_c in counters)
                            base_block = cfg.crew_base_shield if arb_indices else 0.44
                            counter_bonus = 0.14 if has_counter_on_river else -0.08
                            effective_block = (
                                base_block
                                + counter_bonus
                                - cfg.governance_erosion_per_pillar * (k_now - 1)
                                + (0.18 if ss_regime == 2 else 0.0)
                            )
                            effective_block = float(np.clip(effective_block, 0.08, 0.90))

                            if rng_rolls.random() < effective_block:
                                boss_discard.append(chosen_boss)
                                if arb_indices:
                                    w_idx = arb_indices[0]
                                    players[w_idx].wealth = max(0.0, players[w_idx].wealth - 0.6 * k_now)
                                    players[w_idx].mana += cfg.watchdog_block_mana
                                    players[w_idx].init_mana += cfg.watchdog_block_mana
                                    mana_active_this_turn[w_idx] = True
                                loss = min(p.mana, cfg.feral_backfire_forfeit)
                                p.mana -= loss
                                p.forfeit_mana += loss
                            else:
                                p.capture_pillars.add(target_pillar)
                                p.vault_cards.append(chosen_boss)
                                active_hazards.add(chosen_boss)
                                p.wealth += lobby_cost + 0.6 * kb_val
                                p.kickback_wealth += kb_val

            if p.capture_pillars:
                rent = cfg.pillar_passive_rents[len(p.capture_pillars)]
                p.wealth += rent
                if p.strategy == "feral_spoiler":
                    p.kickback_wealth += 0.55 * rent

        # --- PHASE III: Subsystem Completions, T:07 Election Hazards, & N:07 Amber Stabiliser ---
        max_pillars_held = max((len(p.capture_pillars) for p in players), default=0)
        capture_turn_delay = 0 if max_pillars_held <= 1 else (1 if max_pillars_held == 2 else (3 if max_pillars_held == 3 else 5))
        capture_vis_mult = (
            1.0 if max_pillars_held <= 1 else (0.85 if max_pillars_held == 2 else (0.52 if max_pillars_held == 3 else 0.22))
        )
        if t00_stall:
            capture_vis_mult *= 0.88
        if n05_ostrom:
            capture_vis_mult = min(1.18, capture_vis_mult + 0.12)
        if n07_milgrom:
            capture_vis_mult = min(1.22, capture_vis_mult + 0.08)

        table_compass = sum(p.compass_peeks for p in players)
        n01_bonus = 2 if "N:01" in enacted_river else 0
        n04_shield = 2 if n04_williamson else 0
        h01_pen = 2 if ("H:01" in active_hazards and turn <= 8 and "B:09" not in enacted_river and not n04_williamson) else 0
        t04_pen = 3 if ("T:04" in active_hazards and turn <= 5 and "N:01" not in enacted_river) else 0
        t01_pen = 1 if ("T:01" in active_hazards and "C:05" not in enacted_river) else 0

        # Every-3rd-Turn T:07 Parliamentary Election Stability Check
        if turn % 3 == 0 and "T:07" not in excl:
            elec_roll = int(rng_rolls.integers(1, 21)) + 2 * table_compass + n04_shield - int(round((h01_pen + t04_pen + t01_pen) * psi))
            if elec_roll <= 5:
                if n07_milgrom and elec_roll >= 3:
                    # AMBER Two-Key Shock Stabiliser absorbs mid-low election wobble!
                    amber_saves += 1
                    for px in players:
                        if px.strategy != "feral_spoiler":
                            px.wealth = max(0.0, px.wealth - 0.35)
                else:
                    # 6-Yr Stop-Go Scissor-Blade Repeal!
                    nz_cohesion = max(65.0, nz_cohesion - 3.0 * psi)
                    for px in players:
                        if px.strategy != "feral_spoiler":
                            loss_e = min(px.mana, 1.4 * psi)
                            px.mana -= loss_e
                            px.forfeit_mana += loss_e

        for sub_idx in range(3):
            if not subsystems_done[sub_idx]:
                ready_turn = [2, 5, 9][sub_idx] + capture_turn_delay
                if sub_idx == 2 and (table_compass > 0 or n07_milgrom):
                    ready_turn = max(5, ready_turn - 1)  # Plan A Star-Compass / Clearinghouse acceleration!
                if table_mode == "hoarders":
                    ready_turn += 4
                elif table_mode == "bystanders":
                    ready_turn += 9

                if turn >= ready_turn and rng_rolls.random() < min(0.94, 0.52 * river_visibility_boost * capture_vis_mult):
                    weights = np.array([
                        3.4 if p.strategy == "hub_builder" and sub_idx == 0 else
                        3.4 if p.strategy == "finisher" and sub_idx >= 1 else
                        (2.8 + 0.6 * p.compass_peeks) if p.strategy == "shielded_arb" else
                        (2.2 if p.strategy == "constructive" else 0.10)
                        for p in players
                    ])
                    weights /= weights.sum()
                    init_idx = int(rng_rolls.choice(n_p, p=weights))
                    initiator = players[init_idx]
                    mana_active_this_turn[init_idx] = True

                    d20_hazard = int(rng_rolls.integers(1, 21)) + 3 * initiator.compass_peeks + n01_bonus + n04_shield - h01_pen
                    vuln_cutoff = int(round((6 if not front_foil else (4 if (turn % 3 == 0 and not rear_foil) else 2)) * (0.35 + 0.65 * psi)))
                    amber_rescued = n07_milgrom and (d20_hazard >= vuln_cutoff - 3) and initiator.wealth >= 0.5
                    saved_by_window = (table_mode in ("mixed", "balanced")) and (rng_rolls.random() < (0.84 if psi >= 0.8 else 0.94))

                    if d20_hazard > vuln_cutoff or amber_rescued or saved_by_window:
                        if amber_rescued and d20_hazard <= vuln_cutoff:
                            initiator.wealth = max(0.0, initiator.wealth - 0.4)
                            amber_saves += 1

                        subsystems_done[sub_idx] = True
                        n_done = sum(subsystems_done)

                        # One-Time Legislative Reset strips Pillar 3 (idx 2), Pillar 2 (idx 1), or Pillar 1 (idx 0) if <4 Pillars held!
                        stripped_pillar = 2 if sub_idx == 0 else (1 if sub_idx == 1 else 0)
                        for sp in players:
                            if len(sp.capture_pillars) < 4 and stripped_pillar in sp.capture_pillars:
                                sp.capture_pillars.discard(stripped_pillar)
                                sp.vault_cards = [vc for vc in sp.vault_cards if BOSS_TRAP_META[vc][0] != stripped_pillar]

                        mu = 1.25 if n_done == 1 else (1.75 if n_done == 2 else 2.20)
                        if n_done == 2:
                            ss_regime = 1
                        elif n_done == 3:
                            ss_regime = 2
                            ss2_turn = min(ss2_turn, turn)

                        init_card_mana = cfg.tier_mana[sub_idx] + (1.5 if (sub_idx == 0 and n03_heckman) else 0.0)
                        combo_sum = init_card_mana + cfg.tier_mana[0] + cfg.tier_mana[min(2, sub_idx)]
                        initiator.mana += mu * combo_sum
                        initiator.init_mana += mu * combo_sum
                        initiator.wealth = max(0.0, initiator.wealth - drag_cost)

                        if sub_idx == 0:
                            initiator.mana += cfg.abolish_impossible_bonus
                            initiator.legacy_mana += cfg.abolish_impossible_bonus

                        for other_idx, other in enumerate(players):
                            if other_idx == init_idx:
                                if self_combo_allowed and initiator.river_tiers_enacted:
                                    initiator.mana += cfg.hub_royalty_mana
                                    initiator.royalty_mana += cfg.hub_royalty_mana
                                continue
                            if other.strategy not in ("bystander", "feral_spoiler") and rng_rolls.random() < 0.78:
                                hub_c = min(2, sum(1 for t in other.river_tiers_enacted if t == 0))
                                r_tier = other.river_tiers_enacted[0] if other.river_tiers_enacted else 0
                                base_roy = cfg.hub_royalty_mana if r_tier == 0 else cfg.bridge_royalty_mana
                                foundation_dividend = (1.6 * hub_c) if n_done >= 2 else 0.0
                                royalty = base_roy * (1.5 if n_done >= 2 else 1.0) + foundation_dividend
                                other.mana += royalty
                                other.royalty_mana += royalty
                                mana_active_this_turn[other_idx] = True
                                if sub_idx == 0 and other.strategy in ("hub_builder", "constructive") and hub_c > 0:
                                    other.mana += cfg.abolish_impossible_bonus * 0.5
                                    other.legacy_mana += cfg.abolish_impossible_bonus * 0.5
                            else:
                                forfeit = cfg.bystander_forfeit_ss2 if n_done == 3 else cfg.bystander_forfeit_ss1
                                actual_loss = min(other.mana, forfeit)
                                other.mana -= actual_loss
                                other.forfeit_mana += actual_loss
                    else:
                        stake_lost = min(initiator.mana, cfg.tier_mana[sub_idx])
                        initiator.mana -= stake_lost
                        initiator.forfeit_mana += stake_lost

        # Standard Turn Combos, N:03 Heckman Cross-Gate Synergy, & +3 Mana Inverse-Hub Royalties
        royalty_triggers_this_turn = [0] * n_p
        heckman_mult = 1.35 if n03_heckman else 1.0
        for p_idx, p in enumerate(players):
            if p.strategy not in ("bystander", "feral_spoiler"):
                c12 = slot_coverage(p.slot_stacks["G12_TAMARIKI"], singleton_mode)
                c3 = slot_coverage(p.slot_stacks["G3_MENTOR"], singleton_mode)
                c5 = slot_coverage(p.slot_stacks["G5_GRANT"], singleton_mode)
                cross_syn = heckman_mult * (0.45 * ((c12 * c3) ** 0.5) + 0.40 * ((c3 * c5) ** 0.5))
                if cross_syn > 0:
                    p.mana += cross_syn
                    p.royalty_mana += cross_syn

                if rng_rolls.random() < (0.55 + p.pdsa_bonus):
                    card_tier = 2 if (p.strategy == "finisher" and turn >= 11) else (1 if turn >= 5 else 0)
                    base_m = cfg.tier_mana[card_tier]
                    p.mana += base_m + 1.0
                    p.init_mana += base_m + 1.0
                    step_cost = max(0.55, (0.85 if p.exergy_unlocked else 1.1) - (0.15 if n02_coase else 0.0))
                    p.wealth = max(0.0, p.wealth - step_cost)
                    mana_active_this_turn[p_idx] = True

                    if self_combo_allowed and p.river_tiers_enacted and royalty_triggers_this_turn[p_idx] < royalty_cap:
                        if rng_rolls.random() < 0.55:
                            p.mana += cfg.hub_royalty_mana
                            p.royalty_mana += cfg.hub_royalty_mana
                            royalty_triggers_this_turn[p_idx] += 1

                    for other_idx, other in enumerate(players):
                        if other_idx != p_idx and other.river_tiers_enacted:
                            if royalty_triggers_this_turn[other_idx] < royalty_cap:
                                other_g12 = slot_coverage(other.slot_stacks["G12_TAMARIKI"], singleton_mode)
                                other_g3 = slot_coverage(other.slot_stacks["G3_MENTOR"], singleton_mode)
                                eff_hub_weight = (
                                    (2.5 * (other_g12 + other_g3) + 0.5 * sum(1 for t in other.river_tiers_enacted if t == 0))
                                    if singleton_mode
                                    else max(float(sum(1 for t in other.river_tiers_enacted if t == 0)), 1.5 * (other_g12 + other_g3))
                                )
                                bridge_count = sum(1 for t in other.river_tiers_enacted if t == 1)
                                if eff_hub_weight > 0 and rng_rolls.random() < min(0.85, 0.28 * eff_hub_weight):
                                    other.mana += cfg.hub_royalty_mana
                                    other.royalty_mana += cfg.hub_royalty_mana
                                    royalty_triggers_this_turn[other_idx] += 1
                                    mana_active_this_turn[other_idx] = True
                                elif bridge_count > 0 and rng_rolls.random() < min(0.70, 0.28 * bridge_count):
                                    other.mana += cfg.bridge_royalty_mana
                                    other.royalty_mana += cfg.bridge_royalty_mana
                                    royalty_triggers_this_turn[other_idx] += 1
                                    mana_active_this_turn[other_idx] = True

        # --- 2-Turn "Use-It-Or-Lose-It" Manaaki Decay ---
        for p_idx, p in enumerate(players):
            if mana_active_this_turn[p_idx]:
                p.idle_mana_turns = 0
            else:
                p.idle_mana_turns += 1
                if p.idle_mana_turns >= cfg.idle_mana_limit:
                    decay = min(p.mana, cfg.idle_mana_decay)
                    p.mana -= decay
                    p.decay_mana_lost += decay
                    p.idle_mana_turns = 0

        # --- PHASE IV: Global Market D20 Contagion ("Davos") & Chasing Finland Roll ---
        d20_global = int(rng_rolls.integers(1, 21))
        max_k_end = max((len(p.capture_pillars) for p in players), default=0)
        t10_contagion = 1 if ("T:10" in active_hazards and not subsystems_done[1]) else 0
        contagion_cutoff = (
            1
            + max(0, max_k_end - 1)
            + t10_contagion
            + (1 if ss_regime == 0 and turn >= 10 else 0)
            - (1 if subsystems_done[2] else 0)
        )
        if d20_global <= max(1, contagion_cutoff):
            curr_mean_w = float(np.mean([x.wealth for x in players]))
            for p in players:
                if p.wealth > cfg.global_wealth_threshold and p.wealth > 1.18 * curr_mean_w:
                    k_p = len(p.capture_pillars)
                    if k_p == 4:
                        if d20_global <= 2:
                            p.wealth *= 0.72
                            cracked = int(rng_rolls.choice(list(p.capture_pillars)))
                            p.capture_pillars.discard(cracked)
                            p.contagion_hits += 1
                    elif k_p >= 2:
                        p.wealth *= 0.64
                        stripped = int(rng_rolls.choice(list(p.capture_pillars)))
                        p.capture_pillars.discard(stripped)
                        p.contagion_hits += 1
                    elif p.strategy != "shielded_arb" and not n07_milgrom and "E:03" not in enacted_river:
                        p.wealth *= 0.90
                        p.contagion_hits += 1

        f_roll = int(rng_rolls.integers(1, 21))
        finland_cohesion += -0.5 if f_roll <= 5 else (1.0 if f_roll <= 15 else 2.0)
        cohesion_drag = 0.55 if max_k_end >= 3 else 1.0
        n09_coh = 2.2 if n09_medallion else 0.0
        coh_step = cohesion_drag * (0.25 if ss_regime == 0 else (2.60 if ss_regime == 1 else 4.20)) + n09_coh
        # T:08 Scottish Devolution Ceiling caps SS1 cohesion at 96.0 until B:08 / Wing-Sail locks!
        if "T:08" in active_hazards and ss_regime == 1 and not subsystems_done[1] and "B:08" not in enacted_river:
            nz_cohesion = min(96.0, nz_cohesion + coh_step)
        else:
            nz_cohesion = min(126.0, nz_cohesion + coh_step)

        mana_traj.append([p.mana for p in players])
        wealth_traj.append([p.wealth for p in players])

    # --- ENDGAME: Check "Shoot the Moon" (4/4 Capture Pillars) vs. Three Unfortunate Fates ---
    front_foil, wing_sail, rear_foil = subsystems_done
    moon_shot_winner = -1
    for idx, p in enumerate(players):
        if p.strategy == "feral_spoiler":
            if len(p.capture_pillars) == 4:
                moon_shot_winner = idx
                p.wealth *= 1.25
            else:
                if wing_sail and ("T:10" not in excl or "B:08" in enacted_river):
                    p.wealth *= 0.67
                if rear_foil and p.mana < 2.0:
                    p.wealth = max(0.0, p.wealth - 0.55 * p.kickback_wealth)
                if ss_regime == 0:
                    p.wealth *= 0.50

    gamma = 0.5 if ss_regime == 0 else (1.0 if ss_regime == 1 else 1.5 + 0.05 * max(0, cfg.n_turns - ss2_turn))
    if ss_regime == 2 and h09_survived:
        gamma += 0.12
    if n09_medallion:
        gamma += 0.10

    raw_sum = sum(p.mana + p.wealth for p in players)
    combined_score = raw_sum * gamma
    constructive_seats = [p for p in players if p.strategy not in ("bystander", "feral_spoiler")]
    crew_score = sum(p.mana + p.wealth for p in constructive_seats) * gamma / max(1, len(constructive_seats))

    if wealth_traj:
        wealth_traj[-1] = [p.wealth for p in players]

    mana_dyn = compute_lead_dynamics(np.array(mana_traj))
    wealth_dyn = compute_lead_dynamics(np.array(wealth_traj))

    n_cons = max(1, len(constructive_seats))
    timely_g12 = sum(1 for p in constructive_seats if p.got_gate12_in_time) / n_cons
    full_3gate = sum(
        1 for p in constructive_seats
        if slot_coverage(p.slot_stacks["G12_TAMARIKI"], singleton_mode) >= 0.50
        and slot_coverage(p.slot_stacks["G3_MENTOR"], singleton_mode) >= 0.50
        and slot_coverage(p.slot_stacks["G5_GRANT"], singleton_mode) >= 0.50
    ) / n_cons

    return {
        "ss1_reached": float(ss_regime >= 1),
        "ss2_reached": float(ss_regime == 2),
        "ss2_turn": float(ss2_turn),
        "moon_shot": float(moon_shot_winner >= 0),
        "combined_score": combined_score,
        "per_capita_score": combined_score / n_p,
        "crew_score": crew_score,
        "beat_finland": float(nz_cohesion > finland_cohesion),
        "player_mana": [p.mana for p in players],
        "player_wealth": [p.wealth for p in players],
        "player_decay": [p.decay_mana_lost for p in players],
        "player_contagion": [float(p.contagion_hits) for p in players],
        "feral_final_pillars": float(len(players[-1].capture_pillars)) if strategies[-1] == "feral_spoiler" else 0.0,
        "total_trades": float(total_trades),
        "amber_saves": float(amber_saves),
        "n07_enacted": float("N:07" in enacted_river),
        "enacted_nobels": [nx for nx in NOBEL_IDS if nx in enacted_river],
        "p0_t1_tamariki": float(players[0].had_turn1_tamariki),
        "timely_g12": timely_g12,
        "full_3gate": full_3gate,
        "mana_dyn": mana_dyn,
        "wealth_dyn": wealth_dyn,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Run Foils & Founders 20-Turn Monte Carlo Balance Suite (v2026.11e).")
    ap.add_argument("-n", "--n-games", type=int, default=5_000, help="Simulations per table config (default: 5000)")
    args = ap.parse_args()

    cfg = SimConfig(n_games=args.n_games)
    tranche_counts = load_deck_counts_from_yaml(singleton_override=False)
    total_play_shoe = sum(tranche_counts.values()) + len(BOSS_TRAP_META) + 3

    print(f"=== 1. WAVE 3+ REBALANCED 4-PLAYER AUDIT ({total_play_shoe}-CARD ECOSYSTEM + N:07 CLEARINGHOUSE) ===")
    strat_4p = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]
    res_4p = [
        simulate_single_game(None, cfg, strat_4p, deck_counts=tranche_counts, game_seed=cfg.rng_seed + g)
        for g in range(cfg.n_games)
    ]
    mana_m = np.array([r["player_mana"] for r in res_4p])
    wealth_m = np.array([r["player_wealth"] for r in res_4p])
    decay_m = np.array([r["player_decay"] for r in res_4p])
    contagion_m = np.array([r["player_contagion"] for r in res_4p])
    m_wins = np.argmax(mana_m, axis=1)
    w_wins = np.argmax(wealth_m, axis=1)
    moon_rate = np.mean([r["moon_shot"] for r in res_4p]) * 100
    ss2_4p = np.mean([r["ss2_reached"] for r in res_4p]) * 100
    ss2_turn_4p = np.mean([r["ss2_turn"] for r in res_4p])
    avg_pillars = np.mean([r["feral_final_pillars"] for r in res_4p])
    avg_trades = np.mean([r["total_trades"] for r in res_4p])
    n07_rate = np.mean([r["n07_enacted"] for r in res_4p]) * 100
    amber_avg = np.mean([r["amber_saves"] for r in res_4p])

    for i, s in enumerate(strat_4p):
        print(
            f"  P{i+1} ({s:14s}): Mana={mana_m[:,i].mean():5.1f} (Win {np.mean(m_wins==i)*100:4.1f}%, "
            f"IdleDecay={decay_m[:,i].mean():3.1f}) | "
            f"Wealth={wealth_m[:,i].mean():5.1f} (Win {np.mean(w_wins==i)*100:4.1f}%, "
            f"D20Shocks={contagion_m[:,i].mean():3.2f})"
        )
    print(
        f"  -> Feral 'Shoot-the-Moon': {moon_rate:4.1f}% (Avg Pillars={avg_pillars:3.2f}) | "
        f"Trades/Game: {avg_trades:4.1f} | N:07 Live: {n07_rate:4.1f}% (AmberSaves={amber_avg:3.2f}) | "
        f"4P SS2: {ss2_4p:4.1f}% (Turn {ss2_turn_4p:4.1f})"
    )

    print("\n=== 1B. LEAD-SWING INTEGRAL & RACE DYNAMICS TELEMETRY (4P TABLE) ===")
    for label, key in [("MANA RACE  ", "mana_dyn"), ("WEALTH RACE", "wealth_dyn")]:
        dyns = [r[key] for r in res_4p]
        lead_chg = np.mean([d["lead_changes"] for d in dyns])
        reign = np.mean([d["mean_reign"] for d in dyns])
        swing_int = np.mean([d["swing_integral"] for d in dyns])
        gap_int = np.mean([d["gap_integral"] for d in dyns])
        raw_int = np.mean([d["raw_margin_integral"] for d in dyns])
        t10_hold = np.mean([d["turn10_holds"] for d in dyns]) * 100
        era_mat = np.array([d["era_leaders"] for d in dyns])

        regime_tag = (
            "RUNAWAY SLOG" if (lead_chg < 1.5 and t10_hold > 75)
            else ("STOCHASTIC PING-PONG" if (lead_chg > 8.0 and reign < 2.2) else "DYNAMIC MULTI-ERA ARCS")
        )
        print(
            f"  {label}: LeadChanges={lead_chg:4.2f} | AvgReign={reign:4.1f} turns | "
            f"SwingIntegral={swing_int:5.1f} pts | RelGapIntegral={gap_int:4.2f} "
            f"(SumGap={raw_int:5.1f}) | T10LeaderWins={t10_hold:4.1f}% -> [{regime_tag}]"
        )
        era_names = ["Early(T1-6)", "Mid(T7-13)", "Late(T14-20)"]
        era_summary = " | ".join(
            f"{e_name}: " + "/".join(f"P{p_i+1}:{np.mean(era_mat[:,e_i]==p_i)*100:2.0f}%" for p_i in range(4))
            for e_i, e_name in enumerate(era_names)
        )
        print(f"               Era Leaders -> {era_summary}")

    print("\n=== 2. PLAYER-COUNT SCALING AUDIT (P = 2 TO 6 CONSTRUCTIVE, NORMALIZED) ===")
    pool = ["hub_builder", "finisher", "shielded_arb", "hub_builder", "finisher", "shielded_arb"]
    for p_count in range(2, 7):
        sub_strats = pool[:p_count]
        res_p = [
            simulate_single_game(None, cfg, sub_strats, deck_counts=tranche_counts, game_seed=cfg.rng_seed + 50_000 + g)
            for g in range(cfg.n_games)
        ]
        print(
            f"  P={p_count} Players: SS2={np.mean([r['ss2_reached'] for r in res_p])*100:4.1f}% "
            f"(Turn {np.mean([r['ss2_turn'] for r in res_p]):4.1f}) | "
            f"Beat Finland={np.mean([r['beat_finland'] for r in res_p])*100:4.1f}% | "
            f"Trades={np.mean([r['total_trades'] for r in res_p]):4.1f} | "
            f"Per-Capita={np.mean([r['per_capita_score'] for r in res_p]):5.1f} pts"
        )

    print("\n=== 3. SYMMETRIC OPENING-HAND FAIRNESS: SINGLETON VS. TRANCHE + COASIAN TRADING ===")
    sym_strats = ["constructive", "constructive", "constructive", "feral_spoiler"]
    singleton_counts = load_deck_counts_from_yaml(singleton_override=True)
    for mode_label, t_on, tr_on, c_map in [
        ("80-Card Singleton Shoe (1x Binary, No Trade)", False, False, singleton_counts),
        ("100-Card Tranche Shoe (50/25/25%, No Trade)", True, False, tranche_counts),
        ("100-Card Tranche Shoe (50/25/25% + Coasian Trade)", True, True, tranche_counts),
    ]:
        c_sub = SimConfig(n_games=cfg.n_games, tranche_deck_enabled=t_on, coasian_trading_enabled=tr_on)
        r_sub = [
            simulate_single_game(None, c_sub, sym_strats, deck_counts=c_map, game_seed=cfg.rng_seed + 90_000 + g)
            for g in range(cfg.n_games)
        ]
        p0_wins = [float(np.argmax(r["player_mana"]) == 0) for r in r_sub]
        have_w = [w for w, r in zip(p0_wins, r_sub) if r["p0_t1_tamariki"] > 0.5]
        miss_w = [w for w, r in zip(p0_wins, r_sub) if r["p0_t1_tamariki"] < 0.5]
        gap = (np.mean(have_w) - np.mean(miss_w)) * 100 if (have_w and miss_w) else 0.0
        print(
            f"  {mode_label:<48s} -> T1Have={len(have_w)/len(r_sub)*100:4.1f}% | "
            f"Win|Have={np.mean(have_w)*100:4.1f}% vs Win|Miss={np.mean(miss_w)*100:4.1f}% (Gap={gap:+5.1f}pp) | "
            f"G12<=T5={np.mean([r['timely_g12'] for r in r_sub])*100:5.1f}% | "
            f"3Gate={np.mean([r['full_3gate'] for r in r_sub])*100:5.1f}%"
        )

    print("\n=== 4. BACKLOG BIFURCATION (1972 vs. 2026) & N:07 MILGROM CLEARINGHOUSE A/B ===")
    for era_lbl, psi_v, tr_v, excl_s in [
        ("1972 Era (psi=1/16x, Thin No-Trade / No-N:07)", 1.0 / 16.0, False, frozenset({"N:07"})),
        ("1995 Era (psi=1/4x,  Thin No-Trade / No-N:07)", 0.25, False, frozenset({"N:07"})),
        ("2026 Era (psi=1.0x,  Thin No-Trade / No-N:07)", 1.0, False, frozenset({"N:07"})),
        ("2026 Era (psi=1.0x,  Coasian Trade, NO N:07)", 1.0, True, frozenset({"N:07"})),
        ("2026 Era (psi=1.0x,  Full Deck + N:07 Clearing)", 1.0, True, frozenset()),
    ]:
        c_era = SimConfig(n_games=cfg.n_games, era_backlog=psi_v, coasian_trading_enabled=tr_v, excluded_cards=excl_s)
        r_era = [
            simulate_single_game(None, c_era, strat_4p, deck_counts=tranche_counts, game_seed=cfg.rng_seed + g)
            for g in range(cfg.n_games)
        ]
        print(
            f"  {era_lbl:<48s} -> SS2={np.mean([r['ss2_reached'] for r in r_era])*100:5.1f}% "
            f"(T={np.mean([r['ss2_turn'] for r in r_era]):4.1f}) | "
            f"Moon={np.mean([r['moon_shot'] for r in r_era])*100:4.1f}% | "
            f"CrewScore={np.mean([r['crew_score'] for r in r_era]):5.1f} | "
            f"BeatFin={np.mean([r['beat_finland'] for r in r_era])*100:5.1f}%"
        )


if __name__ == "__main__":
    main()