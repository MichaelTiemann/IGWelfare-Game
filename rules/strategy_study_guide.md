# FOILS & FOUNDERS: STRATEGY & ECONOMETRIC STUDY GUIDE
*Bridging Tabletop Gameplay to the 24-File GPU Spatial OLG Solver (`v2026.11`)*  
*Companion to `cards.yaml`, `study_cards.yaml`, `foils_and_founders_gameplay.md`, & `Documents 1A–3`*  
**Author:** Michael Tiemann (`mdtiemann@gmail.com`) | **License:** CC-BY-SA-4.0  
**Repository:** `https://github.com/MichaelTiemann/IGWelfare`

---

## 1. Executive Synthesis: How the Tabletop Mirrors the GPU Solver

Every card, die roll, and token in **Foils & Founders: The Aotearoa Deck** is an exact physical projection of an operator inside the 24-file `IGWelfare` MATLAB/GNU Octave VFI Toolkit suite (`Run_All_NZ_Intergen_Suite.m`). Understanding why certain strategies win on the tabletop means understanding why **"thick" probability distributions** behave completely differently from **"thin" deterministic spreadsheets** (`Document 2T`):

| Tabletop Mechanic | Underlying VFI / General-Equilibrium Operator | Quantitative Calibration (`launch` Branch) |
| :--- | :--- | :--- |
| **20-Turn Clock (`+3 Yrs/Turn`)** | Exact $\Delta t = 3$ scaling in `Configure_TimeGrid_Params.m` | Adult ages `20–99` (`J = 27`), Stage 1 child ages `0–5` (`j_p = 3,4`), Stage 2 ages `6–17` (`j_p = 5..8`), 60-yr transition (`2026–2086`). |
| **Rawlsian D20 (`B:00`)** | Newborn measure $\mu_{1,k}(a_1, h_1, z_1)$ & 10-Tier `Earn + Own` audit | `4` domestic regions (`Rural` 16.0%, `Small` 24.0%, `Large` 25.9%, `Auckland` 34.1%) + `Abroad` ($k=5$, $\varrho_{\mathrm{mig}} = 0.180$). |
| **3-Slot *Whānau* Mat (`2-of-3`)** | Mixed-horizon lifecycle stages (`Being`, `Becoming`, `Crossing Over`) | Asymmetric missing slot forces cross-table Variant B deals until `N:08` + `B:15` (`Super 64`, `TFR -> 1.87/2.03`) unlock Slot 3. |
| **`E:04` Thick vs. Thin Lens** | Dimension-free state-contingent conditioning (`Document 2T`) | Evaluates tail cliffs across `61 x 7 x 9 x 7 = 26,901` states/age/region at **zero extra GPU grid axes** (avoiding an `81x` Markov blowup). |
| **13-Wave *Te Kāhui Waka* (`N:01`)** | Convex Perron–Frobenius mixing (`Doc 2A` §4.4) & $\eta_{k,m}(t)$ (`Doc 2B` §7.6) | Mixes pure `Waiter` and `Active` kernels (`0, 1/3, 2/3, 1`); cuts surge loss `88.9%` ($\phi_{\mathrm{adj}} = 0.18$) and lifts `SS1` yield to `95.5%–96.8%`. |
| **$4 \times 4$ Coalition Matrix (`B:12`)** | 11-Layer Topkis (1998) supermodular lattice (`Table 19` & `Table 22`) | `+11.23 pp` isolated (`45.5%`) + **`+13.47 pp` Synergy Wedges (`54.5%`)** = **`+24.70% CE`** pre-NDC (`+25.19%` wave-convolved). |
| **Labrousse Tax Keys (`C:06`)** | $4 \times 5$ Gumbel step-migration sorting & Guvenen firm Bellman (`ReturnFn_Firm.m`) | `Rural <-> Small <-> Large <-> Auckland` chain exposes `Large` (`25.9%`) to two-flank leakage unless locked; shifts $\Gamma_k$ from $z_l$ (`61%->6%`) to $z_h$ (`29%->88%`). |
| **Food-Medicine Cluster (`C:07–C:10`)** | Dimension-free Rouwenhorst drift $\Delta\mu_{z,k}$ (`Doc 2T` §4.5) | `1.60x–2.16x` food hubs + anti-monopsony shift $\Delta\mu_{z,\mathrm{SS2}} = [+0.041..+0.010]$, retiring **`85%` of `SS1` `T_k`** to fund **`-0.64 pp` PAYE** (`-> 18.25%`). |
| **Year-5 ACC Time-Bend (`B:09`)** | 25-Yr PBE IFRS 17 Continuation Valuation (`Plot_ActuarialContinuationValuation.m`) | At `2.0%` real SRTP (`30%` haircut), Year-5 multiple `35.25B / 9.19B = 3.84x > 3.50` target drives reform credibility $\lambda_{\mathrm{cred}}(t) \to 1.0$. |
| **Two-Key Orbital Launch (`B:13`)** | `Plot_Doc1D_LaunchPlans.m` (`Plans A, B, & C`) & logistic seam $\Phi(t)$ | `Plan C` (`Yr 15`, Debt $\le 42\%$, `+NZD 190B` extra welfare) vs. `Plan B` (`Yr 16.8–20` cash breakeven, `+NZD 104B`) vs. `Plan A` (`Yr 25`). |

---

## 2. Behind Rawls's Veil (`B:00`): Confirming the Fumble (`Nat 1`) & Confirming the Crit (`Nat 20`)

In orthodox political debates, reform is framed as a zero-sum tug-of-war between the bottom vigintile (**Face `1`**) and the top vigintile (**Face `20`**). *Foils & Founders* begins with every player rolling `B:00` (*Te Tatau o Rangiātea*) to prove why **both tails lose under Status Quo (`SS0`)** and **both tails win on coupled hydrofoils (`SS2`)**.

