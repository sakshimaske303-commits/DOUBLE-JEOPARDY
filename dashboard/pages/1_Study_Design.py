import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

# Folder where the 5 island locator maps live.
MAPS_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")


def find_map_image(maps_dir, slug):
    """Looks for the locator map under several possible filename patterns.
    Images saved from a browser/Google don't always keep a clean extension —
    e.g. a file can be named 'maldives.png' but actually be a JPEG, or get
    saved as 'maldives.png.jpeg'. This checks the common variants so the map
    still shows up regardless of exactly how it was saved."""
    candidates = [
        f"{slug}.png", f"{slug}.jpg", f"{slug}.jpeg",
        f"{slug}.png.jpeg", f"{slug}.png.jpg",
        f"{slug}.PNG", f"{slug}.JPG", f"{slug}.JPEG",
    ]
    for name in candidates:
        path = os.path.join(maps_dir, name)
        if os.path.exists(path):
            return path
    return None


st.markdown("<h1 style='text-align: center;'>🏝️ STUDY DESIGN</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #2d6a4f; font-weight: 400;'>Five Islands, Three Ocean Basins, One Question</h3>",
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("""
### The Research Question

Does physical sea-level-rise exposure combine with ecosystem buffer degradation to produce
compounding settlement-level vulnerability — and does this operate uniformly across ecosystem
types, or does it depend on which specific ecosystem is degrading?
""")

st.markdown("---")

st.markdown("### The Five Islands")

col1, col2, col3, col4, col5 = st.columns(5)

islands_info = [
    (col1, "🇲🇻 Maldives", "Indian Ocean", "Low-lying coral atolls, extreme SLR exposure", "maldives"),
    (col2, "🇮🇳 Lakshadweep", "Indian Ocean", "Small coral archipelago, India", "lakshadweep"),
    (col3, "🇸🇨 Seychelles", "Western Indian Ocean", "Granite islands, highest compound risk", "seychelles"),
    (col4, "🇫🇯 Fiji", "South Pacific", "Volcanic islands, largest cyclone record", "fiji"),
    (col5, "🇮🇨 Canary Islands", "Eastern Atlantic", "Volcanic, lowest compound risk", "canary"),
]

for col, name, basin, desc, slug in islands_info:
    with col:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px 12px; text-align: center; min-height: 220px; border: 1px solid rgba(0,180,216,0.2); display: flex; flex-direction: column; justify-content: flex-start;">
            <h4 style="color: {PALETTE['navy']}; margin-bottom: 10px; font-size: 1rem;">{name}</h4>
            <p style="color: {PALETTE['mint']}; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; margin-bottom: 10px;">{basin}</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.82rem; line-height: 1.4; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# ISLAND LOCATOR MAPS — shown one below another, each at a large,
# uncropped size (native aspect ratio preserved). A uniform side-by-side
# thumbnail grid was tried first but forced every map to the same box,
# cropping content out of several of them — this stacked layout avoids
# that entirely.
# ============================================================
st.markdown("### Island Locator Maps")

for i, (col, name, basin, desc, slug) in enumerate(islands_info):
    image_path = find_map_image(MAPS_DIR, slug)
    st.markdown(f"<p style='text-align:center; color:{PALETTE['navy']}; font-weight:700; font-size:1.05rem; margin-bottom:10px;'>{name}</p>", unsafe_allow_html=True)
    if image_path:
        left, center, right = st.columns([1, 3, 1])
        with center:
            st.image(image_path, use_container_width=True)
    else:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border: 2px dashed rgba(150,150,150,0.4);
                    border-radius: 12px; padding: 40px 10px; text-align: center;
                    min-height: 200px; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;">
            <p style="color: {PALETTE['text_muted']}; font-size: 0.9rem; margin: 0;">
                Image will be displayed here
            </p>
        </div>
        """, unsafe_allow_html=True)
    if i < len(islands_info) - 1:
        st.markdown("")

st.markdown("---")

st.markdown("### Two Hypotheses, Tested Independently")

col1, col2 = st.columns(2)
with col1:
    st.info("""
    **H1 — Coral Pathway**

    Coral reef ecosystems will show a statistically detectable increase in thermal
    bleaching stress over a multi-decadal period (1996–2020), more pronounced in
    islands with higher physical SLR exposure.
    """)
with col2:
    st.info("""
    **H2 — Mangrove Pathway**

    Mangrove ecosystems will show a statistically detectable decline in spatial
    extent over the same period, contributing an independent compounding pathway
    alongside coral degradation.
    """)

st.markdown("---")

st.markdown("### Methodology at a Glance")

st.markdown("""
1. **Physical Exposure** — Elevation and slope data intersected with settlement locations,
   identifying the proportion of settlements below a 1-meter sea-level-rise threshold,
   computed on both a settlement-count and a population-weighted basis.

2. **Ecosystem Trends** — Mangrove extent tracked across 3 independent time points
   (1996, 2010, 2020); coral condition tracked via 24 years of continuous thermal stress
   data (1996–2020), tested with both a period-comparison method and a formal Mann-Kendall
   trend test.

3. **Compound Vulnerability Score** — Physical exposure and ecosystem degradation combined
   into a single, normalized, cross-island comparable score, with weighting sensitivity
   tested across the full 0–100% range.

4. **Governance Alignment** — Formal protected-area coverage tested against the compound
   vulnerability score, to assess whether conservation policy is evidence-responsive.

5. **Settlement Encroachment** — Satellite-derived built-up area change (2016–2024) tested
   for concentration within or adjacent to ecosystem buffer zones.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — The Vulnerability Spiral</p>",
    unsafe_allow_html=True,
)