import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pct

R = load_results()
_P = R["primary"]

st.set_page_config(page_title="Ocean Physics & Reef Biogeography — DOUBLE JEOPARDY", page_icon="🌊", layout="wide")
apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 DOUBLE JEOPARDY: THE PHYSICS AND THE BIOGEOGRAPHY</h1>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align: center; color: {PALETTE['navy']}; font-weight: 400;'>"
    "How Sea Level Exposure and Coastal Ecosystems Interact</h3>",
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

st.markdown(f"""
where **α** is seawater's coefficient of thermal expansion. Separately, **land-ice melt (the
eustatic component)** — glaciers and ice sheets on land losing mass adds genuinely new water to
the ocean, rather than merely expanding what's already there. Both raise the level that the
Physical Exposure page measures against: on a bare-earth elevation model,
{pct(R['people'][('maldives', _P)])} of the Maldives' people and {pct(R['people'][('lakshadweep', _P)])}
of Lakshadweep's live on land at or below 1 m, against {pct(R['people'][('canary', _P)])} in the
volcanic, high-relief Canary Islands.
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

st.markdown(f"""
The two halves do not have to point the same way, and in this sample they mostly do not. The
**Maldives** has by far the largest share of people at or below 1 m ({pct(R['people'][('maldives', _P)])}),
but the smallest rise in reef heat stress of the four reef groups
(+{R['coral_change'][('maldives', 'reef_cells')]:.2f} °C-weeks between 1996–2000 and 2016–2020).
**Seychelles** shows the largest rise (+{R['coral_change'][('seychelles', 'reef_cells')]:.2f} °C-weeks) with far fewer
people at or below 1 m ({pct(R['people'][('seychelles', _P)])}). Which of them counts as "most vulnerable"
therefore depends on how the two halves are weighted, which is what the Compound Vulnerability page
shows. Risk is not a function of ocean physics alone: it depends on physical exposure *and* on the
state of the reef standing between that exposure and the shoreline.
""")

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{PALETTE['text_muted']}; font-size:0.85rem;'>DOUBLE JEOPARDY — The Ocean Physics and Reef Biogeography Behind the Risk Score</p>",
    unsafe_allow_html=True,
)
