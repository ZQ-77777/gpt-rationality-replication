"""Parser review, step 2: compare version 2 (src/parse_v2.py) with version 3 (src/parse.py) on every
stored reply, and export every reply that version 3 reads with a weaker rule, so that it can be
checked by hand. Reads data only; changes nothing.

  python scripts/14_parse_review.py

Writes
  results/parse_v3_summary.csv   per prompt set x condition x domain: rounds, valid (v2, v3), rounds whose
                                 choice changed, became invalid / valid, and how often each weaker rule fired
  results/parse_v3_diffs.csv     every round where v2 and v3 disagree, with the reply text
  results/parse_review_all.csv   EVERY round read by a weaker rule (one-sided-full, unlabelled-points) or left
                                 invalid for review (review, ambiguous), with the amounts the reply mentions
  results/parse_review_sample.csv  stratified random sample of rounds read by a labelled rule:
                                 50 per prompt set (seed 1), to estimate the error rate of the main rules
"""
import re
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src import prompts as PARA, prompts_paper as PAPER
from src import parse_v2 as V2
from src import parse as V3
from src.dataio import read_jsonl
from src.prices import discrete_options

SETS = [("paper", C.DATA / "raw"), ("paraphrase", C.DATA / "raw_paraphrase")]
WEAK = {"one-sided-full", "unlabelled-points"}
REVIEW = {"review", "ambiguous"}


def labels(pset, domain):
    return PAPER.labels(domain) if pset == "paper" else (PARA.DOMAIN[domain]["a"], PARA.DOMAIN[domain]["b"])


def same(a, b):
    return a is not None and b is not None and abs(a - b) < 0.5


def amounts(reply):
    """Short snippets around every 'N points' in the reply, to make the hand check quick."""
    out = []
    for mo in re.finditer(r"\d+(?:\.\d+)?\s*points?\b", reply or "", flags=re.I):
        out.append(reply[max(0, mo.start() - 40):mo.end() + 40].replace("\n", " "))
    return " | ".join(out[:8])


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
                d2 = V2.parse_discrete_detail(reply, vals, allow_option_number=num)
                d3 = V3.parse_discrete_detail(reply, vals, allow_option_number=num)
                a2 = opts[d2["j"]][0] if d2["valid"] else None
                a3 = opts[d3["j"]][0] if d3["valid"] else None
            else:
                la, lb = labels(pset, r["domain"])
                d2 = V2.parse_continuous_detail(reply, la, lb)
                d3 = V3.parse_continuous_detail(reply, la, lb)
                a2, a3 = d2["a"], d3["a"]
            rows.append(dict(prompts=pset, condition=r["condition"], domain=r["domain"], choice=cfg["choice"],
                             rep=r.get("rep"), round=r.get("round"), v2_valid=bool(d2["valid"]),
                             v3_valid=bool(d3["valid"]), v2_points_a=a2, v3_points_a=a3,
                             v2_rule=d2["rule"], v3_rule=d3["rule"], reply=reply))

df = pd.DataFrame(rows)
if df.empty:
    sys.exit("No raw data found in data/raw or data/raw_paraphrase.")
df["changed"] = df.v2_valid & df.v3_valid & ~df.apply(lambda x: same(x.v2_points_a, x.v3_points_a), axis=1)
df["lost"] = df.v2_valid & ~df.v3_valid
df["gained"] = ~df.v2_valid & df.v3_valid
for rule in sorted(WEAK | REVIEW):
    df["n_" + rule] = df.v3_rule == rule

g = df.groupby(["prompts", "condition", "domain"])
agg = dict(rounds=("reply", "size"), v2_valid=("v2_valid", "sum"), v3_valid=("v3_valid", "sum"),
           changed=("changed", "sum"), became_invalid=("lost", "sum"), became_valid=("gained", "sum"))
agg.update({"n_" + r: ("n_" + r, "sum") for r in sorted(WEAK | REVIEW)})
summary = g.agg(**agg).reset_index()
C.RESULTS.mkdir(exist_ok=True)
summary.to_csv(C.RESULTS / "parse_v3_summary.csv", index=False)

cols = ["prompts", "condition", "domain", "rep", "round", "v2_valid", "v2_points_a", "v2_rule",
        "v3_valid", "v3_points_a", "v3_rule", "reply"]
diffs = df[df.changed | df.lost | df.gained]
diffs[cols].to_csv(C.RESULTS / "parse_v3_diffs.csv", index=False, encoding="utf-8-sig")

review = df[(df.choice == "continuous") & df.v3_rule.isin(WEAK | REVIEW)].copy()
review["amounts_in_reply"] = review.reply.map(amounts)
review["hand_check"] = ""                             # fill in: ok / wrong (A should be ...) / unclear
review[cols[:5] + ["v3_valid", "v3_points_a", "v3_rule", "amounts_in_reply", "hand_check", "reply"]].to_csv(
    C.RESULTS / "parse_review_all.csv", index=False, encoding="utf-8-sig")

lab = df[(df.choice == "continuous") & df.v3_rule.isin({"labelled", "labelled-decision"})]
sample = pd.concat([x.sample(min(50, len(x)), random_state=1) for _, x in lab.groupby("prompts")]) if len(lab) else lab
sample = sample.assign(hand_check="")
sample[cols[:5] + ["v3_points_a", "v3_rule", "hand_check", "reply"]].to_csv(
    C.RESULTS / "parse_review_sample.csv", index=False, encoding="utf-8-sig")

pd.set_option("display.width", 220)
show = summary[(summary.changed + summary.became_invalid + summary.became_valid
                + summary[["n_" + r for r in sorted(WEAK | REVIEW)]].sum(axis=1)) > 0]
print("Parser review: version 2 vs version 3\n")
print(show.to_string(index=False) if len(show) else "no differences")
tot = summary.drop(columns=["prompts", "condition", "domain"]).sum()
print("\nTotals:\n" + tot.to_string())
print("\nv3 rules used (continuous rounds):\n" + df[df.choice == "continuous"].v3_rule.value_counts().to_string())
print(f"\nWrote parse_v3_summary.csv, parse_v3_diffs.csv ({len(diffs)} rows), "
      f"parse_review_all.csv ({len(review)} rows), parse_review_sample.csv ({len(sample)} rows)")
