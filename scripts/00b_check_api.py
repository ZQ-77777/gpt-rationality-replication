"""Check that the API works before running anything: key, model list, credit balance, one call.

  python scripts/00b_check_api.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import httpx
import config as C
from src.llm_client import make_client

print(f"provider={C.PROVIDER}  base_url={C.BASE_URL}  model={C.MODEL}  key_header={C.KEY_HEADER or '(Bearer)'}")
if not C.API_KEY or C.API_KEY.startswith("<"):
    sys.exit("LLM_API_KEY is empty: fill in .env first.")
client = make_client()

# 1. which models can this key use?
try:
    names = sorted(m.id for m in client.models.list().data)
    print(f"\n{len(names)} models available:\n  " + "\n  ".join(names))
except Exception as e:
    print(f"\nCould not list models ({type(e).__name__}: {e}).\n"
          "Take model names from your provider's 'supported models' page instead.")

# 2. credit balance (HKUST gateway only)
if C.BASE_URL and "hkust-genai" in C.BASE_URL:
    try:
        r = httpx.get(C.BASE_URL.rstrip("/") + "/balance", headers={"api-key": C.API_KEY}, timeout=30)
        print(f"\nBalance (HTTP {r.status_code}): {r.text[:500]}")
    except Exception as e:
        print(f"\nBalance check failed: {e}")

# 3. one tiny call with temperature 0
try:
    r = client.chat.completions.create(
        model=C.MODEL, temperature=0, max_tokens=20,
        messages=[{"role": "user", "content": "Reply with exactly: Asset A: 30, Asset B: 70"}])
    print(f"\nTest call OK -> {r.choices[0].message.content!r}  usage={r.usage}")
except Exception as e:
    print(f"\nTest call FAILED: {type(e).__name__}: {e}")
