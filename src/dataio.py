"""Load choices into one tidy table.

Columns: source (model label / Human), condition, domain, rep (subject id), round, M, N,
         points_a, points_b, valid
GPT choices come from data/raw/*.jsonl (written by scripts/02_run_llm.py).
Human choices (optional) come from data/human.csv with the same columns except source/valid.
"""
import json
import numpy as np
import pandas as pd
import config as C



def read_jsonl(path):
    """Read a .jsonl file, skipping a line cut short by a forced stop (e.g. closing the terminal)."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"  skipped a broken line in {path.name}")
    return out


def load_gpt():
    """Your model's choices: data/raw (original prompts) and data/raw_paraphrase (paraphrased prompts),
    plus any other models copied to data/extra/<label>/."""
    frames = []
    sets = [(C.DATA / "raw", C.SOURCE_LABEL), (C.DATA / "raw_paraphrase", C.PARA_LABEL)]
    extra = C.DATA / "extra"
    if extra.exists():
        sets += [(d, d.name) for d in sorted(extra.glob("*")) if d.is_dir()]
    for folder, label in sets:
        rows = [r for f in sorted(folder.glob("*.jsonl")) for r in read_jsonl(f)] if folder.exists() else []
        if rows:
            frames.append(pd.DataFrame(rows).assign(source=label))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_human():
    f = C.DATA / "human.csv"
    if not f.exists():
        return pd.DataFrame()
    df = pd.read_csv(f)
    df["source"] = "Human"
    df["valid"] = df["points_a"].notna() & df["points_b"].notna()
    return df


def load_all():
    df = pd.concat([load_gpt(), load_human()], ignore_index=True)
    if df.empty:
        raise SystemExit("No choice data found. Run scripts/02_run_llm.py first.")
    return df


def subject_arrays(g):
    """From one subject's valid rows -> (P, X) for revealed-preference tests."""
    g = g[g["valid"]]
    M, N = g["M"].to_numpy(float), g["N"].to_numpy(float)
    P = np.column_stack([1 / M, 1 / N])
    X = np.column_stack([g["points_a"].to_numpy(float) * M, g["points_b"].to_numpy(float) * N])
    return P, X


def append_authors(df, name):
    """Append the authors' subject-level file data/authors_<name>.csv if it exists (07_import_authors.py)."""
    f = C.DATA / f"authors_{name}.csv"
    if not f.exists():
        return df
    return pd.concat([df, pd.read_csv(f)], ignore_index=True)
