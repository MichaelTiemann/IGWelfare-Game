# Foils & Founders Strategy & Empirical Study Guide: Knowledge Is Power!

> *"Knowledge is not cheating; Knowledge is power!"*  
> *"Not all lives are easy, but none should be impossible."*

*Companion Strategy & Mathematical Reference to **Foils & Founders: The Aotearoa Deck***  
**Cross-References:** `decks/study_cards.yaml` • `Document 1A` • `Document 1B` • `Document 1C` • `Document 2 (MATLAB GPU Engine)`

---

## 1. Why Knowing the Math Wins the Game

In **Foils & Founders**, every tabletop mechanic is compiled directly from an empirical theorem or general-equilibrium operator in the **8-PType $\times$ 4-Region Overlapping Generations (OLG) GPU Engine** (`NZ_4Region_Master.m`, `PolicyExperiment_LeeSeshadri_4Region.m`, and `QEA_2026.m`).

Players who study the **Fold-Over Study Deck (`decks/study_cards.yaml`)** gain three decisive advantages:
1. They know **which cards are high-frequency royalty hubs** (`Tier 1`) versus **high-multiplier finishers** (`Tier 3`).
2. They know **how to shrink the D20 Vulnerability Window from 40% to 0%** ("making their own luck") and how to Judo-counter a "Feral" spoiler player.
3. They know how to manage the **Kaumātua mortality cliff** at Age 90 ($j=30$) and scale tactics from a 2-player duel up to a 6-player Big Table (`K:07`).

---

## 2. The Mathematics of the River & Inverse-Hub Mana Pricing

### 2.1 Why Variant B Persists: Romer's Non-Rival Knowledge Theorem (`N:05`)
Why do enacted River cards stay face-up in front of their owner to anchor future combinations instead of being consumed? Because proven policy architectures are **non-rival ideas** ($A_t$). By Paul Romer's (1990, Nobel Prize 2018) endogenous growth equation (`N:05` in `decks/study_cards.yaml`):

$$Y_t = A_t K_t^\alpha \big(L_{Y,t} \bar{h}_t\big)^{1-\alpha}, \qquad \frac{\dot{A}_t}{A_t} = \delta_{\text{R\&D}} \, H_{A,t}\big(\text{B:03}, \text{B:05}, \text{K:06}\big) \implies \frac{\partial^2 Y_t}{\partial A_t \, \partial H_{A,t}} > 0$$

### 2.2 Inverse-Hub Pricing & Monte Carlo Strategy Audit ($N = 10,000$ Games)
Pricing Base Mana ($m_i$) inversely to a card's network connectivity degree $d(i)$ equalizes the expected lifetime Mana of early co-operators and late finishers:

| Strategy Persona | Mean Mana ($\mathcal{M}_i$) | Mana Sources (Init / Royalty / Legacy / Forfeit) | Mean Wealth ($\mathcal{W}_i$) | Mana Win % | Wealth Win % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Catalytic Hub Builder (`K:01`/`K:05`)** *(Exposes `B:01`, `B:02`, `B:05` Turns 1–4)* | **44.2 Mana** | $14.1$ Init + **$25.8$ Royalties** + $5.0$ Legacy $- 0.7$ Forfeit | **31.4 Wealth** | **41.8%** | 19.4% |
| **2. Capstone Finisher (`K:02`/`K:03`)** *(Times Tier 2/3 cards on $\mu=2\times, 3\times$ turns)* | **45.1 Mana** | **$36.4$ Init** + $9.9$ Royalties + $0.0$ Legacy $- 1.2$ Forfeit | **34.8 Wealth** | **44.6%** | **38.2%** |
| **3. Shielded Arbitrageur (`K:04`/`K:06`)** *(Anchors `B:07`/`N` shields & elder `K:06` tokens)* | **38.6 Mana** | $21.2$ Init + $16.4$ Royalties + $2.5$ Legacy $- 1.5$ Forfeit | **36.1 Wealth** | 13.4% | **40.1%** |
| **4. Free-Riding Bystander / Unchecked Feral** *(Withholds stakes or plays countered Traps)* | **6.8 Mana** | $4.5$ Init + $9.1$ Royalties + $0.0$ Legacy **$- 6.8$ Forfeit** | **24.2 Wealth** | **0.2%** | 2.3% |

---

## 3. Master Synergy Combos & Empirical Counter-Plays

