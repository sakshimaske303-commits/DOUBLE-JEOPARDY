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

GITHUB_URL = "https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY"

# ------------------------------------------------------------------
# Robust path resolution: works both locally (running from inside
# dashboard/) and on Streamlit Cloud (which runs from the repo root
# without cd'ing into dashboard/ first) — the same class of fix
# needed after PDFs 404'd only in a prior cloud deployment.
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                      # repo root

st.markdown("<h1 style='text-align: center;'>🌊 DOUBLE JEOPARDY</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400; margin-top: -10px;'>"
    "The Vulnerability Spiral — Compound Climate Risk Across Five Island Nations</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(34, 211, 238, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; margin: 10px 0 18px 0;">
        <a href="https://doi.org/10.5281/zenodo.21739961" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['card_bg']}, #0A0A0A);
                border: 2px solid {PALETTE['navy']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(34, 211, 238, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{PALETTE['green']}; font-family:'Poppins',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_dark']}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.21739961
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
    st.metric("ISLANDS", "5", "3 Ocean Basins")
with col2:
    st.metric("DATASETS", "10+", "Multi-source")
with col3:
    st.metric("TIME SPAN", "1996–2024", "28 years")
with col4:
    st.metric("HIGHEST RISK", "Seychelles", "Score: 0.895")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(34, 211, 238, 0.06);
                border: 1px solid rgba(34, 211, 238, 0.3); border-left: 4px solid {PALETTE['navy']};
                border-radius: 10px;">
        <p style="color:{PALETTE['navy']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:700; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_dark']}; font-size:1rem; line-height:1.6; margin:0;">
            Climate adaptation funding for small island nations is often allocated using
            single-indicator exposure metrics like sea-level-rise risk alone. This project shows that
            can be actively misleading: the Maldives has the highest physical exposure of any island
            tested — yet Seychelles is the highest overall-risk island once ecosystem-buffer
            degradation is factored in. Treating "ecosystem degradation" as one uniform trend would be
            another mistake: coral reefs are genuinely declining, but mangroves, tested with equal
            rigor, are not — a finding that only survives because it wasn't assumed away from the start.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        <div style="background: {PALETTE['card_bg']};
                    border-left: 5px solid {PALETTE['navy']}; border-radius: 12px;
                    padding: 22px; height: 100%; border: 1px solid rgba(34,211,238,0.2);">
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
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['risk']}; min-height: 200px;">
        <p style="color: {PALETTE['risk']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H1 — Supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Coral Reefs Are Degrading</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            4 of 5 islands show a nominal rise in thermal-bleaching stress over 24 years; a
            formal trend test confirms this as statistically significant for Maldives and
            Seychelles (+0.68°C-weeks) — the two islands driving this project's central finding.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['mint']}; min-height: 200px;">
        <p style="color: {PALETTE['mint']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H2 — Not Supported</p>
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
        <p style="color: {PALETTE['cyan']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H3 — Suggestive</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Governance Is Partially Aligned</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Moderate positive correlation (r=0.718) between risk and protection — but not
            statistically significant at this sample size (p=0.172, 95% CI: -0.45 to 0.98).
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Analysis")

nav_items = [
    ("Study Design", "Islands, methodology, and hypotheses"),
    ("Theoretical Foundations", "The physical and ecological theory behind the risk-reversal finding"),
    ("Ecological Findings", "Coral thermal stress vs. mangrove stability"),
    ("Physical Exposure", "Settlement-level sea-level-rise risk"),
    ("Compound Vulnerability", "The signature cross-island ranking"),
    ("Governance & Encroachment", "Protection alignment and settlement pressure"),
    ("Interactive Maps & Plots", "Live geospatial exploration plus the three headline charts"),
]

cols = st.columns(3)
for i, (title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                    margin-bottom: 14px; border: 1px solid rgba(34,211,238,0.2); min-height: 110px;">
            <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin: 10px 0 4px 0;">{title}</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.8rem; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
st.markdown("### Full Project Documentation")
st.markdown(
    f"<p style='color:{PALETTE['text_muted']}; font-weight:600;'>"
    "Download the complete research paper, project journal, and development log.</p>",
    unsafe_allow_html=True,
)

doc0, doc1, doc2, doc3 = st.columns(4)

with doc0:
    pdf_path = os.path.join(ROOT_DIR, "DJ_Executive_Summary.pdf")
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Executive Summary (PDF)",
                data=f,
                file_name="DOUBLE_JEOPARDY_Executive_Summary.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except FileNotFoundError:
        st.warning("DJ_Executive_Summary.pdf not found.")

with doc1:
    pdf_path = os.path.join(ROOT_DIR, "DJ_Research_Paper.pdf")
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Research Paper (PDF)",
                data=f,
                file_name="DOUBLE_JEOPARDY_Research_Paper.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except FileNotFoundError:
        st.warning("DJ_Research_Paper.pdf not found.")

with doc2:
    pdf_path = os.path.join(ROOT_DIR, "DJ_Project_Report.pdf")
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Project Report (PDF)",
                data=f,
                file_name="DOUBLE_JEOPARDY_Project_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except FileNotFoundError:
        st.warning("DJ_Project_Report.pdf not found.")

with doc3:
    pdf_path = os.path.join(ROOT_DIR, "DJ_Development_Log.pdf")
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Development Log (PDF)",
                data=f,
                file_name="DOUBLE_JEOPARDY_Development_Log.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except FileNotFoundError:
        st.warning("DJ_Development_Log.pdf not found.")

st.markdown("---")

# ============================================================
# FOOTER — NAME + GITHUB LINK
# ============================================================
st.markdown(
    f"""
    <div style="text-align: center; padding: 25px; background: {PALETTE['card_bg']};
                border-radius: 16px; border: 1px solid rgba(34,211,238,0.25);">
        <p style="color: {PALETTE['text_muted']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Developed by</p>
        <h2 style="color: {PALETTE['navy']}; margin: 5px 0; border: none; padding: 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['green']}; font-weight: 600; margin-bottom: 18px;">Independent Geospatial Researcher</p>
        <a href="{GITHUB_URL}" target="_blank" style="text-decoration:none;">
            <span style="display:inline-block; background: linear-gradient(90deg, {PALETTE['navy']}, {PALETTE['green']}); color:#0A0A0A; font-weight:800; font-size:0.9rem; padding:10px 24px; border-radius:6px;">View on GitHub</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)