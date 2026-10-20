import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pct, source_label

apply_custom_style()

# Every number on this page is read from the pipeline's CSVs (dashboard/results.py),
# rewritten 2026-10-11 so it cannot drift from the analysis again.
R = load_results()
P = R["primary"]
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")
ORDER = sorted(R["islands"], key=lambda i: R["people"][(i, P)], reverse=True)

st.markdown("<h1 style='text-align: center;'>📉 PHYSICAL EXPOSURE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #67E8F9; font-weight: 400;'>People and Places at or Below 1 m</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown(f"""
Exposure is measured as the **share of people living on land at or below 1 m** (WorldPop 2020, 100 m),
and, as a second measure, the share of **named places** (OpenStreetMap points) at or below 1 m. Heights
come from **{source_label(P)}**, with Copernicus GLO-30 kept for comparison. Heights are above the
EGM2008 geoid, used as an approximation of mean sea level; this is a threshold on elevation, not a flood model.
""")

st.markdown("---")
st.markdown("### Share of People at or Below 1 m")

cols = st.columns(5)
for col, isl in zip(cols, ORDER):
    v = R["people"][(isl, P)]
    v_cop = R["people"].get((isl, "copernicus"))
    hi = v >= 5
    color = PALETTE["risk"] if hi else PALETTE["cyan"]
    with col:
        st.markdown(f"""
        <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 16px;
                    text-align: center; min-height: 190px; border: 1.5px solid rgba(34,211,238,0.3);">
            <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 10px;">{R['label'][isl]}</p>
            <p style="color: {color}; font-weight: 900; font-size: 2rem; margin-bottom: 4px;">{v:.1f}%</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.75rem; margin-bottom: 10px;">of people at or below 1 m</p>
            <p style="color: {PALETTE['text_muted']}; font-size: 0.72rem; margin: 0;">
                {R['people_n'][(isl, P)]:,.0f} of {R['people_total'][(isl, P)]:,.0f} people<br>
                surface model: {v_cop:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")
st.markdown("##### Figure 2 — As it appears in the Research Paper")
fig2_path = os.path.join(FIGURES_DIR, "fig2_physical_exposure_by_island.png")
if os.path.exists(fig2_path):
    st.image(fig2_path, use_container_width=True)

st.info(f"""
**Why two elevation models.** Copernicus GLO-30 is a *surface* model: over a wooded or built-up
atoll it measures the tops of trees and roofs, not the ground. DeltaDTM (Pronk et al. 2024) corrects
Copernicus with ICESat-2 and GEDI lidar to a bare-earth model of the coastal zone. On the Maldives the
share of people at or below 1 m rises from {pct(R['people'][('maldives', 'copernicus')])} to
{pct(R['people'][('maldives', 'deltadtm')])}, and on Lakshadweep from {pct(R['people'][('lakshadweep', 'copernicus')])}
to {pct(R['people'][('lakshadweep', 'deltadtm')])}. Where the Copernicus surface is above 30 m the ground is
treated as high terrain and DeltaDTM is not used: on small forested granite islands in Seychelles
DeltaDTM otherwise reads a hill as sea level.
""")

st.markdown("---")
st.markdown("### Two Ways to Count: People and Named Places")
st.markdown("""
Most OpenStreetMap "settlement" points on these islands are names of islands and islets, not
villages, and some are labels for whole atolls sitting in open water. That is why people are the main
measure. The share of named places is kept as a second measure because it shows where *mapped places*
sit, including uninhabited and resort islets.
""")

names = [R["label"][i] for i in ORDER]
fig = go.Figure()
fig.add_trace(go.Bar(x=names, y=[R["places"][(i, P)] for i in ORDER], name="Named places",
                     marker_color=PALETTE["cyan"],
                     text=[f"{R['places'][(i, P)]:.1f}%" for i in ORDER], textposition="outside"))
fig.add_trace(go.Bar(x=names, y=[R["people"][(i, P)] for i in ORDER], name="People (main measure)",
                     marker_color=PALETTE["green"],
                     text=[f"{R['people'][(i, P)]:.1f}%" for i in ORDER], textposition="outside"))
top = max(max(R["places"][(i, P)] for i in ORDER), max(R["people"][(i, P)] for i in ORDER))
fig.update_layout(barmode="group", template="plotly_dark", height=420,
                  yaxis=dict(title="% at or below 1 m", range=[0, top * 1.25]),
                  font=dict(family="Poppins", color="#FFD60A"), legend=dict(font=dict(color="#F1F1F1")),
                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20))
st.plotly_chart(fig, use_container_width=True)

cov = {i: R["coverage"][(i, P)] for i in R["islands"]}
low_cov = [f"{R['label'][i]} ({cov[i]:.0f}%)" for i in R["islands"] if cov[i] < 80]
st.warning(f"""
**Which island is "most exposed" depends on what is counted.** By people, the Maldives lead
({pct(R['people'][('maldives', P)])}). By named places, the Maldives ({pct(R['places'][('maldives', P)])}) and
Seychelles ({pct(R['places'][('seychelles', P)])}) are close, because Seychelles has many small low coral islets with
few residents. Places with no usable elevation (labels in open water with no land within 60 m) are left out,
not counted as safe; usable coverage is below 80% for {', '.join(low_cov) if low_cov else 'no island'}.
""")

fig3_path = os.path.join(FIGURES_DIR, "fig3_settlement_vs_population_weighted.png")
if os.path.exists(fig3_path):
    st.markdown("##### Figure 3 — As it appears in the Research Paper")
    st.image(fig3_path, use_container_width=True)

st.markdown("---")
st.markdown("### Try a Different Water Level")
st.markdown(f"""
Move the slider to recount the share of **named places** at or below a different height, using the
place-level elevations ({source_label(P)}).
""")


@st.cache_data
def load_elevations():
    return pd.read_csv(os.path.join(PROJECT_ROOT, "dashboard", "static", "settlement_elevations.csv"))


elev_df = load_elevations()
threshold = st.slider("Water level (m above EGM2008)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)
island_order = ["Maldives", "Seychelles", "Lakshadweep", "Fiji", "Canary"]
display = ["Maldives", "Seychelles", "Lakshadweep", "Fiji", "Canary Islands"]
vals, n_all = [], 0
for island in island_order:
    sub = elev_df[elev_df["island"] == island]
    n_all += len(sub)
    vals.append((sub["elevation_m"] <= threshold).mean() * 100 if len(sub) else 0)
fig_d = go.Figure(go.Bar(x=display, y=vals, marker_color=PALETTE["cyan"],
                         text=[f"{v:.1f}%" for v in vals], textposition="outside"))
fig_d.update_layout(template="plotly_dark", height=400, yaxis=dict(title=f"% of named places at or below {threshold} m",
                    range=[0, max(vals + [1]) * 1.25]), font=dict(family="Poppins", color="#FFD60A"),
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=40, l=20, r=20))
st.plotly_chart(fig_d, use_container_width=True)
st.caption(f"Recalculated live from {n_all:,} place-level elevation samples.")

st.info(f"""
**Sensitivity to the water level.** At 0.5 m and 1.5 m the share of named places changes as follows:
Maldives {R['places_05'][('maldives', P)]:.1f}% → {R['places_15'][('maldives', P)]:.1f}%,
Seychelles {R['places_05'][('seychelles', P)]:.1f}% → {R['places_15'][('seychelles', P)]:.1f}%,
Lakshadweep {R['places_05'][('lakshadweep', P)]:.1f}% → {R['places_15'][('lakshadweep', P)]:.1f}%,
Fiji {R['places_05'][('fiji', P)]:.1f}% → {R['places_15'][('fiji', P)]:.1f}%,
Canary Islands {R['places_05'][('canary', P)]:.1f}% → {R['places_15'][('canary', P)]:.1f}%.
On a bare-earth model the atolls are very sensitive to the chosen level: half of the Maldives' named
places sit at or below 1.5 m.
""")

st.markdown("---")
st.markdown("### What These Numbers Cannot Say")
st.info("""
- They are not flood maps: no tides, storm surge, waves or connection to the sea are modelled.
- Heights are relative to EGM2008, an approximation of mean sea level, not to high tide.
- DeltaDTM's mean absolute error against airborne lidar is about 0.4–0.5 m, which is large next to a
  1 m threshold; the comparison between models matters more than any single percentage.
- WorldPop is a modelled population surface, not a census.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Sources: DeltaDTM v1.1 (Pronk et al. 2024), "
    "Copernicus DEM GLO-30, WorldPop 2020, OpenStreetMap</p>",
    unsafe_allow_html=True,
)
