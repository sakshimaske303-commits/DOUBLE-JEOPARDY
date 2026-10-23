"""Independent check of the coral trend p-values in data/coral_trend_results.csv.

Recomputes the seasonal Mann-Kendall test and the Hirsch-Slack (1984) correction for
serial correlation between seasons from scratch with NumPy/SciPy (no pymannkendall),
on the same calendar-month series, and compares the p-values with the stored ones.

Run from the repository root:
    python scripts/validation/coral_trend_check.py
"""
import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

ISLANDS = ["maldives", "seychelles", "fiji", "lakshadweep"]


def monthly_matrix(island):
    df = pd.read_csv(f"data/coral_bleaching_v3/{island}_dhw_reefcells_mean.csv")
    t = pd.to_datetime(df["time"], utc=True).dt.tz_convert(None)
    m = pd.Series(df["dhw_mean"].to_numpy(), index=t).resample("MS").mean()
    full = pd.date_range("1996-01-01", "2020-12-01", freq="MS")
    m = m.reindex(full).interpolate(limit=2, limit_area="inside")
    return m.to_numpy().reshape(-1, 12)  # years x months


def seasonal_mk(X):
    """Returns S, variance assuming independent seasons, Hirsch-Slack variance."""
    n, g = X.shape
    S = 0.0
    for k in range(g):
        x = X[:, k]
        S += np.sign(x[None, :] - x[:, None])[np.triu_indices(n, 1)].sum()
    # covariance between seasons (Hirsch & Slack 1984); the diagonal is Var(S_k) with ties
    R = np.column_stack([rankdata(X[:, k]) for k in range(g)])
    cov = np.zeros((g, g))
    iu = np.triu_indices(n, 1)
    for a in range(g):
        da = np.sign(X[:, a][None, :] - X[:, a][:, None])[iu]
        for b in range(g):
            db = np.sign(X[:, b][None, :] - X[:, b][:, None])[iu]
            K = (da * db).sum()
            cov[a, b] = (K + 4 * (R[:, a] * R[:, b]).sum() - n * (n + 1) ** 2) / 3
    var_indep = np.trace(cov)
    var_hs = cov.sum()
    return S, var_indep, var_hs


def pval(S, var):
    z = (S - np.sign(S)) / np.sqrt(var) if S != 0 else 0.0
    return 2 * (1 - norm.cdf(abs(z)))


if __name__ == "__main__":
    stored = pd.read_csv("data/coral_trend_results.csv")
    stored = stored[stored["series"] == "reef_cells"].set_index("island")
    rows = []
    for isl in ISLANDS:
        X = monthly_matrix(isl)
        assert not np.isnan(X).any(), f"{isl}: missing months"
        S, v0, vhs = seasonal_mk(X)
        rows.append(dict(island=isl, S=int(S),
                         p_seasonal_recomputed=pval(S, v0), p_seasonal_stored=stored.loc[isl, "monthly_smk_p"],
                         p_corrected_recomputed=pval(S, vhs), p_corrected_stored=stored.loc[isl, "csmk_p"]))
    out = pd.DataFrame(rows)
    out["max_abs_diff"] = np.maximum((out.p_seasonal_recomputed - out.p_seasonal_stored).abs(),
                                     (out.p_corrected_recomputed - out.p_corrected_stored).abs())
    print(out.round(4).to_string(index=False))
    out.round(6).to_csv("data/coral_trend_check.csv", index=False)
    print("wrote data/coral_trend_check.csv")
