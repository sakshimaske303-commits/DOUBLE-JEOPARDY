import pandas as pd
from scipy import stats

vulnerability = {
    "seychelles": 0.880,
    "maldives": 0.651,
    "lakshadweep": 0.467,
    "fiji": 0.217,
    "canary": 0.000,
}

wdpa_df = pd.read_csv("data/wdpa_coastal_normalized.csv").set_index("island")

results = []
for island, vuln_score in vulnerability.items():
    wdpa_ratio = wdpa_df.loc[island, "ratio"]
    results.append({"island": island, "vulnerability_score": vuln_score, "wdpa_ratio": wdpa_ratio})
    print(f"{island.upper()}: Vulnerability={vuln_score:.3f}, WDPA-ratio={wdpa_ratio:.2f}")

df = pd.DataFrame(results)

correlation, p_value = stats.pearsonr(df["vulnerability_score"], df["wdpa_ratio"])
print(f"\nCorrelation (Vulnerability vs WDPA-coverage): r={correlation:.3f}, p={p_value:.3f}")

if correlation > 0.3:
    interpretation = "Higher-risk islands tend to have MORE protection (risk-responsive governance)"
elif correlation < -0.3:
    interpretation = "Higher-risk islands tend to have LESS protection (governance-evidence gap)"
else:
    interpretation = "No clear relationship between risk and protection level (protection appears independent of verified risk)"

print(f"Interpretation: {interpretation}")

df.to_csv("data/governance_alignment_test.csv", index=False)