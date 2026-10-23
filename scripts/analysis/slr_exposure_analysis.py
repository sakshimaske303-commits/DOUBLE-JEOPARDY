"""Settlement-based physical exposure to a 1 m sea-level-rise threshold."""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.common.dem_sampling import (ISLANDS, KEPT_STATUSES, available_sources,  # noqa: E402
                                         primary_source, repo_path, sample_settlements)

SLR_THRESHOLD_M = 1.0
SENSITIVITY_THRESHOLDS_M = [0.5, 1.0, 1.5]
OUT_DIR = repo_path("data", "settlement_elevations_full")


def pct(n, d):
    return (n / d * 100) if d else float("nan")


def analyze_island(island, source="copernicus", primary=True):
    df = sample_settlements(island, snap_zero_to_land=True, source=source)
    kept = df[df["status"].isin(KEPT_STATUSES)]
    strict = df[df["status"].isin({"valid", "above_10m"})]  # water-pixel points excluded instead of snapped

    df["at_risk"] = df["status"].isin(KEPT_STATUSES) & (df["elevation_m"] <= SLR_THRESHOLD_M)
    os.makedirs(OUT_DIR, exist_ok=True)
    suffix = "" if primary else f"_{source}"
    df.to_csv(os.path.join(OUT_DIR, f"{island}{suffix}.csv"), index=False)

    counts = df["status"].value_counts()
    result = {
        "island": island,
        "elevation_source": source,
        "dem_file": df["dem_file"].iloc[0] if len(df) else "",
        "n_settlements": len(df),
        "n_valid": int(counts.get("valid", 0)),
        "n_snapped_to_land": int(counts.get("snapped_to_land", 0)),
        "n_water_no_land_nearby": int(counts.get("water_no_land_nearby", 0)),
        "n_nodata": int(counts.get("nodata", 0)),
        "n_out_of_extent": int(counts.get("out_of_extent", 0)),
        "n_above_10m": int(counts.get("above_10m", 0)),
        "n_deltadtm_nodata": int(counts.get("deltadtm_nodata", 0)),
        "total": len(kept),
        "coverage_pct": pct(len(kept), len(df)),
        "at_risk": int((kept["elevation_m"] <= SLR_THRESHOLD_M).sum()),
        "pct_at_risk": pct((kept["elevation_m"] <= SLR_THRESHOLD_M).sum(), len(kept)),
    }
    for t in SENSITIVITY_THRESHOLDS_M:
        result[f"pct_at_risk_{t}m"] = pct((kept["elevation_m"] <= t).sum(), len(kept))
    result["strict_total"] = len(strict)
    result["strict_pct_at_risk_1.0m"] = pct((strict["elevation_m"] <= SLR_THRESHOLD_M).sum(), len(strict))

    print(f"{island.upper()} [{source}] ({result['dem_file']})")
    print(f"  status counts: {counts.to_dict()}")
    print(f"  coverage: {result['total']}/{len(df)} settlements ({result['coverage_pct']:.1f}%)")
    print(f"  at risk <= {SLR_THRESHOLD_M} m: {result['at_risk']} ({result['pct_at_risk']:.1f}%)")
    for t in SENSITIVITY_THRESHOLDS_M:
        print(f"    @ {t} m: {result[f'pct_at_risk_{t}m']:.2f}%")
    print(f"  strict rule (water-pixel points excluded): {result['strict_pct_at_risk_1.0m']:.2f}% "
          f"of {result['strict_total']}\n")
    if result["coverage_pct"] < 80:
        print(f"  WARNING: only {result['coverage_pct']:.0f}% of {island} settlements have a usable "
              f"elevation. Fix DEM coverage before reporting this island's figure.\n")
    return result, df


def place_type_table(frames):
    """Exposure by OSM place type for the primary source."""
    rows = []
    for island, df in frames.items():
        for place, g in df.groupby(df["place"].fillna("(none)")):
            kept = g[g["status"].isin(KEPT_STATUSES)]
            rows.append({"island": island, "place": place, "n": len(g), "n_usable": len(kept),
                         "n_at_risk_1m": int((kept["elevation_m"] <= SLR_THRESHOLD_M).sum())})
    out = pd.DataFrame(rows).sort_values(["island", "n"], ascending=[True, False])
    out.to_csv(repo_path("data", "named_places_by_type.csv"), index=False)
    print("Saved: data/named_places_by_type.csv")


def main():
    primary = primary_source()
    results, frames = [], {}
    for source in available_sources():
        print("=" * 30 + f" elevation source: {source}" + (" (primary)" if source == primary else "") + " " + "=" * 30)
        for island in ISLANDS:
            try:
                res, df = analyze_island(island, source, primary=(source == primary))
                results.append(res)
                if source == primary:
                    frames[island] = df
            except Exception as e:  # keep going so one missing file doesn't hide the others
                print(f"{island.upper()} [{source}]: ERROR - {e}\n")
    allres = pd.DataFrame(results)
    allres.to_csv(repo_path("data", "slr_exposure_summary_by_source.csv"), index=False)
    allres[allres["elevation_source"] == primary].to_csv(repo_path("data", "slr_exposure_summary.csv"), index=False)
    print(f"Saved: data/slr_exposure_summary.csv (primary source: {primary}) and "
          f"data/slr_exposure_summary_by_source.csv")
    if len(allres["elevation_source"].unique()) > 1:
        piv = allres.pivot(index="island", columns="elevation_source", values="pct_at_risk").round(2)
        print("\n% of named places at or below 1 m, by elevation source:\n" + piv.to_string())
    place_type_table(frames)


if __name__ == "__main__":
    main()
