import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from styles import apply_custom_style, PALETTE

st.set_page_config(
    page_title="DOUBLE JEOPARDY",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 DOUBLE JEOPARDY</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #2d6a4f; font-weight: 400; margin-top: -10px;'>"
    "The Vulnerability Spiral — Compound Climate Risk Across Five Island Nations</h3>",
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("ISLANDS", "5", "3 Ocean Basins")
with col2:
    st.metric("DATASETS", "10+", "Multi-source")
with col3:
    st.metric("TIME SPAN", "1996–2024", "28 years")
with col4:
    st.metric("HIGHEST RISK", "Seychelles", "Score: 0.880")

st.markdown("---")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is Double Jeopardy?

    Small island nations face a **compounding vulnerability** to climate change — high 
    physical exposure to sea-level rise, layered with **degrading natural coastal defenses**: 
    mangroves and coral reefs that have historically buffered these islands from erosion 
    and storm damage.

    This project independently tests whether that compounding risk is real, and whether 
    it affects every ecosystem type equally. Rather than assuming mangroves and coral reefs 
    degrade together, each is tested independently across five island nations spanning 
    three ocean basins.
    """)

with col_right:
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {PALETTE['card_bg']}, #e8f4f8);
                    border-left: 5px solid {PALETTE['cyan']}; border-radius: 12px;
                    padding: 22px; height: 100%;">
            <p style="color:{PALETTE['navy']}; text-transform:uppercase; font-size:0.75rem;
                      letter-spacing:1.5px; font-weight:700; margin-bottom:10px;">Core Finding</p>
            <p style="color:{PALETTE['text_dark']}; font-size:0.95rem; line-height:1.6; margin:0;">
                Physical exposure alone doesn't tell the whole story. The <b>Maldives</b> has the 
                highest sea-level-rise exposure of any island tested (99.1% of settlements at risk) — 
                yet <b>Seychelles</b> emerges as the highest overall-risk island once ecosystem 
                degradation is factored in, driven by the most severe coral thermal-stress 
                trend recorded across the sample.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

st.markdown("### Three Hypotheses, Three Outcomes")

h1, h2, h3 = st.columns(3)

with h1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fff0ee, #ffe5e0); border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['risk']}; min-height: 200px;">
        <p style="color: {PALETTE['risk']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">✅ H1 — Supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Coral Reefs Are Degrading</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            4 of 5 islands show rising thermal-bleaching stress over 24 years — Seychelles 
            most severely (+0.68°C-weeks).
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e9, #d4ecd6); border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['mint']}; min-height: 200px;">
        <p style="color: {PALETTE['mint']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">❌ H2 — Not Supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Mangroves Are Stable</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Zero net decline across 3 tested islands and 3 independent time points 
            (1996–2020) — a genuine, robustness-checked finding.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['cyan']}; min-height: 200px;">
        <p style="color: {PALETTE['cyan']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">⚠️ H3 — Suggestive</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Governance Is Partially Aligned</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Moderate positive correlation (r=0.727) between risk and protection — but not 
            statistically significant at this sample size (p=0.164).
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Analysis")

nav_items = [
    ("🏝️", "Study Design", "Islands, methodology, and hypotheses"),
    ("🌡️", "Ecological Findings", "Coral thermal stress vs. mangrove stability"),
    ("📉", "Physical Exposure", "Settlement-level sea-level-rise risk"),
    ("⚠️", "Compound Vulnerability", "The signature cross-island ranking"),
    ("🏛️", "Governance & Encroachment", "Protection alignment and settlement pressure"),
    ("🗺️", "Interactive Maps", "Live geospatial exploration"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                    margin-bottom: 14px; border: 1px solid rgba(0,180,216,0.2); min-height: 110px;">
            <p style="font-size: 1.6rem; margin: 0 0 6px 0;">{icon}</p>
            <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin: 0 0 4px 0;">{title}</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.8rem; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, {PALETTE['card_bg']}, #e8f4f8);
                border-radius: 16px; border: 1px solid rgba(0,180,216,0.2);">
        <p style="color: {PALETTE['text_muted']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Developed by</p>
        <h2 style="color: {PALETTE['navy']}; margin: 5px 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['green']}; font-weight: 600;">Independent Geospatial Researcher</p>
    </div>
    """,
    unsafe_allow_html=True,
)