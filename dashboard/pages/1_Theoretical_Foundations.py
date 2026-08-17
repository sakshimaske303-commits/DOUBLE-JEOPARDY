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
    "Why the Highest-Exposure Island Isn't Always the Highest-Risk Island</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# DIAGRAM
# ============================================================
IMG_PATH = os.path.join(ROOT_DIR, "outputs", "plots", "imgg1.png")
col_a, col_b, col_c = st.columns([1, 4, 1])
with col_b:
    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, use_container_width=True)
    else:
        st.warning("Diagram not found at outputs/plots/imgg1.png")
    st.markdown(
        f"<p style='text-align:center; color:{PALETTE['text_muted']}; font-size:0.85rem; margin-top:6px;'>"
        "🖼️ Conceptual diagram — visual aid only</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background: {PALETTE['card_bg']}; border: 1px solid rgba(34,211,238,0.25);
                    border-radius: 10px; padding: 14px 20px; margin-top: 6px;">
            <p style="color:{PALETTE['text_muted']}; font-size:0.85rem; font-style:italic; margin:0; text-align:center;">
                A visual aid I put together from my own fully-specified brief — every process, label, and
                physical relationship shown reflects my own understanding of coastal oceanography and
                reef ecology.
            </p>
        </div>
        """,
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
computed on this project's Physical Exposure page — the Maldives' 99.1% of settlements at risk
is a direct consequence of a nation built almost entirely at an elevation these combined
processes are steadily eroding.
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
# SECTION 3 — WHY RISK REVERSES
# ============================================================
st.markdown("### Why the Physics and the Biogeography Together Explain the Headline Finding")

st.markdown("""
This is exactly the mechanism behind Double Jeopardy's central, risk-reversing result. The
**Maldives** carries the highest physical sea-level-rise exposure of any island tested — a
straightforward consequence of the oceanographic drivers above acting on very low-lying atoll
terrain. Yet **Seychelles** emerges as the highest *overall*-risk island once ecosystem
degradation is factored in, because it recorded the most severe coral thermal-stress trend in the
sample (+0.68 °C-weeks) — its biogeographic buffer is degrading fastest, even though its raw
physical exposure is lower. Risk, in other words, is not simply a function of ocean physics —
it's the product of physical exposure *and* the biological state of the reef system standing
between that exposure and the shoreline, which is precisely the compound relationship this
project's vulnerability score was built to capture.
""")

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{PALETTE['text_muted']}; font-size:0.85rem;'>DOUBLE JEOPARDY — The Ocean Physics and Reef Biogeography Behind the Risk Score</p>",
    unsafe_allow_html=True,
)
