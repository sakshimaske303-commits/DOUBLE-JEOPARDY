import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📉 PHYSICAL EXPOSURE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Settlement-Level Sea-Level-Rise Risk</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Physical exposure was quantified by sampling elevation at every settlement's location across all 
five islands, identifying the proportion of settlements at or below a standard **1-meter sea-level-rise 
threshold** — a widely used benchmark for near-term coastal flood risk.
""")

st.markdown("---")

st.markdown("### Exposure by Island")

exposure_data = [
    ("Maldives", 99.1, 996),
    ("Seychelles", 78.3, 244),
    ("Lakshadweep", 77.8, 36),
    ("Fiji", 32.0, 1323),
    ("Canary Islands", 12.1, 5483),
]

cols = st.columns(5)
for col, (island, pct, total) in zip(cols, exposure_data):
    with col:
        bar_color = PALETTE["risk"] if pct >= 50 else PALETTE["cyan"]
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                    text-align: center; min-height: 190px; border: 1.5px solid rgba(0,150,199,0.3);">
            <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 10px;">{island}</p>
            <p style="color: {bar_color}; font-weight: 900; font-size: 2rem; margin-bottom: 4px;">{pct}%</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.75rem; margin-bottom: 10px;">at or below 1m</p>
            <div style="background: #dfe9ef; border-radius: 20px; height: 10px; overflow: hidden;">
                <div style="background: {bar_color}; width: {pct}%; height: 100%;"></div>
            </div>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; margin-top: 8px;">{total} settlements</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 🎛️ Try a Different SLR Threshold")
st.markdown("""
The 1-meter threshold is a standard benchmark, but sea-level-rise projections vary. Use the 
slider below to recalculate exposure at a different threshold using the actual settlement-level 
elevation data.
""")

@st.cache_data
def load_elevations():
    return pd.read_csv(os.path.join(PROJECT_ROOT, "dashboard", "static", "settlement_elevations.csv"))

elev_df = load_elevations()

threshold = st.slider("SLR Threshold (meters)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

island_order = ["Maldives", "Seychelles", "Lakshadweep", "Fiji", "Canary"]
custom_pcts = []
custom_totals = []
for island in island_order:
    subset = elev_df[elev_df["island"] == island]
    total = len(subset)
    at_risk = (subset["elevation_m"] <= threshold).sum()
    pct = (at_risk / total * 100) if total > 0 else 0
    custom_pcts.append(pct)
    custom_totals.append(total)

display_names = ["Maldives", "Seychelles", "Lakshadweep", "Fiji", "Canary Islands"]
colors_dynamic = [PALETTE["risk"] if p >= 50 else PALETTE["cyan"] for p in custom_pcts]

fig_dynamic = go.Figure()
fig_dynamic.add_trace(go.Bar(
    x=display_names, y=custom_pcts, marker_color=colors_dynamic,
    text=[f"{p:.1f}%" for p in custom_pcts], textposition="outside",
    textfont=dict(color="#000000", size=13),
))
fig_dynamic.update_layout(
    template="plotly_white",
    yaxis_title=f"% Settlements At or Below {threshold}m",
    yaxis=dict(range=[0, 105], tickfont=dict(color="#000000"), title_font=dict(color="#000000")),
    xaxis=dict(tickfont=dict(color="#000000", size=13)),
    height=400,
    font=dict(family="Poppins", color="#000000"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=20, b=40, l=20, r=20),
)
st.plotly_chart(fig_dynamic, use_container_width=True)

st.caption(f"Recalculated live from {sum(custom_totals):,} settlement-level elevation samples across all 5 islands.")

st.markdown("---")

st.markdown("### Why Elevation Varies So Widely")

col1, col2 = st.columns(2)
with col1:
    st.error("""
    **Low-lying coral atolls** — Maldives and Lakshadweep sit almost entirely within a 0–20 meter 
    elevation range, a direct consequence of their coral-atoll geology. This makes near-total 
    settlement exposure to sea-level rise a structural, not incidental, feature of these nations.
    """)
with col2:
    st.success("""
    **Volcanic, mountainous terrain** — The Canary Islands rise to nearly 3,700 meters at Mount 
    Teide, and Seychelles' granite islands reach over 900 meters, giving settlements considerably 
    more elevation buffer even where coastal development is dense.
    """)

st.markdown("---")

st.markdown("### An Important Caveat")
st.info("""
**Physical exposure alone can be misleading.** The Maldives shows the highest exposure of any 
island in this sample (99.1%), yet — as the Compound Vulnerability analysis shows — it is **not** 
the highest-overall-risk island once ecosystem degradation is factored in. Elevation-based exposure 
is a necessary but insufficient measure of true climate vulnerability.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: Copernicus DEM GLO-30, OpenStreetMap settlements</p>",
    unsafe_allow_html=True,
)