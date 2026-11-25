# Economic Rationality of GPT Revisited

This repository replicates the large-language-model (LLM) experiments in

> Chen, Y., Liu, T. X., Shan, Y. and Zhong, S. (2023). The emergence of economic rationality of GPT. *PNAS* 120(51), e2316205120.

`gpt-3.5-turbo`, the model used in the paper, has been retired, so it cannot be re-run. The replication therefore has two parts:

1. **Computational reproduction.** The full analysis pipeline is re-implemented: GARP, CCEI, HMI, MPI, MCI, the Bronars test, the Spearman test of downward-sloping demand, two-limit Tobit estimation of CES parameters, and all statistical tests. Run on the authors' published subject-level data, it reproduces all 60 target numbers checked against the paper.
2. **Conceptual replication.** Every LLM condition of the paper is re-run with `gpt-4o-mini` (snapshot 2024-07-18). The prompts are the paper's own, verbatim from Appendix A of arXiv:2305.12763v3, and the design is the same: 100 subjects × 25 rounds per domain and condition. The new data contain 104,000 decisions from 4,160 model subjects.

Author of the replication: Zhang Qi

## Main results

| Claim in the paper (GPT-3.5) | gpt-4o-mini | Verdict |
|---|---|---|
| Mean CCEI close to 1 in all four domains | 0.998–1.000 | Replicated |
| More rational than humans and than the literature mean of 0.918 | all p < 0.01 | Replicated |
| Demand slopes downward (Spearman < 0 for every subject) | 100% negative | Replicated |
| Preferences far more homogeneous than humans' | Levene p < 0.001 | Replicated |
| Temperature does not change rationality | no relevant change | Replicated |
| Higher temperature raises the SD of ρ in all domains | time domain only | Partly |
| Higher temperature produces invalid answers | 0% invalid | Not replicated |
| Demographic personas do not matter | 3 of 64 tests at 5% (n = 30) | Replicated |
| Price framing reduces rationality, more than in humans | no reduction | Not replicated |
| Discrete choice reduces rationality, more than in humans | depends on prompt wording | Partly |

The replication also found three things the paper does not report:

- **Off-menu choices.** In the discrete condition with the paper's prompts, the model sometimes names a bundle that is not on the menu: it keeps the largest amount but puts it in the wrong position. This happens in 21% of risk rounds.
- **Fixed rules.** With an 11-option menu, the model picks the same allocation in 81–95% of rounds. These rules pass GARP, so CCEI does not detect them.
- **Preferences depend on the response format.** In the time domain the model makes interior choices with continuous allocation but corner choices with a menu.

See `results/` for every table and figure.

**Parser audit.** Replies are free text and are read by rules. The parser went through three versions, each compared with the previous one on all 104,000 stored replies: version 2 changed 774 rounds (0.7%) and version 3 another 20, all in continuous-allocation conditions; no discrete-menu round changed. Version 3 fixes one-sided full allocations ("Invest 100 points today") and no longer pairs two numbers just because they sum to 100. Every round read by a weaker rule (23) and a stratified sample of 100 labelled readings were checked by hand; all were correct. All results here use version 3 (`src/parse.py`).

## Data boundary

| Source | Content |
|---|---|
| Paper | Design, target numbers, prompts (Appendix A) |
| Authors' `data.csv` (from the paper's data link) | Subject-level indices and estimates for GPT-3.5 and 347 human subjects, used as published. Raw choices are not included in that file. **Not redistributed here; download it from the link in the paper.** |
| This repository | All `gpt-4o-mini` choice data (generated with this code), all `gpt-4o-mini` indices and estimates, the Bronars simulation, and all tests and figures |

In `results/`, the rows labelled `Human` and `gpt-3.5-turbo (paper)` are computed from the authors' data. Human IDs are anonymised as H001–H347.

## Repository layout

