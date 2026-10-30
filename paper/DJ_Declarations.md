# DOUBLE JEOPARDY: Declarations

**DOUBLE JEOPARDY: The Vulnerability Spiral of Compound Climate Risk Across 5 Islands**

Sakshi D. Maske · Independent Geospatial Researcher · ORCID [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Version 2.1.0 · Archived release: Zenodo, DOI [10.5281/zenodo.21739961](https://doi.org/10.5281/zenodo.21739961)  
Preprint of the first version: EarthArXiv, DOI [10.31223/X5M50Q](https://doi.org/10.31223/X5M50Q) · Code and data: [github.com/sakshimaske303-commits/DOUBLE-JEOPARDY](https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY)

## Highlights

- On a bare-earth elevation model, 11.8% of people in the Maldives and 6.4% in Lakshadweep live at or below 1 m, against 8.9% and 0.8% on a surface model.
- Reef heat stress was higher in 2016–2020 than in 1996–2000 on all four reef islands, but no trend is significant once serial correlation is accounted for; mangrove extent shows no decline.
- Seychelles and the Maldives are in a near tie on the compound score, and the top island changes at an exposure weight of 52%.
- Protection of the 10 km coastal zone, from 1.3% to 71.4%, does not follow the compound score (descriptive, n = 4).
- National coastal setbacks reach fewer than one in ten low-lying buildings on the four tropical island groups, against 85% under the Canary Islands' 100 m line.

## Contributions, funding and interests

I am the sole author. I conceived the study, designed the methods, wrote the code, ran and checked the analysis, curated the data, wrote the paper and made the figures and maps (CRediT: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization). The work was not funded by anyone; I paid its costs myself. I have no competing interests to declare. No human participants, animals or personal data were involved, so ethical approval was not needed.

## Data and their licences

The study uses public data only: DeltaDTM v1.1 and the Copernicus DEM GLO-30 for elevation, WorldPop 2020 for population, OpenStreetMap for named places and coastlines, Overture Maps building footprints, NOAA Coral Reef Watch Degree Heating Weeks, Global Mangrove Watch v3, UNEP-WCMC reef and mangrove layers, the World Database on Protected Areas (June 2026 release) and Sentinel-2. My own code and text are released under CC BY 4.0, but third-party data keep their original licences. WDPA extracts are not included because their terms do not allow public redistribution, and the UNEP-WCMC layers are for non-commercial research use. Full citations, licences and attribution texts are in `DATA_SOURCES_AND_LICENSES.md`.

## Reproducing the results

Every reported number is written to a CSV in `data/`, and the figures and dashboard read those files. `scripts/run_all.py` re-runs the analysis, figures, maps and dashboard data and ends by reporting a complete or partial run. Large rasters and the building footprints are not committed; they are rebuilt with the included download scripts. The DeltaDTM tiles are exported with the Earth Engine Python API, which needs an Earth Engine project; the rest runs without it. Two scripts recompute key results independently: the coral trend p-values without the pyMannKendall library, and the setback distances on the WGS84 ellipsoid.

## Limits of the design

These are elevation thresholds, not flood models, and DeltaDTM's vertical error of about 0.4–0.5 m is large next to a 1 m threshold, so the comparison between models and islands matters more than any single percentage. Five island groups, and four for governance, describe this sample; they cannot establish general relationships. The setback analysis compares buildings with the setback written in national law, measured to a mapped shoreline rather than the legal reference line, and says nothing about permits, local plans or compliance.

## What changed from the first version

Six results of the first version were withdrawn on review. The 78.3% of Seychelles settlements "at risk" came from counting the elevation raster's NoData value as land at or below 1 m. The significant coral trends came from a single 5 km cell and a test that treated months as independent. Seychelles ranked first at every weighting only because both inputs happened to be highest there. The governance correlation of r = 0.965 came from counting overlapping protected areas twice and dividing by land area; on the coastal zone it is r = −0.10. The built-up rise in Seychelles was measured over boxes that were mostly ocean. And the first version used a surface elevation model only. Each correction is recorded in `paper/DJ_Development_Log.md`.

## AI assistance

The questions, the choice of islands and data, the methods, the decision to withdraw the six first-version results and the interpretation are mine. Within that work I used Claude (Anthropic), an AI assistant, in a supporting role. Its main job was cross-checking: comparing the exposure shares, reef heat-stress figures, compound scores and setback coverage quoted in the paper, executive summary, README and dashboard against the CSV files my scripts produce. I also asked it for help when one of my Python scripts broke or gave output I could not account for, and for the layout of the project web pages. The paper and other documents are my own writing; I used the assistant to flag wording that was unclear or overly technical, gaps where something seemed to be missing, and punctuation, and I decided which of those points to act on. It did not acquire or process the elevation, population, building, reef or mangrove data, and it did not run the analysis. I reviewed everything it suggested before using it, and the responsibility for the content is mine.

## Licence and citation

Released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0), with the third-party data exceptions above. Citation metadata are in `CITATION.cff`.
