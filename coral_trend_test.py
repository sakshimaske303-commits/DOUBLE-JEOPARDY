"""
DOUBLE JEOPARDY - Coral Thermal Stress Trend Test (Mann-Kendall + OLS)
==========================================================================
Your paper currently reports coral thermal-stress trend as a difference
between two period averages (1996-2000 vs 2016-2020). This script adds a
proper trend test over the FULL 24-year continuous DHW time series per
island, as a robustness check — this is the standard method for testing
trends in environmental time series, and it directly answers the "why not
just fit a trend instead of comparing two windows?" question a reviewer
could raise.

Runs two tests per island:
  1. Mann-Kendall trend test (non-parametric — doesn't assume the data is
     normally distributed, which is standard practice for climate/ecological
     time series) -> reports trend direction, p-value, and Sen's slope
     (an estimate of the trend's magnitude, in degree-heating-weeks/year).
  2. A simple OLS linear regression slope + p-value, as a second,
     more familiar reference point.

HOW TO USE:
1. pip install pymannkendall pandas scipy
2. Run: python coral_trend_test.py
3. Send me the printed table — I'll give you the exact sentence to add to
   the paper.
"""

import pandas as pd
import numpy as np
from scipy import stats

try:
    import pymannkendall as mk
except ImportError:
    raise SystemExit(
        "Missing package. Run this first:\n    pip install pymannkendall\n"
        "then re-run this script."
    )

ISLANDS = {
    "Maldives": "data/coral_bleaching/maldives_dhw_timeseries.csv",
    "Seychelles": "data/coral_bleaching/seychelles_dhw_timeseries.csv",
    "Fiji": "data/coral_bleaching/fiji_dhw_timeseries.csv",
    "Lakshadweep": "data/coral_bleaching/lakshadweep_dhw_timeseries.csv",
    "Canary Islands": "data/coral_bleaching/canary_dhw_timeseries.csv",
}


def run_trend_test(csv_path):
    df = pd.read_csv(csv_path, skiprows=[1])  # skip the units row
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").dropna(subset=["degree_heating_week"])

    values = df["degree_heating_week"].to_numpy()

    # Mann-Kendall trend test (non-parametric, standard for climate time series)
    mk_result = mk.original_test(values)

    # Simple OLS regression on time (in years since first observation) as a
    # more familiar secondary reference point
    years_since_start = (df["time"] - df["time"].iloc[0]).dt.days / 365.25
    slope, intercept, r_value, p_value, std_err = stats.linregress(years_since_start, values)

    return {
        "n_obs": len(values),
        "mk_trend": mk_result.trend,          # 'increasing', 'decreasing', or 'no trend'
        "mk_p": mk_result.p,
        "sens_slope_per_year": mk_result.slope,
        "ols_slope_per_year": slope,
        "ols_p": p_value,
    }


if __name__ == "__main__":
    print(f"{'Island':<16} {'N':>4} {'MK trend':>12} {'MK p-value':>11} "
          f"{'Sen slope/yr':>13} {'OLS slope/yr':>13} {'OLS p-value':>12}")
    print("-" * 90)
    for island, path in ISLANDS.items():
        try:
            r = run_trend_test(path)
            print(f"{island:<16} {r['n_obs']:>4} {r['mk_trend']:>12} {r['mk_p']:>11.4f} "
                  f"{r['sens_slope_per_year']:>13.4f} {r['ols_slope_per_year']:>13.4f} "
                  f"{r['ols_p']:>12.4f}")
        except Exception as e:
            print(f"{island:<16}  ERROR: {e}")
