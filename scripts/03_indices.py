"""Rationality indices per subject + Bronars random benchmark.

Output: results/indices.csv   (source, condition, domain, rep, n_valid, CCEI, HMI, MPI_mean, MPI_max, MCI, spearman)
        results/bronars.csv   (domain, sim, CCEI)
        results/table_indices.csv (summary like the paper's text)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.dataio import load_all, subject_arrays, append_authors
from src import rp
from src.demand import spearman_subject
from src.prices import draw_prices

df = load_all().drop_duplicates(["source", "condition", "domain", "rep", "round"], keep="last")
out = []
for (src, cond, dom, rep), g in df.groupby(["source", "condition", "domain", "rep"]):
    gv = g[g["valid"]]
    rec = dict(source=src, condition=cond, domain=dom, rep=rep, n_valid=len(gv))
    if len(gv) < C.MIN_VALID_ROUNDS:
        out.append(rec)
        continue
    P, X = subject_arrays(gv)
    h, exact = rp.hmi(P, X)
    m_mean, m_max = rp.mpi(P, X)
    rec.update(CCEI=rp.ccei(P, X), HMI=h, HMI_exact=exact, MPI_mean=m_mean, MPI_max=m_max,
               MCI=rp.mci(P, X), GARP_violations=rp.n_violations(rp.cost_matrix(P, X)),
               spearman=spearman_subject(gv["points_a"], gv["points_b"], gv["M"], gv["N"]),
               # share of rounds with the subject's most frequent allocation: flags fixed rules
               # (always the same option / corner) that pass GARP and look price-responsive
               modal_share=gv["points_a"].round().value_counts().iloc[0] / len(gv),
               corner_share=((gv["points_a"] <= 0.5) | (gv["points_b"] <= 0.5)).mean())
    out.append(rec)
ind = append_authors(pd.DataFrame(out), "indices")      # paper's GPT-3.5 and human subjects, if imported
ind.to_csv(C.RESULTS / "indices.csv", index=False)

# Bronars (1987): uniform random choices on the same kind of budget lines
rng = np.random.default_rng(C.SEED_BASE)
br = []
for dom in C.DOMAINS:
    for s in range(C.N_BRONARS):
        pr = draw_prices(rng)
        P = np.column_stack([1 / pr[:, 0], 1 / pr[:, 1]])
        br.append(dict(domain=dom, sim=s, CCEI=rp.bronars(P, rng, 1)[0]))
br = pd.DataFrame(br)
br.to_csv(C.RESULTS / "bronars.csv", index=False)

summ = (ind.dropna(subset=["CCEI"])
        .groupby(["source", "condition", "domain"])
        .agg(n=("CCEI", "size"), CCEI_mean=("CCEI", "mean"),
             share_CCEI_1=("CCEI", lambda s: (s >= 1 - 1e-9).mean()),
             share_CCEI_below_0_9=("CCEI", lambda s: (s < 0.9).mean()),
             HMI_mean=("HMI", "mean"), MPI_mean=("MPI_mean", "mean"), MCI_mean=("MCI", "mean"),
             spearman_mean=("spearman", "mean"),
             share_spearman_neg=("spearman", lambda s: (s < 0).mean()),
             modal_share_mean=("modal_share", "mean"), corner_share_mean=("corner_share", "mean"))
        .reset_index())
summ.to_csv(C.RESULTS / "table_indices.csv", index=False)
viol = br.groupby("domain")["CCEI"].apply(lambda s: (s < 1).mean())
print(summ.round(3).to_string(index=False))
print("\nBronars: share of random subjects violating GARP\n", viol.round(3).to_string())
