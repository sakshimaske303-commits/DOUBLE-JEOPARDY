import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌡️ ECOLOGICAL FINDINGS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Two Ecosystems, Two Very Different Stories</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
DOUBLE JEOPARDY tests mangrove and coral reef ecosystems **independently**, rather than assuming 
both degrade uniformly. The results reveal a striking asymmetry — one ecosystem type shows genuine, 
measurable decline; the other shows remarkable stability across nearly three decades.
""")

st.markdown("---")

tab1, tab2 = st.tabs(["🌿 Coral Reefs — H1 (Supported)", "🌳 Mangroves — H2 (Not Supported)"])

with tab1:
    st.markdown("### Coral Thermal Stress: 1996–2020")
    st.markdown("""
    Coral degradation was measured using **Degree Heating Week (DHW)**, a satellite-derived measure 
    of accumulated thermal stress. Values above 4°C-weeks are associated with significant bleaching; 
    values above 8°C-weeks are associated with severe bleaching and coral mortality.
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    dhw_data = [
        (col1, "Seychelles", "+0.68", "10.47", True),
        (col2, "Maldives", "+0.17", "6.57", False),
        (col3, "Fiji", "+0.10", "5.74", False),
        (col4, "Lakshadweep", "+0.08", "4.39", False),
        (col5, "Canary Islands", "−0.05", "12.46", False),
    ]

    for col, island, change, max_dhw, highlight in dhw_data:
        with col:
            border_color = PALETTE["risk"] if highlight else "rgba(0,150,199,0.3)"
            st.markdown(f"""
            <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 14px;
                        text-align: center; min-height: 160px; border: 2px solid {border_color};">
                <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">{island}</p>
                <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 4px;">Trend Change</p>
                <p style="color: {PALETTE['risk'] if change.startswith('+') else PALETTE['mint']}; font-weight: 800; font-size: 1.3rem; margin-bottom: 8px;">{change}</p>
                <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 2px;">Max DHW</p>
                <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin: 0;">{max_dhw}°C-wk</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.warning("""
    **Seychelles shows the most severe thermal stress increase** — a maximum recorded value of 
    10.47°C-weeks falls within the range associated with severe bleaching and coral mortality. 
    Four of five islands show a rising thermal-stress trend; only the Canary Islands, with a 
    distinct Atlantic climate regime, shows a slight decline.
    """)

with tab2:
    st.markdown("### Mangrove Extent: Three Independent Time Points")
    st.markdown("""
    Rather than relying on a single before/after comparison, mangrove extent was tracked across 
    **three independent snapshots** (1996, 2010, 2020) using the Global Mangrove Watch archive, 
    with area calculated in an equal-area projection to avoid distortion.
    """)

    col1, col2, col3 = st.columns(3)
    mangrove_data = [
        (col1, "Maldives", "0.97", "0.97", "0.97"),
        (col2, "Seychelles", "3.83", "3.84", "3.83"),
        (col3, "Fiji", "485.72", "487.97", "488.41"),
    ]

    for col, island, y1996, y2010, y2020 in mangrove_data:
        with col:
            st.markdown(f"""
            <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                        text-align: center; min-height: 200px; border: 1.5px solid rgba(27,67,50,0.3);">
                <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 12px;">{island}</p>
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem;">1996</p>
                        <p style="color: {PALETTE['green']}; font-weight: 700;">{y1996} km²</p>
                    </div>
                    <div>
                        <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem;">2010</p>
                        <p style="color: {PALETTE['green']}; font-weight: 700;">{y2010} km²</p>
                    </div>
                    <div>
                        <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem;">2020</p>
                        <p style="color: {PALETTE['green']}; font-weight: 700;">{y2020} km²</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.success("""
    **No net decline detected in any tested island.** Mangrove extent remained essentially stable 
    across all three time points and all three islands where mangroves are present — Fiji even 
    shows a marginal net increase. This does not support Hypothesis H2 as originally framed, and 
    is reported transparently as a genuine, robustness-checked finding rather than adjusted to 
    fit the original hypothesis.
    """)

st.markdown("---")

st.markdown("### Why the Difference Matters")
st.markdown("""
This asymmetry — genuine coral degradation alongside mangrove resilience — is itself the project's 
central empirical contribution. It demonstrates that ecosystem buffer degradation is **not a uniform 
phenomenon**, with direct implications for how conservation and adaptation resources should be 
prioritized across ecosystem types, rather than allocated under an assumption of uniform ecosystem risk.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch, Global Mangrove Watch</p>",
    unsafe_allow_html=True,
)