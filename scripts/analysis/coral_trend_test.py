"""Coral Degree Heating Week (DHW) trend tests, per island."""
import numpy as np
import pandas as pd
from scipy.stats import norm

try:
    import pymannkendall as mk
except ImportError:
    raise SystemExit("Missing package. Run:  pip install pymannkendall")

ISLANDS = ["maldives", "seychelles", "fiji", "lakshadweep", "canary"]
PRIMARY_SERIES = "reef_cells"
SOURCES = {
    "single_cell": ("data/coral_bleaching/{}_dhw_timeseries.csv", "degree_heating_week", [1]),
    "box_average": ("data/coral_bleaching_v2/{}_dhw_timeseries_areaavg.csv", "dhw_mean", None),
    # written by scripts/acquisition/download_dhw_reef_cells.py (mean over reef cells only)
    "reef_cells": ("data/coral_bleaching_v3/{}_dhw_reefcells_mean.csv", "dhw_mean", None),
}


def _s_and_var(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    s = sum(np.sign(x[k + 1:] - x[k]).sum() for k in range(n - 1))
    _, c = np.unique(x, return_counts=True)
    var = (n * (n - 1) * (2 * n + 5) - np.sum(c * (c - 1) * (2 * c + 5))) / 18
    return s, var


def seasonal_mk_calendar(df, col):
    S = V = 0.0
    for _, g in df.groupby(df["time"].dt.month):
        s, v = _s_and_var(g.sort_values("time")[col].to_numpy())
        S += s
        V += v
    z = (S - np.sign(S)) / np.sqrt(V) if S != 0 else 0.0
    return S, 2 * (1 - norm.cdf(abs(z)))


def monthly_series(df, col):
    """Calendar-month means, Jan 1996 - Dec 2020; short gaps (<= 2 months) interpolated."""
    t = pd.to_datetime(df["time"], utc=True).dt.tz_convert(None)  # NOAA times are UTC
    m = pd.Series(df[col].to_numpy(), index=t).resample("MS").mean()
    full = pd.date_range("1996-01-01", "2020-12-01", freq="MS")
    m = m.reindex(full).interpolate(limit=2, limit_area="inside")
    return m


def run(island, source):
    pattern, col, skip = SOURCES[source]
    df = pd.read_csv(pattern.format(island), skiprows=skip)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    values = df[col].to_numpy()

    smk_index = mk.seasonal_test(values, period=12)
    _, p_cal = seasonal_mk_calendar(df.dropna(subset=[col]), col)
    annual_max = df.groupby(df["time"].dt.year)[col].max()
    amk = mk.original_test(annual_max.to_numpy())
    y = df["time"].dt.year
    change = df.loc[y.between(2016, 2020), col].mean() - df.loc[y.between(1996, 2000), col].mean()
    weeks_ge4 = int((df[col] >= 4).sum())
    monthly = monthly_series(df, col)
    n_missing_months = int(monthly.isna().sum())
    mvals = monthly.to_numpy()
    csmk = mk.correlated_seasonal_test(mvals, period=12)
    msmk = mk.seasonal_test(mvals, period=12)

    return {"island": island, "series": source, "n_obs": int(np.isfinite(values).sum()),
            "first": df["time"].min().date(), "last": df["time"].max().date(),
            "smk_index_trend": smk_index.trend, "smk_index_p": smk_index.p,
            "smk_index_sen_per_step": smk_index.slope, "smk_calendar_p": p_cal,
            "annual_max_trend": amk.trend, "annual_max_p": amk.p, "annual_max_sen_per_year": amk.slope,
            "period_change_2016_20_vs_1996_2000": change, "max_dhw": float(np.nanmax(values)),
            "samples_ge_4_degC_weeks": weeks_ge4,
            "csmk_trend": csmk.trend, "csmk_p": csmk.p, "csmk_sen_per_year": csmk.slope,
            "monthly_smk_p": msmk.p, "months_missing": n_missing_months,
            "primary": source == PRIMARY_SERIES}


if __name__ == "__main__":
    rows = []
    for source in SOURCES:
        for island in ISLANDS:
            try:
                rows.append(run(island, source))
            except FileNotFoundError as e:
                print(f"{island} [{source}]: SKIPPED ({e})")
    out = pd.DataFrame(rows)
    pd.set_option("display.width", 200)
    print(out[["island", "series", "n_obs", "csmk_p", "monthly_smk_p", "smk_calendar_p", "smk_index_p",
               "annual_max_p", "period_change_2016_20_vs_1996_2000", "max_dhw", "months_missing"]]
          .round(4).to_string(index=False))
    print(f"\nMain test: correlated seasonal Mann-Kendall (csmk_p) on the '{PRIMARY_SERIES}' series.")
    out.to_csv("data/coral_trend_results.csv", index=False)
    print("\nSaved: data/coral_trend_results.csv")
