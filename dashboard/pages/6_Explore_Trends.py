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
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Interactive Island-Level Time Series</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

ISLANDS = ["Maldives", "Seychelles", "Fiji", "Canary Islands", "Lakshadweep"]
ISLAND_FILE_MAP = {
    "Maldives": "maldives", "Seychelles": "seychelles", "Fiji": "fiji",
    "Canary Islands": "canary", "Lakshadweep": "lakshadweep",
}

st.markdown("### 🌡️ Coral Thermal Stress Over Time (1996–2020)")

selected_islands = st.multiselect(
    "Select islands to compare",
    options=ISLANDS,
    default=["Seychelles", "Canary Islands"],
)

if selected_islands:
    fig = go.Figure()
    color_palette = [PALETTE["cyan"], PALETTE["risk"], PALETTE["mint"], PALETTE["navy"], "#f4a261"]

    for i, island_name in enumerate(selected_islands):
        file_key = ISLAND_FILE_MAP[island_name]
        path = os.path.join(PROJECT_ROOT, "data", "coral_bleaching", f"{file_key}_dhw_timeseries.csv")
        try:
            df = pd.read_csv(path, skiprows=[1])
            df["time"] = pd.to_datetime(df["time"])
            fig.add_trace(go.Scatter(
                x=df["time"], y=df["degree_heating_week"],
                mode="lines", name=island_name,
                line=dict(color=color_palette[i % len(color_palette)], width=2),
            ))
        except FileNotFoundError:
            st.warning(f"Data not found for {island_name}")

    fig.add_hline(y=4, line_dash="dot", line_color="orange", annotation_text="Bleaching threshold (4°C-wk)")
    fig.add_hline(y=8, line_dash="dot", line_color="red", annotation_text="Severe bleaching/mortality (8°C-wk)")

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Degree Heating Week (°C-weeks)",
        xaxis=dict(tickfont=dict(color="#000000")),
        yaxis=dict(tickfont=dict(color="#000000"), title_font=dict(color="#000000")),
        height=500,
        font=dict(family="Poppins", color="#000000"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#000000")),
        margin=dict(t=60, b=40, l=40, r=40),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "<p class='caption-text'>Dotted lines mark bleaching thresholds. Higher, more frequent peaks above these lines indicate greater thermal stress on coral reefs.</p>",
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
    for i, island_name in enumerate(selected_mangrove_islands):
        fig2.add_trace(go.Scatter(
            x=years, y=mangrove_data[island_name],
            mode="lines+markers", name=island_name,
            line=dict(color=color_palette[i % len(color_palette)], width=3),
            marker=dict(size=10),
        ))

    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Mangrove Area (km²)",
        xaxis=dict(tickmode="array", tickvals=years, tickfont=dict(color="#000000")),
        yaxis=dict(tickfont=dict(color="#000000"), title_font=dict(color="#000000")),
        height=450,
        font=dict(family="Poppins", color="#000000"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#000000")),
        margin=dict(t=60, b=40, l=40, r=40),
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        "<p class='caption-text'>Note the near-flat lines — mangrove extent shows no meaningful decline across any tested island, contrary to the original hypothesis.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch, Global Mangrove Watch</p>",
    unsafe_allow_html=True,
)