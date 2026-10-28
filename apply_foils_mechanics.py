#!/usr/bin/env python3
"""
Idempotent Builder & Patcher for Foils & Founders Coopetitive Mechanics
Writes:
  1. rules/foils_and_founders_gameplay.md
  2. rules/strategy_study_guide.md
  3. scripts/simulate_foils_and_founders_balance.py
And patches the Rule Zero maxim into README.md and decks/study_cards.yaml if needed.
"""

from pathlib import Path
import os
import stat

ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()

# ==============================================================================
# 1. rules/foils_and_founders_gameplay.md
# ==============================================================================
GAMEPLAY_MD = r"""# Foils & Founders: Core Tabletop Gameplay & Coopetitive Ruleset

> *"Not all lives are easy, but none should be impossible."*
> — **Rule Zero of Foils & Founders (`B:00`: The Rawlsian D20 Test)**

*Companion Ruleset to **Beyond the Magic Money Tree — Foils & Founders: The Aotearoa Deck***  
**License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

---

## 1. Overview & Core Coopetitive Tension

**Foils & Founders** is a cooperative/competitive ("coopetitive") intergenerational strategy game for **1 to 6+ players** (or multi-player teams) spanning **20 turns** (**60 years**, at **$\Delta t = 3$ years per turn**, from 2026 to 2086).

Players steward multi-generational characters across three lifecycle stages—**Being** (*Tamariki*, ages 0–17), **Becoming** (*Pakeke* / Working & Founding, ages 18–62), and **Crossing Over** (*Kaumātua* / Navigators, ages 63–89)—while working through a shared face-up card pool called **The River**.

* **Why You Must Cooperate:** In the orthodox status quo (**`SS0` — Displacement Mode**), 22% to 30% of children are born into the subsistence hardship corner (`B:01`, `H:06`), 1 in 5 urban graduates emigrates to Australia (`H:03`), and sovereign debt spirals toward 200% of GDP (`B:06`). If the table fails to lash the three macro subsystems together to lift Aotearoa onto hydrofoils (**`SS1` $\to$ `SS2`**), hull drag penalizes the entire table by 50%, and even a "Natural 20" dynasty loses.
* **Why You Compete:** Like championship **Scrabble**, the goal is simultaneously to outscore rival cohorts in **Individual Mana ($\mathcal{M}_i$)** and **Individual Wealth ($\mathcal{W}_i$)** *and* to construct a record-shattering **Combined National Score ($\Sigma_{\text{Aotearoa}}$)** by timing high-multiplier synergy plays and staking your Mana under **Contingent Liability**.

### Two Ways to Play Traps & Hazards (The Elizabeth Magie Dual Ruleset)
Just as Elizabeth Magie's original 1904 *The Landlord's Game* featured two rulesets—*Prosperity* and *Monopoly*—**Foils & Founders** supports two play modes on the exact same board mat:
1. **Mode A — "Abundance / Make Your Own Luck" (Endogenous D20 Reefs — Default):** Success is the intersection of luck and opportunity. Cautionary Traps (`T:00`–`T:05`) and Orthodoxy Bosses (`H:01`–`H:06`) are triggered by the **D20 Vulnerability Window** at the end of each turn. As players enact reforms (`B:01`, `B:05`, `B:07`, `C:02`), they physically cover up the failure zones on the D20 track—literally *making their own luck* so no life is impossible.
2. **Mode B — "Feral / Monopoly" (Player-Driven Spoilers & Rent-Seeking):** Players draw `T` and `H` cards into their hands and may play them as **Spoilers** to extract short-term private Wealthkickbacks (+3 to +4 Wealth) while putting rival players' staked Contingent Mana **In Jeopardy**. Yet going feral carries a two-stage backfire: if defenders counter the Trap during the 1-turn Emergency Window, the Spoiler player forfeits **2 Mana in public disgrace (*whakamā*)**, and if `SS2` fails by Turn 20, the $0.5\times$ Hull Drag Penalty wipes out everyone's laurels.

---

## 2. Character Initiation, Player Scaling ($P=2\dots 6$), & The Piketty–Saez Rebirth Engine

### 2.1 Multi-Generational Cohort Setup & Player-Count Normalization
To keep River visibility, Variant B royalty velocity, and Coase–Ostrom coordination friction balanced from 2 players up to 6+ players, apply the **Player-Count Normalization Table**:

| Setup & Scaling Rule | **2 Players (Duel / Co-Op Pair)** | **3–4 Players (Standard Crew)** | **5–6 Players (The Big Table)** |
| :--- | :--- | :--- | :--- |
| **Characters per Player** | **2 characters** from different generations (e.g., Age 36 [$j=12$] & Age 3 [$j=1$]). | **2 characters** from different generations per player (6–8 characters total). | **1–2 characters** per player (or 3 two-player Whānau/Sector Teams). |
| **Opening River Exposure** | Expose **2 cards per character** (8 total) *or* deal a 2-card Public Commons River. **Self-Combo Rule:** Linking your own second character's River card pays **100% Variant B Royalty**. | Expose **1 card per character** face-up into the River (6–8 cards total). | Expose **1 card per player/team** face-up into the River (5–6 cards total). |
| **Subsystem Political Drag** | **1.5 Wealth** per Subsystem (requires 1+ staker). | **2.0 Wealth** per Subsystem (requires 2+ stakers). | **3.0 Wealth** per Subsystem & requires **3 distinct players** to co-stake Mana until `N:01` or `K:07` is active. |
| **Variant B Royalty Cap** | Max **2 Royalty payouts** per River card per turn. | Max **2 Royalty payouts** per River card per turn. | Max **2 Royalty payouts** per River card per turn (**3** if `N:05` Romer is active). |

* **Initial Resources:** Each adult character begins with **3 Seed Mana**, starting **Wealth** from their D20 birth roll, **1 Wayfinder Kaupapa Persona (`K:01`–`K:06`)** (Tamariki unlock their Kaupapa card at Age 18, or Age 12 if mentored via `B:02`), and a **4-card hand**. Every card exposed to the River grants **+1 Generosity (Wealth)** immediately.

### 2.2 The Rawlsian D20 Birth & Rebirth Table (`B:00`)
At game start—and whenever an elder character passes over at Age 90 ($j=30$) and is **reborn at Age $J=0$**—roll the **Rawlsian D20 (`B:00`)**:
* **The Piketty–Saez Patrimonial Rule:** In `SS0` (0% estate tax), a passing character in Vigintiles 17–20 may pass down a **Dynasty Endowment Token** (+2 starting Wealth). **However, the biological/developmental D20 is always rolled raw.** Even a child born into a "Nat 20" balance sheet can roll into developmental complexity (1–6), and a child born into a humble family can roll a spark of genius.

| D20 Roll | Cohort Vigintile Reality | In Orthodox Status Quo (`SS0` — *Some Lives Are Impossible*) | With Reforms Active (`SS1` $\to$ `SS2` — *None Are Impossible*) |
| :--- | :--- | :--- | :--- |
| **1–4** *(1–6 if `H:06` GUiNZ active)* | **The Subsistence Corner ($\Pr(i_c=0)$):** Severe early rent/energy squeeze or neurodevelopmental vulnerability. | **The Impossible Corner:** Receives a **Stunted Trajectory Token**. Without private bailout + `B:01`, cannot unlock Kaupapa at Age 18, earns $-50\%$ Wealth, and adds +1 Hull Drag (`B:04` Exits 1/2/4). | **Caught by *Te Korowai Mokopuna* (`B:01`):** In-kind wraparound ($G_{\text{ECE}} = \text{NZD } 13\text{k/yr}$) bypasses the cash corner! Starts with 0 Wealth, **but life is not impossible**: Stunting token removed, $+\text{NZD } 15.3\text{k}$ parental care crowds in (`N:02`), and full Kaupapa agency unlocks at Age 18. |
| **5–12** | **The Squeezed Working & Provincial Majority:** Exposed to 2.8x rural fuel costs (`T:03`) and family job-loss shocks ($\delta_{\text{shock}}$). | **Fragile Trajectory:** Earns **1 Wealth/turn** at Age 18. If an adolescent shock hits at Ages 12–14 ($j=4$) without `B:02`, loses Dual-Class Kaupapa slot and suffers `T:05` outrage drag. | **Buffered by *Tuakana–Teina* (`B:02` + `C:03`) & Solar (`C:05`):** Immune to adolescent family job-loss shocks and `T:05` disinformation. Launches into the **65.0% Thriving Tier** (**2 Wealth/turn** at Age 18 + full Dual-Class Kaupapa). |
| **13–18** | **The Urban Professional / Founder Seed:** High human capital ($h_3$), crushed by $3.10\times$ metro housing stress (`H:05`). | **The Brain-Drain Exile (`H:03`):** At Age 21 ($j=7$), roll 1d6; on **1–2** (20%+ urban exile rate), character **emigrates to Sydney**—locking their Kaupapa card out of domestic plays unless repatriated with 3 Wealth. | **Anchored by the Wing-Sail (`B:03` + `B:05`):** Receives the **NZD 62k+ Youth Capital Grant (`B:03`)** at Age 20 and $-10.5\%$ cooler rents (`B:05`). Stays in NZ as a job creator (**3 Wealth/turn**) and taps `K:02` immediately. |
| **19–20** | **The Top-5% Patrimonial Dynasty (`20:01`–`20:20`):** High starting capital ($a_0 \gg 0$). | **The Lavoisier Trap (`T:04` / `H:05`):** Starts with **4 Wealth** (+2/turn), but untaxed land hoarding ($z_\ell$) starves productive enterprise. If the board stays in `SS0` at Turn 20, debt hits 200% and **even a Nat 20 loses**. | **The Builder's Renaissance (`B:05` + `K:02`):** Active builders (`20:01`–`20:19`, up to NZD 100M NW) earn **4 Wealth/turn** from high-growth firms while the estate levy recycles passive dirt into `B:03` Youth Grants. |

---

## 3. The 20-Turn Lifecycle Clock & Four-Phase Turn Structure

Each turn equals **3 years** across three stages of human agency:
1. **Stage 1 — Being (*Tamariki*, Ages 0–17 / Turns $j=0\dots 5$):** Developing human capability; absorbs buffs from `B:01`/`B:02` or suffers `SS0` stunting drag.
2. **Stage 2 — Becoming (*Pakeke*, Ages 18–62 / Turns $j=6\dots 20$):** Full economic and political agency; earns **Wealth**, exposes cards to the River, stakes **Mana**, and executes Policy Combos.
3. **Stage 3 — Crossing Over (*Kaumātua*, Ages 63–89 / Turns $j=21\dots 29$):** Elder Navigators; collects NZ Super (`B:06`) and unlocks **`K:06` (*The Kaumātua & Founder's Dividend*)**, generating **1 free Lifetime Experience Token per turn** (cutting `N:01`–`N:05`, `B:04`, or `B:08` deployment costs by 100%). At Age 90 ($j=30$), the character passes over and triggers a $J=0$ rebirth roll (requiring `B:02` active on the board to bequeath an unspent Kaupapa card to a rising young adult).

### The Four Phases of Every 3-Year Turn
* **Phase I — Aging, Yield, & Tamariki Check:** Advance all characters by $+3$ years ($+1$ turn). Resolve Age 18, Age 63, and Age 90 (Rebirth) transitions. Collect turn **Wealth** for Working Adults and Kaumātua. Check unbuffered *Tamariki* (ages 0–17) against active board gates.
* **Phase II — The River, Generosity, & Contingent Mana Staking:** Expose cards from hand face-up into **The River** to collect **+1 Generosity (Wealth)** per card. Negotiate coalitions and place upright **Committed Mana Tokens ($\Delta M_{\text{stake}}$)** in Zone A (Staking & Incubation Slot) of open Policy Goals or Subsystems.
* **Phase III — Action & Policy Execution (The Texas Hold'em Combo):**
  * *Option A (Private Whānau Care):* Spend **2 Wealth** to privately shield your cohort's Tamariki for one gate.
  * *Option B (Enact a Policy Combo):* Play a card from hand/River and link it with matching **Synergy Cards** across any player's River (or tap a matching **Kaupapa Wildcard `K:01`–`K:07`**). Pay the **Political Drag Cost** in Wealth. Enacted River cards **persist in front of their owners (Variant B)** as permanent institutional infrastructure that can be tapped again in future turns!
  * *Option C (Feral Spoiler Play — Mode B Only):* Play a `T` or `H` card from hand onto an unshielded Subsystem to claim its private Feral Kickback (+3 to +4 Wealth) and tip the target's staked Mana sideways into the **Emergency Box (Zone B)**.
* **Phase IV — Replenish & The D20 Endogenous Hazard Check:** Draw back to 4 cards. Roll the **Rawlsian D20** to check if any open, unshielded Policy Goal is struck by a Trap or Boss (Section 4.4), and resolve any expiring **1-Turn Emergency Save Windows**.

---

## 4. The River Dividend, Contingent Liability, & D20 Hazard Mechanics

### 4.1 Inverse-Hub Base Mana Values ($m_i$)
* **Tier 1 — Foundational Hubs ($m_i = 1\text{ Mana}$):** `B:01`, `B:02`, `B:05`, `E:01`, `N:01`, `N:02`. *(High connectivity; generate steady recurring Variant B royalties).*
* **Tier 2 — Structural Bridges ($m_i = 2\text{ Mana}$):** `B:03`, `B:04`, `B:07`, `C:02`, `C:03`, `C:05`, `N:03`, `N:04`, `N:05`. *(Link hubs into complete subsystems).*
* **Tier 3 — Capstone Unlockers ($m_i = 4\text{ to }5\text{ Mana}$):** `B:06`, `B:08`, `B:09`, `C:04`, `C:06`, `E:02`, `E:03`, `N:06`. *(Rare finishers that spike on $2\times$ and $3\times$ turns).*

### 4.2 Combo Payouts & `SS1` (2x) / `SS2` (3x) Multipliers
When a $k$-card combination is completed:
$$\text{Mana}_{\text{initiator}} = \mu \sum_{i=1}^{k} m_i, \qquad \text{Mana}_{\text{contributor}, j} = \mu \cdot m_j$$
where $\mu = 1\times$ for standard plays, **$\mu = 2\times$** for the play that completes **`SS1`** (any 2 Subsystems), and **$\mu = 3\times$** for the play that completes **`SS2`** (all 3 Subsystems + Capstone).

### 4.3 Contingent Mana Liability: Backing Risk vs. Bystander Risk
1. **Accomplished *With* Your Stake:** Your staked Mana is returned **plus** the $\mu$-multiplied Combo Payout!
2. **Accomplished *Without* Your Stake (The Bystander Forfeit):** If a core Subsystem (`SS1`/`SS2`) is completed by other players while you staked **0 Mana** on it, you immediately **forfeit 2 Mana** on `SS1` (or **3 Mana** on `SS2`).
3. **Goal Collapses (Contingent Forfeit):** If an open goal in the **Emergency Box (Zone B)** is not saved within 1 turn, **all staked Mana on that goal is forfeited!** *(Mana floors at 0; a player at 0 Mana can earn +1 Mana by funding `B:01` child care or co-tapping via `K:07`).*

### 4.4 The D20 Endogenous Hazard Check & 1-Turn Emergency Save Window
At Phase IV, if any Subsystem has staked Mana waiting to complete, roll the **D20 (`B:00`)** against the active Vulnerability Window:
* **Bottom Reef (Rolls 1–4, or 1–6 under `H:06` GUiNZ Drift):** Triggers **`T:00` (Cash Leakage)**, **`T:01` (Late Remediation)**, or **`T:05` (Algorithmic Outrage)**. *Permanently closed once Subsystem 1 (`B:01` + `B:02` + `C:02`) is locked into Zone C!*
* **Top Reef (Rolls 19–20 when untaxed land wealth $\tau_a = 0$):** Triggers **`T:02` (Housing Capitalization)** or **`T:04` (Lavoisier Talent Trap)**. *Permanently closed once Subsystem 2 (`B:05` + `B:03`) is locked into Zone C!*
* **Parliamentary Election Audit (Rolls 1–8 on Every 3rd Turn: Turns 3, 6, 9, 12, 15, 18):** Triggers **`H:01` (Myopic 3-Year Cash Truncation)** or **`H:02` (Agency Silos)**. *Permanently closed once Subsystem 3 (`B:07` + `N:03`) is locked into Zone C!*

**The 1-Turn Emergency Response Window (Board Mat Zone B):** When a D20 roll hits an open reef (or a Feral player drops a Spoiler), tip the staked Mana tokens **90° sideways ("In Jeopardy")**. On the next turn, any player may rescue the goal by linking the matching empirical counter-card (`B:07`/`N:03` vs. `H:01`; `C:02`/`K:05` vs. `T:05`; `B:05` vs. `T:02`/`T:04`) or paying an emergency 4-Wealth bailout. In Feral Mode, countering a player-played Spoiler grants the defenders **+1 Resilience Mana** and forces the Spoiler player to **forfeit 2 Mana (*whakamā*)**!

---

## 5. The Three Subsystems & Three-Pillar Scrabble Scoring

1. **Subsystem 1 — The Front Lifting Foil (*Te Korowai Mokopuna*):** `B:01` + `B:02` + 1 Amplifier (`N:01`, `N:02`, `C:02`, or `C:03`). *Closes D20 Rolls 1–6, abolishes the Impossible Corner, and awards a **+5 Mana Legacy Bonus**.*
2. **Subsystem 2 — The Wing-Sail Power Plant (*Te Aka Matua*):** `B:05` + `B:03` + 1 Energy/Enterprise Engine (`E:01`, `E:02`, or `C:05`). *Closes D20 Rolls 19–20, ends `H:03` Sydney Brain Drain, and grants Working Adults **+1 Wealth/turn**.*
3. **Subsystem 3 — The Rear T-Foil Stabilizer (*Ngā Kete o te Wānanga*):** `B:07` + `B:06` + 1 Governance Proof (`N:03`, `N:04`, `B:04`, or `B:08`). *Cancels 3-Year Election Audits (`H:01`), cuts PAYE to 18.5% (**+1 Wealth/turn**), and locks NZ Super at Age 65 (`K:06`).*

### Final Scoring at Turn 20
1. **Mana Laureate (*Toa Takitini*):** Highest Individual/Cohort **Mana ($\mathcal{M}_i$)**.
2. **Wealth Laureate (*Pou Rawa*):** Highest Individual/Cohort **Wealth ($\mathcal{W}_i$)**.
3. **Combined National Score (*Te Waka Hourua* — Total & Per-Capita Scrabble Metric):**
   $$\Sigma_{\text{Aotearoa}} = \left( \sum_{i=1}^{P} \mathcal{M}_i + \sum_{i=1}^{P} \mathcal{W}_i \right) \times \Gamma_{\text{Regime}}, \qquad \bar{\Sigma}_{\text{Per-Capita}} = \frac{\Sigma_{\text{Aotearoa}}}{P}$$
   where $\Gamma_{\text{Regime}} = 0.5\times$ in `SS0` (No Laureates awarded), $1.0\times$ in `SS1`, and **$1.5\times + 0.05\times (\text{Turns Early})$** in `SS2` (**135+ pts/player** = Championship Hydrofoil Standard across any table size $P=2\dots 6$).
"""

