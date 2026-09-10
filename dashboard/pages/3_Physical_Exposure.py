import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

# Folder where the publication-quality static figures (research_paper_figures.py)
# get saved. Used below to show the "as it appears in the Research Paper" version.
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")

st.markdown("<h1 style='text-align: center;'>📉 PHYSICAL EXPOSURE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Settlement-Level Sea-Level-Rise Risk</h3>",
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
    ("Seychelles", 78.3, 244),
    ("Maldives", 14.5, 819),
    ("Lakshadweep", 7.1, 28),
    ("Fiji", 1.0, 909),
    ("Canary Islands", 0.3, 4834),
]

cols = st.columns(5)
for col, (island, pct, total) in zip(cols, exposure_data):
    with col:
        bar_color = PALETTE["risk"] if pct >= 50 else PALETTE["cyan"]
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                    text-align: center; min-height: 190px; border: 1.5px solid rgba(34,211,238,0.3);">
            <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 10px;">{island}</p>
            <p style="color: {bar_color}; font-weight: 900; font-size: 2rem; margin-bottom: 4px;">{pct}%</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.75rem; margin-bottom: 10px;">at or below 1m</p>
            <div style="background: rgba(255,255,255,0.1); border-radius: 20px; height: 10px; overflow: hidden;">
                <div style="background: {bar_color}; width: {pct}%; height: 100%;"></div>
            </div>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; margin-top: 8px;">{total} settlements</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")
st.markdown("##### Figure 2 — As it appears in the Research Paper")
fig2_path = os.path.join(FIGURES_DIR, "fig2_physical_exposure_by_island.png")
if os.path.exists(fig2_path):
    st.image(fig2_path, use_container_width=True)
else:
    st.caption("Figure not found yet — run research_paper_figures.py once to generate it.")

st.markdown("---")

# ============================================================
# POPULATION-WEIGHTED EXPOSURE — complementary metric: what
# fraction of PEOPLE, not just settlement locations, are exposed.
# ============================================================
st.markdown("### Settlement-Based vs. Population-Weighted Exposure")
st.markdown("""
Settlement-count exposure treats every settlement location equally, regardless of how many people
live there. As a complementary check, exposure was also recomputed on a **population-weighted basis**
using WorldPop 2020 data — classifying actual population by the elevation at their location, rather
than counting settlement points alone.
""")

comparison_data = [
    ("Seychelles", 78.3, 17.6),
    ("Maldives", 14.5, 16.9),
    ("Lakshadweep", 7.1, 2.2),
    ("Fiji", 1.0, 2.1),
    ("Canary Islands", 0.3, 1.6),
]
names_c = [d[0] for d in comparison_data]
settlement_pct = [d[1] for d in comparison_data]
population_pct = [d[2] for d in comparison_data]

fig_compare = go.Figure()
fig_compare.add_trace(go.Bar(
    x=names_c, y=settlement_pct, name="Settlement-based",
    marker_color=PALETTE["cyan"],
    text=[f"{p:.1f}%" for p in settlement_pct], textposition="outside",
    textfont=dict(color="#67E8F9", size=11),
))
fig_compare.add_trace(go.Bar(
    x=names_c, y=population_pct, name="Population-weighted",
    marker_color=PALETTE["green"],
    text=[f"{p:.1f}%" for p in population_pct], textposition="outside",
    textfont=dict(color="#FFD60A", size=11),
))
fig_compare.update_layout(
    barmode="group",
    template="plotly_dark",
    yaxis_title="% Exposed to 1m SLR Threshold",
    yaxis=dict(range=[0, 110], tickfont=dict(color="#FFD60A"), title_font=dict(color="#FFD60A")),
    xaxis=dict(tickfont=dict(color="#FFD60A", size=12)),
    legend=dict(font=dict(color="#F1F1F1")),
    height=420,
    font=dict(family="Poppins", color="#FFD60A"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=20, b=40, l=20, r=20),
)
st.plotly_chart(fig_compare, use_container_width=True)

st.warning("""
**Both measures now agree on the same island ranking, though not in magnitude.** Seychelles is
highest by both settlement-based (78.3%) and population-weighted (17.6%) exposure, with Maldives
close behind on the population-weighted measure (16.9%) despite a much lower settlement-based
figure (14.5%). An earlier version of this analysis showed Lakshadweep as the highest
population-weighted-exposure island (87.5%) — that turned out to be a DEM data-quality artifact in
Maldives' and Lakshadweep's original elevation files, not a real finding, and disappeared once the
underlying data was corrected (see the Research Paper's Limitations section).

*Fiji's population-weighted figure reflects approximately 97.6% of its national population —
elevation data did not cover the easternmost Lau Islands, beyond the antimeridian, and this excluded
population is reported explicitly rather than assumed negligible.*
""")

