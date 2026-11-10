# Game Legend & Credits: Why I Know This Game Works in the Real World

In 1987, getting a compiler to generate code for a new microprocessor architecture cost millions of dollars and took years to accomplish. I found that I could port the GNU C compiler to a new architecture in a matter of weeks (and later days, and sometimes hours), generating code that outperformed the vendor's own compiler. I was convinced that such a competitive advantage warranted commercial success, but the idea was absolutely rejected by the economic and entrepreneurial orthodoxy of the day, for two reasons:

1. *"Nobody will pay money for free software."*
2. *"Everybody knows it's illegal to use the Internet for commerce—only research."*

The fact that nobody thought it would succeed (after I pitched the idea for two years) convinced me that we would have no competition—and with no competition, how could we lose? With that confidence, I recruited two co-founders who went "all-in" with me, each matching the USD 2,000 that was all the money in my checking account.

We bent the curve in two ways: (1) I argued that as a Stanford graduate student, it was legitimate research to test whether we could bootstrap a company selling support for free software using the Internet for support and distribution ([`B:11`](rules/rules.md)), and (2) we positioned the company—Cygnus Support—with the tagline: ***"We make Free Software affordable"*** ([`N:02`](rules/rules.md)).

When we started Cygnus in 1989, I used to joke—in all seriousness—that someday an economist would win the Nobel Prize for explaining the theoretical basis of why our company worked. As I later detailed in [*The (awesome) economics of open source*](https://opensource.com/article/18/9/awesome-economics-open-source), open source exceeded expectations yet again when not one, but four Nobel Prizes in Economics validated the exact mechanisms we were pioneering in practice:

* By removing artificial barriers and optimizing transaction costs and institutional governance, we were realizing the theories of **Ronald Coase (Nobel Prize, 1991 — Card [`N:02`](rules/rules.md))** and **Oliver Williamson (Nobel Prize, 2009 — Card [`N:04`](rules/rules.md))**.
* Even more importantly, open source proved the power of polycentric, community-led governance of the commons—the foundational insight for which **Elinor Ostrom (Nobel Prize, 2009 — Card [`N:05`](rules/rules.md))** shared the 2009 prize with Williamson. Together, those governance principles provided an architecture for enabling the collective intelligence of the world to work together: an extraordinary force-multiplier that allowed our scrappy company and the global community to build vast libraries of software that have powered multiple scientific and commercial revolutions, artificial intelligence among them.
* While I knew open source was an engine for compounding knowledge capacity, I didn't realize at the time that proving the economics of endogenous, non-rival knowledge creation would also win a Nobel Prize—awarded to **Paul Romer (Nobel Prize, 2018 — Card [`N:06`](rules/rules.md))** in October 2018, just three weeks after my article was published.
* When paired with **James Heckman's (Nobel Prize, 2000 — Card [`N:03`](rules/rules.md))** proof of dynamic complementarity in early human capability formation, the pieces of the puzzle—joined by **Kenneth Arrow's Learning-by-Doing (`N:01`)**, **Deming–Fixsen Staffing Cycles (`N:07`)**, and **Doepke–Kindermann Fertility Bargaining (`N:08`)**—snap together ([`N:09`](rules/rules.md)).

We founded Cygnus with USD 6,000, and 10 years later sold it to Red Hat for well over USD 600M. Twenty years after that, Red Hat sold to IBM for USD 34B, and IBM's stock price has since doubled. Together, we pioneered the business model for open source, which became the rocket fuel that powered the Internet into the orbit of the mainstream.

---

## We Make Affordable Economics Understandable

I share this legend not to look back, but because I see the exact same **"1925 Moment" ([`B:10`](rules/rules.md), `K:08`)** in front of Aotearoa New Zealand today. Stepping outside established orthodoxy takes real courage—living a new life always costs you the old one. For decades, New Zealand's Treasury and Reserve Bank have been asked to manage an abysmal status quo (`SS0`) using restrictive cash-flow accounting and monetary frameworks that treat human capability as a sunk cost and austerity as prudence ([`H:01`–`H:10`](rules/rules.md)). That is a recipe for floundering in heavy seas.

But we have the power of knowledge and the evidence of history to turn our sinking ship into a flying success—by **making affordable economics understandable**. Consider the two hardest general-equilibrium equations in our GPU solver ([**Documents 1B, 2A, 2B, and 2T**](https://github.com/MichaelTiemann/IGWelfare)), and see how *Foils & Founders* compiles each into a **30-second Two-Card Tabletop Synergy**:

### Equation 1: Multi-Stage CES Human-Capability Formation Under Non-Homothetic Subsistence Corners
*(Full mathematical derivation in **Document 1B, Section 2** and **Document 2A/2B: [`HumanCapital_Lifecycle_aprimeFn.m`](https://github.com/MichaelTiemann/IGWelfare) & [`Counterfactuals_LeeSeshadri_4Region.m`](https://github.com/MichaelTiemann/IGWelfare)**)*

In the GPU engine, a family in region $r \in \{\text{Rural, Small, Large, Auckland}\}$ at lifecycle gate $j$ with liquid assets $a$, human capital $h_j$, entrepreneurial type $z \in \{z_\ell, z_h\}$, and AR(1) energy shock $z_2$ solves the coupled Bellman and Constant-Elasticity-of-Substitution (CES) skill-technology system:

$$
V_j^r(a, h_j, z, z_2) = \max_{c, i_c, \ell, a', pv'} \left[ \frac{\left( \left(c - \bar{c}_r(z_2, pv)\right)^\nu (1 - \ell - \tau_c)^{1-\nu} \right)^{1-\sigma}}{1-\sigma} + \beta \psi_j \mathbb{E}\left[ V_{j+1}^r(a', h_{j+1}, z', z_2') \;\middle|\; z, z_2 \right] + \theta_{\text{child}} V_{\text{launch}}(h_{\text{adult}}, a_{\text{seed}}) \right]
$$

subject to the **Cunha–Heckman–Schennach (2010) / Lee–Seshadri (2019) Two-Gate CES Technology of Skill Formation**:

$$
h_{j+1} = A_j \left[ \gamma_j h_j^{\phi_j} + (1 - \gamma_j) \left( \underbrace{G_{\text{ECE}, j}^{\text{in-kind}}}_{\text{Card B:01 / B:03}} + \kappa_j \max\big(0,\; i_c(y_j - p_h^r \bar{h} - p_e(z_2))\big) + \omega_j \tau_c w_j h_j \right)^{\phi_j} \right]^{\frac{\rho_j}{\phi_j}}, \qquad \frac{\partial^2 h_{\text{adult}}}{\partial h_{\text{Gate 1}} \, \partial I_{\text{Gate 2}}} > 0 \quad (\varphi_1 = +0.35 > 0,\; \varphi_2 = -0.95 < 0)
$$

#### What That Equation Actually Means at the Table $\rightarrow$ Play [`B:01`](rules/rules.md) + [`B:03`](rules/rules.md) + [`N:03`](rules/rules.md)

| What the Math Says (Document 1B / Document 2) | How You Play It on the Table (`B:01` + `B:03` + `N:03` Dual-Gate Synergy) |
| :--- | :--- |
| **1. The Stone–Geary Subsistence Corner ($\bar{c}_r$, $i_c = 0$):** When metropolitan rent ($p_h^r \bar{h}$) and energy shocks ($p_e$) swallow a low-income family's cash, private early-childhood investment hits a hard zero corner ($i_c = 0$), trapping **22.0% of the cohort** in struggling adult trajectories ($h_1\text{–}h_2$, reduced foundational skills) that drive **57%–81%** of adult hospital, care, and prison costs (`Exits 1, 2, 4`). | **Play [`B:01` (*He Kākano i Rangiātea — Tamariki of the First 2000 Days*)](rules/rules.md):** Spend `NZD 13.0k/yr` of **in-kind** wraparound ($G_{\text{ECE}, 1}$—*Te Korowai Mokopuna* & *Whānau Ora*) to bypass the parent's rent-crushed cash constraint directly. Prevent *Struggling Trajectory* (`h1–h2`) tokens from the bottom 4 vigintiles (`1–4` on the `d20`; see [`decks/nat_1.md`](decks/nat_1.md)). |
| **2. Dynamic Complementarity ($\partial^2 h_{\text{adult}} / \partial h_1 \partial I_2 > 0$):** Because Stage 1 is malleable ($\varphi_1 = +0.35$) while Stage 2 is a strict harmonic bottleneck ($\varphi_2 = -0.95$), clearing Gate 1 with high readiness raises the marginal productivity of **every** subsequent dollar of schooling, *Tuakana–Teina* mentoring (`B:03`), and parental time (`Wedge 1 = +3.32% CE`). | **Combo with [`N:03` (*Heckman's Dynamic Complementarity Engine*)](rules/rules.md):** Place a *Readiness Counter* on your `B:01` cohort. It now gains **3x the skill payoff** from Gate 2–3 mentoring (`B:03`) and automatically **Crowds In `+NZD 15.3k` of Private Parental Care (`NZD 8.7k` cash + `NZD 6.5k` time) for free**! |

---

### Equation 2: The Guvenen–MSV–QEA Stationary Distribution & Precautionary Capital Release
*(Full mathematical derivation in **Document 1B, Section 4** and **Document 2: [`QEA_2026.m`](https://github.com/MichaelTiemann/IGWelfare/blob/main/QEA_2026.m) & [`NZ_4Region_Master.m`](https://github.com/MichaelTiemann/IGWelfare/blob/main/NZ_4Region_Master.m)**)*

At the macroeconomic level, the stationary distribution $\mu^\star(a, pv, ks, h, z, z_2, j)$ across all 81 lifecycle ages and 10 wealth tiers (`P01` to `P99.99`) is governed by the coupled **Guvenen et al. (2023) / Murphy–Shleifer–Vishny (1991) Occupational-Return Split** and the **Precautionary Buffer Release Identity**:

$$
r_{\text{after-tax}}(z, \tau_a, \tau_{\text{corp}}) = (1 - \tau_{\text{corp}}) z_h k^{\alpha - 1} + z_\ell \left(\frac{\dot{P}_L}{P_L}\right) - \tau_a \quad \Longrightarrow \quad A^\star(\tau_a) \downarrow \implies \int_{A^\star}^{\bar{A}} dF(A) \text{ shifts from } z_\ell \text{ (Rent-Seeking) to } z_h \text{ (Builders)}
$$

coupled with the **Second-Order Precautionary Capital Release ($\Delta A_{\text{prec}}$)** across the stationary distribution $\mu^\star$ when unbounded AR(1) fossil-fuel volatility ($\sigma_{z_2} = 0.25$) is replaced by a Solar + Battery Endowment ($pv = 5 \implies \sigma_{z_2} \to 0$):

$$
\Delta A_{\text{prec}} \equiv \int_{\mathcal{S}} a \, d\mu^\star\big(s \;\big|\; pv = 0, \sigma_{z_2} = 0.25\big) - \int_{\mathcal{S}} a \, d\mu^\star\big(s \;\big|\; pv = 5, \sigma_{z_2} = 0\big) = \text{NZD } 60.8\text{B–}91.5\text{B} \;\ge\; \sum_{m=1}^{5} \text{CapEx}_m \text{ (NZD } 60.2\text{B–}75.5\text{B)}
$$

#### What That Equation Actually Means at the Table $\rightarrow$ Play [`B:08`](rules/rules.md) + [`E:02`](rules/rules.md)

| What the Math Says (Document 1B / Document 2) | How You Play It on the Table (`B:08` + `E:02` Capital Reallocation Synergy) |
| :--- | :--- |
| **1. The Guvenen "Use-It-Or-Lose-It" & MSV Talent Flip ($z_\ell \to z_h$):** Taxing book-value land/wealth (`1.5%`) and estates (`25% -> 18%`) penalizes low-yield passive land hoarding ($z_\ell$, deflating urban housing stress by `-10.5%` and curing the Lavoisier Trap [`T:05`](rules/rules.md)) while rewarding high-return active builders ($z_h$), who stay **net welfare positive across 19 of 20 Top-5% slices (`20:01`–`20:19`, through the `NZD 50M` IRD High-Wealth median at `+1.2% CE`, breaking even at the `NZD 140M` Rich List median; see [`decks/nat_20.md`](decks/nat_20.md))**! | **Play [`B:08` (*Use-It-Or-Lose-It LVT & Corporate Tax Lockstep*)](rules/rules.md):** Rotate the opponent's **NZD 1.6 Trillion Dormant Property Hoard** out of passive land speculation ($z_\ell$) into high-wage operating firms ($z_h$). Lift real regional wages by **`+3.2% to +9.6%`**, retain `3,550/yr` young graduates (`B:05`/`B:06`), and cut working-age PAYE taxes to **`18.25%`** while lowering Universal NZ Super to **Age 64** (`B:15` + `C:10`). |
| **2. The Precautionary Self-Financing Theorem ($\Delta A_{\text{prec}} \ge \text{CapEx}$):** In incomplete markets ($\sigma = 2.2$), households and firms hoard `NZD 60.8B–91.5B` in sterile cash buffers just to self-insure against fossil-fuel price spikes ($z_2$). Turning energy into a solar + battery endowment ($pv = 5$) eliminates $z_2$ tail-risk, releasing more than 100% of the capital needed to electrify all 5 sectors! | **Combo with [`E:02` (*Energy as Endowment*)](rules/game_changer_tutorial.md#e02--energy-as-endowment-the-qea-2026-stationary-distribution-shift):** Unlock **`NZD 60.8B–91.5B` in trapped precautionary buffers** across households, schools/marae, firms, farms, and transport—self-financing the entire `NZD 60.2B–75.5B` national electrification CapEx (`+NZD 15.55B/yr` cash savings and `-60 to -100 bps` lower RBNZ interest rates via [`E:03`](rules/game_changer_tutorial.md#e03--firming-the-economic-grid-the-rbnz--national-security-dividend)) with **zero crowd-out of `B:01` child investment**! |

> **Want to inspect the full derivations or run the GPU code yourself?**
> * **For the Formal Econometric & OLG Derivations:** Head over to **Document 1B (*Technical & Econometric Appendix*)** in [`github.com/MichaelTiemann/IGWelfare`](https://github.com/MichaelTiemann/IGWelfare).
> * **For the Executable VFI Toolkit GPU Code (`MATLAB` / RTX 5090):** Head over to **Documents 2A, 2B, & 2T (*24-file GPU VFI Toolkit Suite: `Run_All_NZ_Intergen_Suite.m`, `ReturnFn_SpatialHH_Compact4D.m`, `Build_IntergenTransitionMatrix.m`, & `QEA_2026.m`*)** in [`github.com/MichaelTiemann/IGWelfare`](https://github.com/MichaelTiemann/IGWelfare).
> * **Want to "Play the Nerd Card" at the physical table?** Render the **Fold-Over Study Deck** ([`decks/study_cards.yaml`](decks/study_cards.yaml) via [`scripts/render_study_cards.py`](scripts/render_study_cards.py))—putting the exact MathJax Bellman/CES/KFE equation, calibrated parameters, tabletop proof bridge, and peer-reviewed academic citations on the landscape back of every single card in the 80-card deck (16 A3 fold-over sheets)!  The maths and the science is the card art!

---

In policy terms, this requires a few simple changes: adopting ACC-style actuarial accounting ([`B:09`](rules/rules.md)) for all social welfare investments—paired with a "use-it-or-lose-it" capital rebalance ([`B:08`](rules/rules.md)), firming the economic grid ([`E:02`–`E:03`](rules/game_changer_tutorial.md)), and establishing Ostrom-style trust in community-led governance (*Whānau Ora*, Iwi and community trusts, and *Tuakana–Teina* mentoring, [`K:01`–`K:10`](rules/rules.md)) to give Treasury, the Reserve Bank, and our communities the tools and the permission to escape the orthodoxy of austerity and get Aotearoa up on foils.

Just as open source unlocked the collective intelligence of programmers worldwide by removing transaction-cost drag, lifting every child out of the early hardship corner ([`B:01`](rules/rules.md)) and retaining our brightest young minds ([`B:05`/`B:06`](rules/rules.md)) unlocks the compounding collective intelligence of an entire nation. That is why ***Foils & Founders: The Aotearoa Deck*** is released as an open-source game under **CC BY-SA 4.0**: we invite you not just to play the cards on the table, but to inspect the code, roll the Rawlsian d20 ([`B:00`](rules/rules.md)), and submit your own Pull Requests to help steer the vessel. When the math is right and the time is right, enormous change is not only possible, it is good, and it is sustainable.
