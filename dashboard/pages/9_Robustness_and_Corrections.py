import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pct

apply_custom_style()

# Paper Sections 4.6 (sensitivity checks) and 6.1 (what changed from version 1) on one page.
# Numbers read from the pipeline CSVs via dashboard/results.py where they exist (added 2026-10-23).
R = load_results()
G = R["gov"]
SB = R.get("setback")
P, PL = R["people"], R["places"]

st.markdown("<h1 style='text-align: center;'>ROBUSTNESS & CORRECTIONS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>What Holds, What Moves, and What Was Withdrawn</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown(f"""
<div style="padding: 18px 24px; background: rgba(34, 211, 238, 0.06); border: 1px solid rgba(34, 211, 238, 0.3);
            border-left: 4px solid {PALETTE['navy']}; border-radius: 10px; margin-bottom: 18px;">
    <p style="color:{PALETTE['text_dark']}; font-size:1rem; line-height:1.6; margin:0;">
        The main result of this study is about method. The elevation model, the exposure measure and the weighting
        each change which island looks most vulnerable. This page puts every check in one place: the choices that
        move the answer, the ones that do not, and the results from the first version that were withdrawn.
    </p>
</div>
""", unsafe_allow_html=True)

BADGE = {"Holds": "#5fd3a6", "Sensitive": "#e2b23a", "Open": "#cfd8e3", "Withdrawn": "#ff8f66"}


def rows(items):
    html = ""
    for verdict, name, text in items:
        c = BADGE[verdict]
        html += f"""
        <div style="display:grid; grid-template-columns: 120px 240px 1fr; gap: 16px; align-items: baseline;
                    padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="color:{c}; border:1px solid {c}; border-radius:999px; padding:3px 10px; font-size:0.72rem;
                         font-weight:700; letter-spacing:1px; text-transform:uppercase; justify-self:start;">{verdict}</span>
            <b style="color:{PALETTE['text_dark']}; font-size:0.95rem;">{name}</b>
            <span style="color:{PALETTE['text_dark']}; font-size:0.92rem; line-height:1.55;">{text}</span>
        </div>"""
    st.markdown(f"<div style='border-top:1px solid rgba(255,255,255,0.1);'>{html}</div>", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Sensitivity checks", "What changed from Version 1", "Second review, October 2026"])

with tab1:
    st.markdown("### Every check, and what it does to the answer")
    cross = R["cvs_crossover"]
    checks = [
        ("Sensitive", "Elevation model",
         f"Bare earth (DeltaDTM) against surface (Copernicus): Lakshadweep {pct(P[('lakshadweep', 'copernicus')])} → "
         f"{pct(P[('lakshadweep', 'deltadtm')])} of people at or below 1 m, Maldives {pct(P[('maldives', 'copernicus')])} → "
         f"{pct(P[('maldives', 'deltadtm')])}. For named places the leader changes from Seychelles to the Maldives. "
         "No other choice moves the numbers as much."),
        ("Holds", "Same points on both models",
         "DeltaDTM leaves out some points, so the two models do not count quite the same places. On the 154 Seychelles points both share, "
         "Copernicus still puts Seychelles ahead (8.4% against the Maldives' 4.4%), so the change of leader is real."),
        ("Sensitive", "Exposure measure",
         f"Counting named places puts Seychelles ({pct(PL[('seychelles', 'deltadtm')])}) level with the Maldives "
         f"({pct(PL[('maldives', 'deltadtm')])}); counting people puts the Maldives far ahead and Lakshadweep second."),
        ("Sensitive", "Water level",
         f"Maldives named places at 0.5 / 1.0 / 1.5 m: {pct(R['places_05'][('maldives', 'deltadtm')])} / "
         f"{pct(PL[('maldives', 'deltadtm')])} / {pct(R['places_15'][('maldives', 'deltadtm')])}. Half of the Maldives' places sit at or below 1.5 m."),
        ("Sensitive", "Weighting",
         f"Seychelles is top of the compound score up to an exposure weight of {cross - 0.01:.0%}, the Maldives from {cross:.0%}. "
         "Equal weights sit right at the crossover, so the top two are a near tie."),
        ("Holds", "Reef heat series",
         "Reef-cell mean, one 5 km cell, or a ±0.15° box around it: no version reaches p < 0.05 once serial correlation is "
         "accounted for (corrected p 0.09 to 0.90)."),
        ("Sensitive", "Governance, leave one out",
         f"r = {G['r']:.2f} on four island groups; removing Seychelles alone moves it to {G['loo_no_sey']:.2f}. "
         "With n = 4 this is a description, not a test."),
    ]
    if SB is not None:
        s_all = SB.loc[("Seychelles", "all"), "low_outside_every_setback_pct"]
        s_ex = SB.loc[("Seychelles", "excl_negative"), "low_outside_every_setback_pct"]
        l_all = SB.loc[("Lakshadweep", "all"), "low_outside_every_setback_pct"]
        l_ex = SB.loc[("Lakshadweep", "excl_negative"), "low_outside_every_setback_pct"]
        m_b = SB.loc[("Maldives", "all"), "low_pct"]
        checks += [
            ("Holds", "Setbacks: sub-zero cells",
             f"Leaving out buildings on DeltaDTM cells below 0 m moves the share of low buildings outside the setback "
             f"from {s_all:.1f}% to {s_ex:.1f}% in Seychelles and from {l_all:.1f}% to {l_ex:.1f}% in Lakshadweep."),
            ("Holds", "Buildings against people",
             f"The building count gives the same order as WorldPop: Maldives {m_b:.1f}% of buildings and "
             f"{pct(P[('maldives', 'deltadtm')])} of people at or below 1 m."),
        ]
    checks += [
        ("Open", "Shoreline and legal line",
         "Setback distances run to the edge of the island outlines, not the legal high water mark: some tens of metres of error, "
         "small next to medians of 80–136 m. Only national law is compared, not local plans or enforcement."),
        ("Open", "Data coverage",
         "Fiji's buildings are OpenStreetMap only; 4,478 Maldivian buildings fall outside the island outlines; "
         "the Lakshadweep setback width rests on secondary sources; reef heat stress ends in 2020."),
    ]
    rows(checks)

with tab2:
    st.markdown("### Six results from Version 1 that were withdrawn")
    st.markdown("Each came from a measurement choice that is easy to make and hard to see.")
    rows([
        ("Withdrawn", "\"78.3% of Seychelles settlements at risk\"",
         "188 of 244 points read −32767 m, the raster's no-data value, and were counted as below 1 m; most OSM \"settlement\" "
         "points are island names, some in open water. Now: one shared elevation rule, people as the main measure."),
        ("Withdrawn", "Surface elevation model only",
         "Copernicus reads palm canopy and roofs as ground. On bare earth, Lakshadweep goes from under 1% to over 6% of people "
         "at or below 1 m."),
        ("Withdrawn", "\"Significant coral trends\" (p = 0.0046, 0.0069)",
         "One 5 km cell per island and a test that treats overlapping 12-week sums as independent months. With reef-cell means "
         "and the serial-correlation correction, no trend is significant."),
        ("Withdrawn", "\"Seychelles is top at every weighting\"",
         "Both Version 1 inputs happened to be highest for Seychelles, so it scored 1.0 by construction. With people and "
         f"reef-cell means the inputs disagree and the top changes at {cross:.0%}."),
        ("Withdrawn", "\"Governance r = 0.965, p = 0.035\"",
         f"Overlapping protected areas counted twice and coverage divided by land area. As a share of the coastal zone, r = {G['r']:.2f}."),
        ("Withdrawn", "\"Seychelles built-up rise +0.11\"",
         "Measured over bounding boxes that were mostly ocean. On land only, Seychelles shows no rise."),
    ])

with tab3:
    st.markdown("### Corrections from the second review")
    st.markdown("""
| Change | Before | After | Why |
|---|---|---|---|
| Compound score scaling | Reef input scaled across 4 reef islands, Canary set to 0 afterwards | Both inputs scaled across all 5 | The paper said five; the code did four |
| Top-island crossover | 54% exposure weight | 52% | Follows from the scaling fix |
| Governance correlation | r = −0.01 | r = −0.10 (−0.97 to 0.95) | Uses the corrected scores |
| "Uncorrected" coral p-values | Raw 30-day samples | Same monthly series as the corrected test | Like-for-like comparison |
| Land-area validation | Not reproducible from the boundary files | Recomputed in EPSG:6933, all within 4% | New validation script |
| Coastal setbacks | Not analysed | Building-level analysis, about 1.35 million footprints | Policy extension (paper Sections 3.9, 4.8) |
""")
    st.caption("Full record: paper/DJ_Development_Log.md, Entries 15–18.")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — paper Sections 4.6 and 6.1; every number "
    "rerun by scripts/run_all.py</p>",
    unsafe_allow_html=True,
)
