"""Check the shoreline distances used in the setback analysis against geodesic distances.

setback_calibration.py measures distance on a local flat approximation (metres per degree
at the mean latitude). This script takes a sample of buildings, finds the nearest shoreline
point again on the WGS84 ellipsoid (Vincenty inverse formula), and reports the difference.

Run from the repository root, after setback_calibration.py:
    python scripts/validation/setback_distance_check.py
"""
import os
import runpy
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

sc = runpy.run_path("scripts/analysis/setback_calibration.py", run_name="setback_lib")
polygons = sc["polygons"]
A, F = 6378137.0, 1 / 298.257223563
B = A * (1 - F)


def vincenty(lon1, lat1, lon2, lat2):
    L = np.radians(lon2 - lon1)
    U1 = np.arctan((1 - F) * np.tan(np.radians(lat1)))
    U2 = np.arctan((1 - F) * np.tan(np.radians(lat2)))
    sU1, cU1, sU2, cU2 = np.sin(U1), np.cos(U1), np.sin(U2), np.cos(U2)
    lam = L.copy()
    for _ in range(100):
        sl, cl = np.sin(lam), np.cos(lam)
        ss = np.sqrt((cU2 * sl) ** 2 + (cU1 * sU2 - sU1 * cU2 * cl) ** 2)
        cs = sU1 * sU2 + cU1 * cU2 * cl
        sig = np.arctan2(ss, cs)
        sa = np.where(ss == 0, 0, cU1 * cU2 * sl / np.where(ss == 0, 1, ss))
        c2a = 1 - sa ** 2
        c2sm = np.where(c2a == 0, 0, cs - 2 * sU1 * sU2 / np.where(c2a == 0, 1, c2a))
        C = F / 16 * c2a * (4 + F * (4 - 3 * c2a))
        lam_new = L + (1 - C) * F * sa * (sig + C * ss * (c2sm + C * cs * (-1 + 2 * c2sm ** 2)))
        if np.nanmax(np.abs(lam_new - lam)) < 1e-12:
            lam = lam_new; break
        lam = lam_new
    u2 = c2a * (A ** 2 - B ** 2) / B ** 2
    Ak = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    Bk = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = Bk * ss * (c2sm + Bk / 4 * (cs * (-1 + 2 * c2sm ** 2) - Bk / 6 * c2sm * (-3 + 4 * ss ** 2) * (-3 + 4 * c2sm ** 2)))
    return B * Ak * (sig - ds)


def shoreline_points(isl, step_deg=2e-5):
    pts = []
    for p in polygons(f"data/boundaries_v2/{isl}_islands_v2.gpkg"):
        for r in p:
            x, y = r[:, 0], r[:, 1]
            if isl == "fiji":
                x = np.where(x < 0, x + 360, x)
            seg = np.hypot(np.diff(x), np.diff(y)); n = np.maximum(np.ceil(seg / step_deg).astype(int), 1)
            for i in range(len(seg)):
                f = np.arange(n[i]) / n[i]
                pts.append(np.c_[x[i] + f * (x[i + 1] - x[i]), y[i] + f * (y[i + 1] - y[i])])
    return np.vstack(pts)


if __name__ == "__main__":
    import glob, sys
    if not glob.glob("data/buildings/*_buildings_setback.csv.gz"):
        print("Skipped: run scripts/analysis/setback_calibration.py with the building files first")
        sys.exit(0)
    rows = []
    for isl in ["maldives", "lakshadweep", "seychelles", "fiji", "canary"]:
        b = pd.read_csv(f"data/buildings/{isl}_buildings_setback.csv.gz")
        b = b[b.on_land & b.elev_m.notna()]
        low = b[b.elev_m <= 1]
        s = pd.concat([low.sample(min(len(low), 1500), random_state=1), b.sample(1500, random_state=2)]).drop_duplicates("id")
        lon = s.lon.to_numpy(); lat = s.lat.to_numpy()
        if isl == "fiji":
            lon = np.where(lon < 0, lon + 360, lon)
        P = shoreline_points(isl)
        k = np.cos(np.radians(lat.mean()))
        tree = cKDTree(np.c_[P[:, 0] * k, P[:, 1]])
        _, idx = tree.query(np.c_[lon * k, lat], k=30)
        d = vincenty(np.repeat(lon[:, None], 30, 1), np.repeat(lat[:, None], 30, 1), P[idx, 0], P[idx, 1]).min(1)
        diff = s.dist_coast_m.to_numpy() - d
        rel = np.abs(diff) / np.maximum(d, 1)
        for sb in [20, 25, 100]:
            flips = ((s.dist_coast_m.to_numpy() <= sb) != (d <= sb)).mean() * 100
            rows.append(dict(island=isl, buildings_checked=len(s), setback_m=sb, pct_classification_changed=round(flips, 2)))
        print(f"{isl:12s} n={len(s):5d}  median |diff| {np.median(np.abs(diff)):.2f} m  95th pct |diff| {np.percentile(np.abs(diff), 95):.2f} m  "
              f"median rel {np.median(rel) * 100:.2f}%")
    out = pd.DataFrame(rows)
    print(out.pivot(index="island", columns="setback_m", values="pct_classification_changed"))
    out.to_csv("data/setback_distance_check.csv", index=False)
    print("wrote data/setback_distance_check.csv")
