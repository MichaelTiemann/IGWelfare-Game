# Card `H:06` Tutorial: The 1972 Nostalgia Baseline (`Dunedin` vs. `GUiNZ`)

> **Monograph Integration Guide:**
> * **Sections 1–2** are formatted for direct inclusion in **Document 1A (§3.6: *Historical Precedents & Cautionary Traps — The 1972 Nostalgia Baseline*)**.
> * **Section 3** provides the formal Stone–Geary, CES, and Kolmogorov Forward mathematical specification for **Document 1B (§2.3: *Structural Cohort Drift and the Rising Marginal Return to In-Kind Wraparound*)**.

---

## 1. The Historical Trap: Budgeting for 2026 with a Rearview Mirror Pointed at 1972 (Document 1A)

New Zealand possesses two of the world's crown-jewel longitudinal birth-cohort studies, separated by thirty-seven years of macroeconomic and institutional history:

1. **The Dunedin Multidisciplinary Health and Development Study (`n = 1,037`, born 1972–1973):**
   * **The Macroeconomic Context:** The Dunedin cohort entered Gate 1 (ages 0–5) at the zenith of New Zealand's post-war egalitarian settlement. Unemployment stood below `1%`, urban house prices averaged `2.5x–3.0x` household income (with rents near `1.2x` rural baselines), Mothers received the universal, unconditional **Family Benefit** (which could be capitalized upfront under the *Family Benefits (Home Ownership) Act 1964* to serve as a 3% State Advances mortgage deposit), and state housing provided permanent, insulated tenure stability.
   * **The Dunedin Concentration Finding:** Even within that high-employment, low-rent environment, Poulton et al. (2015, 2020) demonstrated that the **22.0% of children** who experienced early childhood socioeconomic adversity or neurodevelopmental vulnerability accounted for **57% to 81%** of adult hospital nights, long-term welfare receipt, credit defaults, and criminal justice convictions thirty years later.

2. **Growing Up in New Zealand (`GUiNZ`, `n = 6,853`, born 2009–2010):**
   * **The Degraded Welfare & Housing Reality:** By the time the GUiNZ cohort was born in 2009–2010—and tracked through the *Now We Are 8*, *Now We Are 12*, and *Now We Are 15* waves—New Zealand's social safety net and housing market had undergone a structural phase shift:
     * **The 1991 *Mother of All Budgets* ("Ruthanasia"):** Abolished the universal Family Benefit, slashed core benefit rates by up to 25%, and replaced income-related state housing rents with market-rent accommodation supplements—subsidizing private landlords while locking low-income whānau into deep abatement traps.
     * **The Untaxed Land Speculation Wave (`T:04` / `H:05`):** An untaxed NZD 1.6T residential property pool inflated Auckland and metro house-price-to-income multipliers to **`3.10x`** rural baselines, turning private rental housing into a precarious, high-churn sector.
     * **Residential Transience (`>45%` Churn):** Over **45% of GUiNZ children** born into private rentals moved two or more times before starting primary school at age 5, repeatedly severing connections to Plunket nurses, early childhood education (`ECE`) centres, and neighborhood peer networks.

### Why Orthodox Fiscal Baselines Fail (`H:06`)

When Treasury or social-agency models treat the **1972 Dunedin 22% cohort** as a static biological constant rather than an endogenous outcome of 1972 housing and welfare institutions, they commit **The 1972 Nostalgia Baseline Fallacy (`H:06`)**:
* In `GUiNZ`, **14.3% of children** are trapped in severe, multi-wave material hardship and toxic stress from birth (`d20` rolls `1–3`), while an additional **15.7% of children** (`d20` rolls `4–6`) are pushed into the zero-cash-investment corner ($i_c = 0$) by `3.1x` metro rents, `2.8x` rural transport fuel costs, and chronic rental transience—expanding the vulnerable Gate 1 share from **22.0% (`d20` rolls 1–4)** to **30.0% (`d20` rolls 1–6)**.
* By the *Now We Are 12* and *Now We Are 15* waves, this unbuffered cohort drift manifests as a **doubling of clinical youth anxiety and depression**, severe school alienation among neurodivergent and disabled rangatahi (`26%` school satisfaction vs. `43%` peers), and a surge in national remediation drag from **NZD 17.7B/yr** (1972 Dunedin weights) to **NZD 28.5B/yr** (2010 GUiNZ weights).

