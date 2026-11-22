"""Tests used in the paper: two-sample and one-sample t-tests, Levene, OLS with robust SE."""
import warnings
import numpy as np
from scipy import stats

warnings.filterwarnings("ignore", category=RuntimeWarning)   # near-constant samples (e.g. all CCEI = 1)


def two_sample(a, b):
    """Two-sided two-sample t-test (Welch; the paper does not say which variant)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    t = stats.ttest_ind(a, b, equal_var=False)
    return dict(mean_a=a.mean(), mean_b=b.mean(), n_a=len(a), n_b=len(b), t=t.statistic, p=t.pvalue)


def one_sample(a, mu):
    a = np.asarray(a, float)
    a = a[~np.isnan(a)]
    t = stats.ttest_1samp(a, mu)
    return dict(mean=a.mean(), mu=mu, n=len(a), t=t.statistic, p=t.pvalue)


def levene(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    r = stats.levene(a[~np.isnan(a)], b[~np.isnan(b)])
    return dict(sd_a=np.nanstd(a, ddof=1), sd_b=np.nanstd(b, ddof=1), W=r.statistic, p=r.pvalue)


def ols_hc1(y, X, names):
    """OLS with HC1 robust standard errors. X must already include a constant column."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    V = XtX_inv @ (X.T * u**2) @ X @ XtX_inv * n / (n - k)
    se = np.sqrt(np.diag(V))
    t = beta / se
    p = 2 * stats.t.sf(np.abs(t), n - k)
    return [dict(term=nm, coef=b, se=s, t=tt, p=pp) for nm, b, s, tt, pp in zip(names, beta, se, t, p)]
