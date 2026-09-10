import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
from styles import (
    apply_custom_style, page_header, lead,
    card, kicker, card_title, card_body, stat_card, nav_card,
    PALETTE,
)

st.set_page_config(
    page_title="GHOST INFRASTRUCTURE",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()

GITHUB_URL = "https://github.com/sakshimaske303-commits/GHOST_INFRASTRUCTURE"

page_header(
    "🏭", "GHOST INFRASTRUCTURE",
    "How 19th-Century Coal Geography Still Shapes Who Gets a \"15-Minute Life\" Today",
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(255, 242, 186, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin: 10px 0 18px 0;">
        <a href="https://eartharxiv.org/repository/view/14809/" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['bg_sidebar']}, {PALETTE['bg_main']});
                border: 2px solid {PALETTE['accent']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(255, 242, 186, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:#E4D28C; font-family:'Bitter',serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>PREPRINT ON EARTHARXIV</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Bitter',serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        Read the preprint
                    </div>
                </div>
            </div>
        </a>
        <a href="https://doi.org/10.5281/zenodo.21761320" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['bg_sidebar']}, {PALETTE['bg_main']});
                border: 2px solid {PALETTE['accent']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(255, 242, 186, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:#E4D28C; font-family:'Bitter',serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Bitter',serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.21761320
                    </div>
                </div>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    stat_card("Study City", "Bochum", "Ruhr Valley, Germany")
with col2:
    stat_card("Historical Sites", "17", "13 mines + 4 colonies")
with col3:
    stat_card("Network Nodes", "69,393", "OSMnx street network")
with col4:
    stat_card("15-Min Coverage", "85.8%", "of network nodes")

st.markdown("---")

card(
    kicker("Why This Matters")
    + card_body(
        "Urban planners often assume that former industrial zones are the neighborhoods most likely "
        "to be left behind — under-served, poorly connected, needing the most investment. This project "
        "tested that assumption directly, on real network data, and found the opposite: it's "
        "neighborhoods <em>further</em> from historical industrial cores that form genuine accessibility "
        "cold-spots today. Getting this backwards isn't academic — it's the difference between planning "
        "resources reaching the areas that actually need them and reinforcing an intuitive but wrong "
        "assumption about where \"neglect\" concentrates. And this isn't unique to Bochum: the raw effect "
        "and its spatial-clustering signature both independently replicate in Essen, a second Ruhr Valley "
        "city tested the same way — see the Robustness page for the full multi-city comparison, including "
        "the one result that does <em>not</em> cleanly replicate, reported honestly rather than left out.",
        large=True,
    ),
    dark=True,
)

st.markdown("---")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("<h3>What Is Ghost Infrastructure?</h3>", unsafe_allow_html=True)
    lead(
        "Bochum's modern shape was never designed for people — it was built around "
        "<strong>coal mines and steel works</strong>, with railways, roads, and worker-housing "
        "colonies (Zechensiedlungen) laid out to serve 19th-century industry, not human accessibility."
    )
    lead(
        "Coal mining ended in Bochum in 1974. This project asks: more than half a century later, "
        "does that historical industrial geography still leave a measurable imprint on which "
        "neighborhoods get a genuine <strong>\"15-minute city\"</strong> — walkable access to "
        "essential services — and which don't?"
    )

with col_right:
    card(
        kicker("The Twist")
        + card_body(
            "The hypothesis was that historical industrial sites would predict present-day "
            "<span class='gi-highlight'>neglect</span>. The data said the opposite: proximity to "
            "historical coal-mine and colony locations statistically predicts "
            "<span class='gi-highlight'>better</span> 15-minute accessibility today — verified "
            "against city-center proximity and corroborated by an independent spatial-clustering "
            "(Local Moran's I) analysis.",
            large=True,
        ),
        dark=True,
    )

st.markdown("---")

st.markdown("<h3>Three Findings</h3>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    card(
        kicker("Finding 1") + card_title("Reversed Effect")
        + card_body(
            "Low-accessibility zones are, on average, further from historical industrial sites — "
            "not closer, as the original hypothesis assumed (Cohen's d=0.589)."
        )
    )
with f2:
    card(
        kicker("Finding 2") + card_title("Confound-Controlled")
        + card_body(
            "Verified via logistic regression: the effect holds even after controlling for "
            "distance to the city center — it isn't just a center-proximity proxy."
        )
    )
with f3:
    card(
        kicker("Finding 3") + card_title("Spatially Clustered")
        + card_body(
            "A Local Moran's I analysis confirms low accessibility forms genuine, statistically "
            "significant cold-spot clusters — not random scatter — farther from historical sites."
        )
    )

st.markdown("---")

st.markdown("<h3>Explore the Research</h3>", unsafe_allow_html=True)

nav_items = [
    ("Study Design", "Bochum, methodology, why this city"),
    ("Theoretical Foundations", "How mining subsidence and legacy landform shaped today's accessibility"),
    ("Historical Geography", "13 mines, 4 worker colonies"),
    ("Accessibility Analysis", "The 15-minute network model"),
    ("The Finding", "Statistical test + confound + spatial clustering"),
    ("Explore Trends", "Live distance-threshold explorer"),
    ("Interactive Maps & Plots", "Live geospatial exploration plus the three headline charts"),
    ("Methodology & Data", "Sources, debugging journey, limitations"),
    ("Robustness: Thresholds & Essen", "10/20-min sensitivity + a second-city replication"),
]

cols = st.columns(3)
for i, (title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        nav_card(title, desc)

st.markdown("---")

st.markdown("<h3>Full Project Documentation</h3>", unsafe_allow_html=True)
lead("The complete research paper, project journal, and development log are available to download below.")

_all_docs = [
    {"label": "Executive Summary", "filename": "GI_Executive_Summary.pdf"},
    {"label": "Research Paper", "filename": "GI_Research_Paper.pdf"},
    {"label": "Development Log", "filename": "GI_Development_Log.pdf"},
]
_existing = [d for d in _all_docs if os.path.exists(os.path.join(BASE_DIR, "static", d["filename"]))]
_missing = [d for d in _all_docs if d not in _existing]

if _existing:
    _cols = st.columns(len(_existing))
    for _col, _d in zip(_cols, _existing):
        with _col:
            with open(os.path.join(BASE_DIR, "static", _d["filename"]), "rb") as _f:
                st.download_button(
                    label=f"⬇ {_d['label']}",
                    data=_f.read(),
                    file_name=_d["filename"],
                    mime="application/pdf",
                    use_container_width=True,
                )
for d in _missing:
    st.warning(f"{d['filename']} not found.")

st.markdown("---")

# ============================================================
# FOOTER — NAME + GITHUB LINK
# ============================================================
card(f"""
    <div style="text-align:center;">
        {kicker("Developed by")}
        <p style="font-family:'Bitter',serif; font-weight:900; font-size:2rem; margin:0 0 6px 0;">SAKSHI D. MASKE</p>
        <p style="font-weight:700; font-size:0.95rem; margin:0 0 16px 0;">Independent Geospatial Researcher</p>
        <a href="{GITHUB_URL}" target="_blank" class="gi-pill-btn">View on GitHub</a>
    </div>
""")