```
config.py              design constants, the 13 conditions, API settings (read from .env)
src/
  prices.py            budget lines (seeded per subject, identical across conditions)
  prompts_paper.py     the paper's prompts, verbatim from Appendix A (default)
  prompts.py           paraphrased prompt set (kept as a sensitivity check)
  prompt_api.py        selects the prompt set (LLM_PROMPTS=paper | paraphrase)
  parse.py             reply -> allocation (continuous and discrete), final version
  parse_v1.py          parser version 1, kept only for the audit
  parse_v2.py          parser version 2, kept only for the review
  llm_client.py        OpenAI-compatible / Azure client with retries; credit check
  experiment.py        one subject = one 25-round conversation; MockClient for offline tests
  rp.py                GARP, CCEI (exact), HMI, MPI, MCI (MILP), Bronars
  demand.py            Spearman test of downward-sloping demand
  estimate.py          two-limit Tobit for CES (alpha, rho), pooled and individual
  stats.py             Welch t, Levene, OLS with HC1 standard errors
  dataio.py            loading model data and the authors' data
scripts/
  00_selftest.py       tests on cases with known answers (must print ALL PASSED)
  00b_check_api.py     lists models, checks the balance, makes one test call
  01_smoke_test.py     one subject per domain, prints transcript and cost projection
  02_run_llm.py        data collection (resumable)
  03_indices.py        rationality indices and demand test
  04_estimate.py       preference estimation
  05_tests.py          all statistical tests -> results/tests.md
  06_figures.py        Figures 1-4
  07_import_authors.py imports the authors' data.csv
  08_clean_failed.py   removes subjects with failed API calls
  09_progress.py       progress, invalid-answer rate, credit
  10_show_invalid.py   lists unparsed replies
  11_reparse.py        re-applies the parser to stored replies (no API calls)
  12_offmenu.py        off-menu answers and robustness of the discrete results
  13_parse_audit.py    compares parser versions 1 and 2 on every stored reply
  14_parse_review.py   compares versions 2 and 3; exports weak-rule rounds and a sample for hand checking
docs/GUIDE_zh.md       step-by-step replication guide (Chinese, with English terms)
results/               final tables and figures used in the report
```

## How to run

Requires Python 3.11 and SciPy 1.11 or later (for `milp`).

```bash
conda create -n gptrat python=3.11 -y
conda activate gptrat
pip install -r requirements.txt
cp .env.example .env          # Windows: copy .env.example .env ; then fill in the key and model
python scripts/00_selftest.py
python scripts/00b_check_api.py
python scripts/01_smoke_test.py --price-in 0.15 --price-out 0.6   # USD per 1M tokens, for the cost projection
```

Collect the data. The runner can be stopped and resumed at any time.

```bash
python scripts/02_run_llm.py --conditions baseline price_framing discrete --workers 1
python scripts/02_run_llm.py --conditions temp_0.5 temp_1 --workers 1
python scripts/02_run_llm.py --conditions female male young_child elderly elementary_edu college_edu asian african_american --reps 30 --workers 1
python scripts/08_clean_failed.py
```

Analyse:

```bash
python scripts/07_import_authors.py data/data.csv    # authors' data, downloaded separately
python scripts/03_indices.py
python scripts/04_estimate.py
python scripts/05_tests.py
python scripts/06_figures.py
python scripts/12_offmenu.py
```

To run the paraphrased prompt set, set `LLM_PROMPTS=paraphrase`. It writes to `data/raw_paraphrase/` and `data/meta_paraphrase/`, so the two sets never mix.

Offline test of the whole pipeline, with no API calls:

```bash
python scripts/02_run_llm.py --conditions baseline --mock
```

Cost: with `gpt-4o-mini` through the HKUST GenAI gateway, all new data cost about HKD 430 of API credit, including pilot runs.

## Implementation choices not fixed by the paper

| | Question | Choice |
|---|---|---|
| A1 | Prices across repetitions and conditions | Seeded per subject; identical across conditions (paired design) |
| A2 | Prompt wording | Appendix A verbatim; a paraphrased set as a sensitivity check |
| A2b | Discrete option formula | Points on the budget line; the appendix formula for N_i contains a typo |
| A3 | Parsing | Labelled amounts in either order; the final allocation after the last decision phrase; one-sided full allocations read as 100/0; otherwise one unique unlabelled "N points" pair, else invalid; negative amounts invalid; sums to 100 (±1). Discrete: the option after the last decision phrase. Three versions, each compared on all replies; final readings checked by hand |
| A4 | Subjects with invalid rounds | Kept if at least 20 of 25 rounds are valid |
| A5 | t-test | Welch |
| A6 | MPI cycles | Violating two-cycles (sufficient with two goods) |
| A7 | Risk-domain ordering | Good 1 is the larger outcome (disappointment aversion) |
| A8 | Model | gpt-4o-mini (2024-07-18) |
| A9 | Price-framing rounding | Effective price is the displayed 1/M (two decimals) |
| A10 | Reply length | Default (no cap); 200 tokens in the paraphrase runs |
| A11 | Off-menu answers | Invalid in the main analysis; two remapping rules as robustness checks |

## Data not in this repository

- `.env` holds your API key. Never commit it.
- `data/` holds the raw transcripts and the authors' file. It is ignored by git; see `data/README.md`.
