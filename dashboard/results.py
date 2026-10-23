"""Every number the dashboard shows, read from the pipeline's CSV outputs.

Added 2026-10-11 so the pages can no longer go stale: run scripts/run_all.py and
the dashboard picks up the new numbers. Nothing here is typed in by hand except
the mangrove areas (from scripts/analysis/mangrove_3point_comparison.py, which
prints them but writes no CSV).
"""
import os

import pandas as pd

try:
    import streamlit as st
    _cache = st.cache_data
except Exception:  # allows import outside Streamlit
    def _cache(f):
        return f

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]
LABEL = {"maldives": "Maldives", "seychelles": "Seychelles", "fiji": "Fiji",
         "canary": "Canary Islands", "lakshadweep": "Lakshadweep"}
POP_KEY = {"Maldives": "maldives", "Seychelles": "seychelles", "Fiji": "fiji",
           "Canary Islands": "canary", "Lakshadweep": "lakshadweep"}

# Global Mangrove Watch v3, km2 in EPSG:6933 (mangrove_3point_comparison.py)
MANGROVES = {
    "maldives": (0.97, 0.97, 0.97),
    "seychelles": (3.83, 3.84, 3.83),
    "fiji": (485.72, 487.97, 488.41),
}


def _read(name):
    path = os.path.join(DATA, name)
    return pd.read_csv(path) if os.path.exists(path) else None


@_cache
def load():
    R = {"islands": ISLANDS, "label": LABEL, "mangroves": MANGROVES}

    # exposure: people (main) and named places, by elevation source
    pop = _read("population_weighted_exposure_by_source.csv")
    if pop is None:
        pop = _read("population_weighted_exposure.csv")
        pop["elevation_source"] = pop.get("elevation_source", "copernicus")
    pop["key"] = pop["island"].map(POP_KEY)
    R["people"] = {(r.key, r.elevation_source): r.pct_at_risk for r in pop.itertuples()}
    R["people_n"] = {(r.key, r.elevation_source): r.pop_at_risk for r in pop.itertuples()}
    R["people_total"] = {(r.key, r.elevation_source): r.pop_with_elevation for r in pop.itertuples()}
    R["sources"] = sorted(pop["elevation_source"].unique(), key=lambda s: s != "deltadtm")
    R["primary"] = "deltadtm" if "deltadtm" in R["sources"] else "copernicus"

    pl = _read("slr_exposure_summary_by_source.csv")
    if pl is None:
        pl = _read("slr_exposure_summary.csv")
        pl["elevation_source"] = pl.get("elevation_source", "copernicus")
    R["places"] = {(r.island, r.elevation_source): r.pct_at_risk for r in pl.itertuples()}
    R["places_05"] = {(row["island"], row["elevation_source"]): row["pct_at_risk_0.5m"] for _, row in pl.iterrows()}
    R["places_15"] = {(row["island"], row["elevation_source"]): row["pct_at_risk_1.5m"] for _, row in pl.iterrows()}
    R["places_n"] = {(r.island, r.elevation_source): (int(r.at_risk), int(r.total), int(r.n_settlements))
                     for r in pl.itertuples()}
    R["coverage"] = {(r.island, r.elevation_source): r.coverage_pct for r in pl.itertuples()}

    # coral
    cor = _read("coral_trend_results.csv")
    pcol = "csmk_p" if "csmk_p" in cor.columns else "smk_calendar_p"
    R["coral_p"] = {(r["island"], r["series"]): r[pcol] for _, r in cor.iterrows()}
    # Uncorrected seasonal test on the SAME monthly series as csmk_p (like-for-like comparison).
    ucol = "monthly_smk_p" if "monthly_smk_p" in cor.columns else "smk_calendar_p"
    R["coral_p_uncorrected"] = {(r["island"], r["series"]): r[ucol] for _, r in cor.iterrows()}
    R["coral_change"] = {(r["island"], r["series"]): r["period_change_2016_20_vs_1996_2000"] for _, r in cor.iterrows()}
    R["coral_max"] = {(r["island"], r["series"]): r["max_dhw"] for _, r in cor.iterrows()}

    def coral_main(i):
        return "reef_cells" if (i, "reef_cells") in R["coral_p"] else "single_cell"
    R["coral_series"] = {i: coral_main(i) for i in ISLANDS}

    # compound score
    cvs = _read("compound_vulnerability_scores.csv").set_index("island")
    R["cvs"] = cvs["compound_vulnerability_score"].to_dict()
    R["cvs_table"] = cvs
    sweep = _read("compound_weighting_sweep.csv")
    tops = sweep["rank_order"].str.split(" > ").str[0]
    change = sweep.loc[tops != tops.shift(), "exposure_weight"].tolist()[1:]
    R["cvs_crossover"] = change[0] if change else None
    R["cvs_sweep"] = sweep

    # governance
    gov = _read("governance_alignment_summary.csv").set_index("metric")
    g = gov.loc["pct_coastal_zone_protected"] if "pct_coastal_zone_protected" in gov.index else gov.iloc[0]
    R["gov"] = {"r": g["pearson_r"], "p": g["pearson_p"], "n": int(g["n"]), "lo": g["ci_low"], "hi": g["ci_high"],
                "rho": g["spearman_rho"], "loo_no_sey": g.get("loo_r_without_seychelles")}
    wd = _read("wdpa_coastal_normalized.csv").set_index("island")
    R["protected"] = wd["pct_coastal_zone_protected"].to_dict()
    R["protected_strict"] = wd["pct_coastal_zone_strict_iucn"].to_dict()

    # NDBI (supplementary)
    # coastal setbacks (building level, added 2026-10-23); optional
    sb = _read("setback_calibration_summary.csv")
    R["setback"] = None if sb is None else sb.set_index(["island", "variant"])
    R["setback_curve"] = _read("setback_coverage_curve.csv")

    nd = _read("ndbi_land_change.csv")
    R["ndbi"] = {} if nd is None else {(r["island"], r["zone"]): (r["mean_change"], r["ci95_low"], r["ci95_high"])
                                        for _, r in nd.iterrows()}
    return R


def pct(x, d=1):
    return f"{x:.{d}f}%"


def pval(p):
    return "p < 0.001" if p < 0.001 else (f"p = {p:.3f}" if p < 0.01 else f"p = {p:.2f}")


def source_label(s):
    return {"deltadtm": "DeltaDTM (bare earth)", "copernicus": "Copernicus GLO-30 (surface)"}.get(s, s)
