"""Coral Degree Heating Week (DHW) trend tests, per island.

Updated 2026-10-10 after the Forensic Review. For each island and for both the
single-cell series (data/coral_bleaching) and the +-0.15 deg box average
(data/coral_bleaching_v2) this reports:

  smk_index_p     seasonal Mann-Kendall as used so far: pymannkendall
                  seasonal_test(period=12) on the sample index. NOTE: samples
                  are every 30 days (12 x 30 = 360 days), so these "seasons"
                  drift ~5 days a year (~4 months over 1996-2020). They are not
                  calendar months.
  smk_calendar_p  seasonal Mann-Kendall with TRUE calendar-month seasons
                  (Hirsch et al. 1982: S and Var(S) summed over months).
                  This is what the paper's wording describes.
  annual_max_p    Mann-Kendall on each year's MAXIMUM DHW, the metric used in
                  bleaching-risk work. Sen's slope reported per year.
  period_change   mean DHW 2016-2020 minus mean DHW 1996-2000 (the value used
                  in the compound score).

Update 2026-10-11 (FINISH_PLAN D3):
  csmk_p          correlated seasonal Mann-Kendall (Hirsch and Slack 1984,
                  pymannkendall.correlated_seasonal_test) on CALENDAR-MONTH
                  means (Jan 1996 ... Dec 2020, 300 months). DHW is a 12-week
                  running sum, so neighbouring months are strongly correlated;
                  the ordinary seasonal test treats them as independent and
                  gives p-values that are too small. This is the MAIN test.
  monthly_smk_p   ordinary seasonal test on the same monthly matrix, to show
                  how much the correction changes.
  primary         True for the series reported in the paper: the mean over
                  every 5 km cell of mapped reef ("reef_cells"). The single
                  cell and the +-0.15 deg box are sensitivity checks.

Results are written to data/coral_trend_results.csv so figures and the paper
can read them instead of hard-coding p-values.
Needs pandas, numpy, scipy, pymannkendall.
"""
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
