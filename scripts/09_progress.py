"""Show progress: finished subjects per condition and domain, invalid-answer rate, credit left.

  python scripts/09_progress.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C
from src.dataio import read_jsonl
from src.llm_client import credit_balance

meta_dir, raw_dir = C.META_DIR, C.RAW_DIR
print(f"Prompt set: {C.PROMPT_SET}  (folders: {raw_dir.name}, {meta_dir.name})  model: {C.MODEL}\n")
rows = []
for f in sorted(meta_dir.glob("*.jsonl")):
    m = pd.DataFrame(read_jsonl(f))
    r = pd.DataFrame(read_jsonl(raw_dir / f.name)) if (raw_dir / f.name).exists() else pd.DataFrame()
    for dom in C.DOMAINS:
        n = int((m["domain"] == dom).sum()) if len(m) else 0
        bad = (1 - r.loc[r["domain"] == dom, "valid"].mean()) if len(r) and (r["domain"] == dom).any() else float("nan")
        rows.append(dict(condition=f.stem, domain=dom, finished=n, invalid_rate=round(bad, 4)))
if not rows:
    print("No finished subjects yet for this prompt set.")
else:
  print(pd.DataFrame(rows).pivot(index="condition", columns="domain", values="finished")
      .reindex(columns=C.DOMAINS).fillna(0).astype(int).to_string())
  print("\nInvalid-answer rate:")
  print(pd.DataFrame(rows).pivot(index="condition", columns="domain", values="invalid_rate").reindex(columns=C.DOMAINS).to_string())
c = credit_balance()
print(f"\nCredit left: {c:.2f}" if c is not None else "\nCredit: not available for this provider")
