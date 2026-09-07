import pandas as pd
from scipy import stats

vulnerability = {
    "seychelles": 0.895,
    "maldives": 0.651,
    "lakshadweep": 0.481,
    "fiji": 0.106,
    "canary": 0.000,
}

# Lakshadweep's WDPA figure in data/wdpa_coastal_normalized.csv is a 0.0
# missing-data placeholder (no protected-area layer was available to clip),
# not a measured zero -- see wdpa_coastal_buffer.py. Feeding a fabricated
# zero into an already-tiny n=5 Pearson correlation biases it rather than
# just "being conservative", so it's excluded from the correlation itself
# (n=4) and reported separately below instead.
EXCLUDED_NO_DATA = {"lakshadweep"}

wdpa_df = pd.read_csv("data/wdpa_coastal_normalized.csv").set_index("island")

results = []
for island, vuln_score in vulnerability.items():
    wdpa_ratio = wdpa_df.loc[island, "ratio"]
    results.append({"island": island, "vulnerability_score": vuln_score, "wdpa_ratio": wdpa_ratio,
                     "excluded_from_correlation": island in EXCLUDED_NO_DATA})
    flag = "  [excluded from correlation: no WDPA data]" if island in EXCLUDED_NO_DATA else ""
    print(f"{island.upper()}: Vulnerability={vuln_score:.3f}, WDPA-ratio={wdpa_ratio:.2f}{flag}")

df = pd.DataFrame(results)
corr_df = df[~df["excluded_from_correlation"]]

correlation, p_value = stats.pearsonr(corr_df["vulnerability_score"], corr_df["wdpa_ratio"])
print(f"\nCorrelation (Vulnerability vs WDPA-coverage), n={len(corr_df)} "
      f"(Lakshadweep excluded, no WDPA data): r={correlation:.3f}, p={p_value:.3f}")

if correlation > 0.3:
    interpretation = "Higher-risk islands tend to have MORE protection (risk-responsive governance)"
elif correlation < -0.3:
    interpretation = "Higher-risk islands tend to have LESS protection (governance-evidence gap)"
else:
    interpretation = "No clear relationship between risk and protection level (protection appears independent of verified risk)"

print(f"Interpretation: {interpretation}")

df.to_csv("data/governance_alignment_test.csv", index=False)