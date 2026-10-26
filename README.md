# Beyond the Magic Money Tree — *Foils & Founders: The Aotearoa Deck*

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)]([https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/))
[![Engine: VFI Toolkit GPU](https://img.shields.io/badge/Engine-VFI_Toolkit_GPU-blue.svg)](https://github.com/MichaelTiemann/IGWelfare)

An open-source cooperative/competitive tabletop strategy game and macroeconomic simulation companion to ***Intergenerational Welfare, Capital Allocation, and Human Potential in New Zealand*** by Michael Tiemann ([Document 1A](https://github.com/MichaelTiemann/IGWelfare), `Document 1B`, and [Document 1C](https://github.com/MichaelTiemann/IGWelfare/blob/main/Document%201C.md)).

---

## 1. Why a Card Game? (Rule Zero: The Rawlsian D20 Test)

Pick up a 20-sided die (`1` to `20`, representing the 20 wealth vigintiles of Aotearoa New Zealand). Imagine you are behind John Rawls's **Veil of Ignorance** (`B:00`), rolling to see which family balance sheet you are born into:

* **In the Orthodox Status Quo (`SS0` — Displacement Mode):**
  * Roll `1–4` (the 22% Dunedin Study early hardship corner) and you face severe developmental stunting, driving 57%–81% of adult hospital nights, state care (`NZD 180k/yr`), and prisons.
  * Roll `5–18` and you face `3.10x` metropolitan housing stress, delayed family formation (`1.66 TFR`), PAYE taxes climbing toward `28.22%`, and emigrating children.
  * Roll `19–20` (even a `Nat 20`) and the macro board *still* collapses around you: net Crown debt spirals toward `200% of GDP`, core infrastructure fails, and your grandchildren move to Sydney. **There is no number you can roll that wins the game.**
* **In the IGWelfare Scenario (`SS0 -> SS1 -> SS2` — Up on Foils / *Te Waka Hourua*):**
  * **All 20 median wealth groups (`1` to `20`) are better off** (`+20.49%` national welfare gain, active entrepreneurs ahead all the way up to `NZD 100M` net worth, Universal NZ Super kept at Age 65, and working-age PAYE taxes cut by `-3.5 percentage points` to `18.5%`). **Roll any number. You win.**

---

## 2. Two Cultural Groundings: One Vessel, Two Hulls (*Te Waka Hourua*)

Like *Te Waka Hourua*—the double-hulled voyaging vessel where two hulls are lashed together by *kīato* (cross-beams)—every mechanic on the board can be played through **two one-to-one isomorphic narratives** (see [**`STORIES.md`**](STORIES.md) for the full lore and [**Side-by-Side Translation Key**](STORIES.md#side-by-side-translation-key-one-game-two-groundings)):

1. [**Story Lens A — *Up on Foils* (Pākehā / Systems Engineering):**](STORIES.md#story-lens-a-up-on-foils--how-emirates-team-new-zealand-bent-the-rulebook) How Emirates Team New Zealand bent the straight-keel orthodoxy in 2013 by coupling a **Front Lifting Foil (`B:01` + `B:02`)**, a **Wing-Sail Power Plant (`B:05` + `B:03` + `E:02`)**, and a **Rear T-Foil Rudder Stabilizer (`B:06` + `B:07`)** to lift the catamaran out of the water and slash hydrodynamic drag by 75%.
2. [**Story Lens B — *Te Waka o Whānau* (Te Ao Māori & Moana Pasifika *Pūrākau*):**](STORIES.md#story-lens-b-te-waka-o-whānau--being-becoming--crossing-over-māori--pasifika-pūrākau) The three-stage intergenerational crossing from **Being** (*He Kākano i Ruia mai i Rangiātea*, wrapping the sacred seed in *Te Korowai Mokopuna* and *Whānau Ora*, `B:01`), through **Becoming** (ascending *Te Aka Matua* together via reciprocal *Tuakana–Teina* and *Ako*, `B:02`, `C:03`, and restoring *Tūrangawaewae* at home, `B:03`, `B:05`), to **Crossing Over** (honoring our *kaumātua* navigators as they pass down *Ngā Kete o te Wānanga*, `K:06`, `B:06`).

---

## 3. Progressive Onboarding: The 7 Modular Decks (`P:DD` Taxonomy)

Every card in [`decks/cards.yaml`](decks/cards.yaml) uses a permanent **`P:DD`** identifier (rendered in the upper-left corner, with an optional **`🌱 CO2e`** impact badge in the upper-right or bottom-right corner) so cross-references never break when the community adds new cards via Pull Request:

| Prefix | Deck Name | Cards | Onboarding Level & Focus |
| :---: | :--- | :---: | :--- |
| **`B`** | **Base Game: Up on Foils** | `B:00` – `B:09` | **Level 1 (15-Min Demo):** The Rawlsian D20, the 3 Lifecycle Gates, the Guvenen Split, ACC Time-Bend, & the 2050 50/50 Stabilizer. |
| **`T`** | **Cautionary Traps** | `T:00` – `T:05` | **Level 1B (Pitch-Pole Warnings):** Molesworth St Cycle-Lane Promo, Scottish Devolution Ceiling, 1989 Tokyo Bubble, Seoul Hagwon Squeeze, Lavoisier Talent Drain, & Disinformation Drag. |
| **`C`** | **Climate & Resilience** | `C:01` – `C:06` | **Level 2 (Rising Seas):** Bilal–Känzig `USD 1,200/tCO2e` Shock, Cognitive Flexibility, Project K / Kura-ā-Iwi, Coastal Armor, & 4-Region Compass. |
| **`K`** | **Wayfinders & Kaupapa** | `K:01` – `K:07` | **Level 3 (Co-Op Personas):** Philanthropist/Iwi (`K:01`), Venture (`K:02`), Treasury/RBNZ (`K:03`), Economist (`K:04`), Artist (`K:05`), Kaumātua (K:06), & Kotahitanga (K:07). |
| **`N`** | **Nobel Archive** | `N:01` – `N:06` | **Level 4A (Theoretical Proof):** Coase (1991), Heckman (2000), Williamson (2009), Ostrom (2009), Romer (2018), & The Aotearoa Synthesis. |
| **`H`** | **Orthodoxy Boss Deck** | `H:01` – `H:05` | **Level 4B (Boss Counters):** Defeating Cash-Flow Myopia, Central Silos, Brain-Drain Vortex, Pension Austerity, & Land Bubbles. |
| **`E`** | **Game-Changer Tutorial** | `E:01` – `E:03` | **Level 5 (Modding the Engine):** Easy Mode (`E:01` Fuels for Finance) vs. Challenge Mode (`E:02`–`E:03` `QEA-2026` Precautionary Capital Release). |

---

## 4. Quick-Start: Rendering & Printing the Deck (5×2 Stacked-Bond A3 Sheets)

The repository includes a Python compiler ([`scripts/render_cards.py`](scripts/render_cards.py)) that merges [`decks/cards.yaml`](decks/cards.yaml) with any theme dictionary in `themes/<theme>/theme.yaml` and outputs print-ready **5×2 Stacked-Bond A3 Landscape** sheets (10 cards per sheet across 5 A3 sheets = 50 card slots, comprising the 43 canonical cards and 7 `P:??` open-source write-in wildcards).

### Step 1: Install Dependencies
```bash
python3 -m pip install pyyaml markdown
```

### Step 2: Render HTML Previews by Theme
Run `scripts/render_cards.py` from the root of the repository:

```bash
: "1. Generic Typographic Theme (CO2e badge in upper-right corner)"
python3 scripts/render_cards.py --theme generic --co2-pos top-right --out build/generic.html

: "2. Te Waka Hourua Theme — Māori & Pasifika Pūrākau (CO2e badge in bottom-right corner)"
python3 scripts/render_cards.py --theme waka_hourua --co2-pos bottom-right --out build/waka_preview.html

: "3. Up on Foils Theme — America's Cup Systems Engineering"
python3 scripts/render_cards.py --theme foils_pakeha --co2-pos top-right --out build/foils_preview.html
```
*(Optional flags: `--no-wildcards` omits the 7 `P:??` write-in cards; `--export-generic-md` exports individual `.md` card files into `themes/generic/cards/`.)*

### Step 3: Print or Export to A3 Landscape PDF
* **From Chrome / Edge (`Ctrl+P` / `Cmd+P`):** Open `build/generic.html` or `build/waka_preview.html`, press `Ctrl+P`, and set **Destination:** `Save as PDF`, **Paper size:** `A3`, **Layout:** `Landscape`, **Margins:** `Default` (or `Minimum`), **Scale:** `Default (100%)`, and check **Background graphics**.
* **One-Command Headless Chrome PDF Build (Windows PowerShell):**
  ```powershell
  & "C:\Program Files\Google\Chrome\Application\chrome.exe" `
    --headless --disable-gpu --no-pdf-header-footer `
    --print-to-pdf="$PWD\build\deck_A3_sheets.pdf" `
    "file:///$PWD/build/generic.html"
  ```

---

## 5. Repository Layout, Contributing, & Licensing

* **Narrative & Lore ([`STORIES.md`](STORIES.md)):** The full dual-lens grounding (*Up on Foils* and *Te Waka o Whānau*) plus the side-by-side translation table.
* **Master Decks & Schemas (`decks/`, `metadata/`, `themes/`):** Canonical card definitions (`decks/cards.yaml`), YAML card template and empirical source registries (`metadata/`), and cascading visual themes (`themes/generic/`, `themes/foils_pakeha/`, `themes/waka_hourua/`).
* **Core Rules & Card Design Tutorials (`rules/`, `decks/`):** Complete tabletop rules ([`rules/rules.md`](rules/rules.md)), the `QEA-2026` Game-Changer Tutorial ([`rules/game_changer_tutorial.md`](rules/game_changer_tutorial.md)), the Finland vs. NZ Disinformation Tutorial ([`rules/T_05_tutorial.md`](rules/T_05_tutorial.md)), and the D20 Sub-Roll Scorecards ([`decks/nat_1.md`](decks/nat_1.md) & [`decks/nat_20.md`](decks/nat_20.md)).
* **Audit & Scorecard Data (`data/`):** Reproducible CSV scorecards for the Rawlsian D20 (`d20_veil_of_ignorance.csv`), the 10-Tier Earn + Own Incidence Audit (`earn_plus_own_10tiers.csv`), and the 5-Sector National Electrification Scorecard (`electrification_5sector.csv`).
* **How to Submit a Pull Request ([`CONTRIBUTING.md`](CONTRIBUTING.md)):** Supports **Track 1** (First-Order Cards), **Track 2** (Second-Order VFI Toolkit Stationary Distribution Shifts), **Track 3** (Demographic & Baseline Customizations: 10 vs. 12 tiers, median vs. mean, bottom- vs. top-weighted), and **Track 4** (Artist Themes & Card Illustrations).
* **License:** Game rules, stories, card text, artwork themes, and data tables are licensed under [Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`)](https://creativecommons.org/licenses/by-sa/4.0/). Simulation and rendering scripts (`*.m`, `*.py`) are dual-licensed under `GPL-3.0-or-later` / `MIT`.
