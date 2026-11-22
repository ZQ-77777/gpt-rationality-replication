"""Revealed-preference toolkit: GARP, CCEI (Afriat), HMI, MPI, MCI, Bronars power test.

Inputs for one subject:
  P : (n, k) prices,  X : (n, k) chosen quantities.
E[i, j] = p_i . x_j  = cost of bundle j at the prices of round i.
x_i is directly revealed preferred to x_j  (x_i R0 x_j)  if  E[i, i] >= E[i, j].
"""
from itertools import combinations
import numpy as np

TOL = 1e-9


def cost_matrix(P, X):
    return np.asarray(P, float) @ np.asarray(X, float).T


def closure(R):
    """Transitive closure (Warshall)."""
    R = R.copy()
    for k in range(R.shape[0]):
        R |= R[:, [k]] & R[[k], :]
    return R


def garp_ok(E, e=1.0, keep=None):
    """True if GARP holds at efficiency e (Afriat: compare e * own expenditure)."""
    own = np.diag(E)[:, None]
    R0 = e * own >= E - TOL          # weak direct revealed preference
    S0 = e * own > E + TOL           # strict direct revealed preference
    if keep is not None:
        R0, S0 = R0[np.ix_(keep, keep)], S0[np.ix_(keep, keep)]
    Rc = closure(R0)
    return not np.any(Rc & S0.T)     # x_i R* x_j and x_j P0 x_i  -> violation


def n_violations(E):
    """Number of ordered pairs (i, j) with x_i R* x_j and x_j P0 x_i."""
    own = np.diag(E)[:, None]
    Rc = closure(own >= E - TOL)
    return int(np.sum(Rc & (own > E + TOL).T))


def ccei(P, X):
    """Critical cost efficiency index in [0, 1] = sup{e : GARP holds at efficiency e}.
    Exact: the relations only change at the ratios E_ij / E_ii, so the sup is one of them
    (or 1). GARP_e is monotone in e, so we binary-search the sorted candidates, testing just
    below each candidate (the sup itself may not be attained)."""
    E = cost_matrix(P, X)
    if garp_ok(E, 1.0):
        return 1.0
    own = np.diag(E)
    ratios = np.unique((E / own[:, None])[~np.eye(len(E), dtype=bool)])
    cand = np.r_[np.sort(ratios[(ratios < 1) & (ratios > 0)]), 1.0]
    lo, hi, best = 0, len(cand) - 1, 0.0
    while lo <= hi:
        mid = (lo + hi) // 2
        if garp_ok(E, cand[mid] * (1 - 1e-9)):
            best, lo = cand[mid], mid + 1
        else:
            hi = mid - 1
    return float(best)


def hmi(P, X, max_checks=2_000_000):
    """Houtman-Maks index: largest share of observations that jointly satisfy GARP.
    Exact search over observations involved in violations; greedy fallback if too many."""
    E = cost_matrix(P, X)
    n = len(E)
    if garp_ok(E):
        return 1.0, True
    own = np.diag(E)[:, None]
    Rc = closure(own >= E - TOL)
    V = Rc & (own > E + TOL).T
    involved = sorted(set(np.where(V)[0]) | set(np.where(V)[1]))
    checks = 0
    for k in range(1, len(involved) + 1):
        for drop in combinations(involved, k):
            checks += 1
            if checks > max_checks:
                return _hmi_greedy(E), False
            keep = [i for i in range(n) if i not in drop]
            if garp_ok(E, 1.0, keep):
                return (n - k) / n, True
    return 1 / n, True


def _hmi_greedy(E):
    keep = list(range(len(E)))
    while not garp_ok(E, 1.0, keep):
        sub = E[np.ix_(keep, keep)]
        own = np.diag(sub)[:, None]
        V = closure(own >= sub - TOL) & (own > sub + TOL).T
        worst = int(np.argmax(V.sum(0) + V.sum(1)))
        keep.pop(worst)
    return len(keep) / len(E)


def mpi(P, X):
    """Money pump index (Echenique, Lee & Shum 2011) over violating 2-cycles.
    With two goods every GARP violation implies a 2-cycle violation (Rose 1958), so 2-cycles suffice
    to detect violations; we report the mean and max MPI over those cycles (0 if none)."""
    E = cost_matrix(P, X)
    own = np.diag(E)
    vals = []
    for i, j in combinations(range(len(E)), 2):
        a = own[i] - E[i, j]          # money saved at prices i by buying x_j instead of x_i
        b = own[j] - E[j, i]
        if (a >= -TOL and b > TOL) or (a > TOL and b >= -TOL):
            vals.append((a + b) / (own[i] + own[j]))
    return (float(np.mean(vals)), float(np.max(vals))) if vals else (0.0, 0.0)


def mci(P, X):
    """Minimum cost index (Dean & Martin 2016): cheapest set of direct revealed-preference relations
    to drop so the rest is GARP-consistent. Cost of dropping x_i R0 x_j = (E_ii - E_ij) / sum_k E_kk.
    Solved as a small MILP with utility levels U (weak edge: U_i >= U_j; strict edge: U_i >= U_j + 1)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    E = cost_matrix(P, X)
    if garp_ok(E):
        return 0.0
    n = len(E)
    own = np.diag(E)
    edges = [(i, j) for i in range(n) for j in range(n) if i != j and own[i] >= E[i, j] - TOL]
    m = len(edges)
    M = n + 2
    # variables: U_0..U_{n-1} (continuous in [0, n]), b_0..b_{m-1} (binary drop indicators)
    c = np.r_[np.zeros(n), [(own[i] - E[i, j]) / own.sum() for i, j in edges]]
    A = np.zeros((m, n + m))
    lb = np.zeros(m)
    for r, (i, j) in enumerate(edges):
        A[r, i], A[r, j], A[r, n + r] = 1, -1, M          # U_i - U_j + M b >= need
        lb[r] = 1.0 if own[i] > E[i, j] + TOL else 0.0
    res = milp(c, constraints=LinearConstraint(A, lb, np.inf),
               integrality=np.r_[np.zeros(n), np.ones(m)],
               bounds=Bounds(np.r_[np.zeros(n), np.zeros(m)], np.r_[np.full(n, n), np.ones(m)]))
    return float(res.fun) if res.success else np.nan


def bronars(P, rng, n_sim=1000):
    """Random choosers: uniform share of budget on each line (Bronars 1987). Returns CCEI array.
    P are prices with income normalised so that p . x = 100 points."""
    P = np.asarray(P, float)
    out = np.empty(n_sim)
    for s in range(n_sim):
        share = rng.uniform(0, 1, len(P))
        X = np.column_stack([share * 100 / P[:, 0], (1 - share) * 100 / P[:, 1]])
        out[s] = ccei(P, X)
    return out
