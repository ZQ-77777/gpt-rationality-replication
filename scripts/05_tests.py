"""Statistical tests reported in the paper, for every model in the data. Output: results/tests.md

Sources: your model (label = LLM_LABEL / LLM_MODEL), the paper's GPT-3.5 subjects and the human
subjects (both added by 07_import_authors.py). Each test is run for every model present.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.stats import two_sample, one_sample, levene, ols_hc1

ind = pd.read_csv(C.RESULTS / "indices.csv").dropna(subset=["CCEI"])
pf = C.RESULTS / "params_individual.csv"
par = pd.read_csv(pf) if pf.exists() else pd.DataFrame(columns=["source", "condition", "domain", "alpha", "rho"])
llms = sorted((s for s in ind.source.unique() if s != "Human"), key=lambda s: s == C.PAPER_LABEL)
lines = ["# Statistical tests\n", f"Models: {', '.join(llms)}" + ("; humans included" if "Human" in set(ind.source) else "")]


def md(df):
    """DataFrame -> Markdown table (no extra package needed)."""
    cols = list(df.columns)
    fmt = lambda v: f"{v:.4g}" if isinstance(v, (float, np.floating)) else str(v)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(out)


def table(rows, title):
    if rows:
        lines.append(f"\n## {title}\n")
        lines.append(md(pd.DataFrame(rows)))
        lines.append("")


def sel(df, src, cond, dom):
    return df[(df.source == src) & (df.condition == cond) & (df.domain == dom)]


# 1. each model vs humans, baseline (Fig. 1, Fig. 2, SI Figs. S2-S5)
rows = []
for m in llms:
    for dom in C.DOMAINS:
        for var in ["CCEI", "spearman", "HMI", "MPI_mean", "MCI"]:
            a, b = sel(ind, m, "baseline", dom)[var], sel(ind, "Human", "baseline", dom)[var]
            if a.notna().any() and b.notna().any():
                rows.append(dict(model=m, domain=dom, measure=var, **two_sample(a, b)))
table(rows, "Model (a) vs human subjects (b), baseline: two-sided two-sample t-tests")

# 2. each model vs literature mean CCEI 0.918 (SI Fig. S1)
rows = [dict(model=m, domain=d, **one_sample(sel(ind, m, "baseline", d)["CCEI"], C.LITERATURE_MEAN_CCEI))
        for m in llms for d in C.DOMAINS if len(sel(ind, m, "baseline", d))]
table(rows, "Model baseline CCEI vs literature mean 0.918: one-sample t-tests")

# 3. baseline vs each variation, within model (Fig. 4, SI Fig. S24)
rows = []
for m in llms:
    for cond in [c for c in C.CONDITIONS if c != "baseline"]:
        for dom in C.DOMAINS:
            a, b = sel(ind, m, "baseline", dom), sel(ind, m, cond, dom)
            if len(a) and len(b):
                for var in ["CCEI", "spearman"]:
                    rows.append(dict(model=m, condition=cond, domain=dom, measure=var, **two_sample(a[var], b[var])))
table(rows, "Within model: baseline (a) vs variation (b)")

# 4. model vs model, same condition (model generations; original vs paraphrased prompts)
rows = []
for i, ma in enumerate(llms):
    for mb in llms[i + 1:]:
        for cond in C.CONDITIONS:
            for dom in C.DOMAINS:
                a, b = sel(ind, ma, cond, dom), sel(ind, mb, cond, dom)
                if len(a) and len(b):
                    for var in ["CCEI", "spearman"]:
                        rows.append(dict(model_a=ma, model_b=mb, condition=cond, domain=dom, measure=var,
                                         **two_sample(a[var], b[var])))
table(rows, "Model (a) vs model (b), same condition")

# 5. heterogeneity of individual parameters (Levene)
rows = []
for m in llms:
    for cond in ["temp_0.5", "temp_1"]:
        for dom in C.DOMAINS:
            for var in ["alpha", "rho"]:
                a, b = sel(par, m, "baseline", dom)[var], sel(par, m, cond, dom)[var]
                if len(a) > 2 and len(b) > 2:
                    rows.append(dict(model=m, comparison=f"baseline vs {cond}", domain=dom, param=var, **levene(a, b)))
    for dom in C.DOMAINS:
        for var in ["alpha", "rho"]:
            a, b = sel(par, m, "baseline", dom)[var], sel(par, "Human", "baseline", dom)[var]
            if len(a) > 2 and len(b) > 2:
                rows.append(dict(model=m, comparison="model vs Human", domain=dom, param=var, **levene(a, b)))
table(rows, "Heterogeneity of individual parameters: Levene tests (sd_a vs sd_b)")

# 6. difference-in-differences (SI Table S4): is the model's drop larger than the humans' drop?
for m in llms:
    for treat in ["price_framing", "discrete"]:
        rows = []
        for dom in C.DOMAINS:
            d = ind[(ind.domain == dom) & ind.condition.isin(["baseline", treat]) & ind.source.isin([m, "Human"])]
            if len(d.groupby(["source", "condition"]).size()) < 4:
                continue
            is_m, is_t = (d.source == m).astype(float), (d.condition == treat).astype(float)
            X = np.column_stack([np.ones(len(d)), is_m, is_t, is_m * is_t])
            for r in ols_hc1(d["CCEI"], X, ["const", "model", treat, f"model x {treat}"]):
                rows.append(dict(domain=dom, **r))
        table(rows, f"{m}: OLS of CCEI on model, {treat}, interaction (HC1 SE)")

(C.RESULTS / "tests.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
