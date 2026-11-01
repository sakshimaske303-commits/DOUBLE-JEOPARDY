import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from styles import apply_custom_style, PALETTE
from doc_viewer import render_doc_viewer
from results import load as load_results, pct, pval

R = load_results()
_P = R["primary"]
_ppl = {i: R["people"][(i, _P)] for i in R["islands"]}
_top_ppl = max(_ppl, key=_ppl.get)
_cvs_sorted = sorted(R["cvs"], key=R["cvs"].get, reverse=True)

st.set_page_config(
    page_title="DOUBLE JEOPARDY",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()

GITHUB_URL = "https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY"

# Path resolution that works both locally and on Streamlit Cloud (runs from
# repo root, doesn't cd into dashboard/ first) -- PDFs 404'd there before.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                      # repo root

st.markdown("<h1 style='text-align: center;'>DOUBLE JEOPARDY</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400; margin-top: -10px;'>"
    "The Vulnerability Spiral — Compound Climate Risk Across 5 Islands</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(34, 211, 238, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin: 10px 0 18px 0;">
        <a href="https://eartharxiv.org/repository/view/14826/" target="_blank" class="doi-badge-link" style="text-decoration:none;">
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
                        <span>PREPRINT ON EARTHARXIV</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_dark']}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        Read the preprint
                    </div>
                </div>
            </div>
        </a>
        <a href="https://doi.org/10.5281/zenodo.23827474" target="_blank" class="doi-badge-link" style="text-decoration:none;">
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
                        DOI: 10.5281/zenodo.23827474
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
    st.metric("TIME SPAN", "1996–2020", "NDBI to 2024")
with col4:
    _top = max(R["cvs"], key=R["cvs"].get)
    st.metric("TOP COMPOUND SCORE", R["label"][_top], f"{R['cvs'][_top]:.2f} (near tie)", delta_color="off")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(34, 211, 238, 0.06);
                border: 1px solid rgba(34, 211, 238, 0.3); border-left: 4px solid {PALETTE['navy']};
                border-radius: 10px;">
        <p style="color:{PALETTE['navy']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:700; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_dark']}; font-size:1rem; line-height:1.6; margin:0;">
            Rankings of small-island exposure are often built from a single elevation model and a single
            exposure measure. This project shows how much those choices matter. On a surface elevation model the
            Maldives have {pct(R['people'][('maldives', 'copernicus')])} of people at or below 1 m; on a
            bare-earth model, {pct(R['people'][('maldives', 'deltadtm')])}, and Lakshadweep moves from
            {pct(R['people'][('lakshadweep', 'copernicus')])} to {pct(R['people'][('lakshadweep', 'deltadtm')])}.
            Counting named places instead of people puts Seychelles level with the Maldives. And once
            reef heat stress is added, the top island depends on the weighting: Seychelles at equal weights,
            the Maldives once exposure carries {R['cvs_crossover']:.0%} or more of the weight. A single number would hide all of this.
            The same goes for policy: the coastal setbacks in national law reach fewer than one in ten
            low-lying buildings on the tropical islands, because on atolls low land is the island, not its edge,
            and a government with more coastal rules does not reach more of them.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is Double Jeopardy?

    Small islands face a **compounding vulnerability** to climate change — high
    physical exposure to sea-level rise, layered with **degrading natural coastal defenses**:
    mangroves and coral reefs that have historically buffered these islands from erosion
    and storm damage.

    This project independently tests whether that compounding risk is real, and whether
    it affects every ecosystem type equally. Rather than assuming mangroves and coral reefs
    degrade together, each is tested independently across five islands spanning
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
                On a bare-earth elevation model, <b>{R['label'][_top_ppl]}</b> has the largest share of people
                living at or below 1 m ({pct(_ppl[_top_ppl])}), followed by Lakshadweep ({pct(_ppl['lakshadweep'])})
                and Seychelles ({pct(_ppl['seychelles'])}). The Copernicus GLO-30 surface model
                puts the Maldives at {pct(R['people'][('maldives', 'copernicus')])}: it measures tree and roof tops,
                which lifts flat atolls most. Combined with the change in reef heat stress, the compound score
                ranks <b>{R['label'][_cvs_sorted[0]]}</b> ({R['cvs'][_cvs_sorted[0]]:.2f}) just ahead of
                {R['label'][_cvs_sorted[1]]} ({R['cvs'][_cvs_sorted[1]]:.2f}); the order flips once exposure
                carries {R['cvs_crossover']:.0%} or more of the weight.
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
        <p style="color: {PALETTE['risk']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H1 — Partly supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">More Reef Heat Stress, No Established Trend</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Mean heat stress over mapped reef was higher in 2016–2020 than in 1996–2000 at all four
            island groups with reefs (largest in Seychelles, +{R['coral_change'][('seychelles', 'reef_cells')]:.2f} °C-weeks).
            Once serial correlation is accounted for, no monotonic trend is significant
            (Seychelles {pval(R['coral_p'][('seychelles', 'reef_cells')])}).
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['mint']}; min-height: 200px;">
        <p style="color: {PALETTE['mint']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H2 — Not Supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">No Mangrove Decline Detected</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Global Mangrove Watch shows no net decline on the 3 islands with mangroves at 1996, 2010 and
            2020. These epochs are derived from a 2010 baseline, so they are not independent surveys, and
            small atoll patches are near the product's resolution.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px;
                padding: 20px; border: 2px solid {PALETTE['cyan']}; min-height: 200px;">
        <p style="color: {PALETTE['cyan']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">H3 — Not supported</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">Protection Does Not Track Risk</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Share of the 10 km coastal zone protected ranges from {pct(R['protected']['maldives'])} (Maldives) to
            {pct(R['protected']['seychelles'])} (Seychelles) and is unrelated to the compound score
            (r = {R['gov']['r']:.2f}, n = {R['gov']['n']}; Lakshadweep has no WDPA record). Descriptive only.
        </p>
    </div>
    """, unsafe_allow_html=True)

_SB = R.get("setback")
if _SB is not None:
    def _o(i):
        return _SB.loc[(i, "all"), "low_outside_every_setback_pct"]
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px; margin-top: 18px;
                padding: 20px; border: 2px solid {PALETTE['navy']};">
        <p style="color: {PALETTE['navy']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">Policy extension — Coastal setbacks</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">The Building Rules Are Drawn in the Wrong Place</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Across about 1.35 million building footprints, {_o('Seychelles'):.0f}% of the buildings at or below 1 m in
            Seychelles stand landward of its 25 m setback, and {_o('Lakshadweep'):.0f}% in Lakshadweep landward of its 20 m zone;
            the Maldives and Fiji have no setback for inhabited land. Only the Canary Islands' 100 m Ley de Costas line
            covers most of them ({100 - _o('Canary Islands'):.0f}%). See Governance &amp; Encroachment → Coastal Setbacks.
        </p>
    </div>
    """, unsafe_allow_html=True)

