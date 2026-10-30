# data/

All paths are relative to the repository root. Large rasters (`*.tif`), the full building footprints and WDPA extracts are not committed; the scripts listed below rebuild them.

## Result tables

| File | Written by | Used in |
|---|---|---|
| `slr_exposure_summary.csv` | `scripts/analysis/slr_exposure_analysis.py` | Paper Figure 2, dashboard |
| `slr_exposure_summary_by_source.csv` | `scripts/analysis/slr_exposure_analysis.py` | Same results for each elevation source (DeltaDTM, Copernicus) |
| `named_places_by_type.csv` | `scripts/analysis/slr_exposure_analysis.py` | Settlement point breakdown by OSM place type |
| `population_weighted_exposure.csv` | `scripts/analysis/population_weighted_exposure.py` | Paper Figure 3, compound score |
| `population_weighted_exposure_by_source.csv` | `scripts/analysis/population_weighted_exposure.py` | Same results for each elevation source (DeltaDTM, Copernicus) |
| `coral_trend_results.csv` | `scripts/analysis/coral_trend_test.py` | Paper Figure 4, dashboard |
| `compound_vulnerability_scores.csv` | `scripts/analysis/compound_vulnerability_score.py` | Paper ranking, dashboard |
| `compound_weighting_sweep.csv` | `scripts/analysis/compound_vulnerability_score.py` | Paper Figure 7 (weighting sensitivity) |
| `wdpa_coastal_normalized.csv` | `scripts/processing/wdpa_coastal_buffer.py` | Governance test |
| `governance_alignment_test.csv` | `scripts/analysis/governance_correlation_test.py` | Paper Figure 6 |
| `governance_alignment_summary.csv` | `scripts/analysis/governance_correlation_test.py` | Dashboard |
| `ndbi_land_change.csv` | `scripts/analysis/ndbi_land_change.py` | Encroachment results |
| `setback_calibration_summary.csv` | `scripts/analysis/setback_calibration.py` | Paper Section 4.8, Figure 9 |
| `setback_coverage_curve.csv` | `scripts/analysis/setback_calibration.py` | Interactive setback curve |

## Checks

| File | Written by | What it checks |
|---|---|---|
| `boundary_area_validation.csv` | `scripts/validation/boundary_area_validation.py` | Island land areas against World Bank and official reference figures |
| `coral_trend_check.csv` | `scripts/validation/coral_trend_check.py` | Coral trend p-values recomputed without pyMannKendall |
| `setback_distance_check.csv` | `scripts/validation/setback_distance_check.py` | Shoreline distances against WGS84 ellipsoid distances |
| `canary_python_elevations_check.csv` | `scripts/processing/export_canary_check.py` | Canary settlement elevations for comparison in QGIS |

## Kept from earlier versions (not used in reported results)

| File | Written by | Note |
|---|---|---|
| `wdpa_area_by_island.csv` | `scripts/processing/compute_wdpa_area.py` | Version 1 WDPA area; replaced by `wdpa_coastal_normalized.csv` |
| `wdpa_normalized.csv` | `scripts/processing/normalize_wdpa.py` | Version 1 ratio; see Development Log Entry 6 |
| `slr_exposure_summary_maldives_lakshadweep_v2.csv` | `scripts/analysis/recompute_maldives_lakshadweep_exposure.py` | Interim recompute; replaced by `slr_exposure_summary.csv` |

## Folders

| Folder | Contents | Source script(s) |
|---|---|---|
| `boundaries/` | Original island boundaries and OSM land polygons | `scripts/local_fixes/rebuild_*` |
| `boundaries_v2/` | Validated island boundary polygons used by all current analyses | `scripts/local_fixes/rebuild_boundary_polygons_osm.py`, `rebuild_fiji_boundary_landpolygons.py` |
| `terrain/` | Copernicus GLO-30 and DeltaDTM tiles and VRTs (not committed) | `scripts/acquisition/download_copernicus_dem_tiles.py`, `export_deltadtm_gee.py`, `prepare_deltadtm_tiles.py` |
| `settlements/` | Cleaned OSM settlement points | `scripts/acquisition`, `scripts/processing` |
| `settlement_elevations_full/` | Per-settlement elevation tables | `scripts/processing/export_settlement_elevations_full.py` |
| `population/` | Population rasters (not committed) | `scripts/acquisition/download_lakshadweep_population.py` |
| `coral_bleaching_v3/` | NOAA CRW DHW for reef cells (current) | `scripts/acquisition/download_dhw_reef_cells.py` |
| `coral_bleaching_v2/` | Area-averaged DHW (earlier version) | `scripts/local_fixes/download_coral_dhw_area_avg.py` |
| `coral_bleaching/` | Single-cell DHW per island (Version 1) | `scripts/acquisition/download_coral_bleaching_stress.py` |
| `mangroves/` | Global Mangrove Watch extents, 1996 / 2010 / 2020 | `scripts/processing/filter_gmw_*.py` |
| `ecosystem_buffers/` | Coastal buffers and protected-area layers (WDPA files not committed) | `scripts/processing/clean_wdpa.py`, `wdpa_coastal_buffer.py` |
| `protected_areas_wdpa/` | WDPA extracts (not committed; download from protectedplanet.net) | — |
| `settlement_encroachment/` | Sentinel-2 NDBI rasters and summaries, 2016 vs. 2024 | `scripts/acquisition/download_ndbi_encroachment*.py`, `scripts/analysis/ndbi_land_change.py` |
| `buildings/` | Overture building points (not committed) | `scripts/acquisition/download_buildings_overture.py`, `scripts/processing/export_building_points.py` |
| `cyclone_tracks/` | Cyclone wind speed records (exploratory, not in the paper) | `scripts/processing/consolidate_wind_speed.py` |
| `satellite_damage_proxy/` | Cyclone damage proxy (exploratory, not in the paper) | `scripts/acquisition/download_cyclone_damage_proxy.py` |
