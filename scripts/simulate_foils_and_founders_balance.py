#!/usr/bin/env python3
"""
Foils & Founders: 20-Turn Coopetitive Monte Carlo Balance Simulator (v2026.11c)
===============================================================================
Evaluates:
  1. +3 Mana Inverse-Hub Royalty boost for foundational/provincial Hub Builders
  2. 2-Turn "Use-It-Or-Lose-It" Manaaki Decay (0 staked & 0 earned for 2 turns -> -1 Mana)
  3. "Shooting the Moon" Plutocrat Gambit with:
       - Strategic Ambiguity (Turns 1-5 seed-capital skim vs. Turn 6-8 reformer pivot)
       - Domino Capture Additionality (easier capture, governance drag, & compounding rents at 2-3 pillars)
       - Global Market D20 Contagion (stochastic tail-risk margin calls on concentrated wealth)
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

    mana_traj: List[List[float]] = []
    wealth_traj: List[List[float]] = []

    for turn in range(1, cfg.n_turns + 1):
        front_foil, wing_sail, rear_foil = subsystems_done
        mana_active_this_turn = [False] * n_p
        mean_wealth = float(np.mean([x.wealth for x in players]))

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
            # Active z_h builders earn full SS1/SS2 dividend; passive z_l hoarders face LVT drag if Wing-Sail locks
            # UNLESS they hold Land/Cartel + Narrative/Offshore capture (>=3 pillars shields LVT drag)!
            if p.strategy == "feral_spoiler":
                z_mult = 0.55 if (wing_sail and len(p.capture_pillars) < 3) else 1.15
            else:
                z_mult = 1.0 + (0.45 if wing_sail else 0.0) + (0.45 if rear_foil else 0.0)
            hardship_penalty = 0.5 if any(p.struggling_flags) and not front_foil else 1.0
            p.wealth += adult_count * 1.25 * z_mult * hardship_penalty

        # --- PHASE II: River Exposure, Strategic Ambiguity, & Domino Capture ---
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
                # Constructive players can still expose a River card on the rest of their turn; Spoiler stops here
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

            # 3. Standard Constructive River Exposure vs. Feral Domino Capture (Pillars 2 -> 3 -> 4)
            if p.strategy in ("hub_builder", "shielded_arb") or (p.strategy == "finisher" and turn >= 5):
                if rng.random() < 0.65:
                    p.wealth += 1.0
                    tier_exposed = 0 if p.strategy == "hub_builder" and turn <= 8 else (1 if turn <= 12 else 2)
                    p.river_tiers_enacted.append(tier_exposed)
                    mana_active_this_turn[p_i] = True

            elif p.strategy == "feral_spoiler":
                # Spoiler escalates toward all 4 Capture Pillars {0:Narrative, 1:Land/Cartel, 2:Labor, 3:Offshore}
                missing = [idx_p for idx_p in range(4) if idx_p not in p.capture_pillars]
                k_now = len(p.capture_pillars)
                lobby_cost = 1.2 * k_now  # Buying state capture requires real upfront campaign capital!
                if missing and p.wealth >= lobby_cost:
                    attempt_p = cfg.pillar_attempt_probs[k_now]
                    # Economic Additionality: out-wealthing the table buys extra lobbying leverage
                    if p.wealth > 1.20 * mean_wealth:
                        attempt_p = min(0.92, attempt_p + 0.06)

                    if rng.random() < attempt_p:
                        target_pillar = int(rng.choice(missing))
                        p.wealth -= lobby_cost  # Spend upfront lobbying grease

                        # If k_now == 0 (missed early skim), Pillar 1 still slips under ambiguity radar
                        if k_now == 0:
                            p.capture_pillars.add(target_pillar)
                            p.wealth += 2.2
                            p.kickback_wealth += 2.2
                        else:
                            # Governance Additionality: Capture 2 pillars and the 3rd is easier; at 3, the 4th barely needs a touch!
                            arb_indices = [
                                idx_x for idx_x, x in enumerate(players)
                                if x.strategy == "shielded_arb" and x.wealth >= 1.2 * k_now
                            ]
                            base_block = cfg.crew_base_shield if arb_indices else 0.48
                            # Each pillar above 1 erodes civic counter-power; completed SS2 boosts institutional defense
                            effective_block = (
                                base_block
                                - cfg.governance_erosion_per_pillar * (k_now - 1)
                                + (0.20 if ss_regime == 2 else 0.0)
                            )
                            effective_block = float(np.clip(effective_block, 0.10, 0.88))

                            if rng.random() < effective_block:
                                # Crew successfully Judo-counters! Watchdog earns Mana; Spoiler's bribe is burned!
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
                                # Capture succeeds! Reap kickback windfall
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
        # Active capture slows down reform readiness and clouds River visibility!
        capture_turn_delay = 0 if max_pillars_held <= 1 else (1 if max_pillars_held == 2 else (3 if max_pillars_held == 3 else 5))
        capture_vis_mult = 1.0 if max_pillars_held <= 1 else (0.85 if max_pillars_held == 2 else (0.52 if max_pillars_held == 3 else 0.22))

        for sub_idx in range(3):
            if not subsystems_done[sub_idx]:
                ready_turn = [2, 5, 9][sub_idx] + capture_turn_delay
                if table_mode == "hoarders":
                    ready_turn += 4
                elif table_mode == "bystanders":
                    ready_turn += 9

                if turn >= ready_turn and rng.random() < min(0.92, 0.52 * river_visibility_boost * capture_vis_mult):
                    weights = np.array([
                        3.4 if p.strategy == "hub_builder" and sub_idx == 0 else
                        3.4 if p.strategy == "finisher" and sub_idx >= 1 else
                        2.8 if p.strategy == "shielded_arb" else 0.10
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

                        # ONE-TIME LEGISLATIVE RESET: Enacting a Hydrofoil Bay strips its matching Capture Pillar
                        # UNLESS the Hoarder has already locked all 4/4 Pillars (full Crown immunity)!
                        for sp in players:
                            if len(sp.capture_pillars) < 4:
                                if sub_idx == 0:
                                    sp.capture_pillars.discard(2)  # Front Foil breaks Labor/Hardship squeeze
                                elif sub_idx == 1:
                                    sp.capture_pillars.discard(1)  # Wing-Sail LVT breaks Land/Cartel extraction
                                elif sub_idx == 2:
                                    sp.capture_pillars.discard(0)  # Rear T-Foil breaks Narrative/Myopia fog

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
                                # Standing on the Shoulders of Hubs: Tier-0 foundations earn co-credit when SS1/SS2 launches!
                                foundation_dividend = (1.6 * hub_c) if n_done >= 2 else 0.0
                                royalty = base_roy * (1.5 if n_done >= 2 else 1.0) + foundation_dividend
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
                            if hub_count > 0 and rng.random() < min(0.85, 0.30 * hub_count):
                                other.mana += cfg.hub_royalty_mana
                                other.royalty_mana += cfg.hub_royalty_mana
                                royalty_triggers_this_turn[other_idx] += 1
                                mana_active_this_turn[other_idx] = True
                            elif bridge_count > 0 and rng.random() < min(0.70, 0.28 * bridge_count):
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

        # --- PHASE IV: Global Market D20 Contagion & Chasing Finland Automa Roll ---
        # As wealth concentrates & capture pillars leverage hot offshore capital, the D20 comes back to bite!
        d20_global = int(rng.integers(1, 21))
        max_k_end = max((len(p.capture_pillars) for p in players), default=0)
        contagion_cutoff = 1 + max(0, max_k_end - 1) + (1 if ss_regime == 0 and turn >= 10 else 0) - (1 if subsystems_done[2] else 0)
        if d20_global <= max(1, contagion_cutoff):
            curr_mean_w = float(np.mean([x.wealth for x in players]))
            for p in players:
                if p.wealth > cfg.global_wealth_threshold and p.wealth > 1.18 * curr_mean_w:
                    k_p = len(p.capture_pillars)
                    if k_p == 4:
                        # Even 4/4 Sovereign Capture faces Sovereign Bond / FX Contagion on D20 <= 2!
                        if d20_global <= 2:
                            p.wealth *= 0.72
                            cracked = int(rng.choice(list(p.capture_pillars)))
                            p.capture_pillars.discard(cracked)
                            p.contagion_hits += 1
                    elif k_p >= 2:
                        # Unfinished Leveraged Hoarder gets Margin-Called by Global Markets!
                        p.wealth *= 0.64
                        stripped = int(rng.choice(list(p.capture_pillars)))
                        p.capture_pillars.discard(stripped)
                        p.contagion_hits += 1
                    elif p.strategy != "shielded_arb":
                        # Mild external liquidity haircut on unhedged concentrated wealth
                        p.wealth *= 0.90
                        p.contagion_hits += 1

        f_roll = int(rng.integers(1, 21))
        finland_cohesion += -0.5 if f_roll <= 5 else (1.0 if f_roll <= 15 else 2.0)
        # Deep state capture (>=3 pillars) also drags on NZ social cohesion gains!
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
                p.wealth *= 1.25  # Plutocrat's Monopoly Crown!
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

    # Update final Turn-20 wealth snapshot after Endgame Moon-Shot / Unfortunate Fate reckoning
    if wealth_traj:
        wealth_traj[-1] = [p.wealth for p in players]

    mana_dyn = compute_lead_dynamics(np.array(mana_traj))
    wealth_dyn = compute_lead_dynamics(np.array(wealth_traj))

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
        "mana_dyn": mana_dyn,
        "wealth_dyn": wealth_dyn,
    }


def main() -> None:
    cfg = SimConfig()
    rng = np.random.default_rng(cfg.rng_seed)

    print("=== 1. REBALANCED 4-PLAYER AUDIT (DOMINO CAPTURE, AMBIGUITY, & GLOBAL D20 CONTAGION) ===")
    strat_4p = ["hub_builder", "finisher", "shielded_arb", "feral_spoiler"]
    res_4p = [simulate_single_game(rng, cfg, strat_4p) for _ in range(cfg.n_games)]
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

    for i, s in enumerate(strat_4p):
        print(
            f"  P{i+1} ({s:14s}): Mana={mana_m[:,i].mean():5.1f} (Win {np.mean(m_wins==i)*100:4.1f}%, "
            f"IdleDecay={decay_m[:,i].mean():3.1f}) | "
            f"Wealth={wealth_m[:,i].mean():5.1f} (Win {np.mean(w_wins==i)*100:4.1f}%, "
            f"D20Shocks={contagion_m[:,i].mean():3.2f})"
        )
    print(
        f"  -> Feral 'Shoot-the-Moon' (4/4 Pillars): {moon_rate:4.1f}% (Avg Final Pillars={avg_pillars:3.2f}) | "
        f"4P Table SS2 Rate: {ss2_4p:4.1f}% (Turn {ss2_turn_4p:4.1f})"
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
        era_mat = np.array([d["era_leaders"] for d in dyns])  # (N, 3)

        # Classify qualitative feel automatically
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
        res_p = [simulate_single_game(rng, cfg, sub_strats) for _ in range(cfg.n_games)]
        print(
            f"  P={p_count} Players: SS2={np.mean([r['ss2_reached'] for r in res_p])*100:4.1f}% "
            f"(Turn {np.mean([r['ss2_turn'] for r in res_p]):4.1f}) | "
            f"Beat Finland={np.mean([r['beat_finland'] for r in res_p])*100:4.1f}% | "
            f"Per-Capita Score={np.mean([r['per_capita_score'] for r in res_p]):5.1f} pts"
        )


if __name__ == "__main__":
    main()
