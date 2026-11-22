"""Original prompts of Chen, Liu, Shan & Zhong (2023), copied from arXiv:2305.12763v3, Appendix A
(the paper is distributed under CC BY-NC-ND 4.0; reproduced verbatim, with attribution, for replication).

Choose this set with LLM_PROMPTS=paper (the default). Differences from the paraphrased set
(src/prompts.py): no "Round k." prefix, no fixed answer format, comprehension questions written in
the same frame as the condition (price framing / discrete), options listed as "($M1,$N1), ...".
Persona variants replace "a human decision maker" in the system message (paper, Section 2.2).
"""
from src.prices import discrete_options

SYSTEM = ("I want you to act as {who}. You will be given 25 rounds of decision-making tasks and will "
          "be responsible for making decisions. You should use your best judgment to come up with "
          "solutions that you like most. My first request is “You must provide your answers in every "
          "round.” If you do not provide an answer, I will assume that you make a random choice.")

WHO = {
    None: "a human decision maker",
    "female": "a female decision maker",
    "male": "a male decision maker",
    "young child": "a young child decision maker",
    "elderly": "an elderly decision maker",
    "elementary_edu": "a decision maker with an elementary school education",
    "college_edu": "a decision maker with a college education",
    "Asian": "an Asian decision maker",
    "African American": "an African American decision maker",
}

LABELS = {"risk": ("Asset A", "Asset B"), "time": ("today", "one month later"),
          "social": ("yourself", "the other"), "food": ("meat", "tomato")}

# ---------------- assistant messages ----------------
_RISK_CONT = ("In every round, the decision maker has 100 points that need to be invested between Asset A "
              "and Asset B. The decision maker has a 50% chance to get the return from Asset A or the other "
              "50% chance to get the return from Asset B. First please only tell me the number of points for "
              "investing Asset A, then please only tell me the number of points for investing Asset B.")
_TIME_CONT = ("In every round, the decision maker has 100 points that need to be invested between today and "
              "one month later. The decision maker will get dollars today from the points invested today and "
              "will get check that can be cashed in one month later from the points invested one month later. "
              "Please first only tell me the number of points for investing today, then please only tell me "
              "the number of points for investing one month later.")
_SOC_CONT = ("In every round, the decision maker is randomly matched with a new anonymous subject and there is "
             "no feedback across rounds. The decision maker has 100 points that need to be allocated between "
             "him/herself and the other one. The decision maker will get return from the points allocated to "
             "him/herself and the other one will get return from the points allocated to him/her. First please "
             "only tell me the number of points you want to allocate to yourself, then please only tell me the "
             "number of points you want to allocate to the other.")
_FOOD_CONT = ("In every round, the decision maker has 100 points that need to be spent between ham meat and "
              "tomato. The decision maker will get the amount of meat and tomato he/she spends on. First please "
              "only tell me the number of points for meat, then please only tell me the number of points for tomato.")

ASSISTANT = {
    ("risk", "continuous"): _RISK_CONT,
    ("time", "continuous"): _TIME_CONT,
    ("social", "continuous"): _SOC_CONT,
    ("food", "continuous"): _FOOD_CONT,
    ("risk", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form ($M, $N). The decision maker has a 50% chance to get M from Asset A or the "
                           "other 50% chance to get N from Asset B. Please only tell me about your best option in "
                           "every round."),
    ("time", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form ($M, $N). The decision maker will get M dollars today and will get a N "
                           "dollars check that can be cashed in one month later. Please only tell me about your "
                           "best option in every round."),
    ("social", "discrete"): ("In every round, the decision maker is randomly matched with a new anonymous subject "
                             "and there is no feedback across rounds. The decision maker will be presented with 11 "
                             "options, each represented in the form ($M, $N). The decision maker will get M dollars "
                             "and the other will get N dollars. Please only tell me about your best option in every "
                             "round."),
    ("food", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form (M Kg, N Kg). The decision maker will get M Kg of meat and get N Kg of "
                           "tomato. Please only tell me about your best option in every round."),
}

# ---------------- comprehension questions ----------------
_R_BASE = ("investing every 1 point for Asset A returns 0.8 dollars, and investing every 1 point for Asset B "
           "returns 0.2 dollars")
_R_INV = ("investing every 1.25 points for Asset A returns 1 dollar, and investing every 5 points for Asset B "
          "returns 1 dollar")
_T_BASE = ("investing every 1 point for today returns 0.8 dollars cash today, and investing every 1 point for one "
           "month later returns 0.2 dollars check which can be cashed one month later")
_T_INV = ("investing every 1.25 points for today returns 1 dollar cash today, and investing every 5 points for "
          "one month later returns 1 dollar check which can be cashed one month later")

