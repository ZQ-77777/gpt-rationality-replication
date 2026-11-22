# data/

This folder is ignored by git, except for this file.

| Path | Created by | Content |
|---|---|---|
| `raw/<condition>.jsonl` | `02_run_llm.py` | One line per round: prices, reply, parsed allocation, validity flag |
| `meta/<condition>.jsonl` | `02_run_llm.py` | One line per subject: full transcript, token usage, comprehension answers |
| `raw_paraphrase/`, `meta_paraphrase/` | `02_run_llm.py` with `LLM_PROMPTS=paraphrase` | Same, for the paraphrased prompt set |
| `data.csv` | download | The authors' subject-level data, from the data link in the paper |
| `authors_*.csv` | `07_import_authors.py` | The authors' data in this project's format |

The raw transcripts for the gpt-4o-mini runs are available from the author on request.
