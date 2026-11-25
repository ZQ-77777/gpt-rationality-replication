"""Check the analysis code before spending any API credit. Run: python scripts/00_selftest.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src import rp
from src.estimate import predicted_share, fit, shares_and_prices
from src.prices import draw_prices
from src.parse import parse_continuous, parse_discrete
from src import prompts as Pm

ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# 1. textbook GARP violation: two budget lines, each choice affordable and cheaper on the other line
P = np.array([[1, 2], [2, 1.]]); X = np.array([[1, 4], [4, 1.]])
check("CCEI = 2/3 on the two-line example", abs(rp.ccei(P, X) - 2 / 3) < 1e-9)
check("HMI = 1/2", rp.hmi(P, X)[0] == 0.5)
check("MPI = 1/3", abs(rp.mpi(P, X)[0] - 1 / 3) < 1e-9)
check("MCI = 1/6", abs(rp.mci(P, X) - 1 / 6) < 1e-6)

# 2. an exact CES maximiser is perfectly rational
rng = np.random.default_rng(0)
pr = draw_prices(rng); M, N = pr[:, 0], pr[:, 1]
share = predicted_share(0.6, 0.3, N / M)
Pp = np.column_stack([1 / M, 1 / N]); Xp = np.column_stack([share * 100 * M, (1 - share) * 100 * N])
check("CES agent: CCEI = 1, HMI = 1, MCI = 0",
      rp.ccei(Pp, Xp) == 1 and rp.hmi(Pp, Xp)[0] == 1 and rp.mci(Pp, Xp) == 0)

# 3. random choosers usually violate GARP (Bronars power)
viol = np.mean(rp.bronars(Pp, rng, 300) < 1)
check(f"Bronars: {viol:.1%} of random subjects violate GARP (paper: 99.9%)", viol > 0.95)

# 4. Tobit recovers known parameters
pr = np.vstack([draw_prices(rng) for _ in range(40)]); M, N = pr[:, 0], pr[:, 1]
for a0, r0 in [(0.6, 0.3), (0.5, -1.0), (0.75, 0.6)]:
    s = np.clip(predicted_share(a0, r0, N / M) + 0.03 * rng.normal(size=len(M)), 0, 1)
    e = fit(s, N / M)
    check(f"Tobit recovers alpha={a0}, rho={r0} -> {e['alpha']:.3f}, {e['rho']:.3f}",
          abs(e["alpha"] - a0) < 0.03 and abs(e["rho"] - r0) < 0.1)

# 5. parser
check("parse 'Asset A: 30, Asset B: 70'", parse_continuous("Asset A: 30, Asset B: 70", "Asset A", "Asset B")[2])
check("parse 'I choose Option 4.' (paraphrase)", parse_discrete("I choose Option 4.", allow_option_number=True) == (3, True))
check("reject 'A: 80, B: 80'", not parse_continuous("A: 80, B: 80", "A", "B")[2])
r = parse_continuous("I will invest 60 points in Asset A and 40 points in Asset B, which returns 52.8 dollars.", "Asset A", "Asset B")
check("parse free text with dollar amounts -> 60/40", r[2] and round(r[0]) == 60)
r = parse_continuous("Today: 100 points\nOne month later: 0 points", "today", "one month later")
check("parse 'Today: 100 points / One month later: 0 points'", r[2] and round(r[0]) == 100)
from src.prices import discrete_options
opts = [(o[2], o[3]) for o in discrete_options(0.88, 0.30)]
check("parse discrete pair '($52.80, $12.00)' -> option 7", parse_discrete("My best option is ($52.80, $12.00).", opts) == (6, True))
listing = "To determine the best option: 1. ($0.00, $30.00) -> 30 2. ($8.80, $27.00) -> 35.8 ... Therefore, I choose ($88.00, $0.00)."
check("discrete: list of options then choice -> last option", parse_discrete(listing, opts) == (10, True))
check("discrete: 'The best option in this round is (...)' among others",
      parse_discrete("Comparing ($0.00, $30.00) with others, the best option in this round is ($88.00, $0.00).", opts) == (10, True))
check("discrete: superlative sentence fallback",
      parse_discrete("($0.00, $30.00) is safe. However, ($88.00, $0.00) offers the highest potential return.", opts) == (10, True))
check("discrete: list cut off before the choice -> invalid", not parse_discrete("To determine the best option: 1. ($0.00, $30.00) 2. ($8.80, $27.00) 3. ($17", opts)[1])
# parser v2: counterexamples that version 1 got wrong
r = parse_continuous("I allocate 30 points to Asset B and 70 points to Asset A.", "Asset A", "Asset B")
check("v2: labels in reverse order -> A=70", r[2] and round(r[0]) == 70)
r = parse_continuous("Asset A: 50, Asset B: 50 is one possibility. My final allocation is Asset A: 70, Asset B: 30.", "Asset A", "Asset B")
check("v2: final allocation wins over an earlier one -> A=70", r[2] and round(r[0]) == 70)
check("v2: negative amount -> invalid", not parse_continuous("Asset A: -20, Asset B: 80", "Asset A", "Asset B")[2])
check("v2: dash as separator is not a minus sign", parse_continuous("Asset A - 70, Asset B - 30", "Asset A", "Asset B")[2])
r = parse_continuous("I would allocate 70 points for the other person and 30 points for myself.", "yourself", "the other")
check("v2: synonyms (myself / the other person) -> self=30", r[2] and round(r[0]) == 30)
check("v2: 'Option 1 is worse. I choose Option 11.' -> option 11",
      parse_discrete("Option 1 is less attractive. I choose Option 11.", allow_option_number=True) == (10, True))
check("v2: off-menu final choice after an on-menu mention -> invalid",
      not parse_discrete("Consider ($0.00, $30.00). I choose ($30.00, $0.00).", opts)[1])

# 6. prompts render
msg = Pm.round_message("risk", "inverse", "continuous", 1, 0.5, 0.25)
check("inverse framing shows 2.00 and 4.00 points", "2.00 points" in msg and "4.00 points" in msg)
print("\nALL PASSED" if ok else "\nSOME CHECKS FAILED")