### 2.1 Confirming the Fumble (`Rolls 1–4 / 1–6`: The `i_c = 0` Corner & Convex Grid Physics)
* **Why Families Pool at `i_c = 0` (`Node 1` & `Node 2`):** Early childhood enrichment exhibits a Stone–Geary subsistence/luxury threshold ($\bar{g}_{\mathrm{ECE}} = 0.032$). After paying `3.10x` Auckland rents ($Q_{\mathrm{Akl}} = 3.10$) or `2.74x` rural transport fuel bills ($\bar{e}_{\mathrm{Rural}} = 0.048$), `25.79%` of New Zealand births hit a binding cash-subsistence corner (`i_c = 0`).
  * *Solver Precision Note (`Doc 2A` §3.2.1):* Even in VFI models, naive linear grid spacing on $i_c \in [0, 0.50]$ places the first positive rung at `NZD 7,917/yr`, artificially rounding squeezed working families (**Node 2**, `~14.2%` of births) down to zero. Our solver uses a convex power grid $d_{\mathrm{grid},ic} = 0.50 \times \mathrm{linspace}(0,1,7)^{1.8}$ (`ic_2 = NZD 1,929/yr`) paired with continuous sub-grid cell interpolation $w_{\mathrm{cell}}$ over a 61-point cubic asset grid (`17` nodes below `NZD 45k`), isolating the *true* structural hardship cliff!
* **`'Dunedin_22'` vs. `'MetroSqueeze_GUiNZ'` (`H:03` Calibration Switch):**
  * **1972 Dunedin Baseline (`Rolls 1–4`, `22.0%`):** Caspi et al. (2016) proved that the most disadvantaged `22%` of three-year-olds account for **`57%–81%` (`74.1%` model fit)** of adult hospital nights, welfare receipt, and criminal convictions (`Exits 1, 2, & 4` = `NZD 17.7B/yr`).
  * **Modern GUiNZ Reality (`Rolls 1–6`, `~30%` National / `34%–36.6%` Auckland):** Incorporating `37%` damp/mould exposure and `>45%` pre-age-5 private rental transience expands reactive drag to `NZD 28.5B/yr`—which simultaneously raises `B:09`'s Year-5 actuarial return from **`3.84x` to `4.26x–4.45x`** once rescued!
* **How Coupled Reform Rescues Every `Nat 1` Sub-Slice:** Universal in-kind `B:01` (`G_{ECE,1}: 0.045 -> 0.130`), `B:02` Farm-to-ECE nutrition, `E:01` household electrification (`-NZD 3,000/yr` net bill relief), and `K:09` Waring *whānau* care lift bottom-vigintile welfare by **`+23.5% to +38.4% CE`**, compress struggling adult launch from `22.0%` to **`1.5%`**, and seed every mentored 20-year-old with `NZD 62k–76k` (`B:05`/`B:06`).

### 2.2 Confirming the Crit (`Roll 20`: Active `z_h` Builders vs. Passive `z_l` Land Hoarders)
What if you roll a **Natural `20`**? In `Plot_WealthBracket_GiveAndGain.m` (`Doc 2B` §5.5), welfare incidence is audited across **10 official survey-anchored `Annual Income + Net Worth` tiers** (Stats NZ HES, Rashbrooke 2021, IRD High-Wealth Individuals Research Project 2023, and the *NBR Rich List*), decomposing **3 Fiscal Give Channels** ($\Delta\mathrm{CE}_{\mathrm{House}} + \Delta\mathrm{CE}_{\mathrm{WealthTax}} + \Delta\mathrm{CE}_{\mathrm{Estate}} \le 0$) against **4 Economic Gain Channels** ($\Delta\mathrm{CE}_{\mathrm{ECE+Rent}} + \Delta\mathrm{CE}_{\mathrm{PAYE}} + \omega_{\mathrm{ent}}\Delta\mathrm{CE}_{\mathrm{Firm}} + \Delta\mathrm{CE}_{\mathrm{Cohesion}} > 0$):

| Survey-Anchored Bracket (`Earn + Own`) | Percentile | **Active `z_h` Builder** ($\omega_{\mathrm{ent}} = 0.80$) | **Passive `z_l` Land Hoarder** ($\omega_{\mathrm{ent}} = 0.15$) | Strategic Tabletop Lesson |
| :--- | :---: | :---: | :---: | :--- |
| **Tiers 1–5 (`NZD 45k+12k` $\to$ `240k+2.15M`)** | `P12–P90` | **`+25.4%` to `+3.6% CE`** | **`+25.4%` to `+3.6% CE`** | **100% of the bottom 90% win unconditionally.** |
| **Tier 8 (`High Professional / SME Owner`)** | `P99` | **`+3.6% CE`** | Mildly negative until rotated | `20%->12%` Corp cut + `18.25%` PAYE + `-60 bps` credit outweigh `1.5%` LVT! |
| **Tier 9 (`IRD High-Wealth Median: 2.1M + 50M`)** | `P99.9` | **`+1.2% CE` (Net Winner!)** | Negative if staying in `z_l` dirt | Guvenen `Use-It-Or-Lose-It` (`B:08`) rewards productive operating equity! |
| **Tier 10 (`NBR Rich List Median: 6.5M + 140M`)** | `P99.99` | **`-0.1% CE` (Exact Breakeven!)** | Bears dynastic estate/land levy | Active founders retain **`95.3%–98.5%`** of fortune (smaller than a routine RBNZ/GFC cycle—without living in a `185%`-debt country!). |

---

## 3. Strategic Core: The 11-Layer Supermodular Lattice & $4 \times 4$ Coalition Matrix (`B:12`)

