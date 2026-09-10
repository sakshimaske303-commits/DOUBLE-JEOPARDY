import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, page_header, footer_caption, card, stat_card, card_body, PALETTE

apply_custom_style()

page_header("📊", "THE FINDING", "A Reversed Effect, Verified Against Its Most Obvious Confound")
st.markdown("---")

_checks = [
    "Full Network-Based Model (69,393 nodes, not straight-line radius)",
    "Most Obvious Confound Explicitly Tested (city-center proximity)",
    "Logistic Regression Confirms Independence",
    "Complementary Check (Local Moran's I, 999 permutations)",
    "Spatial-Dependence Bootstrap (network-block resampling, 95% CI excludes zero)",
    "Effect Size Reported, Not Just Significance (Cohen's d=0.589)",
    "Reversed-Hypothesis Result Reported Honestly",
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

st.markdown("<h3>Distance to Historical Sites: High vs. Low Accessibility</h3>", unsafe_allow_html=True)

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "distance_comparison_boxplot.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Boxplot image not found.")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    stat_card("Low-Accessibility Nodes", "1,984 m", "Average distance to nearest historical site (n=9,858)")
with col2:
    stat_card("High-Accessibility Nodes", "1,450 m", "Average distance to nearest historical site (n=59,535)")

st.markdown("---")

st.markdown("<h3>Statistical Confirmation</h3>", unsafe_allow_html=True)

card(card_body(
    "A Welch's t-test comparing the two groups produced <strong>t=42.887, p&lt;0.00001</strong> "
    "(Cohen's d=0.589, a medium-to-large effect) — a highly significant, practically meaningful "
    "relationship, but in the opposite direction to the original hypothesis. Proximity to "
    "historical industrial sites predicts <strong>better</strong> present-day accessibility, "
    "not worse.",
    large=True,
))

st.markdown("---")

st.markdown("<h3>Checking the Obvious Confound: City Center</h3>", unsafe_allow_html=True)

card(
    card_body(
        "Before accepting this result, the most obvious alternative explanation was tested "
        "directly: historical sites might simply cluster near the city center, which "
        "independently predicts better accessibility regardless of any genuine historical effect."
    )
    + "<div style='height:12px;'></div>"
    + card_body(
        "Correlation between distance-to-historical-site and distance-to-city-center: "
        "<strong>r = 0.063</strong> — no meaningful correlation, so the two are not proxies for one "
        "another. A logistic regression confirms the historical-site effect remains significant "
        "(coefficient = -0.0005, p &lt; 0.001) even after controlling for city-center distance.",
        large=True,
    )
)

st.markdown("---")

st.markdown("<h3>Complementary Check: Local Moran's I Spatial Clustering</h3>", unsafe_allow_html=True)

card(
    card_body(
        "The t-test above shows distance to historical sites <em>differs</em> between accessibility "
        "groups. A separate question is whether low accessibility is spatially <em>clustered</em> — "
        "the specific test this project's own Objectives named. A Local Moran's I analysis "
        "(KNN k=8, 999 permutations) answers this directly."
    )
    + "<div style='height:12px;'></div>"
    + card_body(
        "<strong>97.1%</strong> of all low-accessibility nodes fall inside a statistically "
        "significant Low-Low (\"cold-spot\") spatial cluster — confirming low accessibility is not "
        "randomly scattered, but forms genuine, spatially contiguous zones that are measurably "
        "farther from historical industrial sites (1,992 m vs. 1,447 m for non-clustered nodes).",
        large=True,
    )
)

lisa_image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "lisa_cluster_map.png")
if os.path.exists(lisa_image_path):
    st.image(lisa_image_path, use_container_width=True, caption="Local Moran's I cluster map — significant Low-Low cold-spot clusters in blue")

st.markdown("---")

st.markdown("<h3>Spatial-Dependence Check: Network-Block Bootstrap</h3>", unsafe_allow_html=True)

card(
    card_body(
        "The 69,393 street nodes above are not independent observations — a node right next to "
        "another one on the same street is obviously correlated with it. To test whether that "
        "affects the finding, the street network was split into ~2,600 contiguous blocks "
        "(~500 connected nodes each) and whole blocks were resampled with replacement 999 times, "
        "refitting the same statistics each time."
    )
    + "<div style='height:12px;'></div>"
    + card_body(
        "The observed distance difference (534.25 m) came back with a <strong>95% confidence "
        "interval of [247.24 m, 873.73 m]</strong> — nowhere close to zero. The finding holds up "
        "even when the network's own connected structure, not individual nodes, is treated as the "
        "unit of resampling.",
        large=True,
    )
)

st.markdown("---")

st.markdown("<h3>Interpretation</h3>", unsafe_allow_html=True)

card(card_body(
    "19th-century industrial cores were built dense, by necessity — around the mines and "
    "colonies where workers actually lived. That density appears to persist as present-day "
    "street connectivity and service coverage, decades after the mines closed. This is a "
    "<strong>\"path dependency of centrality\"</strong> rather than the originally hypothesized "
    "\"path dependency of neglect.\" Genuine accessibility gaps concentrate further from, "
    "not closer to, the historical industrial core.",
    large=True,
), dark=True)

st.markdown("---")

st.markdown("<h3>Does This Hold Beyond Bochum and Beyond 15 Minutes?</h3>", unsafe_allow_html=True)
card(card_body(
    "This finding was tested for robustness two ways: across three walking-time thresholds "
    "(10/15/20-minute — it holds and strengthens at every one), and via an independent full-methodology "
    "replication in Essen, a second Ruhr Valley city. The raw effect and the spatial-clustering result "
    "both replicate there; the confound-independence result does not, and that mixed result is reported "
    "in full — see the <strong>Robustness: Thresholds &amp; Essen</strong> page.",
    large=True,
))

st.markdown("---")
footer_caption("GHOST INFRASTRUCTURE — Welch's t-test + logistic regression confound verification + Local Moran's I spatial clustering")
