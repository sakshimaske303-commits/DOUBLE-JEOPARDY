import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📈 EXPLORE TRENDS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Interactive Island-Level Time Series</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

ISLANDS = ["Maldives", "Seychelles", "Fiji", "Canary Islands", "Lakshadweep"]
ISLAND_FILE_MAP = {
    "Maldives": "maldives", "Seychelles": "seychelles", "Fiji": "fiji",
    "Canary Islands": "canary", "Lakshadweep": "lakshadweep",
}

# Precomputed OLS trend line (intercept + slope/year, in years since 1996-01-01)
# and Mann-Kendall significance, from the robustness-check trend test run
# on the complete 24-year series for each island.
TREND_INFO = {
    "Maldives": {"intercept": 0.0895, "slope_per_year": 0.00450, "significant": True, "p": 0.011},
    "Seychelles": {"intercept": -0.0668, "slope_per_year": 0.02532, "significant": True, "p": 0.025},
    "Fiji": {"intercept": 0.3250, "slope_per_year": 0.00151, "significant": False, "p": 0.184},
    "Lakshadweep": {"intercept": 0.1072, "slope_per_year": 0.00254, "significant": False, "p": 0.386},
    "Canary Islands": {"intercept": 0.4762, "slope_per_year": 0.01905, "significant": False, "p": 0.641},
}

# Fixed, clearly-distinguishable color per island (not pulled from PALETTE,
# since several PALETTE entries read as near-identical shades of blue/cyan
# on the dark theme and made the lines impossible to tell apart). Canary
# Islands is deliberately NOT yellow — the chart's axis/legend font is
# already a gold-yellow (#FFD60A), so a yellow data line would blend into
# the text and become hard to read.
ISLAND_COLOR = {
    "Maldives": "#ef4444",        # red
    "Seychelles": "#22c55e",      # green
    "Fiji": "#3b82f6",            # blue
    "Canary Islands": "#ec4899",  # pink/magenta
    "Lakshadweep": "#a855f7",     # purple
}

# Colors for the two horizontal reference thresholds (distinct from every
# island color above, so a threshold line is never confused with island data).
THRESHOLD_COLOR = "#f4a261"       # amber — 4°C-wk bleaching threshold
SEVERE_COLOR = "#dc2626"          # deep red — 8°C-wk severe bleaching/mortality


def add_threshold_line(fig, y, label, color, anchor_x, ay_offset):
    """Draws a horizontal reference line plus a clearly separated, boxed
    annotation with a small arrow pointing back to the line. Placing the
    label in a fixed spot with its own background box (rather than letting
    Plotly auto-place inline text on the line) keeps it legible no matter
    which island lines happen to cross that region."""
    fig.add_hline(y=y, line_dash="dot", line_color=color)
    fig.add_annotation(
        x=anchor_x, y=y, xref="x", yref="y",
        text=label,
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.3,
        arrowcolor=color, ax=0, ay=ay_offset,
        font=dict(color=color, size=11, family="Poppins"),
        bgcolor="rgba(10,10,10,0.75)", bordercolor=color, borderwidth=1, borderpad=5,
    )


st.markdown("### 🌡️ Coral Thermal Stress Over Time (1996–2020)")

selected_islands = st.multiselect(
    "Select islands to compare",
    options=ISLANDS,
    default=["Seychelles", "Canary Islands"],
)

show_trend = st.checkbox("Show trend line (Mann-Kendall / OLS robustness check)", value=True)

