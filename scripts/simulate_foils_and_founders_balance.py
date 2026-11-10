#!/usr/bin/env python3
"""
Foils & Founders: 20-Turn Coopetitive Monte Carlo Balance Simulator (v2026.11b)
===============================================================================
Evaluates:
  1. +3 Mana Inverse-Hub Royalty boost for foundational/provincial Hub Builders
  2. 2-Turn "Use-It-Or-Lose-It" Manaaki Decay (0 staked & 0 earned for 2 turns -> -1 Mana)
  3. "Shooting the Moon" Plutocrat Gambit (4-Pillar State Capture vs. Unfortunate Fates)
  4. 2-Player to 6-Player Normalized Scaling & Chasing Finland Match Race

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
    hub_royalty_mana: float = 3.0   # Upgraded from 1.0/2.0 -> 3.0 Mana for Hub Builders!
    bridge_royalty_mana: float = 2.0
    idle_mana_limit: int = 2        # 2 consecutive turns with 0 staked & 0 earned -> -1 Mana
    idle_mana_decay: float = 1.0
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
    kickback_wealth: float = 0.0
    capture_pillars: set = field(default_factory=set)  # Needs {0,1,2,3} to Shoot the Moon!
    idle_mana_turns: int = 0
    init_mana: float = 0.0
    royalty_mana: float = 0.0
    legacy_mana: float = 0.0
    forfeit_mana: float = 0.0
    decay_mana_lost: float = 0.0
    river_tiers_enacted: List[int] = field(default_factory=list)
    ages: List[int] = field(default_factory=lambda: [12, 1])
    struggling_flags: List[bool] = field(default_factory=lambda: [False, False])


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
        w0, struggling = roll_d20_birth(rng, front_foil_active=False)
        players.append(PlayerState(strategy=s, mana=cfg.seed_mana, wealth=w0 * 2.0, struggling_flags=[False, struggling]))

    subsystems_done = [False, False, False]  # [Front Foil, Wing-Sail, Rear T-Foil]
    ss_regime = 0
    ss2_turn = cfg.n_turns + 1
    struggling_births = sum(1 for p in players for st in p.struggling_flags if st)

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

    for turn in range(1, cfg.n_turns + 1):
        front_foil, wing_sail, rear_foil = subsystems_done
        mana_active_this_turn = [False] * n_p

        # --- PHASE I: Aging, Rebirth, & Earnings ---
        for p in players:
            for c_idx in range(2):
                p.ages[c_idx] += 1
                if p.ages[c_idx] == 7 and not wing_sail and rng.random() < 0.22:
                    p.wealth = max(0.0, p.wealth - 1.5)
                if p.ages[c_idx] >= 30:
                    p.ages[c_idx] = 0
                    _, is_struggling = roll_d20_birth(rng, front_foil_active=front_foil)
                    p.struggling_flags[c_idx] = is_struggling
                    if is_struggling:
                        struggling_births += 1

            adult_count = sum(1 for a in p.ages if a >= 6)
            # Active z_h builders earn full SS1/SS2 dividend; passive z_l hoarders face LVT drag if Wing-Sail locks!
            if p.strategy == "feral_spoiler":
                z_mult = 0.55 if wing_sail else 1.15
            else:
                z_mult = 1.0 + (0.45 if wing_sail else 0.0) + (0.45 if rear_foil else 0.0)
            hardship_penalty = 0.5 if any(p.struggling_flags) and not front_foil else 1.0
            p.wealth += adult_count * 1.25 * z_mult * hardship_penalty

        # --- PHASE II: River Exposure & Feral "Shoot the Moon" Capture Attempts ---
        for p_i, p in enumerate(players):
            if p.strategy in ("hub_builder", "shielded_arb") or (p.strategy == "finisher" and turn >= 5):
                if rng.random() < 0.65:
                    p.wealth += 1.0
                    tier_exposed = 0 if p.strategy == "hub_builder" and turn <= 8 else (1 if turn <= 12 else 2)
                    p.river_tiers_enacted.append(tier_exposed)
                    mana_active_this_turn[p_i] = True
            elif p.strategy == "feral_spoiler":
                # Spoiler tries to assemble all 4 Capture Pillars {0:Narrative, 1:Land/Cartel, 2:Labor, 3:Offshore}
                missing = [k for k in range(4) if k not in p.capture_pillars]
                if rng.random() < 0.58:
                    target_pillar = int(rng.choice(missing)) if missing else int(rng.integers(0, 4))
                    # Lobbying for a Capture Pillar costs 1.0W upfront campaign grease, yields +3.0W gross (+2.0W net)
                    p.wealth += 2.0
                    p.kickback_wealth += 2.5
                    # Table tries to Judo-counter—urgency rises sharply if Spoiler already holds 2+ Pillars!
                    urgency = 0.20 if len(p.capture_pillars) >= 2 else 0.0
                    base_block = 0.62 if any(x.strategy == "shielded_arb" for x in players) else 0.40
                    if rng.random() < min(0.88, base_block + urgency):
                        loss = min(p.mana, cfg.feral_backfire_forfeit)
                        p.mana -= loss
                        p.forfeit_mana += loss
                    else:
                        p.capture_pillars.add(target_pillar)

        # Locking a Hydrofoil Bay strips the corresponding Capture Pillar unless Spoiler holds all 4!
        if front_foil and len(players[-1].capture_pillars) < 4:
            for sp in players:
                sp.capture_pillars.discard(2)  # Labor/Hardship squeeze broken
        if wing_sail and len(players[-1].capture_pillars) < 4:
            for sp in players:
                sp.capture_pillars.discard(1)  # Land/Cartel extraction broken

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
                        3.4 if p.strategy == "hub_builder" and sub_idx == 0 else
                        3.2 if p.strategy == "finisher" and sub_idx >= 1 else
                        2.6 if p.strategy == "shielded_arb" else 0.10
                        for p in players
                    ])
                    weights /= weights.sum()
                    init_idx = int(rng.choice(n_p, p=weights))
                    initiator = players[init_idx]
                    mana_active_this_turn[init_idx] = True

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
                                    royalty = cfg.hub_royalty_mana
                                    initiator.mana += royalty
                                    initiator.royalty_mana += royalty
                                continue
                            if other.strategy not in ("bystander", "feral_spoiler") and rng.random() < 0.78:
                                r_tier = other.river_tiers_enacted[0] if other.river_tiers_enacted else 0
                                base_roy = cfg.hub_royalty_mana if r_tier == 0 else cfg.bridge_royalty_mana
                                royalty = base_roy * (1.5 if n_done >= 2 else 1.0)
                                other.mana += royalty
                                other.royalty_mana += royalty
                                mana_active_this_turn[other_idx] = True
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

        # Standard Turn Combos & Upgraded +3 Mana Inverse-Hub River Royalties
        royalty_triggers_this_turn = [0] * n_p
        for p_idx, p in enumerate(players):
            if p.strategy not in ("bystander", "feral_spoiler") and rng.random() < 0.55:
                card_tier = 2 if (p.strategy == "finisher" and turn >= 11) else (1 if turn >= 5 else 0)
                base_m = cfg.tier_mana[card_tier]
                p.mana += base_m + 1.0
                p.init_mana += base_m + 1.0
                p.wealth = max(0.0, p.wealth - 1.1)
                mana_active_this_turn[p_idx] = True

                if self_combo_allowed and p.river_tiers_enacted and royalty_triggers_this_turn[p_idx] < royalty_cap:
                    if rng.random() < 0.55:
                        p.mana += cfg.hub_royalty_mana
                        p.royalty_mana += cfg.hub_royalty_mana
                        royalty_triggers_this_turn[p_idx] += 1

                for other_idx, other in enumerate(players):
                    if other_idx != p_idx and other.river_tiers_enacted:
                        if royalty_triggers_this_turn[other_idx] < royalty_cap:
                            hub_count = sum(1 for t in other.river_tiers_enacted if t == 0)
                            bridge_count = sum(1 for t in other.river_tiers_enacted if t == 1)
                            if hub_count > 0 and rng.random() < min(0.85, 0.32 * hub_count):
                                other.mana += cfg.hub_royalty_mana
                                other.royalty_mana += cfg.hub_royalty_mana
                                royalty_triggers_this_turn[other_idx] += 1
                                mana_active_this_turn[other_idx] = True
                            elif bridge_count > 0 and rng.random() < min(0.65, 0.25 * bridge_count):
                                other.mana += cfg.bridge_royalty_mana
                                other.royalty_mana += cfg.bridge_royalty_mana
                                royalty_triggers_this_turn[other_idx] += 1
                                mana_active_this_turn[other_idx] = True

        # --- NEW RULE: 2-Turn "Use-It-Or-Lose-It" Manaaki Decay ---
        for p_idx, p in enumerate(players):
            if mana_active_this_turn[p_idx]:
                p.idle_mana_turns = 0
            else:
                p.idle_mana_turns += 1
                if p.idle_mana_turns >= cfg.idle_mana_limit:
                    decay = min(p.mana, cfg.idle_mana_decay)
                    p.mana -= decay
                    p.decay_mana_lost += decay
                    p.idle_mana_turns = 0  # Reset 2-turn clock after decay tick

        # --- PHASE IV: Chasing Finland Automa Roll ---
        f_roll = int(rng.integers(1, 21))
        finland_cohesion += -0.5 if f_roll <= 5 else (1.0 if f_roll <= 15 else 2.0)
        nz_cohesion = min(126.0, nz_cohesion + (0.25 if ss_regime == 0 else (2.60 if ss_regime == 1 else 4.20)))

    # --- ENDGAME: Check "Shoot the Moon" (4/4 Capture Pillars) vs. Unfortunate Fates ---
    moon_shot_winner = -1
    for idx, p in enumerate(players):
        if p.strategy == "feral_spoiler":
            if len(p.capture_pillars) == 4:
                moon_shot_winner = idx
                p.wealth *= 1.35  # Plutocrat's Monopoly Crown!
            else:
                # Failed Moon-Shot -> Suffers Unfortunate Fate (1989 Bubble Pop + IRD/ComCom Clawback at 0 Mana)
                if wing_sail:
                    p.wealth *= 0.68  # Fate 1: Un-rotated z_l dirt deflates under B:08 LVT
                if rear_foil and p.mana < 2.0:
                    p.wealth = max(0.0, p.wealth - 0.55 * p.kickback_wealth)  # Fate 2: ComCom/IRD clawback
                if ss_regime == 0:
                    p.wealth *= 0.50  # Fate 3: King of the Ashes sovereign collapse

    gamma = 0.5 if ss_regime == 0 else (1.0 if ss_regime == 1 else 1.5 + 0.05 * max(0, cfg.n_turns - ss2_turn))
    raw_sum = sum(p.mana + p.wealth for p in players)
    combined_score = raw_sum * gamma

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
    }


def main() -> None:
    cfg = SimConfig()
    rng = np.random.default_rng(cfg.rng_seed)

    print("=== 1. REBALANCED 4-PLAYER AUDIT (+3 HUB ROYALTY, 2-TURN MANA DECAY, SHOOT-THE-MOON) ===")
    strat_4p = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]
    res_4p = [simulate_single_game(rng, cfg, strat_4p) for _ in range(cfg.n_games)]
    mana_m = np.array([r["player_mana"] for r in res_4p])
    wealth_m = np.array([r["player_wealth"] for r in res_4p])
    decay_m = np.array([r["player_decay"] for r in res_4p])
    m_wins = np.argmax(mana_m, axis=1)
    w_wins = np.argmax(wealth_m, axis=1)
    moon_rate = np.mean([r["moon_shot"] for r in res_4p]) * 100

    for i, s in enumerate(strat_4p):
        print(
            f"  P{i+1} ({s:14s}): Mana={mana_m[:,i].mean():5.1f} (Win {np.mean(m_wins==i)*100:4.1f}%, "
            f"IdleDecay={decay_m[:,i].mean():3.1f}) | "
            f"Wealth={wealth_m[:,i].mean():5.1f} (Win {np.mean(w_wins==i)*100:4.1f}%)"
        )
    print(f"  -> Feral 'Shoot-the-Moon' (4/4 Capture Pillars) Rate: {moon_rate:4.1f}% of games")

    print("\n=== 2. PLAYER-COUNT SCALING AUDIT (P = 2 TO 6, NORMALIZED) ===")
    pool = ["hub_builder", "finisher", "shielded_arb", "hub_builder", "finisher", "shielded_arb"]
    for p_count in range(2, 7):
        sub_strats = pool[:p_count]
        res_p = [simulate_single_game(rng, cfg, sub_strats) for _ in range(cfg.n_games)]
        print(
            f"  P={p_count} Players: SS2={np.mean([r['ss2_reached'] for r in res_p])*100:4.1f}% "
            f"(Turn {np.mean([r['ss2_turn'] for r in res_p]):4.1f}) | "
            f"Beat Finland={np.mean([r['beat_finland'] for r in res_p])*100:4.1f}% | "
            f"Per-Capita Score={np.mean([r['per_capita_score'] for r in res_p]):5.1f} pts"
        )


if __name__ == "__main__":
    main()