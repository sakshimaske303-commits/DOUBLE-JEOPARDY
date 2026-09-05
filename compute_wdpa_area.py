import geopandas as gpd
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary"]  # lakshadweep excluded, no WDPA dataset available


def compute_wdpa_area(island):
    filepath = f"data/ecosystem_buffers/{island}_wdpa.gpkg"
    gdf = gpd.read_file(filepath)

    # Reproject to equal-area CRS for accurate km2 calculation
    gdf_proj = gdf.to_crs("EPSG:6933")
    total_area_km2 = gdf_proj.geometry.area.sum() / 1_000_000

    return total_area_km2


def main():
    results = []
    for island in ISLANDS:
        try:
            area = compute_wdpa_area(island)
            results.append({"island": island, "wdpa_area_km2": round(area, 2)})
            print(f"{island.upper()}: {area:.2f} km2 protected")
        except Exception as e:
            print(f"{island.upper()}: ERROR - {e}")

    # No WDPA protected-area dataset was available for Lakshadweep, so it is
    # reported here as 0.0 km2 as a missing-data placeholder, NOT a measured,
    # confirmed absence of protection.
    results.append({"island": "lakshadweep", "wdpa_area_km2": 0.0})
    print("LAKSHADWEEP: 0.00 km2 protected (no WDPA dataset available, not a confirmed zero)")

    df = pd.DataFrame(results)
    df.to_csv("data/wdpa_area_by_island.csv", index=False)
    print("\nSaved: data/wdpa_area_by_island.csv")


if __name__ == "__main__":
    main()