st.markdown("")
st.markdown("##### Figure 3 — As it appears in the Research Paper")
fig3_path = os.path.join(FIGURES_DIR, "fig3_settlement_vs_population_weighted.png")
if os.path.exists(fig3_path):
    st.image(fig3_path, use_container_width=True)
else:
    st.caption("Figure not found yet — run research_paper_figures.py once to generate it.")

st.markdown("---")

st.markdown("### Try a Different SLR Threshold")
st.markdown("""
The 1-meter threshold is a standard benchmark, but sea-level-rise projections vary. Use the
slider below to recalculate settlement-based exposure at a different threshold using the actual
settlement-level elevation data.
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
    textfont=dict(color="#FFD60A", size=13),
))
fig_dynamic.update_layout(
    template="plotly_dark",
    yaxis_title=f"% Settlements At or Below {threshold}m",
    yaxis=dict(range=[0, 105], tickfont=dict(color="#FFD60A"), title_font=dict(color="#FFD60A")),
    xaxis=dict(tickfont=dict(color="#FFD60A", size=13)),
    height=400,
    font=dict(family="Poppins", color="#FFD60A"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=20, b=40, l=20, r=20),
)
st.plotly_chart(fig_dynamic, use_container_width=True)

st.caption(f"Recalculated live from {sum(custom_totals):,} settlement-level elevation samples across all 5 islands.")

st.info("""
**Robustness check — is 1m the right threshold?** Re-running the same analysis at 0.5m and 1.5m
(the practical range of near-term sea-level-rise scenarios) moves most islands by very little; the
largest swing is Maldives, at up to 3.8 percentage points between the two extremes — still small in
absolute terms, and not enough to change the ranking at any threshold tested. Seychelles (≈78%)
stays the most exposed island throughout, Canary Islands and Fiji stay the two least exposed (both
well under 2%) at every threshold tested. The 1m benchmark used throughout this study is not doing
hidden work in the result.
""")

st.markdown("---")

st.markdown("### Why Elevation Varies So Widely")

col1, col2 = st.columns(2)
with col1:
    st.error("""
    **Low-lying coral atolls** — Maldives and Lakshadweep sit almost entirely within a 0–20 meter
    elevation range, a direct consequence of their coral-atoll geology. That still leaves a
    meaningful minority of settlements (14.5% and 7.1% respectively) at or below the 1-meter
    threshold — moderate exposure, not the near-total exposure an earlier, DEM-error-driven version
    of this analysis suggested.
    """)
with col2:
    st.success("""
    **Volcanic, mountainous terrain** — The Canary Islands rise to nearly 3,700 meters at Mount
    Teide, giving settlements considerably more elevation buffer even where coastal development is
    dense. Seychelles is the exception among the higher-elevation islands: despite granite peaks
    over 900 meters, its settlement pattern concentrates disproportionately in low-lying coastal
    areas, which is what drives its 78.3% exposure figure — the highest in this sample.
    """)

st.markdown("---")

# ============================================================
# DEM PRECISION NOTE
# ============================================================
st.markdown("### A Note on Elevation Data Precision")
st.info("""
Exposure figures on this page are derived from Copernicus DEM GLO-30, a 30-meter-resolution,
radar-derived global elevation model. Like all global DEMs, GLO-30 captures surface elevation —
including vegetation canopy and buildings — rather than true bare-earth elevation, introducing
non-trivial vertical uncertainty relative to the fine, 1-meter threshold used here. The **relative
ranking** of islands, which drives this study's central findings, is considered reliable; absolute
percentages should be read as directionally indicative rather than exact counts.
""")

st.markdown("---")

st.markdown("### An Important Caveat")
st.info("""
**Every exposure measure here now agrees — which is itself worth noting.** Seychelles has the
highest settlement-based exposure (78.3%), the highest population-weighted exposure (17.6%), and
the highest overall Compound Vulnerability Score once coral thermal-stress trend is factored in.
An earlier version of this analysis showed Maldives and Lakshadweep as far more exposed on both
measures, which created an appearance of disagreement between indicators — that turned out to be a
DEM data-quality artifact rather than a real finding (see Limitations, Research Paper). The
broader methodological point still holds: exposure, however it's measured, is a necessary but
insufficient measure of true climate vulnerability on its own, since it leaves out ecosystem
condition entirely.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: Copernicus DEM GLO-30, OpenStreetMap settlements</p>",
    unsafe_allow_html=True,
)