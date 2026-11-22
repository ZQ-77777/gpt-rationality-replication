"""Figures 1-4 of the paper, with every model in the data. Output: results/fig1_ccei_cdf.png ... fig4_conditions.png"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C

ind = pd.read_csv(C.RESULTS / "indices.csv").dropna(subset=["CCEI"])
br = pd.read_csv(C.RESULTS / "bronars.csv")
TITLES = {"risk": "Risk", "time": "Time", "social": "Social", "food": "Food"}
llms = sorted((s for s in ind.source.unique() if s != "Human"), key=lambda s: s == C.PAPER_LABEL)
PALETTE = ["#1F4E8C", "#2C7A4B", "#5B47B8"]
STYLE = {m: dict(color=("#8A949E" if m == C.PAPER_LABEL else PALETTE[i % 3]), lw=2) for i, m in enumerate(llms)}
STYLE["Human"] = dict(color="#B42318", ls="--", lw=1.6)


def cdf(ax, x, **kw):
    x = np.sort(np.asarray(x, float))
    x = x[~np.isnan(x)]
    if len(x):
        ax.step(np.r_[x[0], x], np.r_[0, np.arange(1, len(x) + 1) / len(x)], where="post", **kw)


def four_panels(var, fname, xlabel, with_random=False):
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharey=True)
    for ax, dom in zip(axes.flat, C.DOMAINS):
        base = ind[(ind.condition == "baseline") & (ind.domain == dom)]
        if with_random:
            cdf(ax, br[br.domain == dom][var], color="#BCC5C3", ls=":", lw=1.6, label="Simulated (Bronars)")
        for src in ["Human"] + llms:
            cdf(ax, base[base.source == src][var], label=src, **STYLE[src])
        ax.set_title(TITLES[dom]); ax.set_xlabel(xlabel); ax.grid(alpha=.3)
    axes[0, 0].set_ylabel("Cumulative share"); axes[1, 0].set_ylabel("Cumulative share")
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(C.RESULTS / fname, dpi=160); plt.close(fig)


four_panels("CCEI", "fig1_ccei_cdf.png", "CCEI", with_random=True)
four_panels("spearman", "fig2_spearman_cdf.png", "Spearman corr. of ln(xA/xB) and ln(pA/pB)")

# Fig. 3: individual parameters, baseline
pf = C.RESULTS / "params_individual.csv"
if pf.exists():
    par = pd.read_csv(pf)
    par = par[par.condition == "baseline"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    for ax, dom in zip(axes.flat, C.DOMAINS):
        for src in ["Human"] + llms:
            d = par[(par.source == src) & (par.domain == dom)]
            col = STYLE[src]["color"]
            ax.scatter(d["alpha"], d["rho"].clip(lower=-3), marker="o" if src == "Human" else "s", s=20, alpha=.7,
                       facecolors="none" if src == "Human" else col, edgecolors=col, label=src)
        ax.set_title(TITLES[dom]); ax.set_xlabel("alpha"); ax.set_ylabel("rho (clipped at -3)")
        ax.set_xlim(0, 1); ax.grid(alpha=.3)
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(C.RESULTS / "fig3_params.png", dpi=160); plt.close(fig)

# Fig. 4: mean CCEI and 95% CI by condition, one marker per model
conds = [c for c in C.CONDITIONS if c in set(ind[ind.source != "Human"].condition)]
fig, axes = plt.subplots(1, 4, figsize=(15, 4.8), sharey=True)
off = np.linspace(-0.18, 0.18, len(llms)) if len(llms) > 1 else [0.0]
for ax, dom in zip(axes, C.DOMAINS):
    for k, m in enumerate(llms):
        xs, ms, es = [], [], []
        for j, c in enumerate(conds):
            x = ind[(ind.source == m) & (ind.condition == c) & (ind.domain == dom)]["CCEI"]
            if len(x):
                xs.append(j + off[k]); ms.append(x.mean())
                es.append(1.96 * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0)
        lo = [min(e, mm) for e, mm in zip(es, ms)]
        hi = [min(e, 1 - mm) for e, mm in zip(es, ms)]          # CCEI cannot exceed 1
        ax.errorbar(xs, ms, yerr=[lo, hi], fmt="s" if m != C.PAPER_LABEL else "o",
                    color=STYLE[m]["color"], capsize=3, label=m)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels(conds, rotation=70, fontsize=8)
    ax.set_title(TITLES[dom]); ax.grid(alpha=.3)
axes[0].set_ylabel("Mean CCEI (95% CI)"); axes[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(C.RESULTS / "fig4_conditions.png", dpi=160); plt.close(fig)
print("Figures written to", C.RESULTS)
