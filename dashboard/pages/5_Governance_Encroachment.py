import streamlit as st
import plotly.graph_objects as go
import numpy as np
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

st.markdown("<h1 style='text-align: center;'>GOVERNANCE & ENCROACHMENT</h1>", unsafe_allow_html=True)
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

tab1, tab_sb, tab_pol, tab2 = st.tabs(["Protection and Risk (H3)", "Coastal Setbacks", "Policy Comparison", "Built-up Change (supplementary)"])

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
| Maldives | {pct(R['protected']['maldives'])} | {pct(R['protected_strict']['maldives'])} | Many small protected sites under the Environmental Protection and Preservation Act (Law 4/93); 25 of its 93 WDPA records are UNESCO-MAB Biosphere Reserve zones |
| Lakshadweep | – | – | No record in the WDPA extract |
""")

    fig6_path = os.path.join(FIGURES_DIR, "fig6_governance_alignment.png")
    if os.path.exists(fig6_path):
        st.markdown("##### Figure 7 — As it appears in the Research Paper")
        st.image(fig6_path, use_container_width=True)

with tab_sb:
    SB, CUR = R.get("setback"), R.get("setback_curve")
    st.markdown("### Do the Building Rules Reach the Low-Lying Buildings?")
    st.markdown("""
    A setback is the one coastal rule that decides where people may build. For about 1.35 million building
    footprints (Overture Maps, release 2026-08-19.0), the bare-earth elevation (DeltaDTM) and the distance to the
    shoreline were compared with the setback written in national law. The question is how many buildings at or
    below 1 m stand landward of that line, where the rule does not reach them.
    """)
    if SB is None:
        st.info("Run scripts/analysis/setback_calibration.py to produce data/setback_calibration_summary.csv.")
    else:
        variant = st.radio("Elevation cells below 0 m (DeltaDTM artefacts)", ["all", "excl_negative"],
                           format_func=lambda v: "Included (main)" if v == "all" else "Left out (sensitivity)",
                           horizontal=True)
        order = ["Maldives", "Lakshadweep", "Seychelles", "Fiji", "Canary Islands"]
        rows = []
        for isl in order:
            r = SB.loc[(isl, variant)]
            rule = "none for inhabited land" if r["statutory_setback_m"] == "none" else f"{r['statutory_setback_m']} m"
            rows.append(f"| {isl} | {r['low_pct']:.2f}% ({int(r['low_buildings']):,}) | {rule} | "
                        f"{r['low_outside_every_setback_pct']:.1f}% | {r['low_median_dist_m']:.0f} m | "
                        f"{r['setback_covering_90pct_low_m']:.0f} m |")
        st.markdown("| Island group | Buildings at or below 1 m | Statutory setback | Low buildings landward of every setback | Median distance to shore | Distance covering 90% |\n"
                    "|---|---:|---|---:|---:|---:|\n" + "\n".join(rows))

        if CUR is not None:
            col = {"Maldives": "#2c7fb8", "Seychelles": "#e34a33", "Fiji": "#31a354",
                   "Canary Islands": "#756bb1", "Lakshadweep": "#fd8d3c"}
            marks = {"Canary Islands": [100, 20], "Seychelles": [25], "Lakshadweep": [20]}
            fig = go.Figure()
            for isl in order:
                d = CUR[CUR["island"] == isl].sort_values("distance_m")
                fig.add_trace(go.Scatter(x=d["distance_m"], y=d["pct_low_buildings_within"], mode="lines",
                                         name=isl, line=dict(color=col[isl], width=2.4),
                                         hovertemplate=isl + "<br>within %{x:,.0f} m: %{y:.1f}%<extra></extra>"))
                for m in marks.get(isl, []):
                    v = float(np.interp(m, d["distance_m"], d["pct_low_buildings_within"]))
                    fig.add_trace(go.Scatter(x=[m], y=[v], mode="markers+text", text=[f"{m} m: {v:.0f}%"],
                                             textposition="middle left" if isl == "Canary Islands" else "bottom right",
                                             marker=dict(size=11, color=col[isl], line=dict(color="white", width=1.5)),
                                             textfont=dict(color=col[isl]), showlegend=False, hoverinfo="skip"))
            fig.update_layout(template="plotly_dark", height=460,
                              xaxis=dict(title="Distance from shoreline (m, log scale)", type="log", range=[0, 3.48]),
                              yaxis=dict(title="% of buildings at or below 1 m within this distance", range=[0, 100]),
                              font=dict(family="Poppins", color="#FFD60A"), plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20),
                              legend=dict(x=0.99, y=0.02, xanchor="right", yanchor="bottom"))
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Curve: share of low buildings within each distance (all cells). Dots: the statutory setback.")

        mal = SB.loc[("Maldives", "all")]
        st.warning(f"""
        **On the tropical islands the setbacks reach fewer than one in ten low buildings.** Those buildings stand a
        median {SB.loc[('Lakshadweep', 'all'), 'low_median_dist_m']:.0f}–{SB.loc[('Seychelles', 'all'), 'low_median_dist_m']:.0f} m
        from the shore, well behind a 20 m or 25 m line. The Canary Islands are the exception: their low buildings are a
        thin beachfront and port strip, and Spain's 100 m rule covers {100 - SB.loc[('Canary Islands', 'all'), 'low_outside_every_setback_pct']:.0f}% of them.
        Even a 100 m rule would cover only about half of the low buildings in the Maldives, because on an atoll low land
        is most of the island ({mal['low_pct']:.1f}% of all Maldivian buildings are at or below 1 m). Rules written in
        heights (minimum floor or ground levels) would fit atolls better than rules written in distance.
        """)

    st.markdown("##### Coastal instruments by Hood's NATO tools")
    st.markdown("""
