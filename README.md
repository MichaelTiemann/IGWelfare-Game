# **Foils & Founders: The Aotearoa Deck**

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)]([https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/))
[![Engine: VFI Toolkit GPU](https://img.shields.io/badge/Engine-VFI_Toolkit_GPU-blue.svg)](https://github.com/MichaelTiemann/IGWelfare)

An open-source cooperative/competitive tabletop strategy game and macroeconomic simulation companion to ***Intergenerational Welfare, Capital Allocation, and Human Potential in New Zealand*** by Michael Tiemann ([Documents 1A–1D, 2A, 2B, 2T, and 3](https://github.com/MichaelTiemann/IGWelfare)).

## 0. We Make Affordable Economics Understandable

In 1989, [Cygnus Support](CREDITS.md) launched the commercial open-source revolution with a five-word double-entendre: ***"We make Free Software affordable"*** ([`N:02`](rules/rules.md)).

Today, Aotearoa New Zealand faces the exact inverse problem. Orthodox politicians and legacy cash-flow models tell the public that eliminating child poverty ([`B:01`](rules/rules.md)), protecting Universal Superannuation at 65 and lowering it to Age 64 ([`B:15`](rules/rules.md)), and electrifying every home, farm, and school ([`E:01`–`E:02`](rules/rules.md)) are *"unaffordable."* In reality, they are the most **affordable** investments a nation can make—returning **3.84x** on the Crown's actuarial balance sheet by Year 5 ([`B:09`](rules/rules.md)) and unlocking **NZD 60.8B–91.5B** in idle precautionary capital ([`E:02`](rules/rules.md)).

Why doesn't the public know that? Because the proof is locked inside 5-dimensional overlapping-generations Bellman equations and Kolmogorov Forward stationary distributions in [**Document 1B** and **Document 2** of the `IGWelfare` repository](https://github.com/MichaelTiemann/IGWelfare).

***Foils & Founders* [makes affordable economics understandable](CREDITS.md#we-make-affordable-economics-understandable).** Look at the [two hardest equations in our GPU solver](CREDITS.md#equation-1-multi-stage-ces-human-capability-formation-under-non-homothetic-subsistence-corners)—and see how the deck compiles them into two **Two-Card Tabletop Synergies** you can play in thirty seconds:
* **[Equation 1 (Bellman & CES Skill Technology)](CREDITS.md#equation-1-multi-stage-ces-human-capability-formation-under-non-homothetic-subsistence-corners) $\rightarrow$ Play [`B:01` (*First 2000 Days*)](rules/rules.md) + [`B:03` (*Tuakana–Teina*)](rules/rules.md) + [`N:03` (*Heckman's Dynamic Complementarity*)](rules/rules.md)**
* **[Equation 2 (Stationary Distribution & Precautionary Release)](CREDITS.md#equation-2-the-guvenenmsvqea-stationary-distribution--precautionary-capital-release) $\rightarrow$ Play [`B:08` (*Use-It-Or-Lose-It LVT & Corp Lockstep*)](rules/rules.md) + [`E:02` (*Energy as Endowment*)](rules/rules.md)**

* **Want to "Play the Nerd Card" at the Table?** Print the **Fold-Over Study Deck** ([`decks/study_cards.yaml`](decks/study_cards.yaml) + [`scripts/render_study_cards.py`](scripts/render_study_cards.py)). Each card folds along its horizontal crease so the front plays as a standard portrait game card while the back flips open in widescreen landscape (`138mm × 79mm`) with the full MathJax equation, GPU calibration parameters, one-sentence proof bridge, and peer-reviewed academic citations!

---

## 1. Why a Card Game? (Rule Zero: The Rawlsian D20 Test)

> *"Not all lives are easy, but none should be impossible."*

Pick up a 20-sided die (`1` to `20`, representing the 20 wealth vigintiles of Aotearoa New Zealand). Imagine you are behind John Rawls's **Veil of Ignorance** (`B:00`), rolling to see which family balance sheet you are born into:

* **In the Orthodox Status Quo (`SS0` — Displacement Mode):**
  * Roll `1–4` (the 22% Dunedin Study early hardship corner) and you face the unbuffered early hardship corner (`h1–h2`), driving 57%–81% of adult hospital nights, state care (`NZD 180k/yr`), and prisons.
  * Roll `5–18` and you face `3.10x` metropolitan housing stress, delayed family formation (`1.66 TFR`), PAYE taxes climbing toward `28.22%`, and emigrating children.
  * Roll `19–20` (even a `Nat 20`) and the macro board *still* collapses around you: net Crown debt spirals toward `200% of GDP`, core infrastructure fails, and your grandchildren move to Sydney. **There is no number you can roll that wins the game.**
* **In the IGWelfare Scenario (`SS0 -> SS1 -> SS2` — Up on Foils / *Te Waka Hourua*):**
  * **All 20 median wealth groups (`1` to `20`) are better off** (`+24.70% CE` pre-NDC national welfare gain [`+25.19%` on the 13-wave *Te Kāhui Waka* ledger], active `z_h` entrepreneurs ahead through `NZD 50M` net worth and breakeven at `NZD 140M`, Universal NZ Super lowered to **Age 64**, Crown Debt sunk to `21%–22%` of GDP, and working-age PAYE taxes cut by `-3.75 percentage points` down to **`18.25%`**). **Roll any number. You win.**

---

## 2. Two Cultural Groundings: One Vessel, Two Hulls (*Te Waka Hourua*)

Like *Te Waka Hourua*—the double-hulled voyaging vessel where two hulls are lashed together by *kīato* (cross-beams)—every mechanic on the board can be played through **two one-to-one isomorphic narratives** (see [**`STORIES.md`**](STORIES.md) for the full lore and [**Side-by-Side Translation Key**](STORIES.md#side-by-side-translation-key-one-game-two-groundings)):

1. [**Story Lens A — *Up on Foils* (Pākehā / Systems Engineering):**](STORIES.md#story-lens-a-up-on-foils--how-emirates-team-new-zealand-bent-the-rulebook) How Emirates Team New Zealand bent the straight-keel orthodoxy in 2013 by coupling a **Front Lifting Foil (`B:01` + `B:03`)**, a **Wing-Sail Power Plant (`B:08` + `B:05`/`B:06` + `C:09` + `E:01`/`E:02`)**, and a **Rear T-Foil Rudder Stabilizer (`B:14` + `B:15` + `B:09`)** to lift the catamaran out of the water and slash hydrodynamic drag by 75%.
2. [**Story Lens B — *Te Waka o Whānau* (Te Ao Māori & Moana Pasifika *Pūrākau*):**](STORIES.md#story-lens-b-te-waka-o-whānau--being-becoming--crossing-over-māori--pasifika-pūrākau) The three-stage intergenerational crossing from **Being** (*He Kākano i Ruia mai i Rangiātea*, wrapping the sacred seed in *Te Korowai Mokopuna* and *Whānau Ora*, `B:01`), through **Becoming** (ascending *Te Aka Matua* together via reciprocal *Tuakana–Teina* and *Ako*, `B:03`, `C:04`, and restoring *Tūrangawaewae* at home, `B:05`/`B:06`, `B:08`), to **Crossing Over** (honoring our *kaumātua* navigators as they pass down *Ngā Kete o te Wānanga*, `K:09`, `B:15`).

---

## 3. Progressive Onboarding: The 8 Modular Suites (`80-Card X:NN` Taxonomy)

Every card in [`decks/cards.yaml`](decks/cards.yaml) uses a permanent **`X:NN`** identifier (`80` unique cards filling `8` A3 10-up game sheets and `16` A3 5-up fold-over study sheets at `100%` utilization):

| Prefix | Suite Name | Cards | Count | Onboarding Track & Strategic Focus |
| :---: | :--- | :---: | :---: | :--- |
| **`B`** | **Base Policy & Lifecycle** | `B:00` – `B:16` | `17` | **Track 1:** Rawlsian D20, First 2000 Days, Māra Kai, *Tuakana–Teina*, Vanguard/Universal Grants, Dual-Speed Tax, ACC Time-Bend, 4x4 Matrix, & Two-Key `SS2` Launch. |
| **`T`** | **Cautionary Traps** | `T:00` – `T:10` | `11` | **Track 1:** Molesworth St Limo Panic, Disinformation, Hyperbolic Shortcut, 'Solve Debt First' Boomerang, Single-Shot Surge, Stop-Go Scissor-Blade, Scotland, Seoul, & Tokyo. |
| **`C`** | **Resilience, Spatial & Food-Hubs** | `C:01` – `C:10` | `10` | **Track 2:** Macro Shocks, `126.0` Social Credit, `1.65x` Lifeline Armor, Marae/School Microgrids, *Monilukutaito*, 4-Region Tax Keys (`C:06`), & Rural/Small Food-Hub `-0.64 pp` PAYE Graduation (`C:07–C:10`). |
| **`K`** | **Wayfinders & *Whānau* Personas** | `K:01` – `K:10` | `10` | **Track 3:** Coalitions `1–4` (`K:01, K:04, K:05, K:07`), Storyteller (`K:02`), Māra Kai (`K:03`), Tax/Cartel Mediator (`K:06`), VFI Architect (`K:08`), `K_whanau` Elder (`K:09`), & *Te Tiriti* Big Table (`K:10`). |
| **`N`** | **Nobel & Staffing-Cycle Engines** | `N:01` – `N:09` | `9` | **Track 3:** Arrow Learning-by-Doing (`N:01`), Coase (`N:02`), Heckman (`N:03`), Williamson (`N:04`), Ostrom (`N:05`), Romer (`N:06`), Deming–Fixsen (`N:07`), Doepke–Kindermann (`N:08`), & 203X Medallion (`N:09`). |
| **`H`** | **Orthodoxy Boss Deck** | `H:01` – `H:10` | `10` | **Track 3/4:** Cash-Flow Myopia, Silos, GUiNZ Drift, Brain-Drain Vortex, Super-to-70, *Kaiako* Rent Squeeze, Landlord Capture, Cartels, `3.0%` GDP Defense Shock (`H:09`), & Grant Waste (`H:10`). |
| **`E`** | **Energy & Proof Operators** | `E:01` – `E:05` | `5` | **Track 2/4:** Provincial-First Electrification (`E:01`), `QEA-2026` Precautionary Release (`E:02`), `-100 bps` Firmed Grid (`E:03`), *Thick vs. Thin* Lens (`E:04`), & `20.5-Yr` Wave Echo (`E:05`). |
| **`P`** | **Open-Source Wildcards** | `P:01` – `P:08` | `8` | **Track 5:** Custom Flight Plans (`P:01`), *Rohe* Kaupapa (`P:02`), Classroom PRs (`P:03–P:04`), Climate Extension Socket (`P:05`), Live Shocks (`P:06`), Rival Yachts (`P:07`), & Maintainer Fork (`P:08`). |

---

## 4. Quick-Start: Rendering & Printing the Deck, Playmats, & Fold-Over Study Cards

The repository includes three Python compilers sharing [`scripts/render_common.py`](scripts/render_common.py):
* **[`scripts/render_cards.py`](scripts/render_cards.py):** Merges [`decks/cards.yaml`](decks/cards.yaml) with any theme in `themes/<theme>/theme.yaml` to output **8 A3 Landscape sheets** (`5×2` stacked-bond grid = 10 cards per sheet: all 80 unique `X:NN` cards at 100% sheet fill).
* **[`scripts/render_boards.py`](scripts/render_boards.py):** Compiles [`decks/boards_and_tokens.yaml`](decks/boards_and_tokens.yaml) into **2 A3 Landscape sheets** (Sheet 1: National Region 5-Gate River, 4 Exits, 4 Obligations, & 7 Capitals Dashboard; Sheet 2: Two *Whānau & Wayfinder* Player Mats + 5 Double-Sided Cut-Out Token Strips).
* **[`scripts/render_study_cards.py`](scripts/render_study_cards.py) (*"Play the Nerd Card" Mode*):** Merges [`decks/cards.yaml`](decks/cards.yaml) and [`decks/study_cards.yaml`](decks/study_cards.yaml) into **16 A3 Landscape sheets** (5 fold-over cards per sheet: all 80 canonical cards filling all 16 sheets at 100% utilization), with the standard portrait game card on the bottom row and a rotated `138mm × 79mm` landscape MathJax equation & citation blackboard on the top row.

### Step 1: Install Dependencies
```bash
python3 -m pip install pyyaml markdown
```

### Step 2: Render A3 HTML Previews for Cards, Playmats, & Fold-Over Study Cards by Theme
Run the compilers from the root of the repository:

```bash
: "1. Generic Typographic Theme (Cards + A3 Playmats + Fold-Over Study Cards)"
python3 scripts/render_cards.py --theme generic --co2-pos top-right --out build/generic.html
python3 scripts/render_boards.py --theme generic --out build/boards_generic.html
python3 scripts/render_study_cards.py --theme generic --co2-pos top-right --out build/study_generic.html

: "2. Te Waka Hourua Theme — Māori & Pasifika Pūrākau (CO2e badge in bottom-right corner)"
python3 scripts/render_cards.py --theme waka_hourua --co2-pos bottom-right --out build/waka_preview.html
python3 scripts/render_boards.py --theme waka_hourua --out build/boards_waka.html
python3 scripts/render_study_cards.py --theme waka_hourua --co2-pos bottom-right --out build/study_waka.html

: "3. Up on Foils Theme — America's Cup Systems Engineering"
python3 scripts/render_cards.py --theme foils_pakeha --co2-pos top-right --out build/foils_preview.html
python3 scripts/render_boards.py --theme foils_pakeha --out build/boards_foils.html
python3 scripts/render_study_cards.py --theme foils_pakeha --co2-pos top-right --out build/study_foils.html
```

### Step 3: Print to A3 Landscape Paper (or Export to PDF)
1. Open any rendered `.html` file in `build/` (`build/generic.html`, `build/boards_waka.html`, `build/study_foils.html`, etc.) in **Chrome**, **Edge**, **Firefox**, or **Safari**.
2. Press **`Cmd + P`** (macOS) or **`Ctrl + P`** (Windows/Linux).
3. Set **Paper Size** to **`A3`**, **Orientation** to **`Landscape`**, **Margins** to **`None`**, **Scale** to **`100%`**, and check **`Background graphics`**.
4. **Cutting & Folding:**
   * **Standard Cards (`render_cards.py`):** Slice along the dashed `0.25mm` stacked-bond gridlines (`5 columns × 2 rows = 10 cards/sheet`).
   * **Fold-Over Study Cards (`render_study_cards.py`):** Slice into **5 vertical strips** (`79mm × 276mm` each) and fold each strip in half along the solid center horizontal crease (`138mm` mark) so the rotated Landscape equation back sits directly behind the Portrait game card front!
   * **Tokens (`render_boards.py` Sheet 2):** Cut around the dashed token pairs and fold in half (`SS0` liability on Side A $\leftrightarrow$ `SS2` endowment on Side B).

---

## 5. Repository Layout, Contributing, & Licensing

* **Narrative & Lore ([`STORIES.md`](STORIES.md)):** The full dual-lens grounding (*Up on Foils* and *Te Waka o Whānau*) plus the side-by-side translation table.
* **Master Card, Study Card, & Board Databases (`decks/`):** All 80 canonical cards live in [`decks/cards.yaml`](decks/cards.yaml), all 80 fold-over LaTeX equations, calibrations, proof bridges, and citations live in [`decks/study_cards.yaml`](decks/study_cards.yaml), all 5 double-sided tokens, 5 lifecycle gates, 4 exits, and 7 capital tracks live in [`decks/boards_and_tokens.yaml`](decks/boards_and_tokens.yaml), and the 20 sub-roll slices for Nat 1 and Nat 20 live in [`decks/nat_1.md`](decks/nat_1.md) and [`decks/nat_20.md`](decks/nat_20.md). Cascading visual themes live in `themes/generic/`, `themes/foils_pakeha/`, and `themes/waka_hourua/`.
* **Core Rules & Card Design Tutorials (`rules/`):** Complete multi-track rules ([`rules/rules.md`](rules/rules.md)), Coopetitive Gameplay Mechanics ([`rules/foils_and_founders_gameplay.md`](rules/foils_and_founders_gameplay.md)), the Strategy & Econometric Study Guide ([`rules/strategy_study_guide.md`](rules/strategy_study_guide.md)), the Tabletop Playmat Guide ([`rules/boards_and_tokens.md`](rules/boards_and_tokens.md)), the `QEA-2026` Game-Changer Tutorial ([`rules/game_changer_tutorial.md`](rules/game_changer_tutorial.md)), and the Finland vs. NZ Disinformation Tutorial ([`rules/T_05_tutorial.md`](rules/T_05_tutorial.md)).
* **Demographic & Macroeconomic Data (`data/`):** Auditable CSV tables for the Rawlsian `d20` Veil of Ignorance ([`data/d20_veil_of_ignorance.csv`](data/d20_veil_of_ignorance.csv)), the 5-Sector Electrification Scorecard ([`data/electrification_5sector.csv`](data/electrification_5sector.csv)), and the 10-Tier `Earn + Own` Incidence Audit ([`data/earn_plus_own_10tiers.csv`](data/earn_plus_own_10tiers.csv)).
* **Schemas & Empirical Source Registry (`metadata/`):** Formal schemas for game cards ([`metadata/card_schema.yaml`](metadata/card_schema.yaml)), fold-over study cards ([`metadata/study_card_schema.yaml`](metadata/study_card_schema.yaml)), card PR templates ([`metadata/card_template.yaml`](metadata/card_template.yaml)), CO2e badges ([`metadata/co2e_impact.yaml`](metadata/co2e_impact.yaml)), themes ([`metadata/themes_registry.yaml`](metadata/themes_registry.yaml)), and the master bibliography ([`metadata/empirical_sources.yaml`](metadata/empirical_sources.yaml)).
* **Submitting Pull Requests:** See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on **Track 1 ("Easy Mode" First-Order Cards)**, **Track 2 ("Challenge Mode" VFI Toolkit Stationary Distribution Shifts + Study Card Equations)**, **Track 3 (10-Tier / 20-Vigintile Data Customization)**, and **Track 4 (Visual Themes & Card Artwork)**.
* **Lineage, Credits, & Equations-to-Cards Rosetta Stone:** See [`CREDITS.md`](CREDITS.md).
* **License:** Game rules, cards, study cards, playmats, and documentation are licensed under **Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`)**. Simulation and rendering scripts are licensed under **`GPL-3.0-or-later` / `MIT`**.

Donations to [Barnardos Aotearoa](https://investinchildren.nz/donate) (who inspired, but in no way funded, any of this game development) are very welcome.  Ngā mihi nui!
