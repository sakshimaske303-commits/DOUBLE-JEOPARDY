import streamlit as st
import streamlit.components.v1 as components
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🗺️ INTERACTIVE MAPS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Explore the Geospatial Data Live</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

MAP_SERVER_BASE = "/app/static"

# ============ SLR EXPOSURE ============
SLR_DATA = {
    "Maldives": {"folder": "maldives_slr_exposure_webmap",
                 "observation": "99.1% of settlements are at or below 1m elevation — the highest exposure of any island in this study."},
    "Lakshadweep": {"folder": "lakshadweep_slr_exposure_webmap",
                     "observation": "77.8% of settlements are at risk, despite the smallest sample size (36 settlements)."},
    "Seychelles": {"folder": "seychelles_slr_exposure_webmap",
                    "observation": "78.3% of settlements are at risk — yet Seychelles emerges as the highest overall-risk island once ecosystem degradation is factored in."},
    "Fiji": {"folder": "fiji_slr_exposure_webmap",
             "observation": "Only 32.0% of settlements are at risk — Fiji's volcanic terrain provides substantially more elevation buffer."},
    "Canary Islands": {"folder": "canary_slr_exposure_webmap",
                        "observation": "Just 12.1% of settlements are at risk — the lowest of all five islands."},
}

st.markdown("### 📉 Sea-Level-Rise Exposure Maps")

st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
    <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">MAP LEGEND</p>
    <p style="color: {PALETTE['text_dark']}; font-size: 0.9rem; margin: 0;">
        🟥 Red — At/Below 1m Elevation (SLR Risk) &nbsp;|&nbsp;
        🟨 Yellow — Above 1m Elevation (Safe)
    </p>
</div>
""", unsafe_allow_html=True)

selected_island_slr = st.selectbox("🌍 Select Island", list(SLR_DATA.keys()), key="slr_select")
info = SLR_DATA[selected_island_slr]
components.iframe(src=f"{MAP_SERVER_BASE}/{info['folder']}/index.html", height=550, scrolling=True)
st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border-left: 5px solid {PALETTE['cyan']};
            border-radius: 10px; padding: 14px; margin-top: 12px;">
    <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">Key Observation</p>
    <p style="color: {PALETTE['text_dark']}; margin: 0; font-size: 0.95rem;">{info['observation']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============ ECOSYSTEM BUFFER ============
ECO_DATA = {
    "Maldives": {
        "folder": "maldives_ecosystem_buffer_webmap",
        "observation": "All four ecosystem layers present. Maldives shows extensive mangrove and coral coverage alongside 93 WDPA-protected areas.",
        "layers": ["mangroves", "coral", "wdpa", "boundary"],
    },
    "Fiji": {
        "folder": "fiji_ecosystem_buffer_webmap",
        "observation": "All four ecosystem layers present. Fiji shows the largest mangrove extent (488 km²) and 126 WDPA-protected areas of any island tested — consistent with its confirmed ecosystem stability.",
        "layers": ["mangroves", "coral", "wdpa", "boundary"],
    },
    "Seychelles": {
        "folder": "seychelles_ecosystem_buffer_webmap",
        "observation": "All four ecosystem layers present. Despite this coverage, Seychelles shows the most severe coral thermal-stress trend and highest compound vulnerability of any island.",
        "layers": ["mangroves", "coral", "wdpa", "boundary"],
    },
    "Lakshadweep": {
        "folder": "lakshadweep_ecosystem_buffer_webmap",
        "observation": "Only coral reefs are mapped here — mangroves and formal WDPA protection are both genuinely absent, a finding independently confirmed across multiple data sources.",
        "layers": ["coral", "boundary"],
    },
    "Canary Islands": {
        "folder": "canary_ecosystem_buffer_webmap",
        "observation": "Only protected areas are mapped here — mangroves and coral reefs are genuinely absent, consistent with the Canary Islands' subtropical, volcanic Atlantic geography.",
        "layers": ["wdpa", "boundary"],
    },
}

LEGEND_ITEMS = {
    "mangroves": ("🩷", "Pink", "Mangrove Forests (2020)"),
    "coral": ("🟨", "Bright Yellow", "Coral Reefs"),
    "wdpa": ("🩵", "Sky Blue Outline", "Protected Areas (WDPA)"),
    "boundary": ("🟩", "Green Outline", "Island Boundary"),
}

st.markdown("### 🌿 Ecosystem Buffer Overview Maps")

selected_island_eco = st.selectbox("🌍 Select Island", list(ECO_DATA.keys()), key="eco_select")
info2 = ECO_DATA[selected_island_eco]

present_layers = info2["layers"]
legend_html = " &nbsp;|&nbsp; ".join(
    f"{LEGEND_ITEMS[layer][0]} {LEGEND_ITEMS[layer][1]} — {LEGEND_ITEMS[layer][2]}"
    for layer in present_layers
)

st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
    <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">MAP LEGEND — {selected_island_eco}</p>
    <p style="color: {PALETTE['text_dark']}; font-size: 0.9rem; margin: 0;">{legend_html}</p>
</div>
""", unsafe_allow_html=True)

components.iframe(
    src=f"{MAP_SERVER_BASE}/{info2['folder']}/index.html",
    height=550,
    scrolling=True,
)

st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border-left: 5px solid {PALETTE['mint']};
            border-radius: 10px; padding: 14px; margin-top: 12px;">
    <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">Key Observation</p>
    <p style="color: {PALETTE['text_dark']}; margin: 0; font-size: 0.95rem;">{info2['observation']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============ MANGROVE TREND ============
MANGROVE_TREND_IMAGES = {
    "Fiji": "fiji_mangrove_trend.png",
    "Seychelles": "seychelles_mangrove_trend.png",
    "Maldives": "maldives_mangrove_trend.png",
}

st.markdown("### 🌳 Mangrove Extent Trend Maps (1996 / 2010 / 2020)")

selected_island_mangrove = st.selectbox("🌍 Select Island", list(MANGROVE_TREND_IMAGES.keys()), key="mangrove_select")
image_path = os.path.join(PROJECT_ROOT, "dashboard", "static", MANGROVE_TREND_IMAGES[selected_island_mangrove])
st.image(image_path, use_container_width=True)

st.markdown(f"""
<div style="background: {PALETTE['card_bg']}; border-left: 5px solid {PALETTE['mint']};
            border-radius: 10px; padding: 10px 14px; margin-top: 10px;">
    <p style="color: {PALETTE['text_muted']}; margin: 0; font-size: 0.82rem; font-style: italic;">
        Note: This map is shown as a static image rather than an interactive layer due to a QGIS2Web export limitation with historical polygon datasets.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Maps built in QGIS, exported via QGIS2Web</p>",
    unsafe_allow_html=True,
)