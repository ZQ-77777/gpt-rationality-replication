"""Prompt builder.

Structure follows the paper (Methods + SI Appendix A): a system message (role), an
"assistant" message that stores the decision format, three comprehension questions, then
25 decision rounds as user messages in one conversation. The wording below is our own
paraphrase of that structure; replace it with the authors' SI text if you have it.
"""
import config as C
from src.prices import discrete_options

# domain -> labels and how a point converts into payoff
DOMAIN = {
    "risk": dict(
        a="Asset A", b="Asset B", unit="dollars",
        setting=("In every round, the decision maker has 100 points to invest between Asset A and "
                 "Asset B. After the decision, one asset is selected: there is a 50% chance the "
                 "return comes from Asset A and a 50% chance it comes from Asset B. The decision "
                 "maker receives only the return of the selected asset."),
        tests=[
            "What is the probability that the return comes from Asset A?",
            "Suppose investing every 1 point for Asset A returns 0.8 dollars and investing every 1 point "
            "for Asset B returns 0.2 dollars. If you put 90 points in Asset A and 10 points in Asset B, "
            "what are the possible returns?",
            "In the situation of the previous question, is it possible to receive 72 dollars?",
        ]),
    "time": dict(
        a="today", b="one month later", unit="dollars",
        setting=("In every round, the decision maker has 100 points to allocate between today and one "
                 "month later. Points allocated to today are paid in cash today. Points allocated to one "
                 "month later are paid by a check that can be cashed one month from today. The decision "
                 "maker receives both payments."),
        tests=[
            "Suppose every 1 point for today pays 0.8 dollars and every 1 point for one month later pays "
            "0.2 dollars. If you allocate 90 points to today and 10 points to one month later, what is the "
            "total amount you receive?",
            "In the situation of the previous question, when can you receive the 2 dollars?",
            "In that situation, what allocation would you choose, and why?",
        ]),
    "social": dict(
        a="yourself", b="the other person", unit="dollars",
        setting=("In every round, the decision maker is randomly matched with a new anonymous subject, "
                 "and there is no feedback across rounds. The decision maker has 100 points to allocate "
                 "between herself or himself and the other person. Both receive their payments."),
        tests=[
            "Suppose every 1 point for yourself pays you 0.8 dollars and every 1 point for the other person "
            "pays the other person 0.2 dollars. If you allocate 90 points to yourself and 10 points to the "
            "other person, how much does each of you receive?",
            "In the situation of the previous question, who receives the 2 dollars?",
            "Will you allocate anything to the other person? Why?",
        ]),
    "food": dict(
        a="ham meat", b="tomato", unit="units",
        setting=("In every round, the decision maker has 100 points that need to be spent between ham meat "
                 "and tomato. The decision maker receives the food bundle that is chosen."),
        tests=[
            "Suppose every 1 point for ham meat buys 0.8 units of ham meat and every 1 point for tomato buys "
            "0.2 units of tomato. If you spend 90 points on ham meat and 10 points on tomato, what do you get?",
            "Can you receive 72 units of ham meat and 2 units of tomato with 100 points in that situation?",
            "What will you do in each round?",
        ]),
}

DEMO_PHRASE = {
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


def system_message(demo=None) -> str:
    return (f"I want you to act as {DEMO_PHRASE[demo]}. You will make decisions in "
            f"{C.N_ROUNDS} rounds. You should use your best judgment to come up with solutions that you "
            "like most. You must give an answer in every round; a missing answer is treated as a random choice.")


def answer_format(domain: str, choice: str) -> str:
    d = DOMAIN[domain]
    if choice == "discrete":
        return "Please only tell me your best option, in the form: Option <number>."
    return (f"Please only tell me your allocation, in the form: {d['a']}: <points>, {d['b']}: <points>. "
            "The two numbers must add up to 100.")


def assistant_message(domain: str, choice: str) -> str:
    d = DOMAIN[domain]
    return (f"{d['setting']} In each round, the payoff per point for {d['a']} and for {d['b']} changes. "
            f"I will describe the payoffs and you choose. {answer_format(domain, choice)} "
            "I will not ask you to decide yet.")


def _price_text(domain, framing, m, n):
    d = DOMAIN[domain]
    if framing == "baseline":     # "1 point = X units"
        return (f"every 1 point for {d['a']} returns {m:.2f} {d['unit']}, and every 1 point for "
                f"{d['b']} returns {n:.2f} {d['unit']}")
    # inverse framing: "Y points = 1 unit"
    return (f"every {1 / m:.2f} points for {d['a']} return 1 {d['unit'][:-1]}, and every {1 / n:.2f} points "
            f"for {d['b']} return 1 {d['unit'][:-1]}")


def round_message(domain, framing, choice, rnd, m, n) -> str:
    d = DOMAIN[domain]
    if choice == "discrete":
        opts = discrete_options(m, n)
        listing = "; ".join(f"Option {j + 1}: ({d['a']} {o[2]:.2f}, {d['b']} {o[3]:.2f})"
                            for j, o in enumerate(opts))
        return (f"Round {rnd}. In this round, there are {len(opts)} options (amounts in {d['unit']}): "
                f"{listing}. Which is the best? {answer_format(domain, choice)}")
    return (f"Round {rnd}. In this round, {_price_text(domain, framing, m, n)}. "
            f"What is your allocation? {answer_format(domain, choice)}")


def opening_messages(domain, condition_cfg):
    """Messages before the comprehension questions."""
    return [
        {"role": "system", "content": system_message(condition_cfg["demo"])},
        {"role": "assistant", "content": assistant_message(domain, condition_cfg["choice"])},
    ]
