"""Collect GPT choices. Resumable: finished (condition, domain, rep) triples are skipped.

  python scripts/02_run_llm.py --conditions baseline                      # 4 x 100 subjects
  python scripts/02_run_llm.py --conditions price_framing discrete --reps 100
  python scripts/02_run_llm.py --conditions female male --reps 30         # cheaper pass
  python scripts/02_run_llm.py --conditions baseline --mock               # offline pipeline test
Output: data/raw/<condition>.jsonl (one line per round) and data/meta/<condition>.jsonl
(one line per subject: token usage, comprehension answers, full transcript).
A subject is written only after all 25 rounds succeed, so stopping at any time is safe.
Ctrl+C stops the run (with --workers > 1, press it once and wait up to ~1 s).
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.experiment import run_subject, MockClient
from src.llm_client import make_client, credit_balance
from src.dataio import read_jsonl

ap = argparse.ArgumentParser()
ap.add_argument("--conditions", nargs="+", default=["baseline"], choices=list(C.CONDITIONS))
ap.add_argument("--domains", nargs="+", default=C.DOMAINS, choices=C.DOMAINS)
ap.add_argument("--reps", type=int, default=C.N_REPS)
ap.add_argument("--workers", type=int, default=1, help="parallel conversations (HKUST gateway: 1-2)")
ap.add_argument("--mock", action="store_true")
args = ap.parse_args()

raw_dir, meta_dir = C.RAW_DIR, C.META_DIR
raw_dir.mkdir(parents=True, exist_ok=True)
meta_dir.mkdir(parents=True, exist_ok=True)


def done_set(cond):
    f = meta_dir / f"{cond}.jsonl"
    return {(d["domain"], d["rep"]) for d in read_jsonl(f)} if f.exists() else set()


class Stop(Exception):
    pass


def check_credit():
    """Stop before the HKUST credit runs out (threshold: LLM_MIN_CREDIT in .env, default 30)."""
    c = None if args.mock else credit_balance()
    if c is None:
        return
    print(f"  credit left: {c:.2f}")
    if c < C.MIN_CREDIT:
        raise Stop(f"credit {c:.2f} is below LLM_MIN_CREDIT={C.MIN_CREDIT:.0f}; top up or lower the threshold")


for cond in args.conditions:
    done = done_set(cond)
    todo = [(d, r) for d in args.domains for r in range(args.reps) if (d, r) not in done]
    print(f"[{cond}] prompts={C.PROMPT_SET} model={C.MODEL}: {len(todo)} subjects to run ({len(done)} already done)")
    client = MockClient(noise=0.02, seed=1) if args.mock else make_client()
    state = {"n": 0, "fails": 0}

    with open(raw_dir / f"{cond}.jsonl", "a", encoding="utf-8") as fr, \
         open(meta_dir / f"{cond}.jsonl", "a", encoding="utf-8") as fm:

        def save(key, get_result):
            """Write one finished subject; count failures; raise Stop after 3 in a row."""
            try:
                rows, meta = get_result()
            except Exception as e:                       # API down: do not save, rerun next time
                state["fails"] += 1
                print(f"  subject {key} not saved ({e}); it will be rerun next time")
                if state["fails"] >= 3:
                    raise Stop("3 subjects failed in a row: the API looks down")
                return
            state["fails"] = 0
            for row in rows:                              # rows first, meta last = "subject finished"
                fr.write(json.dumps(row, ensure_ascii=False) + "\n")
            fm.write(json.dumps(meta, ensure_ascii=False) + "\n")
            fr.flush(); fm.flush()
            state["n"] += 1
            if state["n"] % 20 == 0 or state["n"] == len(todo):
                bad = sum(not r["valid"] for r in rows)
                print(f"  {state['n']}/{len(todo)} done (last subject: {bad} invalid answers)")
                check_credit()

        try:
            check_credit()                                # before starting this condition
            if args.workers <= 1 or args.mock:            # plain loop: Ctrl+C works immediately
                for d, r in todo:
                    save((d, r), lambda d=d, r=r: run_subject(client, d, cond, r))
            else:                                         # threads, polled every second so Ctrl+C works
                ex = ThreadPoolExecutor(max_workers=args.workers)
                futs = {ex.submit(run_subject, client, d, cond, r): (d, r) for d, r in todo}
                pending = set(futs)
                try:
                    while pending:
                        finished, pending = wait(pending, timeout=1, return_when=FIRST_COMPLETED)
                        for fut in finished:
                            save(futs[fut], fut.result)
                finally:
                    ex.shutdown(wait=False, cancel_futures=True)
        except (KeyboardInterrupt, Stop) as e:
            fr.flush(); fm.flush()
            print(f"\nStopped ({str(e) or 'Ctrl+C'}). Finished subjects are saved; rerun the same command to continue.")
            os._exit(1)                                   # do not wait for running threads
