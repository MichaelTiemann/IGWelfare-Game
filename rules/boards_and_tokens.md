# Tabletop Board, Seven Capitals, & Token Guide — *Foils & Founders: The Aotearoa Deck*

**Schema Reference:** [`decks/board_and_tokens.yaml`](../decks/board_and_tokens.yaml) | **Core Rules:** [`rules/rules.md`](rules.md) | **D20 Sub-Rolls:** [`decks/nat_1.md`](../decks/nat_1.md) & [`decks/nat_20.md`](../decks/nat_20.md)

In *Foils & Founders*, wealth is never reduced to a pile of monopoly cash, and public policy is never reduced to a single 3-year cash-flow budget. To make overlapping-generations economics tactile at the gaming table, players track **five double-sided token types** across **two printable A3 Landscape Playmats** (generated via `scripts/render_boards.py`):

1. **A3 Mat 1 — The National Hydrofoil & *Te Waka Hourua* Board:** Tracks the **5 Lifecycle Gates**, the **4 Fiscal/Demographic Exits**, the **Seven Forms of Capital**, and the **National Obligations Ledger**.
2. **A3 Mat 2 — The Player *Whānau & Wayfinder* Ledgers + Cut-Out Token Sheet:** Gives players personal mats to track their **`B:00` Rawlsian D20 Birth Roll**, the ***Tamariki* and *Rangatahi* in their care**, their **Obligations (*To Whom & How Much*)**, their ***Mana* Balance (*Mana Created vs. Mana Eroded*)**, and the end-of-round ***Passing Over* Inheritance Ritual**.

---

## 1. The Five Double-Sided Token Types (`SS0` Liability $\leftrightarrow$ `SS2` Endowment)

Because the core insight of the monograph is **structural conversion**—turning reactive crisis drag into human capability, dormant land hoarding into active enterprise, and fossil-fuel volatility into a solar endowment—every token in the game is **double-sided**:

| Token ID & Name | Side A: `SS0` Displacement / Liability State | Side B: `SS1 -> SS2` Foil-Borne / Endowment State | How It Flips in Play |
| :--- | :--- | :--- | :--- |
| **`TOK:01` Cohort Meeples** *(Tamariki $\rightarrow$ Rangatahi $\rightarrow$ Kaumātua)* | 🔴 **Stunted / Hardship Corner (`i_c = 0`):** Placed on `d20` rolls `1–4` (22% Dunedin share) if unbuffered. Causes `NZD 105k–180k/yr` drag in `Exits 1, 2, 4`. | 🟢 **Thriving Launch & Readiness (`h6–h7`):** Generates `+NZD 16.1k/yr` net adult fiscal surplus and `65.0%` thriving launch rate. | Flip from 🔴 to 🟢 by playing **`B:01`** (*Te Korowai Mokopuna* wraparound) at Gate 1 and **`B:02` / `C:03`** (*Tuakana–Teina* mentoring) at Gate 2. |
| **`TOK:02` Capital & Energy Discs** *(`z_l / a_prec` $\leftrightarrow$ `z_h / pv=5`)* | 🪨 **Dormant Dirt & Precautionary Hoard (`z_l` / `a_prec`):** Locked in the `NZD 1.6T` untaxed property pool or sterile cash buffers against `z2` energy shocks. | ⚡ **Active Builder & Solar Endowment (`z_h` / `pv=5`):** Funds operating firms, `B:03` Youth Capital Grants, and `1.65x` Resilient Grids (`C:04`). | Flip from 🪨 to ⚡ by playing **`B:05`** (Use-It-Or-Lose-It Rebalancer) or **`E:02`** (Energy as Endowment, releasing `NZD 60.8B–91.5B`). |
| **`TOK:03` Obligation & Ledger Cubes** *(To Whom & How Much)* | 🩸 **Unfunded Liability & Hull Drag Cube:** Owed to *Mokopuna* (`200%` Crown debt path), Banks (`+60 bps`), Foreign Oil (`NZD 20B/yr`), and Reactive Care (`Exits 1, 2, 4`). | 🛡️ **Actuarial Asset & 50/50 Sinking Cube:** Books `3.84x` Year-5 return (`NZD 35.25B`) and locks surpluses 50/50 into Debt Sinking & Grid Armor. | Flip from 🩸 to 🛡️ by playing **`B:07`** (ACC Actuarial Time-Bend) + **`N:03`** in `SS1`, and **`B:06`** (The 2050 50/50 Stabilizer) in `SS2`. |
| **`TOK:04` *Mana*, *Ako*, & Cohesion Stars** *(Social & Care Capital)* | 🌪️ ***Mana* Eroded / Outrage Drag (`T:05`):** Spawned when cohorts are left stunted or exiled (`H:03`). Depresses trust to `40%` and adds `+25%` justice drag. | ✨ ***Mana* Created / *Whanaungatanga* Star:** Tracks `+NZD 15.3k` crowded-in parental care, reciprocal *Ako*, and high institutional trust (`126.0`). | Flip from 🌪️ to ✨ via **`B:01`** + **`B:02`** + **`C:02`** (Finnish *Monilukutaito* inoculation) + **`K:07`** (*Kotahitanga* alliance). |
| **`TOK:05` *Ngā Kete o te Wānanga*** *(Knowledge & Legacy Baskets)* | 📦 **Exiled / Siloed IP (`Exit 3`):** Brain-drained to Australia (`19.3%–23.4%` metro loss under `H:03`) or lost when elders are trapped in survival mode (`H:04`). | 🧺 **Open-Source Wisdom & Tech Token (`K:06` + `N:05`):** Non-rival collective intelligence that multiplies the next generation's starting skill by **`1.75x`**! | Generated every turn at Gate 5 by dignified ***Kaumātua* (`K:06`)** with Universal NZ Super at 65 (`B:06`) and retained Founders (`B:03`). |

