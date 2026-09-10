import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, page_header, footer_caption, card, kicker, card_title, card_body, stat_card, PALETTE

apply_custom_style()

page_header("🧪", "ROBUSTNESS: THRESHOLDS & A SECOND CITY", "Does the Finding Hold Beyond One City and One Threshold?")
st.markdown("---")

_checks = [
    "10-min and 20-min thresholds tested (not only 15-min)",
    "Full methodology independently replicated in Essen",
    "Mixed replication reported in full — nothing suppressed",
    "Two competing explanations tested, not just asserted",
]
_badges = "".join(
    f"""<span style="display:inline-flex; align-items:center; gap:6px; background:rgba(255,242,186,0.10);
        border:1px solid rgba(255,242,186,0.35); border-radius:20px; padding:6px 14px; margin:4px;
        font-size:0.82rem; color:{PALETTE['text_primary']}; font-weight:600;">
        <span style="color:{PALETTE['accent']}; font-weight:900;">✓</span>{c}</span>"""
    for c in _checks
)
st.markdown(
    f"""
    <p style="color:{PALETTE['accent']}; text-transform:uppercase; letter-spacing:1.5px;
              font-weight:700; font-size:0.85rem; margin-bottom:6px;">Robustness At a Glance</p>
    <div style="display:flex; flex-wrap:wrap; margin-bottom: 6px;">{_badges}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("<h3>Part 1 — Is 15 Minutes a Special Threshold?</h3>", unsafe_allow_html=True)
card(card_body(
    "The headline finding used a 15-minute (1,125m) walking threshold. To test whether this specific "
    "choice was doing the work, the full pipeline was re-run at a stricter <strong>10-minute (750m)</strong> "
    "and a more permissive <strong>20-minute (1,500m)</strong> threshold, reusing Bochum's already-downloaded "
    "network — no new data needed.",
    large=True,
))

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "threshold_sensitivity_comparison.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Threshold sensitivity plot not found.")

col1, col2, col3 = st.columns(3)
with col1:
    stat_card("10-Minute Threshold", "d = 0.413", "t=47.06, p<0.00001")
with col2:
    stat_card("15-Minute (Original)", "d = 0.589", "t=42.89, p<0.00001")
with col3:
    stat_card("20-Minute Threshold", "d = 0.661", "t=32.15, p<0.00001")

card(card_body(
    "The reversed relationship holds at every threshold tested — and the effect size actually "
    "<strong>grows</strong> as the threshold widens. This is not a 15-minute-specific artifact.",
    large=True,
), dark=True)

st.markdown("---")

st.markdown("<h3>Part 2 — Does It Hold in a Second City?</h3>", unsafe_allow_html=True)
card(card_body(
    "The identical methodology (historical-site digitization, network accessibility model, Welch's "
    "t-test, city-center confound check, Local Moran's I) was independently replicated in "
    "<strong>Essen</strong> — a second Ruhr Valley city, 15km northeast of Bochum, sharing the same "
    "19th-century coal-mining industrial history. 4 major mines and 4 worker colonies were digitized "
    "from KuLaDig (NRW's state heritage-GIS database) and Wikipedia; Essen's 72,027-node street "
    "network was acquired via OSMnx.",
    large=True,
))

st.markdown("<h4 style='color:#FFF2BA; margin-top: 1.2rem;'>Essen's Study Area &amp; Historical Geography</h4>", unsafe_allow_html=True)
map_col1, map_col2 = st.columns(2)
with map_col1:
    p = os.path.join(PROJECT_ROOT, "outputs", "plots", "study_area_essen.png")
    if os.path.exists(p):
        st.image(p, use_container_width=True, caption="Study area — Essen (directly comparable to Bochum's study-area map)")
with map_col2:
    p = os.path.join(PROJECT_ROOT, "outputs", "plots", "essen_historical_geography.png")
    if os.path.exists(p):
        st.image(p, use_container_width=True, caption="4 coal mines + 4 worker colonies digitized for Essen")

map_col3, map_col4 = st.columns(2)
with map_col3:
    p = os.path.join(PROJECT_ROOT, "outputs", "plots", "essen_ghost_infrastructure_overlay.png")
    if os.path.exists(p):
        st.image(p, use_container_width=True, caption="Historical sites vs. present-day 15-min accessibility — Essen")
with map_col4:
    p = os.path.join(PROJECT_ROOT, "outputs", "plots", "essen_distance_comparison_boxplot.png")
    if os.path.exists(p):
        st.image(p, use_container_width=True, caption="Distance-to-historical-site by accessibility group — Essen")

st.markdown("<h4 style='color:#FFF2BA; margin-top: 1.2rem;'>Side-by-Side Statistical Comparison</h4>", unsafe_allow_html=True)
image_path2 = os.path.join(PROJECT_ROOT, "outputs", "plots", "bochum_essen_comparison.png")
if os.path.exists(image_path2):
    st.image(image_path2, use_container_width=True)
else:
    st.warning("Bochum-Essen comparison plot not found.")

st.markdown("<h4 style='color:#FFF2BA; margin-top: 1.2rem;'>What replicated</h4>", unsafe_allow_html=True)
rep1, rep2 = st.columns(2)
with rep1:
    card(
        kicker("Raw Reversed Effect") + card_title("Replicates ✓")
        + card_body("Low-access nodes further from historical sites in both cities. Bochum d=0.589, Essen d=0.338 — smaller, but same direction, still highly significant (t=24.731, p<0.00001).")
    )
with rep2:
    card(
        kicker("Spatial Clustering (LISA)") + card_title("Replicates ✓")
        + card_body("95.5% of Essen's low-access nodes fall in significant cold-spot clusters, almost matching Bochum's 97.1%. Zero significant hot-spot clusters in either city.")
    )

st.markdown("<h4 style='color:#FFF2BA; margin-top: 1.2rem;'>What did NOT replicate</h4>", unsafe_allow_html=True)
card(card_body(
    "The confound-independence result. In Bochum, distance-to-historical-site and distance-to-city-center "
    "were nearly uncorrelated (r=0.063) — showing no meaningful correlation. In Essen, they're moderately "
    "correlated (<strong>r=0.405</strong>). Once both are entered into a logistic regression together, "
    "the historical-site coefficient's <strong>sign reverses</strong> in Essen — meaning the raw Essen effect "
    "is substantially entangled with city-center proximity, not independent of it the way Bochum's is.",
    large=True,
), dark=True)

image_path3 = os.path.join(PROJECT_ROOT, "outputs", "plots", "essen_lisa_cluster_map.png")
if os.path.exists(image_path3):
    st.image(image_path3, use_container_width=True, caption="Local Moran's I cluster map — Essen (directly comparable to the Bochum map on 'The Finding' page)")

st.markdown("---")

st.markdown("<h3>Why Report a Mixed Result Instead of Only the Good Part?</h3>", unsafe_allow_html=True)
card(card_body(
    "Two explanations for the confound discrepancy were tested rather than picked for convenience. "
    "<strong>(1) Genuine city difference:</strong> Essen's historical coal-mining core may simply sit "
    "closer to its present-day city center than Bochum's more dispersed sites do — a real fact about "
    "each city's own industrial history. <strong>(2) Sample-size artifact:</strong> Essen's dataset "
    "(8 sites) is much smaller relative to its own historical mining register than Bochum's (17 sites) "
    "is to Bochum's — with fewer reference points, 'distance to nearest site' can start to covary with "
    "'distance from center' just from reduced spatial coverage, independent of any real effect. "
    "Expanding an earlier 6-site Essen dataset to the current 8 sites reduced the correlation from "
    "r=0.475 to r=0.405 — evidence consistent with explanation (2) being at least a partial contributor, "
    "though it doesn't rule out explanation (1) either. Both possibilities are documented, and expanding "
    "the Essen dataset further toward Bochum's scale is named as Future Work rather than forced to a "
    "conclusion this round.",
    large=True,
))

st.markdown("---")

st.markdown("<h3>Bottom Line</h3>", unsafe_allow_html=True)
card(card_body(
    "The underlying <strong>\"path dependency of centrality\"</strong> mechanism — historical industrial "
    "density leaving a durable connectivity legacy, corroborated by independent spatial clustering — "
    "appears to generalize across at least two Ruhr Valley cities. The stronger, narrower claim that this "
    "effect is statistically independent of city-center proximity is, on current two-city evidence, a "
    "Bochum-specific finding rather than a universal one. Both results are reported here in full.",
    large=True,
), dark=True)

st.markdown("---")
footer_caption("GHOST INFRASTRUCTURE — Threshold Sensitivity + Multi-City Replication (Essen)")