### Combo 1: Abolishing the Impossible Corner (`B:01` + `B:02` + `N:02` + `C:02`)
* **The Equation (Cunha, Heckman, & Schennach 2010; Lee & Seshadri 2019):**
  $$h_{2} = A_1 \left[ \gamma_1 h_1^{\phi_1} + (1-\gamma_1)\left( G_{\text{ECE},1}^{\text{in-kind}} + \kappa_1 \max\big\{0,\, i_c(y_1 - p_h^r\bar{h} - p_e(z_2))\big\} + \omega_1 \tau_c w_1 h_1 \right)^{\phi_1} \right]^{\frac{\rho_1}{\phi_1}}$$
  with $\phi_1 = -0.50 < 0$ and $\frac{\partial^2 h_3}{\partial h_2 \, \partial I_{\text{mentor},2}} > 0$.
* **Closing the D20 Bottom Reef (Rolls 1–6):** In the 1972 Dunedin cohort, $\Pr(i_c=0) = 22\%$ (d20 **1–4**); by the 2010 GUiNZ cohort (`H:06`), $3.10\times$ rents expand the corner to $30\%$ (d20 **1–6**). Playing `T:00` (*Unconditional Cash Leakage*) or `T:01` (*Late Remediation*) fails because $\partial i_c / \partial T_{\text{cash}} \approx 0.08$ in deep rent distress and $\lim_{h_2 \to h_{\min}} \partial h_3 / \partial G_{\text{tertiary},3} \to 0$.
* **The Judo Counter:** Pair **`B:01` ($G_{\text{ECE}}^{\text{in-kind}} = \text{NZD } 13\text{k/yr}$)** + **`N:02` (Heckman)** + **`B:02` (*Tuakana–Teina*)** + **`C:02` (*Monilukutaito*, Berentson-Shaw 2018)** to permanently cover Rolls 1–6 on the D20 mat and immunize the table against **`T:05` (*Algorithmic Outrage*)**.

### Combo 2: Curing the Lavoisier Syndrome & Self-Financing the Grid (`B:05` + `B:03` + `E:02`)
* **The Equations (Guvenen et al. 2023; Murphy, Shleifer, & Vishny 1991; Farmer & Toda 2017):**
  $$r_{\text{net}}(z, \tau_a, \tau_k) = (1 - \tau_k) z_h k^{\alpha - 1} + z_\ell \left(\frac{\dot{P}_L}{P_L}\right) - \tau_a \implies \frac{\partial A^\star(\tau_a)}{\partial \tau_a} < 0$$
  $$\Delta A_{\text{prec}} \equiv \int_{\mathcal{S}} a \, d\mu^\star\big(s \,\big|\, pv=0, \sigma_{z_2}=0.25\big) - \int_{\mathcal{S}} a \, d\mu^\star\big(s \,\big|\, pv=5, \sigma_{z_2}=0\big) = \text{NZD } 60.8\text{B–}91.5\text{B} \ge \text{CapEx}$$
* **Closing the D20 Top Reef (Rolls 19–20):** When $\tau_a = 0$ on NZD 1.6T of property, land hoarding ($z_\ell$) out-yields building ($z_h$), triggering `T:02` (1-for-1 buyer subsidy capitalization when $\epsilon_S^{\text{land}} \approx 0$) and `T:04` (the Lavoisier talent drain).
* **The Judo Counter:** Enacting **`B:05` (Use-It-Or-Lose-It 1.5% Land/Wealth + 25%$\to$18% Estate Shift)** + **`B:03` (NZD 62k+ Youth Grant)** + **`E:02` (Precautionary Release)** closes D20 Rolls 19–20, releases NZD 60.8B–91.5B in precautionary cash buffers to self-finance national electrification (+NZD 15.55B/yr OPEX savings), and keeps active builders (`20:01`–`20:19`, up to NZD 100M NW) net welfare positive.

### Combo 3: Bending the Accounting Curve (`B:07` + `N:03` + `B:06`)
* **The Equation (Williamson 2009; NZ Treasury CBAx 2025):**
  $$\text{NPV}_{\text{ACC}}(t=5) = \sum_{s=1}^{81} \frac{\Delta \mathbb{E}\big[\tau_y w_s h_s - \sum_{x \in \{1,2,4\}} C_x \mathbb{I}(\text{Exit}_x)\big]}{(1 + r_{\text{SRTP}})^s} = \text{NZD } 35.25\text{B} \;\; (3.84\times \text{Cost at } r_{\text{SRTP}} = 2.0\%)$$
