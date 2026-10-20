"""Governance alignment: does coastal protected-area coverage track the
Compound Vulnerability Score?

Rewritten 2026-10-10 after the Forensic Review. Inputs are read from pipeline
outputs (no hand-typed scores). With n = 4 islands this is DESCRIPTIVE, not a
hypothesis test that can "support" anything: one island (Seychelles) carries
most of the correlation. The script therefore reports, for each coverage
metric, Pearson r with a Fisher-z 95% CI, Spearman rho, and the leave-one-out
Pearson r for every island, so the fragility is visible.

Coverage metrics (from scripts/processing/wdpa_coastal_buffer.py):
  pct_coastal_zone_protected  share of the 10 km coastal zone that is protected
                              (dissolved polygons) -- the recommended metric
  ratio                       protected km2 in the zone / land km2 (older metric;
                              mostly reflects island size and fragmentation)

Islands with no WDPA data (wdpa_available False, currently Lakshadweep) are
excluded from the correlation and listed separately; they are never set to 0.
"""
import numpy as np
import pandas as pd
from scipy import stats

cvs = pd.read_csv("data/compound_vulnerability_scores.csv").set_index("island")["compound_vulnerability_score"]
wdpa = pd.read_csv("data/wdpa_coastal_normalized.csv").set_index("island")
if "wdpa_available" not in wdpa.columns:  # older file format
    wdpa["wdpa_available"] = wdpa.index != "lakshadweep"

metrics = [m for m in ["pct_coastal_zone_protected", "ratio"] if m in wdpa.columns]
df = wdpa[metrics + ["wdpa_available"]].join(cvs.rename("vulnerability_score"), how="inner")
df["excluded_from_correlation"] = ~df["wdpa_available"].astype(bool)
corr = df[~df["excluded_from_correlation"]]
n = len(corr)

print(df.round(3).to_string())
print(f"\nn = {n} (excluded, no WDPA data: {', '.join(df.index[df['excluded_from_correlation']]) or 'none'})\n")

summary = []
for m in metrics:
    x, y = corr["vulnerability_score"], corr[m]
    r, p = stats.pearsonr(x, y)
    rho, p_rho = stats.spearmanr(x, y)
    if n > 3:
        z, se = np.arctanh(np.clip(r, -0.999999, 0.999999)), 1 / np.sqrt(n - 3)
        lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    else:
        lo = hi = np.nan
    loo = {}
    for drop in corr.index:
        sub = corr.drop(drop)
        loo[drop] = stats.pearsonr(sub["vulnerability_score"], sub[m])[0] if len(sub) >= 3 else np.nan
    print(f"[{m}] Pearson r = {r:.3f} (p = {p:.3f}, 95% CI {lo:.2f} to {hi:.2f}); "
          f"Spearman rho = {rho:.2f} (p = {p_rho:.2f})")
    print("   leave-one-out r: " + ", ".join(f"without {k}: {v:.2f}" for k, v in loo.items()))
    summary.append({"metric": m, "n": n, "pearson_r": r, "pearson_p": p, "ci_low": lo, "ci_high": hi,
                    "spearman_rho": rho, "spearman_p": p_rho,
                    **{f"loo_r_without_{k}": v for k, v in loo.items()}})

out = df.reset_index().rename(columns={"index": "island"})
# keep the column the figure script expects
out["wdpa_ratio"] = out["pct_coastal_zone_protected"] if "pct_coastal_zone_protected" in out else out["ratio"]
out.to_csv("data/governance_alignment_test.csv", index=False)
pd.DataFrame(summary).to_csv("data/governance_alignment_summary.csv", index=False)
print("\nSaved: data/governance_alignment_test.csv, data/governance_alignment_summary.csv")
print("Reminder: with n = 4, report these as descriptive associations, not as evidence that "
      "protection responds to risk.")
