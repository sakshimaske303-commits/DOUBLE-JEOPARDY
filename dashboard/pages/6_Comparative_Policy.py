import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE, show_image
from results import load as load_results

apply_custom_style()

# Numbers read from data/coastal_policy_scores.csv, data/policy_coding/*.csv,
# data/coastal_policy_timeline_with_regime.csv and data/regime/vdem_electoral_democracy.csv.
R = load_results()
POL, TL = R.get("policy"), R.get("policy_timeline")
DATA = os.path.join(PROJECT_ROOT, "data")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")
ORDER = ["canary", "lakshadweep", "seychelles", "fiji", "maldives"]
LAB = {"canary": "Canary Islands", "lakshadweep": "Lakshadweep", "seychelles": "Seychelles",
       "fiji": "Fiji", "maldives": "Maldives"}
GOV = {"canary": "Spain · EU outermost region", "lakshadweep": "India · Union Territory",
       "seychelles": "Independent state", "fiji": "Independent state", "maldives": "Independent state"}
COL = {"maldives": "#2c7fb8", "seychelles": "#e34a33", "fiji": "#31a354",
       "canary": "#756bb1", "lakshadweep": "#fd8d3c"}
LAYOUT = dict(template="plotly_dark", font=dict(family="Poppins", color="#FFD60A"),
              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20))

