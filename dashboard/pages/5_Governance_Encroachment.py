import streamlit as st
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🏛️ GOVERNANCE & ENCROACHMENT</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Is Protection Policy Aligned With Verified Risk?</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Beyond ecological and physical risk, DOUBLE JEOPARDY tests a governance dimension: does formal 
protected-area designation — the primary policy instrument for managing coastal ecosystem risk — 
actually align with where empirically verified vulnerability is highest?
""")

st.markdown("---")

tab1, tab2 = st.tabs(["🏛️ Governance Alignment (H3)", "🏗️ Settlement Encroachment"])

with tab1:
    st.markdown("### Protected Area Coverage vs. Compound Vulnerability")

    islands = ["Lakshadweep", "Fiji", "Canary Islands", "Maldives", "Seychelles"]
    vuln_scores = [0.467, 0.217, 0.000, 0.651, 0.880]
    wdpa_ratios = [0.00, 0.42, 2.32, 3.90, 11.32]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vuln_scores, y=wdpa_ratios, mode="markers+text",
        text=islands, textposition="top center",
        textfont=dict(size=12, color="#000000"),
        marker=dict(size=16, color=PALETTE["cyan"], line=dict(width=2, color=PALETTE["navy"])),
    ))

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Compound Vulnerability Score",
        yaxis_title="Coastal WDPA Protection Ratio",
        xaxis=dict(tickfont=dict(color="#000000", size=12), title_font=dict(color="#000000", size=13)),
        yaxis=dict(tickfont=dict(color="#000000", size=12), title_font=dict(color="#000000", size=13)),
        height=440,
        margin=dict(t=20, b=40, l=20, r=20),
        font=dict(family="Poppins", color="#000000"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("CORRELATION (r)", "0.727", "Moderately strong, positive")
    with col2:
        st.metric("P-VALUE", "0.164", "Not statistically significant")

    st.warning("""
    **A suggestive, not confirmatory, finding.** The direction of the relationship is consistent 
    with risk-responsive governance — Seychelles, the highest-vulnerability island, also has the 
    highest coastal protection ratio. But with only five islands in the sample, there isn't 
    sufficient statistical power to confirm this relationship with confidence. Reported honestly 
    as suggestive evidence, not proof.
    """)

with tab2:
    st.markdown("### Built-Up Area Change: 2016 vs. 2024")
    st.markdown("""
    Using Sentinel-2 satellite imagery, the Normalized Difference Built-up Index (NDBI) was compared 
    between 2016 and 2024 for the three islands with mangrove ecosystems, testing whether settlement 
    expansion is concentrated near degrading ecosystem buffer zones.
    """)

    encroach_islands = ["Fiji", "Maldives", "Seychelles"]
    ndbi_change = [-0.0008, 0.0461, 0.1135]

    fig2 = go.Figure()
    colors2 = [PALETTE["mint"] if v < 0.02 else PALETTE["risk"] for v in ndbi_change]
    fig2.add_trace(go.Bar(
        x=encroach_islands, y=ndbi_change, marker_color=colors2,
        text=[f"{v:+.4f}" for v in ndbi_change], textposition="outside",
        textfont=dict(color="#000000", size=13),
    ))

    fig2.update_layout(
        template="plotly_white",
        yaxis_title="NDBI Change (2016 → 2024)",
        xaxis=dict(tickfont=dict(color="#000000", size=13)),
        yaxis=dict(tickfont=dict(color="#000000", size=12), title_font=dict(color="#000000", size=13)),
        height=400,
        margin=dict(t=20, b=40, l=20, r=20),
        font=dict(family="Poppins", color="#000000"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.error("""
    **Seychelles shows the strongest encroachment signal** (+0.1135) — notably crossing from a 
    vegetation-dominated to a built-up-dominated average, consistent with its status as the 
    highest compound-vulnerability island. Fiji shows effectively no change, consistent with its 
    stable mangrove extent and mild coral thermal-stress trend.
    """)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: World Database on Protected Areas, Sentinel-2</p>",
    unsafe_allow_html=True,
)