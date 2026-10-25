# Contributing to *Foils & Founders: The Aotearoa Deck*
**License:** Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`) for all game rules, cards, and data tables; `GPL-3.0-or-later` / `MIT` for VFI Toolkit MATLAB/GPU simulation scripts.

## Repository Architecture

```text
IGWelfare/game/
├── README.md                          # Game overview, Legend, and Quick-Start Guide
├── LICENSE                            # CC-BY-SA-4.0 License text
├── CONTRIBUTING.md                    # Pull Request guidelines for cards & mechanics
├── rules/
│   ├── core_rules.md                  # Base game rules, 3-Turn Demo, & P:DD taxonomy
│   └── game_changer_tutorial.md       # Easy Mode vs. Challenge Mode (QEA-2026) tutorial
├── decks/
│   ├── cards.yaml                     # Canonical master database of all 41 P:DD cards
│   └── cards.json                     # Auto-generated JSON mirror for web/UI rendering
└── data/
    ├── d20_veil_of_ignorance.csv      # B:00 Rawlsian D20 (Nat 1 & Nat 20 sub-roll tables)
    ├── electrification_5sector.csv    # E:01-E:03 5-Sector CapEx & Precautionary Release
    └── earn_plus_own_12tiers.csv      # B:05 Guvenen Use-It-Or-Lose-It 12-Tier Audit
