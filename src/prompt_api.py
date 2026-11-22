"""One interface to the two prompt sets (LLM_PROMPTS = "paper" or "paraphrase")."""
import config as C
from src import prompts as PARA
from src import prompts_paper as PAPER
from src.prices import discrete_options


def opening_messages(domain, cfg):
    return (PAPER if C.PROMPT_SET == "paper" else PARA).opening_messages(domain, cfg)


def test_questions(domain, cfg):
    if C.PROMPT_SET == "paper":
        return PAPER.test_questions(domain, cfg)
    return PARA.DOMAIN[domain]["tests"]


def round_message(domain, cfg, rnd, m, n):
    if C.PROMPT_SET == "paper":
        return PAPER.round_message(domain, cfg, rnd, m, n)
    return PARA.round_message(domain, cfg["framing"], cfg["choice"], rnd, m, n)


def labels(domain):
    if C.PROMPT_SET == "paper":
        return PAPER.labels(domain)
    return PARA.DOMAIN[domain]["a"], PARA.DOMAIN[domain]["b"]


def option_values(m, n):
    """The 11 options as (xA, xB), rounded as shown to the model."""
    return [(o[2], o[3]) for o in discrete_options(m, n)]
