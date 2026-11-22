"""List the replies that could not be parsed, so the parsing rules can be checked or extended.

  python scripts/10_show_invalid.py                 # summary + up to 15 examples
  python scripts/10_show_invalid.py --all > invalid.txt
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C
from src.dataio import read_jsonl

ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true")
args = ap.parse_args()

rows = [r for f in sorted(C.RAW_DIR.glob("*.jsonl")) for r in read_jsonl(f)]
df = pd.DataFrame(rows)
bad = df[~df["valid"]]
print(f"Prompt set: {C.PROMPT_SET}. Invalid rounds: {len(bad)} of {len(df)}\n")
print(bad.groupby(["condition", "domain"]).size().rename("invalid_rounds").to_string())
per_subj = df.groupby(["condition", "domain", "rep"])["valid"].sum()
print(f"\nSubjects with fewer than {C.MIN_VALID_ROUNDS} valid rounds (dropped from analysis): "
      f"{int((per_subj < C.MIN_VALID_ROUNDS).sum())}")
show = bad if args.all else bad.sample(min(15, len(bad)), random_state=0) if len(bad) else bad
for _, r in show.iterrows():
    print(f"\n--- {r['condition']} / {r['domain']} / rep {r['rep']} / round {r['round']}  (M={r['M']:.2f}, N={r['N']:.2f})")
    print(str(r["reply"])[-600:])
