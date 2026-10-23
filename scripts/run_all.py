"""Run the whole DOUBLE JEOPARDY analysis in order.

Run from the repository root:
    python scripts/run_all.py            # analysis + figures (needs data/ rasters present)
    python scripts/run_all.py --download # first fetch DEM tiles and reef-cell DHW
"""
import os
import runpy
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

DOWNLOAD_STEPS = [
    "scripts/acquisition/download_copernicus_dem_tiles.py",
    "scripts/acquisition/download_dhw_reef_cells.py",
]
STEPS = [
    # DeltaDTM (bare earth): extracts the needed tiles from data/terrain/deltadtm/zips/
    # and builds the VRTs. Safe to rerun. Without it, results fall back to Copernicus.
    "scripts/acquisition/prepare_deltadtm_tiles.py",
    "scripts/analysis/slr_exposure_analysis.py",
    "scripts/analysis/population_weighted_exposure.py",
    "scripts/analysis/coral_trend_test.py",
    "scripts/validation/coral_trend_check.py",
    "scripts/analysis/mangrove_3point_comparison.py",
    "scripts/analysis/compound_vulnerability_score.py",
    "scripts/processing/wdpa_coastal_buffer.py",
    "scripts/validation/boundary_area_validation.py",
    "scripts/analysis/governance_correlation_test.py",
    "scripts/analysis/ndbi_land_change.py",
    # Building-level setback calibration: needs data/buildings/*_building_points.csv.gz
    # (download_buildings_overture.py + export_building_points.py); skips cleanly if absent.
    "scripts/analysis/setback_calibration.py",
    "scripts/validation/setback_distance_check.py",
    "scripts/figures/research_paper_figures.py",
    "scripts/figures/setback_example_maps.py",
    "scripts/figures/map1_vulnerability_score.py",
    "scripts/figures/study_area_map.py",
    "scripts/figures/build_interactive_plots.py",
    "scripts/figures/build_slr_exposure_map.py",
    "scripts/figures/build_encroachment_map.py",
    "dashboard/precompute_elevations.py",
]


def run(path):
    print("\n" + "=" * 78 + f"\n>>> {path}\n" + "=" * 78, flush=True)
    t = time.time()
    saved = sys.argv
    sys.argv = [path]
    try:
        runpy.run_path(path, run_name="__main__")
    finally:
        sys.argv = saved
    print(f"<<< done in {time.time() - t:.0f}s")


if __name__ == "__main__":
    steps = (DOWNLOAD_STEPS if "--download" in sys.argv else []) + STEPS
    failed = []
    for step in steps:
        try:
            run(step)
        except SystemExit as e:
            if e.code not in (0, None):
                failed.append((step, f"exit {e.code}"))
        except Exception as e:
            print(f"!!! {step} failed: {e}")
            failed.append((step, str(e)))
    if failed:
        print(f"\nPARTIAL RUN: {len(failed)} of {len(steps)} steps failed. Outputs of these steps were NOT regenerated:")
        for step, err in failed:
            print(f"  - {step}: {err}")
        sys.exit(1)
    print(f"\nCOMPLETE RUN: all {len(steps)} steps ran.")