* **Canceling the Every-3rd-Turn Election Audit (`H:01`):** Pairing **`B:07` (ACC Actuarial Time-Bend)** with **`N:03` (Williamson)** books $1.16\times$ direct cost-avoidance breakeven (NZD 10.68B) and $3.84\times$ total return by Year 5 (Turn 2), neutralizing `H:01` and unlocking **`B:06` (The 2050 50/50 Rule: 18.5% PAYE & Super kept at Age 65)**.

---

## 4. Scaling Strategy from 2 Players to 6 Players ($P = 2 \dots 6$)

| Player Count ($P$, Normalized) | `SS1` Reach % | `SS2` Reach % (Mean Turn) | Win Rate vs. Finland | Hub (`K:01`) vs. Finisher (`K:02`) Win Share | Mean Per-Player Score ($\bar{\Sigma}_{\text{Per-Capita}}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2 Players (Duel / Co-Op Pair)** | 96.2% | 88.9% *(Turn 12.9)* | 91.4% | **43.1% : 44.8%** | **142.1 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 76.4$)* |
| **3 Players** | 97.5% | 90.4% *(Turn 12.6)* | 93.0% | **42.4% : 44.9%** | **141.7 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 75.8$)* |
| **4 Players (Standard Crew)** | 98.4% | 91.2% *(Turn 12.4)* | 94.1% | **41.8% : 44.6%** | **139.2 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 74.2$)* |
| **5 Players** | 98.1% | 90.8% *(Turn 12.5)* | 93.8% | **43.5% : 43.9%** | **137.7 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 73.6$)* |
| **6 Players (The Big Table)** | 97.8% | 89.7% *(Turn 12.7)* | 92.9% | **44.0% : 43.2%** | **135.9 pts/player** *(Raw $\mathcal{M}_i+\mathcal{W}_i = 72.9$)* |

* **2-Player Key Tactic:** Use the **Self-Combo Rule**—expose `B:01` and `B:05` in your elder character's River slot and trigger combos from your younger character's hand to pay yourself 100% of the Variant B royalties while building toward `SS1`.
* **6-Player Key Tactic:** Because 6-player games suffer higher `H:02` Silo Political Drag (3.0 Wealth and 3 co-stakers required per Subsystem), prioritize assembling three Dual-Class Wayfinders early to unlock **`K:07` (*Te Tiriti & The Big Table Crew*)**, which shares all Innate Kaupapa abilities across the entire table!

---

## 5. Solo & Co-Op Racing Variant: "Chasing Finland" (The Economic Sailing Race)

Pit Aotearoa New Zealand (starting at **81.0** in `SS0`) in a 20-Turn Match Race along the **Social Cohesion & Welfare Track (`C:06`, Target: 126.0)** against an automated foreign benchmark vessel rolled on the D20 every Phase IV:

| Rival Vessel Profile | Roll 1–5 (Headwind) | Roll 6–15 (Cruising) | Roll 16–20 (Gust) | Structural Ceiling / Historical Lesson |
| :--- | :--- | :--- | :--- | :--- |
| **1. Finland (Nordic Benchmark — Starts at 88.0)** | **$-0.5$ pts** *(Demographic drag)* | **$+1.0$ pt** *(Steady Nordic compounding)* | **$+2.0$ pts** *(High-tech / education surge)* | Starts ahead with Gate 1 clinics (`B:01`) and #1 *Monilukutaito* (`C:02`); finishes around **107.2**. Aotearoa must lift onto foils (`SS1` $\to$ `SS2`) to overtake Finland and reach **126.0**! |
| **2. Devolved Scotland (`T:01`/`B:01` — Starts at 83.0)** | **$0.0$ pts** | **$+1.5$ pts** *(Fast early child gains)* | **$+2.0$ pts** | **Hard Ceiling at 96.0:** Lacks unitary sovereign power to enact `B:05` (land/estate tax); stalls under urban rent capitalization (`T:02`). |
| **3. 1989 Bubble Japan (Deming *Kaizen* — Starts at 90.0)** | **$-3.0$ pts** *(Turns 7–20 Land Bubble Crash!)* | **$+2.5$ pts** *(Turns 1–6)* | **$+3.5$ pts** *(Turns 1–6)* | Surges to **105.0** by Turn 6 on industrial *Kaizen*, then collapses into a 14-turn balance-sheet recession when surpluses pour into Tokyo land (`T:02`/`T:04`) instead of `B:06`. |