TESTS = {
    ("risk", "baseline"): [
        "What is the probability you will get a return from Asset A?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_BASE}. What return will you get?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_BASE}. Is there a chance to get 72 dollars?"],
    ("risk", "inverse"): [
        "What is the probability you will get a return from Asset A?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_INV}. What return will you get?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_INV}. Is there a chance to get 72 dollars?"],
    ("risk", "discrete"): [
        "What is the probability you will get a return from Asset A?",
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), is there a chance to get 72 dollars?"],
    ("time", "baseline"): [
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_BASE}. What return will you get?",
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_BASE}. When can you get just the 2 dollars cash?",
        f"In this round, {_T_BASE}. What is your allocation? Why?"],
    ("time", "inverse"): [
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_INV}. What return will you get?",
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_INV}. When can you get just the 2 dollars cash?",
        f"In this round, {_T_INV}. What is your allocation? Why?"],
    ("time", "discrete"): [
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), when can you get just the 2 dollars cash?",
        "If you face the options ($40, $10) and ($72, $2), which option will you select? Why?"],
    ("social", "baseline"): [
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1 point to yourself returns 0.8 dollars for yourself, and allocating every 1 point to the other returns 0.2 dollars for the other. What return will you get?",
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1 point for yourself returns 0.8 dollars for yourself, and allocating every 1 point for the other returns 0.2 dollars for the other. Who will get just 2 dollars?",
        "In this round, allocating every 1 point for yourself returns 0.8 dollars for yourself, and allocating every 1 point for the other returns 0.2 dollars for the other. Will you allocate to the other? Why?"],
    ("social", "inverse"): [
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, every 1.25 points to yourself returns 1 dollar for yourself, allocating every 5 points to the other returns 1 dollar for the other. What return will you get?",
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1.25 points for yourself returns 1 dollar for yourself, and allocating every 5 points for the other returns 1 dollar for the other. Who will get just 2 dollars?",
        "In this round, allocating every 1.25 points for yourself returns 1 dollar for yourself, and allocating every 5 points for the other returns 1 dollar for the other. Will you allocate to the other? Why?"],
    ("social", "discrete"): [
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), who will get just 2 dollars?",
        "If you face the options ($40, $10) and ($72, $2), which option will you select? Why?"],
    ("food", "baseline"): [
        "What goods can you get from decisions?",
        "Suppose that you spend 90 points to meat, and 10 points to tomato. In this round, spending every 1 point for meat will get 0.8 Kg meat, and spending every 1 point for tomato will get 0.2 Kg tomato, what will you get?",
        "In this round, spending every 1 point for meat will get 0.8 Kg meat, and spending every 1 point for tomato will get 0.2 Kg tomato. What is your allocation? Why?"],
    ("food", "inverse"): [
        "What goods can you get from decisions?",
        "Suppose that you spend 90 points to meat, and 10 points to tomato. In this round, spending every 1.25 point for meat will get 1 Kg meat, and spending every 5 points for tomato will get 1 Kg tomato, what will you get?",
        "In this round, spending every 1.25 points for meat will get 1 Kg meat, and spending every 5 points for tomato will get 1 Kg tomato. What is your allocation? Why?"],
    ("food", "discrete"): [
        "What goods can you get from decisions?",
        "Suppose you choose the option (72 Kg, 2 Kg), what will you get?",
        "Suppose you face the options (40 Kg, 10 Kg) and (72 Kg, 2 Kg), which option will you select? Why?"],
}

# ---------------- decision tasks ----------------
TASK = {
    ("risk", "baseline"): "In this round, investing every 1 point for Asset A returns {m} dollars, and investing every 1 point for Asset B returns {n} dollars. What is your allocation?",
    ("risk", "inverse"): "In this round, investing every {m} points for Asset A returns 1 dollar, and investing every {n} points for Asset B returns 1 dollar. What is your allocation?",
    ("time", "baseline"): "In this round, investing every 1 point for today returns {m} dollars today, and investing every 1 point for one month later returns {n} dollars check which can be cashed in one month later. What is your allocation?",
    ("time", "inverse"): "In this round, investing every {m} points for today returns 1 dollar today, and investing every {n} points for one month later returns 1 dollar check which can be cashed in one month later. What is your allocation?",
    ("social", "baseline"): "In this round, allocating every 1 point for yourself returns {m} dollars for yourself, and allocating every 1 point for the other one returns {n} dollars for him/her. What is your allocation?",
    ("social", "inverse"): "In this round, allocating every {m} points for yourself returns 1 dollar for yourself, and allocating every {n} points for the other one returns 1 dollar for him/her. What is your allocation?",
    ("food", "baseline"): "In this round, spending every 1 point on meat will get {m} Kg meat, and spending every 1 point on tomato will get {n} Kg tomato. What is your allocation?",
    ("food", "inverse"): "In this round, spending every {m} points on meat will get 1 Kg meat, and spending every {n} points on tomato will get 1 Kg tomato. What is your allocation?",
}


def _key(cfg):
    return "discrete" if cfg["choice"] == "discrete" else cfg["framing"]


def opening_messages(domain, cfg):
    return [{"role": "system", "content": SYSTEM.format(who=WHO[cfg["demo"]])},
            {"role": "assistant", "content": ASSISTANT[(domain, cfg["choice"])]}]


def test_questions(domain, cfg):
    return TESTS[(domain, _key(cfg))]


def option_text(domain, xa, xb):
    return f"({xa:.2f} Kg,{xb:.2f} Kg)" if domain == "food" else f"(${xa:.2f},${xb:.2f})"


def round_message(domain, cfg, rnd, m, n):
    if cfg["choice"] == "discrete":
        opts = ", ".join(option_text(domain, o[2], o[3]) for o in discrete_options(m, n))
        return f"In this round, there are 11 options, which are {opts}. Which is the best?"
    if cfg["framing"] == "inverse":                      # "every 1/M points ... returns 1 dollar", 2 decimals
        return TASK[(domain, "inverse")].format(m=f"{1 / m:.2f}", n=f"{1 / n:.2f}")
    return TASK[(domain, "baseline")].format(m=f"{m:.2f}", n=f"{n:.2f}")


def labels(domain):
    return LABELS[domain]
