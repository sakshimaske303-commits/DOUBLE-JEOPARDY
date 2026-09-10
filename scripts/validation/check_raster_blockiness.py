import rasterio
import numpy as np
from rasterio.windows import Window

# known population centers to sample around
SAMPLES = [
    ("Maldives", "data/population/maldives_population_clean.tif", 73.5090, 4.1755),   # Male
    ("Lakshadweep", "data/population/lakshadweep_population_clean.tif", 72.6420, 10.5669),  # Kavaratti
]

for name, path, lon, lat in SAMPLES:
    with rasterio.open(path) as src:
        print(f"\n{name}")
        print(f"  pixel size (deg): {src.res}")
        row, col = src.index(lon, lat)
        half = 50
        window = Window(col - half, row - half, 2 * half, 2 * half)
        window = window.intersection(Window(0, 0, src.width, src.height))
        arr = src.read(1, window=window).astype("float32")
        nodata = src.nodata
        if nodata is not None:
            arr = np.where(arr == nodata, 0, arr)

        print(f"  window shape: {arr.shape}, unique values in window: {len(np.unique(arr))}")
        print("  sample 12x12 block (top-left of window):")
        for r in range(min(12, arr.shape[0])):
            print("   ", " ".join(f"{v:7.2f}" for v in arr[r, :12]))

        same_below = np.mean(arr[:-1, :] == arr[1:, :])
        same_right = np.mean(arr[:, :-1] == arr[:, 1:])
        print(f"  fraction equal to pixel directly below: {same_below:.3f}")
        print(f"  fraction equal to pixel directly to the right: {same_right:.3f}")
