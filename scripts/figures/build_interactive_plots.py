"""Interactive Plotly versions of the headline DOUBLE JEOPARDY charts. Same underlying
data as the static figures (map1_vulnerability_score.py, research_paper_figures.py
fig4/fig7) - just Plotly instead of matplotlib.
"""

import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go

OUT = "outputs/plots/interactive"
os.makedirs(OUT, exist_ok=True)

ISLAND_ORDER = ["Seychelles", "Maldives", "Lakshadweep", "Fiji", "Canary Islands"]
ISLAND_COLOR = {
    "Maldives": "#2c7fb8", "Seychelles": "#e34a33", "Fiji": "#31a354",
    "Canary Islands": "#756bb1", "Lakshadweep": "#fd8d3c",
}
ISLAND_FILE_MAP = {
    "Maldives": "maldives", "Seychelles": "seychelles", "Fiji": "fiji",
    "Canary Islands": "canary", "Lakshadweep": "lakshadweep",
}

DARK_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Inter, sans-serif", color="#1b2a3a"),
    margin=dict(t=90, b=60, l=140, r=40),
)


# ============================================================
# 1. COMPOUND VULNERABILITY SCORE — headline ranking chart
# ============================================================
def build_compound_vulnerability_score():
    raw = pd.read_csv("data/compound_vulnerability_scores.csv")
    label = {v: k for k, v in ISLAND_FILE_MAP.items()}
    df = pd.DataFrame({"island": raw["island"].map(label), "score": raw["compound_vulnerability_score"]})
    df = df.sort_values("score", ascending=True)
    colors = ["#2c7fb8"] * len(df)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["score"], y=df["island"], orientation="h", marker_color=colors,
        marker_line=dict(color="#333333", width=1),
        text=[f"{s:.3f}" for s in df["score"]], textposition="outside",
        hovertemplate="%{y}<br>Score: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title="Compound Vulnerability Score by Island<br><sub>Share of people at or below 1 m + change in reef heat stress over mapped reef (1996–2000 vs 2016–2020); Canary Islands: no mapped reef</sub>",
        xaxis_title="Compound Vulnerability Score (0 = lowest, 1 = highest)",
        xaxis=dict(range=[0, 1.05]),
        height=480, **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/compound_vulnerability_score.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/compound_vulnerability_score.html")


