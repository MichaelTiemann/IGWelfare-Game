#!/usr/bin/env python3
"""
Foils & Founders: 20-Turn Coopetitive Monte Carlo Balance Simulator
===================================================================
Evaluates:
  1. 4-Player Mixed Strategy Balance (Hub Builder, Finisher, Arbitrageur, Bystander, Feral Spoiler)
  2. 2-Player to 6-Player Scaling (Unadjusted vs. P-Normalized Rules)
  3. Endogenous D20 Hazard Windows & 1-Turn Emergency Judo Counters
  4. Chasing Finland Automa Match Race (Cohesion 81.0 -> 126.0 vs. Finland 88.0 -> 107.2)

Author: Michael Tiemann / IGWelfare-Game
License: GPL-3.0-or-later / MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np


@dataclass
class SimConfig:
    n_games: int = 5_000
    n_turns: int = 20               # 60 years (3 years/turn)
    n_players: int = 4
    normalized_scaling: bool = True
    seed_mana: float = 3.0
    abolish_impossible_bonus: float = 5.0
    bystander_forfeit_ss1: float = 2.0
    bystander_forfeit_ss2: float = 3.0
    feral_backfire_forfeit: float = 2.0
    tier_mana: Tuple[float, float, float] = (1.0, 2.0, 4.5)
    finland_start: float = 88.0
    nz_start: float = 81.0
    rng_seed: int = 20261028


@dataclass
class PlayerState:
    strategy: str
    mana: float
    wealth: float
    init_mana: float = 0.0
    royalty_mana: float = 0.0
    legacy_mana: float = 0.0
    forfeit_mana: float = 0.0
    river_tiers_enacted: List[int] = field(default_factory=list)
    ages: List[int] = field(default_factory=lambda: [12, 1])
    stunted_flags: List[bool] = field(default_factory=lambda: [False, False])


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


def simulate_single_game(
    rng: np.random.Generator,
    cfg: SimConfig,
    strategies: List[str],
    table_mode: str = "mixed",
) -> Dict[str, float | List[float]]:
    n_p = len(strategies)
    players: List[PlayerState] = []
    for s in strategies:
        w0, stunted = roll_d20_birth(rng, front_foil_active=False)
        players.append(PlayerState(strategy=s, mana=cfg.seed_mana, wealth=w0 * 2.0, stunted_flags=[False, stunted]))

    subsystems_done = [False, False, False]  # [Front Foil, Wing-Sail, Rear T-Foil]
    ss_regime = 0
    ss2_turn = cfg.n_turns + 1
    stunted_births = sum(1 for p in players for st in p.stunted_flags if st)

    finland_cohesion = cfg.finland_start
    nz_cohesion = cfg.nz_start

    # Normalization parameters by player count P
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

    for turn in range(1, cfg.n_turns + 1):
        front_foil, wing_sail, rear_foil = subsystems_done

        # --- PHASE I: Aging, Rebirth, & Earnings ---
        for p in players:
            for c_idx in range(2):
                p.ages[c_idx] += 1
                if p.ages[c_idx] == 7 and not wing_sail and rng.random() < 0.22:
                    p.wealth = max(0.0, p.wealth - 1.5)
                if p.ages[c_idx] >= 30:
                    p.ages[c_idx] = 0
                    _, is_stunted = roll_d20_birth(rng, front_foil_active=front_foil)
                    p.stunted_flags[c_idx] = is_stunted
                    if is_stunted:
                        stunted_births += 1

            adult_count = sum(1 for a in p.ages if a >= 6)
            regime_wealth_bonus = (0.8 if wing_sail else 0.0) + (0.8 if rear_foil else 0.0)
            stunt_penalty = 0.5 if any(p.stunted_flags) and not front_foil else 1.0
            p.wealth += adult_count * (1.2 + regime_wealth_bonus) * stunt_penalty

        # --- PHASE II: River Exposure & Feral Spoiler Plays ---
        for p in players:
            if p.strategy in ("hub_builder", "shielded_arb") or (p.strategy == "finisher" and turn >= 5):
                if rng.random() < 0.65:
                    p.wealth += 1.0
                    tier_exposed = 0 if p.strategy == "hub_builder" and turn <= 6 else (1 if turn <= 11 else 2)
                    p.river_tiers_enacted.append(tier_exposed)
            elif p.strategy == "feral_spoiler":
                # Feral player attempts a Spoiler Trap if D20 reefs are still open
                open_reefs = sum(1 for done in subsystems_done if not done)
                if open_reefs > 0 and rng.random() < 0.55:
                    p.wealth += 3.0  # Short-term Feral kickback
                    # Check if crew Judo-counters in the 1-Turn Emergency Window
                    crew_shield_prob = 0.78 if any(x.strategy == "shielded_arb" for x in players) else 0.45
                    if rng.random() < crew_shield_prob:
                        loss = min(p.mana, cfg.feral_backfire_forfeit)
                        p.mana -= loss
                        p.forfeit_mana += loss

        # --- PHASE III: Subsystem Completions & D20 Hazard Check ---
        for sub_idx in range(3):
            if not subsystems_done[sub_idx]:
                ready_turn = [2, 5, 9][sub_idx]
                if table_mode == "hoarders":
                    ready_turn += 4
                elif table_mode == "bystanders":
                    ready_turn += 9

                if turn >= ready_turn and rng.random() < min(0.92, 0.52 * river_visibility_boost):
                    weights = np.array([
                        3.0 if p.strategy == "hub_builder" and sub_idx == 0 else
                        3.5 if p.strategy == "finisher" and sub_idx >= 1 else
                        2.5 if p.strategy == "shielded_arb" else 0.15
                        for p in players
                    ])
                    weights /= weights.sum()
                    init_idx = int(rng.choice(n_p, p=weights))
                    initiator = players[init_idx]

                    # Endogenous D20 Vulnerability Window Check (saved by shields)
                    d20_hazard = int(rng.integers(1, 21))
                    vuln_cutoff = 6 if not front_foil else (4 if (turn % 3 == 0 and not rear_foil) else 2)
                    saved_by_emergency_window = (table_mode in ("mixed", "balanced")) and (rng.random() < 0.85)

                    if d20_hazard > vuln_cutoff or saved_by_emergency_window:
                        subsystems_done[sub_idx] = True
                        n_done = sum(subsystems_done)
                        mu = 2.0 if n_done == 2 else (3.0 if n_done == 3 else 1.0)
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
                                    royalty = mu * cfg.tier_mana[0]
                                    initiator.mana += royalty
                                    initiator.royalty_mana += royalty
                                continue
                            if other.strategy not in ("bystander", "feral_spoiler") and rng.random() < 0.78:
                                r_tier = other.river_tiers_enacted[0] if other.river_tiers_enacted else 0
                                royalty = mu * cfg.tier_mana[r_tier]
                                other.mana += royalty
                                other.royalty_mana += royalty
                                if sub_idx == 0 and other.strategy == "hub_builder":
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

        # Standard Turn Combos & Variant B Persistent River Royalties
        royalty_triggers_this_turn = [0] * n_p
        for p_idx, p in enumerate(players):
            if p.strategy not in ("bystander", "feral_spoiler") and rng.random() < 0.55:
                card_tier = 2 if (p.strategy == "finisher" and turn >= 10) else (1 if turn >= 5 else 0)
                base_m = cfg.tier_mana[card_tier]
                p.mana += base_m + 1.0
                p.init_mana += base_m + 1.0
                p.wealth = max(0.0, p.wealth - 1.2)

                # Self-combo royalty in 2-player normalized mode
                if self_combo_allowed and p.river_tiers_enacted and royalty_triggers_this_turn[p_idx] < royalty_cap:
                    if rng.random() < 0.55:
                        p.mana += cfg.tier_mana[0]
                        p.royalty_mana += cfg.tier_mana[0]
                        royalty_triggers_this_turn[p_idx] += 1

                for other_idx, other in enumerate(players):
                    if other_idx != p_idx and other.river_tiers_enacted:
                        if royalty_triggers_this_turn[other_idx] < royalty_cap:
                            hub_count = sum(1 for t in other.river_tiers_enacted if t == 0)
                            if hub_count > 0 and rng.random() < min(0.85, 0.30 * hub_count):
                                other.mana += cfg.tier_mana[0]
                                other.royalty_mana += cfg.tier_mana[0]
                                royalty_triggers_this_turn[other_idx] += 1

        # --- PHASE IV: Chasing Finland Automa Roll ---
        f_roll = int(rng.integers(1, 21))
        finland_cohesion += -0.5 if f_roll <= 5 else (1.0 if f_roll <= 15 else 2.0)

        if ss_regime == 0:
            nz_cohesion += 0.25
        elif ss_regime == 1:
            nz_cohesion += 2.60
        else:
            nz_cohesion = min(126.0, nz_cohesion + 4.20)

    gamma = 0.5 if ss_regime == 0 else (1.0 if ss_regime == 1 else 1.5 + 0.05 * max(0, cfg.n_turns - ss2_turn))
    raw_sum = sum(p.mana + p.wealth for p in players)
    combined_score = raw_sum * gamma

    return {
        "ss1_reached": float(ss_regime >= 1),
        "ss2_reached": float(ss_regime == 2),
        "ss2_turn": float(ss2_turn),
        "stunted_births": float(stunted_births),
        "combined_score": combined_score,
        "per_capita_score": combined_score / n_p,
        "beat_finland": float(nz_cohesion > finland_cohesion),
        "player_mana": [p.mana for p in players],
        "player_wealth": [p.wealth for p in players],
    }


def main() -> None:
    cfg = SimConfig()
    rng = np.random.default_rng(cfg.rng_seed)

    print("=== 1. MIXED 4-PLAYER STRATEGY AUDIT (WITH FERAL SPOILER VARIANT) ===")
    strat_4p = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]
    res_4p = [simulate_single_game(rng, cfg, strat_4p) for _ in range(cfg.n_games)]
    mana_m = np.array([r["player_mana"] for r in res_4p])
    wealth_m = np.array([r["player_wealth"] for r in res_4p])
    m_wins = np.argmax(mana_m, axis=1)
    w_wins = np.argmax(wealth_m, axis=1)

    for i, s in enumerate(strat_4p):
        print(f"  P{i+1} ({s:14s}): Mana={mana_m[:,i].mean():5.1f} (Win {np.mean(m_wins==i)*100:4.1f}%) | "
              f"Wealth={wealth_m[:,i].mean():5.1f} (Win {np.mean(w_wins==i)*100:4.1f}%)")

    print("\n=== 2. PLAYER-COUNT SCALING AUDIT (P = 2 TO 6, NORMALIZED) ===")
    pool = ["hub_builder", "finisher", "shielded_arb", "hub_builder", "finisher", "shielded_arb"]
    for p_count in range(2, 7):
        sub_strats = pool[:p_count]
        res_p = [simulate_single_game(rng, cfg, sub_strats) for _ in range(cfg.n_games)]
        print(f"  P={p_count} Players: SS2={np.mean([r['ss2_reached'] for r in res_p])*100:4.1f}% "
              f"(Turn {np.mean([r['ss2_turn'] for r in res_p]):4.1f}) | "
              f"Beat Finland={np.mean([r['beat_finland'] for r in res_p])*100:4.1f}% | "
              f"Per-Capita Scrabble Score={np.mean([r['per_capita_score'] for r in res_p]):5.1f} pts")


if __name__ == "__main__":
    main()
