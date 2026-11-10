#!/usr/bin/env python3
"""
Foils & Founders — Canonical Equation Normalizer, MathJax CSS & PPTX MathText Adapter
=====================================================================================
Single source of truth imported by:
  - scripts/render_study_slides.py (81-Slide 16:9 HTML/PDF Deck)
  - scripts/render_study_cards.py  (16-Sheet A3 Fold-Over Study Cards)
  - scripts/render_study_pptx.py   (81-Slide 360-DPI Computer Modern PPTX Exporter)
"""

from __future__ import annotations
import re
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# 1. Canonical 2-Line-Max LaTeX Specifications for All 80 Cards
#    (Compatible with both MathJax 3 SVG and Matplotlib Computer Modern)
# ---------------------------------------------------------------------------
CANONICAL_EQUATIONS: Dict[str, str] = {
    "B:00": (
        r"\mathrm{CE}_k(\Phi) = \left("
        r"\frac{\int V_k(a_1, h_1, z_1, j=1;\,\Phi)\,d\mu_{1,k}(\Phi)}"
        r"{\int V_k(\Phi_0)\,d\mu_{1,k}(\Phi_0)}"
        r"\right)^{\frac{1}{\phi_{\mathrm{nd}}(1 - \sigma_c)}} - 1"
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
        r"P_{G4 \to G5} = \left[(1 - \mathrm{emig}_t) \odot P_{\mathrm{Ret},3\times 4},\;\mathrm{emig}_t\right] \quad \text{mapping Launch Tiers } (h) \\"
        r"\longrightarrow \left[\text{Adversity},\;\text{Core Trades},\;z_\ell,\;z_h,\;\text{Abroad}\right]"
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
        r"a_1 + E &\geq \xi_k \cdot Q_k(\tau_a, \tau_b) \quad (\xi_k = 0.20) \\"
        r"P_{\mathrm{emig}}(k \to \text{Abroad}) &= 1 - \sum_{m=1}^{4} P_t(k \to m \,|\, a_1 + E,\, h_1,\, z_1)"
        r"\end{aligned}"
    ),
    "B:07": (
        r"\begin{aligned}"
        r"u_{\mathrm{beq}}(a';\,\tau_b) &= b_1 \cdot \frac{\left(1 + (1 - \tau_b)\,a' / b_2\right)^{1 - \eta_c} - 1}{1 - \eta_c} \\"
        r"\mathrm{Estates}_{\mathrm{net}} &= (1 - \tau_b)\,a^{\prime *}"
        r"\end{aligned}"
    ),
    "B:08": (
        r"R_k(z_f;\,\Delta t) = (1 - \tau_a)^{\Delta t} + (1 - \tau_k)\left["
        r"r(\Delta t) + \max\left\{0,\;\pi_k^*(z_f, w_k) - \left(r(\Delta t) + \delta_k(\Delta t)\right)\right\}\cdot \lambda_{\mathrm{col}}"
        r"\right]"
    ),
    "B:09": (
        r"V_{k,t_0}^{(L)}(H=25;\,r_{\mathrm{disc}}) = C_{k,\mathrm{realized}}^{(L)}(t_0) + "
        r"(1 - \alpha_{\mathrm{attr}})\,\Phi_{\mathrm{pipe}}(t_0)\sum_{s=1}^{25}"
        r"\left(\frac{1 + g_{\mathrm{cost}}}{1 + r_{\mathrm{disc}}}\right)^{s} (\psi_{k,0})^s\,f_{k,t_0+s}^{(L)}"
    ),
    "B:10": (
        r"\mathcal{L}_{\mathrm{SMM}}(\theta) = \sum_{m=1}^{15} W_m \left("
        r"\frac{\hat{M}_m(\theta) - M_m^{\mathrm{data}}}{\max(0.02,\,|M_m^{\mathrm{data}}|)}"
        r"\right)^{2}"
    ),
    "B:11": (
        r"\Omega_{\mathrm{fiscal}} = \left(\mathrm{Tax}_{\mathrm{GST+Cap+Beq},27} + \mathrm{Tax}_{\mathrm{PAYE},28}\right) - "
        r"\left(\mathrm{Burden}_{\mathrm{Exits\,1,2,4}} + \mathrm{Outlay}_{\mathrm{Infra+Health+Super},26}\right)"
    ),
    "B:12": (
        r"\begin{aligned}"
        r"\Delta_{\mathrm{syn},w} &= \mathrm{CE}_k(A_w \cup B_w) - \mathrm{CE}_k(A_w) - \mathrm{CE}_k(B_w) > 0 \\"
        r"\mathrm{CE}^{\mathrm{SS2}} &= 11.23\text{ pp (Isolated)} + 13.47\text{ pp (Wedges 1--4)} = +24.70\text{ pp}"
        r"\end{aligned}"
    ),
    "B:13": (
        r"\begin{aligned}"
        r"\Phi(t) &= \Phi_1 + \frac{\Phi_2 - \Phi_1}{1 + \exp\left(-\xi_{\mathrm{ramp}}(t - T_1)\right)} \\"
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
        r"u_{\mathrm{rel}}(\mathrm{Frac}_{\mathrm{struggling}}, S_t) &= \chi_{\mathrm{rel}}\left[(0.285 - \mathrm{Frac}_{\mathrm{struggling}}) + 0.015\,(S_t - 100)\right] \\"
        r"S_t &: 100.0 \longrightarrow 118.4 \longrightarrow 126.0"
        r"\end{aligned}"
    ),
    "T:00": (
        r"\mathbb{E}_{\mu_k}\left[f(a, h, \theta_c, z)\right] \ll "
        r"f\left(\mathbb{E}[a],\,\mathbb{E}[h],\,\mathbb{E}[\theta_c],\,\mathbb{E}[z]\right)"
    ),
    "T:01": (
        r"S_t = 100.0 + \zeta_{\mathrm{hardship}}(0.220 - \mathrm{Frac}_{\mathrm{struggling},t}) + "
        r"\zeta_{\mathrm{ret}}(0.1093 - \mathrm{Emig}_{\mathrm{Nat},t}) - "
        r"\zeta_{\mathrm{churn}}\max(0,\,\mathrm{Churn}_t - \overline{\mathrm{Churn}})"
    ),
    "T:02": (
        r"\begin{aligned}"
        r"W_f &= u_f(d_t) + \beta_{\mathrm{hyp}}\,\delta\,V^{\prime}_f(a', h', \theta'_c) \\"
        r"e_{\mathrm{total}} &= e_{\mathrm{real}} + e_{\mathrm{avoidance}} + \bar{e}_{\mathrm{bargaining}} \ll e_{\mathrm{Laffer}}"
        r"\end{aligned}"
    ),
    "T:03": (
        r"K_{\mathrm{whanau}}^{\mathrm{net}}(i_c, z, a, J_r, k) = "
        r"K_{\mathrm{whanau},k}(J_r, Q_k) - \psi_{\mathrm{sandwich}}\cdot "
        r"\mathbb{I}_{\mathrm{Super} > 65}\cdot \mathbb{I}_{\mathrm{distress}}(i_c, z, a) < 0"
    ),
    "T:04": (
        r"1 - \phi_{\mathrm{adj}}(\Delta s)^2:\quad "
        r"1 - 0.180(1)^2 = 0.820\;\text{(Single-Shot)} \quad\text{vs.}\quad "
        r"1 - 0.180\left(\frac{1}{3}\right)^2 = 0.980"
    ),
    "T:05": (
        r"\begin{aligned}"
        r"P_{G4 \to G5}:\quad &\text{Retained Top-Tier Talent in SS0} \\"
        r"&\longrightarrow 61\%\text{ Node 19 } (z_\ell\text{ Speculation}) \;\text{ vs. }\; 29\%\text{ Node 20 } (z_h\text{ Builders})"
        r"\end{aligned}"
    ),
    "T:06": (
        r"P_t(k \to m \,|\, a_1, h_1, z_1) \propto "
        r"\exp\left(\frac{V_{m,t}\left(\max(a_{\min},\,a_1 - \kappa_{k \to m}),\,h_1,\,z_1,\,1\right)}{\varrho_{\mathrm{mig}}}\right)"
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
        r"S_f(n_f) = u_f\left(c_f(n_f)\right) + \beta_{\mathrm{hyp}}\,\delta\,V^{\prime}_f(n_f) - "
        r"\theta_\tau\,\psi_{\mathrm{time}}\,n_f + \omega_{\mathrm{ECE}}\,G_{\mathrm{ECE}}\,n_f - \psi_Q\,Q_k\,n_f < \underline{U}_f"
    ),
    "T:10": (
        r"Q_{k,t} = \sum_{s=1}^{\infty}\left(\frac{G_k}{R(\tau_a)}\right)^{s} d_{\mathrm{land},k,t} + B_{\mathrm{land},k,t} "
        r"\implies B_{\mathrm{land},k,t} > 0 \;\text{ whenever }\; G_k \geq R(\tau_a = 0)"
    ),
    "C:01": (
        r"R_k(z_f;\,\Delta t) = (1 - \tau_a)^{\Delta t} + (1 - \tau_k)\left["
        r"r(\Delta t) + \max\left\{0,\;\pi_k^* - \left(r(\Delta t) + \delta_k^{\mathrm{shock}}(\Delta t)\right)\right\}\cdot \lambda_{\mathrm{col}}"
        r"\right]"
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
        r"\Psi_{J=5} = -\psi_{\mathrm{unemp}}\left[\mathbb{I}(z_p \in Z_{\mathrm{distress}}) + \lambda_{\mathrm{psy}}(M_{\mathrm{mentor}})\right]"
        r"(1 - \zeta_{\mathrm{buf}} M_{\mathrm{mentor}})(1 - 0.55\,K_{\mathrm{whanau}}^{\mathrm{eff}}) + \kappa_{\mathrm{up}} M_{\mathrm{mentor}}"
    ),
    "C:05": (
        r"\begin{aligned}"
        r"\ell_{\mathrm{eff}} &= \max(0,\,\ell - I_h), \quad I_h \in \{0,\,0.15,\,0.30\} \\"
        r"\lambda_{\mathrm{cred}}^{\mathrm{actuarial}}(t) &\longrightarrow 1.0 \quad \text{under Monilukutaito epistemic framing}"
        r"\end{aligned}"
    ),
    "C:06": (
        r"P_t(k \to m \,|\, a_1, h_1, z_1) = "
        r"\frac{\exp\left(V_{m,t}\left(\max(a_{\min},\,a_1 - \kappa_{k \to m}),\,h_1,\,z_1,\,1\right) / \varrho_{\mathrm{mig}}\right)}"
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
        r"T_k^{\mathrm{SS2}} &= T_k^{\mathrm{SS0}} + (1 - \psi_{\mathrm{retire},T})\left(T_k^{\mathrm{SS1}} - T_k^{\mathrm{SS0}}\right) \quad (\psi_{\mathrm{retire},T} = 0.850) \\"
        r"&\implies \Delta\tau_{\ell,\mathrm{retire}} = -0.0064 \quad (-0.64\text{ pp})"
        r"\end{aligned}"
    ),
    "K:01": (
        r"\frac{\partial^2 \theta_c^{\mathrm{ces},2}}{\partial \theta_c^{\mathrm{ret}}\,\partial X_m} = "
        r"(1 - \phi_2)\,\gamma_{2,\mathrm{self}}\,\gamma_{2,m}\,(\theta_c^{\mathrm{ces},2})^{1 - 2\phi_2}"
        r"(\theta_c^{\mathrm{ret}}\cdot X_m)^{\phi_2 - 1} > 0"
    ),
    "K:02": (
        r"\tilde{V}_{k,t+1} = \left(1 - \lambda_{\mathrm{cred}}(t)\right)V_{k,t+1}^{\mathrm{perm,SS1}} + "
        r"\lambda_{\mathrm{cred}}(t)\,V_{k,t+1}^{\mathrm{full,SS2}}"
    ),
    "K:03": (
        r"G_{\mathrm{ECE},1}^{\mathrm{eff}} \to \Theta_1 \;+\; \mathrm{GrowingChange} \to M_{\mathrm{mentor}} \;+\; "
        r"\mathrm{LFPI}\,(1.60\times\text{--}2.16\times) \to \Delta\mu_{z,k} \implies \psi_{\mathrm{retire},T} = 0.85"
    ),
    "K:04": (
        r"p_H(a, z, Q_k) = \left(\xi_{\mathrm{hh}}(a, Q_k)\,\mathrm{rh}_k + "
        r"(1 - \xi_{\mathrm{hh}})\frac{\mathrm{rr}_k}{0.5\,\bar{\chi}}\right)"
        r"\left(1 + 0.12\cdot\mathbb{I}(a < 0.08\,Q_k \;\land\; z < 0.85)\right)"
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
        r"\lambda_{\mathrm{cred}}^{\mathrm{actuarial}}(t) = \min\left\{1,\; \lambda_0 + (1 - \lambda_0)\cdot"
        r"\max\left(0,\;\frac{V^{(\mathrm{Fiscal})}(H;\,0.02) / C^{(\mathrm{Inv})}(t) - 1}{3.50 - 1}\right)\right\}"
    ),
    "K:08": (
        r"Y_{\mathrm{VFI}} = \sum_{a,h,\theta_c,z} \mu_k(a, h, \theta_c, z, j)\cdot f(a, h, \theta_c, z)"
    ),
    "K:09": (
        r"K_{\mathrm{whanau}}^{\mathrm{eff}}(k) = K_{\mathrm{whanau},0}(k)\cdot \Phi_{\mathrm{time}}(A_{\mathrm{super}})\cdot "
        r"\min\left(1.15,\;\max\left(0.50,\;\frac{p_{\mathrm{super}}}{0.18}\left(\frac{Q_{k,0}}{Q_k}\right)^{0.35}\right)\right)"
    ),
    "K:10": (
        r"\mathrm{CE}_{\mathrm{Nat}}(\text{All 4 Coalitions}) = +24.70\% \;\gg\; "
        r"\sum_{c=1}^{4} \mathrm{CE}_{\mathrm{Nat}}(\text{Silo}_c\text{ alone vs. LTFM} < 0)"
    ),
    "N:01": (
        r"\begin{aligned}"
        r"\eta_{k,m}(t) &= \left(1 - \delta_{\mathrm{adopt}}\,e^{-\lambda_{\mathrm{adopt}}(t - t_0)}\right)"
        r"\left[1 - \tau_{\mathrm{fric},\min} - (\tau_{\mathrm{fric},0} - \tau_{\mathrm{fric},\min})\,e^{-\gamma_{\mathrm{learn}} L_m(t-1)}\right] \\"
        r"&\quad \times \left[1 - \phi_{\mathrm{adj}}\left(\Delta s_{k,m}(t)\right)^2\right]"
        r"\end{aligned}"
    ),
    "N:02": (
        r"G_{\mathrm{ECE},s}^{\mathrm{net}} = (1 - \tau_{\mathrm{agency}})\,G_{\mathrm{ECE},s}^{\mathrm{gross}}:\quad "
        r"\tau_{\mathrm{agency}} = 0.32\;\text{(fragmented silos)} \longrightarrow \leq 0.08\;\text{(high-trust commissioning)}"
    ),
    "N:03": (
        r"\Theta_s = \left[\gamma_{s,\mathrm{self}}\,\theta_c^{\phi_s} + \gamma_{s,\mathrm{inv}}\,I_s^{\phi_s} + "
        r"\gamma_{s,\mathrm{par}}\,h_p^{\phi_s}\right]^{1/\phi_s}, \qquad \phi_1 = +0.35,\;\; \phi_2 = -0.95"
    ),
    "N:04": (
        r"\frac{V_{k,t_0}^{(\mathrm{Fiscal})}(H=25;\,r = 0.02)}{C_{k,\mathrm{realized}}^{(\mathrm{Inv})}(t_0)} = "
        r"\frac{35.25\text{B}}{9.19\text{B}} = 3.84\times > \chi_{\mathrm{target}}\;(3.50) \quad \text{at Year 5}"
    ),
    "N:05": (
        r"M_{\mathrm{trust}}(K_{\mathrm{whanau}}^{\mathrm{net}}, M_{\mathrm{mentor}}) = "
        r"M_{\mathrm{mentor}}\cdot\left(0.45 + 0.55\cdot\min\left(1.0,\;\frac{K_{\mathrm{whanau}}^{+}}{0.35}\right)\right)"
    ),
    "N:06": (
        r"\begin{aligned}"
        r"Y_k &= Z_k(\Gamma_k, H_k)\cdot K_k^{\alpha_k}\,H_k^{1 - \alpha_k}, \\"
        r"&\text{where } \Gamma_k \to z_{h,k} \;\land\; \text{retained } h_6\text{--}h_7\text{ talent compound } Z_k"
        r"\end{aligned}"
    ),
    "N:07": (
        r"\begin{aligned}"
        r"1 - \tau_{\mathrm{fric}}(t) &= 1 - 0.035 - (0.280 - 0.035)\exp\left(-0.450\,L_m(t-1)\right) \\"
        r"\text{Local adoption} &= 1 - 0.220\exp\left(-0.350\,(t - t_{k,m}^0)\right)"
        r"\end{aligned}"
    ),
    "N:08": (
        r"\begin{aligned}"
        r"n^t &= n^c \cdot \beta_{\mathrm{hyp}}^{1/\epsilon} \quad \text{(Cao \& Li Prop. 5)} \\"
        r"S_f\left(n_f;\;Q_k \downarrow,\, G_{\mathrm{ECE}} \uparrow,\, \Phi_{\mathrm{time}}(64) = 1.081\right) &\geq \underline{U}_f"
        r"\end{aligned}"
    ),
    "N:09": (
        r"\begin{aligned}"
        r"T_{\mathrm{IG}} &= Q_h \times Q_a \times \Pi_{\mathrm{mig}} \quad \text{coupled with } \mathrm{Solve\_Spatial\_GE\_Loop}(\mathrm{HH}_{1..4},\,\mathrm{Firm}_{1..4}) \\"
        r"&\implies +24.70\%\text{ CE (SS2 Pre-NDC)}"
        r"\end{aligned}"
    ),
    "H:01": (
        r"\begin{aligned}"
        r"\mathrm{OBEGAL}_{\mathrm{cash}}(t \leq 3) &< 0, \quad \text{while } V_{\mathrm{Nat},t=5}^{(\mathrm{Fiscal})}(H=25;\,r=0.02) = +\text{NZD } 35.25\text{B}\;(3.84\times) \\"
        r"&\land\; \text{Direct Savings} = +\text{NZD } 10.68\text{B}\;(1.16\times)"
        r"\end{aligned}"
    ),
    "H:02": (
        r"\begin{aligned}"
        r"\Psi_{\mathrm{adolescent}} &= -\psi_{\mathrm{unemp}}\,\mathbb{I}(i_c < 0.01)(1 - 0.55\,K_{\mathrm{whanau}}^{\mathrm{net}})(1 - 0.80\,M_{\mathrm{trust}}) \\"
        r"M_{\mathrm{trust}} &\longrightarrow 0.45\,M_{\mathrm{mentor}} \quad \text{without whānau trust}"
        r"\end{aligned}"
    ),
    "H:03": (
        r"\mathrm{crowd}_{1\mathrm{D}}(a_p;\,k) = W_{\mathrm{cell},3}\,\psi_{\mathrm{crowd,sev}} + "
        r"(W_{\mathrm{cell},4} - W_{\mathrm{cell},3})(0.35\,\psi_{\mathrm{crowd,ahc}}), \quad \psi_{\mathrm{crowd}}: 0.14 \to 0.18"
    ),
    "H:04": (
        r"P_{\mathrm{emig},t}(k \to \text{Abroad} \,|\, a_1, h_1, z_1) = "
        r"\frac{1}{1 + \sum_{r=1}^{4}\exp\left(\left(V_{r,t}(a_1 - \kappa_{k \to r}, h_1, z_1, 1) - V_{\mathrm{Abroad},t}\right) / 0.180\right)}"
    ),
    "H:05": (
        r"\begin{aligned}"
        r"\psi_{\mathrm{wear}}(h, j) &= 1.0 + 0.35\,\mathbb{I}(\mathrm{age}_j \geq 65)\max\left(0,\;\frac{1.00 - h}{0.55}\right) \\"
        r"1 - s_j^{\mathrm{eff}}(h, j) &= \min\left(0.99,\;(1 - s_j)\exp\left(0.18(1 - h)\right)\right)"
        r"\end{aligned}"
    ),
    "H:06": (
        r"\begin{aligned}"
        r"G_{\mathrm{ece},s}^{\mathrm{eff}}(Q_k) &= G_{\mathrm{ece},s}\cdot \left(\frac{Q_{\mathrm{reg,base},k}}{Q_k}\right)^{0.35} \\"
        r"\Phi_{\mathrm{home}}(p_{\mathrm{super}}, Q_k) &= \frac{p_{\mathrm{super}}}{0.18}\left(\frac{Q_{k,0}}{Q_k}\right)^{0.35}"
        r"\end{aligned}"
    ),
    "H:07": (
        r"\begin{aligned}"
        r"r_{h,k}^{\mathrm{rent}} &= \left(1 + \mu_{\mathrm{maint}} - \frac{G_k}{R(\tau_a)}\right)Q_k \\"
        r"&\text{When } \tau_a = 0 \;\land\; \delta_{H,\mathrm{Akl}} = 0.10,\;\text{demand subsidies capitalize into } Q_k"
        r"\end{aligned}"
    ),
    "H:08": (
        r"\begin{aligned}"
        r"\pi_k^*(z_f, w_k;\,M_{\mathrm{olig}}) &\text{ depressed in Rural/Small } (z_f \to z_\ell) \\"
        r"&\text{while consumer price index inflated by } M_{\mathrm{olig}} = [1.08,\,1.07,\,1.05,\,1.04]"
        r"\end{aligned}"
    ),
    "H:09": (
        r"\begin{aligned}"
        r"\Delta G_{\mathrm{def}} &= +0.018\,Y \quad (+\text{NZD } 8.0\text{B/yr}) \\"
        r"\mathrm{CE}(\mathrm{SS0} + \mathrm{Def}) &= -21.69\% \quad \text{vs.} \quad \mathrm{CE}(\mathrm{SS2} + \mathrm{Def}) = +21.18\%\;\text{(Pre-NDC)}"
        r"\end{aligned}"
    ),
    "H:10": (
        r"\begin{aligned}"
        r"\text{When } h_1 \in \{h_1, h_2\} \;\land\; Q_k = 3.10:\quad &a_1 + E < 0.20\,Q_k \;\land\; R_k(z_\ell)\text{ dominates} \\"
        r"&\implies 42\%\text{ grant dissipation (NZD } 3.8\text{B waste)}"
        r"\end{aligned}"
    ),
    "E:01": (
        r"\begin{aligned}"
        r"e_{\mathrm{tot}} &= \frac{y_{\mathrm{disp}} - \bar{e}_k(t) - \mathbb{I}_{j \in J_c}(1 - s_{\mathrm{sub}})\,i_c - a'}{1 + \tau_c} \\"
        r"\Delta\bar{e}_k &< 0 \implies \text{relaxes } i_c^* = 0"
        r"\end{aligned}"
    ),
    "E:02": (
        r"\Delta A_{\mathrm{prec}} = \sum_{k} \omega_{\mathrm{HH},k}\left["
        r"\int a_{\mathrm{fin}}\,d\mu_k(\sigma_{z_2} = 0.25) - "
        r"\int a_{\mathrm{fin}}\,d\mu_k^*(\sigma_{z_2} \to 0,\,\mathrm{pv}=5)"
        r"\right] \geq \mathrm{CapEx}_{\mathrm{grid}}"
    ),
    "E:03": (
        r"\sum_{k=1}^{4} \omega_{F,k}\int (k_f - a_f)\,d\Gamma_{k,t} + B_{\mathrm{gov},t} = "
        r"\sum_{k=1}^{4} \omega_{\mathrm{HH},k,t}\int a_{\mathrm{fin}}\,d\mu_{k,t} + B_t^* "
        r"\implies \Delta r = -60\text{ to }-100\text{ bps}"
    ),
    "E:04": (
        r"T_{k,t}^{\mathrm{Mix}} = \left(1 - s_{k,m}(t)\right)\,T_k^{\mathrm{Waiter}}(G_{m,0}) + "
        r"s_{k,m}(t)\,T_k^{\mathrm{Active}}\left(G_{k,m}^{\mathrm{eff}}(t)\right)"
    ),
    "E:05": (
        r"\mathrm{Jump2}_{\mathrm{SS2}}(t) = \sum_{w=1}^{13} \Delta s_m(w)\cdot K_{\mathrm{mat}}(t - w - T_{\mathrm{gen},m})"
    ),
    "P:01": (
        r"\begin{aligned}"
        r"\Omega_{\mathrm{debt}} &= \alpha_{\mathrm{split}}\cdot \Omega_{\mathrm{reform}}, \qquad "
        r"\Omega_{\mathrm{reinv}} = (1 - \alpha_{\mathrm{split}})\cdot \Omega_{\mathrm{reform}} \\"
        r"&\text{triggered when } B_{\mathrm{gov}} / Y \leq \mathrm{Debt\_Gate}"
        r"\end{aligned}"
    ),
    "P:02": (
        r"\Psi_{J=5}(\text{rohe}) = f\left(M_{\mathrm{trust}}(K_{\mathrm{whanau}}^{\mathrm{net}}, M_{\mathrm{mentor}}),\; G_{\mathrm{ECE},s}^{\mathrm{eff}}(Q_k)\right)"
    ),
    "P:03": (
        r"\Delta\mathrm{CE}_{\mathrm{tot}} = \Delta\mathrm{CE}_{\mathrm{PE}}(\text{fixed } w, r, Q, \mu_1) + "
        r"\Delta\mathrm{CE}_{\mathrm{GE}}(w^*, r^*, Q^*) + \Delta\mathrm{CE}_{\mathrm{IG}}(\text{endogenous } T_{\mathrm{IG}}\,\mu_1^*)"
    ),
    "P:04": (
        r"\pi_k^*(z_f, w_k) = \alpha_k\left(\frac{1 - \alpha_k}{w_k}\right)^{\frac{1 - \alpha_k}{\alpha_k}} z_f^{1/\alpha_k}, "
        r"\quad \text{amplified by } \lambda_{\mathrm{col}} = 2.50"
    ),
    "P:05": (
        r"\mathrm{CE}_{\mathrm{full}}^{\mathrm{SS2}}\;(+24.92\%) = \mathrm{CE}_{\mathrm{pre\text{-}NDC}}^{\mathrm{SS2}}\;(+24.70\%) + "
        r"\Delta\mathrm{CE}_{\mathrm{NDC+Biogenic+CleanGreen}}\;(\text{Wedge 5} = +1.03\%)"
    ),
    "P:06": (
        r"\Delta\mathrm{CE}(\text{Shock} \,|\, \mathrm{SS2}) - \Delta\mathrm{CE}(\text{Shock} \,|\, \mathrm{SS0}) \gg 0"
    ),
    "P:07": (
        r"\mathrm{Ceiling}(\mathrm{Rival}) < \mathrm{CE}_{\mathrm{Aotearoa}}^{\mathrm{SS2}} \quad "
        r"\text{whenever Rival omits } \geq 1\text{ of }\{\text{Lens 1 HC},\;\text{Lens 2 Spatial},\;\text{Lens 3 LVT/Actuarial}\}"
    ),
    "P:08": (
        r"y_{\mathrm{top}}(\tau) - y_{\mathrm{bot}}(\tau) = \left(1 - s(\tau)\right)H_L + s(\tau)H_R > 0, \qquad "
        r"s(\tau) = \frac{1}{2}\left(1 - \cos(\pi\tau)\right)"
    ),
}