_POL = R.get("policy")
if _POL is not None:
    _p = _POL.set_index("jurisdiction")
    st.markdown(f"""
    <div style="background: {PALETTE['card_bg']}; border-radius: 14px; margin-top: 18px;
                padding: 20px; border: 2px solid {PALETTE['green']};">
        <p style="color: {PALETTE['green']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">Policy extension — Comparing the five governments' coastal rules</p>
        <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">More Rules Did Not Mean More Reach</p>
        <p style="color: {PALETTE['text_dark']}; font-size: 0.85rem; margin: 0;">
            Each government's coastal rules were coded from the legal texts: six instrument types for policy density,
            the setback width for intensity, and 23 dated rule changes since 1988. Lakshadweep has
            {int(_p.loc['lakshadweep', 'density'])} of the 6 instrument types and its setback reaches
            {_p.loc['lakshadweep', 'low_reached_by_setback_pct']:.1f}% of its low buildings; the Maldives has
            {int(_p.loc['maldives', 'density'])} and reaches none. Spain relaxed its coastal law in 2013, and the Maldives
            widened exemptions from environmental review in 2024–2025. See Governance &amp; Encroachment → Policy Comparison.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Analysis")

nav_items = [
    ("Study Design", "Islands, methodology, and hypotheses"),
    ("Theoretical Foundations", "The physical and ecological theory behind compound coastal risk"),
    ("Ecological Findings", "Coral thermal stress vs. mangrove stability"),
    ("Physical Exposure", "People and places at or below 1 m, on two elevation models"),
    ("Compound Vulnerability", "The signature cross-island ranking"),
    ("Governance & Encroachment", "Protection alignment, coastal setbacks, policy comparison and settlement pressure"),
    ("Interactive Maps & Plots", "Live geospatial exploration plus the four headline charts"),
    ("Robustness & Corrections", "Every sensitivity check, and what Version 1 got wrong"),
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
    "The complete research paper, project journal, and development log open directly below, no download needed.</p>",
    unsafe_allow_html=True,
)

_all_docs = [
    {"label": "Executive Summary", "filename": "DJ_Executive_Summary.pdf"},
    {"label": "Research Paper", "filename": "DJ_Research_Paper.pdf"},
    {"label": "Development Log", "filename": "DJ_Development_Log.pdf"},
    {"label": "Policy Brief", "filename": "DJ_Policy_Brief.pdf"},
]
_docs = [d for d in _all_docs if os.path.exists(os.path.join(BASE_DIR, "static", d["filename"]))]
_missing = [d for d in _all_docs if d not in _docs]

if _docs:
    render_doc_viewer(
        docs=_docs,
        colors={
            "navy_dark": "#141414",
            "navy_med": "#272727",
            "magenta": PALETTE["green"],
            "teal": PALETTE["navy"],
            "text_light": PALETTE["text_dark"],
        },
    )
for d in _missing:
    st.warning(f"{d['filename']} not found.")

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
        <p style="color: {PALETTE['green']}; font-weight: 600; margin-bottom: 18px;">Satellite data and policy, self-directed research</p>
        <a href="{GITHUB_URL}" target="_blank" style="text-decoration:none;">
            <span style="display:inline-block; background: linear-gradient(90deg, {PALETTE['navy']}, {PALETTE['green']}); color:#0A0A0A; font-weight:800; font-size:0.9rem; padding:10px 24px; border-radius:6px;">View on GitHub</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)