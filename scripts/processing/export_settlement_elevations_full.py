"""SUPERSEDED (2026-10-10). The per-settlement CSVs in
data/settlement_elevations_full/ are now written by
scripts/analysis/slr_exposure_analysis.py, using the shared DEM rule in
scripts/common/dem_sampling.py (NoData, out-of-extent and water-pixel handling
identical for all five islands). This file is kept only so old instructions
that call it still work; it simply runs that script.
"""
import os
import runpy

runpy.run_path(
    os.path.join(os.path.dirname(__file__), "..", "analysis", "slr_exposure_analysis.py"),
    run_name="__main__",
)
