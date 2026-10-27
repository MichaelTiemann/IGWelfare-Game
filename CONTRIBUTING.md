# Contributing to *Foils & Founders: The Aotearoa Deck*

**License:** Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`) for all game rules, cards, artwork themes, and data tables; `GPL-3.0-or-later` / `MIT` for VFI Toolkit MATLAB/GPU simulation and Python rendering scripts.

> ### 🌟 Essential Reading Before You Design a Card: [The "Game Changer" Tutorial (`rules/game_changer_tutorial.md`)](rules/game_changer_tutorial.md)
> Every card in *Foils & Founders* is a rigorous, multi-perspective policy and systems-engineering argument. Before submitting a Pull Request, read [**Module 5: The "Game Changer" Tutorial**](rules/game_changer_tutorial.md) to see a complete, worked walkthrough of how a player proposal ("Electrify Aotearoa!") gets cross-examined by the Personas at the Big Table (`K:01`, `K:02`, `K:03`, `K:04`)—first producing the **Track 1 Easy Mode Card (`E:01`)** via the 4-option Intensity Dial, and then unlocking the **Track 2 Challenge Mode Cards (`E:02` & `E:03`)** via an open-source, 500-line [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) GPU stationary-distribution proof and the 5-Sector National Scorecard.  This is a serious game!

---

## Repository Architecture

```text
IGWelfare-Game/
├── README.md                          # Game overview, Dual-Lens Lore, and A3 Quick-Start Guide
├── STORIES.md                         # Dual cultural groundings: Up on Foils & Te Waka Hourua
├── CONTRIBUTING.md                    # Pull Request guidelines for cards, mechanics, & data
├── CREDITS.md                         # Game Legend & "We Make Affordable Economics Understandable"
├── rules/
│   ├── rules.md                       # Complete card rules, 3-Turn Demo, & P:DD modules
│   ├── boards_and_tokens.md           # Tabletop Playmats, Seven Capitals, Obligations, & Tokens guide
│   ├── game_changer_tutorial.md       # Full worked case study: Easy Mode (E:01) vs. Challenge Mode (E:02-E:03)
│   └── T_05_tutorial.md               # Worked case study: Finland vs. NZ Disinformation Drag (T:05)
├── decks/
│   ├── cards.yaml                     # Canonical master database of all 43 P:DD cards (+ 7 P:?? wildcards)
│   ├── study_cards.yaml               # Fold-over Landscape backs: LaTeX equations, parameters, & citations
│   ├── boards_and_tokens.yaml         # Canonical schema for A3 playmats, 7 capitals, & 5 double-sided tokens
│   ├── nat_1.md                       # Confirming the Fumble: 20 sub-roll slices of the Bottom 5% (01:01-01:20)
│   └── nat_20.md                      # Confirming the Crit: 20 sub-roll slices of the Top 5% (20:01-20:20)
├── metadata/
│   ├── card_schema.yaml               # JSON Schema validating decks/cards.yaml
│   ├── study_card_schema.yaml         # JSON Schema validating decks/study_cards.yaml
│   ├── card_template.yaml             # Blank copy-paste YAML template for new card PRs
│   ├── co2e_impact.yaml               # Schema & methodology for card CO2e badges
│   ├── empirical_sources.yaml         # Master bibliography of empirical & theoretical anchors
│   └── themes_registry.yaml           # Registry of available visual themes & fallback chains
├── themes/
│   ├── generic/                       # Root fallback theme (Markdown-driven typography)
│   │   ├── theme.yaml                 # Base CSS variables, fonts, & deck color borders
│   │   └── cards/                     # Optional per-card Markdown overrides (B_01.md)
│   ├── foils_pakeha/                  # America's Cup Hydrofoil & Systems Engineering theme
│   │   ├── theme.yaml                 # fallback_chain: ["generic"]
│   │   └── assets/                    # Optional per-card illustrations (B_04.png, E_02.svg)
│   └── waka_hourua/                   # Te Ao Māori & Pasifika Pūrākau theme (Kaitiaki-vetted)
│       ├── theme.yaml                 # fallback_chain: ["foils_pakeha", "generic"]
│       └── assets/                    # Optional per-card illustrations (B_01.png, B_02.png)
├── data/
│   ├── d20_veil_of_ignorance.csv      # B:00 Rawlsian D20 (All 20 faces + Nat 1 & Nat 20 sub-rolls)
│   ├── electrification_5sector.csv    # E:01-E:03 5-Sector CapEx & Precautionary Release
│   └── earn_plus_own_10tiers.csv      # B:05 Guvenen Use-It-Or-Lose-It 10-Tier Audit
└── scripts/
    ├── render_common.py               # Shared YAML/theme loader, copyright constants, & base A3 CSS
    ├── render_cards.py                # Compiles cards.yaml + theme into 5x2 Stacked-Bond A3 HTML/PDF sheets
    └── render_boards.py               # Compiles boards_and_tokens.yaml + theme into 2 A3 Playmat & Token sheets