The #1 strategic mistake in *Foils & Founders* is playing inside your own Wayfinder's comfort zone ("Silo Play"). `Plot_Counterfactuals_And_MirrorInvestments.m` (`Table 19`) and `Plot_Doc3_CoalitionSynergies_And_LTFMSinkhole.m` (`Table 22`) prove two iron laws of Aotearoa's political economy:

### 3.1 Iron Law 1: Every Single-Lane Silo Sinks Underwater Over 60 Years
Measured against the endogenous `-16.21% CE` LTFM fiscal sinkhole (`185%` debt, `28.2%` PAYE), **no coalition can save itself alone**:
* **Coalition 3 Alone (`K:05` GrowthNZ Tax/Enterprise Silo):** Finishes at **`-9.12% CE`** (`64.1%` of its connected potential comes from neighbors!). Cutting corporate taxes fails when `22%–30%` of youth arrive lacking foundational skills and `1 in 5` graduates move to Australia.
* **Coalition 4 Alone (`K:07` "Solve Debt First" Austerity Silo, `T:03`):** Finishes at **`-6.80% CE` & `112%` Debt** (`74.3%` neighbor-dependent!). Cutting ECE and hiking Super to 70 triggers a `52%–68%` senior disability leak and strips `-36.2%` of `K_whanau` care.
* **Coalition 2 Alone (`K:04` WellBeing Transfers/Housing Silo):** Finishes at **`-2.40% CE`** (`43.8%` neighbor-dependent!). Without `z_h` job upgrading (`C:09`) and early skill formation (`B:01+B:03`), cash transfers turn into permanent fiscal drag (`T:08` Scotland ceiling).
* **Coalition 1 Alone (`K:01` Barnardos/Early-Years Silo):** Finishes at **`-0.06% CE`** (`42.5%` neighbor-dependent!). Even world-class ECE/mentoring stalls if *Kaiako* are priced out by `3.10x` urban rents (`H:06`) and mentored 21-year-olds are exiled across the Tasman (`H:04`).

### 3.2 Iron Law 2: `54.5%` (`+13.47 pp`) of the Prize Lives in Four Supermodular Wedges
When all four lanes lash their hulls together (`B:12` + `K:10`), **7 Isolated Policy Levers (`+11.23 pp`, `45.5%`)** combine with **4 Dynamic Complementarity Wedges (`+13.47 pp`, `54.5%`)** to generate **`+24.70% CE` pre-NDC national welfare**:

1. **Wedge 1 — Dual-Gate Human Capital Synergy (`+3.32% CE` Nat., `13.4%` Share | `B:01 + B:03 + N:03`):**
   * *Math:* Stage 1 (`Ages 0–5`) is highly malleable ($\varphi_1 = +0.35, \sigma_1 = 1.54 > 1$), whereas Stage 2 (`Ages 6–17`) is a strict Cunha–Heckman harmonic bottleneck ($\varphi_2 = -0.95, \sigma_2 = 0.513 < 1$) with `22%` unbanked fade-out ($\delta_{\theta,\mathrm{fade}} = 0.22$). Deploying `B:01` + `B:03` together eliminates fade-out, activates downward *tuakana* scaffolding ($G_{\mathrm{ECE},1}^{\mathrm{eff}} = G_{\mathrm{ECE},1}(1 + \kappa_{\mathrm{down}}M_{\mathrm{mentor}}\bar{\theta}_{J=5})$), and yields `+7.33% CE` (`+2.46%` L1 + `+1.56%` L2 + **`+3.32%` Wedge 1**).
2. **Wedge 2 — 20% LVR Cliff & *Whānau* Co-Location Synergy (`+2.33% CE` Nat., `9.4%` Share | `B:06 + B:07/B:08 + C:07`):**
   * *Math:* Young adults escape rental user costs $r_{h,k}^{\mathrm{rent}}$ iff $a_1 + E \ge 0.20 Q_k(\tau_a, \tau_b)$. In Auckland ($0.20 \times 3.10 = 0.620$), neither the Youth Grant $E$ alone (`+0.89% CE`) nor `-10.5%` land cooling alone (`+2.24% CE`) clears the cliff; together they lift young Auckland ownership from `28.0%` to **`41.2%`** while anchoring *kuia* and *Kaiako* in urban suburbs via $(Q_{k,0}/Q_k)^{0.35}$.
3. **Wedge 3 — Cross-Stack Talent $\times$ Enterprise Ignition (`+5.20% CE` Nat., `+5.63%` Akl, `21.1%` Share | `K:01 x K:05 x K:03`):**
   * *Math:* The **single largest wedge in the entire model**! Captures four cross-partials: (i) assortative matching $\partial^2 Y_k / \partial Z_k \partial H_k > 0$ as thriving `h6–h7` youth (`23.5% -> 65.0%`) meet `z_h` firms (`29% -> 88%` of retained top talent); (ii) Gumbel brain-drain reversal (`10.93% -> 7.60%`, retaining `~3,550` graduates/yr); (iii) relief of the `H:06` *Kaiako* rent deflator; and (iv) provincial `z_l -> z_h` upgrading (`C:08 + C:09`, $\Delta\mu_{z,k} > 0$).
4. **Wedge 4 — Fiscal Harvest, Super-64 *Kuia* Dividend & 2nd-Gen Closure (`+2.62% CE` Nat., `10.6%` Share | `B:14 + B:15 + K:09 + N:08 + E:05`):**
   * *Math:* Combines `-60 bps` debt-sinking (`+1.25% CE`), `-3.75 pp` PAYE relief (`22.0% -> 18.25%`, incl. `-0.64 pp` from `85%` `T_k` retirement) + **Universal Super at Age 64** (`+2.69% CE`, $\Phi_{\mathrm{time}}(64) = 1.081$), Cao & Li ($\beta_{\mathrm{hyp}} = 0.72$) fertility recovery (`TFR: 1.66 -> 1.87 / 2.03`), and Daruich `Jump 2` second-generation parental transmission $\mathcal{T}_{\mathrm{IG}}$.
