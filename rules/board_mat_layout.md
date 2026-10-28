# Foils & Founders: Board Mat Layout, Visual Zones, & Component Architecture

> *"Not all lives are easy, but none should be impossible."*  
> — **Rule Zero (`B:00`: The Rawlsian D20 Reef Bar)**

*Physical & Visual Tabletop Specification for **Beyond the Magic Money Tree — Foils & Founders: The Aotearoa Deck***  
**Cross-References:** `rules/foils_and_founders_gameplay.md` • `rules/strategy_study_guide.md` • `rules/kaupapa_identities.md` • `STORIES.md`  
**License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

---

## 1. Physical Dimensions & Dual-Lens Visual Theme

The **Foils & Founders Central Macro Mat** is formatted for standard tabletop and workshop printing at **$900\text{ mm} \times 600\text{ mm}$ ($36'' \times 24''$)** (rendered at $1800 \times 1220\text{ px}$ in `scripts/render_board_mat.py`), paired with individual **Multi-Generational Cohort Command Mats** ($280\text{ mm} \times 180\text{ mm}$ / A4 landscape).

Every zone on the mat displays **dual-lens bilingual typography** honoring the two hulls of *Te Waka Hourua* (`STORIES.md`):
* **Hull A (Systems Engineering / America's Cup Hydrofoil):** Deep Pacific Navy (`#0B1D33`), Foiling Cyan (`#00B4D8`), and Titanium Silver.
* **Hull B (*Te Waka o Whānau* / Te Ao Māori & Moana Pasifika *Pūrākau*):** Kauri Gold (`#D4A359`), Pounamu Green (`#2A9D8F`), and Kokowai Ochre (`#E76F51`).
* **Hazard & Emergency States:** Subsistence/Jeopardy Crimson (`#D62828`) and Lavoisier Speculation Amber (`#F77F00`).

---

## 2. Zone-by-Zone Architecture of the Central Macro Mat

### Zone 1: The Rawlsian D20 Reef & Vigintile Compass (`B:00` — Top Horizon Bar)
Spanning the top $95\text{ mm}$ of the mat is a 20-cell horizontal bar (`1` through `20`) representing the 20 wealth vigintiles of Aotearoa New Zealand ($\pi_k = 5.0\%$ each), crowned by the Rule Zero epigraph: *"Not all lives are easy, but none should be impossible."*

| D20 Cells | Visual Styling & Reef State in `SS0` | Birth Roll Effect ($J=0$) | Phase IV Hazard Roll Effect | How Players "Make Their Own Luck" (Reef Cover) |
| :--- | :--- | :--- | :--- | :--- |
| **Cells `1–4`** *(+ `5–6` dashed for `H:06` GUiNZ)* | **Crimson Reef Zone ("The Impossible Corner"):** Marked with Dunedin Study $22\%$ ($1\text{–}4$) and GUiNZ $30\%$ ($1\text{–}6$) boundary brackets. | Newborn receives a **Stunted Trajectory Token** ($-50\%$ earnings, no Age-18 Kaupapa unlock, $+1$ Hull Drag) unless privately bailed out. | Triggers **`T:00` (Cash Leakage)**, **`T:01` (Late Remediation)**, or **`T:05` (Algorithmic Outrage)** against unshielded staked Mana! | Completing **Bay 1 (Front Foil: `B:01` + `B:02` + Amp)** slides the **Pounamu Reef Cover** over Cells `1–6`—permanently abolishing the Impossible Corner! |
| **Cells `7–18`** *(`1–8` marked with Ballot Icon)* | **Teal Clear Channel ("Working & Founding Majority"):** Dashed overlay on Cells `1–8` for **Every-3rd-Turn Election Audits**. | Normal birth launch (`5–12`: 1–2 Wealth/turn; `13–18`: 2–3 Wealth/turn, subject to Age-21 `H:03` Sydney Brain Drain if Bay 2 is open). | Every turn (1 parliamentary term = 3 years), rolling `1–8` triggers **`H:01` (Myopic 3-Year Cash Truncation)** or **`H:02` (Agency Silos)**! | Completing **Bay 3 (Rear T-Foil: `B:07` + `B:06` + Proof)** locks the **Actuarial Shield** over the Ballot Bracket—canceling `H:01` audits forever! |
| **Cells `19–20`** | **Amber-Gold Reef Zone ("The Lavoisier & Land-Bubble Reef"):** Represents the Top-5% patrimonial balance sheet (`20:01`–`20:20`). | Born with **4 Wealth** (+ Dynasty Endowment in `SS0`), but exposed to sovereign debt collapse if `SS2` fails by Turn 20. | When any player holds $>8$ Wealth while $\tau_a = 0$, rolling `19–20` triggers **`T:02` (Housing Capitalization)** or **`T:04` (Lavoisier Trap)**! | Completing **Bay 2 (Wing-Sail: `B:05` + `B:03` + Engine)** slides the **Kauri Reef Cover** over Cells `19–20`—rotating passive dirt into builders! |

---

### Zone 2: The Three Interlocking Subsystem Bays (Upper-Center Structural Deck)
Directly beneath the D20 Reef Bar sit the **Three Subsystem Bays** ($270\text{ mm}$ wide $\times 210\text{ mm}$ tall each), linked horizontally by **Kīato Cross-Beam Connectors** that light up when **`SS1` (Any 2 Bays = $2\times$ Mana Multiplier)** and **`SS2` (All 3 Bays + Capstone = $3\times$ Mana Multiplier)** are achieved.

Each Subsystem Bay is divided into **Three Vertical State Sub-Zones** so players can track Contingent Mana Liability and Emergency Saves at a glance:

1. **Bay Header (Title, Dual-Lens Name, Recipe, & Scaled Political Drag):**
   * Prints the required 3-card synergy recipe and the normalized Political Drag cost by player count: **`[2P: 1.5 Wealth]`** • **`[3–4P: 2.0 Wealth]`** • **`[5–6P: 3.0 Wealth + 3 Co-Stakers (unless K:07)]`**.
2. **Sub-Zone A — Staking & Incubation Slot (Teal Border):**
   * Holds candidate Policy Cards and **upright (`0°`) Committed Mana Tokens ($\Delta M_{\text{stake}}$)**. Co-stakers place $\ge 1$ upright Mana token here during Phase II to back the goal and avoid the Bystander Forfeit.
3. **Sub-Zone B — 1-Turn Emergency / Jeopardy Box (Crimson Dashed Alert Box):**
   * When struck by a Phase IV D20 Reef Roll or a player-driven Feral Spoiler (`T` or `H` card):
     * Place the attacking Trap/Boss card into the left **Trap/Boss Slot**.
     * Tip all staked Mana tokens in this bay **$90^\circ$ sideways ("In Jeopardy!")**.
     * Players have **1 Turn** to play the printed **Empirical Shield / Judo Counter Card** into the right slot (or pay a 4-Wealth emergency bailout). Saving a Feral Spoiler awards **+1 Resilience Mana** to the defenders and inflicts **$-2\text{ Mana}$ (*whakamā*)** on the Feral player; failing to save forfeits all sideways Mana tokens!
4. **Sub-Zone C — Locked Hydrofoil / Kīato Plinth (Pounamu & Gold Border):**
   * Once the recipe and Political Drag are paid, slide the completed Subsystem cards into Sub-Zone C, cover the matching D20 Reef cells in Zone 1, and trigger the **Bystander Forfeit Check** ($-2\text{ Mana}$ on `SS1` / $-3\text{ Mana}$ on `SS2` for any player who staked $0$ Mana).

#### Specific Recipes & Printed Judo Counters for Each Bay
| Bay | Subsystem Title & Dual-Lens Name | Required Recipe | Printed Emergency Judo Counters (Sub-Zone B) | Locked Plinth Reward (Sub-Zone C) |
| :--- | :--- | :--- | :--- | :--- |
| **Bay 1** | **Front Lifting Foil** / *Te Korowai Mokopuna* | `B:01` + `B:02` + **1 Amplifier** (`N:01`, `N:02`, `C:02`, `C:03`) | **`B:01` + `N:02`** (or `K:01`) vs. `T:00`/`T:01`; **`C:02`** or **`K:05`** vs. `T:05` Outrage | Covers D20 Reef `1–6` (No Life Impossible!) + **+5 Legacy Mana Bonus** |
| **Bay 2** | **Wing-Sail Power Plant** / *Te Aka Matua* | `B:05` + `B:03` + **1 Engine** (`E:01`, `E:02`, `C:05`) | **`B:05` + `N:05`** (or `K:02`) vs. `T:02`/`T:04`/`H:05`; **`B:03`** vs. `H:03` Exile | Covers D20 Reef `19–20` + Ends Sydney Brain Drain + **Adults +1 Wealth/Turn** |
| **Bay 3** | **Rear T-Foil Stabilizer** / *Ngā Kete o te Wānanga* | `B:07` + `B:06` + **1 Proof** (`N:03`, `N:04`, `B:04`, `B:08`) | **`B:07` + `N:03`** (or `K:03`/`K:04`) vs. `H:01`; **`N:01`/`N:04`** vs. `H:02` Silos | Cancels Election Audits (`1–8`) + PAYE Cut to $18.5\%$ (**+1W/Turn**) + **Super @ 65 (`K:06`)** |

---

### Zone 3: The Texas Hold'em River & Persistent Infrastructure Commons (Center Strip)
Running across the middle of the mat ($860\text{ mm} \times 135\text{ mm}$) are **8 River Card Slots** (`River 1` to `River 8`, accommodating 2–6 players plus the 2-Player Public Commons slots):
* **Top Exposure Badge:** Prints **`EXPOSE -> +1 GENEROSITY (WEALTH)`**, reminding players to collect 1 liquid Wealth token whenever they place a card face-up into the River during Phase II.
* **Status Banner (Middle):** Cards waiting to be used sit in the upper half of the slot; once linked into an enacted combination (**Variant B Persistent Asset**), slide the card down $15\text{ mm}$ to reveal the gold **`ENACTED INFRASTRUCTURE (NON-RIVAL IDEA — N:05)`** header.
* **Bottom Royalty Tracker:** Prints three checkboxes **`[ Roy 1 ]  [ Roy 2 ]  [ N:05 ]`**. Each time another player links that enacted River card in a combo during a turn, place a marker on a checkbox and pay $\mu \cdot m_i$ Mana to the owner (capped at 2 payouts/turn, or 3 if `N:05` is active; reset markers at the end of Phase IV).

---

### Zone 4: The 20-Turn OLG Clock & "Chasing Finland" Match-Race Track (Bottom Strip)
The bottom $110\text{ mm}$ of the mat houses two parallel horizontal tracks:
1. **Track 4A — The 20-Turn Intergenerational Clock ($\Delta t = 3\text{ Years/Turn}$, `2026` $\to$ `2086`):**
   * 20 sequential boxes (`Turn 1: 2026` through `Turn 20: 2086`).
   * **Turn 9 (`2050`)** is highlighted in Gold as the **2050 50/50 Protocol Target (`B:06`)**.
   * Because each 3-year turn equals one NZ parliamentary term, unshielded multi-turn stakes face the **`H:01` 3-Year Term Audit (`D20 Rolls 1–8`)** until Bay 3 (`B:07`) is locked.
2. **Track 4B — The Economic Sailing Race / Social Cohesion Track (`C:06`, `80.0` $\to$ `126.0`):**
   * A graduated regatta track where the **Aotearoa Catamaran/Waka Marker** races against foreign benchmark vessels:
     * **`81.0`:** Aotearoa `SS0` Start ($\Gamma = 0.5\times$ Hull Drag; $+0.25$ pts/turn in `SS0`).
     * **`83.0` $\to$ `96.0`:** Devolved Scotland Vessel ($+1.5$ pts/turn early, **Hard Constitutional Ceiling at `96.0`** without `B:05`).
     * **`88.0` $\to$ `107.2`:** **Finland Benchmark Vessel** (moves each Phase IV via D20: `1–5` = $-0.5$, `6–15` = $+1.0$, `16–20` = $+2.0$).
     * **`90.0` $\to$ `105.0`:** 1989 Bubble Japan Vessel (surges to `105.0` by Turn 6, then crashes $-3.0$/turn under `T:02`/`T:04`).
     * **`114.8`:** Aotearoa `SS1` Foiling Milestone ($\Gamma = 1.0\times$; $+2.60$ pts/turn).
     * **`126.0`:** **Aotearoa `SS2` Victory Finish Line** ($\Gamma = 1.5\times + 0.05\times/\text{Early Turn}$; $+4.20$ pts/turn; #1 OECD Intergenerational Cohesion).

---

## 3. Zone 5: Individual Cohort Command Mats (Player Boards)

Each player (or cohort team) sits behind an A4-landscape **Cohort Command Mat** featuring:
1. **Two Generational Character Tracks (Character Slot A & Character Slot B):**
   * A 30-box lifecycle age strip ($j = 0 \dots 29$, representing Ages $0\text{–}89$ in 3-year steps):
     * **Boxes `0–5` (Ages `0–17` — *Being / Tamariki*):** Slot for Stunted or Thriving tokens; unlocks Kaupapa at Box `6` (or Box `4` with `B:02`).
     * **Boxes `6–20` (Ages `18–62` — *Becoming / Pakeke*):** Box `7` (Age `21`) prints the **`H:03` Sydney Brain-Drain Check (1d6: 1–2 if Bay 2 open)**; collects full Working Wealth yield.
     * **Boxes `21–29` (Ages `63–89` — *Crossing Over / Kaumātua*):** Unlocks **`K:06` (+1 Free Lifetime Experience Token/turn)**.
     * **Box `30` (Age `90` — *Passing Over & Piketty–Saez Rebirth*):** Triggers immediate $J=0$ rebirth roll on the Zone 1 D20 Reef Bar (and *Tuakana–Teina* `B:02` Kaupapa bequest check).
2. **Command & Treasury Bays:**
   * **Primary Kaupapa Slot (`K:01`–`K:06`)** + **Dual-Class *Kotahitanga* Overlay Slot**.
   * **Available Mana Pool ($\mathcal{M}_i$)** (distinct from Staked Mana currently on the central mat).
   * **Liquid Wealth & Generosity Treasury ($\mathcal{W}_i$)**.
