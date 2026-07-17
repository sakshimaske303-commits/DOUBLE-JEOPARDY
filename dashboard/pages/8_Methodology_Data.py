import streamlit as st
import pandas as pd
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📖 METHODOLOGY & DATA</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Full Transparency, Reproducibility, and Limitations</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### Data Sources")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **Settlements, Tourism, Infrastructure** — OpenStreetMap
    - **Mangrove Extent (1996/2010/2020)** — Global Mangrove Watch
    - **Coral Reef Extent** — WCMC / OpenStreetMap
    - **Coral Thermal Stress (1996–2020)** — NOAA Coral Reef Watch
    """)
with col2:
    st.markdown("""
    - **Elevation, Slope** — Copernicus DEM GLO-30
    - **Population** — WorldPop 2020
    - **Cyclone Tracks** — IBTrACS v04r01
    - **Protected Areas** — World Database on Protected Areas (WDPA)
    """)

st.markdown("---")

st.markdown("### The Validation Journey (Click to view the dropdown)")

with st.expander("**Feature Count ≠ Area: The Mangrove Measurement Trap**"):
    st.markdown("""
    An initial comparison using raw polygon feature counts suggested a 14.2% mangrove decline in 
    Fiji between 1996 and 2020. Before accepting this, area was independently recalculated in an 
    equal-area projection across all three time points — revealing the apparent decline was an 
    artifact of how satellite classification algorithms segment polygons differently across years, 
    not a genuine reduction in mangrove extent. True area remained essentially stable.
    """)

with st.expander("**A Data-Quality Bug: Maldives' Coral File Wasn't Actually Coral Data**"):
    st.markdown("""
    An initial coral reef file for the Maldives contained 4,230 rows — but inspection revealed 
    columns like `cuisine`, `spa`, and `payment:visa`, indicating the file was an unfiltered 
    general OpenStreetMap export, not coral-specific data. Filtering to genuine `natural=reef` 
    tags recovered 2,921 verified coral reef features.
    """)

with st.expander("**A Satellite-Record Constraint: Cyclone Damage Verification**"):
    st.markdown("""
    An attempt to extend satellite-based cyclone damage verification to Maldives, Seychelles, and 
    Lakshadweep failed for a structural reason: each island's strongest historically recorded 
    cyclone predates 2015, when Sentinel-2 (the satellite used throughout this project) launched. 
    No valid "before" imagery could exist for these events. This is documented as a genuine 
    methodological boundary, not a gap to work around.
    """)

with st.expander("**Governance Ratio Sanity Check: Comparing Land to Marine EEZs**"):
    st.markdown("""
    An initial protected-area-to-land ratio for Seychelles came out to 1,005.69 — a nonsensical 
    result caused by including the country's Exclusive Economic Zone (over a million km² of ocean) 
    in the calculation. This was corrected by restricting the metric to a 10km coastal buffer 
    around each island, producing interpretable, comparable ratios.
    """)

st.markdown("---")

st.markdown("### Honest Limitations")

st.warning("""
**Small sample size.** With only five islands, several findings — particularly the governance 
correlation (H3) — are statistically suggestive rather than confirmatory. This is a genuine 
constraint of cross-national island-nation research, not glossed over in this project's conclusions.
""")

st.info("""
**Uneven data depth.** Lakshadweep population data and Canary Islands coral/mangrove data were 
confirmed genuinely absent (not acquisition failures) — geographically and ecologically explained, 
and documented transparently rather than substituted or estimated.
""")

st.markdown("---")

st.markdown("### Download the Data")

try:
    df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "compound_vulnerability_scores.csv"))
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Compound Vulnerability Scores (CSV)", csv,
                        "double_jeopardy_vulnerability_scores.csv", "text/csv")
except FileNotFoundError:
    st.markdown("*(Data file not found — check path)*")

st.markdown("---")

st.markdown("""
<div style="background: rgba(0,150,199,0.06); border: 1px solid rgba(0,150,199,0.25); border-radius: 10px; padding: 16px;">
    <strong style="color: #072a4d;">GitHub Repository:</strong> <a href="https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY" target="_blank" style="color: #0096c7;">github.com/sakshimaske303-commits/DOUBLE-JEOPARDY</a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, {PALETTE['card_bg']}, #e8f4f8); border-radius: 16px; border: 1px solid rgba(0,150,199,0.2);">
        <p style="color: {PALETTE['text_muted']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Project Author</p>
        <h2 style="color: {PALETTE['navy']}; margin: 5px 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['green']}; font-weight: 600;">Independent Geospatial Researcher</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — The Vulnerability Spiral</p>",
    unsafe_allow_html=True,
)