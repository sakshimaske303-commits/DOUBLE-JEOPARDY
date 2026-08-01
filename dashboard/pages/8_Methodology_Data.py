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
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Full Transparency, Reproducibility, and Limitations</h3>",
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

with st.expander("**Filling a Data Gap: Lakshadweep's Population, Revisited**"):
    st.markdown("""
    Lakshadweep population data was initially unavailable, since the only access method found
    required downloading a population raster covering the entirety of India. A smaller, more
    targeted file — WorldPop's constrained, UN-adjusted 2020 India dataset (~470MB rather than
    several gigabytes) — was later identified, clipped down to Lakshadweep's boundary, and
    incorporated into a population-weighted exposure analysis alongside all four other islands.
    """)

st.markdown("---")

st.markdown("---")

st.markdown("### Behind the Scenes — QGIS & VS Code")
st.markdown(
    "<p class='caption-text'>A look at the actual geospatial and coding workflow behind this "
    "project — not just the finished dashboard.</p>",
    unsafe_allow_html=True,
)

SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")

QGIS_SHOTS = [
    ("QGIS_SS1.png", "Canary Islands WDPA protected areas overlaid on satellite basemap, with live attribute inspection (Identify Results panel)."),
    ("QGIS_SS2.png", "Seychelles elevation (Copernicus DEM) styled as a pseudocolor raster, with the Symbology panel used to configure the classification."),
    ("QGIS_SS3.png", "Fiji coral reef features — attribute table showing 196 individual reef polygons alongside cyclone track data."),
    ("QGIS_SS4.png", "Canary Islands settlement points with live attribute inspection — real place names and metadata (population, source tags) pulled directly via the Identify tool."),
]

VS_SHOTS = [
    ("VS_SS1.png", "population_weighted_exposure.py — per-island elevation/population raster windows, including the antimeridian handling for Fiji."),
    ("VS_SS2.png", "coral_trend_test.py — the Mann-Kendall trend test function, run live in the integrated terminal."),
    ("VS_SS3.png", "governance_correlation_test.py — the Pearson correlation test between compound vulnerability and protected-area coverage."),
    ("VS_SS4.png", "6_Explore_Trends.py — source code for one of the dashboard's interactive pages."),
]

st.markdown("##### QGIS — Geospatial Analysis")
cols = st.columns(2)
for i, (fname, caption) in enumerate(QGIS_SHOTS):
    path = os.path.join(SCREENSHOTS_DIR, fname)
    with cols[i % 2]:
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            st.markdown(f"<p class='caption-text'>{caption}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"*(Missing: {fname})*")

st.markdown("##### VS Code — Analysis & Dashboard Code")
cols = st.columns(2)
for i, (fname, caption) in enumerate(VS_SHOTS):
    path = os.path.join(SCREENSHOTS_DIR, fname)
    with cols[i % 2]:
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            st.markdown(f"<p class='caption-text'>{caption}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"*(Missing: {fname})*")

st.markdown("### Honest Limitations")

st.warning("""
**Small sample size.** With only five islands, several findings — particularly the governance
correlation (H3), whose 95% confidence interval spans from r = -0.43 to r = 0.98 — are
statistically suggestive rather than confirmatory. This is a genuine constraint of cross-national
island-nation research, not glossed over in this project's conclusions.
""")

st.info("""
**Uneven data depth.** Canary Islands coral and mangrove data were confirmed genuinely absent —
geographically and ecologically explained by its subtropical, volcanic Atlantic setting outside
typical coral and mangrove habitat range — and documented transparently rather than substituted
or estimated. Lakshadweep population data, initially unavailable for the reason described above,
was later obtained and is now included in the population-weighted exposure analysis.
""")

st.error("""
**Partial elevation coverage for Fiji.** Elevation data did not extend to Fiji's easternmost
territory (the Lau Islands, beyond the antimeridian). Fiji's population-weighted exposure figure
therefore reflects approximately 97.6% of its national population; the excluded population is
reported explicitly rather than assumed negligible.
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

st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border: 1px solid rgba(34,211,238,0.3); border-radius: 10px; padding: 16px;">
    <strong style="color: {PALETTE['green']};">GitHub Repository:</strong> <a href="https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY" target="_blank" style="color: {PALETTE['navy']};">github.com/sakshimaske303-commits/DOUBLE-JEOPARDY</a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px; background: {PALETTE['card_bg']}; border-radius: 16px; border: 1px solid rgba(34,211,238,0.25);">
        <p style="color: {PALETTE['text_muted']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Project Author</p>
        <h2 style="color: {PALETTE['navy']}; margin: 5px 0; border: none; padding: 0;">SAKSHI D. MASKE</h2>
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