| Island group | Setback for buildings (Authority) | Other coastal instruments | Legal basis of the setback |
|---|---|---|---|
| Canary Islands | 100 m; 20 m on land already urban in 1988 | Natura 2000 sites and national parks (Authority) | Ley 22/1988 de Costas, art. 23 and Transitional Provision 3 |
| Seychelles | 25 m from the high water mark; 10 m with permission | Marine Spatial Plan (Authority), financed through a 2016 debt-for-nature swap (Treasure) | S.I. 91 of 2023, reg. 13 |
| Lakshadweep | 20 m no development zone | none in WDPA | ICRZ Notification 2019 (width from secondary sources) |
| Maldives | none for inhabited islands; 5 m from the vegetation line on resort islands | protected areas and UNESCO-MAB zones (Authority) | Tourism environment regulation, cl. 2.10 |
| Fiji | none found | locally managed marine areas (Organisation, co-management) | – |
""")
    st.caption("The Maldives and Lakshadweep are the closest pair to a most similar systems design: Indian Ocean coral atolls, "
               "with Mahl (a Dhivehi dialect) spoken on Minicoy, but a sovereign state against a Union Territory under India's "
               "coastal regulation. Their low buildings are outside any setback at almost the same rate.")

    for name, cap in (("fig9_setback_calibration.png", "Figure 9 — Setback coverage, as in the Research Paper"),
                      ("fig10_setback_close_ups.png", "Figure 10 — Close-ups of the densest low-lying clusters")):
        pth = os.path.join(FIGURES_DIR, name)
        if os.path.exists(pth):
            st.markdown(f"##### {cap}")
            st.image(pth, use_container_width=True)

with tab_pol:
    POL, TL = R.get("policy"), R.get("policy_timeline")
    st.markdown("### Do More Coastal Rules Mean More Reach?")
    st.markdown("""
    Each government's coastal rules in force in October 2026 were coded by hand from the legal texts. **Policy density**
    counts six instrument types (building setback, statutory coastal zones, impact assessment law, national coastal plan,
    coast-specific authority, climate framework law). **Setback intensity** is the setback width, averaged over built-up
    and other land and divided by 100 m. Following Knill, Schulze and Tosun (2012), these policy outputs are compared with
    an outcome: the share of buildings at or below 1 m that the setback reaches.
    """)
    if POL is None:
        st.info("Run scripts/analysis/coastal_policy_coding.py to produce data/coastal_policy_scores.csv.")
    else:
        rows = []
        for _, r in POL.iterrows():
            rule = "none" if r["setback_general_m"] == 0 else (
                f"{int(r['setback_inhabited_m'])} m" if r["setback_inhabited_m"] == r["setback_general_m"]
                else f"{int(r['setback_inhabited_m'])} m built-up / {int(r['setback_general_m'])} m elsewhere")
            rows.append(f"| {r['label']} | {int(r['density'])} | {rule} | {r['intensity']:.2f} | "
                        f"{r['low_reached_by_setback_pct']:.1f}% | {r['setback_for_75pct_low_m']:.0f} m |")
        st.markdown("| Jurisdiction | Density (of 6) | Setback | Intensity | Low buildings reached | Setback needed for 75% |\n"
                    "|---|---:|---|---:|---:|---:|\n" + "\n".join(rows))
        col = {"maldives": "#2c7fb8", "seychelles": "#e34a33", "fiji": "#31a354",
               "canary": "#756bb1", "lakshadweep": "#fd8d3c"}
        fig = go.Figure()
        for _, r in POL.iterrows():
            fig.add_trace(go.Scatter(x=[r["density"]], y=[r["low_reached_by_setback_pct"]], mode="markers+text",
                                     text=[r["label"]], textposition="top center", name=r["label"],
                                     marker=dict(size=16, color=col[r["jurisdiction"]], line=dict(color="white", width=1.5)),
                                     hovertemplate=r["label"] + "<br>density %{x} of 6<br>reached %{y:.1f}%<extra></extra>"))
        fig.update_layout(template="plotly_dark", height=420, showlegend=False,
                          xaxis=dict(title="Policy density (instrument types in force, of 6)", range=[1, 6.8], dtick=1),
                          yaxis=dict(title="% of low buildings reached by the setback", range=[-5, 100]),
                          font=dict(family="Poppins", color="#FFD60A"), plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
        lak = POL.set_index("jurisdiction").loc["lakshadweep"]
        st.warning(f"""
        **Outputs do not translate into reach on the tropical islands.** Lakshadweep has {int(lak['density'])} of the 6
        instrument types and its setback reaches {lak['low_reached_by_setback_pct']:.1f}% of its low buildings. The Canary
        Islands are the only case where many rules and a wide setback also reach most low buildings, because low land
        there is a narrow beachfront strip.
        """)
    if TL is not None:
        st.markdown("##### Rule changes since 1988")
        lab = {"canary": "Canary Islands", "lakshadweep": "Lakshadweep", "seychelles": "Seychelles",
               "maldives": "Maldives", "fiji": "Fiji"}
        pick = st.selectbox("Jurisdiction", ["All"] + list(lab.values()), key="pol_tl")
        t = TL.copy()
        t["Jurisdiction"] = t["jurisdiction"].map(lab)
        if pick != "All":
            t = t[t["Jurisdiction"] == pick]
        cols = ["Jurisdiction", "date", "instrument", "direction", "change", "verification"]
        if "electoral_democracy_at_change" in t:
            cols.insert(5, "electoral_democracy_at_change")
        st.dataframe(t[cols].rename(columns={"date": "Date", "instrument": "Instrument", "direction": "Direction",
                                             "change": "What changed", "verification": "Source level",
                                             "electoral_democracy_at_change": "V-Dem electoral democracy"}),
                     use_container_width=True, hide_index=True)
        st.caption("Direction: expansion adds or tightens a rule; dismantling removes, relaxes or exempts; reallocation moves "
                   "competence between levels of government. Coding and sources: data/policy_coding/.")
    for name, cap in (("fig11_policy_density_intensity.png", "Figure 11 — Policy density, intensity and reach"),
                      ("fig12_coastal_policy_timeline.png", "Figure 12 — Coastal rule changes since 1988")):
        pth = os.path.join(FIGURES_DIR, name)
        if os.path.exists(pth):
            st.markdown(f"##### {cap}")
            st.image(pth, use_container_width=True)

with tab2:
    st.markdown("### Built-up Change on Land, 2016 to 2024 (supplementary)")
    st.markdown("""
    Change in the Normalized Difference Built-up Index (NDBI) from cloud-masked Sentinel-2 composites,
    measured **on land pixels only** and on land within 1 km of mapped mangroves and reefs, with 95% block-bootstrap
    intervals. Each island is one window, not the whole country: the Malé area (Maldives), Mahé (Seychelles)
    and western Viti Levu (Fiji). This is supporting context, not one of the study's hypotheses.
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
    "Copernicus Sentinel-2; Overture Maps buildings (ODbL)</p>",
    unsafe_allow_html=True,
)
