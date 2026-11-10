# FOILS & FOUNDERS: GAMEPLAY & COOPETITIVE MECHANICS GUIDE
*Companion to `cards.yaml` (80-Card Master Deck, v2026.11), `study_cards.yaml`, & `rules.md`*  
**Author:** Michael Tiemann (`mdtiemann@gmail.com`) | **License:** CC-BY-SA-4.0  
**Repository:** `https://github.com/MichaelTiemann/IGWelfare`

---

## 1. Core Design Philosophy: Learning General Equilibrium by Doing (`N:01`)

**Foils & Founders: The Aotearoa Deck** is a **2-to-6 player coopetitive tabletop simulation** (with Solo and Full Co-Op *Chasing Finland+* modes) spanning **20 turns at $\Delta t = 3$ years per turn (60 calendar years: 2026–2086)**.

Most policy games fail in one of two ways: either they preach a pre-scripted moral where players march in lockstep, or they reward zero-sum monopoly hoarding until the board collapses. *Foils & Founders* is built on the exact mathematical tension of Aotearoa New Zealand's spatial Overlapping Generations (OLG) economy:

1. **You Cannot Win on a Sinking Hull (The `-16.21% CE` LTFM Sinkhole):** Under Status Quo (`SS0`) fiscal drift, unprevented early childhood hardship (`22%–30%`), `3.10x` metropolitan housing costs, `19.3%–23.4%` metro graduate brain drain, and `61%` top-talent capture in passive land speculation (`z_l`) drag Crown Debt toward `185%–200%` of GDP and working-age PAYE toward `28.2%–32.0%`. Every single policy silo fighting alone finishes **net negative** over 60 years (`-9.12%` GrowthNZ-only, `-6.80%` Solve-Debt-First, `-2.40%` WellBeing-only, `-0.06%` Barnardos-only).
2. **Over Half the Prize Lives Between Our Lanes (`+13.47%` of `+24.70% CE`):** Uniting the **Four Coalitions** (`K:01` Barnardos/Iwi Early Years, `K:04` WellBeing & Housing Justice, `K:05` GrowthNZ Enterprise Builders, and `K:07` Sovereign Fiscal Stewards) unlocks `+24.70% CE` pre-NDC national welfare (`+25.19% CE` on the wave-convolved *Te Kāhui Waka* ledger), sinks Crown Debt to `21%–22%` of GDP, cuts PAYE from `22.0%` to **`18.25%`**, and lowers Universal NZ Superannuation from Age 65 (`SS1`) to **Age 64 (`SS2`)**!
3. **Asymmetric Urgency Creates the Wrestling Scramble:** Even when players agree on the 60-year destination, rolling different **Regions**, **Starting Child Ages**, and **Wealth Vigintiles (`B:00`)** creates fierce short-term positional scrambles over *who gets covered in Wave 1 vs. Wave 9*, *who pays Political Drag vs. who collects Mana Royalties*, and *when to gamble on launching Phase 2 (`SS2`)*.
4. **Cardboard Before Cabinet (`N:01` & `T:00`):** As Kenneth Arrow (`N:01`) proved, capability is forged in the doing—and when citizens, students, and Ministers burn through their `28%` Wave-1 commissioning friction on a tabletop in 45 minutes, nobody's *mokopuna* has to pay the tuition in real life.

---

## 2. Tabletop Zones, Currencies & The 3-Slot *Whānau* Mat

### 2.1 Central Shared Board Zones
* **The River (Enacted Commons):** Shared central row where enacted Base (`B`), Cluster (`C`), Nobel (`N`), and Energy (`E`) cards persist permanently as **non-rival public infrastructure (`N:06` Variant B)**. Any player may tap a River card's synergy by paying **Mana Royalties** to its founders.
* **The 13-Wave *Te Kāhui Waka* Track (`Waves 1–13`):** Tracks regional rollout echelons in thirds (`0 -> 1/3 -> 2/3 -> 3/3`) across four core subsystems:
  1. **Dual-Gate ECE & *Tuakana–Teina* Mentoring (`B:01` + `B:03`):** Waves `1–9` (`Rural + Small` $\to$ `Large` $\to$ `Auckland`).
  2. **Household, Farm & Marae Electrification (`E:01`):** Consecutive provincial-first waves—`Rural + Small` in **Waves `1–3`** (hitting `100%` provincial coverage at Year 3 / Turn 1!), `Large` in **Waves `4–6`**, and `Auckland` in **Waves `7–9`**.
  3. **Age-20 Youth Capital Grants (`B:05` $\to$ `B:06`):** `B:05` (`17.3%` Early-Adopter Vanguard Bridge) runs in **Waves `1–6`** (`0%` waste), folding into universal `B:06` coverage across **Waves `7–13`** as Wave-1 mentored adolescents turn Age 20.
  4. **Dual-Speed Tax & Surplus Engines (`B:07`, `B:08`, `B:14`, `B:15`):** Each tracked on a **`0% -> 100%` Sufficiency Dial** (`33%` steps for 3-yr `B:07` CGT/Estate; `10%–30%` steps for 10-yr `B:08` LVT/Corp lockstep), governed by the **4 Regional Tax Key Tokens (`C:06`)**.
