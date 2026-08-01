"""
Coral thermal stress trend test — Mann-Kendall + OLS

The paper originally compared just two period averages (1996-2000 vs
2016-2020) for the coral DHW trend. Adding a proper trend test over the
full 24-year series here as a robustness check, since a two-window
comparison alone doesn't really hold up to "why not just fit a trend
line" scrutiny.

Runs two tests per island:
  1. Mann-Kendall (non-parametric, standard for climate/ecological time
     series) -> trend direction, p-value, Sen's slope (DHW/year)
  2. OLS linear regression slope + p-value as a simpler reference point

Run: python coral_trend_test.py
Needs: pymannkendall, pandas, scipy
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
