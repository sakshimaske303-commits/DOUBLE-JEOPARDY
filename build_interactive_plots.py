"""Interactive Plotly versions of the three headline DOUBLE JEOPARDY charts.
Same underlying data as the static figures (map1_vulnerability_score.py,
research_paper_figures.py fig4/fig7) - just Plotly instead of matplotlib."""

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
    data = {
        "island": ["Seychelles", "Maldives", "Lakshadweep", "Fiji", "Canary Islands"],
        "score": [0.895, 0.651, 0.481, 0.263, 0.000],
    }
    df = pd.DataFrame(data).sort_values("score", ascending=True)
    colors = ["#2c7fb8" if s < 0.5 else "#e34a33" for s in df["score"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["score"], y=df["island"], orientation="h", marker_color=colors,
        marker_line=dict(color="#333333", width=1),
        text=[f"{s:.3f}" for s in df["score"]], textposition="outside",
        hovertemplate="%{y}<br>Score: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title="Compound Vulnerability Score by Island<br><sub>Combining physical SLR exposure and coral thermal-stress trend</sub>",
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
    trend_info = {
        "Maldives": {"intercept": 0.0895, "slope_per_year": 0.00450, "significant": True, "p": 0.011},
        "Seychelles": {"intercept": -0.0668, "slope_per_year": 0.02532, "significant": True, "p": 0.025},
        "Fiji": {"intercept": 0.3250, "slope_per_year": 0.00151, "significant": False, "p": 0.184},
        "Lakshadweep": {"intercept": 0.1072, "slope_per_year": 0.00254, "significant": False, "p": 0.386},
        "Canary Islands": {"intercept": 0.4762, "slope_per_year": 0.01905, "significant": False, "p": 0.641},
    }

    fig = go.Figure()
    for island in ISLAND_ORDER:
        file_key = ISLAND_FILE_MAP[island]
        path = f"data/coral_bleaching/{file_key}_dhw_timeseries.csv"
        df = pd.read_csv(path, skiprows=[1])
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time")
        color = ISLAND_COLOR[island]

        fig.add_trace(go.Scatter(
            x=df["time"], y=df["degree_heating_week"], mode="lines", name=f"{island} (raw)",
            line=dict(color=color, width=1.3), opacity=0.75, legendgroup=island,
            hovertemplate=f"{island}<br>%{{x|%Y-%m}}<br>DHW: %{{y:.2f}}°C-wk<extra></extra>",
        ))

        info = trend_info[island]
        start_date, end_date = df["time"].iloc[0], df["time"].iloc[-1]
        years_elapsed = (end_date - start_date).days / 365.25
        y_start = info["intercept"]
        y_end = info["intercept"] + info["slope_per_year"] * years_elapsed
        sig_label = "significant" if info["significant"] else "not significant"
        fig.add_trace(go.Scatter(
            x=[start_date, end_date], y=[y_start, y_end], mode="lines",
            name=f"{island} trend (MK {sig_label}, p={info['p']:.3f})",
            line=dict(color=color, width=2.6, dash="dash"), legendgroup=island,
            hovertemplate=f"{island} trend<br>MK {sig_label}, p={info['p']:.3f}<extra></extra>",
        ))

    fig.add_hline(y=4, line_color="orange", line_dash="dot", annotation_text="Bleaching threshold (4°C-wk)", annotation_font_color="orange")
    fig.add_hline(y=8, line_color="darkred", line_dash="dot", annotation_text="Severe bleaching/mortality (8°C-wk)", annotation_font_color="darkred")

    fig.update_layout(
        title="Coral Thermal Stress Over Time (1996-2020), with Trend Lines<br>"
              "<sub>Dashed lines are OLS fits; significance assessed via Mann-Kendall trend test on the full series</sub>",
        xaxis_title="Date", yaxis_title="Degree Heating Week (°C-weeks)",
        height=600, hovermode="closest", **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/coral_thermal_stress_trends.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/coral_thermal_stress_trends.html")


# ============================================================
# 3. WEIGHTING SENSITIVITY CURVE
# ============================================================
def build_weighting_sensitivity():
    slr_data = {"Maldives": 99.1, "Seychelles": 78.3, "Fiji": 32.0, "Canary Islands": 0.3, "Lakshadweep": 77.8}
    coral_decline = {"Maldives": 0.17, "Seychelles": 0.68, "Fiji": 0.10, "Canary Islands": -0.05, "Lakshadweep": 0.08}

    def normalize(d):
        values = list(d.values())
        min_v, max_v = min(values), max(values)
        return {k: (v - min_v) / (max_v - min_v) if max_v > min_v else 0 for k, v in d.items()}

    slr_norm = normalize(slr_data)
    coral_norm = normalize(coral_decline)
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
              "<sub>Seychelles leads up to ~76.8% physical-exposure weighting; Maldives overtakes beyond that</sub>",
        xaxis_title="Physical Exposure Weight (%) — remainder assigned to coral ecosystem decline",
        yaxis_title="Compound Vulnerability Score (normalized, 0-1)",
        xaxis=dict(range=[0, 100]), yaxis=dict(range=[-0.05, 1.05]),
        height=560, **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/weighting_sensitivity_curve.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/weighting_sensitivity_curve.html")


if __name__ == "__main__":
    build_compound_vulnerability_score()
    build_coral_thermal_stress_trends()
    build_weighting_sensitivity()
