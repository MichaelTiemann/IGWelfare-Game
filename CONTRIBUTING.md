# Contributing to *Foils & Founders: The Aotearoa Deck*

**License:** Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`) for all game rules, cards, artwork themes, and data tables; `GPL-3.0-or-later` / `MIT` for VFI Toolkit MATLAB/GPU simulation scripts[cite: 1].

## Repository Architecture

```text
IGWelfare-Game/
├── README.md                          # Game overview, Dual-Lens Lore, and Quick-Start Guide
├── LICENSE                            # CC-BY-SA-4.0 License text
├── CONTRIBUTING.md                    # Pull Request guidelines for cards, mechanics, & data
├── rules/
│   ├── core_rules.md                  # Base game rules, 3-Turn Demo, & P:DD taxonomy
│   └── game_changer_tutorial.md       # Easy Mode vs. Challenge Mode (QEA-2026) tutorial
├── decks/
│   ├── cards.yaml                     # Canonical master database of all 41 P:DD cards
│   └── cards.json                     # Auto-generated JSON mirror for web/UI rendering
├── themes/
│   ├── generic/                    # Root fallback theme (Markdown-driven typography)
│   │   ├── theme.yaml              # Base CSS variables, fonts, & deck color borders
│   │   └── cards/                  # Optional per-card Markdown overrides (B_01.md)
│   ├── foils_pakeha/               # America's Cup Hydrofoil & Systems Engineering art
│   │   ├── theme.yaml              # fallback_chain: ["generic"]
│   │   └── assets/                 # B_04.png, E_02.svg, T_00.webp, etc.
│   └── waka_hourua/                # Te Ao Māori & Pasifika Pūrākau art (Kaitiaki-vetted)
│       ├── theme.yaml              # fallback_chain: ["foils_pakeha", "generic"]
│       ├── cards/                  # Optional localized Māori/Pasifika title overrides
│       └── assets/                 # B_01.png (He Kākano), B_02.png (Tuakana-Teina), etc.
├── data/
│   ├── d20_veil_of_ignorance.csv      # B:00 Rawlsian D20 (Nat 1 & Nat 20 sub-roll tables)
│   ├── electrification_5sector.csv    # E:01-E:03 5-Sector CapEx & Precautionary Release
│   └── earn_plus_own_10tiers.csv      # B:05 Guvenen Use-It-Or-Lose-It 10-Tier Audit
└── scripts/
    └── render_cards.py                # Compiles cards.yaml + theme into HTML/Print-PDF/MD
