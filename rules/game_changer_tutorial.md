# Module 5: The "Game Changer" Tutorial — What Happens When You Want to Play a Card That Doesn't Exist?

> *"Welcome to **game CHANGER**, the only game show where the game changes every show. [...] The only way to learn is by playing; the only way to win is by learning; and the only way to begin is by beginning."* — **Sam Reich**

We have our own **Game Changer** Premise: In conventional politics, players treat the economic board as fixed and fight zero-sum battles over a shrinking pie. In *Foils & Founders*, every card in the deck is a dense, empirically anchored systems-engineering argument. When a player discovers that a vital card is missing from the game, the table doesn't just make up a wishful rule—it puts the proposal through the crucible of first-order fiscal honesty (**Easy Mode**) and second-order general-equilibrium discovery (**Challenge Mode**).

Suppose a player sits down at the Big Table and says: **"I want to play the Energy Transition / Electrify Aotearoa Card!"**

They flip through the Base Game (`B:00`–`B:09`) and the Climate Expansion (`C:01`–`C:06`), and realize: there is no standalone *"Electrify Every Household"* card in the base deck.

In an open-source strategy game (just like in a real democracy), when a card doesn't exist yet, you don't have to sit on your hands—you can author a **Game Changer**. There are two ways to do this:

* **Level 1 (Tabletop Easy Mode — The First-Order Fiscal Debate):** You propose a house-rule card on the fly by arguing over upfront capital costs, fossil-fuel import savings, and how much an aggressive energy transition might crowd out urgent social investments (`B:01`, `B:02`) inside a fixed budget envelope.
* **Level 2 (Open-Source Challenge Mode — Recomputing the Stationary Distribution):** Instead of fighting over a fixed pile of capital, you write a new VFI Toolkit module (like [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m)) that changes the underlying physics of the board—proving that turning energy from an unbounded stochastic shock into a solar endowment eliminates excess precautionary savings, unlocking dormant capital across the entire economy so nothing gets crowded out.

Here is **Tutorial Part 1 (Easy Mode)**—how a table of players negotiates a new card inside conventional first-order economics.

---

## Tutorial Part 1 (Easy Mode): Negotiating the "Energy Transition" Card & The Crowd-Out Debate

In Easy Mode, players don't touch the MATLAB code. Instead, the player proposing the Energy Transition drafts a custom card on a write-in wildcard (`E:??`) and has to get the other Wayfinders at the table (`K:01` Philanthropist/Iwi, `K:02` Venture Catalyst, `K:03` Treasury/RBNZ Helmsman) to agree on its **Cost** and **Game Text**.

### Step 1: The Player's Opening Pitch (First-Order Savings)

The proposing player points to the *Rewiring Aotearoa* and *Queenstown Electrification Accelerator (QEA)* benchmarks:

* **The Pitch:** *"New Zealand households and businesses burn roughly **NZD 20B/yr** on mostly imported fossil fuels (or NZD 29M a day). Replacing petrol cars and gas heaters with EVs, heat pumps, rooftop solar, and batteries cuts appliance lifecycle costs by **2x to 3x** (and **4x to 9x** over a homeowner's lifetime) and saves Aotearoa **NZD 10.7B/yr by 2040**—while avoiding the coalition Government's **NZD 6.2B imported LNG terminal** boondoggle! I want to claim **+NZD 10.7B/yr** in additional budgetary clearance!"*

### Step 2: The Table Contests the Card (The "Crowd-Out" Clash)

Before the card can enter play, the other Personas around the table challenge its **Upfront Capital Intensity**:

* **The `K:03` Treasury Helmsman Objects (The Upfront CapEx Wall):** *"Hold on! As Rewiring Aotearoa notes, electrification requires 'swapping fuels for finance'. A 5kW rooftop solar + 10kWh battery setup costs roughly **NZD 20,000 per household** (1/6th of median household income). Across 2 million households, rapid national electrification requires **NZD 30B to NZD 40B in upfront capital**! In Phase 1 (`SS1`), our fiscal envelope is strictly cash-neutral: every dollar of public subsidy or Crown debt capacity is already committed to `B:01` (First-2000-Days Wraparound, NZD 9.19B over 5 years) and `B:02` (*Tuakana–Teina* Mentoring)."*
* **The `K:01` Catalytic Steward Warns of Social Crowd-Out:** *"If you divert NZD 3B/yr of Phase 1 public funds away from `B:01` (First 2000 Days) to subsidize rooftop solar panels for middle-class homeowners, low-income renters stay trapped in the 22% Dunedin hardship corner (`i_c = 0`). You'll save on petrol imports, but you'll blow a **NZD 17.7B to 28.5B/yr hole** in Oranga Tamariki state care, hospital nights, and prisons (`Exits 1, 2, 4`)!"*

