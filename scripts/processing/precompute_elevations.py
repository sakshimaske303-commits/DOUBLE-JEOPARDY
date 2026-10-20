"""SUPERSEDED (2026-10-10): the dashboard's slider data is built by
dashboard/precompute_elevations.py, which uses the shared DEM rule in
scripts/common/dem_sampling.py. This older copy read the pre-fix Maldives /
Lakshadweep rasters and had no NoData handling; it now just runs the
dashboard version so there is only one implementation.
"""
import os
import runpy

runpy.run_path(
    os.path.join(os.path.dirname(__file__), "..", "..", "dashboard", "precompute_elevations.py"),
    run_name="__main__",
)