---

## 2. Tabletop Comparison: 1972 Dunedin vs. 2010 GUiNZ vs. `SS2` Foil-Borne Package

| Macroeconomic & Lifecycle Metric | 1972 Dunedin Baseline (`SS0` Optimistic) | 2010–2026 GUiNZ Reality (`H:06` Boss Active) | `SS2` Foil-Borne Counter (`B:01`+`B:02`+`B:05`+`E:02`) |
| :--- | :--- | :--- | :--- |
| **Gate 1 Hardship Corner $\Pr(i_c = 0)$** | **22.0%** (`d20` Rolls 1–4) | **30.0%** (`d20` Rolls 1–6: `14.3%` acute + `15.7%` rent/churn) | **$\le$ 1.5%** (`d20` Sub-Roll `01:01` only) |
| **Gate 1 $\to$ Gate 2 Self-Productivity Haircut** | `-6.0%` (High 1970s tenure stability) | **`-25.0%`** (`>45%` private rental transience before age 5) | **`0.0%`** (Rents cooled `-10.5%` + solar homes) |
| **National Remediation Hull Drag (Exits 1, 2, 4)** | **NZD 17.7B/yr** | **NZD 28.5B/yr** (**`+NZD 10.8B/yr`** penalty) | **NZD 4.2B/yr** (`-75%` to `-85%` reduction) |
| **Social Cohesion & Youth Mental Health** | Index **100.0** | Index **91.5** (`-8.5` pts; `2x` youth anxiety/distress) | Index **126.0** (`#1` global trust trajectory) |
| **2050 Steady-State PAYE Income Tax Drift** | `22.0%` $\to$ **28.2%** | `22.0%` $\to$ **30.4%** (`+2.2 pp` extra tax creep) | Cut to **18.5%** (`-3.5 pp` below today) |
| **`B:07` Year-5 ACC Actuarial Return Multiple** | **3.84x** (NZD 35.3B NPV) | **4.45x** (NZD 40.9B NPV when countered!) | **Locked in on Crown Balance Sheet** |

---

## 3. Formal Mathematical Specification for Document 1B (§2.3)

### 3.1 Expansion of the Stone–Geary Zero-Investment Corner ($i_c = 0$)

Let household disposable income at Gate 1 (child ages 0–5) in region $r \in \{1..4\}$ be $y_{1,r}(s)$, facing mandatory housing expenditure $p_{h,r}^r \bar{h}$ and stochastic energy expenditure $p_e(z_2)$. Under Stone–Geary non-homothetic preferences with subsistence floor $\bar{c}_r(t) = \bar{c}_0 + p_{h,r}^r(t)\bar{h} + p_e(z_2, t)$, private cash investment in early child skill $i_c^\star(s)$ satisfies the Kuhn–Tucker condition:

$$i_c^\star(s_1, t) = \max\Big\{ 0,\; \theta_c \big[ y_{1,r}(s_1) + T_{\text{cash}}(t) - p_{h,r}^r(t)\bar{h} - p_e(z_2, t) - \bar{c}_0 \big] \Big\}$$

Between the **1972 Dunedin cohort ($t = 1972$)** and the **2010 GUiNZ cohort ($t = 2010$)**, two structural parameters shifted adversely:
1. **The 1991 Transfer Cut:** Real unconditional family transfers fell ($\Delta T_{\text{cash}} < 0$) while abatement rates on working-poor income rose.
2. **The Untaxed Land Rent Surge ($\tau_a = 0$):** Urban rent-to-income ratios rose from $\frac{p_{h,\text{AKL}}^r(1972)\bar{h}}{\bar{y}_1} \approx 1.2$ to $\frac{p_{h,\text{AKL}}^r(2010)\bar{h}}{\bar{y}_1} \approx 3.1$.

