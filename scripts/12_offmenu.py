"""Discrete condition: choices that are NOT on the menu ("off-menu"), and how much they matter.

With the original prompts the model sometimes names a pair that is not among the 11 options, e.g. it
answers ($93.00, $0.00) when the menu contains ($0.00, $93.00) but only ($64.00, $0.00) as the A corner:
it keeps the larger amount but moves it to the first slot. Such a reply is not a feasible choice, so the
main analysis treats it as invalid (rule "strict"). This script reports how often it happens and
recomputes the indices under three rules:
  strict : off-menu rounds dropped; subjects need >= 20 valid rounds (as in 03_indices.py)
  amount : off-menu pair mapped to the menu option with the same two amounts in swapped order
           (the model got the amount right and the slot wrong)
  slot   : (X, 0) mapped to the A corner, (0, X) to the B corner
           (the model got the slot right - "from Asset A", "for me", "today" - and the amount wrong)
Output: results/offmenu_rates.csv, results/offmenu_robustness.csv

  python scripts/12_offmenu.py
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src import rp
from src.dataio import load_gpt, subject_arrays
from src.demand import spearman_subject
from src.parse import DECIDE, NUM
from src.prices import discrete_options

PAIR = r"\(\s*\$?\s*" + NUM + r"\s*(?:Kg)?\s*,\s*\$?\s*" + NUM


def stated_pair(text):
    """The pair the reply settles on: first pair after the last decision phrase, else the only pair."""
    t = str(text).replace(",", ", ").replace("**", "")
    pairs = [(mo.start(), float(mo.group(1)), float(mo.group(2))) for mo in re.finditer(PAIR, t, flags=re.I)]
    if not pairs:
        return None
    decide = [mo.start() for mo in re.finditer(DECIDE, t, flags=re.I)]
    if decide:
        after = [p for p in pairs if p[0] > decide[-1]]
        if after:
            return after[0][1:]
    distinct = {(a, b) for _, a, b in pairs}
    return distinct.pop() if len(distinct) == 1 else None


def find(opts, a, b):
    for j, (oa, ob) in enumerate(opts):
        if abs(a - oa) < 0.011 and abs(b - ob) < 0.011:
            return j
    return None


df = load_gpt()
df = df[df["condition"] == "discrete"].copy()
if df.empty:
    sys.exit("No discrete-condition data found.")
df["offmenu"] = False
df["pa_amount"], df["pa_slot"] = df["points_a"], df["points_a"]
for i, r in df[~df["valid"]].iterrows():
    opts_full = discrete_options(r["M"], r["N"])
    opts = [(o[2], o[3]) for o in opts_full]
    sp = stated_pair(r["reply"])
    if sp is None or find(opts, *sp) is not None:
        continue
    df.at[i, "offmenu"] = True
    j = find(opts, sp[1], sp[0])                       # swapped order
    if j is not None:
        df.at[i, "pa_amount"] = opts_full[j][0]
    if sp[1] < 0.011:                                  # (X, 0): slot A
        df.at[i, "pa_slot"] = C.ENDOWMENT
    elif sp[0] < 0.011:                                # (0, X): slot B
        df.at[i, "pa_slot"] = 0.0

rates = (df.groupby(["source", "domain"])
         .agg(rounds=("valid", "size"), invalid=("valid", lambda s: (~s).sum()), offmenu=("offmenu", "sum"))
         .assign(offmenu_rate=lambda d: d["offmenu"] / d["rounds"]).reset_index())
rates.to_csv(C.RESULTS / "offmenu_rates.csv", index=False)
print("Off-menu choices in the discrete condition:\n", rates.round(3).to_string(index=False))

out = []
for rule, col in [("strict", "points_a"), ("amount", "pa_amount"), ("slot", "pa_slot")]:
    for (src, dom, rep), g in df.groupby(["source", "domain", "rep"]):
        gv = g[g[col].notna()].copy()
        if len(gv) < C.MIN_VALID_ROUNDS:
            continue
        gv["points_a"], gv["points_b"] = gv[col], C.ENDOWMENT - gv[col]
        gv["valid"] = True
        P, X = subject_arrays(gv)
        out.append(dict(rule=rule, source=src, domain=dom, rep=rep, n_valid=len(gv), CCEI=rp.ccei(P, X),
                        spearman=spearman_subject(gv["points_a"], gv["points_b"], gv["M"], gv["N"]),
                        modal_share=gv["points_a"].round().value_counts().iloc[0] / len(gv)))
res = pd.DataFrame(out)
summ = (res.groupby(["source", "domain", "rule"])
        .agg(n_subjects=("CCEI", "size"), CCEI_mean=("CCEI", "mean"),
             share_CCEI_below_0_9=("CCEI", lambda s: (s < 0.9).mean()),
             spearman_mean=("spearman", "mean"), modal_share_mean=("modal_share", "mean"))
        .reset_index())
summ.to_csv(C.RESULTS / "offmenu_robustness.csv", index=False)
print("\nIndices under the three rules:\n", summ.round(3).to_string(index=False))
