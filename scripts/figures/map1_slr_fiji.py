import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import os

SLR_THRESHOLD_M = 1.0
BACKGROUND_COLOR = "#000000"
LAND_COLOR = "#2d7a3e"
SAFE_COLOR = "#f4d03f"
RISK_COLOR = "#e63232"
TEXT_COLOR = "#ffffff"


def load_settlement_elevations(island):
    gdf = gpd.read_file(f"data/settlements/{island}_settlements_clean.gpkg")
    with rasterio.open(f"data/terrain/{island}_elevation.tif") as src:
        coords = [(g.centroid.x, g.centroid.y) for g in gdf.geometry]
        raw_elevations = [val[0] for val in src.sample(coords)]
    elevations = [np.nan if e == 0.0 else e for e in raw_elevations]
    gdf["elevation_m"] = elevations
    gdf["at_risk"] = gdf["elevation_m"] <= SLR_THRESHOLD_M
    return gdf


def add_north_arrow(ax, x=0.94, y=0.95):
    ax.annotate("N", xy=(x, y), xytext=(x, y - 0.09),
                xycoords="axes fraction", textcoords="axes fraction",
                fontsize=16, fontweight="bold", color="white", ha="center",
                arrowprops=dict(facecolor="white", edgecolor="white", width=4.5, headwidth=14, headlength=11))


def add_scale_bar(ax, gdf_bounds, x_start=0.05, y=0.05):
    km_per_degree = 106
    bar_length_km = 50
    bar_length_deg = bar_length_km / km_per_degree

    x0 = gdf_bounds[0] + (gdf_bounds[2] - gdf_bounds[0]) * x_start
    y0 = gdf_bounds[1] + (gdf_bounds[3] - gdf_bounds[1]) * y

    ax.plot([x0, x0 + bar_length_deg], [y0, y0], color="white", linewidth=3, solid_capstyle="butt")
    ax.text(x0 + bar_length_deg / 2, y0 + 0.05, "50 km", color="white",
            fontsize=10, ha="center", fontweight="bold")


def make_fiji_map():
    os.makedirs("outputs/plots", exist_ok=True)

    gdf = load_settlement_elevations("fiji")
    boundary = gpd.read_file("data/boundaries/fiji_islands.gpkg")

    fig = plt.figure(figsize=(14, 11))
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax = fig.add_axes([0.06, 0.06, 0.88, 0.78])
    ax.set_facecolor(BACKGROUND_COLOR)

    boundary.plot(ax=ax, color=LAND_COLOR, edgecolor="#1a4d26", linewidth=0.8, zorder=1)

    safe = gdf[~gdf["at_risk"]]
    at_risk = gdf[gdf["at_risk"]]
    safe.plot(ax=ax, color=SAFE_COLOR, markersize=35, alpha=0.9,
              edgecolor="black", linewidth=0.4, zorder=3)
    at_risk.plot(ax=ax, color=RISK_COLOR, markersize=35, alpha=0.95,
                  edgecolor="black", linewidth=0.4, zorder=4)

    ax.set_xlim(177.0, 180.0)
    ax.set_ylim(-19.2, -15.7)
    ax.set_axis_off()

    add_north_arrow(ax)
    add_scale_bar(ax, (177.0, -19.2, 180.0, -15.7))

    fig.text(0.5, 0.93, "FIJI", fontsize=28, fontweight="bold", color=TEXT_COLOR, ha="center")
    valid = gdf["elevation_m"].notna().sum()
    at_risk_pct = (at_risk.shape[0] / valid * 100) if valid > 0 else 0
    fig.text(0.5, 0.885,
             f"Sea-Level-Rise Exposure — {at_risk_pct:.1f}% of {valid} settlements at or below 1m elevation\n"
             "Viti Levu and Vanua Levu, Fiji's two largest and most populated islands",
             fontsize=13, fontweight="bold", color="#e8e8e8", ha="center")

    # Legend now placed as a figure-level element, just below the subtitle
    # text block, left-aligned — not inside the map axes anymore
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=SAFE_COLOR, markersize=10, label="Above 1m elevation (safe)"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=RISK_COLOR, markersize=10, label="At/below 1m (SLR risk)"),
    ]
    fig.legend(handles=handles, loc="upper left", fontsize=11, frameon=True,
               facecolor="#1a1a1a", edgecolor="#444444", framealpha=0.9, labelcolor="white",
               bbox_to_anchor=(0.08, 0.83))

    fig.text(0.5, 0.02, "DOUBLE JEOPARDY — Source: Copernicus DEM GLO-30, OpenStreetMap settlements",
              fontsize=8, color="#888888", ha="center")

    plt.savefig("outputs/plots/slr_exposure_fiji.png", dpi=220, facecolor=BACKGROUND_COLOR, bbox_inches="tight")
    plt.close(fig)
    print("Saved: outputs/plots/slr_exposure_fiji.png")


if __name__ == "__main__":
    make_fiji_map()