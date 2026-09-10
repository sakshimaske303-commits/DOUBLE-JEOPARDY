from population_weighted_exposure import ISLANDS
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds, Window
import geopandas as gpd

for name in ["Maldives", "Lakshadweep"]:
    cfg = ISLANDS[name]
    minx, miny, maxx, maxy = cfg["windows"][0]
    with rasterio.open(cfg["population"]) as src:
        window = from_bounds(minx, miny, maxx, maxy, transform=src.transform)
        window = window.round_offsets().round_lengths()
        window = window.intersection(Window(0, 0, src.width, src.height))
        arr = src.read(1, window=window).astype("float32")
        nodata = src.nodata
        if nodata is not None:
            arr = np.where(arr == nodata, 0, arr)
        arr = np.where(arr < 0, 0, arr)
        transform = src.window_transform(window)
        crs = src.crs

    gdf = gpd.read_file(cfg["boundary"])
    if gdf.crs is not None and str(gdf.crs) != str(crs):
        gdf = gdf.to_crs(crs)
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]

    raw_total = arr.sum()
    print(f"\n{name} (raw total in this window: {raw_total:,.0f})")
    for buffer_m in [0, 200, 500, 1000, 2000, 5000]:
        if buffer_m == 0:
            geoms = [g.__geo_interface__ for g in gdf.geometry]
        else:
            buf_deg = buffer_m / 111000  # rough degrees-per-meter conversion
            geoms = [g.buffer(buf_deg).__geo_interface__ for g in gdf.geometry]
        mask = geometry_mask(geoms, out_shape=arr.shape, transform=transform, invert=True, all_touched=True)
        captured = arr[mask].sum()
        pct_of_window = (captured / raw_total * 100) if raw_total > 0 else float("nan")
        print(f"  buffer +{buffer_m:>5}m: land pixels={mask.sum():>8,}  population captured={captured:>10,.0f}  ({pct_of_window:5.1f}% of window total)")
