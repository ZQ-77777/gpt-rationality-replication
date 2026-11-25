"""Audit the parser: compare version 1 (src/parse_v1.py, used for the first results) with version 2
(src/parse.py) on every stored reply. Reads data only; changes nothing.

  python scripts/13_parse_audit.py

Writes
  results/parse_audit_summary.csv  per prompt set x condition x domain: rounds, valid (v1, v2),
                                   rounds whose choice changed, rounds that became invalid / valid
  results/parse_audit_diffs.csv    every round where v1 and v2 disagree, with the reply text
  results/parse_audit_sample.csv   200 rounds that v2 counts as valid, for reading by hand:
                                   all rounds parsed by an unlabelled fallback rule (up to 100),
                                   then a random sample of the rest
"""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src import prompts as PARA, prompts_paper as PAPER
from src import parse_v1 as V1
from src import parse as V2
from src.dataio import read_jsonl
from src.prices import discrete_options

SETS = [("paper", C.DATA / "raw"), ("paraphrase", C.DATA / "raw_paraphrase")]


def labels(pset, domain):
    return PAPER.labels(domain) if pset == "paper" else (PARA.DOMAIN[domain]["a"], PARA.DOMAIN[domain]["b"])


def same(a, b):
    return a is not None and b is not None and abs(a - b) < 0.5


rows = []
for pset, folder in SETS:
    if not folder.exists():
        continue
    for f in sorted(folder.glob("*.jsonl")):
        for r in read_jsonl(f):
            cfg = C.CONDITIONS[r["condition"]]
            reply = r.get("reply") or ""
            if cfg["choice"] == "discrete":
                opts = discrete_options(r["M"], r["N"])
                vals = [(o[2], o[3]) for o in opts]
                num = pset != "paper"
                j1, ok1 = V1.parse_discrete(reply, vals, allow_option_number=num)
                d2 = V2.parse_discrete_detail(reply, vals, allow_option_number=num)
                a1 = opts[j1][0] if ok1 else None
                a2 = opts[d2["j"]][0] if d2["valid"] else None
                ok2, rule = d2["valid"], d2["rule"]
            else:
                la, lb = labels(pset, r["domain"])
                a1, _, ok1 = V1.parse_continuous(reply, la, lb)
                d2 = V2.parse_continuous_detail(reply, la, lb)
                a2, ok2, rule = d2["a"], d2["valid"], d2["rule"]
            rows.append(dict(prompts=pset, condition=r["condition"], domain=r["domain"], rep=r.get("rep"),
                             round=r.get("round"), v1_valid=bool(ok1), v2_valid=bool(ok2),
                             v1_points_a=a1, v2_points_a=a2, v2_rule=rule, reply=reply))

df = pd.DataFrame(rows)
if df.empty:
    sys.exit("No raw data found in data/raw or data/raw_paraphrase.")
df["changed"] = df.v1_valid & df.v2_valid & ~df.apply(lambda x: same(x.v1_points_a, x.v2_points_a), axis=1)
df["lost"] = df.v1_valid & ~df.v2_valid
df["gained"] = ~df.v1_valid & df.v2_valid
df["unlabelled"] = df.v2_rule.str.startswith("unlabelled")

g = df.groupby(["prompts", "condition", "domain"])
summary = g.agg(rounds=("reply", "size"), v1_valid=("v1_valid", "sum"), v2_valid=("v2_valid", "sum"),
                changed=("changed", "sum"), became_invalid=("lost", "sum"), became_valid=("gained", "sum"),
                unlabelled_rule=("unlabelled", "sum")).reset_index()
C.RESULTS.mkdir(exist_ok=True)
summary.to_csv(C.RESULTS / "parse_audit_summary.csv", index=False)
diffs = df[df.changed | df.lost | df.gained]
diffs.to_csv(C.RESULTS / "parse_audit_diffs.csv", index=False, encoding="utf-8-sig")

valid = df[df.v2_valid]
unl = valid[valid.unlabelled]
sample = pd.concat([unl.sample(min(100, len(unl)), random_state=1),
                    valid[~valid.unlabelled].sample(min(200 - min(100, len(unl)), (~valid.unlabelled).sum()),
                                                    random_state=1)])
sample.to_csv(C.RESULTS / "parse_audit_sample.csv", index=False, encoding="utf-8-sig")

pd.set_option("display.width", 200)
print("Parser audit: version 1 (first results) vs version 2\n")
print(summary[(summary.changed + summary.became_invalid + summary.became_valid + summary.unlabelled_rule) > 0]
      .to_string(index=False) if len(summary) else "no data")
tot = summary[["rounds", "changed", "became_invalid", "became_valid", "unlabelled_rule"]].sum()
print(f"\nAll rounds: {tot.rounds}; choice changed {tot.changed}; became invalid {tot.became_invalid}; "
      f"became valid {tot.became_valid}; parsed by an unlabelled fallback {tot.unlabelled_rule}")
print("\nv2 rules used:\n" + df.v2_rule.value_counts().to_string())
print(f"\nWrote {C.RESULTS / 'parse_audit_summary.csv'}, parse_audit_diffs.csv ({len(diffs)} rows), "
      f"parse_audit_sample.csv ({len(sample)} rows)")