# ---------------------------------------------------------------------------
# 2. Fallback ASCII-to-LaTeX Compiler (for future / modded cards in YAML)
# ---------------------------------------------------------------------------
_GREEK_LETTERS = {
    "alpha": r"\alpha", "beta": r"\beta", "gamma": r"\gamma", "Gamma": r"\Gamma",
    "delta": r"\delta", "Delta": r"\Delta", "epsilon": r"\epsilon", "varepsilon": r"\varepsilon",
    "zeta": r"\zeta", "eta": r"\eta", "theta": r"\theta", "Theta": r"\Theta",
    "iota": r"\iota", "kappa": r"\kappa", "lambda": r"\lambda", "Lambda": r"\Lambda",
    "lamba": r"\lambda",
    "mu": r"\mu", "nu": r"\nu", "xi": r"\xi", "Xi": r"\Xi",
    "pi": r"\pi", "Pi": r"\Pi", "rho": r"\rho", "sigma": r"\sigma", "Sigma": r"\Sigma",
    "tau": r"\tau", "upsilon": r"\upsilon", "phi": r"\phi", "Phi": r"\Phi",
    "chi": r"\chi", "psi": r"\psi", "Psi": r"\Psi", "omega": r"\omega", "Omega": r"\Omega",
    "ell": r"\ell",
}