---

## 2. Tracking the Seven Forms of Capital & The Obligations Matrix

Across the top and bottom of **A3 Mat 1**, players move markers along **Seven Capital Tracks** and audit their **Four Core Obligations**:

### A. The Seven Capital Tracks (`CAP:01` – `CAP:07`)

1. **Financial & Actuarial Capital (`CAP:01`):** Tracks the Crown and household balance sheet from `-NZD 17.7B/yr` reactive hull drag and the `200%` debt spiral in `SS0`, through the **Year 5 ACC Actuarial Breakeven (`1.16x` direct cost avoidance / `3.84x` total return via `B:07`)** in `SS1`, to **`<40%` Crown debt, `-60 to -100 bps` lower interest rates, and an `18.5%` PAYE tax rate (`-3.5 pp` cut via `B:06`)** in `SS2`.
2. **Built Environment & Grid Infrastructure (`CAP:02`):** Tracks urban housing overvaluation (`3.10x` metro rent stress cooled by `-7.5% to -10.5%` via `B:05`), the cancellation of the `NZD 6.2B` imported LNG terminal (`E:01`), the **1.65x Ring-Fenced Infrastructure Pool (`C:04`)**, and the **5-Sector Solar + Battery Grid (`E:02`–`E:03`, saving `+NZD 15.55B/yr`)**.
3. **Domestic & *Whānau* Care Capital (`CAP:03`):** Tracks the household's internal care economy. In `SS0`, rent and energy costs push low-income families into the Stone–Geary subsistence corner (`i_c = 0`) and crush working-age leisure (`leisure_h`). Playing `B:01` (`NZD 13.0k/yr` in-kind wraparound) + `E:02` (Household Solar) automatically **crowds in `+NZD 15.3k/yr` of private parental care (`NZD 8.7k` cash + `NZD 6.5k` parental time)** and expands working-age leisure!
4. **Natural & Ecological Capital (`CAP:04`):** Driven by the **`🌱 CO2e Impact` badges** in the corner of every card. Tracks Aotearoa's shift from unbuffered exposure to the `+1°C` Bilal–Känzig shock (`USD 1,200/tCO2e`, `C:01`) to **`-14.8 MtCO2e/yr` in 5-sector emissions cuts (`E:02`)**, cyclone-proof school/marae microgrids (`C:03`), and floating solar across 19,000+ farm ponds.
5. **Social & Epistemic Capital (`CAP:05`):** Tracks the **Social Cohesion Index (`100.0 -> 114.8 -> 126.0`, `C:06`)**. Leaving children stunted at Gate 1 or unmentored at Gate 2 spawns `T:05` Outrage Drag tokens (dropping government trust to `40%`). Pairing `B:01` + `B:02` + `C:02` (*Monilukutaito* critical thinking) neutralizes `T:05` and lifts Aotearoa to **#1 in the world on institutional trust (`126.0`)**.
6. **Cultural & *Pūrākau* Capital (`CAP:06`):** Tracks the lashing together of Story Lens A (*Up on Foils*) and Story Lens B (*Te Waka Hourua*) via **`K:07` (*Kotahitanga & Te Tiriti Partnership*)** and **`K:05` (*The Cultural Weaver*)**, unlocking the domestic creative IP renaissance (`B:03`).
7. **Technology & Collective Intelligence Capital (`CAP:07`):** Tracks the occupational talent split (`z_l` vs. `z_h`). In `SS0`, the Lavoisier Trap (`T:04`) siphons top graduates into property speculation (`z_l`). Playing `B:05` + `B:03` + `N:05` flips the cutoff back to active builders (`z_h`), expands the thriving launch cohort to **`65.0%`**, lifts real wages by **`+3.2% to +9.6%`**, and activates the **`1.75x` Romer Generational Multiplier**.