* **The $4 \times 4$ Coalition Matrix (`B:12`):** Displays the 4 Diagonal Coalition Silos and 6 **Off-Diagonal Synergy Wedge Cells** (`1x2`, `1x3`, `1x4`, `2x3`, `2x4`, `3x4`). Off-diagonal cells begin **unrevealed** showing only Prior Additionality Bands `[Headwind 1–5 | Baseline 6–15 | Tailwind 16–20]`, resolved via the D20 when ignited!
* **Macro Telemetry Tracks:**
  * **Core Crown Debt & Mirror-Investment J-Curve Track:** Starts at `42.0% of GDP` (`Year 0`), tracks unrecovered `SS1` cash deficits during Years `1–16` (`Turns 1–5`), and targets `21%–22% of GDP` in `SS2` (vs. the `185%–200%` LTFM ceiling).
  * **Off-Balance-Sheet *Whānau* Pool (`K_whanau`):** Shared kinship care track initialized by regional mix (`[0.42 Rural, 0.38 Small, 0.32 Large, 0.28 Auckland]`). Rises with `B:08` housing cooling and `B:15` Age-64 Super (`+8.1%`); collapses by `-36.2%` (flipping negative at the distress tail!) under `H:05` / `T:03` Age-70 hikes.
  * **Social Cohesion Index (`C:02`):** Starts at `100.0` (`81/100` CPI reality), climbs through `118.4` (`SS1`) to **`126.0` (`SS2` #1 Global Social Credit Rating)**.
  * **The Abroad / Sydney Exile Zone (`k = 5`):** Holds working-age adults exiled at Age 21 by `H:04` (*Trans-Tasman Brain-Drain Vortex*) until repatriated via `B:06` + `B:08`.

### 2.2 The Two Distinct Currencies: **Wealth** vs. **Mana**
Never conflate private cash with civic standing:
1. **Wealth (Silver Coins — Rival Private Liquidity):** Earned from working-age `Slot 2` labor/enterprise (`1–3 Wealth/turn` depending on skill tier `h` and firm state `z_l` vs. `z_h`). Spent to pay **Political/Commissioning Drag** when enacting policies, buy private bridges, or stake against election resets. *Wealth alone never wins the game; at endgame, uninvested cash converts at only `5:1` into Victory Score.*
2. **Mana (Pounamu / Gold Counters — Generational Standing & Contingent Stewardship):** Earned ONLY by building enduring capability, co-staking Coalition Wedges, shielding neighbors across the River (`Variant B` Inverse-Hub Royalties), and lifting cohorts across lifecycle gates.
   * **Zone A (Banked Mana — Upright):** Permanent generational legacy immune to political resets.
   * **Zone B (Staked Contingent Mana — Flat on Unfinished Subsystems / Bets):** Represents your skin in the game. Tipped **sideways into Jeopardy** if an election reset (`T:07`) or premature `SS2` launch shoal (`B:13`) strikes before completion; multiplies **`2x` (`SS1`) or `3x` (`SS2`)** into Zone A upon subsystem lock-in!

### 2.3 The 3-Slot *Whānau* Player Mat (`2-of-3` Default vs. `3-of-3` Full Mode)
Every player places a **Command Zone Wayfinder Persona (`K:01–K:09`)** beside a **3-Slot *Whānau* Mat** spanning the human lifecycle:
* **Slot 1 — *Being* (`Tamariki & Rangatahi`, Ages `0–17`):** Consumes household/public investment across **Gate 1 (`Ages 0–5`)** and **Gates 2–3 (`Ages 6–17`)**. Generates `0` cash Wealth now, but determines your future adult skill tier (`Struggling h1–h2`, `Core h3–h5`, or `Thriving h6–h7`).
* **Slot 2 — *Becoming* (`Pakeke`, Ages `18–63`):** Your household economic engine. Generates **Wealth** each turn (`1 Wealth` if Struggling/`z_l` wage-squeezed, `2 Wealth` if Core Trades `Node 18`, `3 Wealth` if Thriving `z_h` Builder `Node 20`), pays PAYE taxes, and faces the Age-21 `H:04` Brain-Drain check upon entering Slot 2.
* **Slot 3 — *Crossing Over* (`Kaumātua & Kuia`, Ages `64–89` in `SS2` / `65–89` in `SS0–SS1`):** Receives Universal NZ Superannuation, unlocks the **Off-Balance-Sheet `K_whanau` Pool (`K:09`)**, emits **1 free Lifetime Experience Token per turn**, and leaves a De Nardi Estate (`B:07` / `E:02` solar bequest) upon reaching the **Age-90 Rebirth Horizon**.

#### Why Default Coopetitive Play Uses **2-of-3 Active Slots ("Playing Out of Your Hand")**
* **Standard Mode (`2-of-3` Asymmetric *Whānau* — Recommended for 3–6 Players):** At Setup, each player populates **only 2 of their 3 slots**, leaving **1 generational slot empty**. That structural gap mirrors modern demographic reality and forces dynamic cross-table (*out-of-hand*) alliances:
  1. **`[Slot 1 + Slot 2 | Empty Kaumātua]` (Young Urban Family):** You have cash and a child, **but no Elder in Slot 3**—so `K_whanau` tokens yield almost nothing to you directly, and when a Gate-2 shock hits, you *must* pay Variant B Mana royalties to a rival holding a Slot-3 *Kuia* ("Aunty's House", `K:09`) to shield your child!
  2. **`[Empty Tamariki | Slot 2 + Slot 3]` (Delayed-Fertility / *Hagwon* Household):** Peak cash (`Slot 2`) + free Experience Tokens & `K_whanau` shields (`Slot 3`), **but no child of your own**—forcing you to mentor or sponsor neighbors' *Tamariki* across the River so the board is safe when your Elder hits Age 90 and rebirths into `Slot 1`!
  3. **`[Slot 1 | Empty Pakeke | Slot 3]` (Skipped-Generation / Grandparent-Led *Whānau*):** High wisdom (`Slot 3`) + rising youth (`Slot 1`), **but cash-poor** (e.g., after an Age-21 `H:04` exile to Sydney)—making Universal Super (`B:15`) existential and motivating you to trade `K:09` Experience Tokens to cash-rich `K:05`/`K:07` players in exchange for funding Political Drag!
* **Endogenous Mid-Game 3rd-Slot Unlock (`TFR = 2.03` & Repatriation Power-Up!):** Filling all **3 slots simultaneously** is earned on the mat! Whenever the table unlocks **`N:08` + `B:15` (Age-64 Super + Cooled Housing restoring replacement fertility)**—or repatriates an exiled `Slot 2` adult via **`B:06` + `B:08`**—players may immediately populate their empty 3rd *Whānau* slot ahead of the Age-90 cliff!
* **Workshop / 2-Player Teaching Toggle (`3-of-3` Full *Whānau* Mode, `P:08`):** For 2-player duels or introductory wānanga, populate all 3 slots from Turn 1 (applying a `+1 Wealth` Self-Combo surcharge whenever triggering your own River card without a neighbor).

---

## 3. Pre-Game Setup: Rolling Behind Rawls's Veil of Ignorance (`B:00`)

Before anyone chooses a policy strategy, every player picks up **`B:00` (*Te Tatau o Rangiātea* — The Rawlsian D20)** to discover where they are born in Aotearoa:

1. **Step 1 — Roll Birth Vigintile (`1d20`):**
   * **Rolls `1–4` (`1–6` if `H:03` *1972 Nostalgia / GUiNZ Drift* is active):** **The Early Hardship Reef (`22%–30%` Corner, Nodes 1–2).** Start with `1 Wealth`. Your `Slot 1` child begins exposed to the `i_c = 0` subsistence corner unless rescued before Age 6 (`B:01`). *(On a Natural `1`, roll a second `1d20` on the `01:01–01:20` Bottom-5% sub-table to see the specific acute hurdle your whānau faces).*
   * **Rolls `5–14` (or `7–14`):** **The Squeezed Working Middle (`Node 2–3` Residual AHC Squeeze).** Start with `2 Wealth` (renter below the `20%` LVR hurdle in `Large`/`Auckland`).
   * **Rolls `15–19`:** **Asset-Holding Homeowner / Professional (`P75–P95`).** Start with `3 Wealth` and homeowner tenure (`a >= 0.20 * Q_k`).
   * **Roll `20` (Natural `20`):** **Top-5% Wealth Bracket (`20:01–20:20` Sub-Roll).** Start with `4 Wealth`—and immediately roll `1d20` to determine whether your legacy fortune is locked in **Passive Land Speculation (`1–12`: `z_l`, `omega_ent = 0.15`, exposed to `B:08` LVT until rotated!)** or **Active Enterprise Equity (`13–20`: `z_h`, `omega_ent = 0.80`, net welfare positive right up to `NZD 50M` and breakeven at `NZD 140M`!)**.
2. **Step 2 — Roll Home Region (`1d20`, Weighted to Stats NZ Population Shares):**
   * `1–3` (**`Rural`**, `16.0%` pop, `Q = 1.05`, `2.74x` mandatory fuel burden $\bar{e}_k = 0.048$, Wave-1 Vanguard).
   * `4–8` (**`Small` Towns**, `24.0%` pop, `Q = 1.40`, `2.25x` fuel burden $\bar{e}_k = 0.036$, Wave-1 Vanguard).
   * `9–13` (**`Large` Regional Cities**, `25.9%` pop, `Q = 2.05`, exposed middle-hinge in `C:06`, Wave-2 Follower).
   * `14–20` (**`Auckland`**, `34.1%` pop, `Q = 3.10`, `z_h = 1.75` ceiling, severe LVR crowd-out, Wave-3 Follower).
3. **Step 3 — Roll Starting `2-of-3` *Whānau* Ages:**
   * Roll `1d20` for configuration: `1–10` `[Slot 1 + Slot 2]` (roll `1d6` for child starting age: `1–2` = **Age 1**, `3–4` = **Age 4**, `5–6` = **Age 12**; adult starts at **Age 30**); `11–16` `[Slot 2 (Age 42) + Slot 3 (Age 66)]`; `17–20` `[Slot 1 (Age 11) + Slot 3 (Age 67)]`.
4. **Step 4 — Draft Wayfinder Personas (`K:01–K:09`) & Deal Opening Hands:**
   * In **Rawlsian Turn Order** (lowest Birth Vigintile roll drafts first!), each player claims 1 Wayfinder Persona for their Command Zone and draws **5 cards** from the shuffled Playable Deck (`B:01–B:15`, `C:02–C:10`, `N:01–N:08`, `E:01–E:05`, plus active `P` mods; `B:16`, `K:10`, and `N:09` sit face-up as Capstone Milestones).
   * Place `H:01` (*Cash-Flow Myopia*) and `H:02` (*Wellington Silos*) face-up in the Orthodoxy Row; shuffle `H:03–H:10` and `T:01–T:10` into the **Headwind & Trap Deck** (or deal 2 to each player's secret Feral Hand in **Mode B**).

---

## 4. Turn Sequence & The 20-Turn ($\Delta t = 3\text{ Yr}$) Lifecycle Clock

Each of the **20 turns** represents **3 calendar years** (`Turn 1 = Years 1–3`, `Turn 2 = Years 4–6`, ..., `Turn 5 = Years 13–15 [Plan C Window]`, `Turn 6 = Years 16–18 [Year 16.8 Cash Breakeven]`, `Turn 7 = Years 19–21 [Plan B Window & Wave-1 Echo]`, `Turn 20 = Year 60`):

1. **Phase A — Sunrise & Biological Aging (`+3 Years`):**
   * Advance the Turn Marker and age every active character on all *Whānau* Mats by **`+3 years`**.
   * **Check Biological Gates ("Use-It-Or-Lose-It"):**
     * *Crossing Age 6 (`Slot 1`):* Did this child receive `B:01` (*First 2000 Days*) in an active regional wave (or a `2-Wealth` private bridge)? If **Yes**, place a **Readiness Counter (`N:03`)**. If **No** and Vigintile $\le 4$ (`6` under `H:03`), attach a **Struggling Trajectory Token (`h1–h2`)** *and* add **+1 Contingent Liability** to the Crown Debt Track!
     * *Crossing Age 15 (`Slot 1`):* Did this youth receive `B:03` / `B:04` (*Tuakana–Teina* / *GrowingChange*)? If **No**, any unbanked `B:01` Readiness Counter suffers **Fade-Out** (`22%` 1-term / `39.2%` 2-term loss if hit by `z_1` distress)! If **Yes**, promote to **Thriving (`h6–h7`)** and mark **Eligible for `B:05` Early-Adopter Grant**!
     * *Crossing Age 20 (`Slot 1 -> Slot 2` Launch):* Award `B:05` (if mentored in Turns `1–2`) or `B:06` (once universal wave is active). If unseeded in an uncooled metro region (`Large`/`Auckland`), roll `1d20` against **`H:04` (*Brain-Drain Vortex*)**: on `1–5`, exile that new `Slot 2` adult to the **Sydney/Abroad Zone**!
     * *Crossing Age 65 (`SS0/SS1`) or Age 64 (`SS2` via `B:15`) (`Slot 2 -> Slot 3`):* Retire into *Kaumātua/Kuia* status, activating `K:09`!
     * *Crossing Age 90 (`Slot 3 -> Rebirth`):* Settle estate (`B:07` / `E:02`), then roll `B:00` to **rebirth a newborn (`Age 0`) into `Slot 1`**!
2. **Phase B — Resource Harvest & Election / Shock Check:**
   * Collect **Wealth** from active `Slot 2` earners + **Experience Tokens** from active `Slot 3` *Kaumātua* (`K:09`).
   * **Every 3rd Turn (`Turns 3, 6, 9, 12, 15, 18` — Parliamentary Election):** Roll the **D20 Political Stability Check** (Section 7.1), modified by unrecovered Mirror-Investment J-curve deficits (Turns `1–5` only) and active shields (`B:09`, `K:02`, `K:10`).
3. **Phase C — Wayfinder Actions (In Rawlsian Turn Order, 2 Actions per Player):**
   * Choose any 2 actions: **(i) Advance a Regional Wave / Tax Sufficiency Dial**, **(ii) Enact a Card to the River** (paying Wealth Political Drag and staking Mana), **(iii) Co-Stake a Neighbor's Subsystem or $4 \times 4$ Coalition Wedge** (paying Variant B Royalties), **(iv) Tap Your Command-Zone Wayfinder *Kaupapa* Power**, or **(v) Call `B:13` (*Te Kapehu Whetū* Early `SS2` Launch Bet — Turn 5+)**.
4. **Phase D — End-of-Turn Telemetry & Draw:**
   * Update the J-Curve / Debt Track (`B:14`), `K_whanau` Pool, and Social Cohesion (`C:02`); draw back up to **5 cards**.
# ==============================================================================
# FOILS & FOUNDERS GAMEPLAY GUIDE — BATCH 2 (SECTIONS 5 & 6)
# ==============================================================================

---

## 5. The 13-Wave *Te Kāhui Waka* Scramble, Vanguard Grants & Hyperbolic Bargains

In a naive deterministic spreadsheet, giving `100%` of families `1/3` of a mentor looks identical to giving `1/3` of families a full mentor. In real life—and inside our GPU solver's convex Perron–Frobenius operator (`Document 2A` §4.4)—`1/3` of a mentor fails the $\varphi_2 = -0.95$ adolescent bottleneck and `1/3` of a grant fails the `20%` LVR deposit cliff! Capacity **must** roll out in discrete regional echelons (`0 -> 1/3 -> 2/3 -> 3/3`), dividing the table into **Active Wave Vanguards** and **Temporary Waiters**.

### 5.1 Pacing Choice: 13-Wave *Te Kāhui Waka* (`N:01`) vs. Day-1 Single-Shot (`T:04`)
Whenever a subsystem (`B:01` ECE, `B:03` Mentoring, or `E:01` Electrification) is first initiated, the initiating player (or a table majority vote if contested) chooses its rollout mode:

| Rollout Mechanic | **13-Wave *Te Kāhui Waka* (`N:01` + `N:07` Default)** | **Day-1 Single-Shot Surge (`T:04` Fast-Starter Gamble)** |
| :--- | :--- | :--- |
| **Step Size & Order** | Advances **`1/3` regional capacity per wave**: `Rural + Small` first (`Waves 1–3`), then `Large` (`Waves 4–6`), then `Auckland` (`Waves 7–9`). *(Electrification `E:01` hits `100%` `Rural + Small` at Turn 1 / Year 3!)* | Jumps straight to **`3/3` national coverage on Turn 1** across all 4 regions simultaneously. |
| **Workforce & Commissioning Friction** | Quadratic surge penalty drops **`88.9%`** ($\phi_{\mathrm{adj}}(\frac{1}{3})^2 = 0.02$ vs. $0.18$); PDSA learning ($\gamma_{\mathrm{learn}} = 0.45$) lifts delivery yield from `72%` (`Wave 1`) to **`>95%` (`Wave 7`)**, averaging **`95.5%–96.8%`** across `SS1`! | Suffers `28%` Day-1 uncalibrated friction + `18%` workforce bottleneck (`~18.5%` permanent `SS1` haircut) and triggers **`H:10`** (`42%` / `NZD 3.8B` unmentored grant waste). |
| **Early J-Curve Risk & Stability Modifier** | Year-3 capital at risk cut **`75%`** (`-NZD 1.6B/yr`); places **+1 Fleet Experience Counter (`L_m`)** per completed echelon (`+2` to next Additionality D20 roll) and pulls cash breakeven 2.4 yrs earlier to **Year 16.8**! | Quadruples Year-3 deficit (`-NZD 6.5B/yr`), inflicts **`-4` on Additionality & Political Stability D20 rolls** during Turns `1–5`, delays breakeven to **Year 19.3**, and **locks out `Plan C` (`B:13`)**! |
| **Why Someone Still Tempts `T:04`!** | Waiters holding an Age `3–5` toddler in `Auckland` risk missing Gate 1 unless they buy a `2-Wealth` private bridge or trade for an early Vanguard slot! | An `Auckland` toddler parent captures immediate Turn-1 public coverage for *their* child—dumping the `-4` macro stability risk onto everyone else! |

### 5.2 Fast Starters vs. Patient Followers & The `17.3%` Vanguard Grant Bridge (`B:05`)
Stepped *Te Kāhui Waka* pacing rewards **both** ends of the queue with distinct strategic advantages:
1. **Fast-Starter Vanguard Upside (`Rural` & `Small` Waves `1–3`):** Your `Slot 1` children clear biological gates immediately at low Political Drag (`K:01` cuts Wave-1 drag by `50%`), bank Readiness Counters early, and start the `20.5-year` generational wave echo (`E:05`) first.
2. **The `17.3%` Early-Adopter Youth Grant Bridge (`B:05`, Waves `1–6` / Turns `1–2`):** Any player whose `Slot 1` adolescent completes `B:03` (*Tuakana–Teina* Mentoring) or `B:04` (*GrowingChange*) during Turns `1–2` represents Aotearoa's `17.3%` ready vanguard—immediately unlocking the **`NZD 62k+` Youth Capital Grant at Age 20 with `0%` waste** (`-NZD 0.28B/yr` funded by `B:07`'s 3-yr CGT/Estate fast ramp), up to **4 turns ahead** of Wave-13 universal `B:06`!
3. **Late-Wave Follower Certainty (`Large` & `Auckland` Waves `4–9`):** By the time `Large` and `Auckland` scale up in Turns `2–3`, vanguard PDSA learning (`N:07`, matching NZ's `~5.4–5.8 yr` educator staffing cycle) has pushed effective fidelity above **`95%`** and `B:08` has begun cooling urban rents—so Followers pay less commissioning waste, enjoy `+2` `L_m` bonuses on Additionality rolls, and fuse onto the exact same asymptotic welfare curve by **Turn 5–6 (Year 16)**!

### 5.3 Bridging Waiters vs. The Hyperbolic Present-Bias Shortcut (`T:02`)
What happens if you hold an Age-4 toddler in `Auckland` (`Vigintile 6`) on Turn 1 while Wave 1 is launching in `Rural + Small`? You have three real choices before your child turns 7 on Turn 2:
* **Option A — Private Sacrifice / Whānau Bridge:** Spend `2 Wealth` out-of-pocket (or pay `1 Mana` Royalty to tap a neighbor's `K:09` *Aunty's House* shield) to bridge your child cleanly across Gate 1 while waiting for your public wave.
* **Option B — Coalition Wage/Cost Advance:** Negotiate with `K:05` (*GrowthNZ Enterprise*) or `K:04` (*WellBeing*) to play **`C:07` (*Income $\times$ Geography Bridge*)** or advance `1 Wealth` forward support to cover your gap.
* **Option C — Accept `T:02` (*Hyperbolic Coerced-Shift Shortcut*, $\beta_{\mathrm{hyp}} = 0.72$):** Take **`+2 Wealth` cash immediately** by working coerced double shifts. *Consequence:* Strips parental mentoring time (`Lane B`), permanently forfeits `Thriving h6–h7` status and `B:05` Vanguard Grant eligibility for that youth, **AND drops 1 Skill-Shortage Liability Token onto `K:05` (Enterprise) and `K:07` (Fiscal) mats** (`-1 Wealth/turn` domestic talent bottleneck)! Smart `K:05` employers quickly learn it is cheaper to co-fund `Option B` than let squeezed parents take `Option C`!

---

## 6. Stochastic $4 \times 4$ Additionality, Spatial Tax Keys, Food Hubs & `K_whanau`

### 6.1 Discovering Off-Diagonal Wedges on the $4 \times 4$ Coalition Matrix (`B:12`)
The four Coalitions cannot inspect exact deterministic synergy payouts before committing resources. Whenever two (or more) Wayfinders link their lanes across one of the **6 Off-Diagonal Wedge Cells** on the $4 \times 4$ Matrix, roll **`B:00` (`1d20`)** to discover the realized structural elasticity:

* **Linked Coalition Advantage (`B:12`):** If **both** Coalition Wayfinders actively co-stake the wedge (each placing `1 Mana` in Zone B and splitting the Political Drag), **roll `2d20` and take the HIGHER result ("Roll with Advantage")**! *(Add `+2` per active `N:01` Fleet Experience Counter `L_m`, `+2` from `E:04`, or re-roll a `1–5` fumble once per game via `B:10` / `K:08`).*

| Off-Diagonal Wedge Cell | Linked Coalitions & Core Cards | **Headwind (`1–5`)** *(0.65x Yield)* | **Baseline (`6–15`)** *(1.00x Canonical)* | **Tailwind (`16–20`)** *(1.35x Breakthrough)* |
| :--- | :--- | :---: | :---: | :---: |
| **Wedge `1x2` (`Kaiako` & LVR Co-Location)** | `K:01` (Barnardos) $\times$ `K:04` (WellBeing): `B:01+B:08` | `+1.5% CE` (`+2 Mana`) | **`+2.27% CE`** (`+3 Mana`, clears `H:06`!) | `+3.1% CE` (`+4 Mana` + `1 Audit` card) |
| **Wedge `1x3` (Thriving Talent $\times$ `z_h` Firms)** | `K:01` (Barnardos) $\times$ `K:05` (GrowthNZ): `B:03+B:06+B:08` | `+1.3% CE` (`+2 Mana`) | **`+2.06% CE`** (`+3 Mana`, clears `H:04`!) | `+2.8% CE` (`+4 Mana` + `+1 Wealth/turn`) |
| **Wedge `1x4` (Year-5 ACC Continuation Ledger)** | `K:01` (Barnardos) $\times$ `K:07` (Fiscal): `B:01+B:09+N:04` | `+1.0% CE` (`+2 Mana`) | **`+1.53% CE`** (`+3 Mana`, `3.84x` audit!) | `+2.1% CE` (`+4 Mana`, `4.4x` GUiNZ ROI!) |
| **Wedge `2x3` (De-Hoarded Land & Food Hubs)** | `K:04`/`K:03` $\times$ `K:05` (GrowthNZ): `B:08+C:08+C:09` | `+0.8% CE` (`+2 Mana`) | **`+1.21% CE`** (`+3 Mana`, `1.6x–2.16x` hub!) | `+1.7% CE` (`+4 Mana`, unlocks `C:10` early!) |
| **Wedge `2x4` (Super-64, `K_whanau` & `TFR 2.03`)** | `K:04`/`K:09` $\times$ `K:07` (Fiscal): `B:15+K:09+N:08` | `+0.5% CE` (`+2 Mana`) | **`+0.69% CE`** (`+3 Mana` + **3rd Slot Unlock!**) | `+1.0% CE` (`+4 Mana` + **3rd Slot + `-0.5%` PAYE**) |
| **Wedge `3x4` (`-60 to -100 bps` Credit & `18.25%` PAYE)** | `K:05` (GrowthNZ) $\times$ `K:07` (Fiscal): `B:14+B:15+E:03` | `+0.5% CE` (`+2 Mana`) | **`+0.69% CE`** (`+3 Mana`, debt $\to 21\%$!) | `+1.0% CE` (`+4 Mana` + `+1 Audit` card) |

*(Note: Combined with Intra-Coalition-1 Dual-Gate Wedge 1 [`B:01 + B:03` = **`+3.32% CE`**] and the 7 isolated policy levers [`+11.23% CE`], the Baseline column sums to the exact **`+24.70% CE`** pre-NDC national benchmark!)*

### 6.2 The 4-Region Tax Synchronization Compact (`C:06` & Exposed Middle-Hinge `Large`)
Scalable tax levers **`B:07` (3-Yr Fast CGT/Estate Ramp)** and **`B:08` (10-Yr LVT + `20% -> 12%` Corporate Tax Lockstep)** require assembling the **4 Regional Tax Keys (`Rural <-> Small <-> Large <-> Auckland`)**:
* **Labrousse Nearest-Neighbor Leakage Rule (`T:06`):** Household step-migration and mobile capital flow primarily between **adjacent** tiers (`Rural <-> Small <-> Large <-> Auckland`), with minimal one-step jumping (`-15%` leakage) directly between `Rural/Small` and `Auckland`.
* **Why `Large` Cities Need Neighbors Most:** If `Rural + Small` enact `B:07`/`B:08` together, they retain **`85%` tax sufficiency** even before `Auckland` joins. By contrast, **`Large` Regional Cities (`25.9%` pop) sit exposed on both flanks** (`Small <-> Large <-> Auckland`): moving alone in `Large` triggers **`-60%` two-flank tax leakage** (land-bankers hop outward to untaxed `Small`/`Rural` districts while commercial capital shifts upward to untaxed `Auckland`)!
* **Locking the 4 Keys (`C:06` + `K:06`):** Tapping `K:06` (*Fair-Markets & Tax-Compact Mediator*) binds two adjacent Regional Keys in a single action and awards `+1 Generosity Wealth` split between them. Once all 4 Keys lock into `C:06`, border leakage drops to **`0%`**, `B:07` and `B:08` reach **`100%` Sufficiency**, and active `z_h` founders remain net welfare positive right up to **`NZD 50M` net worth** (breaking even at the `NZD 140M` Rich List median)!

### 6.3 The Rural & Small Prosperity Sub-Goal ("Good Food Is Medicine!" $\to$ `-0.64 pp` PAYE Cut)
Provincial players (`Rural` 16% + `Small` 24% = **40% of Aotearoa**) are never consigned to permanent welfare dependency. Completing the **4-Card Provincial Graduation Chain** transforms `Rural` and `Small` into high-wage `z_h` engines and gifts a tax cut to the *entire* nation:
1. **`C:07` (*Income $\times$ Geography Bridge*) + `E:01` (*Waves 1–3 Rural/Small Electrification*):** Cushions the `2.74x` mandatory fuel burden and cuts provincial household energy bills by `~NZD 3,000/yr` net (`-28%` / `-25%` off $\bar{e}_k$) by Turn 1!
2. **`B:02` (*Te Māra Kai / Farm-to-ECE*) + `B:04` (*GrowingChange Youth Ag Enterprise*):** Boosts preschool vegetable intake `+24%–33%`, cuts youth recidivism (`92%` non-recidivism), and blocks `T:06` (*Corporate Import Caterer Siphon*).
3. **`C:08` (*Wholesale Monopsony & Retail Duopoly Breaker*) + `C:09` (`1.60x–2.16x` *Regional Food Hubs*):** Shatters `H:08` farm-gate monopsony and grocery/supply cartels (`M_olig -> 1.00`), shifting provincial jobs from `z_l` to `z_h` (`\Delta\mu_z = +0.041` Rural, `+0.031` Small).
4. **Capstone `C:10` (*Endogenous `85%` Transfer Retirement*):** Because provincial households now earn thriving `z_h` wages, **`85%` of `C:07`'s temporary `SS1` transfer retires automatically in `SS2`**—shrinking public outlays from `NZD 8.06B/yr` to `NZD 6.52B/yr` and rewarding **every player at the table** with an extra **`-0.64 pp` working-age PAYE cut** (`18.89% -> 18.25%`)!

### 6.4 Off-Balance-Sheet *Whānau* Accounting (`K_whanau` & `K:09` *Aunty's House*)
Standard GDP ledgers count a paid crash-ward bed as "output" while valuing a grandmother's daily care at zero (`Marilyn Waring`, 1988). On the tabletop, the **`K_whanau` Pool** is decisive infrastructure—with sharp asymmetric incentives:
* **Empty Slot 3 (`0` Direct Yield):** If your `Slot 3` (*Kaumātua/Kuia*) is empty, you cannot tap the `K_whanau` Pool directly for yourself.
* **Active Slot 3 (`K:09` *Aunty's House* Royalties):** Any player holding an active `Slot 3` Elder may tap `K_whanau` to shield **any neighbor's** `Slot 1` child against Gate-1 hardship or Gate-2/3 unemployment shocks (`\Psi_{J=5}`), collecting **`+2 Mana` Variant B Royalties** while boosting school mentoring trust `M_trust` from `45%` to `100%`!
* **The Two-Phase Superannuation Rule (`H:05` Trap vs. `B:15` Age-64 Sweet Spot):**
  * *If `H:05` / `T:03` pushes Super to Age 70:* `K_whanau` drops **`-36.2%`**, `52%–68%` of manual elders leak onto disability support, and distressed households flip to **negative net care (`K_whanau^net < 0`, Sandwich-Generation Reversal)**—imposing `-1 Wealth/turn` caregiver drag on `Slot 2` working parents!
  * *Under IGWelfare (`SS1` Super protected at **65** $\to$ `SS2` lowered to **Age 64** via `B:15`):* Universal Super is never means-tested (preserving saving incentives `a'`), and lowering eligibility to **Age 64** in `SS2` releases a **`+8.1%` *Kuia/Koroua* caregiving boost** (`28%` offset by avoided ACC/disability claims), triggering `N:08` to unlock everyone's 3rd *Whānau* slot!
# ==============================================================================
# FOILS & FOUNDERS GAMEPLAY GUIDE — BATCH 3 (SECTIONS 7 TO 10)
# ==============================================================================

---

## 7. Every-3rd-Turn Political Stability Checks & The Two-Term "Stop-Go" Scissor-Blade (`T:07`)

In a parliamentary democracy with a 3-year electoral cycle, reforms must survive the ballot box before their 20-year human-capital dividends mature in cash. At the start of **Turns `3, 6, 9, 12, 15, and 18`** (Years `9, 18, 27, 36, 45, and 54`), the table rolls **`B:00` (`1d20`)** for **Political Stability**:

### 7.1 Computing the D20 Political Stability Modifier
$$\mathrm{Roll}_{\mathrm{Stability}} = 1\mathrm{d}20 - \mathrm{Penalty}_{\text{J-Curve}} + \mathrm{Shields}_{\text{Active}} + \mathrm{Stakes}_{\text{Player}}$$

* **Early J-Curve Deficit Exposure (`Turns 3 & 6` Only, Before Cash Breakeven):**
  * `-1` per unrecovered `NZD 1.5B/yr` Mirror-Investment cash deficit (`-1` under 13-Wave *Te Kāhui Waka* [`-NZD 1.6B/yr` trough] vs. **`-4` under `T:04` Day-1 Single-Shot [`-NZD 6.5B/yr` trough]**!).
  * `-2` if **`H:01` (*Cash-Flow Myopia*)** is still uncountered on the board.
* **Institutional & Narrative Shields (Permanent Once Enacted):**
  * **`+3`** from **`B:09`** (*ACC Year-5 Continuation Valuation*, booking `3.84x` total / `1.16x` direct cost avoidance so $\lambda_{\mathrm{cred}} \to 1.0$).
  * **`+2`** from **`N:04`** (*Williamson's Actuarial Ledger*) + **`+2`** from **`C:02`** (*Social Cohesion $\ge 118.4$*).
  * **`+4`** from **`K:10`** (*Kotahitanga & Te Tiriti Big Table Crew* constitutional entrenchment).
* **Voluntary Player Campaign Stakes (Coopetitive Dilemma!):** Before rolling, any player may tap `K:02` (*Pūrākau Weaver*, `1 Mana` for `+2`) or spend private **Wealth (`1 Wealth = +1` to the die)** to defend the coalition—creating a classic free-rider tension over *who pays to keep the waka upright*!

### 7.2 Election Check Outcomes & The Durable Banking Rule (`E:05`)

| Modified D20 Roll | Electoral Regime Outcome | Impact on Subsystems, Additionality & Cohorts |
| :---: | :--- | :--- |
| **`12+` (Mandate Renewed!)** | **Full Continuity (`\lambda_{\mathrm{cred}} = 1.0`)** | All active subsystems advance uninterrupted; Zone B staked Mana stays upright; Social Cohesion (`C:02`) gains `+3.0`. |
| **`6–11` (3-Yr Flip Friction)** | **50% Duty-Cycle Sawtooth (`T:07` Mid)** | **Off-Diagonal Wedge Additionality is cut in HALF (`0.50x`)** until the next election (`~+12.5% CE` linear ceiling; `+6.58% CE` if base levers also pause, inflicting `22.0%` 1-term fade-out on unmentored `Slot 1` children). |
| **`1–5` (6-Yr Scissor-Blade!)** | **Two-Term Repeal (`T:07` Low -> `+3.84% CE`!)** | Unfinished `SS1` waves freeze for **2 turns (6 years)**! Zone B Mana on unbanked subsystems tips sideways into **Jeopardy**; `Slot 1` youth under Age 20 without a `B:03` lock suffer **`39.2%` two-term fade-out** (`1 - 0.78^2`); and **Off-Diagonal Wedge Additionality drops to `0%`** (`84.6%` of the generational prize destroyed)! |

* **The Age-20 Durable Equity Seal (`E:05` Asymmetry):** Developing childhood skill (`Ages 0–19`) is biological wet cement, whereas banked adult capability is bedrock. Once a cohort crosses **Age 20** with **`B:03` Mentoring + `B:05`/`B:06` Youth Grant** locked in, place a **Durable Equity Seal (`E:05`)** on that character: even if a future `T:07` repeal strikes after Year 20, **`83.7%` of their harvest (`+20.86% CE`) is permanently repeal-proof**, and `20.5` years (`~7 turns`) after wave launch they still trigger the **2nd-Generation Daruich Echo** (free Readiness Counters for newborn `Slot 1` *Tamariki*)!

---

## 8. *Te Kapehu Whetū*: The *Catan*-Style Two-Key `SS2` Orbital Launch Gamble (`B:13`)

Crossing from **Phase 1 (`SS1` Incubation & Reallocation)** into **Phase 2 (`SS2` Sovereign Debt-Sinking, `18.25%` PAYE Cut, `1.65x` Infra Armor & Age-64 Super Harvest)** is the dramatic centerpiece of the mid-game (`Plot_Doc1D_LaunchPlans.m`).

Throughout `Turns 1–5`, whenever a player completes a regional wave echelon, unlocks **`B:09`**, or hits a **`16–20` Tailwind** on a Coalition Wedge, they draw **1 secret face-down Orbital Audit / Compass Card** (`+0.5%` to `+2.0%` verified fiscal cushion) into their private hand. Only by pooling clues—or peeking via **`B:10` / `E:04`**—does anyone know the exact total across the table!

### 8.1 Two Keys to Ignite `SS2` (`Plans C, B, & A`)

* **Key 1 — Calling the Early `"We Got This!"` Slingshot (`Plan C` @ Turn 5 / Year 15):**
  * During Phase C of **Turn 5** (or Turn 6 prior to hard cash breakeven), any bold player may step forward as **Launch Caller**, staking `2 Mana` into Zone B to declare *"We Got This!"* Other players must immediately declare **Co-Sponsor** (`1 Mana` stake) or **Skeptical Bystander** (`0` stake).
  * **Reveal & Audit:** Flip all face-down Orbital Audit cards and check the three statutory `Plan C` gates:
    1. All **13 *Te Kāhui Waka* waves** are active on the board;
    2. Consolidated **Core Crown Debt $\le 42.0\%$ of GDP** (`41.7%` target); and
    3. Revealed Audit cushions + realized Wedge yields cover **$\ge 95\%$ of the cumulative J-curve** (leaving $\le \text{NZD } 1.49\text{B}$ tail).
  * **If the `Plan C` Launch Succeeds (`+NZD 190B` Slingshot!):** `SS2` ignites immediately at Turn 5 (10 years ahead of `Plan A`), unlocking **`B:14`** + **`B:15`** (`18.25%` PAYE & **Universal Super at Age 64**!) and crossing the 60-year welfare target **13.1 years early**! The Launch Caller claims the **`3x` Initiator Mana Multiplier**, Co-Sponsors claim **`2x`**, and **Skeptical Bystanders suffer `-3 Mana` Forfeit** (and miss Turn-5 `SS2` tax-cut royalties)!
  * **If the Call Is Premature ("Grounded on the Shoals!"):** Cutting taxes before the J-curve matures violates the `42%` debt gate! `SS2` aborts; the premature Caller's staked Mana tips into **Jeopardy**, their Wayfinder is **exhausted for 2 turns**, Crown Debt takes `+2%` penalty drag, and patient rivals wait cleanly for Key 2!
* **Key 2 — Hard Cash-Flow Breakeven Lock (`Plan B` @ Turn 6–7 / Year 16.8–20.0, or `Plan A` @ Turn 8 / Year 25):**
  * Once annual fiscal savings + tax revenues exceed ongoing reform outlays (`Year 16.8` under *Te Kāhui Waka* $\to$ `Year 20` statutory `Plan B`), `SS2` unlocks **automatically with zero audit risk** (`NZD 0` bridge financing, `60.0x` peak fiscal ROI, `+NZD 104B` extra welfare over conservative Year-25 `Plan A`), awarding standard `2x` Zone-B Mana conversion to all active stewards.

---

## 9. Coopetitive Scoring (`Variant B`), Mode B Feral Spoilers & *Chasing Finland+*

### 9.1 Canonical Coopetitive Scoring: `Variant B` (Non-Rival River + Inverse-Hub Royalties)
At Game End (`Turn 20 / Year 60`, or immediate Mythic Victory upon enacting **`B:16` *Lifting the Gold from the River***), each player computes their **Final Stewardship Score**:

$$\mathrm{Score}_i = \Bigl(\mathrm{Mana}_{\text{Zone A},i} + \mathrm{Royalties}_{i} + \mathrm{CohortTierBonus}_{i} + \left\lfloor \frac{\mathrm{Wealth}_{i}}{5} \right\rfloor - \mathrm{BystanderPenalties}_{i}\Bigr) \times \mathcal{M}_{\mathrm{Regime}}$$

1. **The Shared Hull Regime Multiplier ($\mathcal{M}_{\mathrm{Regime}}$):**
   * **Sunk in `SS0` LTFM Drift (`-16.21% CE` / `-21.69%` under `H:09` Defense):** $\mathcal{M}_{\mathrm{Regime}} = \mathbf{0.5\times}$ *(No individual hoarder wins on a broken nation—if Struggling Launch stays $>15\%$ or Crown Debt $>100\%$, there is no individual winner; the table loses to Orthodoxy!)*
   * **Stable `SS1` Foil-Borne (`+15.04% CE` National):** $\mathcal{M}_{\mathrm{Regime}} = \mathbf{1.0\times}$
   * **Full `SS2` Harvest (`+24.70% CE` Pre-NDC / `+25.19%` *Te Kāhui Waka*, Debt `21%–22%`, Super `64`, Cohesion `126.0`):** $\mathcal{M}_{\mathrm{Regime}} = \mathbf{1.5\times} + \mathbf{0.05\times}$ **per Turn Early** (`+0.25x = 1.75x` under `Plan C`!). *(Bonus `+0.25x` Resilience Badge if the crew also absorbed **`H:09` `3.0%` GDP Defense Shock** at `+21.18% CE` and `31.5%` debt!)*
2. **Inverse-Hub Mana Royalties (`Variant B` Anti-Snowball Engine):**
   * Whenever Player B uses a River card or `K:09` *Aunty's House* shield founded by Player A, the **Shared Commons (`N:06`)** mints **Mana Royalties** to Player A (capped at `2 payouts/card/turn`, or `3` with `N:06` *Paul Romer*).
   * **Inverse-Hub Scaling:** Founding rare outer-edge or provincial cluster cards (`C:08`, `C:09`, `C:10`, `B:05`, `E:02`) pays **`+2 Mana` per neighbor tap**, whereas crowded central hub cards (`B:01`, `B:08`) pay **`+1 Mana` per tap**—preventing Turn-1 snowballing so rural and specialist stewards race neck-and-neck with early-years founders!
3. **Bystander Forfeit Rule:** Any player who contributed **zero Zone-B Mana stakes** to active River subsystems during an era (`SS1` or `SS2`) suffers `-4 Mana` Free-Rider Forfeit at era transition.

### 9.2 Mode A (Standard Automated Bosses) vs. Mode B (Feral Rentier Spoiler Cards)
* **Mode A — Automated Structural Headwinds (Default):** `H:01–H:10` and `T:01–T:10` trigger automatically when their board conditions or D20 Reef/Stability windows hit. All players are constructive stewards wrestling over wave priority, royalties, and launch timing.
* **Mode B — Cutthroat Lobbyist / Feral Spoiler Variant (`3–6 Players`):** Each player holds 2 secret Trap/Orthodoxy cards (`feral_kickback_wealth: 2..4`). On your turn, you may play a Trap/Boss card *against* the table to pocket its immediate **Private Kickback (`+3` or `+4 Wealth`)**—e.g., lobbying for `H:07` (*Landlord Capture*), `H:08` (*Duopoly Cartel*), or `T:04` (*Single-Shot Surge*). *The Catch:* If your sabotage drags the macro hull below `SS1` or triggers **`H:09`** collapse (`0.5x` multiplier), your hoarded `5:1` silver coins turn to ashes alongside everyone else!

### 9.3 Solo & Full Co-Op Race Mode: *Chasing Finland+* (`P:07`)
In Solo or pure Co-Op play, place rival yacht markers on the **0–130 Cohesion & Capability Track** and roll `1d20` each turn to advance the automated pace-boats:
* **Scotland (`T:08` Pace-Boat):** Fast early sprint (`+6 pts/turn` via ECE & mentoring), **hard-stalls at `96.0`** for lack of Land/Estate tax sovereignty (`B:07`/`B:08`).
* **1989 Japan (`T:10` Pace-Boat):** Surges to **`112.0`** on Deming industrial quality, then **crashes `-3 pts/turn`** into a 14-turn land bubble because `B:08` + `B:14/B:15` were omitted.
* **Finland (`C:02` Benchmark Yacht):** Steady high-trust pace (`Roll 1–5: +4 | 6–15: +5 | 16–20: +6`), cruising to **`118.0`**. To overtake Finland and hit **`126.0`** before Turn 20, Aotearoa must weather the J-curve (`Turns 1–5`) and slingshot past on coupled `SS2` hydrofoils!

---

## 10. Worked 2-Turn Tabletop Walkthrough (4 Players, `2-of-3` *Whānau* Mode)

* **Setup Rolls (`B:00`):**
  * **Player 1 (`Vigintile 2`, `Rural`, `[Slot 1 Age 4 + Slot 2 Age 30]`, `1 Wealth`):** Drafts **`K:01` (*Catalytic Steward — Barnardos/Iwi*)** first under Rawls's Maximin rule.
  * **Player 2 (`Vigintile 6`, `Auckland`, `[Slot 1 Age 4 + Slot 2 Age 30]`, `2 Wealth`):** Drafts **`K:04` (*Whānau & Housing Justice Weaver*)**. *Urgent Crunch:* Holds an Age-4 toddler in Wave-3 `Auckland`!
  * **Player 3 (`Vigintile 13`, `Large` [Wellington], `[Slot 2 Age 42 + Slot 3 Age 66]`, `2 Wealth`, Empty `Slot 1`):** Drafts **`K:09` (*Kaumātua & `K_whanau` Anchor*)**.
  * **Player 4 (`Vigintile 20` -> Sub-roll `16` Active `z_h` Founder, `Small` Town, `[Slot 2 Age 39 + Slot 3 Age 65]`, `4 Wealth`, Empty `Slot 1`):** Drafts **`K:05` (*Enterprise Wayfinder — GrowthNZ*)**.

* **Turn 1 (`Years 1–3`):**
  1. **P1 (`K:01`, `Rural`):** Taps `K:01` to launch **Wave 1 (`1/3 Rural + Small`) of `B:01` (*First 2000 Days*)** under **`N:01` (*Te Kāhui Waka*)** at `50%` Political Drag (`1 Wealth`), staking `1 Mana` in Zone B. P1's Age-4 rural child is covered just before turning 7! Enacts **`E:01` (*Waves 1–3 Provincial Electrification*)** with P4's `1-Wealth` co-stake—hitting `100%` `Rural+Small` solar/EV relief (`-28%` fuel burden) immediately!
  2. **P2 (`K:04`, `Auckland` Waiter Dilemma!):** P2's Age-4 Auckland toddler will turn **Age 7** at Turn-2 Sunrise—before Wave 7 reaches `Auckland`! Tempted by **`T:02`** (`+2 Wealth` coerced double-shift shortcut), P2 warns P4 (`K:05`) that taking `T:02` will drop a **Skill-Shortage Liability Token** onto P4's enterprise mat. P3 (`K:09`, holding a `Slot 3` *Kuia*) offers **`Aunty's House` (`K_whanau` shield)**: P2 pays `1 Wealth` + `1 Mana` Royalty to P3 (`Variant B`) to bridge the Auckland toddler cleanly across Gate 1! With Action 2, P2 initiates **`B:08` (*10-Yr LVT + Corp Cut*)** in `Auckland`.
  3. **P3 (`K:09`, `Large` [Wellington]):** Collects `1 free Experience Token` from `Slot 3` Elder and spends it to play **`N:04` (*Williamson's Actuarial Ledger*)** for `0 Wealth`! Uses Action 2 to lock `Large`'s Regional Tax Key into **`C:06`** alongside P2's `Auckland` and P4's `Small`—saving `Large` from `-60%` two-flank tax leakage!
  4. **P4 (`K:05`, `Small` `z_h` Builder):** Co-stakes **`B:07` (*3-Yr Fast CGT/Estate Ramp*)** + **`C:08` (*Monopsony/Duopoly Breaker*)**, then links with P1 (`K:01`) on **Wedge `1x2`/`2x3`**—rolling `2d20` with Advantage (`B:12`: rolls `4` and `17` $\to$ keeps **`17` Tailwind**!), banking `+4 Mana` and drawing the table's **first hidden `B:13` Orbital Compass Card**!

* **Turn 2 (`Years 4–6` — Year-5 Audit Window):**
  * At Sunrise, both P1's and P2's children cross Age 6 (`-> Age 7`) holding **Readiness Counters (`N:03`)** with `0` Struggling Tokens added to the Crown ledger!
  * P1 + P4 co-stake **`B:09` (*ACC Year-5 Continuation Valuation*)**, booking **`3.84x` (`NZD 35.25B`)** forward return to shatter **`H:01` (*Cash-Flow Myopia*)** permanently and arming **`+5` total Stability Shields (`B:09` + `N:04`)** just in time for Turn 3's first Parliamentary Election roll!
