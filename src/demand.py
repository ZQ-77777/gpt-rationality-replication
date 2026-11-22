"""Downward-sloping demand: Spearman correlation of ln(xA/xB) with ln(pA/pB) per subject."""
import numpy as np
from scipy.stats import spearmanr
import config as C


def spearman_subject(points_a, points_b, M, N):
    a = np.maximum(np.asarray(points_a, float), C.CORNER_ADJ_POINTS)   # 0.1% of budget at corners
    b = np.maximum(np.asarray(points_b, float), C.CORNER_ADJ_POINTS)
    M, N = np.asarray(M, float), np.asarray(N, float)
    log_x = np.log((a * M) / (b * N))
    log_p = np.log((1 / M) / (1 / N))
    if np.ptp(log_x) == 0:          # identical choices in every round -> undefined
        return np.nan
    return float(spearmanr(log_x, log_p).statistic)