### B. The Obligations Matrix (*To Whom & How Much*)

Every turn, players check the four rows of the **Obligations Ledger** on their mat to see whether they are in breach (`SS0`) or fulfillment (`SS2`):

* **To *Tamariki* & *Mokopuna* (Future Generations):** Owed a thriving start (`1.5%` stunting vs. `22.0%`), a debt-free sovereign balance sheet (`<40%` vs. `200%`), and an [`NZD 62,000+` Youth Capital Seed (`B:03`)](../decks/nat_1.md).
* **To *Kaumātua* & *Kuia* (Elders Aged 65+):** Owed **Universal NZ Superannuation kept solvent at Age 65 (`B:06`)** (defeating the `H:04` age-70 austerity trap) and the dignity to pass down *Ngā Kete o te Wānanga* (`K:06`) to grandchildren living in Aotearoa.
* **To Working *Whānau* & Regions (`Rural`, `Small`, `Large`, `Auckland`):** Owed `-7.5% to -10.5%` cooler urban rents (`B:05`), relief from the `2.7x–2.8x` rural transport fuel penalty (`C:05` + `E:02`), and a **`-3.5 pp` PAYE income tax cut (`22.0% -> 18.5%`)**.
* **To Active Builders (`z_h`) & Sovereign Bondholders:** Owed cheaper expansion credit (`-60 to -100 bps`), a deeper skilled workforce (`+38%`), and a tax system where **[19 out of 20 Top-5% entrepreneurial slices (`20:01`–`20:19`, up to `NZD 100M` net worth) win outright](../decks/nat_20.md)**.

---

## 3. The End-of-Round Ritual: *"Passing Over & Taking On the Inheritance"* (*Ka Pū te Ruha, Ka Hao te Rangatahi*)

At the end of Round 1 (`SS0 -> SS1`) and Round 2 (`SS1 -> SS2`), the table performs a 60-second generational transition representing a 25-year wave:

1. **Step 1 — Launch the *Rangatahi* (Gates 1 & 2 $\rightarrow$ Gate 3 & Mid-Career):**
   * Advance all **Gate 1 (`0–5`)** and **Gate 2 (`12–14`)** Cohort Meeples into **Gate 3 (`20–35`)** and **Gate 4 (`36–64`)**.
   * Any 🔴 **Red (Stunted)** Meeples that were not rescued by `B:01` + `B:02` fall into the **`Exits 1, 2, 4` Drain Box**, inflicting `NZD 105k–180k/yr` in fiscal drag and spawning a 🌪️ ***Mana* Eroded (`T:05`)** token.
   * All 🟢 **Green (Thriving)** Meeples that receive a ⚡ **Gold Capital Seed (`B:03`, `NZD 62k`)** stay in Aotearoa (immune to `Exit 3` brain drain) and generate **`+NZD 16.1k/yr` net fiscal surplus** plus **+1 ✨ *Mana* Created Star**.
2. **Step 2 — The *Kaumātua* Cross the Horizon (Gate 5 $\rightarrow$ *Hawaiki Anamata*):**
   * Cohort Meeples in **Gate 5 (Ages 65–100)** complete their lifecycle and pass over, triggering the **Intergenerational Bequest Split** across the `NZD 1.6 Trillion` estate wave:
     * **Without `B:05` & `E:02` (`SS0`):** Departing wealth stays locked in 🪨 **Grey Dormant Dirt Discs** (`z_l`), inflating rents for the next generation, while precautionary cash buffers die as sterile accidental bequests.
     * **With `B:05`, `B:06`, `K:06`, & `E:02` (`SS1 -> SS2`):**
       1. **Financial Seed Recycle (`B:05` $\rightarrow$ `B:03`):** The `25% -> 18%` estate levy recycles a slice of the `NZD 1.6T` transfer into ⚡ **Gold `NZD 62k+` Youth Capital Seeds** for every incoming Gate 3 young adult—while departing families still keep **89.4% to 98.5% of their fortune**!
       2. **Physical Solar & Grid Bequest (`E:02` + `C:04`):** Paid-off **Rooftop Solar + Battery Endowments (`pv = 5`)** and **1.65x Armored Grids (`C:04`)** remain permanently on the board, immunizing the new generation against `z2` energy shocks.
       3. **The Three Baskets of Wisdom (`K:06` + `N:05`):** Every 🧺 ***Kete o te Wānanga* Token** generated by the departing *Kaumātua* is placed onto the incoming Gate 1 & Gate 2 cohorts—multiplying their starting human capital by **1.75x**!
3. **Step 3 — Become Your Own Descendants:**
   * Players now step into the shoes of the rising cohort they just nurtured: **you inherit the exact housing affordability, grid resilience, sovereign debt load, and social trust (`126.0`) that your previous generation left behind.**
   * 
