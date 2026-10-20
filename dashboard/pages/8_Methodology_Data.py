import streamlit as st
import pandas as pd
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pct, source_label

apply_custom_style()

# Limitations text reads its numbers from the pipeline's CSVs (rewritten 2026-10-11).
R = load_results()
G = R["gov"]

st.markdown("<h1 style='text-align: center;'>📖 METHODOLOGY & DATA</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Full Transparency, Reproducibility, and Limitations</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Proof-of-work popovers: pulsing buttons that reveal a screenshot inline.
# Falls back to a quiet note if the PNG isn't in outputs/proof_screenshots/ yet.
st.markdown(f"""
<style>
    div[data-testid="stPopover"] button {{
        animation: proof-blink 1.8s ease-in-out infinite;
        border: 3px solid {PALETTE['navy']} !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        min-height: unset !important;
        min-width: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stPopover"] button p {{
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1 !important;
    }}
    @keyframes proof-blink {{
        0%, 100% {{ box-shadow: 0 0 0px rgba(34, 211, 238, 0); }}
        50% {{ box-shadow: 0 0 12px rgba(34, 211, 238, 0.85); }}
    }}
</style>
""", unsafe_allow_html=True)

PROOF_DIR = os.path.join(PROJECT_ROOT, "outputs", "proof_screenshots")

# Code screenshots (*_vscode.png) show an earlier version of the scripts and are not displayed.
def proof_popover(filename, caption):
    if filename.endswith("_vscode.png"):
        return
    path = os.path.join(PROOF_DIR, filename)
    with st.popover("Proof"):
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.caption(f"Screenshot not added yet — save it as `outputs/proof_screenshots/{filename}`.")

st.markdown("### Data Sources")

col1, col2 = st.columns(2)
with col1:
    r1a, r1b = st.columns([0.88, 0.12])
    with r1a:
        st.markdown("- **Named places** — OpenStreetMap")
    with r1b:
        proof_popover("04_canary_settlements_qgis.png", "Canary Islands OpenStreetMap settlement points in QGIS, attribute table open — named places (Santa Cruz de La Palma, San Telmo, El Muelle, etc.) used for the named-places exposure measure.")
    st.markdown("- **Mangrove Extent (1996/2010/2020)** — Global Mangrove Watch")
    r2a, r2b = st.columns([0.88, 0.12])
    with r2a:
        st.markdown("- **Coral Reef Extent** — WCMC / OpenStreetMap")
    with r2b:
        proof_popover("03_fiji_coral_qgis.png", "Fiji's cleaned coral reef layer in QGIS, attribute table open — 196 reef features (Albert Reef, Cakaulevu, etc.) — the same cleaning pass that caught the Maldives coral data-quality bug described below.")
    st.markdown("- **Coral Thermal Stress (1996–2020)** — NOAA Coral Reef Watch")
with col2:
    r3a, r3b = st.columns([0.88, 0.12])
    with r3a:
        st.markdown("- **Elevation** — DeltaDTM v1.1 bare-earth model (main), Copernicus DEM GLO-30 (comparison)")
    with r3b:
        proof_popover("02_seychelles_elevation_qgis.png", "Seychelles elevation (Copernicus DEM) in QGIS, pseudocolor-styled, with the Seychelles WDPA boundary overlaid — the surface model that the bare-earth DeltaDTM results are compared against.")
    r5a, r5b = st.columns([0.88, 0.12])
    with r5a:
        st.markdown("- **Population** — WorldPop 2020")
    with r5b:
        proof_popover("05_population_exposure_vscode.png", "population_weighted_exposure.py open in VS Code — computes what % of each island's population (not just settlements) lives at or below the 1m sea-level-rise threshold.")
    r4a, r4b = st.columns([0.88, 0.12])
    with r4a:
        st.markdown("- **Protected Areas** — World Database on Protected Areas (WDPA)")
    with r4b:
        proof_popover("01_canary_wdpa_qgis.png", "Canary Islands WDPA protected areas in QGIS over a satellite basemap — La Resbala, Las Lagunetas, Montes y Cumbre de Tenerife, etc. — the layer behind the coastal protected-area coverage.")

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

rga, rgb = st.columns([0.94, 0.06])
with rga:
    with st.expander("**Governance Ratio Sanity Check: Comparing Land to Marine EEZs**"):
        st.markdown("""
        An initial protected-area-to-land ratio for Seychelles came out to 1,005.69 — a nonsensical
        result caused by including the country's Exclusive Economic Zone (over a million km² of ocean)
        in the calculation. The metric is now the share of a 10 km coastal zone around each island
        that lies inside a protected area, with overlapping sites merged so no area is counted twice.
        """)
with rgb:
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    proof_popover("06_wdpa_coastal_buffer_vscode.png", "wdpa_coastal_buffer.py open in VS Code — the fix for the Seychelles 1,005.69 EEZ bug, restricting WDPA area to a 10km coastal buffer per island.")

with st.expander("**Filling a Data Gap: Lakshadweep's Population, Revisited**"):
    st.markdown("""
    Lakshadweep population data was initially unavailable, since the only access method found
    required downloading a population raster covering the entirety of India. A smaller, more
    targeted file — WorldPop's constrained, UN-adjusted 2020 India dataset (~470MB rather than
    several gigabytes) — was later identified, clipped down to Lakshadweep's boundary, and
    incorporated into a population-weighted exposure analysis alongside all four other islands.
    """)

st.markdown("---")

st.markdown("### Honest Limitations")

hl1, hl2 = st.columns([0.94, 0.06])
with hl1:
    st.warning(f"""
    **Small sample size.** Four island groups have a usable protected-area record (Lakshadweep has none in the
    WDPA extract). Across them, coastal protection and the compound score are unrelated (r = {G['r']:.2f},
    95% interval {G['lo']:.2f} to {G['hi']:.2f}), and removing Seychelles alone moves r to {G['loo_no_sey']:.2f}.
    With n = 4 this is a description of these islands, not a test that could generalise. The first version
    reported r = 0.965, p = 0.035; that came from double-counted overlapping sites and a land-area denominator.
    """)
with hl2:
    proof_popover("07_governance_correlation_vscode.png", "governance_correlation_test.py open in VS Code — the correlation (r, interval, leave-one-out) behind the descriptive H3 governance comparison.")

st.info("""
**Uneven data depth.** Canary Islands coral and mangrove data were confirmed genuinely absent —
geographically and ecologically explained by its subtropical, volcanic Atlantic setting outside
typical coral and mangrove habitat range — and documented transparently rather than substituted
or estimated. Lakshadweep population data, initially unavailable for the reason described above,
was later obtained and is now included in the population-weighted exposure analysis.
""")

_pop = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "population_weighted_exposure_by_source.csv"))
_cov = _pop[_pop["elevation_source"] == R["primary"]].set_index("island")["pct_pop_covered"]
st.error(f"""
**Elevation is an approximation, not a flood model.** Heights from {source_label(R['primary'])} are above the
EGM2008 geoid, treated as mean sea level; DeltaDTM's error against airborne lidar is about 0.4–0.5 m. Tides, surge
and waves are not modelled. Population with a usable elevation ranges from {_cov.min():.1f}% ({_cov.idxmin()}) to
{_cov.max():.1f}% ({_cov.idxmax()}); people on cells with no elevation are reported, not assumed safe.
""")

st.markdown("---")

dd1, dd2 = st.columns([0.94, 0.06])
with dd1:
    st.markdown("### Download the Data")
with dd2:
    st.markdown("<div style='margin-top: 1.6rem;'></div>", unsafe_allow_html=True)
    proof_popover("08_compound_vulnerability_score_vscode.png", "compound_vulnerability_score.py open in VS Code — the script that computes the compound score (people at or below 1 m + change in reef heat stress) and produces this CSV.")

try:
    df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "compound_vulnerability_scores.csv"))
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Compound Vulnerability Scores (CSV)", csv,
                        "double_jeopardy_vulnerability_scores.csv", "text/csv")
except FileNotFoundError:
    st.markdown("*(Data file not found — check path)*")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — The Vulnerability Spiral</p>",
    unsafe_allow_html=True,
)