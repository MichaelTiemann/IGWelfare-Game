#!/usr/bin/env python3
"""
Foils & Founders: 20-Turn Coopetitive Monte Carlo Balance Simulator (v2026.11d — Wave 3B)
=========================================================================================
Evaluates:
  1. +3 Mana Inverse-Hub Royalty boost for foundational/provincial Hub Builders
  2. 2-Turn "Use-It-Or-Lose-It" Manaaki Decay (0 staked & 0 earned for 2 turns -> -1 Mana)
  3. "Shooting the Moon" Plutocrat Gambit with:
       - Strategic Ambiguity (Turns 1-5 seed-capital skim vs. Turn 6-8 reformer pivot)
       - Domino Capture Additionality (easier capture, governance drag, & compounding rents at 2-3 pillars)
       - Global Market D20 Contagion (stochastic tail-risk margin calls on concentrated wealth)
  4. 2-Player to 6-Player Normalized Scaling & Chasing Finland Match Race
  5. Wave 3 100-Card Tranche Shoe (6x B:01, 3x B:02, 7x B:03, 3x B:04, 3x B:05, 4x B:06):
       - Diminishing marginal returns per lifecycle slot (1st=50%, 2nd=+25%, 3rd=+25%)
       - Endogenous Coasian Trading (25% surplus swapped/sold into 50% first-tranche slots + Spoiler ransom)
       - B:09 Turn 7+ fiscal audit dividend floor & K:09 Slot-3 Kaumātua wisdom-token gate

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    import yaml
except ImportError:
    yaml = None  # Graceful fallback to default 100-card counts if PyYAML unavailable


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


@dataclass
class SimConfig:
    n_games: int = 5_000
    n_turns: int = 20               # 60 years (3 years/turn)
    n_players: int = 4
    normalized_scaling: bool = True
    tranche_deck_enabled: bool = True
    coasian_trading_enabled: bool = True
    seed_mana: float = 3.0
    hub_royalty_mana: float = 3.0   # Upgraded from 1.0/2.0 -> 3.0 Mana for Hub Builders!
    bridge_royalty_mana: float = 2.5
    idle_mana_limit: int = 2        # 2 consecutive turns with 0 staked & 0 earned -> -1 Mana
    idle_mana_decay: float = 1.0
    abolish_impossible_bonus: float = 5.0
    bystander_forfeit_ss1: float = 2.0
    bystander_forfeit_ss2: float = 3.0
    feral_backfire_forfeit: float = 2.0
    watchdog_block_mana: float = 1.0        # Mana earned by Shielded Arb / defender for Judo-blocking capture!
    tier_mana: Tuple[float, float, float] = (1.0, 2.1, 4.6)
    # --- Domino Capture & Global D20 Contagion Tuning Knobs ---
    pillar_attempt_probs: Tuple[float, float, float, float] = (0.48, 0.40, 0.58, 0.78)
    pillar_passive_rents: Tuple[float, float, float, float, float] = (0.0, 0.6, 1.5, 3.2, 5.4)
    crew_base_shield: float = 0.80          # Base Judo-block at k=1->2 when shielded_arb is present
    governance_erosion_per_pillar: float = 0.16  # Capture 2 -> 3rd easier (-0.16); Capture 3 -> 4th easier (-0.32)
    global_wealth_threshold: float = 26.0   # Wealth level where global markets notice NZ concentration
    finland_start: float = 88.0
    nz_start: float = 81.0
    rng_seed: int = 20261028


@dataclass
class PlayerState:
    strategy: str
    mana: float
    wealth: float
    kickback_wealth: float = 0.0
    capture_pillars: set = field(default_factory=set)  # Needs {0,1,2,3} to Shoot the Moon!
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
    # --- Wave 3 Shoe, Hand, & Lifecycle Tranche State ---
    hand: List[str] = field(default_factory=list)
    slot_stacks: Dict[str, int] = field(default_factory=lambda: {s: 0 for s in LIFECYCLE_SLOTS})
    had_turn1_tamariki: bool = False
    got_gate12_in_time: bool = False
    compass_peeks: int = 0
    pdsa_bonus: float = 0.0
    exergy_unlocked: bool = False
    trades_made: int = 0


def load_deck_counts_from_yaml(repo_root: Optional[Path] = None, singleton_override: bool = False) -> Dict[str, int]:
    """Loads exact Play-Deck card multiplicities from decks/cards.yaml (100 cards in Wave 3)."""
    if singleton_override:
        base = {cid: 1 for cid in DEFAULT_TRANCHE_COPIES}
        base.update({"B:08": 1, "B:09": 1, "N:01": 2, "E:01": 2, "OTHER": 68})
        return base

    root = repo_root or Path(__file__).resolve().parents[1]
    cards_yaml = root / "decks" / "cards.yaml"
    if yaml is not None and cards_yaml.exists():
        data = yaml.safe_load(cards_yaml.read_text(encoding="utf-8")) or {}
        cards = data.get("cards", [])
        if cards:
            counts: Dict[str, int] = {"OTHER": 0}
            tracked = set(DEFAULT_TRANCHE_COPIES) | {"B:08", "B:09", "N:01", "N:07", "E:01", "E:02"}
            for c in cards:
                cid = str(c.get("id", "")).strip()
                n_cop = max(1, int(c.get("copies", 1)))
                if cid in ("N:01", "N:07"):
                    counts["N:01"] = counts.get("N:01", 0) + n_cop
                elif cid in ("E:01", "E:02"):
                    counts["E:01"] = counts.get("E:01", 0) + n_cop
                elif cid in tracked:
                    counts[cid] = counts.get(cid, 0) + n_cop
                else:
                    counts["OTHER"] += n_cop
            return counts

    fallback = dict(DEFAULT_TRANCHE_COPIES)
    fallback.update({"B:08": 1, "B:09": 1, "N:01": 2, "E:01": 2, "OTHER": 68})
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


def roll_d20_birth(rng: np.random.Generator, front_foil_active: bool, guinz_drift: bool = True) -> Tuple[float, bool]:
    roll = int(rng.integers(1, 21))
    corner_cutoff = 6 if guinz_drift else 4
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
    """
    Measures lead-swing integrals, reign lengths, and era leadership across a (T, P) score trajectory.
      - gap_integral: time-averaged (Top1 - Top2) / max(1, mean_positive_score)
      - swing_integral: cumulative point displacement across all lead-change overtakes
      - lead_changes: number of turns where argmax strictly changes owner
      - mean_reign: average consecutive turns a leader holds #1
      - turn10_holds: 1.0 if Turn-10 leader is also Turn-20 leader
      - era_leaders: [Early (T1-6), Mid (T7-13), Late (T14-20)] modal leader index
    """
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
            # Full overtake displacement: deficit closed from t-1 plus new margin opened at t
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
    rng: np.random.Generator,
    cfg: SimConfig,
    strategies: List[str],
    table_mode: str = "mixed",
    deck_counts: Optional[Dict[str, int]] = None,
) -> Dict[str, float | List[float]]:
    n_p = len(strategies)
    singleton_mode = not cfg.tranche_deck_enabled
    counts = deck_counts or load_deck_counts_from_yaml(singleton_override=singleton_mode)

    shoe = [cid for cid, cnt in counts.items() for _ in range(cnt)]
    rng.shuffle(shoe)
    discard: List[str] = []

    players: List[PlayerState] = []
    for s in strategies:
        w0, struggling = roll_d20_birth(rng, front_foil_active=False)
        p_init = PlayerState(strategy=s, mana=cfg.seed_mana, wealth=w0 * 2.0, struggling_flags=[False, struggling])
        p_init.hand.extend(draw_from_shoe(rng, shoe, discard, 4))
        p_init.had_turn1_tamariki = any(c in ("B:01", "B:02", "B:03") for c in p_init.hand)
        players.append(p_init)

    river_cards = draw_from_shoe(rng, shoe, discard, 4)

    subsystems_done = [False, False, False]  # [Front Foil, Wing-Sail, Rear T-Foil]
    ss_regime = 0
    ss2_turn = cfg.n_turns + 1
    struggling_births = sum(1 for p in players for st in p.struggling_flags if st)
    total_trades = 0

    finland_cohesion = cfg.finland_start
    nz_cohesion = cfg.nz_start

    if cfg.normalized_scaling:
        drag_cost = 1.5 if n_p == 2 else (2.0 if n_p <= 4 else 3.0)
        royalty_cap = 2
        self_combo_allowed = (n_p == 2)
        river_visibility_boost = 1.15 if n_p == 2 else (0.90 if n_p >= 5 else 1.0)
    else:
        drag_cost = 2.0
        royalty_cap = 99
        self_combo_allowed = False
        river_visibility_boost = 0.72 if n_p == 2 else (1.28 if n_p >= 5 else 1.0)

    mana_traj: List[List[float]] = []
    wealth_traj: List[List[float]] = []

    for turn in range(1, cfg.n_turns + 1):
        front_foil, wing_sail, rear_foil = subsystems_done
        mana_active_this_turn = [False] * n_p
        mean_wealth = float(np.mean([x.wealth for x in players]))

        # --- PHASE 0: Shoe Draw, River Turnover, & Coasian Tranche Trading ---
        for p in players:
            p.hand.extend(draw_from_shoe(rng, shoe, discard, 1))
        if river_cards:
            discard.append(river_cards.pop(0))
        river_cards.extend(draw_from_shoe(rng, shoe, discard, 1))

        # Constructive players can draft 1 needed Gate tranche or B:09 from the open River
        for p in players:
            if p.strategy in ("bystander", "feral_spoiler"):
                continue
            best_rc, best_val = None, 0.0
            for rc in river_cards:
                sl = CARD_TO_SLOT.get(rc)
                if sl is not None:
                    mg = slot_marginal_gain(p.slot_stacks[sl], singleton_mode)
                    if mg > best_val:
                        best_rc, best_val = rc, mg
                elif rc == "B:09" and turn <= 8 and best_val < 0.45:
                    best_rc, best_val = rc, 0.45
            if best_rc is not None and best_val >= 0.25:
                river_cards.remove(best_rc)
                p.hand.append(best_rc)
                river_cards.extend(draw_from_shoe(rng, shoe, discard, 1))

        # Endogenous Coasian Trading: 25% duplicate in Seat A -> 50% first-tranche slot in Seat B!
        if cfg.coasian_trading_enabled and not singleton_mode:
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

                        # 1-for-1 complementary swap between constructive Wayfinders
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
                                        sa.mana += 0.5
                                        sb.mana += 0.5
                                        sa.royalty_mana += 0.5
                                        sb.royalty_mana += 0.5
                                        mana_active_this_turn[a_i] = True
                                        mana_active_this_turn[b_i] = True
                                        sa.trades_made += 1
                                        sb.trades_made += 1
                                        total_trades += 1
                                        swapped = True
                                        break
                        # Unilateral Coasian purchase (or Feral Spoiler hostage ransom at 1.8W)
                        price = 1.8 if a_is_spoiler else 1.1
                        if not swapped and sb.wealth >= price + 1.2:
                            sa.hand.remove(c_a)
                            sb.hand.append(c_a)
                            sb.wealth -= price
                            sa.wealth += price
                            if a_is_spoiler:
                                sa.kickback_wealth += 0.8
                            else:
                                sa.mana += 0.7
                                sa.royalty_mana += 0.7
                                mana_active_this_turn[a_i] = True
                            sa.trades_made += 1
                            sb.trades_made += 1
                            total_trades += 1
                        break

        # --- PHASE I: Aging, Rebirth, & Earnings ---
        for p in players:
            g12_cov = slot_coverage(p.slot_stacks["G12_TAMARIKI"], singleton_mode)
            g3_cov = slot_coverage(p.slot_stacks["G3_MENTOR"], singleton_mode)
            g4_cov = slot_coverage(p.slot_stacks["G4_LAUNCH"], singleton_mode)
            g5_cov = slot_coverage(p.slot_stacks["G5_GRANT"], singleton_mode)

            for c_idx in range(2):
                p.ages[c_idx] += 1
                # H:10 Unmentored Grant / LVR Cliff softened proportionally by Gate 3 + Gate 5 coverage
                cliff_shield = min(1.0, 0.5 * (g3_cov + g5_cov))
                if p.ages[c_idx] == 7 and not wing_sail and rng.random() < 0.22 * (1.0 - 0.75 * cliff_shield):
                    p.wealth = max(0.0, p.wealth - 1.5)
                if p.ages[c_idx] >= 30:
                    p.ages[c_idx] = 0
                    _, is_struggling = roll_d20_birth(rng, front_foil_active=(front_foil or g12_cov >= 0.50))
                    p.struggling_flags[c_idx] = is_struggling
                    if is_struggling:
                        struggling_births += 1

            adult_count = sum(1 for a in p.ages if a >= 6)
            # Active z_h builders earn full SS1/SS2 dividend; passive z_l hoarders face LVT drag if Wing-Sail locks
            # UNLESS they hold Land/Cartel + Narrative/Offshore capture (>=3 pillars shields LVT drag)!
            if p.strategy == "feral_spoiler":
                z_mult = 0.55 if (wing_sail and len(p.capture_pillars) < 3) else 1.15
            else:
                tranche_lift = 0.12 * (g4_cov + g5_cov)
                z_mult = 1.0 + (0.45 if wing_sail else 0.0) + (0.45 if rear_foil else 0.0) + tranche_lift
            # Early Tamariki tranche coverage mitigates household hardship penalty proportionally
            hardship_penalty = (0.5 + 0.5 * g12_cov) if (any(p.struggling_flags) and not front_foil) else 1.0
            exergy_div = 0.35 if p.exergy_unlocked else 0.0
            p.wealth += adult_count * 1.25 * z_mult * hardship_penalty + exergy_div

        # --- PHASE II: Hand/River Card Execution, Strategic Ambiguity, & Domino Capture ---
        for p_i, p in enumerate(players):
            k = len(p.capture_pillars)

            # 1. Strategic Ambiguity (Turns 1-5): Early 1st Pillar looks like routine seed-capital skimming!
            if (
                k == 0
                and turn <= 5
                and p.strategy in ("finisher", "shielded_arb", "feral_spoiler")
                and rng.random() < (cfg.pillar_attempt_probs[0] if p.strategy == "feral_spoiler" else 0.28)
            ):
                initial_pillar = int(rng.choice([0, 1]))  # Narrative or Land/Cartel position
                p.capture_pillars.add(initial_pillar)
                p.wealth += 2.0
                if p.strategy == "feral_spoiler":
                    p.kickback_wealth += 2.0
                if p.strategy == "feral_spoiler":
                    p.wealth += cfg.pillar_passive_rents[len(p.capture_pillars)]
                    continue

            # 2. Reformer Mid-Game Pivot (Turns 6-8): Constructive players divest early Pillar into clean z_h equity!
            if k == 1 and turn in (6, 7, 8) and p.strategy in ("finisher", "shielded_arb"):
                p.capture_pillars.clear()
                p.wealth += 1.5
                p.mana += 1.5
                p.init_mana += 1.5
                mana_active_this_turn[p_i] = True

            # 3. Constructive Tranche / Special Card Play + River Exposure vs. Feral Domino Capture
            if p.strategy in ("hub_builder", "shielded_arb", "constructive") or (p.strategy == "finisher" and turn >= 5):
                # Check hand for highest-priority Lifecycle Tranche or Wave-3 balanced special card (B:09, N:01, E:01, B:08)
                played_special = False
                best_card, best_gain = None, 0.0
                for hc in p.hand:
                    sl = CARD_TO_SLOT.get(hc)
                    if sl is not None:
                        urg = 1.35 if (sl in ("G12_TAMARIKI", "G3_MENTOR") and turn <= 5) else 1.0
                        g = slot_marginal_gain(p.slot_stacks[sl], singleton_mode) * urg
                        if g > best_gain:
                            best_card, best_gain = hc, g
                if best_card is not None and best_gain > 0 and p.wealth >= 0.6:
                    sl = CARD_TO_SLOT[best_card]
                    mg = slot_marginal_gain(p.slot_stacks[sl], singleton_mode)
                    p.hand.remove(best_card)
                    p.slot_stacks[sl] += 1
                    if sl in ("G12_TAMARIKI", "G3_MENTOR") and turn <= 5:
                        p.got_gate12_in_time = True
                        p.struggling_flags = [False, False]
                    tier_exposed = 0 if sl in ("G12_TAMARIKI", "G3_MENTOR") else 1
                    p.river_tiers_enacted.append(tier_exposed)
                    pioneer_bonus = 0.9 if (p.strategy == "hub_builder" and sl in ("G12_TAMARIKI", "G3_MENTOR")) else 0.0
                    p.mana += 1.8 * mg + pioneer_bonus
                    p.init_mana += 1.8 * mg + pioneer_bonus
                    p.wealth += 0.4
                    mana_active_this_turn[p_i] = True
                    played_special = True
                elif "B:09" in p.hand:
                    # Wave 3A B:09 rule: Years 1-8 stern-kick shield + Compass peek OR Turn 7+ matured audit floor (+2.5M)
                    p.hand.remove("B:09")
                    discard.append("B:09")
                    if turn <= 8:
                        p.compass_peeks += 1
                        p.mana += 2.8
                        p.init_mana += 2.8
                    else:
                        p.mana += 2.5
                        p.init_mana += 2.5
                        p.exergy_unlocked = True  # -30 bps sovereign spread dividend
                    mana_active_this_turn[p_i] = True
                    played_special = True
                elif "N:01" in p.hand:
                    p.hand.remove("N:01")
                    discard.append("N:01")
                    # K:09 Wisdom Token rule: 50% discount base, 100% free if Kaumātua (age >= 20) active in Slot 3!
                    has_kaumatua = any(a >= 20 for a in p.ages)
                    nobel_cost = 0.0 if (p.strategy == "hub_builder" and has_kaumatua) else 0.5
                    p.wealth = max(0.0, p.wealth - nobel_cost)
                    p.pdsa_bonus = min(0.16, p.pdsa_bonus + 0.08)
                    p.mana += 1.4
                    p.init_mana += 1.4
                    mana_active_this_turn[p_i] = True
                    played_special = True
                elif "E:01" in p.hand:
                    p.hand.remove("E:01")
                    discard.append("E:01")
                    p.exergy_unlocked = True
                    p.wealth += 1.0
                    p.mana += 1.2
                    p.init_mana += 1.2
                    mana_active_this_turn[p_i] = True
                    played_special = True

                if not played_special and rng.random() < (0.62 + p.pdsa_bonus):
                    if p.hand:
                        discard.append(p.hand.pop(0))
                    p.wealth += 1.0
                    tier_exposed = 0 if p.strategy == "hub_builder" and turn <= 8 else (1 if turn <= 12 else 2)
                    p.river_tiers_enacted.append(tier_exposed)
                    mana_active_this_turn[p_i] = True

            elif p.strategy == "feral_spoiler":
                # Discard excess non-tranche cards to keep hand fresh for hostage trades
                if len(p.hand) > 5:
                    for hc in list(p.hand):
                        if hc not in CARD_TO_SLOT:
                            p.hand.remove(hc)
                            discard.append(hc)
                            break
                # Spoiler escalates toward all 4 Capture Pillars {0:Narrative, 1:Land/Cartel, 2:Labor, 3:Offshore}
                missing = [idx_p for idx_p in range(4) if idx_p not in p.capture_pillars]
                k_now = len(p.capture_pillars)
                lobby_cost = 1.2 * k_now
                if missing and p.wealth >= lobby_cost:
                    attempt_p = cfg.pillar_attempt_probs[k_now]
                    if p.wealth > 1.20 * mean_wealth:
                        attempt_p = min(0.92, attempt_p + 0.06)

                    if rng.random() < attempt_p:
                        target_pillar = int(rng.choice(missing))
                        p.wealth -= lobby_cost

                        if k_now == 0:
                            p.capture_pillars.add(target_pillar)
                            p.wealth += 2.2
                            p.kickback_wealth += 2.2
                        else:
                            arb_indices = [
                                idx_x for idx_x, x in enumerate(players)
                                if x.strategy == "shielded_arb" and x.wealth >= 1.2 * k_now
                            ]
                            base_block = cfg.crew_base_shield if arb_indices else 0.48
                            effective_block = (
                                base_block
                                - cfg.governance_erosion_per_pillar * (k_now - 1)
                                + (0.20 if ss_regime == 2 else 0.0)
                            )
                            effective_block = float(np.clip(effective_block, 0.10, 0.88))

                            if rng.random() < effective_block:
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
                                p.wealth += lobby_cost + 2.4
                                p.kickback_wealth += 2.6

            # Compounding Economic Rent from held Capture Pillars
            if p.capture_pillars:
                rent = cfg.pillar_passive_rents[len(p.capture_pillars)]
                p.wealth += rent
                if p.strategy == "feral_spoiler":
                    p.kickback_wealth += 0.6 * rent

        # --- PHASE III: Subsystem Completions (with Governance Capture Drag) & D20 Hazard Check ---
        max_pillars_held = max((len(p.capture_pillars) for p in players), default=0)
        capture_turn_delay = 0 if max_pillars_held <= 1 else (1 if max_pillars_held == 2 else (3 if max_pillars_held == 3 else 5))
        capture_vis_mult = 1.0 if max_pillars_held <= 1 else (0.85 if max_pillars_held == 2 else (0.52 if max_pillars_held == 3 else 0.22))
        table_compass = sum(p.compass_peeks for p in players)

        for sub_idx in range(3):
            if not subsystems_done[sub_idx]:
                ready_turn = [2, 5, 9][sub_idx] + capture_turn_delay
                if sub_idx == 2 and table_compass > 0:
                    ready_turn = max(6, ready_turn - 1)  # Plan A Star-Compass acceleration via B:09!
                if table_mode == "hoarders":
                    ready_turn += 4
                elif table_mode == "bystanders":
                    ready_turn += 9

                if turn >= ready_turn and rng.random() < min(0.92, 0.52 * river_visibility_boost * capture_vis_mult):
                    weights = np.array([
                        3.4 if p.strategy == "hub_builder" and sub_idx == 0 else
                        3.4 if p.strategy == "finisher" and sub_idx >= 1 else
                        (2.8 + 0.6 * p.compass_peeks) if p.strategy == "shielded_arb" else
                        (2.2 if p.strategy == "constructive" else 0.10)
                        for p in players
                    ])
                    weights /= weights.sum()
                    init_idx = int(rng.choice(n_p, p=weights))
                    initiator = players[init_idx]
                    mana_active_this_turn[init_idx] = True

                    d20_hazard = int(rng.integers(1, 21)) + 3 * initiator.compass_peeks
                    vuln_cutoff = 6 if not front_foil else (4 if (turn % 3 == 0 and not rear_foil) else 2)
                    saved_by_emergency_window = (table_mode in ("mixed", "balanced")) and (rng.random() < 0.85)

                    if d20_hazard > vuln_cutoff or saved_by_emergency_window:
                        subsystems_done[sub_idx] = True
                        n_done = sum(subsystems_done)

                        for sp in players:
                            if len(sp.capture_pillars) < 4:
                                if sub_idx == 0:
                                    sp.capture_pillars.discard(2)
                                elif sub_idx == 1:
                                    sp.capture_pillars.discard(1)
                                elif sub_idx == 2:
                                    sp.capture_pillars.discard(0)

                        mu = 1.25 if n_done == 1 else (1.75 if n_done == 2 else 2.20)
                        if n_done == 2:
                            ss_regime = 1
                        elif n_done == 3:
                            ss_regime = 2
                            ss2_turn = min(ss2_turn, turn)

                        init_card_mana = cfg.tier_mana[sub_idx]
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
                                    royalty = cfg.hub_royalty_mana
                                    initiator.mana += royalty
                                    initiator.royalty_mana += royalty
                                continue
                            if other.strategy not in ("bystander", "feral_spoiler") and rng.random() < 0.78:
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

        # Standard Turn Combos, Heckman Cross-Gate Synergy, & +3 Mana Inverse-Hub Royalties
        royalty_triggers_this_turn = [0] * n_p
        for p_idx, p in enumerate(players):
            if p.strategy not in ("bystander", "feral_spoiler"):
                # Heckman-Topkis cross-gate supermodular yield from active lifecycle tranches
                c12 = slot_coverage(p.slot_stacks["G12_TAMARIKI"], singleton_mode)
                c3 = slot_coverage(p.slot_stacks["G3_MENTOR"], singleton_mode)
                c5 = slot_coverage(p.slot_stacks["G5_GRANT"], singleton_mode)
                cross_syn = 0.45 * ((c12 * c3) ** 0.5) + 0.40 * ((c3 * c5) ** 0.5)
                if cross_syn > 0:
                    p.mana += cross_syn
                    p.royalty_mana += cross_syn

                if rng.random() < (0.55 + p.pdsa_bonus):
                    card_tier = 2 if (p.strategy == "finisher" and turn >= 11) else (1 if turn >= 5 else 0)
                    base_m = cfg.tier_mana[card_tier]
                    p.mana += base_m + 1.0
                    p.init_mana += base_m + 1.0
                    step_cost = 0.85 if p.exergy_unlocked else 1.1
                    p.wealth = max(0.0, p.wealth - step_cost)
                    mana_active_this_turn[p_idx] = True

                    if self_combo_allowed and p.river_tiers_enacted and royalty_triggers_this_turn[p_idx] < royalty_cap:
                        if rng.random() < 0.55:
                            p.mana += cfg.hub_royalty_mana
                            p.royalty_mana += cfg.hub_royalty_mana
                            royalty_triggers_this_turn[p_idx] += 1

                    for other_idx, other in enumerate(players):
                        if other_idx != p_idx and other.river_tiers_enacted:
                            if royalty_triggers_this_turn[other_idx] < royalty_cap:
                                # Scale hub trigger probability smoothly by tranche coverage in Wave 3
                                other_g12 = slot_coverage(other.slot_stacks["G12_TAMARIKI"], singleton_mode)
                                other_g3 = slot_coverage(other.slot_stacks["G3_MENTOR"], singleton_mode)
                                eff_hub_weight = (
                                    (2.5 * (other_g12 + other_g3) + 0.5 * sum(1 for t in other.river_tiers_enacted if t == 0))
                                    if singleton_mode
                                    else max(float(sum(1 for t in other.river_tiers_enacted if t == 0)), 1.5 * (other_g12 + other_g3))
                                )
                                bridge_count = sum(1 for t in other.river_tiers_enacted if t == 1)
                                if eff_hub_weight > 0 and rng.random() < min(0.85, 0.28 * eff_hub_weight):
                                    other.mana += cfg.hub_royalty_mana
                                    other.royalty_mana += cfg.hub_royalty_mana
                                    royalty_triggers_this_turn[other_idx] += 1
                                    mana_active_this_turn[other_idx] = True
                                elif bridge_count > 0 and rng.random() < min(0.70, 0.28 * bridge_count):
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

        # --- PHASE IV: Global Market D20 Contagion & Chasing Finland Automa Roll ---
        d20_global = int(rng.integers(1, 21))
        max_k_end = max((len(p.capture_pillars) for p in players), default=0)
        contagion_cutoff = 1 + max(0, max_k_end - 1) + (1 if ss_regime == 0 and turn >= 10 else 0) - (1 if subsystems_done[2] else 0)
        if d20_global <= max(1, contagion_cutoff):
            curr_mean_w = float(np.mean([x.wealth for x in players]))
            for p in players:
                if p.wealth > cfg.global_wealth_threshold and p.wealth > 1.18 * curr_mean_w:
                    k_p = len(p.capture_pillars)
                    if k_p == 4:
                        if d20_global <= 2:
                            p.wealth *= 0.72
                            cracked = int(rng.choice(list(p.capture_pillars)))
                            p.capture_pillars.discard(cracked)
                            p.contagion_hits += 1
                    elif k_p >= 2:
                        p.wealth *= 0.64
                        stripped = int(rng.choice(list(p.capture_pillars)))
                        p.capture_pillars.discard(stripped)
                        p.contagion_hits += 1
                    elif p.strategy != "shielded_arb":
                        p.wealth *= 0.90
                        p.contagion_hits += 1

        f_roll = int(rng.integers(1, 21))
        finland_cohesion += -0.5 if f_roll <= 5 else (1.0 if f_roll <= 15 else 2.0)
        cohesion_drag = 0.55 if max_k_end >= 3 else 1.0
        nz_cohesion = min(
            126.0,
            nz_cohesion + cohesion_drag * (0.25 if ss_regime == 0 else (2.60 if ss_regime == 1 else 4.20)),
        )

        mana_traj.append([p.mana for p in players])
        wealth_traj.append([p.wealth for p in players])

    # --- ENDGAME: Check "Shoot the Moon" (4/4 Capture Pillars) vs. Unfortunate Fates ---
    front_foil, wing_sail, rear_foil = subsystems_done
    moon_shot_winner = -1
    for idx, p in enumerate(players):
        if p.strategy == "feral_spoiler":
            if len(p.capture_pillars) == 4:
                moon_shot_winner = idx
                p.wealth *= 1.25
            else:
                if wing_sail:
                    p.wealth *= 0.68
                if rear_foil and p.mana < 2.0:
                    p.wealth = max(0.0, p.wealth - 0.55 * p.kickback_wealth)
                if ss_regime == 0:
                    p.wealth *= 0.50

    gamma = 0.5 if ss_regime == 0 else (1.0 if ss_regime == 1 else 1.5 + 0.05 * max(0, cfg.n_turns - ss2_turn))
    raw_sum = sum(p.mana + p.wealth for p in players)
    combined_score = raw_sum * gamma

    if wealth_traj:
        wealth_traj[-1] = [p.wealth for p in players]

    mana_dyn = compute_lead_dynamics(np.array(mana_traj))
    wealth_dyn = compute_lead_dynamics(np.array(wealth_traj))

    constructive_seats = [p for p in players if p.strategy not in ("bystander", "feral_spoiler")]
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
        "beat_finland": float(nz_cohesion > finland_cohesion),
        "player_mana": [p.mana for p in players],
        "player_wealth": [p.wealth for p in players],
        "player_decay": [p.decay_mana_lost for p in players],
        "player_contagion": [float(p.contagion_hits) for p in players],
        "feral_final_pillars": float(len(players[-1].capture_pillars)) if strategies[-1] == "feral_spoiler" else 0.0,
        "total_trades": float(total_trades),
        "p0_t1_tamariki": float(players[0].had_turn1_tamariki),
        "timely_g12": timely_g12,
        "full_3gate": full_3gate,
        "mana_dyn": mana_dyn,
        "wealth_dyn": wealth_dyn,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Run Foils & Founders 20-Turn Monte Carlo Balance Suite (Wave 3B).")
    ap.add_argument("-n", "--n-games", type=int, default=5_000, help="Simulations per table config (default: 5000)")
    args = ap.parse_args()

    cfg = SimConfig(n_games=args.n_games)
    rng = np.random.default_rng(cfg.rng_seed)
    tranche_counts = load_deck_counts_from_yaml(singleton_override=False)
    total_shoe = sum(tranche_counts.values())

    print(f"=== 1. WAVE 3 REBALANCED 4-PLAYER AUDIT ({total_shoe}-CARD TRANCHE SHOE + COASIAN TRADING) ===")
    strat_4p = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]
    res_4p = [simulate_single_game(rng, cfg, strat_4p, deck_counts=tranche_counts) for _ in range(cfg.n_games)]
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

    for i, s in enumerate(strat_4p):
        print(
            f"  P{i+1} ({s:14s}): Mana={mana_m[:,i].mean():5.1f} (Win {np.mean(m_wins==i)*100:4.1f}%, "
            f"IdleDecay={decay_m[:,i].mean():3.1f}) | "
            f"Wealth={wealth_m[:,i].mean():5.1f} (Win {np.mean(w_wins==i)*100:4.1f}%, "
            f"D20Shocks={contagion_m[:,i].mean():3.2f})"
        )
    print(
        f"  -> Feral 'Shoot-the-Moon' (4/4 Pillars): {moon_rate:4.1f}% (Avg Final Pillars={avg_pillars:3.2f}) | "
        f"Coasian Trades/Game: {avg_trades:4.1f} | 4P SS2 Rate: {ss2_4p:4.1f}% (Turn {ss2_turn_4p:4.1f})"
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

        if lead_chg < 1.5 and t10_hold > 75:
            regime_tag = "RUNAWAY SLOG"
        elif lead_chg > 8.0 and reign < 2.2:
            regime_tag = "STOCHASTIC PING-PONG"
        else:
            regime_tag = "DYNAMIC MULTI-ERA ARCS"

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
        res_p = [simulate_single_game(rng, cfg, sub_strats, deck_counts=tranche_counts) for _ in range(cfg.n_games)]
        print(
            f"  P={p_count} Players: SS2={np.mean([r['ss2_reached'] for r in res_p])*100:4.1f}% "
            f"(Turn {np.mean([r['ss2_turn'] for r in res_p]):4.1f}) | "
            f"Beat Finland={np.mean([r['beat_finland'] for r in res_p])*100:4.1f}% | "
            f"Trades={np.mean([r['total_trades'] for r in res_p]):4.1f} | "
            f"Per-Capita={np.mean([r['per_capita_score'] for r in res_p]):5.1f} pts"
        )

    print("\n=== 3. SYMMETRIC OPENING-HAND FAIRNESS: 80-CARD SINGLETON VS. 100-CARD TRANCHE + TRADING ===")
    sym_strats = ["constructive", "constructive", "constructive", "feral_spoiler"]
    singleton_counts = load_deck_counts_from_yaml(singleton_override=True)
    for mode_label, t_on, tr_on, c_map in [
        ("80-Card Singleton Shoe (1x Binary, No Trade)", False, False, singleton_counts),
        (f"{total_shoe}-Card Tranche Shoe (50/25/25%, No Trade)", True, False, tranche_counts),
        (f"{total_shoe}-Card Tranche Shoe (50/25/25% + Coasian Trade)", True, True, tranche_counts),
    ]:
        c_sub = SimConfig(n_games=cfg.n_games, tranche_deck_enabled=t_on, coasian_trading_enabled=tr_on)
        r_sub = [simulate_single_game(rng, c_sub, sym_strats, deck_counts=c_map) for _ in range(cfg.n_games)]
        p0_wins = [float(np.argmax(r["player_mana"]) == 0) for r in r_sub]
        have_w = [w for w, r in zip(p0_wins, r_sub) if r["p0_t1_tamariki"] > 0.5]
        miss_w = [w for w, r in zip(p0_wins, r_sub) if r["p0_t1_tamariki"] < 0.5]
        gap = (np.mean(have_w) - np.mean(miss_w)) * 100 if (have_w and miss_w) else 0.0
        print(
            f"  {mode_label:<46s} -> T1Have={len(have_w)/len(r_sub)*100:4.1f}% | "
            f"Win|Have={np.mean(have_w)*100:4.1f}% vs Win|Miss={np.mean(miss_w)*100:4.1f}% (Gap={gap:+5.1f}pp) | "
            f"G12<=T5={np.mean([r['timely_g12'] for r in r_sub])*100:5.1f}% | "
            f"3Gate={np.mean([r['full_3gate'] for r in r_sub])*100:5.1f}%"
        )


if __name__ == "__main__":
    main()