_GREEK_RE = re.compile(r"(?<!\\)\b(" + "|".join(sorted(_GREEK_LETTERS, key=len, reverse=True)) + r")(?=_|\b)")
_VARGREEK_RE = re.compile(r"(?<!\\)\b(var(?:" + "|".join(_GREEK_LETTERS.keys()) + r"))(?=_|\b)")
_FUNC_MAP = {
    "int": r"\int", "sum": r"\sum", "prod": r"\prod", "exp": r"\exp",
    "min": r"\min", "max": r"\max", "inf": r"\infty", "prop": r"\propto", "iff": r"\iff",
}
_FUNC_RE = re.compile(r"(?<!\\)\b(" + "|".join(_FUNC_MAP.keys()) + r")(?=_|\^|\(|\s|\b)")


def _wrap_balanced_paren_exponents(s: str) -> str:
    """Converts ^(expr) -> ^{(expr)} with full nested-parenthesis balance."""
    out: List[str] = []
    i, n = 0, len(s)
    while i < n:
        if s[i] == "^" and i + 1 < n and s[i + 1] == "(":
            depth, j = 0, i + 1
            while j < n:
                if s[j] == "(":
                    depth += 1
                elif s[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if depth == 0:
                out.append("^{(" + s[i + 2 : j] + ")}")
                i = j + 1
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def ascii_eq_to_latex(eq: str) -> str:
    """Fallback converter for new/unregistered cards in study_cards.yaml."""
    if not eq:
        return ""
    s = str(eq).strip()
    s = re.sub(r"(?<!\\)%", r"\\%", s)
    for old, new in [
        ("===", r" \equiv "), ("==>", r" \Longrightarrow "), ("=>", r" \Rightarrow "),
        ("<->", r" \leftrightarrow "), ("->", r" \to "), ("!=", r" \neq "),
        (">=", r" \geq "), ("<=", r" \leq "), (">>", r" \gg "), ("<<", r" \ll "),
        ("≈", r" \approx "), (".*", r" \odot "),
    ]:
        s = s.replace(old, new)
    for old, new in [
        ("theta_bar", r"\bar{\theta}"), ("e_bar", r"\bar{e}"), ("g_bar", r"\bar{g}"),
        ("h_bar", r"\bar{h}"), ("H_bar", r"\bar{H}"), ("U_bar", r"\underline{U}"),
        ("Churn_bar", r"\overline{\mathrm{Churn}}"), ("chi_bar", r"\bar{\chi}"),
        ("V_tilde", r"\tilde{V}"), ("M_hat", r"\hat{M}"),
    ]:
        s = s.replace(old, new)

    s = _wrap_balanced_paren_exponents(s)
    s = _VARGREEK_RE.sub(lambda m: "\\" + m.group(1), s)
    s = _GREEK_RE.sub(lambda m: _GREEK_LETTERS[m.group(1)], s)
    s = _FUNC_RE.sub(lambda m: _FUNC_MAP[m.group(1)], s)
    s = re.sub(r"(?<=\s)in(?=\s)", r"\\in", s)
    if r"\begin{aligned}" not in s:
        s = re.sub(r"(?<!\\)&", r"\\land", s)
    s = re.sub(r"_([A-Za-z0-9]+(?:,[A-Za-z0-9]+)*)", r"_{\1}", s)
    s = re.sub(r"\s+\*\s+", lambda _: r" \cdot ", s)
    return s


def resolve_card_latex(card_or_study: Dict[str, Any], cid: str | None = None) -> str:
    """Primary entry point for all 3 renderers."""
    card_id = (cid or str(card_or_study.get("id", ""))).strip()
    if card_id in CANONICAL_EQUATIONS:
        return CANONICAL_EQUATIONS[card_id]
    explicit = card_or_study.get("latex_equation")
    if explicit:
        return str(explicit).strip()
    return ascii_eq_to_latex(str(card_or_study.get("key_equation", ""))).strip()


# ---------------------------------------------------------------------------
# 3. Shared HTML Sizing & MathJax SVG Overflow Protection CSS
# ---------------------------------------------------------------------------
def pick_eq_size_class(latex_eq: str) -> str:
    """Picks .eq-size-lg / .eq-size-md / .eq-size-sm based on visual line length."""
    lines = latex_eq.split(r"\\")

    def _vis_len(ln: str) -> int:
        s = re.sub(r"\\(begin|end)\{[^}]+\}", "", ln)
        s = re.sub(r"\\(mathrm|text|mathbf|mathcal|mathbb)\{([^}]*)\}", r"\2", s)
        s = re.sub(r"\\[A-Za-z]+", "X", s)
        s = re.sub(r"[{}_^]", "", s)
        return len(s.strip())

    max_len = max((_vis_len(ln) for ln in lines), default=0)
    if len(lines) >= 2:
        return "eq-size-md" if max_len <= 78 else "eq-size-sm"
    if max_len <= 62:
        return "eq-size-lg"
    if max_len <= 88:
        return "eq-size-md"
    return "eq-size-sm"


def get_mathjax_svg_fit_css(
    container_selector: str,
    max_height: str,
    print_max_height: str | None = None,
) -> str:
    """
    Shared CSS snippet ensuring MathJax 3 SVGs scale proportionally inside their
    bounding box without horizontal scrollbars or right-edge clipping.
    """
    print_rule = ""
    if print_max_height:
        print_rule = f"""
    @media print {{
      {container_selector} mjx-container > svg {{
        max-height: {print_max_height} !important;
      }}
    }}"""
    return f"""
    {container_selector} {{
      overflow: hidden !important;
    }}
    {container_selector} mjx-container {{
      max-width: 100% !important;
      margin: 0 !important;
    }}
    {container_selector} mjx-container > svg {{
      max-width: 100% !important;
      max-height: {max_height} !important;
      height: auto !important;
    }}{print_rule}
    """


# ---------------------------------------------------------------------------
# 4. Matplotlib MathText Adapter for render_study_pptx.py (0 Fallbacks)
# ---------------------------------------------------------------------------
def _extract_braced(s: str, start_idx: int) -> tuple[str, int]:
    depth = 0
    for i in range(start_idx, len(s)):
        if s[i] == "{" and (i == 0 or s[i - 1] != "\\"):
            depth += 1
        elif s[i] == "}" and (i == 0 or s[i - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return s[start_idx + 1 : i], i + 1
    return s[start_idx + 1 :], len(s)


def _replace_underbrace_balanced(s: str) -> str:
    token = r"\underbrace"
    while token in s:
        idx = s.find(token)
        i = idx + len(token)
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s) or s[i] != "{":
            s = s[:idx] + s[idx + len(token) :]
            continue
        expr, next_i = _extract_braced(s, i)
        while next_i < len(s) and s[next_i].isspace():
            next_i += 1
        if next_i < len(s) and s[next_i] == "_":
            next_i += 1
            while next_i < len(s) and s[next_i].isspace():
                next_i += 1
            if next_i < len(s) and s[next_i] == "{":
                lbl, end_i = _extract_braced(s, next_i)
                s = s[:idx] + f"\\left[{expr}\\right]_{{{lbl}}}" + s[end_i:]
                continue
        s = s[:idx] + f"\\left[{expr}\\right]" + s[next_i:]
    return s


def _replace_text_macros(s: str) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        inner = inner.replace(r"\&", "and").replace("&", "and")
        inner = inner.replace("ā", "a").replace("Ā", "A")  # Computer Modern glyph safety
        inner = inner.replace("%", r"\%").replace("--", "-").replace("–", "-").replace("—", "-")
        inner = inner.replace(" ", r"\ ")
        return r"\mathrm{" + inner + "}"

    return re.sub(r"\\(?:text|textbf|operatorname)\{([^{}]*)\}", repl, s)


def to_mathtext_lines(latex_str: str) -> List[str]:
    """
    Converts canonical LaTeX (including \\begin{aligned} ... \\end{aligned})
    into 1 or 2 clean lines strictly valid for matplotlib.mathtext.MathTextParser.
    """
    s = " ".join(latex_str.strip().strip("$").splitlines()).strip()

    if r"\begin{aligned}" in s:
        s = s.replace(r"\begin{aligned}", "").replace(r"\end{aligned}", "").strip()
        parts = [p.strip() for p in s.split(r"\\") if p.strip()]
    elif len(s) > 115 and r"\qquad" in s:
        parts = [p.strip() for p in s.split(r"\qquad", 1)]
    elif len(s) > 115 and r"\quad" in s:
        parts = [p.strip() for p in s.split(r"\quad", 1)]
    elif len(s) > 155 and r"\Longrightarrow" in s:
        idx = s.find(r"\Longrightarrow")
        parts = [s[:idx].strip(), r"\Longrightarrow " + s[idx + len(r"\Longrightarrow") :].strip()]
    else:
        parts = [s]

    cleaned_lines: List[str] = []
    for p in parts:
        # Protect escaped \& before stripping alignment-& tabs
        line = p.replace(r"\&", "and")
        line = line.replace("&=", "=").replace("&", "")
        line = re.sub(
            r"\\xrightarrow\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
            lambda m: f"\\overset{{{m.group(1)}}}{{\\longrightarrow}}",
            line,
        )
        line = re.sub(
            r"\\stackrel\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}",
            lambda m: f"\\overset{{{m.group(1)}}}{{{m.group(2)}}}",
            line,
        )
        line = _replace_underbrace_balanced(line)
        line = re.sub(r"\\substack\{([^{}]*)\}", lambda m: m.group(1).replace(r"\\", ", "), line)
        for _ in range(3):
            line = _replace_text_macros(line)

        line = re.sub(r"\\mathbb\{([A-Z])\}", lambda m: f"\\mathbf{{{m.group(1)}}}", line)
        line = line.replace(r"\tfrac", r"\frac")
        line = line.replace(r"\middle|", r"\,|\,")
        line = line.replace(r"\implies", r"\Rightarrow").replace(r"\iff", r"\Leftrightarrow")
        line = re.sub(r"\\le(?![a-zA-Z])", lambda _: r"\leq", line)
        line = re.sub(r"\\ge(?![a-zA-Z])", lambda _: r"\geq", line)
        line = re.sub(r"\\ne(?![a-zA-Z])", lambda _: r"\neq", line)
        line = line.replace(r"\land", r"\wedge").replace(r"\lor", r"\vee")
        line = line.replace(r"\big", "").replace(r"\Big", "").replace(r"\bigg", "").replace(r"\Bigg", "")
        line = line.replace(r"\qquad", r"\ \ \ ").replace(r"\quad", r"\ \ ")
        line = line.replace("–", "-").replace("—", "-")

        if len(re.findall(r"\\left\b", line)) != len(re.findall(r"\\right\b", line)):
            line = re.sub(r"\\left\b", "", line)
            line = re.sub(r"\\right\b", "", line)

        cleaned_lines.append(line.strip())

    return [ln for ln in cleaned_lines if ln]
