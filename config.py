"""Central settings for the GPT economic-rationality replication.

Chen, Liu, Shan & Zhong (2023), "The emergence of economic rationality of GPT", PNAS 120(51).
Edit this file (or set environment variables) instead of editing code elsewhere.
"""
import os
from pathlib import Path

try:                                    # read .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
DATA.mkdir(exist_ok=True)
# each prompt set writes to its own folders, so the two versions never mix
RAW_DIR = DATA / ("raw" if os.getenv("LLM_PROMPTS", "paper") == "paper" else "raw_paraphrase")
META_DIR = DATA / ("meta" if os.getenv("LLM_PROMPTS", "paper") == "paper" else "meta_paraphrase")
RESULTS.mkdir(exist_ok=True)

# ---------------- design (paper: Methods) ----------------
N_ROUNDS = 25            # decisions per subject (budget lines)
N_REPS = 100             # GPT "subjects" per domain x condition
ENDOWMENT = 100          # points
PRICE_LOW, PRICE_HIGH = 0.10, 1.00   # M, N drawn from [0.1, 1]
PRICE_MAX_AT_LEAST = 0.50            # max{M, N} >= 0.5
N_DISCRETE_OPTIONS = 11              # discrete-choice condition
DOMAINS = ["risk", "time", "social", "food"]

# condition name -> settings. "demo" is the demographic phrase in the system prompt.
CONDITIONS = {
    "baseline":      dict(temperature=0.0, framing="baseline", choice="continuous", demo=None),
    "temp_0.5":      dict(temperature=0.5, framing="baseline", choice="continuous", demo=None),
    "temp_1":        dict(temperature=1.0, framing="baseline", choice="continuous", demo=None),
    "price_framing": dict(temperature=0.0, framing="inverse",  choice="continuous", demo=None),
    "discrete":      dict(temperature=0.0, framing="baseline", choice="discrete",   demo=None),
    "female":        dict(temperature=0.0, framing="baseline", choice="continuous", demo="female"),
    "male":          dict(temperature=0.0, framing="baseline", choice="continuous", demo="male"),
    "young_child":   dict(temperature=0.0, framing="baseline", choice="continuous", demo="young child"),
    "elderly":       dict(temperature=0.0, framing="baseline", choice="continuous", demo="elderly"),
    "elementary_edu":dict(temperature=0.0, framing="baseline", choice="continuous", demo="elementary_edu"),
    "college_edu":   dict(temperature=0.0, framing="baseline", choice="continuous", demo="college_edu"),
    "asian":         dict(temperature=0.0, framing="baseline", choice="continuous", demo="Asian"),
    "african_american": dict(temperature=0.0, framing="baseline", choice="continuous", demo="African American"),
}

# ---------------- analysis (paper: Results) ----------------
CCEI_CUTOFF_FOR_ESTIMATION = 0.95   # footnote: drop subjects with CCEI < 0.95
CORNER_ADJ_POINTS = 0.1             # 0.1% of the 100-point budget, for ln(xA/xB)
LITERATURE_MEAN_CCEI = 0.918        # SI Fig. S1 average of prior studies
N_BRONARS = 1000                    # simulated random subjects per domain
MIN_VALID_ROUNDS = 20               # keep a subject only if >= 20 of 25 answers parse

# ---------------- LLM access (fill in .env or environment) ----------------
# PROVIDER = "openai"  -> any OpenAI-compatible endpoint (OpenAI, a university gateway, Ollama, vLLM)
# PROVIDER = "azure"   -> Azure OpenAI style endpoint (deployment name + api-version)
PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
PROMPT_SET = os.getenv("LLM_PROMPTS", "paper")   # "paper" = authors' original prompts; "paraphrase" = our first version
SOURCE_LABEL = os.getenv("LLM_LABEL", MODEL)   # how this model's subjects are labelled in results
PARA_LABEL = SOURCE_LABEL + " (paraphrase)"    # label for runs made with the paraphrased prompts
PAPER_LABEL = "gpt-3.5-turbo (paper)"          # the authors' GPT subjects, imported by 07_import_authors.py
BASE_URL = os.getenv("LLM_BASE_URL")          # e.g. http://localhost:11434/v1 for Ollama
API_KEY = os.getenv("LLM_API_KEY", "")
KEY_HEADER = os.getenv("LLM_KEY_HEADER", "")  # "api-key" for gateways that want the key in an api-key header (e.g. HKUST)
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")  # copy from your provider's portal
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-06-01")
# No reply-length cap by default: the paper kept all API parameters at their defaults, and a cap cuts
# long answers before the model states its choice. Set LLM_MAX_TOKENS in .env to impose one.
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS")) if os.getenv("LLM_MAX_TOKENS") else None
MIN_CREDIT = float(os.getenv("LLM_MIN_CREDIT", "30"))   # stop the run when the HKUST balance falls below this
SEED_BASE = 20231212   # any fixed integer; makes the price draws reproducible
