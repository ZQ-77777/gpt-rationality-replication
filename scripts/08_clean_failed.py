"""Remove subjects that contain API failures (empty replies) or never finished, so that
scripts/02_run_llm.py reruns them. Genuine invalid answers (non-empty text) are kept.
Originals are backed up as *.jsonl.bak.

  python scripts/08_clean_failed.py
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.dataio import read_jsonl

pairs = [(C.DATA / "raw", C.DATA / "meta"), (C.DATA / "raw_paraphrase", C.DATA / "meta_paraphrase")]
for raw, meta_dir in [(f, m) for r, m in pairs if r.exists() for f in sorted(r.glob("*.jsonl"))]:
    meta = meta_dir / raw.name
    rows = read_jsonl(raw)
    bad = {(r["domain"], r["rep"]) for r in rows if not (r.get("reply") or "").strip()}
    done = {(m["domain"], m["rep"]) for m in (read_jsonl(meta) if meta.exists() else [])}
    bad |= {(r["domain"], r["rep"]) for r in rows} - done      # rows of a subject that never finished
    if not bad:
        print(f"{raw.parent.name}/{raw.stem}: no API failures")
        continue
    metas = read_jsonl(meta) if meta.exists() else []
    for f in (raw, meta):
        if f.exists():
            shutil.copy(f, f.with_suffix(".jsonl.bak"))
    with open(raw, "w", encoding="utf-8") as fh:
        for r in rows:
            if (r["domain"], r["rep"]) not in bad:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(meta, "w", encoding="utf-8") as fh:
        for m in metas:
            if (m["domain"], m["rep"]) not in bad:
                fh.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(f"{raw.parent.name}/{raw.stem}: removed {len(bad)} failed/unfinished subjects: {sorted(bad)}")
