import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE
from results import load as load_results, pval

R = load_results()

apply_custom_style()

# Folder where the publication-quality static figures (research_paper_figures.py)
# get saved. Used below to show the "as it appears in the Research Paper" version.
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")

st.markdown("<h1 style='text-align: center;'>🌡️ ECOLOGICAL FINDINGS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #1b4332; font-weight: 400;'>Two Ecosystems, Two Very Different Stories</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
DOUBLE JEOPARDY tests mangrove and coral reef ecosystems **independently**, rather than assuming
both degrade uniformly. Reef heat stress was higher in 2016–2020 than in 1996–2000 at every island
group with mapped reef, although no monotonic trend is statistically established; mangrove area shows
no change in Global Mangrove Watch between 1996 and 2020.
""")

st.markdown("---")

tab1, tab2 = st.tabs(["Coral Reefs — H1 (Partly supported)", "Mangroves — H2 (Not supported)"])

with tab1:
    st.markdown("### Coral Thermal Stress: 1996–2020")
    st.markdown("""
    Coral degradation was measured using **Degree Heating Week (DHW)**, a satellite-derived measure
    of accumulated thermal stress. Values above 4°C-weeks are associated with significant bleaching;
    values above 8°C-weeks are associated with severe bleaching and coral mortality.
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    # Main series: mean over every 5 km cell of mapped reef; the Canary Islands have no
    # mapped reef, so their single offshore cell is shown. Test: correlated seasonal
    # Mann-Kendall (Hirsch and Slack 1984). All values read from data/coral_trend_results.csv.
    _order = ["seychelles", "maldives", "fiji", "lakshadweep", "canary"]
    _top = max(_order[:4], key=lambda i: R["coral_change"][(i, R["coral_series"][i])])
    dhw_data = []
    for col, key in zip((col1, col2, col3, col4, col5), _order):
        ser = R["coral_series"][key]
        ch = R["coral_change"][(key, ser)]
        name = R["label"][key] + (" (offshore cell; no reefs mapped)" if key == "canary" else "")
        dhw_data.append((col, name, f"{ch:+.2f}".replace("-", "−"), f"{R['coral_max'][(key, ser)]:.2f}",
                         key == _top, R["coral_p"][(key, ser)] < 0.05))

    for col, island, change, max_dhw, highlight, trend_significant in dhw_data:
        with col:
            border_color = PALETTE["risk"] if highlight else "rgba(0,150,199,0.3)"
            sig_line = (
                f"<p style='color:{PALETTE['risk']}; font-size:0.65rem; font-weight:700; margin-top:8px;'>✓ trend significant</p>"
                if trend_significant else
                f"<p style='color:{PALETTE['text_muted']}; font-size:0.65rem; margin-top:8px;'>trend not significant</p>"
            )
            st.markdown(f"""
            <div style="background: {PALETTE['card_bg']}; border-radius: 12px; padding: 14px;
                        text-align: center; min-height: 175px; border: 2px solid {border_color};">
                <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">{island}</p>
                <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 4px;">2016–20 vs 1996–2000</p>
                <p style="color: {PALETTE['risk'] if change.startswith('+') else PALETTE['mint']}; font-weight: 800; font-size: 1.3rem; margin-bottom: 8px;">{change}</p>
                <p style="color: {PALETTE['text_muted']}; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 2px;">Max DHW</p>
                <p style="color: {PALETTE['navy']}; font-weight: 700; font-size: 1rem; margin: 0;">{max_dhw}°C-wk</p>
                {sig_line}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    _s = R["coral_series"]
    st.warning(f"""
    **Heat stress was higher in 2016–2020 than in 1996–2000 at all four island groups with mapped
    reef**, most in Seychelles (+{R['coral_change'][('seychelles', 'reef_cells')]:.2f} °C-weeks on average over its reef
    cells, peak {R['coral_max'][('seychelles', 'reef_cells')]:.1f} °C-weeks in 2016). A monotonic trend over the full
    1996–2020 series is **not** established: the correlated seasonal Mann-Kendall test, which allows for
    the strong month-to-month dependence of a 12-week running sum like DHW, gives
    {pval(R['coral_p'][('seychelles', 'reef_cells')])} for Seychelles and {pval(R['coral_p'][('maldives', 'reef_cells')])} for the Maldives.
    An ordinary seasonal test, which treats neighbouring months as independent, would have called both
    significant ({pval(R['coral_p_uncorrected'][('seychelles', 'reef_cells')])} and {pval(R['coral_p_uncorrected'][('maldives', 'reef_cells')])});
    that was the first version's mistake. The Canary Islands value comes from an offshore cell with no mapped reef.
    """)

    st.markdown("")
    st.markdown("##### Figure 5 — As it appears in the Research Paper")
    fig4_path = os.path.join(FIGURES_DIR, "fig4_coral_thermal_stress_trends.png")
    if os.path.exists(fig4_path):
        st.image(fig4_path, use_container_width=True)
    else:
        st.caption("Figure not found yet — run research_paper_figures.py once to generate it.")

with tab2:
    st.markdown("### Mangrove Extent at Three Epochs")
    st.markdown("""
    Mangrove extent was measured at **three epochs** (1996, 2010, 2020) from Global Mangrove Watch v3,
    with area calculated in an equal-area projection. The 1996 and 2020 layers are derived by change
    detection from the 2010 baseline, so they are not independent surveys.
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
    shows a marginal net increase. Note that the Global Mangrove Watch 1996 and 2020 layers are
    change maps built on its 2010 baseline, so the three dates are not fully independent surveys. This does not support Hypothesis H2 as originally framed, and
    is reported transparently as the observed result of this three-point snapshot comparison —
    not a continuous trend test comparable to the coral analysis — rather than adjusted to
    fit the original hypothesis.
    """)

    st.markdown("")
    st.markdown("##### Figure 4 — As it appears in the Research Paper")
    fig5_path = os.path.join(FIGURES_DIR, "fig5_mangrove_extent_over_time.png")
    if os.path.exists(fig5_path):
        st.image(fig5_path, use_container_width=True)
    else:
        st.caption("Figure not found yet — run research_paper_figures.py once to generate it.")

st.markdown("---")

st.markdown("### Why the Difference Matters")
st.markdown("""
Over 1996–2020 the two buffers did not move together: mean reef heat stress was higher in the later
period, driven largely by the 2016 event, while Global Mangrove Watch detects no change in mangrove
area. With five island groups this describes these cases; it is a reason to assess the two
ecosystems separately rather than as one buffer, not a general result.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>DOUBLE JEOPARDY — Source: NOAA Coral Reef Watch, Global Mangrove Watch</p>",
    unsafe_allow_html=True,
)