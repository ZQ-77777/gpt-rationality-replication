"""Run one GPT 'subject': opening messages, 3 comprehension questions, 25 decision rounds."""
import re
import numpy as np
import config as C
from src import prompt_api as P
from src.prices import draw_prices, subject_seed, discrete_options
from src.parse import parse_continuous, parse_discrete
from src.llm_client import chat


class MockClient:
    """Offline stand-in for an LLM: a noisy CES utility maximiser. Lets you test the whole
    pipeline without spending API credit. Not a model of GPT. Understands both prompt sets."""

    def __init__(self, alpha=0.6, rho=0.3, noise=0.0, seed=0):
        self.alpha, self.rho, self.noise = alpha, rho, noise
        self.rng = np.random.default_rng(seed)

    def reply(self, messages):
        last = messages[-1]["content"]
        if not ("What is your allocation?" in last or "Which is the best?" in last) or "Suppose" in last \
                or "Why?" in last:
            return "Understood."
        nums = [float(v) for v in re.findall(r"(\d+\.\d+)", last)]
        if "options" in last:   # discrete: option 1 = (0, 100N), option 2 = (10M, 90N)
            pairs = list(zip(nums[0::2], nums[1::2]))
            m, n = pairs[1][0] / 10, pairs[0][1] / 100
            a = self._optimum(m, n)
            j = int(np.argmin([abs(10 * k - a) for k in range(len(pairs))]))
            if "Option 1:" in last:                       # paraphrased prompts
                return f"Option {j + 1}"
            return f"I choose (${pairs[j][0]:.2f}, ${pairs[j][1]:.2f})."
        if " 1 dollar" in last or " 1 Kg" in last:       # inverse framing: numbers are 1/M, 1/N
            m, n = 1 / nums[0], 1 / nums[1]
        else:
            m, n = nums[0], nums[1]
        a = round(self._optimum(m, n))
        return f"I would put {a} points in the first and {100 - a} points in the second."

    def _optimum(self, m, n):
        # share of points on A for CES u = [a xA^r + (1-a) xB^r]^(1/r), prices 1/M, 1/N
        ra = self.rho / (1 - self.rho)
        g = (self.alpha / (1 - self.alpha)) ** (1 / (1 - self.rho))
        share = g / ((n / m) ** ra + g)        # pA/pB = (1/M)/(1/N) = N/M
        share = np.clip(share + self.noise * self.rng.normal(), 0, 1)
        return 100 * share


def _ask(client, messages, temperature):
    if isinstance(client, MockClient):
        return client.reply(messages), {"in": 0, "out": 0}
    return chat(client, messages, temperature)


def run_subject(client, domain, cond_name, rep, keep_transcript=True):
    cfg = C.CONDITIONS[cond_name]
    rng = np.random.default_rng(subject_seed(domain, cond_name, rep))
    prices = draw_prices(rng)
    msgs = P.opening_messages(domain, cfg)
    usage = {"in": 0, "out": 0}
    tests = []
    for q in P.test_questions(domain, cfg):          # comprehension check, kept in the history
        msgs.append({"role": "user", "content": q})
        ans, u = _ask(client, msgs, cfg["temperature"])
        msgs.append({"role": "assistant", "content": ans})
        tests.append(ans)
        usage = {k: usage[k] + u[k] for k in usage}
    rows = []
    lab_a, lab_b = P.labels(domain)
    for r, (m, n) in enumerate(prices, start=1):
        msgs.append({"role": "user", "content": P.round_message(domain, cfg, r, m, n)})
        ans, u = _ask(client, msgs, cfg["temperature"])
        msgs.append({"role": "assistant", "content": ans})
        usage = {k: usage[k] + u[k] for k in usage}
        if cfg["choice"] == "discrete":
            j, ok = parse_discrete(ans, P.option_values(m, n), allow_option_number=(C.PROMPT_SET != "paper"))
            a, b = (discrete_options(m, n)[j][0], discrete_options(m, n)[j][1]) if ok else (None, None)
        else:
            a, b, ok = parse_continuous(ans, lab_a, lab_b)
        if cfg["framing"] == "inverse":   # the model saw 1/M rounded to 2 decimals: use what it saw
            m, n = 1 / round(1 / m, 2), 1 / round(1 / n, 2)
        rows.append(dict(condition=cond_name, domain=domain, rep=rep, round=r, M=m, N=n,
                         points_a=a, points_b=b, valid=bool(ok), reply=ans, prompts=C.PROMPT_SET))
    meta = dict(condition=cond_name, domain=domain, rep=rep, prompts=C.PROMPT_SET, model=C.MODEL,
                usage=usage, tests=tests, transcript=msgs if keep_transcript else None)
    return rows, meta