# ==============================================================================
# FOILS & FOUNDERS STRATEGY & STUDY GUIDE — BATCH 2 (SECTIONS 4 & 5)
# ==============================================================================

---

## 4. Pacing, Space & Uncounted Care: Mastering Waves, Regions & *Whānau* Physics

### 4.1 Why Wave Thirds Beat Day-1 Sprints (`N:01` + `N:07` vs. `T:04`)
In `Build_IntergenTransitionMatrix.m` (`Doc 2A` §4.4), phased rollouts cannot be modeled by feeding a blended mean parameter $\bar{G}_{k,m}(t) = (1 - s_{k,m})G_{m,0} + s_{k,m}G_{k,m}^{\mathrm{eff}}$ into the household Bellman equation—because giving `100%` of adolescents `1/3` of a mentor or `100%` of 20-year-olds `1/3` of a Youth Grant violates Jensen's Inequality across the concave $\varphi_2 = -0.95$ bottleneck and the discrete $a_1 + E \ge 0.20 Q_k$ deposit cliff:

$$f_{\mathrm{CES}}\Bigl(\theta_c, i_c, (1 - s_{k,m})G_{m,0} + s_{k,m}G_{k,m}^{\mathrm{eff}}\Bigr) > (1 - s_{k,m})f_{\mathrm{CES}}\bigl(\theta_c, i_c, G_{m,0}\bigr) + s_{k,m}f_{\mathrm{CES}}\bigl(\theta_c, i_c, G_{k,m}^{\mathrm{eff}}\bigr)$$

Instead, the GPU solver mixes pure **Waiter** and **Active Participant** Perron–Frobenius transition kernels at zero extra grid-dimension cost:

$$\mathbf{T}_{k,t}^{\mathrm{Mix}} = \bigl(1 - s_{k,m}(t)\bigr)\mathbf{T}_k^{\mathrm{Waiter}}\bigl(G_{m,0}\bigr) + s_{k,m}(t)\mathbf{T}_k^{\mathrm{Active}}\bigl(G_{k,m}^{\mathrm{eff}}(t)\bigr), \qquad s_{k,m}(t) \in \left\{0, \frac{1}{3}, \frac{2}{3}, 1\right\}$$