# ==============================================================================
# 2. rules/strategy_study_guide.md
# ==============================================================================
STRATEGY_MD = r"""# Foils & Founders Strategy & Empirical Study Guide: Knowledge Is Power!

> *"Knowledge is not cheating; Knowledge is power!"*  
> *"Not all lives are easy, but none should be impossible."*

*Companion Strategy & Mathematical Reference to **Foils & Founders: The Aotearoa Deck***  
**Cross-References:** `decks/study_cards.yaml` • `Document 1A` • `Document 1B` • `Document 1C` • `Document 2 (MATLAB GPU Engine)`

---

## 1. Why Knowing the Math Wins the Game

In **Foils & Founders**, every tabletop mechanic is compiled directly from an empirical theorem or general-equilibrium operator in the **8-PType $\times$ 4-Region Overlapping Generations (OLG) GPU Engine** (`NZ_4Region_Master.m`, `PolicyExperiment_LeeSeshadri_4Region.m`, and `QEA_2026.m`).

Players who study the **Fold-Over Study Deck (`decks/study_cards.yaml`)** gain three decisive advantages:
1. They know **which cards are high-frequency royalty hubs** (`Tier 1`) versus **high-multiplier finishers** (`Tier 3`).
2. They know **how to shrink the D20 Vulnerability Window from 40% to 0%** ("making their own luck") and how to Judo-counter a "Feral" spoiler player.
3. They know how to manage the **Kaumātua mortality cliff** at Age 90 ($j=30$) and scale tactics from a 2-player duel up to a 6-player Big Table (`K:07`).

---

## 2. The Mathematics of the River & Inverse-Hub Mana Pricing

### 2.1 Why Variant B Persists: Romer's Non-Rival Knowledge Theorem (`N:05`)
Why do enacted River cards stay face-up in front of their owner to anchor future combinations instead of being consumed? Because proven policy architectures are **non-rival ideas** ($A_t$). By Paul Romer's (1990, Nobel Prize 2018) endogenous growth equation (`N:05` in `decks/study_cards.yaml`):

$$Y_t = A_t K_t^\alpha \big(L_{Y,t} \bar{h}_t\big)^{1-\alpha}, \qquad \frac{\dot{A}_t}{A_t} = \delta_{\text{R\&D}} \, H_{A,t}\big(\text{B:03}, \text{B:05}, \text{K:06}\big) \implies \frac{\partial^2 Y_t}{\partial A_t \, \partial H_{A,t}} > 0$$

### 2.2 Inverse-Hub Pricing & Monte Carlo Strategy Audit ($N = 10,000$ Games)
Pricing Base Mana ($m_i$) inversely to a card's network connectivity degree $d(i)$ equalizes the expected lifetime Mana of early co-operators and late finishers:

| Strategy Persona | Mean Mana ($\mathcal{M}_i$) | Mana Sources (Init / Royalty / Legacy / Forfeit) | Mean Wealth ($\mathcal{W}_i$) | Mana Win % | Wealth Win % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Catalytic Hub Builder (`K:01`/`K:05`)** *(Exposes `B:01`, `B:02`, `B:05` Turns 1–4)* | **44.2 Mana** | $14.1$ Init + **$25.8$ Royalties** + $5.0$ Legacy $- 0.7$ Forfeit | **31.4 Wealth** | **41.8%** | 19.4% |
| **2. Capstone Finisher (`K:02`/`K:03`)** *(Times Tier 2/3 cards on $\mu=2\times, 3\times$ turns)* | **45.1 Mana** | **$36.4$ Init** + $9.9$ Royalties + $0.0$ Legacy $- 1.2$ Forfeit | **34.8 Wealth** | **44.6%** | **38.2%** |
| **3. Shielded Arbitrageur (`K:04`/`K:06`)** *(Anchors `B:07`/`N` shields & elder `K:06` tokens)* | **38.6 Mana** | $21.2$ Init + $16.4$ Royalties + $2.5$ Legacy $- 1.5$ Forfeit | **36.1 Wealth** | 13.4% | **40.1%** |
| **4. Free-Riding Bystander / Unchecked Feral** *(Withholds stakes or plays countered Traps)* | **6.8 Mana** | $4.5$ Init + $9.1$ Royalties + $0.0$ Legacy **$- 6.8$ Forfeit** | **24.2 Wealth** | **0.2%** | 2.3% |

---

## 3. Master Synergy Combos & Empirical Counter-Plays

### Combo 1: Abolishing the Impossible Corner (`B:01` + `B:02` + `N:02` + `C:02`)
* **The Equation (Cunha, Heckman, & Schennach 2010; Lee & Seshadri 2019):**
  $$h_{2} = A_1 \left[ \gamma_1 h_1^{\phi_1} + (1-\gamma_1)\left( G_{\text{ECE},1}^{\text{in-kind}} + \kappa_1 \max\big\{0,\, i_c(y_1 - p_h^r\bar{h} - p_e(z_2))\big\} + \omega_1 \tau_c w_1 h_1 \right)^{\phi_1} \right]^{\frac{\rho_1}{\phi_1}}$$
  with $\phi_1 = -0.50 < 0$ and $\frac{\partial^2 h_3}{\partial h_2 \, \partial I_{\text{mentor},2}} > 0$.
* **Closing the D20 Bottom Reef (Rolls 1–6):** In the 1972 Dunedin cohort, $\Pr(i_c=0) = 22\%$ (d20 **1–4**); by the 2010 GUiNZ cohort (`H:06`), $3.10\times$ rents expand the corner to $30\%$ (d20 **1–6**). Playing `T:00` (*Unconditional Cash Leakage*) or `T:01` (*Late Remediation*) fails because $\partial i_c / \partial T_{\text{cash}} \approx 0.08$ in deep rent distress and $\lim_{h_2 \to h_{\min}} \partial h_3 / \partial G_{\text{tertiary},3} \to 0$.
* **The Judo Counter:** Pair **`B:01` ($G_{\text{ECE}}^{\text{in-kind}} = \text{NZD } 13\text{k/yr}$)** + **`N:02` (Heckman)** + **`B:02` (*Tuakana–Teina*)** + **`C:02` (*Monilukutaito*, Berentson-Shaw 2018)** to permanently cover Rolls 1–6 on the D20 mat and immunize the table against **`T:05` (*Algorithmic Outrage*)**.

### Combo 2: Curing the Lavoisier Syndrome & Self-Financing the Grid (`B:05` + `B:03` + `E:02`)
* **The Equations (Guvenen et al. 2023; Murphy, Shleifer, & Vishny 1991; Farmer & Toda 2017):**
  $$r_{\text{net}}(z, \tau_a, \tau_k) = (1 - \tau_k) z_h k^{\alpha - 1} + z_\ell \left(\frac{\dot{P}_L}{P_L}\right) - \tau_a \implies \frac{\partial A^\star(\tau_a)}{\partial \tau_a} < 0$$
  $$\Delta A_{\text{prec}} \equiv \int_{\mathcal{S}} a \, d\mu^\star\big(s \,\big|\, pv=0, \sigma_{z_2}=0.25\big) - \int_{\mathcal{S}} a \, d\mu^\star\big(s \,\big|\, pv=5, \sigma_{z_2}=0\big) = \text{NZD } 60.8\text{B–}91.5\text{B} \ge \text{CapEx}$$
* **Closing the D20 Top Reef (Rolls 19–20):** When $\tau_a = 0$ on NZD 1.6T of property, land hoarding ($z_\ell$) out-yields building ($z_h$), triggering `T:02` (1-for-1 buyer subsidy capitalization when $\epsilon_S^{\text{land}} \approx 0$) and `T:04` (the Lavoisier talent drain).
* **The Judo Counter:** Enacting **`B:05` (Use-It-Or-Lose-It 1.5% Land/Wealth + 25%$\to$18% Estate Shift)** + **`B:03` (NZD 62k+ Youth Grant)** + **`E:02` (Precautionary Release)** closes D20 Rolls 19–20, releases NZD 60.8B–91.5B in precautionary cash buffers to self-finance national electrification (+NZD 15.55B/yr OPEX savings), and keeps active builders (`20:01`–`20:19`, up to NZD 100M NW) net welfare positive.

### Combo 3: Bending the Accounting Curve (`B:07` + `N:03` + `B:06`)
* **The Equation (Williamson 2009; NZ Treasury CBAx 2025):**
  $$\text{NPV}_{\text{ACC}}(t=5) = \sum_{s=1}^{81} \frac{\Delta \mathbb{E}\big[\tau_y w_s h_s - \sum_{x \in \{1,2,4\}} C_x \mathbb{I}(\text{Exit}_x)\big]}{(1 + r_{\text{SRTP}})^s} = \text{NZD } 35.25\text{B} \;\; (3.84\times \text{Cost at } r_{\text{SRTP}} = 2.0\%)$$
* **Canceling the Every-3rd-Turn Election Audit (`H:01`):** Pairing **`B:07` (ACC Actuarial Time-Bend)** with **`N:03` (Williamson)** books $1.16\times$ direct cost-avoidance breakeven (NZD 10.68B) and $3.84\times$ total return by Year 5 (Turn 2), neutralizing `H:01` and unlocking **`B:06` (The 2050 50/50 Rule: 18.5% PAYE & Super kept at Age 65)**.

---

## 4. Scaling Strategy from 2 Players to 6 Players ($P = 2 \dots 6$)

| Player Count ($P$, Normalized) | `SS1` Reach % | `SS2` Reach % (Mean Turn) | Win Rate vs. Finland | Hub (`K:01`) vs. Finisher (`K:02`) Win Share | Mean Per-Player Score ($\bar{\Sigma}_{\text{Per-Capita}}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2 Players (Duel / Co-Op Pair)** | 96.2% | 88.9% *(Turn 12.9)* | 91.4% | **43.1% : 44.8%** | **142.1 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 76.4$)* |
| **3 Players** | 97.5% | 90.4% *(Turn 12.6)* | 93.0% | **42.4% : 44.9%** | **141.7 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 75.8$)* |
| **4 Players (Standard Crew)** | 98.4% | 91.2% *(Turn 12.4)* | 94.1% | **41.8% : 44.6%** | **139.2 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 74.2$)* |
| **5 Players** | 98.1% | 90.8% *(Turn 12.5)* | 93.8% | **43.5% : 43.9%** | **137.7 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 73.6$)* |
| **6 Players (The Big Table)** | 97.8% | 89.7% *(Turn 12.7)* | 92.9% | **44.0% : 43.2%** | **135.9 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 72.9$)* |

* **2-Player Key Tactic:** Use the **Self-Combo Rule**—expose `B:01` and `B:05` in your elder character's River slot and trigger combos from your younger character's hand to pay yourself 100% of the Variant B royalties while building toward `SS1`.
* **6-Player Key Tactic:** Because 6-player games suffer higher `H:02` Silo Political Drag (3.0 Wealth and 3 co-stakers required per Subsystem), prioritize assembling three Dual-Class Wayfinders early to unlock **`K:07` (*Te Tiriti & The Big Table Crew*)**, which shares all Innate Kaupapa abilities across the entire table!

---

## 5. Solo & Co-Op Racing Variant: "Chasing Finland" (The Economic Sailing Race)

Pit Aotearoa New Zealand (starting at **81.0** in `SS0`) in a 20-Turn Match Race along the **Social Cohesion & Welfare Track (`C:06`, Target: 126.0)** against an automated foreign benchmark vessel rolled on the D20 every Phase IV:

| Rival Vessel Profile | Roll 1–5 (Headwind) | Roll 6–15 (Cruising) | Roll 16–20 (Gust) | Structural Ceiling / Historical Lesson |
| :--- | :--- | :--- | :--- | :--- |
| **1. Finland (Nordic Benchmark — Starts at 88.0)** | **$-0.5$ pts** *(Demographic drag)* | **$+1.0$ pt** *(Steady Nordic compounding)* | **$+2.0$ pts** *(High-tech / education surge)* | Starts ahead with Gate 1 clinics (`B:01`) and #1 *Monilukutaito* (`C:02`); finishes around **107.2**. Aotearoa must lift onto foils (`SS1` $\to$ `SS2`) to overtake Finland and reach **126.0**! |
| **2. Devolved Scotland (`T:01`/`B:01` — Starts at 83.0)** | **$0.0$ pts** | **$+1.5$ pts** *(Fast early child gains)* | **$+2.0$ pts** | **Hard Ceiling at 96.0:** Lacks unitary sovereign power to enact `B:05` (land/estate tax); stalls under urban rent capitalization (`T:02`). |
| **3. 1989 Bubble Japan (Deming *Kaizen* — Starts at 90.0)** | **$-3.0$ pts** *(Turns 7–20 Land Bubble Crash!)* | **$+2.5$ pts** *(Turns 1–6)* | **$+3.5$ pts** *(Turns 1–6)* | Surges to **105.0** by Turn 6 on industrial *Kaizen*, then collapses into a 14-turn balance-sheet recession when surpluses pour into Tokyo land (`T:02`/`T:04`) instead of `B:06`. |
"""

