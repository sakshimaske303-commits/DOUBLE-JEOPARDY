import streamlit as st
import streamlit.components.v1 as components
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

# Folder where the 5 island locator maps live.
MAPS_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots", "locator_maps")


def find_locator_map(maps_dir, slug):
    path = os.path.join(maps_dir, f"{slug}.html")
    return path if os.path.exists(path) else None


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
    (col1, "Maldives", "Indian Ocean", "Low-lying coral atolls, moderate SLR exposure", "maldives"),
    (col2, "Lakshadweep", "Indian Ocean", "Small coral archipelago, India", "lakshadweep"),
    (col3, "Seychelles", "Western Indian Ocean", "Granite islands, highest compound risk", "seychelles"),
    (col4, "Fiji", "South Pacific", "Volcanic islands, largest cyclone record", "fiji"),
    (col5, "Canary Islands", "Eastern Atlantic", "Volcanic, lowest compound risk", "canary"),
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

# Stacked layout, native aspect ratio -- a side-by-side thumbnail grid
# cropped several of these maps.
st.markdown("### Island Locator Maps")

for i, (col, name, basin, desc, slug) in enumerate(islands_info):
    map_path = find_locator_map(MAPS_DIR, slug)
    st.markdown(f"<p style='text-align:center; color:{PALETTE['navy']}; font-weight:700; font-size:1.05rem; margin-bottom:10px;'>{name}</p>", unsafe_allow_html=True)
    if map_path:
        with open(map_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        left, center, right = st.columns([1, 3, 1])
        with center:
            components.html(map_html, height=420)
    else:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border: 2px dashed rgba(150,150,150,0.4);
                    border-radius: 12px; padding: 40px 10px; text-align: center;
                    min-height: 200px; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;">
            <p style="color: {PALETTE['text_muted']}; font-size: 0.9rem; margin: 0;">
                Map will be displayed here
            </p>
        </div>
        """, unsafe_allow_html=True)
    if i < len(islands_info) - 1:
        st.markdown("")

st.markdown("---")

st.markdown("### Three Hypotheses, Tested Independently")

col1, col2, col3 = st.columns(3)
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
with col3:
    st.info("""
    **H3 — Governance Alignment**

    Islands with higher compound vulnerability scores will show correspondingly
    higher formal protected-area coverage, consistent with risk-responsive
    governance.
    """)

st.markdown("---")

st.markdown("### Methodology at a Glance")

st.markdown("""
1. **Physical Exposure** — Share of people (WorldPop 2020) living at or below 1 m on a bare-earth
   elevation model (DeltaDTM v1.1), with Copernicus GLO-30 as a comparison and the share of
   OpenStreetMap named places as a second measure; 0.5 m and 1.5 m as sensitivity checks.

2. **Ecosystem Trends** — Mangrove extent at three time points (1996, 2010, 2020); reef heat
   stress as mean Degree Heating Weeks over all mapped reef, 1996–2020, compared by period
   and tested with a seasonal Mann-Kendall test corrected for serial correlation.

3. **Compound Vulnerability Score** — Exposure and change in reef heat stress, each scaled 0–1
   and averaged, with the weighting swept from 0 to 100%. A descriptive ranking within this sample.

4. **Governance Alignment** — Share of the 10 km coastal zone that is protected, compared with
   the compound score across the four island groups with a WDPA record. Descriptive only (n = 4).

5. **Built-up Change (supplementary)** — Sentinel-2 NDBI change on land, 2016–2024, including
   land within 1 km of mangroves and reefs.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — The Vulnerability Spiral</p>",
    unsafe_allow_html=True,
)