Simultaneously, `Plot_Doc1D_TeKahuiWakaSequencing.m` (`Doc 2B` §7.6, File #24) governs each wave's **Effective Delivery Multiplier** $\eta_{k,m}(t)$ via three operational frictions:

$$\eta_{k,m}(t) = \bigl(1 - \delta_{\mathrm{adopt}} e^{-\lambda_{\mathrm{adopt}}(t - t_{k,m}^0)}\bigr) \cdot \left[1 - \tau_{\mathrm{fric},\min} - \bigl(\tau_{\mathrm{fric},0} - \tau_{\mathrm{fric},\min}\bigr) e^{-\gamma_{\mathrm{learn}} \mathcal{L}_m(t-1)}\right] \cdot \left[1 - \phi_{\mathrm{adj}} \bigl(\Delta s_{k,m}(t)\bigr)^2\right]$$

* **Tactical Takeaway on the Mat:**
  1. **Never Fall for `T:04` (`SingleShot` $\Delta s = 1$):** Jumping straight to `3/3` on Turn 1 eats the full Day-1 Coase–North friction ($\tau_{\mathrm{fric},0} = 0.280$) *plus* the full Lucas–Hayashi workforce bottleneck ($\phi_{\mathrm{adj}}(1)^2 = 0.180$), slashing `SS1` delivery yield to **`79.5%–83.5%`**, wasting `NZD 3.8B` on unmentored grants (`H:10`), quadrupling Year-3 cash deficits (`-NZD 6.5B/yr`), and slapping a `-4` penalty onto Political Stability rolls!
  2. **Step in Regional Thirds (`*Te Kāhui Waka*` $\Delta s = 1/3$):** Cuts the quadratic bottleneck penalty by **`88.9%`** ($0.18 \times (\frac{1}{3})^2 = 0.020$) while Arrow–Deming inter-wave learning ($\gamma_{\mathrm{learn}} = 0.450$ toward $\tau_{\mathrm{fric},\min} = 0.035$) lifts `SS1` delivery yield to **`95.5%–96.8%`** (`98.5%–99.0%` in `SS2`).
  3. **Front-Load Provincial Electrification (`E:01` Waves `1–3`):** Deploy all three `Rural + Small` electrification waves consecutively in Turn 1 (`Years 1–3`) where mandatory fuel/energy floors ($\bar{e}_{\mathrm{Rural}} = 0.048, \bar{e}_{\mathrm{Small}} = 0.036$) are `2.25x–3.00x` Auckland's ($0.016$), compressing $\bar{e}_k$ by **`[-28%, -25%, -18%, -14%]`** (`NZD 3,000/yr` net household saving) before rolling out `Large` (`Waves 4–6`) and `Auckland` (`Waves 7–9`).

### 4.2 Spatial Tax Bargaining: Protecting the Exposed Middle Hinge (`C:06` vs. `T:06`)
In our $4 \times 5$ Gumbel location-choice matrix (`Build_IntergenTransitionMatrix.m`, calibrated to $\varrho_{\mathrm{mig}} = 0.180$ and Stillman & Maré's `-4.4` house-price retention elasticity), domestic mobility follows a nearest-neighbor chain: **`Rural (16.0%) <-> Small (24.0%) <-> Large (25.9%) <-> Auckland (34.1%)`**.
* **Strategic Positioning for `Large` Players (Wellington, Christchurch, Hamilton, Tauranga, Dunedin):** Do *not* advance `B:07` or `B:08` unilaterally! While `Rural + Small` lose only `-15%` to one-step jumps into `Auckland`, `Large` sits exposed on *both* flanks (`Q_Large = 2.05`) and suffers **`-60%` two-flank tax leakage** until `K:06` (*Fair-Markets & Tax-Compact Mediator*) locks adjacent keys into **`C:06`**.

### 4.3 The Rural & Small Graduation Playbook ("Good Food Is Medicine!" $\to$ `-0.64 pp` PAYE Cut)
Urban players sometimes ask why they should co-stake provincial cards (`B:02`, `B:04`, `C:08`, `C:09`). `Document 2T` §4.5 provides the exact answer:
* Breaking upstream farm-gate wholesale monopsony and retail grocery/supply duopolies (`C:08`, `Duffy & ComCom` [Ref 49]) while anchoring `Ka Ora, Ka Ako` (`B:02`) and `GrowingChange` youth enterprises (`B:04`, `92%` non-recidivism) in decentralized regional food hubs (`C:09`, `1.60x–2.16x` multiplier [Ref 56]) induces an upward productivity drift directly on the 7-point Rouwenhorst shock grid:
  $$\Delta\mu_{z,\mathrm{SS2}} = \bigl[+0.0408\ (\mathrm{Rural}),\ +0.0307\ (\mathrm{Small}),\ +0.0170\ (\mathrm{Large}),\ +0.0102\ (\mathrm{Auckland})\bigr]$$
* **Payoff for the Whole Table (`C:10`):** Lifting Rural welfare by `+2.81 pp` (`SS1`) and `+2.42 pp` (`SS2`) moves provincial households above the lower-tail abatement threshold of `C:07` (`T_k`), **retiring $\psi_{\mathrm{retire},T} = 85\%$ of the `SS1` geographic transfer top-up** (`T_k` falls from `[0.038, 0.031, 0.025, 0.028]` to `[0.018, 0.013, 0.008, 0.004]`) and funding **`-0.64 pp` of the national working-age PAYE tax cut** (`22.0% -> 18.25%`) for *every* region!

### 4.4 Marilyn Waring's `K_whanau` Operator & The Retirement-Age U-Curve (`Age 64` Sweet Spot)
`FertilityBargaining_Module.m` (`Table8B_SuperAge_UCurve_60to75.csv`, `Doc 2B` §5.4) and `Document 2T` §4.1 & §4.4 sweep statutory NZ Superannuation eligibility continuously across $A_{\mathrm{super}} \in [60, 75]$, exposing why orthodox calls to *"raise Super to 70 or means-test it"* (`H:05` / `T:03`) backfire catastrophically:

| Statutory Super Age ($A_{\mathrm{super}}$) | *Kuia / Whānau* Time Factor $\Phi_{\mathrm{time}}$ | Fiscal Leak / Offset & Sandwich Drag | Required `SS2` PAYE ($\tau_l^{\mathrm{req}}$) | National Welfare (`CE`) & Strategic Verdict |
| :---: | :---: | :--- | :---: | :--- |
| **Age `70` (`H:05` / `T:03` Trap)** | `0.638` (**`-36.2%` care loss!**) | `52%–68%` senior disability/ACC leak + **`K_whanau^net < 0` sandwich reversal** ($\psi_{\mathrm{sandwich}} = 0.28..0.35$) + regressive `h1–h2` wear! | `22.48%` (`25.00%` in `SS0` — **wipes out tax cut!**) | Boomerangs to `-6.80% CE` if paired with Year-0 ECE austerity! |
| **Age `65` (`SS1` Baseline Shield)** | `1.000` (Protected) | `0%` displacement leak; universal rule preserves private saving incentives ($a'$). | `17.97%` | **`+24.53% CE`** — Essential `SS1` stability anchor. |
| **Age `64` (`B:15` `SS2` Peak!)** | **`1.081` (`+8.1%` *Kuia* boost!)** | **`28%` (`\omega_{\mathrm{offset}} = 0.28`) avoided ACC / Supported Living offset**; lifts `TFR` (`1.66 -> 1.87 / 2.03`). | **`18.25%`** (`-3.75 pp` cut!) | **`+24.70% CE` (Global Optimum & Unlocks 3rd *Whānau* Slot!)** |
| **Age `60` (Denominator Wall)** | `1.158` (`+15.8%`) | Retiree dependency ratio swells to `39.78%`. | `21.05%` | Overshoots the working-age tax denominator. |

---

## 5. Surviving the Ballot Box, Calling Orbital Launch & Weathering Macro Shocks

### 5.1 Perishable Childhood (`T:07`) vs. Repeal-Proof Adult Equity (`E:05`) & Actuarial Credibility (`B:09`)
Why do early parliamentary elections (`Turns 3 & 6`) pose existential peril, whereas post-Year-20 elections barely dent the hydrofoil?
1. **Before Age 20 (Biological Wet Cement):** Unbanked childhood skill gains depreciate at $\delta_{\theta,\mathrm{fade}} = 0.22$ per period without sustaining adolescent environments. A **6-Year ("Two-Term") Stop-Go Pendulum (`T:07` Low Roll `1–5`)** inflicts $1 - (1 - 0.22)^2 = \mathbf{39.2\%}$ compound skill fade-out inside the $\varphi_2 = -0.95$ bottleneck and zeroes out off-diagonal Wedge Additionality—destroying **`84.6%` of the generational prize** (`+3.84% CE` vs. `+24.92%` full / `+12.46%` thin 50% duty-cycle guess)!
2. **The Year-5 Actuarial Credibility Shield (`B:09` + `N:04`):** Under Public Finance Act 1989 s26G(1)(e), Treasury Circular 2024/15 (`2.0%` real SRTP, `30%` attribution haircut), and ACC's PBE IFRS 17 *Outstanding Claims Liability* (`NZD 63.6B`) accounting standard, `Plot_ActuarialContinuationValuation.m` books **`NZD 10.68B` direct cost avoidance (`1.16x`)** and **`NZD 35.25B` total fiscal return (`3.84x > 3.50` target)** by Year 5 (`Turn 2`). That audited `3.84x` multiple drives private belief blending $\lambda_{\mathrm{cred}}^{\mathrm{actuarial}}(t) \to 1.0$ inside Bellman continuation values and arms **`+5` D20 Stability Shields** before Turn 3's election!
3. **After Age 20 (Durable Bedrock, `E:05`):** Once Wave `w` cohorts cross Age 20 with `B:03` mentoring + `B:05`/`B:06` home/enterprise equity banked, **`83.7%` of their welfare gain (`+20.86% CE`) is permanently immune to future political repeal**, and discrete wave convolution $\sum_{w=1}^{13} \Delta s_m(w) K_{\mathrm{mat}}(t - w - T_{\mathrm{gen},m})$ delivers the 2nd-generation Daruich harvest smoothly across `Years 21.5–35`!

### 5.2 Reading the Telemetry for `B:13` (*Te Kapehu Whetū* Orbital Launch: Plans C, B, & A)
`Plot_Doc1D_LaunchPlans.m` (`File #23`) compares three statutory Phase-2 (`SS2`) launch windows:
* **`Plan A` (Conservative Statutory Year 25 / Turn 8):** Zero risk, baseline reference trajectory reaching target at Year 60.0.
* **`Plan B` (Hard Cash-Flow Breakeven @ Year 16.8–20.0 / Turn 6–7 — Key 2):** Automatic zero-risk ignition once annual fiscal inflows exceed outlays (`NZD 0` bridge, `60.0x` peak fiscal ROI, **`+NZD 104B` extra cumulative welfare** over `Plan A`).
* **`Plan C` (`"We Got This!"` Slingshot @ Year 15 / Turn 5 — Key 1):** Requires all 13 *Te Kāhui Waka* waves live, **Debt $\le 42.0\%$ GDP (`41.7%` actual)**, and **$\ge 95\%$ J-curve paid off ($\le \text{NZD } 1.49\text{B}$ tail)**. Unlocks **`+NZD 190B` extra welfare** and hits the 60-year horizon **13.1 years early (`Year 46.9`)**!
  * *Catan Launch Strategy:* Track how many `16–20` Wedge Tailwinds and `B:09` Audit draws have occurred—and use `B:10` or `E:04` on Turn 4 to peek at unrevealed face-down Audit cards before staking `2 Mana` on a Turn-5 `Plan C` call!

### 5.3 Same Dollar Outlay, Opposite Economic Physics: The `3.0%` GDP Defense Stress Test (`H:09`)
Lifting defense spending from `~1.2%` to `3.0%` of GDP costs **`+1.8%` of GDP (`+NZD 8.0B/yr`)**—the **exact same gross annual outlay** as our 5-pillar `SS1` Generational Plan, except external military hardware carries a **`0x` domestic human-capital/TFP multiplier**:
* **Loaded onto an Unreformed `SS0` Hull:** Debt hits the **`200.0%` sovereign ceiling**, PAYE surges to **`30.68%`**, and national welfare collapses to **`-21.69% CE`**.
* **Carried on Coupled `SS2` Hydrofoils (`B:11 + B:14 + B:15`):** Aotearoa absorbs the entire `+NZD 8.0B/yr` defense levy in stride—achieving **`+21.18% CE` pre-NDC (`+42.87 pp` above `SS0`!)**, sinking Crown Debt from `42.0%` down to **`31.5%` of GDP**, and *still* cutting working-age PAYE to **`19.95%–20.65%`**!
# ==============================================================================
# FOILS & FOUNDERS STRATEGY & STUDY GUIDE — BATCH 3 (SECTIONS 6 & 7)
# ==============================================================================

---

## 6. *Chasing Finland+*: Cross-Country Out-of-Sample Calibration & Rival Ceilings (`P:07`)

Why can we trust that Aotearoa's simulated `+24.70% CE` (`SS2` pre-NDC), `-33.4%` Intergenerational Elasticity (IGE) compression, and `6.86x` 60-year GDP multiplier are achievable in the real world? Section 6.3 of `Document 2B` cross-validates every elasticity in our solver against **six historical and contemporary empirical episodes**—which double as your automated rival pace-boats in Solo and Co-Op *Chasing Finland+* race mode (`P:07`):

| Benchmark Vessel / Episode | What They Built (Active Foils) | Missing Foil / Structural Ceiling | Empirical Proof & Tabletop Pace-Boat Rule |
| :--- | :--- | :--- | :--- |
| **1. Finland & Sweden (`C:02`, `C:05`)** | Universal `1.6%–2.0%` GDP ECE, *Monilukutaito* media literacy (`#1` EU), & 1993 dual capital/labor tax. | High baseline labor tax rates without an explicit Age-20 Youth Capital Grant (`B:06`) or `1.5%` pure LVT. | Compresses earnings & dynastic shock variance by **`-52%`** (De Nardi 2004); `>80%` maternal employment. **Pace-boat cruises to `118.0`; Aotearoa overtakes to `126.0` in `SS2`!** |
| **2. Estonia (`1994–2025`, `B:08`)** | Pure **Land Value Tax** + **`0%` tax on reinvested firm equity** + universal kindergartens & 18-mo leave. | Smaller domestic scale (`1.37M` pop) & post-Soviet starting wealth base. | Propelled a small open economy to **`#1` in Europe in OECD PISA** with minimal socio-economic skill gaps—validating Guvenen (`B:08`) + Heckman (`B:01`)! |
| **3. Ireland, Singapore & Quebec (`B:06`, `N:08`)** | Ireland post-1967 tech/secondary + corp tax; Singapore CDA/Edusave (`E`) + ABSD land cooling; Quebec universal childcare. | Modern Dublin & Sydney/Melbourne omitted ongoing `B:08` LVT cooling once FDI surged. | Ireland reversed **150 years of youth emigration** (`\Pi_{\mathrm{mig}}`); Quebec childcare lifted maternal work `+7–8 pp` at **`>100%` fiscal self-financing** (Baker, Gruber, & Milligan 2008). |
| **4. Scotland (`2017–2026`, `T:08`)** | Doubled ECE (`600 -> 1,140 hrs`), *Scottish Child Payment* (`T_k`), & *MCR Pathways* mentoring (`B:03`). | **Lacks sovereign `B:07`/`B:08` Land & Estate Tax powers** under UK devolution (`PAYE -> 42%–48%`). | Cut AHC child poverty **`-6.0 pp` vs. rest of UK** (`21%` vs. `27%+`, `\Delta\ell_f \approx 0`), then **hard-stalled at `96.0`** (`3 pp` short of `18%` target) as uncooled rents absorbed transfers! |
| **5. South Korea (`T:09`)** | High private educational ambition & frontier industrial conglomerates. | **`3.10x` Seoul primate-city land squeeze** + weak public ECE wraparound + *Hagwon* arms race. | Marital fertility surplus $S_f(n_f)$ collapsed under $\beta_{\mathrm{hyp}} = 0.72$, driving **TFR down to `0.72–0.75`**—the exact warning facing `Q = 3.10` Auckland! |
| **6. Post-War -> 1989 Japan (`N:07` -> `T:10`)** | Deming's 1950 Mt. Hakone quality revolution + *Boshi Kenko Techo* First-2000-Days maternal health + post-1945 estate de-concentration. | **Omitted Rear T-Foil (`\tau_a = 0`, `B:08 + B:14/B:15`)** once tradable TFP growth $G_k$ exceeded $R(0)$. | Triggered **Hirano & Toda's (2025) Rational Land Bubble** ($B_{\mathrm{land},k,t} > 0$), culminating in 1989 Tokyo and 30 years of balance-sheet stagnation! Setting $\tau_a = 1.5\%$ forces $R_{\mathrm{eff}}(\tau_a) > G_k \Rightarrow B_{\mathrm{land}} \equiv 0$. |

---

## 7. Winning Playbooks by Wayfinder (`K:01–K:10`) & Master Suite-to-Codebase Index

### 7.1 Tactical Playbooks for All 10 *Kaupapa* Wayfinders
* **`K:01` Catalytic Steward (Barnardos / Iwi Early Years — `42.5%` Neighbor-Dependent):** Open Turn 1 by piloting Wave 1 (`Rural + Small`) of `B:01` + `B:03` at `50%` Political Drag to seed PDSA counters (`N:01`/`N:07`). Immediately co-stake Wedge `1x2` with `K:04` (to stop `H:06` from pricing *Kaiako* out of Auckland) and Wedge `1x4` with `K:07` (`B:09` Year-5 ACC audit).
* **`K:02` Pūrākau Weaver (Storyteller & Epistemic Guardian):** Guard the table's reform credibility ($\lambda_{\mathrm{cred}} \to 1$). Deploy `C:05` (*Monilukutaito*) early to neutralize `T:01` (*Disinformation Drag*), and sell `+2` Election Stability shields on Turns `3` and `6` in exchange for neighbor Mana co-stakes.
* **`K:03` Kaitiaki Māra Kai (Food-Medicine & Provincial Navigator):** Your signature engine is **`B:02` + `B:04` $\to$ `C:08` + `C:09` $\to$ `C:10`**. Pitch urban players on co-funding `C:09` (`1.60x–2.16x` food hubs) because retiring `85%` of `C:07` transfers hands *them* a `-0.64 pp` PAYE cut (`C:10`) while paying you `+2 Mana` Inverse-Hub Royalties!
* **`K:04` Whānau & Housing Justice Weaver (WellBeing — `43.8%` Neighbor-Dependent):** Pair `B:08` (`-10.5%` urban rent cooling) with `B:06` (`NZD 62k+` Youth Grant) and `E:01` (`CERF` Healthy Homes) to clear the `20%` LVR cliff (`Wedge 2 = +2.33% CE`). In `SS2`, link with `K:07` + `K:09` on `B:15` + `N:08` to unlock everyone's 3rd *Whānau* slot.
* **`K:05` Enterprise Wayfinder (GrowthNZ — `64.1%` Neighbor-Dependent):** Because nearly two-thirds of your score comes from neighbors (`Wedge 3 = +5.20% CE`!), **proactively bridge squeezed Waiter parents** so they never take `T:02` (*Hyperbolic Coerced-Shift Shortcut*, which dumps Skill-Shortage Liability Tokens onto your mat!). Rotate any `Nat 20` `z_l` land holdings into `z_h` firms via `B:08` to stay net positive up to `NZD 50M`.
* **`K:06` Fair-Markets & Tax-Compact Mediator:** Essential ally for exposed middle-hinge `Large` City players (`25.9%` pop). Tap Turn 1–2 to bind adjacent Regional Tax Keys under `C:06` (preventing `-60%` two-flank leakage under `T:06`) and pair with `C:08` to crush `H:08` grocery/bank/gentailer/supply cartels.
* **`K:07` Sovereign Helmsman (Treasury & RBNZ — `74.3%` Neighbor-Dependent):** Never play `T:03` (*Solve Debt First*, `-6.80% CE`). Authorize `B:09` at Turn 2 (`3.84x` Year-5 audit) to defeat `H:01` and draw bonus hidden `B:13` Compass cards; after `SS2` launch, lock `B:14` + `B:15` (`50/50` split) + `E:03` (`-60 to -100 bps` OCR cut) to sink debt to `21%–22%` and shrug off `H:09` (`3.0%` Defense Shock).
* **`K:08` '1925 Moment' Architect (Open-Source VFI Modeler):** Use `B:10` + `E:04` (*Thick vs. Thin Lens*) to cancel `T:03` austerity bluffs, re-roll fumbled `1–5` Additionality draws, peek at face-down `B:13` Audit cards before calling Turn-5 `Plan C`, and unlock `E:02` (`NZD 60.8B–91.5B` precautionary capital release) drag-free.
* **`K:09` Kaumātua & `K_whanau` Anchor:** Whenever you hold an active `Slot 3` Elder, monetize the `K_whanau` Pool via cross-table *Aunty's House* shields (`+2 Mana` Variant B Royalties per tap) and trade your free `1/turn` Experience Token to fund `N:01–N:08` or `E:02` at `0 Wealth`! Protect Super at 65 in `SS1` and champion **Age 64** in `SS2` (`+8.1%` care dividend).
* **`K:10` Kotahitanga & *Te Tiriti* Big Table Crew (Capstone Alliance):** Once 3+ Wayfinders cooperate, enact `K:10` to share Innate *Kaupapa* powers, cut Big-Table Political Drag (`3.0 -> 2.0 Wealth`), add `+4` to Political Stability rolls (locking out `T:07` permanently), and unlock `B:16` + `N:09` Mythic Victory!

### 7.2 Master 80-Card Suite-to-Codebase Architecture Map (`Files #1–#24`)

| Suite & Card Span | Card Count | A3 Game Sheets (`10-Up`) | A3 Study Sheets (`5-Up`) | Primary `IGWelfare` VFI Scripts (`Document 2B` §8 Manifest) |
| :--- | :---: | :---: | :---: | :--- |
| **Suite 1: Base Policy & Lifecycle (`B:00–B:16`)** | `17` | Sheets `1–2` (`#1–#17`) | Sheets `1–4` (`1:1`–`4:2`) | `ReturnFn_SpatialHH_Compact4D.m` (`#4`), `HumanCapital_Lifecycle_aprimeFn.m` (`#6`), `ReturnFn_Firm.m` (`#7`), `Plot_ChildFiscal_SSankey.m` (`#16`), `Plot_Doc1D_LaunchPlans.m` (`#23`). |
| **Suite 2: Cautionary Traps (`T:00–T:10`)** | `11` | Sheets `2–3` (`#18–#28`) | Sheets `4–6` (`4:3`–`6:3`) | `FertilityBargaining_Module.m` (`#13`), `Counterfactuals_LeeSeshadri_4Region.m` (`#12`), `Plot_Doc3_CoalitionSynergies_And_LTFMSinkhole.m` (`#22`). |
| **Suite 3: Macro Resilience & Spatial (`C:01–C:10`)** | `10` | Sheets `3–4` (`#29–#38`) | Sheets `6–8` (`6:4`–`8:3`) | `Build_IntergenTransitionMatrix.m` (`#8`), `Solve_Spatial_GE_Loop.m` (`#9`), `WelfareDecomposition_4Region.m` (`#11`), `Doc 2T` §4.5 (`\Delta\mu_{z,k}`). |
| **Suite 4: *Kaupapa* Wayfinders (`K:01–K:10`)** | `10` | Sheets `4–5` (`#39–#48`) | Sheets `8–10` (`8:4`–`10:3`) | `Plot_WealthBracket_GiveAndGain.m` (`#20`), `Plot_Doc3_CoalitionSynergies_And_LTFMSinkhole.m` (`#22`), `Document 2T` §4.1–4.4 (`K_whanau^net`, `M_trust`). |
| **Suite 5: Nobel & Learning Engines (`N:01–N:09`)** | `9` | Sheets `5–6` (`#49–#57`) | Sheets `10–12` (`10:4`–`12:2`) | `Plot_Doc1D_TeKahuiWakaSequencing.m` (`#24`), `Plot_ActuarialContinuationValuation.m` (`#17`), `FertilityBargaining_Module.m` (`#13`). |
| **Suite 6: Orthodoxy Boss Deck (`H:01–H:10`)** | `10` | Sheets `6–7` (`#58–#67`) | Sheets `12–14` (`12:3`–`14:2`) | `Audit_GUiNZ_vs_Dunedin_4Region.m` (`#17`), `Plot_Fertility_SuperSolvency_2Panel.m` (`#18`), `Plot_Doc3_CoalitionSynergies_And_LTFMSinkhole.m` (`#22`). |
| **Suite 7: Energy & Proof Operators (`E:01–E:05`)** | `5` | Sheets `7–8` (`#68–#72`) | Sheets `14–15` (`14:3`–`15:2`) | `QEA_2026.m`, `Configure_TimeGrid_Params.m` (`#2`), `Build_IntergenTransitionMatrix.m` (`#8`, `Doc 2A` §4.4 Convex Mixing), `Document 2T`. |
| **Suite 8: Open-Source Wildcards (`P:01–P:08`)** | `8` | Sheet `8` (`#73–#80`) | Sheets `15–16` (`15:3`–`16:5`) | `Run_All_NZ_Intergen_Suite.m` (`#1`), `Build_Phase_Registry.m` (`#3`), `Calibrate_NZ_Moments.m` (`#10`), `exportSankeyToHTML.m` (`#21`). |