```

---

## Four Tracks for Submitting a Pull Request

Because *Foils & Founders* is designed as an open-source policy and pedagogical engine, contributors can modify or extend the game across **four tracks** (and can sketch new cards right at the gaming table using the 7 write-in `P:??` wildcard slots printed on the A3 sheets):

### Track 1: "Easy Mode" Pull Request (First-Order Card or Rule Tweak)
*(See [**Tutorial Part 1 in `rules/game_changer_tutorial.md`**](rules/game_changer_tutorial.md#tutorial-part-1-easy-mode-negotiating-the-energy-transition-card--the-crowd-out-debate) for the complete worked example of how `E:01` is negotiated at the table.)*

Use Track 1 if you are proposing a new **Cohort (`B:XX`)**, **Cautionary Trap (`T:XX`)**, **Climate Resilience (`C:XX`)**, **Kaupapa Persona (`K:XX`)**, or **Orthodoxy Hazard (`H:XX`)** card that operates within the existing stationary distribution and fiscal envelope.

1. **Assign a Unique `P:DD` ID** in [`decks/cards.yaml`](decks/cards.yaml) using the appropriate deck prefix (`B`, `T`, `C`, `K`, `N`, `H`, or `E`), starting from [`metadata/card_template.yaml`](metadata/card_template.yaml).
2. **Enforce Fiscal & Crowd-Out Honesty:** In **Phase 1 (`SS1`)**, the Crown ledger is strictly cash-neutral (`NZD 9.19B` 5-year envelope). If your card requires upfront public cash in `SS1`, your `effects` block *must* specify either:
   * Which existing revenue stream or avoided remediation cost (`Exits 1, 2, 4`) funds it, **OR**
   * The exact **Social Crowd-Out Penalty** (`+NZD 105,000/yr per stunted child`) incurred if it raids `B:01` or `B:02`.
3. **Include the `co2e_impact` Slot:** Populate `co2e_impact.display` if your card has a computable direct or indirect emissions impact (or set `status: "na"`).
4. **Cite Empirical Anchors:** Every quantitative claim must cite a peer-reviewed or official benchmark in [`metadata/empirical_sources.yaml`](metadata/empirical_sources.yaml) (e.g., Dunedin Study, Growing Up in NZ, Stats NZ HES, Murphy-Shleifer-Vishny 1991, Koi Tū, or an international natural experiment).

---

### Track 2: "Challenge Mode" Pull Request (Second-Order Stationary Distribution Shift)
*(See [**Tutorial Part 2 & The 5-Sector Answer Key in `rules/game_changer_tutorial.md`**](rules/game_changer_tutorial.md#tutorial-part-2-challenge-mode-recomputing-the-stationarydist-qea-2026--firming-the-economic-grid) for the complete worked example of how [`QEA_2026.m`](https://github.com/MichaelTiemann/QEA-2026/blob/main/QEA_2026.m) unlocks `E:02` and `E:03`.)*

Use Track 2 if you are proposing a **Game-Changer Card (`E:XX` or new prefix)** that alters the underlying macroeconomic equilibrium (such as `QEA_2026.m` converting energy from an AR(1) stochastic expense `z2` into a solar endowment `pv`, releasing `NZD 60.8B–91.5B` in precautionary savings).

1. **Include or Link the VFI Toolkit / MATLAB Script:** Provide your reproducible `.m` script (compatible with `VFIToolkit-matlab` on GPU) showing:
   * The state-space definition (`n_d`, `n_a`, `n_z`, `N_j`);
   * The `ReturnFn` and parameters (`sigma`, discount factor `beta`, shock persistence `rho_z`);
   * The Baseline (`Regime 1`) vs. Reformed (`Regime 2`) stationary distribution output.
2. **Add the Summary CSV Table to `data/`:** Export the sector-by-sector or decile-by-decile quantitative impact as a clean CSV in `data/` (like [`data/electrification_5sector.csv`](data/electrification_5sector.csv)) so non-programmers can audit the numbers.
3. **Add the Unlocked Cards to `decks/cards.yaml`:** Include both the Track 1 first-order compromise card (e.g., `E:01`) and the Track 2 general-equilibrium unlocked cards (e.g., `E:02`, `E:03`).

---

### Track 3: Demographic Data & Baseline Customization (`data/*.csv`)
Researchers, teachers, and international adapters are encouraged to customize or expand the demographic and distributional tables in `data/` (`earn_plus_own_10tiers.csv`, `d20_veil_of_ignorance.csv`, `electrification_5sector.csv`):

* **Expanding or Re-Binning Wealth & Income Tiers (e.g., 10 Tiers vs. 12 Tiers vs. 20 Vigintiles):**
  * The canonical [`data/earn_plus_own_10tiers.csv`](data/earn_plus_own_10tiers.csv) uses 10 representative `Earn + Own` (`Annual Income + Net Worth`) archetypes anchored to Document 1A.
  * Contributors can submit alternative CSV tables (or toggle scripts) that expand the resolution to **12 tiers** (e.g., inserting intermediate `P98: 600k + 5M` and `P99.7: 1M + 20M` brackets), **20 vigintiles** (for 1:1 `d20` mapping), or **100 percentiles**.
* **Changing Statistical Baselines (Median vs. Mean, Top-Weighted vs. Bottom-Weighted):**
  * **Median vs. Mean Anchoring:** In skewed wealth distributions, the New Zealand household *median* net worth (`NZD 529k` in Stats NZ HES, `Tier 3: 200k + 500k`) sits at roughly half the *mean* net worth (`NZD 1.041M`, `Tier 4: 300k + 1M`). Users can configure the `d20` and Sankey baselines to weight cohorts by **vigintile medians** (best for typical voter/household experience) or **vigintile means** (required for exact aggregate fiscal and estate-tax revenue closure).
  * **Bottom-Weighted (Rawlsian / Dunedin 22% Focus) vs. Top-Weighted (Pareto Tail / IRD High-Wealth Focus):**
    * Use **Bottom-Weighted** binning (like the `01:01` to `01:20` Nat 1 sub-roll in `d20_veil_of_ignorance.csv` or the 14.3% GUiNZ vs. 22.0% Dunedin hardship benchmarks) when stress-testing early childhood wraparound (`B:01`), Oranga Tamariki care exits (`Exit 1`), and ACC actuarial cost avoidance (`B:07`).
    * Use **Top-Weighted** Pareto-tail binning (like the `20:01` to `20:20` Nat 20 sub-roll or the IRD High-Wealth Individuals Research Project cohorts from `NZD 50M` to `NZD 250M+`) when stress-testing the Guvenen "use-it-or-lose-it" entrepreneurial split (`z_h` vs. `z_l` in `B:05`) and estate-levy revenue curves.
* **Adding Regional or International Disaggregations:** Users can add columns or companion CSVs disaggregating trajectories across the **4 Regions + Abroad** (`Rural`, `Small`, `Large`, `Auckland`, `Abroad`), housing tenure (`Renters`, `Leveraged Owners`, `Outright Retiree Owners`), or peer-country comparisons (e.g., adapting the deck for Finland, Scotland, Australia, or Canada).

---

### Track 4: "Theme & Artwork" Pull Request (Skinning the Deck)
Artists, designers, and school/community groups can create a new visual theme (or contribute individual card illustrations to an existing theme) without writing a single line of simulation code:

1. **Create a Theme Folder:** Copy `themes/generic/theme.yaml` to `themes/<your_theme>/theme.yaml` and set `fallback_chain: ["generic"]` (or chain off another theme like `["waka_hourua", "generic"]`).
2. **Drop Canonically Named Files into `assets/` or `cards/`:**
   * Replace the colon in the card's `P:DD` ID with an underscore (`B:01` $\rightarrow$ `B_01`).
   * **Visual Art:** Save your illustration as `themes/<your_theme>/assets/B_01.png` (or `.svg` / `.webp`).
   * **Custom Markdown Text:** Save localized or translated card text as `themes/<your_theme>/cards/B_01.md`.
   * **Automatic Fallback:** You do *not* need to draw all 43 cards to publish a theme! Any card missing from your folder automatically cascades down your `fallback_chain` to `themes/generic/`, which renders the card directly from Markdown with the `P:DD` face index in the upper-left corner and the `🌱 CO2e` impact badge in the upper-right (or bottom-right) corner.
3. **Preview & Print Your Deck on A3 Landscape Sheets:** See the [Quick-Start Rendering & Printing Guide in `README.md`](README.md#4-quick-start-rendering--printing-the-deck-52-stacked-bond-a3-sheets).

---

## Card Schema Specification (`decks/cards.yaml`)

Every card in [`decks/cards.yaml`](decks/cards.yaml) conforms to the following YAML schema (also available as a blank template in [`metadata/card_template.yaml`](metadata/card_template.yaml)):

```yaml
  - id: "P:DD"                          # Unique prefix + 2-digit code (e.g., "B:01", "T:05", "E:02")
    name: "Card Title"                  # Full display title
    deck: "base"                        # Enum: base | traps | climate | kaupapa | nobel | orthodoxy | electrification
    module_level: 1                     # Onboarding level (1=Base/Traps, 2=Climate, 3=Kaupapa, 4=Nobel/Boss, 5=Game-Changer)
    type: "Card Type"                   # e.g., "Cohort Identity", "Legendary Artifact", "Wayfinder Persona"
    lens: ["Lens 1"]                    # Lifecycle lenses affected: Lens 1 (0-19), Lens 2 (20-64), Lens 3 (65+)
    gate_or_phase: "Gate 1"             # Gate 1 (0-5), Gate 2 (12-14), Gate 3 (20-35), SS0, SS1, or SS2
    cost_or_requirement: "..."          # Resource cost, policy lever, or combo requirement
    synergy_links: ["B:02"]             # Array of P:DD card IDs that combo with this card
    co2e_impact:                        # Optional CO2e badge rendered in top-right or bottom-right corner
      display: "-10.0 MtCO2e / yr"
      status: "computed"                # Enum: computed | indirect_enabler | hazard_increase | na
    effects:                            # Array of named game mechanics / rules text
      - label: "Mechanic Name"
        rule: "Exact quantitative and tabletop rule effect."
    flavor_text: "..."                  # Thematic quote capturing the political-economy insight
    empirical_anchor: "..."             # Citation to Document 1A/1B/1C, QEA-2026, or historical data
```