# ============================================================
# 2. CORAL THERMAL STRESS TRENDS — time series, toggleable per island
# ============================================================
def build_coral_thermal_stress_trends():
    """Reef-cell mean series (main series, Development Log Entry 16); the Canary Islands
    have no mapped reef and show their single offshore cell. The old OLS lines
    are gone (a straight line through a zero-inflated series misleads); instead
    each island shows its 1996-2000 and 2016-2020 means, and the legend gives the
    correlated seasonal Mann-Kendall p from data/coral_trend_results.csv."""
    res = pd.read_csv("data/coral_trend_results.csv")
    fig = go.Figure()
    for island in ISLAND_ORDER:
        key = ISLAND_FILE_MAP[island]
        v3 = f"data/coral_bleaching_v3/{key}_dhw_reefcells_mean.csv"
        if os.path.exists(v3):
            df, col, series = pd.read_csv(v3), "dhw_mean", "reef_cells"
        else:
            df, col, series = (pd.read_csv(f"data/coral_bleaching/{key}_dhw_timeseries.csv", skiprows=[1]),
                               "degree_heating_week", "single_cell")
        df["time"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert(None)
        df = df.sort_values("time")
        r = res[(res["island"] == key) & (res["series"] == series)]
        pcol = "csmk_p" if "csmk_p" in res.columns else "smk_calendar_p"
        p = float(r[pcol].iloc[0]) if len(r) else float("nan")
        where = "mapped-reef cells" if series == "reef_cells" else "one offshore cell, no mapped reef"
        color = ISLAND_COLOR[island]
        fig.add_trace(go.Scatter(
            x=df["time"], y=df[col], mode="lines", name=f"{island} ({where}; trend p={p:.2f})",
            line=dict(color=color, width=1.3), opacity=0.8, legendgroup=island,
            hovertemplate=f"{island}<br>%{{x|%Y-%m}}<br>DHW: %{{y:.2f}}°C-wk<extra></extra>",
        ))
        y = df["time"].dt.year
        for y0, y1 in ((1996, 2000), (2016, 2020)):
            m = df.loc[y.between(y0, y1), col].mean()
            fig.add_trace(go.Scatter(
                x=[pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y1}-12-31")], y=[m, m], mode="lines",
                line=dict(color=color, width=3), legendgroup=island, showlegend=False,
                hovertemplate=f"{island}: mean {y0}–{y1} = {m:.2f}°C-wk<extra></extra>",
            ))
    fig.add_hline(y=4, line_color="orange", line_dash="dot", annotation_text="Bleaching likely (4°C-wk)", annotation_font_color="orange")
    fig.add_hline(y=8, line_color="darkred", line_dash="dot", annotation_text="Severe (8°C-wk)", annotation_font_color="darkred")
    fig.update_layout(
        title="Coral Thermal Stress, 1996–2020<br>"
              "<sub>Thick segments: mean of 1996–2000 and of 2016–2020. Trend p: correlated seasonal Mann-Kendall "
              "on calendar-month means (corrects for serial correlation)</sub>",
        xaxis_title="Date", yaxis_title="Degree Heating Week (°C-weeks)",
        height=600, hovermode="closest", **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/coral_thermal_stress_trends.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/coral_thermal_stress_trends.html")


# ============================================================
# 3. WEIGHTING SENSITIVITY CURVE
# ============================================================
def build_weighting_sensitivity():
    cvs = pd.read_csv("data/compound_vulnerability_scores.csv").set_index("island")
    # scaled inputs straight from compound_vulnerability_score.py (same Canary rule)
    slr_norm = {lab: cvs.loc[key, "slr_norm"] for lab, key in ISLAND_FILE_MAP.items()}
    coral_norm = {lab: cvs.loc[key, "coral_norm"] for lab, key in ISLAND_FILE_MAP.items()}
    weights = np.linspace(0, 1, 101)

    fig = go.Figure()
    for island in ISLAND_ORDER:
        scores = [slr_norm[island] * w + coral_norm[island] * (1 - w) for w in weights]
        fig.add_trace(go.Scatter(
            x=weights * 100, y=scores, mode="lines", name=island,
            line=dict(color=ISLAND_COLOR[island], width=2.4),
            hovertemplate=f"{island}<br>Weight: %{{x:.0f}}%<br>Score: %{{y:.3f}}<extra></extra>",
        ))

    fig.add_vline(x=50, line_dash="dot", line_color="#333333", annotation_text="Weighting used in this study (50/50)")
    fig.update_layout(
        title="Compound Vulnerability Score — Weighting Sensitivity<br>"
              "<sub>Score of each island as the exposure weight goes from 0% to 100%</sub>",
        xaxis_title="Exposure weight (%), share of people at or below 1 m — remainder: change in reef heat stress",
        yaxis_title="Compound Vulnerability Score (normalized, 0-1)",
        xaxis=dict(range=[0, 100]), yaxis=dict(range=[-0.05, 1.05]),
        height=560, **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/weighting_sensitivity_curve.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/weighting_sensitivity_curve.html")


# ============================================================
# 4. COASTAL SETBACK COVERAGE CURVE
# ============================================================
SETBACKS = {"Canary Islands": [100, 20], "Seychelles": [25], "Lakshadweep": [20]}


def build_setback_coverage():
    path = "data/setback_coverage_curve.csv"
    if not os.path.exists(path):
        print("Skipped setback coverage: run scripts/analysis/setback_calibration.py first")
        return
    cur = pd.read_csv(path)
    summ = pd.read_csv("data/setback_calibration_summary.csv")
    summ = summ[summ["variant"] == "all"].set_index("island")
    fig = go.Figure()
    for island in ["Maldives", "Lakshadweep", "Seychelles", "Fiji", "Canary Islands"]:
        d = cur[cur["island"] == island].sort_values("distance_m")
        if d.empty:
            continue
        n = int(summ.loc[island, "low_buildings"])
        rule = summ.loc[island, "statutory_setback_m"]
        rule = "no national setback" if rule == "none" else f"setback {rule} m"
        fig.add_trace(go.Scatter(
            x=d["distance_m"], y=d["pct_low_buildings_within"], mode="lines",
            name=f"{island} ({n:,} low buildings; {rule})", line=dict(color=ISLAND_COLOR[island], width=2.4),
            legendgroup=island,
            hovertemplate=f"{island}<br>Within %{{x:,.0f}} m of shore: %{{y:.1f}}% of low buildings<extra></extra>",
        ))
        for sb in SETBACKS.get(island, []):
            v = float(np.interp(sb, d["distance_m"], d["pct_low_buildings_within"]))
            fig.add_trace(go.Scatter(
                x=[sb], y=[v], mode="markers+text", text=[f"{sb} m: {v:.0f}%"],
                textposition="middle left" if island == "Canary Islands" else "bottom right",
                marker=dict(color=ISLAND_COLOR[island], size=11, line=dict(color="white", width=1.5)),
                textfont=dict(color=ISLAND_COLOR[island], size=12), legendgroup=island, showlegend=False,
                hovertemplate=f"{island} statutory setback {sb} m<br>covers {v:.1f}% of low buildings<extra></extra>",
            ))
    fig.update_layout(
        title="How Much of the Low-Lying Building Stock Each Coastal Setback Covers<br>"
              "<sub>Share of buildings at or below 1 m (DeltaDTM, bare earth) within a given distance of the shoreline; "
              "Overture Maps buildings 2026-08-19.0</sub>",
        xaxis_title="Distance from shoreline (m, log scale)",
        yaxis_title="% of buildings at or below 1 m within this distance",
        xaxis=dict(type="log", range=[0, np.log10(3000)]), yaxis=dict(range=[0, 100]),
        legend=dict(x=0.99, y=0.02, xanchor="right", yanchor="bottom", bgcolor="rgba(255,255,255,0.8)"),
        height=580, **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/setback_coverage_curve.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/setback_coverage_curve.html")


if __name__ == "__main__":
    build_compound_vulnerability_score()
    build_coral_thermal_stress_trends()
    build_weighting_sensitivity()
    build_setback_coverage()
