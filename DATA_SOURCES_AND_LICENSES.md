# Data sources, licences and attribution

This project's own code and text are released under the terms in `LICENSE`. **Third-party data used or redistributed in this repository keep their original licences**, which CC BY 4.0 cannot override. Some of those licences limit redistribution. This file lists every dataset, its licence, the attribution it requires, and what that means for this repository.

| Dataset | Used for | Provider / citation | Licence and redistribution | Attribution text |
|---|---|---|---|---|
| OpenStreetMap: named places (settlement points), coastlines, tourism, infrastructure, Maldives/Canary reef and wetland features | Named places (second exposure measure), island boundaries (`data/boundaries_v2`), some ecosystem layers | OpenStreetMap contributors | Open Database Licence (ODbL) 1.0. Derived databases that are shared must stay under ODbL (share-alike). | "© OpenStreetMap contributors, ODbL" |
| OSM land polygons (osmdata.openstreetmap.de) | Fiji boundary | OpenStreetMap contributors, processed by FOSSGIS | ODbL 1.0 | "© OpenStreetMap contributors, ODbL" |
| Copernicus DEM GLO-30 | Surface elevation, kept as the comparison model | European Space Agency, Copernicus Programme | Free licence; attribution required. Tiles can be re-downloaded with `scripts/acquisition/download_copernicus_dem_tiles.py` instead of being committed. | "Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved." |
| DeltaDTM v1.1 | Bare-earth coastal elevation, the main elevation model for exposure | Pronk et al. (2024), *Scientific Data* 11, 273, doi:10.1038/s41597-024-03091-9; data on 4TU.ResearchData. Tiles taken from the Earth Engine community catalogue copy (`projects/sat-io/open-datasets/DELTARES/deltadtm_v1-1`) with `scripts/acquisition/export_deltadtm_gee.py` | CC BY 4.0. Tiles are not committed; they can be rebuilt with the export script and `prepare_deltadtm_tiles.py`. | Cite Pronk et al. (2024) and DeltaDTM v1.1 |
| Global Mangrove Watch v3 (1996, 2010, 2020) | Mangrove extent | Bunting et al. (2022), *Remote Sensing* 14(15), 3657, doi:10.3390/rs14153657 | CC BY 4.0 | Cite Bunting et al. (2022) |
| NOAA Coral Reef Watch, Daily 5 km Degree Heating Week v3.1 | Reef heat stress, averaged over mapped reef cells | NOAA Coral Reef Watch (2018, updated daily), accessed via NOAA CoastWatch ERDDAP (`noaacrwdhwDaily`) | US Government work, no use restrictions | "NOAA Coral Reef Watch. 2018, updated daily. NOAA Coral Reef Watch Version 3.1 Daily Global 5km Satellite Coral Bleaching Degree Heating Week Product, Jan. 1, 1996 – Dec. 31, 2020. College Park, Maryland, USA: NOAA Coral Reef Watch." |
| UNEP-WCMC coral reef and mangrove layers | Fiji, Lakshadweep, Seychelles reef/mangrove extent (`data/ecosystem_buffers`) | UNEP-WCMC, WorldFish Centre, WRI, TNC (2021). Global distribution of warm-water coral reefs, v4.1; Giri et al. (2011) mangroves | UNEP-WCMC data licence: non-commercial use, **redistribution requires permission** | Cite the exact version listed on the UNEP-WCMC Ocean Data Viewer download page |
| World Database on Protected Areas (WDPA), June 2026 release | Protected-area coverage | UNEP-WCMC and IUCN (2026), Protected Planet | WDPA terms of use: non-commercial use, **no public redistribution of the data** without permission | "UNEP-WCMC and IUCN (2026), Protected Planet: The World Database on Protected Areas (WDPA) [Online], June 2026, Cambridge, UK: UNEP-WCMC and IUCN. Available at: www.protectedplanet.net." |
| WorldPop 2020 population, 100 m | People at or below 1 m (main exposure measure) | WorldPop, University of Southampton | CC BY 4.0 | Cite the specific WorldPop dataset and DOI shown on its download page |
| IBTrACS v04r01 | Cyclone tracks (collected, not used in the paper) | Knapp et al. (2010), *Bull. Amer. Meteor. Soc.* 91, 363–376; NOAA NCEI | US Government work | Cite Knapp et al. (2010) and IBTrACS v04r01 |
| Sentinel-2 L2A | NDBI built-up change on land (supplementary) | Copernicus Sentinel data, accessed via Copernicus Data Space Ecosystem / Sentinel Hub | Free, full and open; attribution required | "Contains modified Copernicus Sentinel data [2016, 2024]" |

## What this means for the public repository (action needed)

- [ ] **Remove WDPA extracts from the public repository** (`data/ecosystem_buffers/*_wdpa.gpkg`, `data/protected_areas_wdpa/`) and from any webmap layer files that embed them, or obtain permission from UNEP-WCMC. Keep `scripts/processing/filter_wdpa_islands.py` so others can rebuild them from their own WDPA download.
- [ ] Check the same for the UNEP-WCMC coral and mangrove extracts in `data/ecosystem_buffers/`.
- [ ] Keep OSM-derived files (settlements, `boundaries_v2`) under ODbL; state this in `LICENSE`.
- [ ] Add the attribution lines above to the paper's Data section and to the dashboard footer and maps.
- [ ] Consider licensing the code under MIT or Apache-2.0 and the text and figures under CC BY 4.0 (Creative Commons recommends against CC licences for software). This is the author's decision; `LICENSE` has not been changed.

## Software

Python packages used: GeoPandas, Rasterio, Earth Engine Python API (DeltaDTM export only), Shapely, NumPy, pandas, SciPy, pyMannKendall (Hussain & Mahmud, 2019, *Journal of Open Source Software* 4(39), 1556), Matplotlib, Plotly, Folium, Streamlit. Cite them in the paper's Methods or Acknowledgements.
