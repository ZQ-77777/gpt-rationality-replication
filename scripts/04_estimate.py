"""Preference parameters (alpha, rho): pooled (SI Table S2) and individual (Fig. 3, SI Table S3).

Only subjects with CCEI >= 0.95 are used. The paper does not estimate preferences in the
price-framing and discrete conditions (rationality too low), so those are skipped here too.
Output: results/params_pooled.csv, results/params_individual.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.dataio import load_all, append_authors
from src.estimate import shares_and_prices, fit

SKIP = {"price_framing", "discrete"}
df = load_all().drop_duplicates(["source", "condition", "domain", "rep", "round"], keep="last")
df = df[df["valid"] & ~df["condition"].isin(SKIP)]
ind = pd.read_csv(C.RESULTS / "indices.csv")
keep = ind[ind["CCEI"] >= C.CCEI_CUTOFF_FOR_ESTIMATION][["source", "condition", "domain", "rep"]]
keep = keep[keep.source.isin(set(df.source))].astype({"rep": int})   # authors' rows are already estimated
df = df.merge(keep, on=["source", "condition", "domain", "rep"])

pooled, indiv = [], []
for (src, cond, dom), g in df.groupby(["source", "condition", "domain"]):
    s, ratio = shares_and_prices(dom, g["points_a"], g["points_b"], g["M"], g["N"])
    est = fit(s, ratio)
    pooled.append(dict(source=src, condition=cond, domain=dom, n_subjects=g["rep"].nunique(), **est))
    for rep, h in g.groupby("rep"):
        s, ratio = shares_and_prices(dom, h["points_a"], h["points_b"], h["M"], h["N"])
        indiv.append(dict(source=src, condition=cond, domain=dom, rep=rep, **fit(s, ratio)))
    print(f"{src:5s} {cond:16s} {dom:6s} alpha={est['alpha']:.3f} rho={est['rho']:.3f}")

pd.DataFrame(pooled).pipe(append_authors, "params_pooled").to_csv(C.RESULTS / "params_pooled.csv", index=False)
ind_df = pd.DataFrame(indiv).pipe(append_authors, "params")
ind_df.to_csv(C.RESULTS / "params_individual.csv", index=False)
print("\nIndividual-level means / SDs (cf. SI Table S3):")
print(ind_df.groupby(["source", "condition", "domain"])[["alpha", "rho"]].agg(["mean", "std"]).round(3))