### Step 3: The Easy-Mode Compromise (The Intensity Dial)

To resolve the dispute using only first-order budget math, the table must agree on an **Electrification Intensity Dial** (*Option A, B, C, or D*) that balances fuel savings against social-investment crowd-out:

| Chosen Intensity / Targeting Level | Upfront Capital Draw | First-Order Fuel & Household Benefit | Social Investment & Distributional Risk (`SS1`) | Table Verdict (First-Order Math Only) |
| :--- | :--- | :--- | :--- | :--- |
| **Option A: Aggressive Universal Sprint** *(100% Upfront)* | **High** *(Diverts NZD 3B–5B/yr from `SS1` pool)* | `+NZD 10.7B/yr` savings + cancels NZD 6.2B LNG terminal | **Severe Crowd-Out:** Raids `B:01` & `B:02`; leaves cohort stunting at `>12%` and triggers `H:01` (Cash-Flow Trap). | **Rejected by `K:01` & `K:03`:** Saving kilowatt-hours by sacrificing three-year-olds breaks the front foil! |
| **Option B: "End-of-Life" Replacement Pace** *(84% Machines)* | **Moderate** *(Private green-loans + `SS2` `C:04` pool)* | `+NZD 5.5B/yr` early savings, ramping to `NZD 10.7B/yr` by 2040 | **Zero Crowd-Out:** Protects 100% of `B:01` First 2000 Days & `B:02` Mentoring in `SS1`; scales grid in `SS2`. | **Accepted as Baseline `E:01`:** Safe within first-order rules, but takes 15–20 years to ramp up. |
| **Option C: Tax Breaks for Median & Above** *(`P50–P100` Rebates)* | **High Fiscal Leakage** *(`-NZD 1.5B–2.5B/yr` in lost tax revenue)* | Subsidizes `P50–P100` owners who already earn `15%–17%` IRR on PV | **Regressive "Grid Death Spiral":** Shifts fixed lines charges onto `P01–P50` renters, worsening the `B:01` hardship corner! | **Rejected (The "Reverse Robin Hood" Trap):** Pays wealthy homeowners for what they'd buy anyway while squeezing renters. |
| **Option D: Infra-Pool Solar for Median & Below** *(`P01–P50` via `C:04`)* | **Targeted** *(`NZD 1.5B/yr` via Kāinga Ora, Iwi, & `C:04` VPP bonds)* | `+NZD 2.5k–4.5k/yr` bill relief for `P01–P50` whānau, schools, & marae | **Negative Crowd-Out (Synergy!):** Warm, dry homes slash `Exit 2` (Paediatric Hospitalisations) & lift `B:01` family budgets! | **Accepted as Upgraded `E:01+`:** Solves the landlord-tenant split incentive and accelerates Year 5 ACC breakeven (`B:07`)! |

### The Resulting "Easy Mode" Custom Card (`E:01`)

#### `E:01` — Swapping Fuels for Finance (The First-Order Electrification Card)
* **Type:** Player-Drafted Artifact — First-Order Energy Transition (Easy Mode)
* **CO2e Impact Badge:** `🌱 -10.0 MtCO2e / yr` (`computed`)
* **Cost / Requirement:** Cancel the NZD 6.2B Imported LNG Terminal + Sequence via End-of-Life Appliance Replacement (or pay Social Crowd-Out Penalty if rushed in Turn 1).
* **Game Text:**
  * **The Crowd-Out Constraint:** If you fund this card by raiding `B:01` (First 2000 Days) or `B:02` (*Tuakana–Teina* Mentoring) in Phase 1 (`SS1`), take **+NZD 105,000/yr per stunted child** in reactive remediation hull drag.
  * **Disciplined Sequencing:** If you sequence electrification through end-of-life machine replacement in `SS1` and pair it with `B:06` / `C:04` (The 2050 50/50 Infrastructure Pool) in `SS2`, gain **+NZD 10.7B/yr in Household Energy Savings**, improve the Balance of Trade, and cut **10.0 MtCO2e/yr** of emissions without crowding out a single dollar of child investment.
  * **Targeting Rule (Option D Beats Option C):** Never spend Crown tax breaks subsidizing top-half homeowners (`P50–P100`) who can already finance solar out of their own precautionary buffers (*Option C*—causes a regressive Grid Death Spiral for renters). Instead, route public infrastructure capital (`C:04`) into **Bottom-Half Whānau, Social Housing, Schools, and Marae (*Option D*)**—overcoming the landlord-tenant split incentive, slashing `Exit 2` (Paediatric Respiratory Hospitalisations) from cold/damp homes, and accelerating `B:07` (Year 5 ACC Breakeven)!
