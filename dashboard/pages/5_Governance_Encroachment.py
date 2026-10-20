import streamlit as st
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pct

apply_custom_style()

# Numbers read from data/wdpa_coastal_normalized.csv, data/governance_alignment_summary.csv,
# data/compound_vulnerability_scores.csv and data/ndbi_land_change.csv (rewritten 2026-10-11).
R = load_results()
G = R["gov"]
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")

st.markdown("<h1 style='text-align: center;'>🏛️ GOVERNANCE & ENCROACHMENT</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Does Protection Follow Risk?</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Coverage is measured the same way for every island group: the share of the zone within 10 km of the
coastline that lies inside a protected area in the World Database on Protected Areas (June 2026), with
overlapping sites merged so no area is counted twice. Lakshadweep has no record in the WDPA extract and is
left out of the comparison rather than set to zero.
""")

tab1, tab2 = st.tabs(["Protection and Risk (H3)", "Built-up Change (supplementary)"])

with tab1:
    isl = [i for i in R["islands"] if R["protected"].get(i) == R["protected"].get(i)]  # drop NaN
    fig = go.Figure(go.Scatter(
        x=[R["cvs"][i] for i in isl], y=[R["protected"][i] for i in isl], mode="markers+text",
        text=[R["label"][i] for i in isl], textposition="top center",
        marker=dict(size=16, color=PALETTE["cyan"], line=dict(width=2, color=PALETTE["navy"])),
    ))
    fig.update_layout(template="plotly_dark", height=440,
                      xaxis=dict(title="Compound vulnerability score"),
                      yaxis=dict(title="Share of 10 km coastal zone protected (%)"),
                      font=dict(family="Poppins", color="#FFD60A"), plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Pearson r", f"{G['r']:.2f}", f"n = {G['n']}")
    c2.metric("95% interval", f"{G['lo']:.2f} to {G['hi']:.2f}")
    c3.metric("Spearman ρ", f"{G['rho']:.2f}")

    st.warning(f"""
    **Protection does not track risk in this sample.** Coverage ranges from {pct(R['protected']['maldives'])} of the
    coastal zone in the Maldives to {pct(R['protected']['seychelles'])} in Seychelles, and is unrelated to the
    compound score (r = {G['r']:.2f}). With four island groups this is a description, not a test: removing
    Seychelles alone moves r to {G['loo_no_sey']:.2f}.

    **What changed from the first version:** it reported r = 0.965, p = 0.035. Overlapping protected areas had been
    counted twice and coverage was divided by land area, which for small islands with large marine reserves gives
    ratios far above 1. Measured as a share of the coastal zone, the relationship disappears.
    """)

    st.markdown("##### Coverage and instruments")
    st.markdown(f"""
| Island group | Coastal zone protected | Strict (IUCN Ia–IV) | Main instrument behind the coverage |
|---|---:|---:|---|
| Seychelles | {pct(R['protected']['seychelles'])} | {pct(R['protected_strict']['seychelles'])} | Marine Spatial Plan, more than 30% of the EEZ designated in 2020, prepared under a 2016 debt-for-nature swap |
| Canary Islands | {pct(R['protected']['canary'])} | {pct(R['protected_strict']['canary'])} | Natura 2000 sites (EU Habitats and Birds Directives) and Spanish national parks |
| Fiji | {pct(R['protected']['fiji'])} | {pct(R['protected_strict']['fiji'])} | Locally managed marine areas: 102 of 126 WDPA records |
| Maldives | {pct(R['protected']['maldives'])} | {pct(R['protected_strict']['maldives'])} | Protected areas under the Environmental Protection and Preservation Act (Law 4/93) |
| Lakshadweep | – | – | No record in the WDPA extract |
""")

    fig6_path = os.path.join(FIGURES_DIR, "fig6_governance_alignment.png")
    if os.path.exists(fig6_path):
        st.markdown("##### Figure 6 — As it appears in the Research Paper")
        st.image(fig6_path, use_container_width=True)

with tab2:
    st.markdown("### Built-up Change on Land, 2016 to 2024 (supplementary)")
    st.markdown("""
    Change in the Normalized Difference Built-up Index (NDBI) from cloud-masked Sentinel-2 composites,
    measured **on land pixels only** and on land within 1 km of mapped mangroves and reefs, with 95% block-bootstrap
    intervals. This is supporting context, not one of the study's hypotheses.
    """)
    rows = []
    for key in ("maldives", "seychelles", "fiji"):
        for zone, zl in (("all_land", "all land"), ("land_within_1000m_of_ecosystems", "land within 1 km of ecosystems")):
            v = R["ndbi"].get((key, zone))
            if v:
                rows.append((R["label"][key], zl, v))
    if rows:
        st.markdown("| Island | Zone | NDBI change | 95% interval |\n|---|---|---:|---|\n" + "\n".join(
            f"| {a} | {b} | {v[0]:+.3f} | {v[1]:+.3f} to {v[2]:+.3f} |" for a, b, v in rows))
    st.info("""
    **What changed from the first version:** it reported a large rise for Seychelles (+0.11). That was measured over
    bounding boxes that were mostly ocean. On land pixels only, Seychelles shows no rise and the Maldives a small one.
    """)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Sources: UNEP-WCMC and IUCN, Protected Planet (WDPA, June 2026); "
    "Copernicus Sentinel-2</p>",
    unsafe_allow_html=True,
)