```

---

## Four Tracks for Submitting a Pull Request

Because *Foils & Founders* is designed as an open-source policy and pedagogical engine, contributors can modify or extend the game across **four tracks**:

### Track 1: "Easy Mode" Pull Request (First-Order Card or Rule Tweak)
Use Track 1 if you are proposing a new **Cohort (`B:XX`)**, **Cautionary Trap (`T:XX`)**, **Climate Resilience (`C:XX`)**, **Kaupapa Persona (`K:XX`)**, or **Orthodoxy Hazard (`H:XX`)** card that operates within the existing stationary distribution and fiscal envelope.

1. **Assign a Unique `P:DD` ID** in `decks/cards.yaml` using the appropriate deck prefix (`B`, `T`, `C`, `K`, `N`, `H`, or `E`).
2. **Enforce Fiscal & Crowd-Out Honesty:** In `Phase 1 (SS1)`, the Crown ledger is strictly cash-neutral (`NZD 9.19B` 5-year envelope). If your card requires upfront public cash in `SS1`, your `effects` block **must** specify either:
   * Which existing revenue stream or avoided remediation cost (`Exits 1, 2, 4`) funds it, OR
   * The exact **Social Crowd-Out Penalty** (`+NZD 105,000/yr per stunted child`) incurred if it raids `B:01` or `B:02`.
3. **Include the `co2e_impact` Slot:** Populate `co2e_impact.display` if your card has a computable direct or indirect emissions impact (or set `status: "na"`).
4. **Cite Empirical Anchors:** Every quantitative claim must cite a peer-reviewed or official benchmark (e.g., Dunedin Study, Growing Up in NZ, Stats NZ HES, Treasury CBAx Circular 2024/15, or an international natural experiment).

---

### Track 2: "Challenge Mode" Pull Request (Second-Order Stationary Distribution Shift)
Use Track 2 if you are proposing a **Game-Changer Card (`E:XX` or new prefix)** that alters the underlying macroeconomic equilibrium (such as `QEA_2026.m` converting energy from an AR(1) stochastic expense `z2` into a solar endowment `pv`, releasing `NZD 60.8B–91.5B` in precautionary savings).

1. **Include or Link the VFI Toolkit / MATLAB Script:** Provide your reproducible `.m` script (compatible with `VFIToolkit-matlab` on GPU) showing:
   * The state-space definition (`n_d`, `n_a`, `n_z`, `N_j`);
   * The `ReturnFn` and parameters (`sigma`, discount factor `beta`, shock persistence `rho_z`);
   * The Baseline (`Regime 1`) vs. Reformed (`Regime 2`) stationary distribution output.
2. **Add the Summary CSV Table to `data/`:** Export the sector-by-sector or decile-by-decile quantitative impact as a clean CSV in `data/` so non-programmers can audit the numbers.
3. **Add the Unlocked Cards to `decks/cards.yaml`:** Include both the Track 1 first-order compromise card (e.g., `E:01`) and the Track 2 general-equilibrium unlocked cards (e.g., `E:02`, `E:03`).

---

### Track 3: Demographic Data & Baseline Customization (`data/*.csv`)
Researchers, teachers, and international adapters are encouraged to customize or expand the demographic and distributional tables in `data/` (`earn_plus_own_10tiers.csv`, `d20_veil_of_ignorance.csv`, `electrification_5sector.csv`):

* **Expanding or Re-Binning Wealth & Income Tiers (e.g., 10 Tiers vs. 12 Tiers vs. 20 Vigintiles):**
  * The canonical [`data/earn_plus_own_10tiers.csv`](data/earn_plus_own_10tiers.csv) uses 10 representative `Earn + Own` (`Annual Income + Net Worth`) archetypes anchored to Document 1A.
  * Contributors can submit alternative CSV tables (or toggle scripts) that expand the resolution to **12 tiers** (e.g., inserting intermediate `P98: 600k + 5M` and `P99.7: 1M + 20M` brackets), **20 vigintiles** (for 1:1 d20 mapping), or **100 percentiles**.
* **Changing Statistical Baselines (Median vs. Mean, Top-Weighted vs. Bottom-Weighted):**
  * **Median vs. Mean Anchoring:** In skewed wealth distributions, the New Zealand household **median** net worth (`NZD 529k` in Stats NZ HES, Tier 3: `200k + 500k`) sits at roughly half the **mean** net worth (`NZD 1.041M`, Tier 4: `300k + 1M`). Users can configure the d20 and Sankey baselines to weight cohorts by **vigintile medians** (best for typical voter/household experience) or **vigintile means** (required for exact aggregate fiscal and estate-tax revenue closure).
  * **Bottom-Weighted (Rawlsian / Dunedin 22% Focus) vs. Top-Weighted (Pareto Tail / IRD High-Wealth Focus):**
    * Use **Bottom-Weighted** binning (like the `01:01` to `01:20` Nat 1 sub-roll in `d20_veil_of_ignorance.csv` or the `14.3%` GUiNZ vs. `22.0%` Dunedin hardship benchmarks) when stress-testing early childhood wraparound (`B:01`), Oranga Tamariki care exits (`Exit 1`), and ACC actuarial cost avoidance (`B:07`).
    * Use **Top-Weighted** Pareto-tail binning (like the `20:01` to `20:20` Nat 20 sub-roll or the IRD High-Wealth Individuals Research Project cohorts from `NZD 50M` to `NZD 250M+`) when stress-testing the Guvenen "use-it-or-lose-it" entrepreneurial split (`z_h` vs. `z_l` in `B:05`) and estate-levy revenue curves.
* **Adding Regional or Demographic Disaggregations:** Users can add columns or companion CSVs disaggregating trajectories across the **4 Regions + Abroad** (`Rural`, `Small`, `Large`, `Auckland`, `Abroad`), housing tenure (`Renters`, `Leveraged Owners`, `Outright Retiree Owners`), or custom country datasets (e.g., adapting the deck for Scotland, Australia, Canada, or the Nordic countries).

---

### Track 4: "Theme & Artwork" Pull Request (Skinning the Deck)
Artists, designers, and school/community groups can create a new visual theme (or contribute individual card illustrations to an existing theme) without writing a single line of simulation code:

1. **Create a Theme Folder:** Copy `themes/generic/theme.yaml` to `themes/<your_theme>/theme.yaml` and set `fallback_chain: ["generic"]` (or chain off another theme like `["waka_hourua", "generic"]`).
2. **Drop Canonically Named Files into `assets/` or `cards/`:**
   * Replace the colon in the card's `P:DD` ID with an underscore (`B:01` -> `B_01`).
   * **Visual Art:** Save your illustration as `themes/<your_theme>/assets/B_01.png` (or `.svg` / `.webp`).
   * **Custom Markdown Text:** Save localized or translated card text as `themes/<your_theme>/cards/B_01.md`.
   * **Automatic Fallback:** You do **not** need to draw all 41 cards to publish a theme! Any card missing from your folder automatically cascades down your `fallback_chain` to `themes/generic/`, which renders the card directly from Markdown with the `P:DD` face index in the upper-left corner and the `🌱 CO2e` impact badge in the upper-right (or bottom-right) corner.
3. **Preview Your Deck:** Run `python3 scripts/render_cards.py --theme <your_theme> --co2-pos top-right` and open `build/deck_preview.html` in any browser.

---

## Card Schema Specification (`decks/cards.yaml`)

Every card in `decks/cards.yaml` conforms to the following YAML schema:

```yaml
- id: "P:DD"                  # Unique prefix + 2-digit code (e.g., "B:01", "K:04", "E:02")
  name: "Card Title"          # Full display title
  deck: "base"                # Enum: base | traps | climate | kaupapa | nobel | orthodoxy | electrification
  module_level: 1             # Onboarding level (1=Base Demo, 2=Climate, 3=Kaupapa, 4=Nobel/Boss, 5=Game-Changer)
  type: "Card Type"           # e.g., "Cohort Identity", "Legendary Artifact", "Wayfinder Persona"
  lens: ["Lens 1"]            # Lifecycle lenses affected: Lens 1 (0-19), Lens 2 (20-64), Lens 3 (65+)
  gate_or_phase: "Gate 1"     # Gate 1 (0-5), Gate 2 (12-14), Gate 3 (20-35), SS0, SS1, or SS2
  cost_or_requirement: "..."  # Resource cost, policy lever, or combo requirement
  synergy_links: ["B:02"]     # Array of P:DD card IDs that combo with this card
  co2e_impact:                # Optional CO2e badge rendered in top-right or bottom-right corner
    display: "-10.0 MtCO2e/yr"
    status: "computed"        # Enum: computed | indirect_enabler | hazard_increase | na
  effects:                    # Array of named game mechanics / rules text
    - label: "Mechanic Name"
      rule: "Exact quantitative and tabletop rule effect."
  flavor_text: "..."          # Thematic quote capturing the political-economy insight
  empirical_anchor: "..."     # Citation to Document 1A/1B/1C, QEA-2026, or historical data
```