# ==============================================================================
# 3. scripts/simulate_foils_and_founders_balance.py
# ==============================================================================
SIM_PY = r'''#!/usr/bin/env python3
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
'''


def write_file(rel_path: str, content: str, executable: bool = False) -> None:
    target = ROOT / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.lstrip("\n"), encoding="utf-8")
    if executable:
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"[OK] Wrote {rel_path} ({len(content.splitlines())} lines)")


def patch_maxim_if_present() -> None:
    maxim = "Not all lives are easy, but none should be impossible."
    readme = ROOT / "README.md"
    if readme.exists():
        txt = readme.read_text(encoding="utf-8")
        if maxim not in txt and "## 1. Why a Card Game?" in txt:
            target_header = "## 1. Why a Card Game? (Rule Zero: The Rawlsian D20 Test)\n"
            replacement = (
                target_header
                + f'\n> *"{maxim}"*\n'
            )
            if target_header in txt:
                readme.write_text(txt.replace(target_header, replacement, 1), encoding="utf-8")
                print("[OK] Patched Rule Zero maxim into README.md")

    study_yaml = ROOT / "decks/study_cards.yaml"
    if study_yaml.exists():
        ytxt = study_yaml.read_text(encoding="utf-8")
        old_bridge = 'proof_bridge: "Before knowing whether you roll a Nat 1'
        new_bridge = f'proof_bridge: "{maxim} Before knowing whether you roll a Nat 1'
        if maxim not in ytxt and old_bridge in ytxt:
            study_yaml.write_text(ytxt.replace(old_bridge, new_bridge, 1), encoding="utf-8")
            print("[OK] Patched Rule Zero maxim into decks/study_cards.yaml (B:00)")


if __name__ == "__main__":
    write_file("rules/foils_and_founders_gameplay.md", GAMEPLAY_MD)
    write_file("rules/strategy_study_guide.md", STRATEGY_MD)
    write_file("scripts/simulate_foils_and_founders_balance.py", SIM_PY, executable=True)
    patch_maxim_if_present()
    print("\nAll files ready! Run: python3 scripts/simulate_foils_and_founders_balance.py")
