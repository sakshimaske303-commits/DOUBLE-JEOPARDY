import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE

st.set_page_config(page_title="Ocean Physics & Reef Biogeography — DOUBLE JEOPARDY", page_icon="🌊", layout="wide")
apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 DOUBLE JEOPARDY: THE PHYSICS AND THE BIOGEOGRAPHY</h1>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align: center; color: {PALETTE['navy']}; font-weight: 400;'>"
    "Why Physical Exposure Alone Isn't the Whole Risk Picture</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# DIAGRAM
# ============================================================
IMG_PATH = os.path.join(ROOT_DIR, "outputs", "plots", "imgg1.png")
col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, use_container_width=True)
    else:
        st.warning("Diagram not found at outputs/plots/imgg1.png")
    st.markdown(
        f"<p style='text-align:center; color:{PALETTE['text_muted']}; font-size:0.85rem; margin-top:6px;'>"
        "Sea-level-rise physics schematic — thermal expansion and land-ice melt pathways.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================
# SECTION 1 — TWO PHYSICAL DRIVERS OF SEA-LEVEL RISE
# ============================================================
st.markdown("### Sea-Level Rise Has Two Distinct Physical Causes")

st.markdown("""
The exposure half of Double Jeopardy's risk score is driven by global sea-level rise, which is
not one process but the sum of two physically independent ones. **Thermal expansion (the steric
component)** — as ocean water warms, it expands in volume, since the volume of a fluid increases
with temperature at constant mass:
""")

st.latex(r"\frac{\Delta V}{V} = \alpha \, \Delta T")

st.markdown("""
where **α** is seawater's coefficient of thermal expansion. Separately, **land-ice melt (the
eustatic component)** — glaciers and ice sheets on land losing mass adds genuinely new water to
the ocean, rather than merely expanding what's already there. Both mechanisms are captured
together in the diagram above, and both contribute to the settlement-level exposure scores
computed on this project's Physical Exposure page — **Seychelles'** 78.3% of settlements at risk
is the highest in this sample, a direct consequence of a nation with a substantial share of its
settlements sitting at an elevation these combined processes are steadily eroding.
""")

st.markdown("---")

# ============================================================
# SECTION 2 — CORAL REEFS AS BIOGEOGRAPHIC BUFFERS
# ============================================================
st.markdown("### A Reef Is a Living Coastal Defense — Until It Isn't")

st.markdown("""
Coral reefs have a distinct **biogeographic zonation** — fore-reef, reef crest, and lagoon —
each hosting different coral and associated species communities adapted to that zone's specific
wave-energy and light conditions. That structural complexity is what makes a healthy reef crest
so effective at **dissipating incoming wave energy** before it ever reaches shore, visibly
different from the smoother wave pattern reaching a bleached, structurally degraded reef in the
diagram above. When sustained thermal stress causes coral bleaching — the loss of the
symbiotic algae that give coral its color and much of its energy supply — that living
wave-buffering structure degrades, and the shoreline behind it loses a natural defense it
previously had.
""")

st.markdown("---")

# ============================================================
# SECTION 3 — WHY BOTH HALVES OF THE SCORE MATTER
# ============================================================
st.markdown("### Why the Physics and the Biogeography Together Explain the Headline Finding")

st.markdown("""
This is exactly the mechanism behind Double Jeopardy's central finding. **Seychelles** carries the
highest physical sea-level-rise exposure of any island tested (78.3% of settlements at or below the
1-meter threshold) — a straightforward consequence of its settlement pattern concentrating in
low-lying coastal areas despite its granite interior. It also recorded the most severe coral
thermal-stress trend in the sample (+0.68 °C-weeks), meaning its biogeographic buffer is degrading
fastest at the same time its physical exposure is highest — a genuine double jeopardy, where both
halves of the risk equation point the same way rather than pulling against each other. Risk, in
other words, is not simply a function of ocean physics — it's the product of physical exposure
*and* the biological state of the reef system standing between that exposure and the shoreline,
which is precisely the compound relationship this project's vulnerability score was built to
capture. (An earlier version of this analysis, based on a DEM data-quality artifact in the
Maldives' and Lakshadweep's elevation files, showed the Maldives as the highest-exposure island;
the corrected figure is 14.5% — see the Research Paper's Limitations section.)
""")

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{PALETTE['text_muted']}; font-size:0.85rem;'>DOUBLE JEOPARDY — The Ocean Physics and Reef Biogeography Behind the Risk Score</p>",
    unsafe_allow_html=True,
)
