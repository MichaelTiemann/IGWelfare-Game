"""
canonical_equations.py
Single source of truth for clean HTML (MathJax) and PPTX equation rendering
in MichaelTiemann/IGWelfare-Game.
"""

import re

# ---------------------------------------------------------------------------
# 1. Exact, hand-audited canonical LaTeX overrides for multi-line, quotient,
#    prose-heavy, &-escaped, and parenthetical-trimmed cards.
# ---------------------------------------------------------------------------
CANONICAL_EQUATIONS: dict[str, str] = {
    "B:00": (
        r"\mathrm{CE}_k(\Phi) = \left("
        r"\frac{\int V_k(a_1, h_1, z_1, j=1;\,\Phi)\,d\mu_{1,k}(\Phi)}"
        r"{\int V_k(\Phi_0)\,d\mu_{1,k}(\Phi_0)}"
        r"\right)^{\!\frac{1}{\phi_{\mathrm{nd}}(1 - \sigma_c)}} - 1"
    ),
    "B:01": (
        r"\Theta_1(\theta_c) = \left["
        r"\gamma_{1,\mathrm{self}}\,\theta_c^{\phi_1} + "
        r"\gamma_{1,\mathrm{inv}}\,(i_c + G_{\mathrm{ECE},1}^{\mathrm{eff}} + \bar{g}_{\mathrm{ECE}})^{\phi_1} + "
        r"\gamma_{1,\mathrm{par}}\,\bar{h}_p^{\phi_1}"
        r"\right]^{1/\phi_1}, \quad \phi_1 = +0.35"
    ),
    "B:02": (
        r"e_{\mathrm{tot}} = \frac{y_{\mathrm{disp}} - \bar{e}_k - "
        r"\mathbb{I}_{j \in J_c}(1 - s_{\mathrm{sub}})\,i_c - a'}{1 + \tau_c}"
    ),
    "B:03": (
        r"\begin{aligned}"
        r"\theta_{c,\mathrm{ret}} &= \theta_c - \delta_{\theta,\mathrm{fade}}(1 - M_{\mathrm{mentor}})\max(0,\,\theta_c - \theta_{\mathrm{base}}) \\"
        r"G_{\mathrm{ECE},1}^{\mathrm{eff}} &= G_{\mathrm{ECE},1}\left(1 + \kappa_{\mathrm{down}}\,M_{\mathrm{mentor}}\,\bar{\theta}_{J=5}\right)"
        r"\end{aligned}"
    ),
    "B:04": (
        r"\begin{aligned}"
        r"P_{G4 \to G5} = \big[\,(1 - \mathrm{emig}_t) \odot P_{\mathrm{Ret},3\times 4},\;\mathrm{emig}_t\,\big] \quad \text{mapping Launch Tiers } (h) \\"
        r"\longrightarrow \big[\,\text{Adversity},\;\text{Core Trades},\;z_\ell,\;z_h,\;\text{Abroad}\,\big]"
        r"\end{aligned}"
    ),
    "B:05": (
        r"\begin{aligned}"
        r"E_t(h_1, M_{\mathrm{mentor}}) &= E_{\mathrm{grant}} \cdot \mathbb{I}_{M_{\mathrm{mentor}} = 1} \quad \text{for } t \in \text{Waves } 1\text{--}6, \\"
        r"&\text{transitioning to universal } E_{\mathrm{grant}} \text{ across Waves } 7\text{--}13"
        r"\end{aligned}"
    ),
    "B:06": (
        r"\begin{aligned}"
        r"a_1 + E &\ge \xi_k \cdot Q_k(\tau_a, \tau_b) \quad (\xi_k = 0.20) \\"
        r"P_{\mathrm{emig}}(k \to \text{Abroad}) &= 1 - \sum_{m=1}^{4} P_t(k \to m \mid a_1 + E,\, h_1,\, z_1)"
        r"\end{aligned}"
    ),
    "B:07": (
        r"\begin{aligned}"
        r"u_{\mathrm{beq}}(a';\,\tau_b) &= b_1 \cdot \frac{\big(1 + (1 - \tau_b)\,a' / b_2\big)^{1 - \eta_c} - 1}{1 - \eta_c} \\"
        r"\mathrm{Estates}_{\mathrm{net}} &= (1 - \tau_b)\,a'^*"
        r"\end{aligned}"
    ),
    "B:08": (
        r"R_k(z_f;\,\Delta t) = (1 - \tau_a)^{\Delta t} + (1 - \tau_k)\Big["
        r"r(\Delta t) + \max\!\big\{0,\;\pi_k^*(z_f, w_k) - \big(r(\Delta t) + \delta_k(\Delta t)\big)\big\}\cdot \lambda_{\mathrm{col}}"
        r"\Big]"
    ),
    "B:09": (
        r"V_{k,t_0}^{(L)}(H=25;\,r_{\mathrm{disc}}) = C_{k,\mathrm{realized}}^{(L)}(t_0) + "
        r"(1 - \alpha_{\mathrm{attr}})\,\Phi_{\mathrm{pipe}}(t_0)\sum_{s=1}^{25}"
        r"\left(\frac{1 + g_{\mathrm{cost}}}{1 + r_{\mathrm{disc}}}\right)^{\!s} (\psi_{k,0})^s\,f_{k,t_0+s}^{(L)}"
    ),
    "B:10": (
        r"\mathcal{L}_{\mathrm{SMM}}(\theta) = \sum_{m=1}^{15} W_m \left("
        r"\frac{\hat{M}_m(\theta) - M_m^{\mathrm{data}}}{\max(0.02,\,|M_m^{\mathrm{data}}|)}"
        r"\right)^{\!2}"
    ),
    "B:11": (
        r"\Omega_{\mathrm{fiscal}} = \big(\mathrm{Tax}_{\mathrm{GST+Cap+Beq},27} + \mathrm{Tax}_{\mathrm{PAYE},28}\big) - "
        r"\big(\mathrm{Burden}_{\mathrm{Exits\,1,2,4}} + \mathrm{Outlay}_{\mathrm{Infra+Health+Super},26}\big)"
    ),
    "B:12": (
        r"\begin{aligned}"
        r"\Delta_{\mathrm{syn},w} &= \mathrm{CE}_k(A_w \cup B_w) - \mathrm{CE}_k(A_w) - \mathrm{CE}_k(B_w) > 0 \\"
        r"\mathrm{CE}^{\mathrm{SS2}} &= 11.23\text{ pp (Isolated)} + 13.47\text{ pp (Wedges 1--4)} = +24.70\text{ pp}"
        r"\end{aligned}"
    ),
    "B:13": (
        r"\begin{aligned}"
        r"\Phi(t) &= \Phi_1 + \frac{\Phi_2 - \Phi_1}{1 + \exp\!\big(-\xi_{\mathrm{ramp}}(t - T_1)\big)} \\"
        r"\tilde{V}_{t+1} &= (1 - \lambda_{\mathrm{cred}})\,V^{\mathrm{SS1}} + \lambda_{\mathrm{cred}}\,V^{\mathrm{SS2}}"
        r"\end{aligned}"
    ),
    "B:14": (
        r"\begin{aligned}"
        r"\Delta D_{2050}(\mathrm{reg}) &= (\omega_{\mathrm{reg}}\cdot N_{\mathrm{births}})\cdot (0.50\,\Omega_{\mathrm{reform}})\sum_{\tau=1}^{25}(1 + r_{\mathrm{bond}})^{\tau - 1} \\"
        r"\Delta r &= -0.006 \quad (-60\text{ bps})"
        r"\end{aligned}"
    ),
    "B:15": (
        r"\begin{aligned}"
        r"S_{\mathrm{reinv}} &= 1.65 \cdot (0.50\,\Omega_{\mathrm{reform}}) \\"
        r"\tau_{\ell,t}^{\mathrm{req}}(A_{\mathrm{super}}) &= \tau_{\ell,\mathrm{non\text{-}super}} - 0.0064 + \frac{\mathrm{Ret\_Outlays}(A_{\mathrm{super}})}{\bar{H}_t}"
        r"\end{aligned}"
    ),
    "B:16": (
        r"\begin{aligned}"
        r"u_{\mathrm{rel}}(\mathrm{Frac}_{\mathrm{struggling}}, S_t) &= \chi_{\mathrm{rel}}\Big[(0.285 - \mathrm{Frac}_{\mathrm{struggling}}) + 0.015\,(S_t - 100)\Big] \\"
        r"S_t &: 100.0 \longrightarrow 118.4 \longrightarrow 126.0"
        r"\end{aligned}"
    ),
    "T:00": (
        r"\mathbb{E}_{\mu_k}\!\big[f(a, h, \theta_c, z)\big] \ll "
        r"f\!\big(\mathbb{E}[a],\,\mathbb{E}[h],\,\mathbb{E}[\theta_c],\,\mathbb{E}[z]\big)"
    ),
    "T:01": (
        r"S_t = 100.0 + \zeta_{\mathrm{hardship}}(0.220 - \mathrm{Frac}_{\mathrm{struggling},t}) + "
        r"\zeta_{\mathrm{ret}}(0.1093 - \mathrm{Emig}_{\mathrm{Nat},t}) - "
        r"\zeta_{\mathrm{churn}}\max(0,\,\mathrm{Churn}_t - \overline{\mathrm{Churn}})"
    ),
    "T:02": (
        r"\begin{aligned}"
        r"W_f &= u_f(d_t) + \beta_{\mathrm{hyp}}\,\delta\,V'_f(a', h', \theta'_c) \\"
        r"e_{\mathrm{total}} &= e_{\mathrm{real}} + e_{\mathrm{avoidance}} + \bar{e}_{\mathrm{bargaining}} \ll e_{\mathrm{Laffer}}"
        r"\end{aligned}"
    ),
    "T:03": (
        r"K_{\mathrm{wh\bar{a}nau}}^{\mathrm{net}}(i_c, z, a, J_r, k) = "
        r"K_{\mathrm{wh\bar{a}nau},k}(J_r, Q_k) - \psi_{\mathrm{sandwich}}\cdot "
        r"\mathbb{I}_{\mathrm{Super} > 65}\cdot \mathbb{I}_{\mathrm{distress}}(i_c, z, a) < 0"
    ),
    "T:04": (
        r"1 - \phi_{\mathrm{adj}}(\Delta s)^2:\quad "
        r"1 - 0.180(1)^2 = 0.820\;\text{(Single-Shot)} \quad\text{vs.}\quad "
        r"1 - 0.180\!\left(\tfrac{1}{3}\right)^2 = 0.980"
    ),
    "T:05": (
        r"\begin{aligned}"
        r"P_{G4 \to G5}:\quad &\text{Retained Top-Tier Talent in SS0} \\"
        r"&\longrightarrow 61\%\text{ Node 19 } (z_\ell\text{ Speculation}) \;\text{ vs. }\; 29\%\text{ Node 20 } (z_h\text{ Builders})"
        r"\end{aligned}"
    ),
    "T:06": (
        r"P_t(k \to m \mid a_1, h_1, z_1) \propto "
        r"\exp\!\left(\frac{V_{m,t}\big(\max(a_{\min},\,a_1 - \kappa_{k \to m}),\,h_1,\,z_1,\,1\big)}{\varrho_{\mathrm{mig}}}\right)"
    ),
    "T:07": (
        r"\mathrm{Retained\_Gain}(2\text{ terms off}) = (1 - \delta_{\theta,\mathrm{fade}})^2 = (1 - 0.22)^2 = 0.6084 "
        r"\implies 39.2\%\text{ compound fade-out}"
    ),
    "T:08": (
        r"\Delta G_{\mathrm{ECE}} + \Delta T_k > 0 \;\text{ with }\; \Delta\tau_a = \Delta\tau_b = 0 "
        r"\implies \tau_\ell \to 42\%\text{--}48\% \;\land\; r_{h,k}^{\mathrm{rent}}(Q_k)\text{ unchanged}"
    ),
    "T:09": (
        r"S_f(n_f) = u_f\big(c_f(n_f)\big) + \beta_{\mathrm{hyp}}\,\delta\,V'_f(n_f) - "
        r"\theta_\tau\,\psi_{\mathrm{time}}\,n_f + \omega_{\mathrm{ECE}}\,G_{\mathrm{ECE}}\,n_f - \psi_Q\,Q_k\,n_f < \underline{U}_f"
    ),
    "T:10": (
        r"Q_{k,t} = \sum_{s=1}^{\infty}\left(\frac{G_k}{R(\tau_a)}\right)^{\!s} d_{\mathrm{land},k,t} + B_{\mathrm{land},k,t} "
        r"\implies B_{\mathrm{land},k,t} > 0 \;\text{ whenever }\; G_k \ge R(\tau_a = 0)"
    ),
    "C:01": (
        r"R_k(z_f;\,\Delta t) = (1 - \tau_a)^{\Delta t} + (1 - \tau_k)\Big["
        r"r(\Delta t) + \max\!\big\{0,\;\pi_k^* - \big(r(\Delta t) + \delta_k^{\mathrm{shock}}(\Delta t)\big)\big\}\cdot \lambda_{\mathrm{col}}"
        r"\Big]"
    ),
    "C:02": (
        r"S_t = 100.0 + \zeta_{\mathrm{hardship}}(0.220 - \mathrm{Frac}_{\mathrm{struggling},t}) + "
        r"\zeta_{\mathrm{ret}}(0.1093 - \mathrm{Emig}_{\mathrm{Nat},t}) - "
        r"\zeta_{\mathrm{churn}}\max(0,\,\mathrm{Churn}_t - \overline{\mathrm{Churn}})"
    ),
    "C:03": (
        r"\Omega_{\mathrm{reinv}} = 0.50\cdot\max(0,\,\Omega_{\mathrm{fiscal}}), \qquad "
        r"S_{\mathrm{reinv}} = \mu_{\mathrm{infra}}\cdot \Omega_{\mathrm{reinv}} \quad (\mu_{\mathrm{infra}} = 1.65)"
    ),
    "C:04": (
        r"\Psi_{J=5} = -\psi_{\mathrm{unemp}}\big[\mathbb{I}(z_p \in Z_{\mathrm{distress}}) + \lambda_{\mathrm{psy}}(M_{\mathrm{mentor}})\big]"
        r"(1 - \zeta_{\mathrm{buf}} M_{\mathrm{mentor}})(1 - 0.55\,K_{\mathrm{wh\bar{a}nau}}^{\mathrm{eff}}) + \kappa_{\mathrm{up}} M_{\mathrm{mentor}}"
    ),
    "C:05": (
        r"\begin{aligned}"
        r"\ell_{\mathrm{eff}} &= \max(0,\,\ell - I_h), \quad I_h \in \{0,\,0.15,\,0.30\} \\"
        r"\lambda_{\mathrm{cred}}^{\mathrm{actuarial}}(t) &\longrightarrow 1.0 \quad \text{under Monilukutaito epistemic framing}"
        r"\end{aligned}"
    ),
    "C:06": (
        r"P_t(k \to m \mid a_1, h_1, z_1) = "
        r"\frac{\exp\!\Big(V_{m,t}\big(\max(a_{\min},\,a_1 - \kappa_{k \to m}),\,h_1,\,z_1,\,1\big)\big/\varrho_{\mathrm{mig}}\Big)}"
        r"{\exp(V_{\mathrm{Abroad}} / \varrho_{\mathrm{mig}}) + \sum_{r=1}^{4}\exp(V_{r,t} / \varrho_{\mathrm{mig}})}"
    ),
    "C:07": (
        r"e_{\mathrm{tot}} = \frac{y_{\mathrm{disp}} + T_k(a, y_{\mathrm{lab}}) - \bar{e}_k - "
        r"\mathbb{I}_{j \in J_c}(1 - s_{\mathrm{sub}})\,i_c - a'}{1 + \tau_c}"
    ),
    "C:08": (
        r"\begin{aligned}"
        r"z_k^{\mathrm{eff}}(i_z) &= z_{k,\mathrm{base}}(i_z) + \Delta\mu_{z,k}, \quad \text{where} \\"
        r"&\text{competition + procurement lift } \Delta\mu_{z,\mathrm{SS1}} = [+0.024,\,+0.018,\,+0.010,\,+0.006]"
        r"\end{aligned}"
    ),
    "C:09": (
        r"z_k^{\mathrm{eff}}(i_z) = z_{k,\mathrm{base}}(i_z) + \Delta\mu_{z,\mathrm{SS2}}, \qquad "
        r"\Delta\mu_{z,\mathrm{SS2}} = [+0.0408,\,+0.0307,\,+0.0170,\,+0.0102]"
    ),
    "C:10": (
        r"\begin{aligned}"
        r"T_k^{\mathrm{SS2}} &= T_k^{\mathrm{SS0}} + (1 - \psi_{\mathrm{retire},T})\big(T_k^{\mathrm{SS1}} - T_k^{\mathrm{SS0}}\big) \quad (\psi_{\mathrm{retire},T} = 0.850) \\"
        r"&\implies \Delta\tau_{\ell,\mathrm{retire}} = -0.0064 \quad (-0.64\text{ pp})"
        r"\end{aligned}"
    ),
    "K:01": (
        r"\frac{\partial^2 \theta_c^{\mathrm{ces},2}}{\partial \theta_c^{\mathrm{ret}}\,\partial X_m} = "
        r"(1 - \phi_2)\,\gamma_{2,\mathrm{self}}\,\gamma_{2,m}\,(\theta_c^{\mathrm{ces},2})^{1 - 2\phi_2}"
        r"(\theta_c^{\mathrm{ret}}\cdot X_m)^{\phi_2 - 1} > 0"
    ),
    "K:02": (
        r"\tilde{V}_{k,t+1} = \big(1 - \lambda_{\mathrm{cred}}(t)\big)V_{k,t+1}^{\mathrm{perm,SS1}} + "
        r"\lambda_{\mathrm{cred}}(t)\,V_{k,t+1}^{\mathrm{full,SS2}}"
    ),
    "K:03": (
        r"G_{\mathrm{ECE},1}^{\mathrm{eff}} \to \Theta_1 \;+\; \mathrm{GrowingChange} \to M_{\mathrm{mentor}} \;+\; "
        r"\mathrm{LFPI}\,(1.60\times\text{--}2.16\times) \to \Delta\mu_{z,k} \implies \psi_{\mathrm{retire},T} = 0.85"
    ),
    "K:04": (
        r"p_H(a, z, Q_k) = \left(\xi_{\mathrm{hh}}(a, Q_k)\,\mathrm{rh}_k + "
        r"(1 - \xi_{\mathrm{hh}})\frac{\mathrm{rr}_k}{0.5\,\bar{\chi}}\right)"
        r"\Big(1 + 0.12\cdot\mathbb{I}(a < 0.08\,Q_k \;\land\; z < 0.85)\Big)"
    ),
    "K:05": (
        r"\begin{aligned}"
        r"\frac{\partial^2 Y_k}{\partial Z_k\,\partial H_k} &= (1 - \alpha_k)\,K_k^{\alpha_k}\,H_k^{-\alpha_k} > 0 \\"
        r"\Delta\mathrm{CE}_m(\omega_{\mathrm{ent}} = 0.80) &> 0 \quad \text{up to NZD } 50\text{M}"
        r"\end{aligned}"
    ),
    "K:06": (
        r"\mathrm{PassThrough}(\Delta\tau_k, T_k) \to 1.0 \iff "
        r"M_{\mathrm{olig}} \to 1.00 \;\land\; \tau_{a,k}\text{ synchronized across } k \in \{1,\dots,4\}"
    ),
    "K:07": (
        r"\lambda_{\mathrm{cred}}^{\mathrm{actuarial}}(t) = \min\!\left\{1,\; \lambda_0 + (1 - \lambda_0)\cdot"
        r"\max\!\left(0,\;\frac{V^{(\mathrm{Fiscal})}(H;\,0.02)\big/C^{(\mathrm{Inv})}(t) - 1}{3.50 - 1}\right)\right\}"
    ),
    "K:08": (
        r"Y_{\mathrm{VFI}} = \sum_{a,h,\theta_c,z} \mu_k(a, h, \theta_c, z, j)\cdot f(a, h, \theta_c, z)"
    ),
    "K:09": (
        r"K_{\mathrm{wh\bar{a}nau}}^{\mathrm{eff}}(k) = K_{\mathrm{wh\bar{a}nau},0}(k)\cdot \Phi_{\mathrm{time}}(A_{\mathrm{super}})\cdot "
        r"\min\!\left(1.15,\;\max\!\left(0.50,\;\frac{p_{\mathrm{super}}}{0.18}\left(\frac{Q_{k,0}}{Q_k}\right)^{\!0.35}\right)\right)"
    ),
    "K:10": (
        r"\mathrm{CE}_{\mathrm{Nat}}(\text{All 4 Coalitions}) = +24.70\% \;\gg\; "
        r"\sum_{c=1}^{4} \mathrm{CE}_{\mathrm{Nat}}(\text{Silo}_c\text{ alone vs. LTFM} < 0)"
    ),
    "N:01": (
        r"\begin{aligned}"
        r"\eta_{k,m}(t) &= \Big(1 - \delta_{\mathrm{adopt}}\,e^{-\lambda_{\mathrm{adopt}}(t - t_0)}\Big)"
        r"\Big[1 - \tau_{\mathrm{fric},\min} - (\tau_{\mathrm{fric},0} - \tau_{\mathrm{fric},\min})\,e^{-\gamma_{\mathrm{learn}} L_m(t-1)}\Big] \\"
        r"&\quad \times \Big[1 - \phi_{\mathrm{adj}}\big(\Delta s_{k,m}(t)\big)^2\Big]"
        r"\end{aligned}"
    ),
    "N:02": (
        r"G_{\mathrm{ECE},s}^{\mathrm{net}} = (1 - \tau_{\mathrm{agency}})\,G_{\mathrm{ECE},s}^{\mathrm{gross}}:\quad "
        r"\tau_{\mathrm{agency}} = 0.32\;\text{(fragmented silos)} \longrightarrow \le 0.08\;\text{(high-trust commissioning)}"
    ),
    "N:03": (
        r"\Theta_s = \Big[\gamma_{s,\mathrm{self}}\,\theta_c^{\phi_s} + \gamma_{s,\mathrm{inv}}\,I_s^{\phi_s} + "
        r"\gamma_{s,\mathrm{par}}\,h_p^{\phi_s}\Big]^{1/\phi_s}, \qquad \phi_1 = +0.35,\;\; \phi_2 = -0.95"
    ),
    "N:04": (
        r"\frac{V_{k,t_0}^{(\mathrm{Fiscal})}(H=25;\,r = 0.02)}{C_{