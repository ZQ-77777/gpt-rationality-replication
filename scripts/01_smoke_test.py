"""Run ONE subject per domain, print the whole conversation, and project the full cost.

  python scripts/01_smoke_test.py --mock                     # offline, no API key needed
  python scripts/01_smoke_test.py --condition baseline       # real API, 4 subjects
  python scripts/01_smoke_test.py --price-in 0.15 --price-out 0.60   # USD per 1M tokens
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.experiment import run_subject, MockClient
from src.llm_client import make_client

ap = argparse.ArgumentParser()
ap.add_argument("--condition", default="baseline", choices=list(C.CONDITIONS))
ap.add_argument("--mock", action="store_true")
ap.add_argument("--price-in", type=float, default=0.0, help="USD per 1M input tokens")
ap.add_argument("--price-out", type=float, default=0.0, help="USD per 1M output tokens")
args = ap.parse_args()

client = MockClient() if args.mock else make_client()
tot_in = tot_out = 0
for domain in C.DOMAINS:
    rows, meta = run_subject(client, domain, args.condition, rep=0)
    print(f"\n================ {domain} / {args.condition} / prompts={C.PROMPT_SET} ================")
    for m in meta["transcript"]:
        print(f"[{m['role']}] {m['content']}")
    print("--> parsed choices (points A / points B):",
          "; ".join(f"R{r['round']}: {r['points_a']:.0f}/{r['points_b']:.0f}" if r["valid"] else f"R{r['round']}: INVALID"
                    for r in rows))
    ok = sum(r["valid"] for r in rows)
    print(f"--> valid answers: {ok}/{len(rows)}; tokens in={meta['usage']['in']} out={meta['usage']['out']}")
    tot_in += meta["usage"]["in"]
    tot_out += meta["usage"]["out"]

subjects = len(C.DOMAINS) * C.N_REPS
per_in, per_out = tot_in / len(C.DOMAINS), tot_out / len(C.DOMAINS)
print(f"\nOne condition = {subjects} subjects ~ {per_in * subjects / 1e6:.1f}M input + "
      f"{per_out * subjects / 1e6:.2f}M output tokens")
if args.price_in or args.price_out:
    cost = (per_in * args.price_in + per_out * args.price_out) * subjects / 1e6
    print(f"Estimated cost per condition: USD {cost:.2f}; all {len(C.CONDITIONS)} conditions: "
          f"USD {cost * len(C.CONDITIONS):.2f}")
