"""Import the authors' subject-level data (data.csv from the paper's Dropbox folder).

The file has one row per subject with indices already computed (no raw choices):
  label = GPT_<domain>_<condition> (100 GPT-3.5 subjects each) or Human_<condition> (347 people,
  each with all four domains in one row). Columns ccei_/hmi_/mpi_/mci_/spearman_/alpha_/rho_<domain>,
  aggregate estimates <param>_<domain>_agg, and Q366-Q370 (human demographics, coding not documented).

  python scripts/07_import_authors.py data/data.csv
Writes data/authors_indices.csv, data/authors_params.csv, data/authors_params_pooled.csv; these are
appended automatically by 03_indices.py and 04_estimate.py. Then rerun 03-06.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C

COND = {"baseline": "baseline", "priceframing": "price_framing", "discrete": "discrete",
        "temp5": "temp_0.5", "temp1": "temp_1", "female": "female", "male": "male",
        "kid": "young_child", "elder": "elderly", "low_edu": "elementary_edu",
        "high_edu": "college_edu", "asian": "asian", "black": "african_american"}

src = Path(sys.argv[1] if len(sys.argv) > 1 else C.DATA / "data.csv")
raw = pd.read_csv(src)
# human ids in the file are platform participant ids: replace them with neutral codes H001, H002, ...
hid = {v: f"H{i + 1:03d}" for i, v in enumerate(raw.loc[raw["label"].str.startswith("Human"), "id"].unique())}
raw["id"] = [hid.get(v, v) for v in raw["id"]]
ind, par, pooled = [], [], []
for _, row in raw.iterrows():
    parts = row["label"].split("_")
    if parts[0] == "GPT":
        source, domains, cond = C.PAPER_LABEL, [parts[1]], COND["_".join(parts[2:])]
    else:
        source, domains, cond = "Human", C.DOMAINS, COND["_".join(parts[1:])]
    for dom in domains:
        if pd.isna(row[f"ccei_{dom}"]):
            continue
        ind.append(dict(source=source, condition=cond, domain=dom, rep=str(row["id"]), n_valid=C.N_ROUNDS,
                        CCEI=row[f"ccei_{dom}"], HMI=row[f"hmi_{dom}"], MPI_mean=row[f"mpi_{dom}"],
                        MCI=row[f"mci_{dom}"], spearman=row[f"spearman_{dom}"]))
        if pd.notna(row[f"alpha_{dom}"]):
            par.append(dict(source=source, condition=cond, domain=dom, rep=str(row["id"]),
                            alpha=row[f"alpha_{dom}"], rho=row[f"rho_{dom}"]))
        if pd.notna(row.get(f"alpha_{dom}_agg")):
            pooled.append(dict(source=source, condition=cond, domain=dom,
                               alpha=row[f"alpha_{dom}_agg"], rho=row[f"rho_{dom}_agg"],
                               alpha_se=row[f"alpha_se_{dom}_agg"], rho_se=row[f"rho_se_{dom}_agg"]))

ind, par = pd.DataFrame(ind), pd.DataFrame(par)
pooled = pd.DataFrame(pooled).drop_duplicates(["source", "condition", "domain"])
ind.to_csv(C.DATA / "authors_indices.csv", index=False)
par.to_csv(C.DATA / "authors_params.csv", index=False)
pooled.to_csv(C.DATA / "authors_params_pooled.csv", index=False)

# check against the numbers printed in the paper
chk = (ind[ind.condition.isin(["baseline", "price_framing", "discrete"])]
       .groupby(["source", "condition", "domain"])
       .agg(n=("CCEI", "size"), CCEI_mean=("CCEI", "mean"), CCEI_eq_1=("CCEI", lambda s: (s >= 1 - 1e-9).sum()),
            below_0_9=("CCEI", lambda s: (s < 0.9).mean()), spearman_mean=("spearman", "mean")).round(3))
print(chk.to_string())
print(f"\nWrote {len(ind)} subject-domain rows, {len(par)} individual estimates, {len(pooled)} pooled estimates.")
print("Paper: GPT baseline CCEI=1 counts 95/89/81/92; human mean CCEI 0.980/0.985/0.967/0.963.")
