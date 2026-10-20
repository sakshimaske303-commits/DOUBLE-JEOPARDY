"""Builds dashboard/static/settlement_elevations.csv, the data behind the
Physical Exposure page's live threshold slider.

Rewritten 2026-10-10 (Forensic Review): uses the same shared DEM rule as the
analysis (scripts/common/dem_sampling.py), so the slider can no longer count
NoData (-32767) or out-of-extent points as "at risk". Only settlements with a
usable elevation (status valid, snapped_to_land or above_10m) are written.

Run from anywhere:  python dashboard/precompute_elevations.py
"""
import os
import sys

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from scripts.common.dem_sampling import ISLANDS, KEPT_STATUSES, primary_source, sample_settlements  # noqa: E402

# Same elevation source as the main results (DeltaDTM when prepared, 2026-10-11).
SOURCE = primary_source()
frames = []
for island in ISLANDS:
    df = sample_settlements(island, source=SOURCE)
    kept = df[df["status"].isin(KEPT_STATUSES)]
    print(f"{island}: {len(kept)}/{len(df)} settlements with usable elevation")
    frames.append(pd.DataFrame({"island": island.capitalize(), "elevation_m": kept["elevation_m"]}))

out = os.path.join(ROOT, "dashboard", "static", "settlement_elevations.csv")
pd.concat(frames).to_csv(out, index=False)
print(f"Saved {out} (elevation source: {SOURCE})")