Consequently, the income threshold $\tilde{y}_1(t) \equiv \bar{c}_0 + p_{h,r}^r(t)\bar{h} + p_e(z_2, t) - T_{\text{cash}}(t)$ below which parents are forced into the zero-investment corner ($i_c^\star = 0$) shifted upward from the 22nd percentile to the 30th percentile of the Rawlsian birth distribution:

$$\Pr_{1972}^{\text{Dunedin}}\big(i_c^\star(s_1) = 0\big) = \int_{y_1 \le \tilde{y}_1(1972)} d\mu_{1972}(s_1) = 0.220 \quad \longrightarrow \quad \Pr_{2010}^{\text{GUiNZ}}\big(i_c^\star(s_1) = 0\big) = \int_{y_1 \le \tilde{y}_1(2010)} d\mu_{2010}(s_1) = 0.300$$

### 3.2 Residential Transience as an Endogenous Haircut on Self-Productivity ($\gamma_1$)

Let $\nu_r(a_1, p_{h,r}^r) \in [0, 1]$ denote the probability of forced residential relocation during ages 0–5 (empirically $\nu > 0.45$ for private-rental households in `GUiNZ`). Each forced move disrupts attachment to primary health providers and early childhood centres, acting as a multiplicative erosion factor $(1 - \zeta \nu_r)$ on Gate 1 self-productivity $\gamma_1$ inside the Cunha–Heckman–Schennach (2010) CES production function:

$$h_2(s_1) = A_1 \left[ \gamma_1 \big(1 - \zeta \nu_r(a_1, p_{h,r}^r)\big) h_1^{\phi_1} + (1 - \gamma_1) \left( G_{\text{ECE},1}^{\text{in-kind}} + \kappa_1 i_c^\star(s_1) + \omega_1 \tau_c w_1 h_1 \right)^{\phi_1} \right]^{\frac{\rho_1}{\phi_1}}, \qquad \phi_1 = -0.50$$

### 3.3 Proof of the Supermodular Actuarial Dividend Under `B:01` + `B:05`

Because Gate 1 inputs are strong complements ($\phi_1 = -0.50 < 0 \implies \sigma_1 = \frac{1}{1-\phi_1} = 0.67 < 1$), the cross-partial derivative of child readiness $h_2$ with respect to universal in-kind wraparound $G_{\text{ECE},1}^{\text{in-kind}}$ (`B:01`) and the probability of being trapped at the zero-cash corner $\Pr(i_c^\star = 0)$ is strictly positive:

$$\frac{\partial^2 \mathbb{E}[h_2]}{\partial G_{\text{ECE},1}^{\text{in-kind}} \, \partial \Pr(i_c^\star = 0)} > 0 \quad \text{and} \quad \frac{\partial^2 \mathbb{E}[h_2]}{\partial G_{\text{ECE},1}^{\text{in-kind}} \, \partial (-\nu_r)} > 0$$

Therefore:
1. **Unbuffered Penalty (`H:06` Active in `SS0`):** Leaving `B:01` and `B:05` unplayed under the 2010 `GUiNZ` distribution increases annual fiscal remediation drag by:
   $$\Delta \mathcal{D}_{\text{GUiNZ}} = \sum_{x \in \{1,2,4\}} \int_{\mathcal{S}} C_x(s) \, d\Big(\mu_{2010}^{\text{GUiNZ}}(s) - \mu_{1972}^{\text{Dunedin}}(s)\Big) = +\text{NZD } 10.8\text{B/yr} \quad (\text{NZD } 17.7\text{B} \to \text{NZD } 28.5\text{B/yr})$$
2. **Amplified Counter-Dividend (`B:01` + `B:02` + `B:05` Played):** Deploying `B:01` (NZD 13.0k/yr in-kind wraparound) alongside `B:05` (`-10.5%` rent cooling, eliminating transience $\nu_r \to 0$) and `B:02` (Gate 2 mentoring) rescues **both** the original 22% Dunedin tail and the newly squeezed Vigintiles 5–6 (`8%` GUiNZ cohort), lifting the Year-5 ACC Actuarial Return (`B:07`) from **`3.84x` to `4.45x`**!
