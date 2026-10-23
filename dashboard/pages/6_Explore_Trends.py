import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pval

apply_custom_style()

# Trend results read from data/coral_trend_results.csv (rewritten 2026-10-11).
R = load_results()

st.markdown("<h1 style='text-align: center;'>EXPLORE TRENDS</h1>", unsafe_allow_html=True)
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

# Fixed per-island colors (not PALETTE -- several entries look near-identical
# on the dark theme). Canary isn't yellow since the axis/legend font already is.
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
    """Horizontal reference line with a boxed, arrow-anchored label (fixed
    position reads better than Plotly's auto-placed inline text)."""
    fig.add_hline(y=y, line_dash="dot", line_color=color)
    fig.add_annotation(
        x=anchor_x, y=y, xref="x", yref="y",
        text=label,
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.3,
        arrowcolor=color, ax=0, ay=ay_offset,
        font=dict(color=color, size=11, family="Poppins"),
        bgcolor="rgba(10,10,10,0.75)", bordercolor=color, borderwidth=1, borderpad=5,
    )


st.markdown("### Coral Thermal Stress Over Time (1996–2020)")

selected_islands = st.multiselect(
    "Select islands to compare",
    options=ISLANDS,
    default=["Seychelles", "Maldives"],
)

show_periods = st.checkbox("Show 1996–2000 and 2016–2020 period means", value=True)


def load_series(key):
    """Mean DHW over all mapped reef cells; the Canary Islands have no mapped reef, so one 5 km cell."""
    reef = os.path.join(PROJECT_ROOT, "data", "coral_bleaching_v3", f"{key}_dhw_reefcells_mean.csv")
    if os.path.exists(reef):
        df = pd.read_csv(reef).rename(columns={"dhw_mean": "dhw"})
    else:
        df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "coral_bleaching", f"{key}_dhw_timeseries.csv"),
                         skiprows=[1]).rename(columns={"degree_heating_week": "dhw"})
    df["time"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert(None)
    return df.sort_values("time")[["time", "dhw"]]


if selected_islands:
    fig = go.Figure()
    for island_name in selected_islands:
        key = ISLAND_FILE_MAP[island_name]
        try:
            df = load_series(key)
        except FileNotFoundError:
            st.warning(f"Data not found for {island_name}")
            continue
        series = R["coral_series"][key]
        p = R["coral_p"][(key, series)]
        line_color = ISLAND_COLOR[island_name]
        fig.add_trace(go.Scatter(x=df["time"], y=df["dhw"], mode="lines",
                                 name=f"{island_name} (trend test {pval(p)})",
                                 line=dict(color=line_color, width=2)))
        if show_periods:
            for y0, y1 in ((1996, 2000), (2016, 2020)):
                m = df[(df["time"].dt.year >= y0) & (df["time"].dt.year <= y1)]["dhw"].mean()
                fig.add_trace(go.Scatter(x=[pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y1}-12-31")], y=[m, m],
                                         mode="lines", showlegend=False, hoverinfo="text",
                                         text=f"{island_name} mean {y0}–{y1}: {m:.2f}",
                                         line=dict(color=line_color, width=3, dash="dash")))

    # Threshold labels spread apart on the x-axis so they don't sit on a data spike.
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
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    sig = [ISLANDS[i] for i, k in enumerate(ISLAND_FILE_MAP.values())
           if R["coral_p"][(k, R["coral_series"][k])] < 0.05]
    st.markdown(
        "<p class='caption-text'>Each line is the mean Degree Heating Weeks over all mapped reef cells "
        "(Canary Islands: one 5 km cell, no mapped reef). Dashed segments are the 1996–2000 and 2016–2020 means. "
        "The p-value is a seasonal Mann-Kendall test on monthly means, corrected for serial correlation "
        "(DHW is a 12-week running sum, so neighbouring months are not independent). "
        + ("No island shows a significant trend at the 5% level once this is accounted for; "
           "without the correction Seychelles would appear significant."
           if not sig else f"Significant at the 5% level: {', '.join(sig)}.")
        + "</p>",
        unsafe_allow_html=True,
    )
else:
    st.info("Select at least one island above to view its thermal stress series.")

st.markdown("---")

st.markdown("### Mangrove Extent Over Time (1996, 2010, 2020)")

mangrove_data = {R["label"][k]: list(v) for k, v in R["mangroves"].items()}
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
        "<p class='caption-text'>Near-flat lines: Global Mangrove Watch shows no decline in mapped mangrove extent on any of the three islands. Mangrove patches on the atolls are close to the 25 m pixel size, so small losses there may not be detectable.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch, Global Mangrove Watch</p>",
    unsafe_allow_html=True,
)