st.markdown("<h1 style='text-align: center;'>COMPARATIVE POLICY ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>Five Governments, One Rising Sea</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Five governments regulate five low island groups against the same rising sea. This page compares their coastal
policy in four steps: the **design** of the comparison, the **instruments** each government uses, how dense and
demanding those instruments are against whether a distance rule can fit the low-lying land (**policy design**), and how
the rules **changed over time** and under which political setting.
""")

c1, c2, c3, c4 = st.columns(4)
for col, big, small in ((c1, "5", "governments compared"), (c2, "6", "instrument types coded per government"),
                        (c3, "23", "dated rule changes, 1988–2025"), (c4, "1.35 M", "buildings the rules are set against")):
    col.markdown(f"""
    <div style="background:{PALETTE['card_bg']}; border:1px solid rgba(34,211,238,0.35); border-radius:12px;
                padding:16px; text-align:center;">
        <p style="color:{PALETTE['navy']}; font-size:1.8rem; font-weight:800; margin:0;">{big}</p>
        <p style="color:{PALETTE['text_muted']}; font-size:0.8rem; margin:4px 0 0 0;">{small}</p>
    </div>""", unsafe_allow_html=True)

# ---------------- 1. Design ----------------
st.markdown("### 1. Design")
st.markdown("""
| | |
|---|---|
| **Cases** | Maldives, Seychelles, Fiji (independent states); Lakshadweep (Indian Union Territory); Canary Islands (Spain, EU outermost region). Chosen for ecological range; read as a structured, focused comparison, not a controlled design |
| **Closest pair** | Maldives and Lakshadweep: Indian Ocean coral atolls of similar height, with Mahl (a Dhivehi dialect) spoken on Minicoy, under a sovereign state and under India's national coastal regulation; they also differ in population, reclamation and tourism |
| **Multi-level governance** | EU, national and regional levels in the Canary Islands; national rules for a Union Territory in Lakshadweep; national governments with island councils in the Maldives |
| **Instruments** | Hood's NATO tools (Nodality, Authority, Treasure, Organisation); policy density and intensity (Knill, Schulze and Tosun 2012) |
| **Design fit** | Share of buildings at or below 1 m within each setback, and within the same 20 m width on every island. Not a policy outcome: many buildings predate the rules |
| **Political setting** | V-Dem electoral democracy index in the year of each rule change; descriptive only |
""")

# ---------------- 2. Instruments ----------------
st.markdown("### 2. Who Regulates the Coast, and With What")
st.markdown("""
| Island group | Governed by | Setback for buildings (Authority) | Other coastal instruments |
|---|---|---|---|
| Canary Islands | Spain · EU outermost region | 100 m; 20 m on land already urban in 1988 (Ley 22/1988 de Costas) | Natura 2000 sites and national parks (Authority) |
| Seychelles | Independent state | 25 m from the high water mark; 10 m with permission (S.I. 91 of 2023) | Marine Spatial Plan (Authority), financed through a 2016 debt-for-nature swap (Treasure) |
| Lakshadweep | India · Union Territory | 20 m no development zone (ICRZ Notification 2019, secondary sources) | none in WDPA |
| Maldives | Independent state | none for inhabited islands; 5 m on resort islands | protected areas and UNESCO-MAB zones (Authority) |
| Fiji | Independent state | none found | locally managed marine areas (Organisation, co-management) |
""")

# ---------------- 3. Density, intensity, reach ----------------
st.markdown("### 3. Instrument Counts and Design Fit")
st.markdown("""
Each government's coastal rules in force in October 2026 were coded by hand from the legal texts. **Policy density**
counts six instrument types; **setback intensity** is the setback width, averaged over built-up and other land and
divided by 100 m. Both are policy outputs. They are set next to the share of buildings at or below 1 m within 20 m of
the shore, the same width on every island, which shows whether a distance rule can fit the low land at all.
""")
code_path = os.path.join(DATA, "policy_coding", "coastal_policy_coding.csv")
if POL is None or not os.path.exists(code_path):
    st.info("Run scripts/analysis/coastal_policy_coding.py to produce the policy coding outputs.")
else:
    code = pd.read_csv(code_path)
    items = [("D1_building_setback", "Setback"), ("D2_statutory_coastal_zones", "Coastal zones"),
             ("D3_eia_law", "Impact assessment"), ("D4_coastal_plan", "Coastal plan"),
             ("D5_dedicated_coastal_authority", "Coastal authority"), ("D6_climate_law_coastal", "Climate law")]
    P = POL.set_index("jurisdiction")
    rows = []
    for j in ORDER:
        cells = []
        for it, _ in items:
            r = code[(code["jurisdiction"] == j) & (code["item"] == it)].iloc[0]
            mark = "●" if int(r["value"]) == 1 else "○"
            if int(r["value"]) == 1 and r["verification"] == "secondary":
                mark += " †"
            cells.append(mark)
        rows.append(f"| {LAB[j]} | " + " | ".join(cells) +
                    f" | {int(P.loc[j, 'density'])} of 6 | {P.loc[j, 'intensity']:.2f} | "
                    + ("no setback" if pd.isna(P.loc[j, 'low_within_statutory_setback_pct']) else f"{P.loc[j, 'low_within_statutory_setback_pct']:.1f}%")
                    + f" | {P.loc[j, 'low_within_20m_pct']:.1f}% |")
    st.markdown("| Jurisdiction | " + " | ".join(n for _, n in items) + " | Density | Intensity | Low buildings within the setback | Within 20 m, same width |\n"
                "|---|" + ":---:|" * len(items) + "---:|---:|---:|---:|\n" + "\n".join(rows))
    st.caption("● in force · ○ not found · † secondary source only. Every value, with its legal basis and source, is in "
               "data/policy_coding/coastal_policy_coding.csv; the coding rules are in data/policy_coding/CODEBOOK.md.")

    fig = go.Figure()
    for j in ORDER:
        fig.add_trace(go.Scatter(x=[P.loc[j, "density"]], y=[P.loc[j, "low_within_20m_pct"]],
                                 mode="markers+text", text=[LAB[j]], textposition="top center",
                                 marker=dict(size=10 + 40 * P.loc[j, "intensity"], color=COL[j],
                                             line=dict(color="white", width=1.5)),
                                 hovertemplate=(LAB[j] + "<br>density %{x} of 6<br>intensity "
                                                + f"{P.loc[j, 'intensity']:.2f}" + "<br>within 20 m: %{y:.1f}%<extra></extra>")))
    fig.update_layout(**LAYOUT, height=430, showlegend=False,
                      xaxis=dict(title="Policy density (instrument types in force, of 6)", range=[1, 6.8], dtick=1),
                      yaxis=dict(title="% of low buildings within 20 m (same width)", range=[-5, 100]))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Marker size: setback intensity.")
    lak, mal = P.loc["lakshadweep"], P.loc["maldives"]
    st.warning(f"""
    **Instrument counts do not track design fit.** Lakshadweep has {int(lak['density'])} of the 6 instrument types and a
    20 m zone covering {lak['low_within_statutory_setback_pct']:.1f}% of its low buildings; the Maldives has {int(mal['density'])}
    and no setback, and the same 20 m width would cover {mal['low_within_20m_pct']:.1f}% there. Covering three in four low
    buildings would take
    {P.loc[['lakshadweep', 'seychelles', 'fiji', 'maldives'], 'setback_for_75pct_low_m'].min():.0f}–{P.loc[['lakshadweep', 'seychelles', 'fiji', 'maldives'], 'setback_for_75pct_low_m'].max():.0f} m
    on these islands, against {P.loc['canary', 'setback_for_75pct_low_m']:.0f} m in the Canary Islands.
    """)

# ---------------- 4. Change over time ----------------
st.markdown("### 4. How the Rules Changed, 1988–2025")
if TL is None:
    st.info("Run scripts/analysis/coastal_policy_coding.py to produce the rule timeline.")
else:
    t = TL.copy()
    t["year"] = t["date"].astype(str).str[:4].astype(int)
    n = t["direction"].value_counts()
    st.markdown(f"""
    Of {len(t)} dated changes, **{n.get('expansion', 0)} added or tightened rules**, **{n.get('dismantling', 0)} relaxed them**
    and **{n.get('reallocation', 0)} moved competence between levels of government**. Spain's 2013 reform extended
    coastal concessions and removed 12 settlements from the public domain; in the Maldives, a 2024 amendment allowed
    reclamation in previously protected areas and in 2025 the Environmental Protection Agency was replaced by an
    authority under ministerial control. In 2023 Spain transferred coastal management functions to the Canary Islands
    government.
    """)
    mark = {"expansion": ("triangle-up", "#2b8cbe"), "dismantling": ("triangle-down", "#ef3b2c"),
            "reallocation": ("diamond", "#9e9ac8"), "reform": ("circle", "#969696"), "implementation": ("circle", "#d9d9d9")}
    rowpos = {j: i for i, j in enumerate(ORDER[::-1])}
    fig2 = go.Figure()
    vdem_path = os.path.join(DATA, "regime", "vdem_electoral_democracy.csv")
    if os.path.exists(vdem_path):
        v = pd.read_csv(vdem_path)
        for j, i in rowpos.items():
            s = v[v["jurisdiction"] == j]
            fig2.add_trace(go.Scatter(x=s["year"], y=i - 0.35 + 0.7 * s["electoral_democracy_vdem"], mode="lines",
                                      line=dict(color="rgba(200,200,200,0.45)", width=1.5), showlegend=False,
                                      customdata=s["electoral_democracy_vdem"],
                                      hovertemplate=LAB[j] + " %{x}: V-Dem %{customdata:.2f}<extra></extra>"))
    for d, (sym, c) in mark.items():
        s = t[t["direction"] == d]
        if s.empty:
            continue
        fig2.add_trace(go.Scatter(x=s["year"], y=[rowpos[j] for j in s["jurisdiction"]], mode="markers", name=d,
                                  marker=dict(symbol=sym, size=14, color=c, line=dict(color="white", width=1)),
                                  customdata=s[["instrument", "change"]].values,
                                  hovertemplate="%{x}: %{customdata[0]}<br>%{customdata[1]}<extra></extra>"))
    fig2.update_layout(**LAYOUT, height=440,
                       yaxis=dict(tickvals=list(rowpos.values()), ticktext=[LAB[j] for j in rowpos], range=[-0.6, 4.6]),
                       xaxis=dict(range=[1986, 2027], dtick=5),
                       legend=dict(orientation="h", y=1.08, x=0))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Grey line in each row: V-Dem electoral democracy index of the national government (0 at the bottom of the row, 1 at the top). "
               "Hover a marker for the instrument and what changed.")
    if "electoral_democracy_at_change" in t:
        st.info("""
        **Regime type does not sort the changes.** Rules were added under V-Dem electoral democracy scores from 0.13
        (Fiji, 2011, under military rule) to 0.89 (Spain, 1988), and relaxed at 0.88 (Spain) and 0.56–0.58 (Maldives).
        With five countries this is a description, not a test.
        """)
    pick = st.selectbox("Show the changes for", ["All"] + [LAB[j] for j in ORDER])
    t["Jurisdiction"] = t["jurisdiction"].map(LAB)
    if pick != "All":
        t = t[t["Jurisdiction"] == pick]
    cols = ["Jurisdiction", "date", "instrument", "direction", "change", "verification"]
    if "electoral_democracy_at_change" in t:
        cols.insert(5, "electoral_democracy_at_change")
    st.dataframe(t[cols].rename(columns={"date": "Date", "instrument": "Instrument", "direction": "Direction",
                                         "change": "What changed", "verification": "Source level",
                                         "electoral_democracy_at_change": "V-Dem"}),
                 use_container_width=True, hide_index=True)

# ---------------- 5. Policy brief ----------------
st.markdown("### 5. What It Means for Coastal Policy")
st.success("""
**Policy brief: Distance rules do not fit atolls**

1. **Set height requirements on atolls and low islands.** Minimum floor or ground levels apply to low buildings wherever they stand.
2. **Test proposed rules against where buildings stand**, using open building footprints and bare-earth elevation.
3. **Use bare-earth elevation data** on forested islands; surface models can understate exposure five to eight times.
4. **Check instrument counts against design fit**, since counting laws can rank a government highly when its rules are drawn where few people at risk live.
5. **Track amendments over time.** Exemptions and longer concessions weaken protection without repealing any rule.

The full two-page brief opens from the documentation viewer on the home page.
""")

st.markdown("##### Limits")
st.markdown("""
- The coding was done by one coder; every value carries its source and verification level so it can be rechecked.
- "Not found" is coded 0 but is not proof that a rule does not exist.
- The Lakshadweep setback width and the Maldivian changes of 2024–2025 rest on secondary sources.
- Only national law is compared, not local plans, permits or enforcement, and many buildings predate the rules, so coverage shows design fit, not compliance.
- The Canary figure rests on 192 low buildings, many on port land, with the 100 m width applied to all of them.
- Whether the 2019 Lakshadweep change was a relaxation depends on its 2011 island management plans, not yet verified.
""")

for name, cap in (("fig11_policy_density_intensity.png", "Figure 11 — Policy density, intensity and the same 20 m width"),
                  ("fig12_coastal_policy_timeline.png", "Figure 12 — Coastal rule changes since 1988")):
    pth = os.path.join(FIGURES_DIR, name)
    if os.path.exists(pth):
        st.markdown(f"##### {cap}")
        show_image(pth)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — paper Sections 3.9–3.10, 4.8–4.9 and 6.8; "
    "every number rerun by scripts/run_all.py</p>",
    unsafe_allow_html=True,
)
