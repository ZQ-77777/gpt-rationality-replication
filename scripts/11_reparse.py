"""Re-apply the current parsing rules to replies already collected (no API calls).
Use after src/parse.py is improved. Originals are backed up as *.jsonl.bak.

  python scripts/11_reparse.py
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src import prompt_api as P
from src.dataio import read_jsonl
from src.parse import parse_continuous, parse_discrete
from src.prices import discrete_options

for f in sorted(C.RAW_DIR.glob("*.jsonl")):
    rows = read_jsonl(f)
    before = sum(r["valid"] for r in rows)
    for r in rows:
        cfg = C.CONDITIONS[r["condition"]]
        if cfg["choice"] == "discrete":
            opts = discrete_options(r["M"], r["N"])
            j, ok = parse_discrete(r["reply"], [(o[2], o[3]) for o in opts],
                                   allow_option_number=(C.PROMPT_SET != "paper"))
            r["points_a"], r["points_b"] = (opts[j][0], opts[j][1]) if ok else (None, None)
        else:
            a, b, ok = parse_continuous(r["reply"], *P.labels(r["domain"]))
            r["points_a"], r["points_b"] = a, b
        r["valid"] = bool(ok)
    shutil.copy(f, f.with_suffix(".jsonl.bak"))
    with open(f, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{f.name}: valid rounds {before} -> {sum(r['valid'] for r in rows)} of {len(rows)}")
