"""Thin wrapper around the OpenAI Python SDK (works with any OpenAI-compatible endpoint)."""
import time
import config as C


def make_client():
    if C.PROVIDER == "azure":
        from openai import AzureOpenAI
        return AzureOpenAI(api_key=C.API_KEY, azure_endpoint=C.AZURE_ENDPOINT,
                           api_version=C.AZURE_API_VERSION, timeout=60, max_retries=0)
    from openai import OpenAI
    # timeout=60: a hung request fails after 60 s instead of the SDK default of 10 min;
    # max_retries=0: retries are handled (and printed) by chat() below
    kw = {"api_key": C.API_KEY or "not-needed", "timeout": 60, "max_retries": 0}
    if C.BASE_URL:
        kw["base_url"] = C.BASE_URL
    if C.KEY_HEADER:                      # e.g. HKUST GenAI gateway expects header "api-key: <key>"
        kw["default_headers"] = {C.KEY_HEADER: C.API_KEY}
    return OpenAI(**kw)


def chat(client, messages, temperature, model=C.MODEL, max_tokens=C.MAX_TOKENS, retries=8):
    """One chat call with exponential back-off. Returns (text, usage_dict).
    Raises RuntimeError if every retry fails, so the subject is NOT saved and gets rerun later."""
    for attempt in range(retries):
        try:
            kw = {"max_tokens": max_tokens} if max_tokens else {}
            r = client.chat.completions.create(model=model, messages=messages, temperature=temperature, **kw)
            u = getattr(r, "usage", None)
            usage = {"in": getattr(u, "prompt_tokens", 0), "out": getattr(u, "completion_tokens", 0)}
            return (r.choices[0].message.content or "").strip(), usage
        except Exception as e:   # rate limit, timeout, 5xx ...
            wait = min(60, 2 ** attempt)
            print(f"  API error ({type(e).__name__}: {e}); retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"API still failing after {retries} attempts")


def credit_balance():
    """Remaining credit on the HKUST GenAI gateway, or None if not available (other providers)."""
    if not (C.BASE_URL and "hkust-genai" in C.BASE_URL and C.API_KEY):
        return None
    import json, urllib.request
    try:
        req = urllib.request.Request(C.BASE_URL.rstrip("/") + "/balance", headers={"api-key": C.API_KEY})
        with urllib.request.urlopen(req, timeout=30) as r:
            return float(json.loads(r.read().decode())["credit"])
    except Exception:
        return None
