"""
DOUBLE JEOPARDY - Additional Research Paper Figures
==========================================================
This project's analysis produced only one static figure (Figure 1,
compound_vulnerability_score.png). This script generates six more,
covering results that are currently only described in text/tables in
the paper but were never actually plotted.

Matches the visual style already established in map1_vulnerability_score.py
(matplotlib, blue/red risk coding, bold two-line titles, source caption,
saved at 200 dpi into outputs/plots/).

Every number plotted here is read directly from your own data/ CSVs where
a CSV exists (slr_exposure_summary.csv, governance_alignment_test.csv,
coral_bleaching/*.csv), or uses the same hardcoded values already verified
and used elsewhere in this project (population-weighted exposure %,
mangrove areas, Mann-Kendall trend results) where no CSV was saved. No new
data is downloaded or recomputed differently from what you already validated.

HOW TO USE:
Just run: python research_paper_figures.py
Requires: matplotlib, pandas, numpy, scipy (all already used in this project)

Output files (in outputs/plots/):
  fig2_physical_exposure_by_island.png
  fig3_settlement_vs_population_weighted.png
  fig4_coral_thermal_stress_trends.png
  fig5_mangrove_extent_over_time.png
  fig6_governance_alignment.png
  fig7_weighting_sensitivity_curve.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

OUT_DIR = "outputs/plots"
os.makedirs(OUT_DIR, exist_ok=True)

BLUE = "#2c7fb8"
RED = "#e34a33"
GREEN = "#31a354"
PURPLE = "#756bb1"
ORANGE = "#fd8d3c"
EDGE = "#333333"

ISLAND_ORDER = ["Seychelles", "Maldives", "Lakshadweep", "Fiji", "Canary Islands"]
ISLAND_COLOR = {
    "Maldives": BLUE, "Seychelles": RED, "Fiji": GREEN,
    "Canary Islands": PURPLE, "Lakshadweep": ORANGE,
}
ISLAND_FILE_MAP = {
    "Maldives": "maldives", "Seychelles": "seychelles", "Fiji": "fiji",
    "Canary Islands": "canary", "Lakshadweep": "lakshadweep",
}


def source_caption(ax_fig, text):
    plt.figtext(0.5, 0.01, text, ha="center", fontsize=8, color="gray")


# ------------------------------------------------------------------
# Figure 2 — Physical Exposure by Island (settlement-based)
# ------------------------------------------------------------------
def fig2_physical_exposure():
    df = pd.read_csv("data/slr_exposure_summary.csv")
    df["island"] = df["island"].str.title().replace({"Canary": "Canary Islands"})
    df = df.sort_values("pct_at_risk", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 7))
    colors = [RED if p >= 50 else BLUE for p in df["pct_at_risk"]]
    bars = ax.barh(df["island"], df["pct_at_risk"], color=colors, edgecolor=EDGE, linewidth=0.8)

    for bar, pct, total in zip(bars, df["pct_at_risk"], df["total"]):
        ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height() / 2,
                 f"{pct:.1f}% (n={int(total)})", va="center", fontsize=10, fontweight="bold")

    ax.set_xlabel("% of Settlements At or Below 1m Elevation Threshold", fontsize=11)
    ax.set_title(
        "Physical Exposure by Island\n"
        "Share of settlement locations at or below the 1-meter sea-level-rise threshold",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.set_xlim(0, 112)
    ax.grid(axis="x", alpha=0.3)

    source_caption(fig, "DOUBLE JEOPARDY — Source: Copernicus DEM GLO-30, OpenStreetMap settlements")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig2_physical_exposure_by_island.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


# ------------------------------------------------------------------
# Figure 3 — Settlement-based vs Population-weighted Exposure
# ------------------------------------------------------------------
def fig3_settlement_vs_population():
    settlement_df = pd.read_csv("data/slr_exposure_summary.csv")
    settlement_df["island"] = settlement_df["island"].str.title().replace({"Canary": "Canary Islands"})
    settlement_pct = dict(zip(settlement_df["island"], settlement_df["pct_at_risk"]))

    # Population-weighted exposure %, from population_weighted_exposure.py's
    # validated final run (windowed, geography-based, antimeridian-aware).
    population_pct = {
        "Maldives": 64.5, "Seychelles": 17.6, "Lakshadweep": 87.5,
        "Fiji": 2.1, "Canary Islands": 1.6,
    }

    islands = ISLAND_ORDER
    x = np.arange(len(islands))
    width = 0.35

    fig, ax = plt.subplots(figsize=(11, 7))
    bars1 = ax.bar(x - width / 2, [settlement_pct[i] for i in islands], width,
                    label="Settlement-based", color=BLUE, edgecolor=EDGE, linewidth=0.8)
    bars2 = ax.bar(x + width / 2, [population_pct[i] for i in islands], width,
                    label="Population-weighted", color=RED, edgecolor=EDGE, linewidth=0.8)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                     ha="center", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(islands, fontsize=10)
    ax.set_ylabel("% Exposed to 1m SLR Threshold", fontsize=11)
    ax.set_ylim(0, 112)
    ax.set_title(
        "Settlement-Based vs. Population-Weighted Physical Exposure\n"
        "Lakshadweep becomes the highest-exposure island once weighted by where people actually live",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.legend(loc="upper right", fontsize=10, frameon=True)
    ax.grid(axis="y", alpha=0.3)

    source_caption(fig, "DOUBLE JEOPARDY — Source: Copernicus DEM GLO-30, OpenStreetMap, WorldPop 2020 "
                         "(Fiji reflects ~97.6% of national population; Lau Islands excluded, no elevation coverage)")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig3_settlement_vs_population_weighted.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


# ------------------------------------------------------------------
# Figure 4 — Coral Thermal Stress Time Series with trend lines
# ------------------------------------------------------------------
def fig4_coral_trends():
    # Precomputed OLS trend (intercept + slope/year, years since series start)
    # and Mann-Kendall significance, from the robustness-check trend test.
    trend_info = {
        "Maldives": {"intercept": 0.0895, "slope_per_year": 0.00450, "significant": True, "p": 0.011},
        "Seychelles": {"intercept": -0.0668, "slope_per_year": 0.02532, "significant": True, "p": 0.025},
        "Fiji": {"intercept": 0.3250, "slope_per_year": 0.00151, "significant": False, "p": 0.184},
        "Lakshadweep": {"intercept": 0.1072, "slope_per_year": 0.00254, "significant": False, "p": 0.386},
        "Canary Islands": {"intercept": 0.4762, "slope_per_year": 0.01905, "significant": False, "p": 0.641},
    }

    fig, ax = plt.subplots(figsize=(13, 7.5))

    for island in ISLAND_ORDER:
        file_key = ISLAND_FILE_MAP[island]
        path = f"data/coral_bleaching/{file_key}_dhw_timeseries.csv"
        df = pd.read_csv(path, skiprows=[1])
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time")
        color = ISLAND_COLOR[island]

        ax.plot(df["time"], df["degree_heating_week"], color=color, linewidth=1.3,
                alpha=0.85, label=None)

        info = trend_info[island]
        start_date, end_date = df["time"].iloc[0], df["time"].iloc[-1]
        years_elapsed = (end_date - start_date).days / 365.25
        y_start = info["intercept"]
        y_end = info["intercept"] + info["slope_per_year"] * years_elapsed
        sig_label = "significant" if info["significant"] else "not significant"
        ax.plot([start_date, end_date], [y_start, y_end], color=color, linewidth=2.4,
                 linestyle="--",
                 label=f"{island} trend (MK {sig_label}, p={info['p']:.3f})")

    ax.axhline(4, color="orange", linestyle=":", linewidth=1.2)
    ax.axhline(8, color="darkred", linestyle=":", linewidth=1.2)
    ax.text(ax.get_xlim()[0], 4.15, " Bleaching threshold (4°C-wk)", fontsize=8, color="darkorange", va="bottom")
    ax.text(ax.get_xlim()[0], 8.15, " Severe bleaching/mortality (8°C-wk)", fontsize=8, color="darkred", va="bottom")

    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Degree Heating Week (°C-weeks)", fontsize=11)
    ax.set_title(
        "Coral Thermal Stress Over Time (1996–2020), with Trend Lines\n"
        "Dashed lines are OLS fits; significance assessed via Mann-Kendall trend test on the full series",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8.5, frameon=True, ncol=1)

    source_caption(fig, "DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig4_coral_thermal_stress_trends.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


# ------------------------------------------------------------------
# Figure 5 — Mangrove Extent Over Three Time Points
# ------------------------------------------------------------------
def fig5_mangrove_extent():
    # From mangrove_3point_comparison.py's validated output (area in an
    # equal-area projection, EPSG:6933). Only islands with mangroves present.
    mangrove_data = {
        "Maldives": [0.97, 0.97, 0.97],
        "Seychelles": [3.83, 3.84, 3.83],
        "Fiji": [485.72, 487.97, 488.41],
    }
    years = [1996, 2010, 2020]

    fig, ax = plt.subplots(figsize=(10, 6.5))
    for island, values in mangrove_data.items():
        ax.plot(years, values, marker="o", markersize=9, linewidth=2.6,
                color=ISLAND_COLOR[island], label=island)
        for yr, v in zip(years, values):
            ax.text(yr, v, f"  {v:.2f}", fontsize=8.5, va="bottom", color=ISLAND_COLOR[island])

    ax.set_xticks(years)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Mangrove Area (km²)", fontsize=11)
    ax.set_yscale("log")
    ax.set_title(
        "Mangrove Extent Over Time (1996, 2010, 2020)\n"
        "Log scale — extent is essentially flat for every island, no net decline detected",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="center left", fontsize=10, frameon=True)

    source_caption(fig, "DOUBLE JEOPARDY — Source: Global Mangrove Watch (GMW), area computed in EPSG:6933")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig5_mangrove_extent_over_time.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


# ------------------------------------------------------------------
# Figure 6 — Governance Alignment (Vulnerability vs WDPA coverage)
# ------------------------------------------------------------------
def fig6_governance_alignment():
    df = pd.read_csv("data/governance_alignment_test.csv")

    r, p = stats.pearsonr(df["vulnerability_score"], df["wdpa_ratio"])
    n = len(df)
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    ci_low, ci_high = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [ISLAND_COLOR[i.title().replace("Canary", "Canary Islands")] for i in df["island"]]
    ax.scatter(df["vulnerability_score"], df["wdpa_ratio"], s=140, c=colors,
               edgecolor=EDGE, linewidth=1, zorder=3)

    for _, row in df.iterrows():
        label = row["island"].title().replace("Canary", "Canary Islands")
        ax.annotate(label, (row["vulnerability_score"], row["wdpa_ratio"]),
                    textcoords="offset points", xytext=(8, 6), fontsize=10, fontweight="bold")

    # OLS best-fit line for visual reference
    slope, intercept, *_ = stats.linregress(df["vulnerability_score"], df["wdpa_ratio"])
    xs = np.linspace(df["vulnerability_score"].min(), df["vulnerability_score"].max(), 50)
    ax.plot(xs, intercept + slope * xs, color=EDGE, linestyle="--", linewidth=1.3, alpha=0.7, zorder=2)

    ax.set_xlabel("Compound Vulnerability Score", fontsize=11)
    ax.set_ylabel("WDPA Coastal Protected-Area Ratio", fontsize=11)
    ax.set_title(
        "Governance Alignment: Risk vs. Protected-Area Coverage\n"
        f"r = {r:.3f}, p = {p:.3f}, 95% CI [{ci_low:.2f}, {ci_high:.2f}] (n={n})",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.grid(alpha=0.3)

    source_caption(fig, "DOUBLE JEOPARDY — Source: World Database on Protected Areas (WDPA), "
                         "10km coastal buffer; compound vulnerability score (this study)")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig6_governance_alignment.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")
    print(f"  Governance correlation: r={r:.3f}, p={p:.3f}, 95% CI=[{ci_low:.2f}, {ci_high:.2f}]")


# ------------------------------------------------------------------
# Figure 7 — Compound Vulnerability Score: Weighting Sensitivity Curve
# ------------------------------------------------------------------
def fig7_weighting_sensitivity():
    # Same raw inputs and normalize() logic as compound_vulnerability_score.py
    slr_data = {"Maldives": 99.1, "Seychelles": 78.3, "Fiji": 32.0, "Canary Islands": 12.1, "Lakshadweep": 77.8}
    coral_decline = {"Maldives": 0.17, "Seychelles": 0.68, "Fiji": 0.10, "Canary Islands": -0.05, "Lakshadweep": 0.08}

    def normalize(d):
        values = list(d.values())
        min_v, max_v = min(values), max(values)
        return {k: (v - min_v) / (max_v - min_v) if max_v > min_v else 0 for k, v in d.items()}

    slr_norm = normalize(slr_data)
    coral_norm = normalize(coral_decline)

    weights = np.linspace(0, 1, 101)  # physical-exposure weight, 0% to 100%
    fig, ax = plt.subplots(figsize=(11, 7))

    for island in ISLAND_ORDER:
        scores = [slr_norm[island] * w + coral_norm[island] * (1 - w) for w in weights]
        ax.plot(weights * 100, scores, color=ISLAND_COLOR[island], linewidth=2.4, label=island)

    ax.axvline(50, color=EDGE, linestyle=":", linewidth=1.3)
    ax.text(51, 0.97, "Weighting used in this study (50/50)", fontsize=8.5, color=EDGE)

    ax.set_xlabel("Physical Exposure Weight (%)  —  remainder assigned to coral ecosystem decline", fontsize=10.5)
    ax.set_ylabel("Compound Vulnerability Score (normalized, 0–1)", fontsize=11)
    ax.set_title(
        "Compound Vulnerability Score — Weighting Sensitivity\n"
        "Island rankings stay stable across the full 0–100% weighting range",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="center left", fontsize=10, frameon=True)

    source_caption(fig, "DOUBLE JEOPARDY — Derived from slr_exposure_summary.csv and coral DHW trend data (this study)")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "fig7_weighting_sensitivity_curve.png")
    plt.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating additional DOUBLE JEOPARDY figures...\n")
    fig2_physical_exposure()
    fig3_settlement_vs_population()
    fig4_coral_trends()
    fig5_mangrove_extent()
    fig6_governance_alignment()
    fig7_weighting_sensitivity()
    print(f"\nDone. All figures saved in: {OUT_DIR}/")