if selected_islands:
    fig = go.Figure()

    for island_name in selected_islands:
        file_key = ISLAND_FILE_MAP[island_name]
        path = os.path.join(PROJECT_ROOT, "data", "coral_bleaching", f"{file_key}_dhw_timeseries.csv")
        try:
            df = pd.read_csv(path, skiprows=[1])
            df["time"] = pd.to_datetime(df["time"])
            df = df.sort_values("time")
            line_color = ISLAND_COLOR[island_name]

            fig.add_trace(go.Scatter(
                x=df["time"], y=df["degree_heating_week"],
                mode="lines", name=island_name,
                line=dict(color=line_color, width=2),
            ))

            if show_trend and island_name in TREND_INFO:
                info = TREND_INFO[island_name]
                start_date = df["time"].iloc[0]
                end_date = df["time"].iloc[-1]
                years_elapsed = (end_date - start_date).days / 365.25
                y_start = info["intercept"]
                y_end = info["intercept"] + info["slope_per_year"] * years_elapsed
                sig_label = f"significant, p={info['p']:.3f}" if info["significant"] else f"not significant, p={info['p']:.3f}"

                fig.add_trace(go.Scatter(
                    x=[start_date, end_date], y=[y_start, y_end],
                    mode="lines", name=f"{island_name} trend ({sig_label})",
                    line=dict(color=line_color, width=2, dash="dash"),
                    opacity=0.85,
                ))
        except FileNotFoundError:
            st.warning(f"Data not found for {island_name}")

    # Reference threshold lines — labels boxed and arrow-anchored, spread
    # apart on the x-axis and offset upward, so they never sit on top of a
    # data spike the way a default inline annotation would.
    add_threshold_line(fig, y=4, label="Bleaching threshold (4°C-wk)",
                        color=THRESHOLD_COLOR, anchor_x="1997-03-01", ay_offset=-38)
    add_threshold_line(fig, y=8, label="Severe bleaching / mortality (8°C-wk)",
                        color=SEVERE_COLOR, anchor_x="2001-09-01", ay_offset=-38)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Degree Heating Week (°C-weeks)",
        xaxis=dict(tickfont=dict(color="#FFD60A")),
        yaxis=dict(tickfont=dict(color="#FFD60A"), title_font=dict(color="#FFD60A")),
        height=520,
        font=dict(family="Poppins", color="#FFD60A"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#FFD60A")),
        margin=dict(t=70, b=40, l=40, r=40),
    )

    # Hide the hover modebar (camera/zoom/pan icons) — on the live dashboard
    # it was rendering directly over the legend text, adding clutter.
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        "<p class='caption-text'>Dashed lines (if shown) are the OLS trend fit for each island; significance is "
        "assessed via a Mann-Kendall trend test on the complete 24-year series. Only Maldives and Seychelles reach "
        "statistical significance — the two islands driving this project's compound vulnerability ranking.</p>",
        unsafe_allow_html=True,
    )
else:
    st.info("Select at least one island above to view its thermal stress trend.")

st.markdown("---")

st.markdown("### 🌳 Mangrove Extent Over Time (1996, 2010, 2020)")

mangrove_data = {
    "Maldives": [0.97, 0.97, 0.97],
    "Seychelles": [3.83, 3.84, 3.83],
    "Fiji": [485.72, 487.97, 488.41],
}
years = [1996, 2010, 2020]

selected_mangrove_islands = st.multiselect(
    "Select islands to compare (mangrove-present islands only)",
    options=list(mangrove_data.keys()),
    default=list(mangrove_data.keys()),
)

if selected_mangrove_islands:
    fig2 = go.Figure()
    for island_name in selected_mangrove_islands:
        fig2.add_trace(go.Scatter(
            x=years, y=mangrove_data[island_name],
            mode="lines+markers", name=island_name,
            line=dict(color=ISLAND_COLOR[island_name], width=3),
            marker=dict(size=10),
        ))

    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Mangrove Area (km²)",
        xaxis=dict(tickmode="array", tickvals=years, tickfont=dict(color="#FFD60A")),
        yaxis=dict(tickfont=dict(color="#FFD60A"), title_font=dict(color="#FFD60A")),
        height=450,
        font=dict(family="Poppins", color="#FFD60A"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#FFD60A")),
        margin=dict(t=60, b=40, l=40, r=40),
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        "<p class='caption-text'>Note the near-flat lines — mangrove extent shows no meaningful decline across any tested island, contrary to the original hypothesis.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch, Global Mangrove Watch</p>",
    unsafe_allow_html=True,
)