* **Flavor Text:** *"In first-order economics, every dollar spent on a solar panel looks like a dollar stolen from a kindergartner. To get both at once without waiting twenty years, you have to look at the second-order math..."*

---

## Tutorial Part 2 (Challenge Mode): Recomputing the `StationaryDist` (`QEA-2026` & Firming the Economic Grid)

In Challenge Mode, the player refuses to accept the "Easy Mode" compromise where electrification has to wait 15–20 years for end-of-life replacement to avoid crowding out social investment. Instead, the player taps `K:04` (The "1925 Moment" Architect) and `N:05` (Paul Romer's Collective Intelligence Reactor) to ask a deeper, second-order question: **Why does the table think capital is scarce in the first place?**

### Step 1: Identifying the Hidden Orthodoxy Bug (Excess Precautionary Savings)

Drawing on *Firming the Economic Grid* (and heterodox economist Steve Keen's maxim that *"Capital without energy is a statue; Labor without energy is a corpse"*), the player exposes a massive second-order inefficiency in the status quo board state:

* **The Unbounded Energy Shock (`z2`):** In the fossil-fuel status quo, households and firms face not only working-age unemployment shocks and retirement medical shocks (`z1`), but lifelong, unbounded AR(1) commodity energy price shocks (`z2`)—amplified whenever geopolitical wars (Ukraine 2022, Iran 2026) spike oil, gas, and electricity prices.
* **The Precautionary Over-Saving Trap:** As VFI Toolkit creator Professor Robert Kirkby observed, incomplete-market agents facing uninsurable tail risks (`sigma = 2.2`, `rho_z2 = 0.75`, `sigma_epsilon_z2 = 0.25`) systematically **over-save** compared to what their utility functions imply, hoarding liquid buffer stocks that end up as excess "accidental bequests" at death.
* **The RBNZ Monetary Drag:** As the Reserve Bank of New Zealand (RBNZ) noted in February 2026 (when holding the OCR at 2.25%), household precautionary savings in New Zealand remains stubbornly "high"—forcing the Reserve Bank to expend monetary effort fighting paradoxical household hoarding while productive businesses starve for capital and workers grind through life with almost zero leisure before age 65!

### Step 2: Writing the Open-Source Module ([`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m))

Rather than arguing at the table with hand-waving assertions, the Challenge Mode player forks the open-source VFI Toolkit codebase and writes [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) to solve for a new Stationary Distribution (`StationaryDist_FHorz_Case1`) across 81 lifecycle periods (ages 20 to 100):

* **3 Endogenous Asset States (`n_a = [97, 5, 41]`):**
  1. `a`: Household liquid savings and debt (`asset_grid`);
  2. `pv`: Shares of Rooftop Solar PV + Battery assets (`pv_grid`), where a full 5kW PV + 10kWh battery system costs 1/6th of median household income (~NZD 20k on a NZD 120k median income), divided into five 1kW + 2kWh shares at `pv_share_price = 1/30` of income each;
  3. `ks`: KiwiSaver retirement account modeled as an `experienceassetz` (`ks_r = 7%`, with employee/employer contributions).
* **2 Exogenous Stochastic Shocks (`n_z = [2, 5]`):**
  1. `z1`: Age-dependent unemployment shock before retirement (`Jr = 65`) and idiosyncratic medical expense shock (`z1 == 0.3`) in retirement;
  2. `z2`: Discretized Farmer–Toda AR(1) energy price shock (`Params.energy_shock_magnitude = 2`).
* **The Mechanism (Energy as Endowment vs. Expense):** When agents purchase `pv` shares, the solar + battery endowment first covers their own household energy budget (immunizing them against `z2` fossil-fuel spikes) and then on-sells surplus electricity to the grid at 50% of the retail rate, while converting a depreciating fossil-fuel expense into an intergenerational physical asset that satisfies the warm-glow bequest motive (`wg1 = 1.5`, `wg2 = 3`).

### Step 3: What the New Stationary Distribution Reveals (Changing the Rules of the Game)

When the GPU finishes solving `ValueFnIter_Case1_FHorz` and `LifeCycleProfiles_FHorz_Case1`, the player projects **Figure 1 (`Energy as Expense: pv = 0`)** and **Figure 2 (`Energy as Endowment: pv_regimes = [5]`)** onto the Big Table:

| Lifecycle & Macro Dimension | Regime 1: Energy as Expense (`pv = 0`, Fossil/LNG Status Quo) | Regime 2: Energy as Endowment (`pv = 5`, Solar + Battery) | Why It Changes the Game (Second-Order Payoff) |
| :--- | :--- | :--- | :--- |
| **Exposure to Energy Shocks (`z2`)** | **Unbounded:** Geopolitical fuel spikes hit transport, heating, and indirect goods prices across all 81 years. | **Immunized:** Rooftop PV + battery covers household load and earns 50% grid feed-in revenue when prices spike. | Turns an uninsurable stochastic liability into a hedge and a planned intergenerational bequest. |
| **Precautionary Savings (`a`)** | **Artificially High (Hoarded):** Households over-save liquid cash all life to self-insure against `z1 × z2` compound shocks. | **Released into the Economy:** Eliminating energy tail-risk cures excess precautionary hoarding across working life. | **Unlocks the "Missing Capital":** Households don't need subsidies—freed precautionary buffers self-finance `pv` AND crowd in consumption/investment! |
| **Working-Age & Retirement Leisure (`leisure_h`)** | **Crushed Before Age 65:** Average Kiwis must over-work (`h`) to maintain buffer stocks, enjoying leisure only after retirement. | **Expanded Across the Lifespan:** Agents work less frantic hours to cover the same shocks and enjoy higher leisure before and after 65. | Directly confirms Saul Griffith's observation: nations that electrify see unexpectedly higher GDP and well-being! |
| **RBNZ Monetary & Trade Stability** | **High Friction:** Excess precautionary savings + NZD 20B/yr fuel imports force RBNZ to fight the economy with OCR hikes. | **Firmed Economic Grid:** Lower precautionary drag + `+NZD 10.7B/yr` trade improvement + national energy security. | Gives the Reserve Bank (`K:03`) permission to lower OCR rates without stoking imported inflation! |

### Step 4: The Resulting "Challenge Mode" Game-Changer Cards (`E:02` & `E:03`)

Because the player proved mathematically in [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) that electrification releases trapped precautionary capital rather than crowding out social spending, the table upgrades `E:01` into two permanent **Challenge Mode Game-Changer Cards**:

#### `E:02` — Energy as Endowment (The `QEA-2026` Stationary Distribution Shift)
* **Type:** Open-Source Engine — Second-Order Lifecycle Transformation (Challenge Mode)
* **CO2e Impact Badge:** `🌱 -14.8 MtCO2e / yr` (`computed`)
* **Requirement:** Fork [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) on the GPU + Allow Households to Acquire 1/30th-Income Solar PV + Battery Shares (`pv_regimes = [5]`).
* **Game Text:**
  * **Cancel the Crowd-Out Myth:** Converting household energy from an unbounded AR(1) fossil-fuel shock (`z2`) into a Solar + Battery Endowment (`pv`) eliminates the need for Excess Precautionary Savings against energy spikes.
  * **Self-Financing Capital Release:** Release hoarded precautionary buffer stocks (`a`: **NZD 60.8B to 91.5B nationally**) back into active circulation—financing household and 5-sector electrification (`NZD 60.2B–75.5B` CapEx) without raiding `B:01` (First 2000 Days) or `B:02` (*Tuakana–Teina* Mentoring) in Phase 1 (`SS1`)!
  * **The Leisure & Bequest Dividend:** Increase household Leisure (`leisure_h`) across both working age and retirement, generate 50% grid feed-in income, and turn rooftop solar panels into an Intergenerational Bequest Asset for the next cohort.
* **Flavor Text:** *"Capital without energy is a statue; labor without energy is a corpse. Turn the sun into a household endowment, and the statue starts flying."*

#### `E:03` — Firming the Economic Grid (The RBNZ & National Security Dividend)
* **Type:** Macroeconomic Enchantment — Monetary & Trade Stabilizer (Challenge Mode)
* **CO2e Impact Badge:** `🌱 -3.2 MtCO2e (No LNG)` (`computed`)
* **Cost / Requirement:** Pair `E:02` (Energy as Endowment) with `K:03` (The Sovereign Helmsman — Treasury & RBNZ).
* **Game Text:**
  * **Cure the Precautionary Paradox:** Because households are no longer over-saving out of fear of commodity fuel shocks, the Reserve Bank of New Zealand no longer has to fight paradoxical demand drag with blunt OCR interest-rate hikes.
  * **Triple Macro Payoff:**
    1. **Horsepower-to-Weight Lift:** Increase the operating efficiency of the national economic engine—generating unexpectedly higher GDP (`+3.8% to +5.4%`) alongside **NZD 15.55B/yr** in direct 5-sector fuel savings.
    2. **Balance of Trade & National Security Shield:** Slash reliance on imported fossil fuels and cancel the **NZD 6.2B imported LNG terminal**, insulating Aotearoa against foreign wartime energy blockades.
    3. **Combined Rate Cut:** Stack with `B:06` (The 2050 50/50 Stabilizer) to reinforce the **-60 to -100 bps domestic interest rate reduction** for all homeowners and high-growth firms (`B:05`).
* **Flavor Text:** *"Why spend NZD 6.2 billion on an LNG terminal to import foreign price shocks when you can firm the electricity grid and the macroeconomic grid with the same ray of sunshine?"*

---

## Summary of the Tutorial: Why Open-Source Economics Wins the Game

* **In Easy Mode (`E:01`):** Players trapped inside a static, first-order budget pie are forced to argue over whether solar panels crowd out kindergartners.
* **In Challenge Mode (`E:02` + `E:03`):** A player who can write a 500-line open-source VFI Toolkit module ([`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m)) proves that the pie itself was artificially shrunken by precautionary fear—and that removing the fear unlocks the capital to fund both!

---

## Tutorial Answer Key: The 5-Sector National Electrification Scorecard (`QEA-2026` Scaled to All of Aotearoa)

When a player scales the second-order mechanism in [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) and *Firming the Economic Grid* across all five sectors of the New Zealand economy—(1) Households, (2) Schools & Marae, (3) Commercial Firms, (4) Agriculture, and (5) Transport—the macroeconomic result resolves the "Crowd-Out" debate once and for all:

> **The Self-Financing Theorem:** The **Second-Order Precautionary Capital Release (`NZD 60.8B – 91.5B`)** unlocked by eliminating fossil-fuel price volatility (`z2`) is larger than the entire **Upfront 5-Sector CapEx (`NZD 60.2B – 75.5B`)** required to electrify the country. New Zealand already has 100% of the capital sitting idle in defensive buffer stocks on private balance sheets—meaning we can electrify all five sectors without crowding out a single dollar of Phase 1 (`SS1`) child and adolescent investment (`B:01`, `B:02`).

### 1. The 5-Sector Scorecard: CapEx, Cash Payback, & Precautionary Capital Unchained

*(Calibrated to New Zealand's ~2.0M households, ~2,500 schools + ~800 marae, ~550k SMEs/commercial buildings, ~50,000 farms/orchards, and ~4.5M fleet vehicles, using `QEA_2026.m` relative risk aversion `sigma = 2.2` and AR(1) energy shock persistence `rho_z2 = 0.75`, `sigma_epsilon_z2 = 0.25`; see [`data/electrification_5sector.csv`](../data/electrification_5sector.csv))*

| Sector | Upfront CapEx (Net) | Annual Cash Savings | Cash Payback | Precautionary Capital (`Delta A_prec`) | Key Macro & IGWelfare Payoff |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Households** *(~1.6M homes: 5kW PV + 10kWh battery + heat pump)* | `NZD 28B – 32B` *(~1/6th median income)* | `NZD 4.80B / yr` *(3x lifecycle + 50% export)* | `5.8 – 6.5 yrs` *(15%–17% IRR)* | `NZD 32.0B – 45.0B` *(~NZD 20k–28k/hh buffer)* | Eliminates `z2` utility tail-risk; frees leisure (`leisure_h`), relieves `B:01` corner, & creates bequest asset. |
| **2. Schools (~2,500) & Marae (~800)** *(25–100kW PV + storage)* | `NZD 1.2B – 1.5B` *(Via `B:06` / `C:04` Pool)* | `NZD 0.35B / yr` *(School & Marae op-cash)* | `3.5 – 4.3 yrs` *(1:1 daytime load match)* | `NZD 1.8B – 2.5B` *(Disaster reserve release)* | **Civil Defence & Tuakana Hubs (`C:03`):** Cyclone-proof microgrids; redirects power bills to classrooms (`T:05` counter). |
| **3. Commercial & Industrial** *(Roof PV, heat pumps, & BESS)* | `NZD 12B – 15B` *(Corp CapEx / PPAs)* | `NZD 3.10B / yr` *(Peak-shave + process heat)* | `4.0 – 4.8 yrs` *(20%+ pre-tax IRR)* | `NZD 14.0B – 20.0B` *(Working-capital buffers)* | **Unchains Firm Value (`z_h`, `B:05`, `T:04` counter):** Rotates idle winter-spike cash into R&D, plant, & `+3.2%–9.6%` wages. |
| **4. Agriculture & Horticulture** *(EV tractors, dairy, & pond PV)* | `NZD 6B – 8B` *(Farms & 19k+ ponds)* | `NZD 1.40B / yr` *(Cuts diesel & pumping)* | `4.3 – 5.5 yrs` *(Forest Lodge / Acquasol)* | `NZD 5.0B – 8.0B` *(Farm diesel/input buffer)* | **Dual-Use Water & Land:** Turns farm ponds into 250kW–1MW power plants; shields food from oil shocks. |
| **5. Transport (Light, Ute, Freight)** *(End-of-life swap of 84% fleet)* | `NZD 13B – 19B` *(Marginal over ICE)* | `NZD 5.90B / yr` *(Petrol/diesel vs. solar EV)* | `2.5 – 3.5 yrs` *(Marginal EV premium)* | `NZD 8.0B – 16.0B` *(Household/freight fuel buffer)* | **4-Region Compass (`C:05`):** Eliminates the `2.7x–2.8x` Rural/Small-town fuel penalty; lifts regional welfare. |
| **NATIONAL TOTAL (All 5 Sectors Coupled)** | **`NZD 60.2B – 75.5B`** *(~NZD 5B/yr over 12 yrs)* | **`NZD 15.55B / yr`** *(>NZD 10.7B/yr baseline)* | **`4.5 – 5.2 yrs`** *(Within 1.5 parl. terms)* | **`NZD 60.8B – 91.5B`** *(100%+ CapEx unlocked!)* | **Firms Macro Grid (`E:02`+`E:03`):** Cancels NZD 6.2B LNG terminal & lets RBNZ cut rates `60–100 bps`! |

---

### 2. Sector-by-Sector Notes for the Game Master (`K:04` Architect's Guide)

1. **Households (`NZD 28B–32B` CapEx $\rightarrow$ `NZD 4.8B/yr` Savings + `NZD 32B–45B` Precautionary Release):**
   * With relative risk aversion `sigma = 2.2` and an AR(1) energy shock of magnitude `2x` (`rho_z2 = 0.75`), a typical Kiwi household holds **NZD 20,000 to NZD 28,000** in low-yield liquid precautionary savings (`a`) across its working life just to buffer the compound risk of an unemployment or medical shock (`z1`) colliding with a winter power or petrol spike (`z2`).
   * Swapping NZD 20,000 of that sterile precautionary buffer into 5 shares of Solar PV + Battery (`pv = 5`) drops `z2` exposure to zero (and turns it positive via the 50% grid feed-in tariff). Households no longer need to hoard precautionary cash or work frantic overtime hours (`h`) to rebuild buffer stocks—expanding working-age leisure (`leisure_h`) while leaving the solar panels as a physical bequest for their children.
2. **Schools (~2,500) & Marae (~800) (`NZD 1.2B–1.5B` CapEx $\rightarrow$ `NZD 0.35B/yr` Savings + `3.5–4.3 Year` Payback):**
   * **Why Schools & Marae Have the Fastest Stationary Payback:** Unlike homes (which peak in the morning and evening), schools consume **85%+ of their electricity between 8:30 AM and 3:30 PM**—matching the solar generation curve 1:1 without needing oversized batteries.
   * Electrifying all 2,500 state/integrated schools and 800 marae costs just NZD 1.2B to 1.5B and saves **NZD 350M/yr** in school and marae operational budgets—enough to fund **25,000+ student places** in *Tuakana–Teina* / Graeme Dingle Foundation mentoring (`B:02`) and Finnish-style *Monilukutaito* disinformation inoculation (`T:05` counter-play) every year for free, while turning every school and marae in Aotearoa into a cyclone-proof civil defence lifeboat (`C:03`).
3. **Commercial & Industrial Firms (`NZD 12B–15B` CapEx $\rightarrow$ `NZD 3.1B/yr` Savings + `NZD 14B–20B` Working-Capital Release):**
   * In the Guvenen et al. (2023) and Murphy, Shleifer, & Vishny (1991) firm modules (`B:05`, `T:04`), collateral-constrained entrepreneurs (`z_h`) must hold defensive cash buffers against input-cost volatility (especially dry-year wholesale electricity spikes and fossil process-heat shocks).
   * Deploying commercial rooftop solar, heat-pump process heat, and behind-the-meter batteries cuts commercial energy bills by **NZD 3.1B/yr** (4.0–4.8 year payback) and releases **NZD 14B–20B in corporate precautionary working capital**—rotating idle bank deposits directly into R&D, productive plant, and `+3.2% to +9.6%` higher regional wages (`B:05`).
4. **Agriculture & Horticulture (`NZD 6B–8B` CapEx $\rightarrow$ `NZD 1.4B/yr` Savings + `NZD 5B–8B` Rural Buffer Release):**
   * Proven at **Forest Lodge Orchard** in Central Otago and across New Zealand's **19,000+ farm irrigation and oxidation ponds** (via standardized 250kW–1MW floating solar arrays plus electric tractors, frost fans, and dairy sheds), electrifying the farm gate pays back in 4.3–5.5 years and permanently insulates domestic food prices and rural exporters from Middle East diesel blockades.
5. **Transport (`NZD 13B–19B` Marginal CapEx $\rightarrow$ `NZD 5.9B/yr` Savings + `2.5–3.5 Year` Marginal Payback):**
   * Replacing the 84% of vehicles that can be cost-effectively electrified at the end of their normal useful life requires only NZD 13B–19B in *marginal* CapEx over buying another combustion vehicle, while saving **NZD 5.9B/yr** in imported petrol/diesel and maintenance.
   * Crucially, this solves **`C:05` (The 4-Region Just-Transition Compass)**: because **Rural (`16%` pop)** and **Small Provincial Towns (`24%` pop)** spend **2.7x to 2.8x more** of their household budget on transport fuel than metropolitan cities, pairing rural rooftop solar with EVs/electric utes eliminates that geographic penalty and boosts rural/provincial welfare by an extra `+2.5% to +3.8%` CE.

---

### 3. The Three Macroeconomic Equations That Change the Board (`E:02` + `E:03`)

1. **Zero Social Crowd-Out (`Delta A_prec >= CapEx`):**
   $$\text{Upfront 5-Sector CapEx } (\text{NZD } 60.2\text{B}–75.5\text{B}) \le \text{Released Precautionary Capital } (\text{NZD } 60.8\text{B}–91.5\text{B})$$
   Removing energy tail-risk releases enough trapped precautionary capital from private balance sheets to self-finance the entire national transition without touching Phase 1 (`SS1`) social investment.
2. **A `+NZD 15.55B/yr` Balance-of-Payments & GDP Engine (`+3.8% to +5.4%` Permanent GDP Lift):**
   Stopping NZD 15B–20B/yr in foreign fossil-fuel outflows (and canceling the NZD 6.2B imported LNG terminal) keeps **NZD 15.55B/yr** compounding inside Rural, Small, Large, and Auckland regional economies—explaining Saul Griffith's observation that nations that electrify achieve unexpectedly higher GDP.
3. **The RBNZ "OCR Freedom" Dividend (`-60 to -100 bps` Lower Interest Rates):**
   Eliminating imported oil-shock inflation from the CPI basket and curing paradoxical precautionary hoarding allows the Reserve Bank (`K:03`) and the 2050 50/50 Debt-Sinking Protocol (`B:06`) to lower equilibrium New Zealand interest rates by **60 to 100 basis points**—cutting mortgage stress for every young family and supercharging productive enterprise across Aotearoa.
