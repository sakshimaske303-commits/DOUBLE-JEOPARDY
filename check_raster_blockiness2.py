import rasterio
import numpy as np
from rasterio.windows import Window

SAMPLES = [
    ("Maldives", "data/population/maldives_population_clean.tif", 73.5090, 4.1755),   # Male
    ("Lakshadweep", "data/population/lakshadweep_population_clean.tif", 72.6420, 10.5669),  # Kavaratti
]

for name, path, lon, lat in SAMPLES:
    with rasterio.open(path) as src:
        print(f"\n{name}  (pixel size: {src.res})")
        row, col = src.index(lon, lat)
        half = 100
        window = Window(col - half, row - half, 2 * half, 2 * half)
        window = window.intersection(Window(0, 0, src.width, src.height))
        arr = src.read(1, window=window).astype("float32")
        nodata = src.nodata
        if nodata is not None:
            arr = np.where(arr == nodata, 0, arr)
        arr = np.where(arr < 0, 0, arr)

        r0, c0 = np.unravel_index(np.argmax(arr), arr.shape)
        print(f"  max value in window: {arr[r0, c0]:.2f} at local row={r0}, col={c0}")
        r1, r2 = max(0, r0 - 10), min(arr.shape[0], r0 + 10)
        c1, c2 = max(0, c0 - 10), min(arr.shape[1], c0 + 10)
        print("  20x20 block around the densest pixel:")
        for r in range(r1, r2):
            print("   ", " ".join(f"{v:7.2f}" for v in arr[r, c1:c2]))

        # Blockiness test on NONZERO pixels only, comparing pixels 10 apart
        # (10px * ~93m = ~930m -- tests for ~1km-cell upsampling artifacts)
        nz = arr > 0
        eq_right_10 = (arr[:, :-10] == arr[:, 10:]) & nz[:, :-10] & nz[:, 10:]
        eq_down_10 = (arr[:-10, :] == arr[10:, :]) & nz[:-10, :] & nz[10:, :]
        denom_right = np.sum(nz[:, :-10] & nz[:, 10:])
        denom_down = np.sum(nz[:-10, :] & nz[10:, :])
        pct_right = (eq_right_10.sum() / denom_right * 100) if denom_right else float("nan")
        pct_down = (eq_down_10.sum() / denom_down * 100) if denom_down else float("nan")
        print(f"  nonzero pixels matching the one 10px to the right: {eq_right_10.sum()}/{denom_right} ({pct_right:.1f}%)")
        print(f"  nonzero pixels matching the one 10px below:        {eq_down_10.sum()}/{denom_down} ({pct_down:.1f}%)")
        print(f"  total nonzero pixels in this window: {nz.sum()} / {arr.size}")
