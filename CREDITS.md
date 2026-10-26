## Game Legend & Credits: Why I Know This Game Works in the Real World

In 1987, getting a compiler to generate code for a new microprocessor architecture cost millions of dollars and took years to accomplish. I found that I could port the GNU C compiler to a new architecture in a matter of weeks (and later days, and sometimes hours), generating code that outperformed the vendor's own compiler. I was convinced that such a competitive advantage warranted commercial success, but the idea was absolutely rejected by the economic and entrepreneurial orthodoxy of the day, for two reasons:

1. *"Nobody will pay money for free software."*
2. *"Everybody knows it's illegal to use the Internet for commerce—only research."*

The fact that nobody thought it would succeed (after I pitched the idea for two years) convinced me that we would have no competition—and with no competition, how could we lose? With that confidence, I recruited two co-founders who went "all-in" with me, each matching the USD 2,000 that was all the money in my checking account.

We bent the curve in two ways: (1) I argued that as a Stanford graduate student, it was legitimate research to test whether we could bootstrap a company selling support for free software using the Internet for support and distribution (`B:04`), and (2) we positioned the company—Cygnus Support—with the tagline: *"We make free software affordable"* (`N:01`).

When we started Cygnus in 1989, I used to joke—in all seriousness—that someday an economist would win the Nobel Prize for explaining the theoretical basis of why our company worked. As I later detailed in *The (awesome) economics of open source*, open source exceeded expectations yet again when not one, but four Nobel Prizes in Economics validated the exact mechanisms we were pioneering in practice:
* By removing artificial barriers and optimizing transaction costs and institutional governance, we were realizing the theories of **Ronald Coase (Nobel Prize, 1991 — Card `N:01`)** and **Oliver Williamson (Nobel Prize, 2009 — Card `N:03`)**.
* Even more importantly, open source proved the power of polycentric, community-led governance of the commons—the foundational insight for which **Elinor Ostrom (Nobel Prize, 2009 — Card `N:04`)** shared the 2009 prize with Williamson. Together, those governance principles provided an architecture for enabling the collective intelligence of the world to work together: an extraordinary force-multiplier that allowed our scrappy company and the global community to build vast libraries of software that have powered multiple scientific and commercial revolutions, artificial intelligence among them.
* While I knew open source was an engine for compounding knowledge capacity, I didn't realize at the time that proving the economics of endogenous, non-rival knowledge creation would also win a Nobel Prize—awarded to **Paul Romer (Nobel Prize, 2018 — Card `N:05`)** in October 2018, just three weeks after my article was published.
* When paired with **James Heckman's (Nobel Prize, 2000 — Card `N:02`)** proof of dynamic complementarity in early human capability formation, the five pieces of the puzzle snap together (`N:06`).

We founded Cygnus with USD 6,000, and 10 years later sold it to Red Hat for well over USD 600M. Twenty years after that, Red Hat sold to IBM for USD 34B, and IBM's stock price has since doubled. Together, we pioneered the business model for open source, which became the rocket fuel that powered the Internet into the orbit of the mainstream.

I share this legend not to look back, but because I see the exact same "1925 Moment" (`B:08`) in front of Aotearoa New Zealand today. Stepping outside established orthodoxy takes real courage—living a new life always costs you the old one. For decades, New Zealand's Treasury and Reserve Bank have been asked to manage an abysmal status quo (`SS0`) using restrictive cash-flow accounting and monetary frameworks that treat human capability as a sunk cost and austerity as prudence (`H:01`–`H:05`). That is a recipe for floundering in heavy seas.  But we have the power of knowledge and the evidence of history to turn our sinking ship into a flying success.  Consider:

### Equation 1: Multi-Stage CES Human-Capability Formation Under Non-Homothetic Subsistence Corners
*(Full mathematical derivation in **Document 1B, Section 2** and **Document 2: `PolicyExperiment_LeeSeshadri_4Region.m`**)*

In the GPU engine, a family in region $r \in \{\text{Rural, Small, Large, Auckland}\}$ at lifecycle gate $j$ with liquid assets $a$, human capital $h_j$, entrepreneurial type $z \in \{z_\ell, z_h\}$, and AR(1) energy shock $z_2$ solves the coupled Bellman and Constant-Elasticity-of-Substitution (CES) skill-technology system:

$$V_j^r(a, h_j, z, z_2) = \max_{c, i_c, \ell, a', pv'} \left\{ \frac{\left( \left(c - \bar{c}_r(z_2, pv)\right)^\nu (1 - \ell - \tau_c)^{1-\nu} \right)^{1-\sigma}}{1-\sigma} + \beta \psi_j \mathbb{E}\left[ V_{j+1}^r(a', h_{j+1}, z', z_2') \;\middle|\; z, z_2 \right] + \theta_{\text{child}} V_{\text{launch}}(h_{\text{adult}}, a_{\text{seed}}) \right\}$$

subject to the **Cunha–Heckman–Schennach (2010) / Lee–Seshadri (2019) Two-Gate CES Technology of Skill Formation**:

$$h_{j+1} = A_j \left[ \gamma_j h_j^{\phi_j} + (1 - \gamma_j) \left( \underbrace{G_{\text{ECE}, j}^{\text{in-kind}}}_{\text{Card B:01 / B:02}} + \kappa_j \max\left\{0,\; i_c(y_j - p_h^r \bar{h} - p_e(z_2))\right\} + \omega_j \tau_c w_j h_j \right)^{\phi_j} \right]^{\frac{\rho_j}{\phi_j}}, \qquad \frac{\partial^2 h_{\text{adult}}}{\partial h_{\text{Gate 1}} \, \partial I_{\text{Gate 2}}} > 0 \quad (\phi_1 < 0 < \phi_2)$$

#### What That Equation Actually Means at the Table $\rightarrow$ Play **`B:01` + `N:02`**

| What the Math Says (Document 1B / Document 2) | How You Play It on the Table (`B:01` + `N:02` Synergy) |
| :--- | :--- |
| **1. The Stone–Geary Subsistence Corner ($\bar{c}_r$, $i_c = 0$):** When metropolitan rent ($p_h^r \bar{h}$) and energy shocks ($p_e(z_2)$) swallow a low-income family's cash, private early-childhood investment hits a hard zero corner ($i_c = 0$), trapping **22.0% of the cohort** in stunted adult trajectories ($h_1\text{–}h_2$) that drive **57%–81%** of adult hospital, care, and prison costs (`Exits 1, 2, 4`). | **Play `B:01` (*Tamariki of the First 2000 Days*):** Spend `NZD 13.0k/yr` of **in-kind** wraparound ($G_{\text{ECE}, 1}^{\text{in-kind}}$—*Te Korowai Mokopuna* & *Whānau Ora*) to bypass the parent's rent-crushed cash constraint directly. Remove all *Stunted Trajectory* tokens from the bottom 4 vigintiles (`1–4` on the `d20`). |
| **2. Dynamic Complementarity ($\partial^2 h_{\text{adult}} / \partial h_1 \partial I_2 > 0$):** Because early elasticity of substitution is complementary ($\phi_1 < 0$), a child who clears Gate 1 with high readiness ($h_1$) raises the marginal productivity of **every** subsequent dollar of schooling, *Tuakana–Teina* mentoring (`B:02`), and parental time ($\tau_c$). | **Combo with `N:02` (*Heckman's Dynamic Complementarity Engine*):** Place a *Readiness Counter* on your `B:01` cohort. It now gains **3x the skill payoff** from Gate 2 mentoring (`B:02`) and automatically **Crowds In `+NZD 15.3k` of Private Parental Care (`NZD 8.7k` cash + `NZD 6.5k` time) for free**! |

---

### Equation 2: The Guvenen–MSV–QEA Stationary Distribution & Precautionary Capital Release
*(Full mathematical derivation in **Document 1B, Section 4** and **Document 2: `QEA_2026.m` & `NZ_4Region_Master.m`**)*

At the macroeconomic level, the stationary distribution $\mu^*(a, pv, ks, h, z, z_2, j)$ across all 81 lifecycle ages and 10 wealth tiers (`P01` to `P99.99`) is governed by the coupled **Guvenen et al. (2023) / Murphy–Shleifer–Vishny (1991) Occupational-Return Split** and the **Precautionary Buffer Release Identity**:

$$r_{\text{after-tax}}(z, \tau_a, \tau_{\text{corp}}) = (1 - \tau_{\text{corp}}) z_h k^{\alpha - 1} + z_\ell \left(\frac{\dot{P}_L}{P_L}\right) - \tau_a \quad \Longrightarrow \quad A^*(\tau_a) \downarrow \implies \int_{A^*}^{\bar{A}} dF(A) \text{ shifts from } z_\ell \text{ (Rent-Seeking) to } z_h \text{ (Builders)}$$

coupled with the **Second-Order Precautionary Capital Release ($\Delta A_{\text{prec}}$)** across the stationary distribution $\mu^*$ when unbounded AR(1) fossil-fuel volatility ($\sigma_{\epsilon, z_2}^2 > 0$) is replaced by a Solar + Battery Endowment ($pv = 5 \implies \sigma_{\epsilon, z_2}^2 \to 0$):

$$\Delta A_{\text{prec}} \equiv \int_{\mathcal{S}} a \, d\mu^*\big(s \;\big|\; pv = 0, \sigma_{z_2} = 0.25\big) - \int_{\mathcal{S}} a \, d\mu^*\big(s \;\big|\; pv = 5, \sigma_{z_2} = 0\big) = \text{NZD } 60.8\text{B–}91.5\text{B} \;\ge\; \sum_{m=1}^{5} \text{CapEx}_m \text{ (NZD } 60.2\text{B–}75.5\text{B)}$$

#### What That Equation Actually Means at the Table $\rightarrow$ Play **`B:05` + `E:02`**

| What the Math Says (Document 1B / Document 2) | How You Play It on the Table (`B:05` + `E:02` Synergy) |
| :--- | :--- |
| **1. The Guvenen "Use-It-Or-Lose-It" & MSV Talent Flip ($z_\ell \to z_h$):** Taxing book-value land/wealth (`1.5%`) and estates (`25% -> 18%`) penalizes low-yield passive land hoarding ($z_\ell$, deflating urban housing stress by `-10.5%` and curing the Lavoisier Trap `T:04`) while rewarding high-return active builders ($z_h$), who stay **net welfare positive across 19 of 20 Top-5% slices (`20:01`–`20:19`, up to `NZD 100M` net worth)**! | **Play `B:05` (*Use-It-Or-Lose-It Rebalancer*):** Rotate the opponent's **NZD 1.6 Trillion Dormant Property Hoard** out of passive land speculation (`z_l`) into high-wage operating firms (`z_h`). Lift real regional wages by **`+3.2% to +9.6%`**, retain `3,550/yr` young graduates (`B:03`), and cut working-age PAYE taxes to **`18.5%`** (`B:06`). |
| **2. The Precautionary Self-Financing Theorem ($\Delta A_{\text{prec}} \ge \text{CapEx}$):** In incomplete markets (`sigma = 2.2`), households and firms hoard `NZD 60.8B–91.5B` in sterile cash buffers just to self-insure against fossil-fuel price spikes ($z_2$). Turning energy into a solar + battery endowment ($pv = 5$) eliminates $z_2$ tail-risk, releasing more than 100% of the capital needed to electrify all 5 sectors! | **Combo with `E:02` (*Energy as Endowment*):** Unlock **`NZD 60.8B–91.5B` in trapped precautionary buffers** across households, schools/marae, firms, farms, and transport—self-financing the entire `NZD 60.2B–75.5B` national electrification CapEx (`+NZD 15.55B/yr` cash savings and `-60 to -100 bps` lower RBNZ interest rates via `E:03`) with **zero crowd-out of `B:01` child investment**! |

> **Want to inspect the full derivations or run the GPU code yourself?**
> * **For the Formal Econometric & OLG Derivations:** Head over to **Document 1B (*Technical & Econometric Appendix*)** in [`github.com/MichaelTiemann/IGWelfare`](https://github.com/MichaelTiemann/IGWelfare).
> * **For the Executable VFI Toolkit GPU Code (`MATLAB` / RTX 5090):** Head over to **Document 2 (*`NZ_4Region_Master.m`, `PolicyExperiment_LeeSeshadri_4Region.m`, & `QEA_2026.m`*)** in [`github.com/MichaelTiemann/IGWelfare`](https://github.com/MichaelTiemann/IGWelfare).

In policy terms, this requires a few simple changes: adopting ACC-style actuarial accounting (`B:07`) for all social welfare investments—paired with a "use-it-or-lose-it" capital rebalance (`B:05`), firming the economic grid (`E:02`–`E:03`), and establishing Ostrom-style trust in community-led governance (*Whānau Ora*, Iwi and community trusts, and *Tuakana–Teina* mentoring, `K:01`–`K:07`) to give Treasury, the Reserve Bank, and our communities the tools and the permission to escape the orthodoxy of austerity and get Aotearoa up on foils.

Just as open source unlocked the collective intelligence of programmers worldwide by removing transaction-cost drag, lifting every child out of early stunting (`B:01`) and retaining our brightest young minds (`B:03`) unlocks the compounding collective intelligence of an entire nation. That is why **Foils & Founders: The Aotearoa Deck** is released as an open-source game under **CC BY-SA 4.0**: we invite you not just to play the cards on the table, but to inspect the code, roll the Rawlsian d20 (`B:00`), and submit your own Pull Requests to help steer the vessel. When the math is right and the time is right, enormous change is not only possible, it is good, and it is sustainable.
