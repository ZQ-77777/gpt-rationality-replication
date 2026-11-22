"""Structural estimation of (alpha, rho) by two-limit (nonlinear) Tobit on expenditure shares.

Paper, Materials and Methods: for all four domains the first-order condition gives
    share_1 = p1 x1 / E = g / ((p1/p2)^r + g),   r = rho / (1 - rho),  g = [alpha / (1 - alpha)]^(1/(1 - rho)).
Shares are censored at 0 and 1 (corner choices) -> two-limit Tobit maximum likelihood.
  risk  : good 1 = the better (larger) outcome, alpha = weight on it (disappointment aversion, Gul 1991)
  time  : good 1 = today,     alpha = weight on today
  social: good 1 = self,      alpha = weight on self
  food  : good 1 = ham meat,  alpha = weight on meat
Because the expenditure share in this design equals points/100, share_1 = points on good 1 / 100.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.special import expit


def shares_and_prices(domain, points_a, points_b, M, N):
    a = np.asarray(points_a, float) / 100
    M, N = np.asarray(M, float), np.asarray(N, float)
    pa_pb = N / M                                  # (1/M) / (1/N)
    if domain == "risk":                           # reorder: good 1 = larger quantity
        xa, xb = a * 100 * M, (1 - a) * 100 * N
        first_is_a = xa >= xb
        s = np.where(first_is_a, a, 1 - a)
        ratio = np.where(first_is_a, pa_pb, 1 / pa_pb)
    else:
        s, ratio = a, pa_pb
    return s, ratio


def _unpack(theta):
    alpha = 1 / (1 + np.exp(-theta[0]))           # (0, 1)
    rho = 1 - np.exp(theta[1])                    # (-inf, 1)
    sigma = np.exp(theta[2])
    return alpha, rho, sigma


def predicted_share(alpha, rho, ratio):
    """g / (ratio^r + g), computed in logs to avoid overflow: expit(ln g - r ln ratio)."""
    r = rho / (1 - rho)
    log_g = np.log(alpha / (1 - alpha)) / (1 - rho)
    return expit(log_g - r * np.log(ratio))


def negloglik(theta, s, ratio, eps=1e-6):
    alpha, rho, sigma = _unpack(theta)
    mu = predicted_share(alpha, rho, ratio)
    lo, hi = s <= eps, s >= 1 - eps
    mid = ~(lo | hi)
    ll = np.zeros_like(s)
    ll[lo] = norm.logcdf((0 - mu[lo]) / sigma)
    ll[hi] = norm.logsf((1 - mu[hi]) / sigma)
    ll[mid] = norm.logpdf((s[mid] - mu[mid]) / sigma) - np.log(sigma)
    v = -np.sum(ll)
    return v if np.isfinite(v) else 1e12


def fit(s, ratio):
    """Return dict(alpha, rho, sigma, nll, ok).
    A coarse grid over (alpha, rho, sigma) picks the two best starting points; Nelder-Mead refines them."""
    s, ratio = np.asarray(s, float), np.asarray(ratio, float)
    grid = [(a, r, sg) for a in np.linspace(-2.5, 2.5, 11)            # logit(alpha)
            for r in np.log([0.02, 0.1, 0.3, 0.6, 1.0, 1.5, 2.5, 5.0, 10.0])   # rho = 1 - e^r
            for sg in np.log([0.02, 0.1, 0.3])]
    vals = np.array([negloglik(g, s, ratio) for g in grid])
    best = None
    for k in np.argsort(vals)[:2]:
        res = minimize(negloglik, x0=list(grid[k]), args=(s, ratio), method="Nelder-Mead",
                       options={"maxiter": 3000, "xatol": 1e-6, "fatol": 1e-8})
        if best is None or res.fun < best.fun:
            best = res
    alpha, rho, sigma = _unpack(best.x)
    return dict(alpha=alpha, rho=rho, sigma=sigma, nll=best.fun, ok=bool(best.success))
