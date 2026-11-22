"""Budget lines. One point in A pays M units of A; one point in B pays N units of B.

So with 100 points the budget line is  xA / M + xB / N = 100,
i.e. prices pA = 1/M, pB = 1/N and income 100 (in points).
"""
import numpy as np
import config as C


def draw_prices(rng: np.random.Generator, n: int = C.N_ROUNDS) -> np.ndarray:
    """Return an (n, 2) array of (M, N): M, N ~ U[0.1, 1], two decimals, max(M, N) >= 0.5."""
    out = []
    while len(out) < n:
        m, k = np.round(rng.uniform(C.PRICE_LOW, C.PRICE_HIGH, size=2), 2)
        if max(m, k) >= C.PRICE_MAX_AT_LEAST:
            out.append((m, k))
    return np.array(out)


def subject_seed(domain: str, condition: str, rep: int) -> int:
    """Stable seed per (domain, condition, rep). Same rep -> same prices across conditions,
    so the baseline and its variations face identical budget lines (a paired design)."""
    d = {"risk": 1, "time": 2, "social": 3, "food": 4}[domain]
    return C.SEED_BASE + 1000 * d + rep


def to_quantities(points_a, points_b, m, n):
    """Points -> commodity quantities (xA, xB)."""
    return np.asarray(points_a) * m, np.asarray(points_b) * n


def price_vectors(m, n):
    """(M, N) -> price vectors p = (1/M, 1/N) so that p . x = points spent."""
    return np.column_stack([1.0 / np.asarray(m), 1.0 / np.asarray(n)])


def discrete_options(m, n, k: int = C.N_DISCRETE_OPTIONS):
    """11 points on the budget line: option j puts 10*j points in A (j = 0..10).
    Returns list of (points_a, points_b, xA, xB)."""
    step = C.ENDOWMENT / (k - 1)
    opts = []
    for j in range(k):
        a = step * j
        b = C.ENDOWMENT - a
        opts.append((a, b, round(a * m, 2), round(b * n, 2)))
    return opts
