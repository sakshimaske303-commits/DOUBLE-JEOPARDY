"""Building footprints for the five island groups from Overture Maps.

Run from the repository root:
    python scripts/acquisition/download_buildings_overture.py
"""
import os
import subprocess
import sys

OUT_DIR = "data/buildings"
BOXES = {
    "maldives":    [(72.55, -0.80, 73.90, 7.25)],
    "lakshadweep": [(71.90, 8.10, 74.00, 12.50)],
    "seychelles":  [(46.10, -10.50, 56.50, -3.60)],
    "fiji_west":   [(176.50, -21.00, 180.00, -12.30)],
    "fiji_east":   [(-180.00, -21.00, -178.00, -12.30)],
    "canary":      [(-18.20, 27.60, -13.30, 29.50)],
}


def download(name, bbox, fmt="geoparquet"):
    out = os.path.join(OUT_DIR, f"{name}_buildings.parquet" if fmt == "geoparquet" else f"{name}_buildings.geojsonseq")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"{name}: already downloaded ({out})")
        return out
    cmd = ["overturemaps", "download", "--bbox=" + ",".join(str(v) for v in bbox),
           "-f", fmt, "--type=building", "-o", out]
    print(f"{name}: " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    print(f"{name}: saved {out} ({os.path.getsize(out) / 1e6:.1f} MB)")
    return out


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    fmt = sys.argv[1] if len(sys.argv) > 1 else "geoparquet"   # fallback: geojsonseq
    for name, boxes in BOXES.items():
        for bbox in boxes:
            try:
                download(name, bbox, fmt)
            except subprocess.CalledProcessError as e:
                print(f"{name}: FAILED ({e}). Try:  python {sys.argv[0]} geojsonseq")
