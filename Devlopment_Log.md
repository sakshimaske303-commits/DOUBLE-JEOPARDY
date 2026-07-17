# DOUBLE JEOPARDY: The Vulnerability Spiral — Quantifying Compound Coastal Risk and Governance-Evidence Alignment Across Five Island Nations

## Project Overview

DOUBLE JEOPARDY is a geospatial framework that tests whether small island nations face a compounding vulnerability to sea-level rise: high physical exposure combined with degrading natural coastal defenses. Rather than assuming all coastal ecosystems degrade uniformly, this project rigorously tests each ecosystem type independently — mangroves and coral reefs — across five island nations spanning three ocean basins: Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands. The project deliberately avoids treating "ecosystem buffer" as a single undifferentiated category, testing mangrove and coral trajectories separately and combining them with physical exposure into a composite, evidence-based vulnerability assessment.

Beyond quantifying ecological and physical risk, this project extends into an explicit governance dimension: it tests whether formal protected-area designation — the primary policy instrument through which island governments and international bodies claim to manage coastal ecosystem risk — is actually aligned with where empirically verified vulnerability is highest. This transforms the project from a purely environmental-science exercise into a policy-evaluation framework, testing whether governance response is evidence-based or spatially disconnected from the risk it claims to manage — directly relevant to environmental economics, adaptation-finance prioritization, and marine spatial governance.

## Problem Statement

International climate adaptation policy and nature-based solutions financing frequently treat coastal ecosystems as a single protective category, assuming mangroves and coral reefs degrade together under climate pressure and jointly determine a settlement's exposure to sea-level rise. This assumption is rarely tested against independent, multi-temporal evidence at a systematic, cross-national scale. If ecosystems degrade at genuinely different rates — or in different directions entirely — then adaptation planning that treats ecosystem buffer as a single category risks misallocating resources and misjudging which coastal zones are genuinely most at risk.

A second, distinct problem compounds the first: formal protected-area designation is widely treated, in both national policy and international financing frameworks, as a proxy for effective ecosystem management. Yet protected-area boundaries are frequently drawn based on historical, political, or administrative considerations rather than continuously updated empirical risk data. Whether protection status in these five island nations genuinely corresponds to locations of highest verified ecological and physical vulnerability — or is a "paper park" phenomenon, spatially disconnected from where risk is actually concentrated — has not been systematically tested using independent, satellite-derived evidence.

## Aim

To develop a reproducible geospatial framework that (1) independently quantifies physical sea-level-rise exposure and multi-temporal ecosystem trajectory — tested separately for mangroves and coral reefs — across five island nations, producing a composite, evidence-based vulnerability assessment; and (2) tests whether existing formal protected-area governance is statistically aligned with this empirically verified vulnerability, or represents a measurable governance-evidence gap.

## Research Questions

**RQ1 (Ecological/Physical)**: Does physical sea-level-rise exposure combine with ecosystem buffer degradation to produce compounding settlement-level vulnerability across five island nations — and does this compounding effect operate uniformly across ecosystem types, or does it depend on which specific ecosystem is actually degrading in a given location?

**RQ2 (Governance)**: Does the spatial distribution of formal protected-area designation (WDPA) correlate with empirically verified compound vulnerability — indicating evidence-responsive governance — or is protection status statistically independent of, or even inversely related to, actual satellite-derived ecosystem risk, indicating a spatial misalignment between policy instrument and empirical need?

## Hypotheses

**H1 (Coral Pathway)**: Coral reef ecosystems will show a statistically detectable increase in thermal bleaching stress over a multi-decadal period, and this increase will be more pronounced in islands with higher physical sea-level-rise exposure, consistent with a genuine compounding vulnerability pathway.

**H2 (Mangrove Pathway)**: Mangrove ecosystems will show a statistically detectable decline in spatial extent over the same period, contributing an independent compounding pathway alongside coral degradation. This hypothesis is tested with equal rigor to H1, and will be reported honestly regardless of outcome.

**H3 (Governance-Evidence Alignment)**: Islands and coastal zones with higher composite vulnerability scores will show correspondingly higher formal protected-area coverage, consistent with risk-responsive governance. A finding of no relationship, or an inverse relationship, would indicate that protected-area designation in this sample is not empirically risk-driven — a substantive governance finding in its own right, reported transparently regardless of direction.

## Objectives

- Construct a settlement-level physical exposure dataset across five island nations using elevation and slope data, identifying the proportion of settlements below a standard one-meter sea-level-rise threshold.
- Construct a multi-temporal mangrove extent dataset across five island nations using the Global Mangrove Watch archive, testing for genuine area-based decline across multiple independent time points rather than relying on a single before-after snapshot.
- Construct a multi-temporal coral reef thermal stress dataset across five island nations using satellite-derived Degree Heating Week data, testing for a measurable increase in bleaching-level heat stress over time.
- Construct a composite Compound Vulnerability Score integrating physical exposure and ecosystem degradation signals at the island level.
- Quantify formal protected-area (WDPA) coverage at the island and coastal-zone level, and statistically test its relationship to the Compound Vulnerability Score — directly testing whether governance instruments are spatially aligned with empirically verified risk.
- Test whether settlement and infrastructure expansion disproportionately occurs within or adjacent to ecosystem buffer zones over time, using satellite-derived built-up area change detection.
- Validate all ecosystem-trend findings against multiple independent time points rather than a single comparison, consistent with rigorous causal-inference practice.
- Produce a reproducible, cross-national geospatial framework and interactive dashboard communicating both the compound vulnerability findings and the governance-alignment analysis, framed for direct relevance to adaptation policy and conservation finance decision-making.

## Methodology Summary

Physical exposure is quantified using elevation and slope data intersected with settlement locations across all five islands, identifying the proportion of settlements at or below a one-meter elevation threshold. Ecosystem degradation is quantified independently for two ecosystem types: mangrove extent, using multiple independent time points from the Global Mangrove Watch archive to test for genuine multi-decadal area change; and coral reef condition, using a continuous multi-decadal time series of satellite-derived thermal stress data, comparing early-period and recent-period averages. These two ecosystem signals, together with physical exposure, are combined into a normalized Compound Vulnerability Score per island.

The governance dimension is tested by quantifying the spatial extent and density of formally designated protected areas (drawn from the World Database on Protected Areas) per island and, where resolution permits, per coastal zone, and statistically comparing this governance coverage against the Compound Vulnerability Score — testing directly whether higher-risk zones are more, equally, or less likely to carry formal protection status. This transforms the project's ecological findings into a direct, testable statement about policy effectiveness and resource allocation, rather than leaving the governance implications as unexamined commentary.

A subsequent phase tests whether settlement and infrastructure expansion, derived from satellite-based built-up area change detection, is disproportionately concentrated within or adjacent to ecosystem buffer zones — testing whether human response to environmental pressure itself contributes to a self-reinforcing vulnerability dynamic, and whether such encroachment is more prevalent inside or outside formally protected boundaries.

## Study Area

Five island nations spanning three ocean basins: Maldives and Lakshadweep (Indian Ocean), Seychelles (western Indian Ocean), Fiji (South Pacific), and the Canary Islands (eastern Atlantic) — selected for consistent multi-source data availability and geographic, geological, and climatic diversity, allowing the compound vulnerability and governance-alignment framework to be tested across genuinely different island contexts, protected-area regimes, and administrative systems rather than a single case.

## Expected Outputs

- A settlement-level physical exposure dataset across five island nations.
- A validated multi-temporal mangrove extent dataset.
- A validated multi-decadal coral reef thermal stress dataset.
- A composite Compound Vulnerability Score and risk ranking across all five islands.
- A governance-alignment analysis testing the statistical relationship between protected-area coverage and empirically verified vulnerability, including identification of any "governance-evidence gap" zones — areas of high verified risk with low or no formal protection.
- A settlement/infrastructure encroachment analysis testing the ecosystem-buffer feedback hypothesis, disaggregated by protection status.
- An interactive geospatial dashboard and complete open-source codebase, extensible to additional island nations and ecosystem types.

## Relevance

This project is directly relevant to climate adaptation policy, nature-based solutions financing, ecosystem-services valuation, and marine spatial governance. Its central contribution is twofold: first, demonstrating that treating coastal ecosystem protection as an undifferentiated category can obscure materially different risk profiles, requiring rigorous, ecosystem-specific, multi-temporal verification rather than an assumed uniform decline narrative; and second, directly testing — rather than assuming — whether existing conservation governance instruments are empirically aligned with verified risk, providing a transferable methodology for evaluating adaptation-finance and protected-area prioritization decisions in any coastal or island context facing compound climate vulnerability.

## Current Status

Project Concept Finalized
Version 1.0

---------------------------------------------------------------------------------------------------

# Development Log — Part 1 of 6: Project Setup and Data Architecture Design

## Status
Complete. This part covers the initial project structure decisions made once the DOUBLE JEOPARDY research question and five-island study area were finalized, before any data acquisition began.

---

## Starting Point

With the research question finalized — testing whether physical sea-level-rise exposure compounds with ecosystem buffer degradation across five island nations, and whether this differs by ecosystem type — the first task was designing a project folder structure that would support the specific analytical needs of this study, rather than adopting a generic template.

## Folder Structure Decision: Category-Based, Not Island-Based

Two organizational approaches were considered before writing any acquisition code: organizing folders by island (a Maldives folder, a Seychelles folder, and so on, each containing all its data types), or organizing by data category (a settlements folder, a mangroves folder, and so on, each containing all five islands' files).

The category-based structure was chosen deliberately, for a specific reason directly tied to the project's methodology. Because DOUBLE JEOPARDY's core analysis requires comparing the same variable across all five islands simultaneously — comparing coral bleaching stress across islands, comparing settlement encroachment rates across islands — an island-based folder structure would have required navigating into five separate folders every time a cross-island comparison script needed to run, and would have made it easy to accidentally use an inconsistent file-naming convention in one island's folder versus another's. A category-based structure keeps every version of a given dataset type together, making cross-island scripts simpler to write (a single loop over island names, reading from one folder) and making it immediately visually obvious if any island's file is missing from a given category, since all five would be expected to sit side by side.

The resulting top-level structure was established as:

```
DOUBLE_JEOPARDY/
├── data/
│   ├── settlements/
│   ├── ecosystem_buffers/       (mangroves, coral reefs, protected areas)
│   ├── terrain/                 (elevation, slope)
│   ├── population/
│   ├── cyclone_tracks/
│   ├── boundaries/               (island outlines)
│   ├── mangroves/                (raw multi-temporal GMW archives, kept separate from processed ecosystem_buffers)
│   ├── coral_bleaching/          (NOAA thermal stress time series)
│   └── settlement_encroachment/  (satellite-derived built-up change data)
├── outputs/
│   └── plots/
├── Project_Journal.md
└── Devlopment_Log.md
```

## A Deliberate Inconsistency, Explained

One departure from strict category-based organization is worth noting explicitly: the raw multi-temporal Global Mangrove Watch archives (1996, 2010, 2020 snapshots) were kept in their own `mangroves/` folder, separate from the cleaned, per-island mangrove files that live inside `ecosystem_buffers/`. This was a practical decision rather than an architectural inconsistency — the raw GMW shapefiles are extremely large (roughly 900MB to 950MB per year, covering the entire globe) and are processed once into much smaller per-island, per-year extracts. Keeping the large source archives physically separate from the small, final per-island files made it easier to later exclude the bulky raw archives from version control while keeping the lightweight final outputs tracked, without needing folder-level exceptions scattered throughout a single mixed directory.

## Environment Setup

The project reused the `gpie2` conda environment already established and verified in prior work, rather than creating a new environment from scratch. This environment had already been fixed for a critical numerical computing issue (a corrupted Intel MKL backend, resolved by installing NumPy and SciPy with the `nomkl` OpenBLAS backend instead), and reusing it avoided the risk of reintroducing that same class of failure in a fresh environment. Two files were carried over directly from prior work rather than rewritten: `auth_sentinelhub.py` (the Sentinel Hub OAuth authentication module) and the `.env` file containing Copernicus Data Space credentials, since both API access patterns and credentials were identical to what this project would also require for its own Sentinel-2 and Sentinel-5P-adjacent acquisition needs.

## Why This Setup Mattered Later

This upfront structural decision proved directly useful once multi-temporal analysis began: because every mangrove-year file, every coral time series file, and every island's settlement file lived in a predictable, category-consistent location, later scripts that needed to loop across all five islands for a given analysis (elevation exposure, mangrove area comparison, coral stress trends) could be written generically, with the island name as the only variable changing between iterations — rather than requiring five near-duplicate scripts, one hardcoded per island's folder layout.

---

*Continued in Part 2: Core Dataset Acquisition and Cleanup (Settlements, Tourism, Infrastructure).*

----------------------------------------------------------------------------------------------------

# Development Log — Part 2 of 6: Core Dataset Acquisition and Cleanup (Settlements, Tourism, Infrastructure)

## Status
Complete. This part covers acquisition and cleaning of the three OpenStreetMap-derived datasets forming the human-activity baseline for all five islands: settlements, tourism infrastructure, and general infrastructure.

---

## Data Source and Acquisition Method

All three datasets were acquired via OpenStreetMap, using Overpass Turbo queries filtered to each island's approximate extent, producing one raw GeoJSON export per island per category (fifteen files total: five islands × three categories). This source was chosen for consistency and free accessibility across all five islands, which span three different national administrative systems (Maldives, India, Seychelles, Fiji, Spain) where a single authoritative government dataset covering all five uniformly does not exist.

## The Column-Bloat Problem

Every raw OpenStreetMap export arrived with an extremely large number of columns — commonly 200 to 240 per file — the overwhelming majority of which were irrelevant to this project's analysis: place-name translations into dozens of languages (`name:ta`, `name:zh-Latn-pinyin`, `wikipedia:ur`, and similar), Wikidata cross-references, contact details (phone, email, social media handles), and other OSM tagging metadata unrelated to settlement identity, population, or location. Retaining all of this metadata would have meant carrying substantial file-size overhead with no analytical benefit, and made every dataset harder to inspect manually during development.

A consistent cleaning pattern was applied across all fifteen files: each was read with `geopandas`, reduced to a small set of genuinely relevant columns (for settlements: name, place type, population, and geometry; for tourism: name, tourism type, amenity type, and geometry; for infrastructure: name, man-made feature type, amenity type, power infrastructure type, and geometry), and saved as a new `_clean.gpkg` file, leaving the original raw GeoJSON untouched. This reduced settlement files, for example, from as many as 240 columns down to 4 or 5, while preserving every row and every field actually needed for analysis.

## Bug: Mislabeled Sea Features in Settlement Data

During validation of the cleaned settlement files — specifically, while investigating why the Maldives and Lakshadweep settlement datasets each produced an implausibly large bounding box that appeared to span far outside the expected island extent — two rows were found responsible in both files: entries labeled "Arabian Sea" and "Laccadive Sea." These were not settlements at all, but OpenStreetMap features representing named bodies of water that had been incorrectly captured by the Overpass Turbo place-type query used during acquisition, since OSM's `place` tagging schema is applied inconsistently across contributors and occasionally includes large natural water-body labels alongside genuine settlements.

This was identified by computing the centroid longitude and latitude of every settlement in each file, sorting by longitude, and inspecting the extreme values at both ends of the sorted list — a technique that immediately surfaced the two sea-name entries sitting far outside the cluster of genuine settlement coordinates. Both rows were removed from both the Maldives file (reducing it from 998 to 996 rows) and the Lakshadweep file (reducing it from 38 to 36 rows), with the fix applied directly to the cleaned `.gpkg` files rather than requiring re-acquisition from OpenStreetMap.

## Bug: Invalid Geometry in Tourism Data

While cleaning the Canary Islands tourism dataset, `geopandas.read_file()` raised a `GEOSException: Invalid number of points in LinearRing found 2 - must be 0 or >= 4` — a hard crash indicating at least one polygon in the source file had fewer than the minimum four coordinate pairs required to form a valid closed ring (a well-known defect pattern in crowd-sourced OSM polygon data, where a contributor's edit occasionally produces a malformed, near-degenerate shape).

Rather than allowing this single bad record to block processing of the entire 10,877-row file, the read operation was modified to pass `on_invalid="ignore"` to `geopandas.read_file()`, which causes unreadable geometries to be silently dropped rather than raising an exception, followed by an explicit check and count of any rows where the geometry column ended up null after the read. This confirmed exactly two invalid rows in the Canary tourism file, which were dropped, leaving 10,875 valid rows. The same defensive pattern (`on_invalid="ignore"` plus an explicit null-geometry check and count) was applied to all subsequent vector-cleaning scripts in the project as a standard precaution, since the same class of malformed-polygon defect could plausibly recur in any OSM-sourced file.

## Duplicate and Naming Inconsistencies

Several minor naming inconsistencies were identified and resolved during this phase, consistent with a broader pattern (observed throughout this project) of manually-repeated export or download attempts producing near-duplicate files with slightly different names. Fiji's protected-area equivalent file appeared twice under `FIJI_INFRAA_SLR.gpkg` (a typo, extra "A") and `FIJI_INFRA_SLR.gpkg`, both identical in file size — the typo'd duplicate was deleted, retaining only the correctly-named version. This pattern of manually re-run exports producing filename drift recurred across multiple dataset categories throughout the project and was handled consistently the same way each time: verify file sizes or row counts to confirm which copy (if any) differed in content, then delete confirmed duplicates rather than leaving ambiguous near-identical files in the working dataset.

## Final Status of This Phase

| Dataset | Islands Covered | Typical Column Reduction |
|---|---|---|
| Settlements | 5 (with 2 outlier rows removed from 2 islands) | ~240 → 4–5 |
| Tourism | 5 (with 2 invalid rows removed from 1 island) | ~200–490 → 4 |
| Infrastructure | 5 | ~200 → 4 |

All fifteen files (five islands × three categories) were confirmed clean, correctly bounded to their respective islands, and free of invalid geometries by the end of this phase, providing the human-activity baseline used throughout the rest of the project, including the settlement-encroachment analysis conducted much later.

---

*Continued in Part 3: Ecosystem Data (Mangroves, Coral Reefs, Protected Areas).*

----------------------------------------------------------------------------------------------------

# Development Log — Part 3 of 6: Ecosystem Data (Mangroves, Coral Reefs, Protected Areas)

## Status
Complete. This part covers acquisition and cleaning of the three ecosystem-buffer datasets central to the project's core hypothesis testing: mangrove extent, coral reef extent, and formally designated protected areas.

---

## Mixed Source Types — A Structural Complication

Unlike the settlements, tourism, and infrastructure datasets (uniformly sourced from OpenStreetMap across all five islands), the ecosystem-buffer datasets arrived from two structurally different sources depending on the island, requiring two separate cleaning pipelines rather than one shared script.

Fiji, Lakshadweep, and Seychelles mangrove and coral data originated from the WCMC (World Conservation Monitoring Centre) Global Mangrove Watch and coral reef atlases, identifiable immediately by their distinctive uppercase column-naming convention: `LAYER_NAME`, `METADATA_I`, `NAME`, `FAMILY`, `GENUS`, `SPECIES`, `DATA_TYPE`, `GIS_AREA_K`, `REP_AREA_K`, and similar scientific-atlas fields. Maldives and Canary Islands data for the same two categories instead came from OpenStreetMap, with the same style of lowercase, `place`/`natural`/`tourism`-tagged schema seen in the settlements and tourism datasets. This meant every cleaning script for mangroves and corals needed to detect or be told which source format a given island's file used, and apply the correct column-selection logic accordingly — a `WCMC_KEEP_COLUMNS` list versus an OSM-style `KEEP_COLUMNS` list, rather than one universal column set.

## Bug: The Maldives Coral Reef File Was Not Actually Coral Data

The most significant data-quality issue discovered in this phase was in `coral_maldives.gpkg`, which on initial inspection contained 4,230 rows and 79 columns. Closer inspection of the column list revealed fields entirely unrelated to coral reefs — `cuisine`, `spa`, `restaurant`, `rooms`, `payment:visa`, `payment:mastercard`, `opening_hours`, `parking` — indicating the file was not a filtered coral-reef dataset at all, but an essentially unfiltered general-purpose OpenStreetMap export for the Maldives region that happened to be named as though it were coral-specific.

To recover genuine coral reef features from this file, rather than discarding it, the data was filtered using the OSM tagging convention for reef features (`natural == "reef"`), which correctly identified 2,921 of the 4,230 rows as genuine coral reef polygons — the remaining 1,309 rows were unrelated tourism, hospitality, and amenity points that had been mixed into the same export at the point of original acquisition. Further inspection confirmed a `reef` attribute column existed with a single consistent value (`"coral"`) across the genuinely-reef-tagged rows, providing a secondary confirmation that the `natural == "reef"` filter had correctly isolated the intended feature type. This filtering step — reducing 4,230 rows to 2,921 verified coral reef features — was applied before any further column cleanup, ensuring downstream analysis was not silently diluted by thousands of irrelevant tourism records misclassified as coral data.

## Genuine Ecological Absences, Not Data Gaps

Two islands returned zero results for specific ecosystem categories, and both were investigated and confirmed as genuine ecological absences rather than acquisition failures, consistent with a standard applied throughout this project: any zero-result finding is treated as a hypothesis to verify, not an error to silently work around.

Lakshadweep returned zero mangrove features across every source checked. This is consistent with mangroves being ecologically rare in this specific archipelago, a small coral-atoll chain without the muddy intertidal delta conditions mangroves typically require, and was accepted as a genuine finding rather than a missing download.

The Canary Islands returned zero coral reef features. This is consistent with the islands' subtropical, volcanic, cooler-water Atlantic setting, outside the warm tropical shallow-water conditions coral reef ecosystems require — reinforced later in the project when a Global Mangrove Watch bounding-box query (used for an unrelated multi-temporal analysis) also returned zero mangrove features for the Canary Islands even after deliberately widening the search box, providing independent cross-confirmation that this island's coastal ecology genuinely differs from the tropical islands in the sample rather than reflecting a systematic data-acquisition problem specific to one dataset.

## Protected Areas: Upgrading From a Low-Quality Source

The protected-area dataset initially available for four islands (Maldives, Canary Islands, Seychelles, Fiji) had been sourced from OpenStreetMap via the QuickOSM plugin, and on inspection was found to contain an implausibly small number of features per island — as few as one protected area recorded for Fiji, and four for Maldives — strongly suggesting incomplete rather than genuinely sparse protection coverage, since these regions are known to host numerous formally gazetted marine and terrestrial protected areas.

This was resolved by switching to the World Database on Protected Areas (WDPA), the authoritative global protected-area dataset maintained by UNEP-WCMC. The full WDPA download (approximately 4.15 gigabytes, split by the data provider into three sequentially-numbered zip archives due to shapefile attribute-table size limits) was extracted, and each of the three extracted polygon shapefiles was filtered directly to each island's bounding box using `geopandas.read_file()`'s `bbox` parameter — reading only the geographically relevant subset from disk without loading the full multi-gigabyte global file into memory, the same memory-efficient filtering strategy already proven necessary for datasets of this scale elsewhere in the project. Results from all three WDPA archive parts were then concatenated per island into a single combined file.

This substantially increased protected-area feature counts: Maldives rose from 4 to 93 features, Fiji from 1 to 126 (after combining two sub-queries needed to correctly capture Fiji's territory, which spans the antimeridian), Seychelles from 4 to 49, and Canary Islands from 258 to 385. Lakshadweep was independently confirmed to have zero WDPA-registered protected areas, consistent with its earlier OpenStreetMap-derived result of zero — providing cross-source confirmation that this is a genuine finding about Lakshadweep's protected-area status, not a data-source-specific artifact. The previously-used QuickOSM-derived protected-area files were deleted and replaced with the new WDPA-derived files across all four islands where WDPA data existed.

The raw WDPA files carried 34 columns per feature, including the full range of standard WDPA metadata fields (governance type, ownership type, management authority, IUCN category, verification status, and others). This was reduced to nine columns judged directly relevant to this project's analysis: name, designation, designation type, IUCN category, legal status, status year, and both reported and GIS-calculated area — retaining the fields needed to later assess protection type and extent while discarding administrative metadata not used in any planned analysis.

## Final Status of This Phase

| Dataset | Islands With Data | Confirmed Genuine Absences |
|---|---|---|
| Mangroves | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |
| Coral Reefs | Maldives, Fiji, Lakshadweep, Seychelles | Canary Islands |
| Protected Areas (WDPA) | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |

This phase established the ecosystem-buffer baseline used both for the project's static ecosystem-extent context and, later, as the foundation extended into full multi-temporal analysis (covered in Part 5).

---

*Continued in Part 4: Terrain, Population, and Cyclone Track Data.*

----------------------------------------------------------------------------------------------------

# Development Log — Part 4 of 6: Terrain, Population, and Cyclone Track Data

## Status
Complete. This part covers acquisition and validation of the three remaining baseline datasets: elevation and slope (terrain), population density, and historical cyclone tracks.

---

## Terrain: Elevation and Slope

Elevation data (Copernicus DEM) was acquired for all five islands and, on inspection, was found to already be in the correct EPSG:4326 coordinate reference system across every island — no reprojection was required for this dataset.

Slope data required correction for three of the five islands (Canary, Fiji, Lakshadweep), which were found in EPSG:3857 rather than the project's standard EPSG:4326, and were reprojected using `rasterio`'s `calculate_default_transform` and `reproject` functions with bilinear resampling — the resampling method appropriate for continuous elevation-derived data, as opposed to the nearest-neighbor resampling required for categorical data such as land cover. No standalone slope file existed at all for Seychelles; rather than treating this as a missing dataset requiring separate acquisition, it was generated directly from the already-validated Seychelles elevation raster using GDAL's `gdaldem slope` command-line tool, producing a correctly-projected slope raster without requiring any new external data source.

Elevation values across all five islands were checked against known geography as a validation step, rather than accepted at face value. The Canary Islands showed a maximum elevation of approximately 3,696 meters, consistent with the known height of Mount Teide (Spain's highest peak, at approximately 3,715 meters). Seychelles showed a maximum of approximately 904 meters, consistent with its granite mountain terrain (Morne Seychellois). Maldives and Lakshadweep both remained within an approximate 0–20 meter range throughout, consistent with their nature as low-lying coral atoll nations. This cross-check against independently known real-world geography provided confidence that the elevation data was correctly processed and not, for example, silently corrupted or misaligned during acquisition.

## Population: Validation Against Real-World Figures

Population density rasters (WorldPop, 2020) were acquired for four of five islands (Fiji, Seychelles, Maldives, and Canary Islands, the last derived by clipping Spain's national population raster to the Canary Islands' extent). Lakshadweep population data was not acquired in this phase, since the only available access method required downloading a population raster covering the entirety of India — determined to be an impractical file size relative to the small area of Lakshadweep actually needed, and deferred as a lower-priority item to be revisited with a more targeted acquisition approach if time permitted.

Each acquired population raster was validated by summing all pixel values to produce a total estimated population per island, then compared against independently known real-world population figures rather than assumed correct simply because the acquisition process completed without error. All four matched closely: Canary Islands estimated at approximately 2.09 million against an actual figure of roughly 2.2 million; Fiji at approximately 896,000 against an actual figure of roughly 900,000; Seychelles at approximately 98,000 against an actual figure of roughly 100,000; and Maldives at approximately 540,000, consistent with its known population range. This validation step was treated as essential rather than optional, following the general principle applied throughout this project that a dataset producing no errors during processing is not, by itself, evidence that the dataset is correct.

One large raster (Fiji's population file) initially failed to read with a `rasterio.errors.RasterioIOError: cannot allocate 884736000 bytes` memory error when attempting a standard full-array read. This was resolved by reading the raster in tiled blocks using `rasterio`'s `block_windows` iterator rather than loading the entire array into memory at once, accumulating the sum, minimum, and maximum incrementally across blocks — the same class of memory-efficient reading strategy required elsewhere in this project for other unusually large single files.

## Cyclone Tracks: IBTrACS and the Wind-Speed Consolidation Problem

Historical cyclone track data was sourced from IBTrACS (International Best Track Archive for Climate Stewardship), the standard global authoritative cyclone dataset maintained by NOAA, combining reports from over a dozen meteorological agencies worldwide. The complete global shapefile was filtered per island using the same bounding-box-based `geopandas.read_file(bbox=...)` approach used for the WDPA protected-area data, given its similarly large global scope.

Four of five islands returned genuine cyclone track records: Fiji (143 records), Lakshadweep (4), Maldives (5), and Seychelles (2). The Canary Islands file, confirmed independently across two separately-named filtering attempts, returned zero cyclone track records — accepted as a genuine finding rather than an acquisition gap, consistent with the Canary Islands' geographic position outside the typical Atlantic tropical cyclone formation and travel corridor.

A data-quality issue specific to this dataset was identified during inspection: the primary intended wind-speed field, `WMO_WIND` (the wind speed as assessed by the WMO-designated regional meteorological authority for a given basin), was populated for only a minority of records — for example, only 1 of 5 Maldives records and 31 of 143 Fiji records carried a non-null `WMO_WIND` value. Given that IBTrACS separately reports wind-speed estimates from numerous individual national agencies (`USA_WIND`, `REU_WIND`, `BOM_WIND`, `TOK_WIND`, `CMA_WIND`, `HKO_WIND`, and others, each populated only for storms that agency specifically tracked), a consolidation step was implemented using `pandas`' `bfill(axis=1)` across a prioritized list of these agency-specific wind columns, selecting the first available non-null value per record regardless of which specific agency had reported it. This improved usable wind-speed coverage substantially for Fiji (from 31 to 87 of 143 records with any available wind-speed value), though coverage for the three smaller-sample islands (Maldives, Seychelles, Lakshadweep) remained limited by the underlying scarcity of recorded storms in those regions, rather than by any deficiency in the consolidation method itself — confirmed by testing the same multi-agency consolidation logic against those islands and finding no additional records recovered beyond what the initial four-agency check had already found.

This consolidated wind-speed field, along with a reduced set of relevant columns (storm ID, season, name, timestamp, nature, position, consolidated wind speed, and distance-to-land), was saved as a new `_final.gpkg` file per island, replacing the much wider raw IBTrACS export (which carried over 150 columns, the majority representing per-agency fields with no data for most storms) as the dataset used in all subsequent analysis.

## Final Status of This Phase

| Dataset | Islands With Full Coverage | Notes |
|---|---|---|
| Elevation | All 5 | Cross-validated against known peak elevations |
| Slope | All 5 | 3 islands reprojected; Seychelles generated from elevation |
| Population | 4 of 5 | Lakshadweep deferred; all 4 validated against real-world totals |
| Cyclone Tracks | 4 of 5 | Canary Islands genuinely absent; wind-speed consolidated across agencies |

This phase completed the full baseline dataset inventory required before beginning the project's core multi-temporal and cross-dataset analyses, covered in the remaining parts of this log.

---

*Continued in Part 5: Multi-Temporal Analysis Core (Mangrove Time Series, Coral Bleaching Stress, Physical Exposure, Compound Vulnerability Score).*

----------------------------------------------------------------------------------------------------

# Development Log — Part 5 of 6: Multi-Temporal Analysis Core (Mangrove Time Series, Coral Bleaching Stress, Physical Exposure, Compound Vulnerability Score)

## Status
Complete. This part covers the project's central analytical work: constructing genuinely multi-temporal ecosystem trend data (rather than relying on single before/after snapshots), quantifying physical exposure, and combining both into a composite vulnerability measure.

---

## Why Multi-Temporal, Not Single-Snapshot

The ecosystem-buffer data acquired in Part 3 represented only a single point in time. Testing whether mangroves or coral reefs were genuinely degrading required data at multiple, well-separated points in time, following a design principle already established through direct experience earlier in this line of work: a single before/after comparison is vulnerable to being driven by noise or an atypical reference period, whereas a finding confirmed across multiple independent time points is substantially more credible.

## Mangrove Time Series: Three Independent Points

The Global Mangrove Watch (GMW) archive was identified as providing pre-processed, ready-to-use annual mangrove extent snapshots rather than requiring extent to be derived manually from raw satellite imagery. Three time points were selected for acquisition: 1996 (the earliest available baseline), 2010 (a mid-point), and 2020 (the most recent available single-year snapshot at time of acquisition), providing a 24-year span with an intermediate check rather than a single 24-year jump that could obscure whether any observed change was gradual or concentrated in a shorter sub-period.

A naming-convention distinction in the GMW archive was noted and deliberately navigated: files are provided both as single-year snapshots (for example, `gmw_v3_2020_vec.zip`) and as change-detection products spanning a date range (for example, `gmw_v3_f1996_t2020_vec.zip`, where "f" denotes "from" and "t" denotes "to"). Since this project's approach was to independently derive area change from three separately-verified snapshots rather than rely on GMW's own internal change-detection algorithm, the three single-year snapshot files were used, not the pre-computed change file.

Each global GMW shapefile (ranging from approximately 894 to 948 megabytes) was filtered per island using the same memory-efficient `bbox`-parameter approach used for WDPA and IBTrACS in earlier phases, avoiding the need to load the full global mangrove dataset into memory. This produced per-island, per-year mangrove extent files for the three years, for the four islands where mangroves are present (Lakshadweep confirmed absent, as established in Part 3).

### Bug: Feature Count Is Not a Valid Proxy for Area

An initial comparison across the three time points used raw polygon feature counts per island as a quick indicator of change, and appeared to show a substantial decline for Fiji — 5,608 features in 1996 versus 4,810 in 2020, an apparent 14.2% reduction. This was not accepted as a finding without further verification, given that polygon feature count and actual mapped area are not equivalent measures: a single large contiguous mangrove area could be represented as one polygon in one year's dataset and as several smaller adjacent polygons in another year's dataset (or vice versa) due to differences in the underlying satellite classification algorithm's segmentation behavior, with no actual change in total mangrove area.

To test this directly, all three years' data for each of the three mangrove-present islands were reprojected to an equal-area coordinate reference system (EPSG:6933, appropriate for accurate area calculation, as opposed to geographic coordinates which distort area depending on latitude) and summed to produce total area in square kilometers rather than feature counts. This produced a materially different and more reliable result: Fiji's mangrove area was essentially stable across all three time points (485.72 km² in 1996, 487.97 km² in 2010, 488.41 km² in 2020, a net increase of 0.6%), and Maldives and Seychelles showed area changes of less than 0.01 km² across the full 24-year span in both cases — confirming that the apparent decline suggested by feature counts was an artifact of polygon segmentation differences between GMW's processing of different years' source imagery, not a genuine reduction in mangrove extent. This finding — that mangrove extent has remained essentially stable across all three tested islands over nearly a quarter-century — directly informed the project's later hypothesis-testing framing, distinguishing it from the coral reef finding described below.

## Coral Reef Condition: Thermal Stress Time Series

Because coral reef degradation manifests primarily as bleaching (a health/condition change driven by thermal stress) rather than a measurable reduction in mapped physical extent, a fundamentally different data source and metric was required for corals than for mangroves. The Allen Coral Atlas, initially considered, was found to provide only a single-snapshot composite map (built from 2018–2020 imagery) rather than a genuine multi-year time series, making it unsuitable for this project's temporal-trend requirement.

NOAA Coral Reef Watch's Degree Heating Week (DHW) product was identified as the appropriate alternative: a continuous daily satellite-derived measure of accumulated thermal stress, available from 1985 to the present, where values above 4°C-weeks are associated with significant coral bleaching and values above 8°C-weeks are associated with severe bleaching and coral mortality. This directly measures the physiological stress driver of coral degradation rather than attempting to detect area loss, which is scientifically appropriate given that coral reef structures can persist physically for years after a bleaching event even as the living coral tissue itself dies.

### Bug: Access Denied, Then Wrong Variable Name

Data access was obtained via NOAA's ERDDAP data server, queried programmatically via constructed URL requests rather than manual download, following the same API-based acquisition pattern used throughout this project. The first access attempt failed with an HTTP 403 Forbidden error. This was diagnosed as the server rejecting Python's default `requests` library user-agent string, treating it as an automated bot request; the fix was to explicitly set a browser-style `User-Agent` header (`"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`) on the request, after which the server began accepting requests (returning an HTTP 500 error instead of 403, confirming access was now permitted but a different issue remained).

The resulting HTTP 500 error message (`destinationVariableName=CRW_DHW wasn't found in datasetID=noaacrwdhwDaily`) indicated the wrong variable name had been requested. The dataset's actual metadata page was consulted directly to find the correct variable name, `degree_heating_week`, which resolved the request successfully once substituted.

### Bug: A Coordinate That Fell on Land

Four of five islands returned valid, non-null DHW time series immediately using representative offshore coordinate points. The Canary Islands point initially chosen returned an entirely empty series (305 of 305 values null), traced to the coordinate falling on or too close to land or an otherwise invalid pixel in the 5km-resolution grid — plausible given the Canary Islands' comparatively small landmass relative to the dataset's spatial resolution, where a coordinate only slightly misplaced could fall outside any valid ocean pixel. Three alternative offshore coordinates were tested with a minimal single-month request each to quickly identify a working location without repeating a full 24-year download for each candidate; one (south of Gran Canaria) returned a valid non-null value, and was used to re-request the complete Canary Islands time series, this time successfully.

### DHW Trend Result

Comparing an early reference period (1996–2000 average) against a recent period (2016–2020 average) across all five islands, four showed an increase in average thermal stress: Maldives (+0.17°C-weeks), Fiji (+0.10), Lakshadweep (+0.08), and most substantially, Seychelles (+0.68°C-weeks, with a maximum recorded single-reading value of 10.47°C-weeks — within the range associated with severe bleaching and mortality). The Canary Islands showed a slight decrease (−0.05°C-weeks), the only island of the five not showing an increasing thermal-stress trend, itself consistent with Canary Islands' distinct Atlantic climate regime relative to the four Indian Ocean and Pacific islands.

## Physical Exposure: Settlement-Level Sea-Level-Rise Risk

Physical exposure was quantified by sampling the elevation raster at each settlement point's centroid coordinate (using `rasterio`'s `sample` method) across all five islands, and calculating the proportion of settlements at or below a standard one-meter sea-level-rise exposure threshold. This produced a wide and geographically consistent range: 99.1% of Maldives settlements at risk, 78.3% for Seychelles, 77.8% for Lakshadweep, 32.0% for Fiji, and 12.1% for the Canary Islands — directly reflecting the same low-lying-atoll-versus-volcanic-terrain distinction already established through the elevation cross-validation described in Part 4.

## Compound Vulnerability Score

A composite score was constructed combining the two independently-validated risk signals — physical SLR exposure and coral thermal stress trend — normalized to a common 0–1 scale using min-max normalization across the five islands for each input variable, then averaged with equal weighting. Mangrove trend was not included as a weighted input to this score, since the multi-temporal analysis had found no measurable decline in any tested island to weight.

The resulting ranking placed Seychelles as the highest overall compound-vulnerability island (score 0.880), followed by Maldives (0.651), Lakshadweep (0.467), Fiji (0.217), and Canary Islands (0.000, the reference minimum by construction of the normalization). This result was noted as directly illustrating the project's central methodological argument: Maldives has substantially higher physical exposure alone (99.1% versus Seychelles' 78.3%), yet Seychelles produces a higher overall compound score once ecosystem degradation is incorporated — demonstrating that physical exposure alone, considered in isolation, would misidentify which island carries the greatest actual compound risk.

## Final Status of This Phase

| Analysis | Result |
|---|---|
| Mangrove extent (1996/2010/2020) | Stable across all 3 tested islands; no decline detected |
| Coral thermal stress (1996–2020) | Increasing in 4 of 5 islands; Seychelles most severe |
| Physical SLR exposure | Wide variation, 12.1%–99.1% of settlements at risk |
| Compound Vulnerability Score | Seychelles ranked highest; Canary Islands lowest |

---

*Continued in Part 6: Governance Alignment Test, Settlement Encroachment Analysis, and Final Synthesis.*

----------------------------------------------------------------------------------------------------

# Development Log — Part 6 of 6: Governance Alignment Test, Settlement Encroachment Analysis, and Final Synthesis

## Status
Complete. This part covers the project's two final analytical components — testing whether formal protected-area governance aligns with verified risk, and testing whether human settlement is encroaching into ecosystem buffer zones over time — followed by a synthesis of the complete project's findings.

---

## Adding a Governance Dimension

Following completion of the core ecological and physical vulnerability analysis, a deliberate extension was added to connect the project more directly to policy and governance evaluation, reflecting the intended relevance to environmental-policy-focused academic programs rather than a purely natural-science framing. Rather than treating protected-area designation as background context, a specific, testable hypothesis was formulated: that formal protection status (WDPA coverage) should, if governance is genuinely risk-responsive, correlate positively with the independently-derived Compound Vulnerability Score already established in Part 5.

## Bug: Comparing Land Area to Marine Exclusive Economic Zones

An initial attempt to calculate a simple ratio of protected area to island land area produced a nonsensical result for Seychelles — a ratio of 1005.69, meaning the calculated protected area exceeded the island's land area by over a thousand-fold. Investigation traced this to the WDPA dataset's inclusion of Seychelles' Exclusive Economic Zone (EEZ), one of the largest in the world relative to national landmass (encompassing over a million square kilometers of ocean), which had been captured by the bounding-box filtering approach used to extract WDPA data in Part 3. Comparing this vast marine protected area figure directly against a small land-area denominator produced a ratio with no meaningful interpretation.

This was corrected by restricting the protected-area calculation to a 10-kilometer coastal buffer zone around each island's boundary, rather than the entire captured WDPA extent, on the reasoning that a settlement's actual exposure to nearby ecosystem protection is meaningfully related to nearby coastal protection, not to a offshore marine protected area potentially hundreds of kilometers distant. This was implemented by buffering each island's boundary geometry by 10 kilometers (after reprojecting to an equal-area CRS), and calculating the spatial intersection between this buffer and each island's WDPA polygons before summing area. This produced substantially more interpretable ratios — Seychelles fell from 1005.69 to 11.32, still the highest of the five islands but no longer nonsensical, with Maldives at 3.90, Canary Islands at 2.32, Fiji at 0.42, and Lakshadweep at 0.00 (consistent with its confirmed zero WDPA coverage established in Part 3).

## Governance-Alignment Result

A Pearson correlation was calculated between each island's Compound Vulnerability Score and its coastal-buffer WDPA ratio, using `scipy.stats.pearsonr`. This produced a correlation coefficient of r=0.727 — a moderately strong positive relationship, with Seychelles (highest vulnerability) also showing the highest protection ratio — but a p-value of 0.164, which does not meet the conventional 0.05 significance threshold. This was interpreted and reported honestly as a suggestive but not statistically confirmatory finding: the direction of the relationship is consistent with risk-responsive governance, but a sample of only five islands provides insufficient statistical power to establish this relationship with confidence, a limitation of small sample size directly analogous to a similar statistical-power limitation encountered and explicitly documented in prior causal-inference work with a comparably small country sample.

## Settlement Encroachment: Satellite-Derived Built-Up Area Change

The final analytical component tested whether settlement and infrastructure expansion was concentrated within or adjacent to ecosystem buffer zones over time, using the Normalized Difference Built-up Index (NDBI), a satellite-derived measure analogous in construction to NDVI but designed to detect built-up/urban surface rather than vegetation, calculated from Sentinel-2 shortwave-infrared and near-infrared bands. This was applied to three islands where mangroves are present (Maldives, Seychelles, Fiji), comparing a 2016 baseline period against a 2024 recent period.

### Bug: Empty Results With No Error

The first acquisition attempt, using a full calendar-year aggregation window (`P1Y`) per island, returned an HTTP 200 success status but an empty data array (`"data": []`) with `"geometryPixelCount": null` for every request across all three islands and both time periods — a silent failure pattern rather than an explicit error, requiring direct inspection of the raw JSON response structure to diagnose rather than relying on the request's success/failure status alone.

Two changes were made simultaneously to address this: the aggregation interval was changed from a full year (`P1Y`) to six-month periods (`P6M`), based on the same lesson learned earlier in this project's NO₂ and NDVI acquisition work that certain Sentinel Hub aggregation interval lengths are handled inconsistently depending on data type; and an explicit `maxCloudCoverage: 30` filter was added to the request, since persistently empty results across an entire year-long window for tropical island locations were also consistent with cloud cover preventing any usable clear-sky observation from being included in the aggregation. Following both changes, all six requests (three islands × two time periods) returned populated data successfully.

### Encroachment Result

Comparing average NDBI values between the two periods, both Maldives (+0.0461) and Seychelles (+0.1135) showed a clear increase in built-up-index values, consistent with genuine settlement and infrastructure expansion in or near ecosystem buffer zones between 2016 and 2024. Seychelles' change was the more pronounced of the two, and notably crossed from a negative average value (vegetation-dominated) in 2016 to a positive average value (built-up-dominated) in 2024. Fiji showed effectively no change (−0.0008), consistent with the stability already observed in Fiji's mangrove extent data from Part 5.

## Final Synthesis

Across all analytical components, Seychelles consistently emerged as the island showing the strongest evidence of a compounding, self-reinforcing vulnerability pattern: the highest Compound Vulnerability Score (driven substantially by the most severe coral thermal-stress trend of any island tested), the highest coastal protected-area ratio (a governance response that, while not statistically confirmed given the small sample, is directionally consistent with risk-awareness), and the most pronounced settlement encroachment signal of the three islands tested for this measure. Fiji, by contrast, showed a consistently stable profile across every temporal measure tested — stable mangrove extent, the smallest coral thermal-stress increase among the four islands showing any increase at all, and effectively no settlement encroachment — providing an internally consistent low-change comparison case against Seychelles' consistently high-change profile.

The mangrove-decline hypothesis (H2), tested with the same rigor and multi-point validation as every other component of this project, was not supported by the evidence across any of the three islands where it could be tested — a result reported transparently as a genuine finding rather than adjusted, downplayed, or omitted to better fit the project's originally hypothesized framing. This is treated as a substantive contribution in its own right: it demonstrates that ecosystem buffer degradation is not a uniform phenomenon across ecosystem types, and that coral reef systems in this five-island sample show measurably greater vulnerability to ongoing environmental pressure than mangrove systems over the same multi-decadal period — a distinction with direct implications for how conservation and adaptation resources might be prioritized across ecosystem types, rather than allocated under an assumption of uniform ecosystem risk.

## Complete Project Data Inventory

| Category | Coverage |
|---|---|
| Settlements, Tourism, Infrastructure | 5 islands each |
| Mangroves (multi-temporal, 3 time points) | 4 islands (Lakshadweep genuinely absent) |
| Coral Reefs (extent) | 4 islands (Canary Islands genuinely absent) |
| Coral Thermal Stress (24-year time series) | 5 islands |
| Protected Areas (WDPA) | 4 islands (Lakshadweep genuinely absent) |
| Elevation, Slope | 5 islands each |
| Population | 4 islands (Lakshadweep deferred) |
| Cyclone Tracks | 4 islands (Canary Islands genuinely absent) |
| Settlement Encroachment (NDBI) | 3 islands (mangrove-present islands only) |

## Design Principle Reinforced

This project's development consistently applied the same evidence-first discipline established in prior work: every zero-result or unexpected finding (Lakshadweep's absent mangroves, Canary Islands' absent corals and cyclones, the mangrove-decline hypothesis's lack of support) was investigated and either confirmed as genuine or traced to a specific, fixable technical cause, rather than assumed to be an error or silently worked around. Where a hypothesis was not supported by the data — most significantly, the absence of measurable mangrove decline — this was reported as a substantive finding in its own right rather than reframed or minimized, consistent with the project's stated methodological commitment to evidence-based rather than narrative-driven conclusions.

---------------------------------------------------------------------------------------------------

# Development Log — Addendum: Cyclone Damage Proxy as Supporting Evidence

## Status
Complete. This addendum covers the addition of cyclone-driven satellite damage detection as supporting evidence, conducted after the six core development-log parts had already been written, and documents both the scope decision behind adding it and a significant data-availability constraint discovered during its execution.

---

## Context and Rationale

The core DOUBLE JEOPARDY analysis (documented in Parts 1 through 6) centers on sea-level-rise exposure and ecosystem buffer degradation as its two primary compounding factors, with cyclone activity treated as background context rather than a primary analytical pillar — a deliberate scope decision made after data acquired for an earlier, differently-framed version of this island-nations project (built around cyclone impact specifically) revealed that meaningful cyclone-intensity variation existed only for Fiji, with the remaining four islands showing historically weak, low-intensity storm records unsuitable for detecting a genuine damage signal.

Rather than discarding this cyclone-related work entirely once the project's core framing shifted toward sea-level-rise and ecosystem degradation, a decision was made to retain it as explicit supporting evidence — a smaller, clearly-scoped addition rather than a re-expansion of the project's core analytical structure. Two Sentinel-2-derived NDVI before-after comparisons, previously produced during the earlier project phase for Fiji's two strongest historically recorded cyclones (Winston, 2016, and Yasa, 2020), were confirmed to still exist in the project's data folder, unaffected by the subsequent folder rename from the project's earlier working title to its final name.

## Attempting to Extend Coverage to the Remaining Four Islands

Before finalizing Fiji as the sole island with cyclone damage evidence, an attempt was made to extend the same satellite-based damage-detection approach to Maldives, Seychelles, and Lakshadweep, using each island's single strongest historically recorded cyclone from the IBTrACS wind-speed data already established in Part 4. This required first identifying each island's peak-intensity cyclone event and its date, since the appropriate before/after imagery window depends directly on knowing when the event occurred.

## Discovery: A Satellite-Record Start-Date Constraint

Constructing the acquisition script surfaced a constraint that had not been explicitly considered up to this point: Sentinel-2, the satellite source used for all NDVI-based analysis throughout this project, was launched in 2015, meaning no Sentinel-2 imagery exists for any date before that year. Checking each of the three candidate islands' strongest recorded cyclone dates against this constraint revealed that all three predated Sentinel-2's operational availability — Maldives' strongest recorded cyclone occurred in 2006, Seychelles' in 1996, and Lakshadweep's in 1997 — meaning no valid "before" imagery could exist for any of them regardless of how the acquisition request was constructed, since the satellite itself did not yet exist at the time of these historical events.

This check was implemented directly in the acquisition script as an explicit pre-condition (checking the cyclone year against a 2016 cutoff before attempting any Sentinel Hub request), rather than allowing the script to proceed and produce an uninformative empty-data response that would then require separate diagnosis, following the pattern established elsewhere in this project of building known constraints directly into acquisition logic rather than discovering them only through failed requests. Running this script confirmed all three islands were correctly and immediately skipped, each with an explicit printed reason, rather than silently returning no data.

## Interpretation and Reporting Decision

This finding was not treated as a gap to work around — for example, by substituting a later, weaker cyclone event for one of the three affected islands purely to produce some result — but as a genuine, structural limitation of satellite-based historical verification: any remote-sensing method is inherently bounded by the operational start date of the satellite platform being used, and events predating that start date cannot be verified by that method regardless of how the acquisition is configured. This is documented transparently as a scope constraint on the cyclone-damage supporting evidence specifically (affecting only this one supplementary analysis), rather than affecting the project's core sea-level-rise or ecosystem-degradation findings, which do not depend on Sentinel-2's temporal coverage in the same way.

## Final Cyclone Damage Proxy Status

| Island | Cyclone Damage Evidence | Reason |
|---|---|---|
| Fiji | Available (Winston 2016, Yasa 2020) | Both events post-date Sentinel-2 availability |
| Maldives | Not available | Strongest recorded cyclone (2006) predates Sentinel-2 |
| Seychelles | Not available | Strongest recorded cyclone (1996) predates Sentinel-2 |
| Lakshadweep | Not available | Strongest recorded cyclone (1997) predates Sentinel-2 |
| Canary Islands | Not applicable | No cyclone events recorded in this region (established in Part 4) |

The two available Fiji results — a clear NDVI decline (−0.0246) following Cyclone Winston (150 knots, Category 5-equivalent intensity) versus no clear decline (+0.0049) following Cyclone Yasa (115 knots) — are retained as supporting evidence that satellite-detectable vegetation damage in this sample only emerges at extreme storm intensity, consistent with and reinforcing the broader pattern of ecosystem stability observed in Fiji's multi-temporal mangrove data (Part 5), rather than being presented as a general finding extrapolated to the other four islands.

## Design Principle Reinforced

This addendum reinforces a constraint-awareness principle distinct from, but related to, patterns established earlier in this project: where prior sessions dealt primarily with verifying that acquired data was correct once obtained (checking bounding boxes, validating population totals, confirming genuine ecological absences), this case required recognizing a structural limitation of the acquisition method itself — the fixed start date of a satellite platform — before attempting acquisition, rather than discovering it only through an empty or failed result. Building this kind of known methodological boundary directly into request logic, with an explicit and immediately visible skip reason, is treated as preferable to allowing a script to run to completion and produce an ambiguous empty result requiring separate post-hoc diagnosis.

----------------------------------------------------------------------------------------------------

# Development Log — Part 7: Dashboard Development, Interactive Maps, and Live-Data Features

## Status
Complete (ongoing additions possible). This part covers the transition from completed data analysis to a public-facing Streamlit dashboard: page architecture, styling, QGIS-based interactive map integration, and several significant debugging efforts specific to embedding QGIS2Web exports inside Streamlit.

---

## Dashboard Architecture Decision

Following the pattern established in prior project work, a multi-page Streamlit dashboard was built with a category-based page structure mirroring the project's analytical structure rather than its data-acquisition structure: Study Design, Ecological Findings, Physical Exposure, Compound Vulnerability, Governance & Encroachment, Explore Trends, Interactive Maps, and Methodology & Data. A shared `styles.py` module was created early, centralizing all CSS and a color palette dictionary (`PALETTE`) imported by every page, so that a single visual-design change (for example, adjusting the color scheme's saturation) could propagate across the entire dashboard without editing each page individually — a decision that proved directly useful when the color palette was later revised twice for increased contrast and boldness.

## Styling Iteration: From Muted to Bold

An initial color palette (soft blues and greens, moderate font weights) was judged, after review, to look visually "faint" and lacking presence for a scientific dashboard intended to make a strong impression in an application context. The palette was revised to darker, higher-contrast tones (navy `#072a4d`, cyan `#0096c7`, forest green `#1b4332`) with font weights increased across headers, metrics, and card labels (700–900 weight throughout, versus 400–600 in the initial version). This was implemented as a single revision to the shared `styles.py` file rather than page-by-page edits, directly validating the earlier architectural decision to centralize styling.

A recurring visibility issue was identified and fixed across the dashboard's use of `st.expander()`: expander section headers and their disclosure-triangle icons were rendering in a color too close to the background to be visibly distinguishable, particularly problematic because an invisible expand/collapse icon gives no visual affordance that a section is interactive. This was resolved with a targeted CSS rule forcing the expander icon's `fill`, `stroke`, and `color` properties to explicit black across multiple possible internal DOM selectors (`svg`, `path`, and `::marker` pseudo-elements), since Streamlit's internal expander markup structure was not fully predictable from the visible page alone and required covering several selector variants to guarantee the fix applied regardless of the specific rendering path used.

## Plotly Chart Text-Color Bug

Several Plotly charts (the Compound Vulnerability Score bar chart, the governance-alignment scatter plot, the NDBI encroachment bar chart) initially rendered with axis tick labels and legend text in a very light, near-invisible color against the dashboard's white background — despite the chart's `font` color parameter appearing to be set. This was traced to Plotly's `layout.font` setting not automatically cascading to axis tick labels, which require their own explicit `tickfont` color specification per axis, and to legend text similarly requiring its own `legend.font` color setting rather than inheriting from the general layout font. All affected charts were corrected by explicitly setting `xaxis=dict(tickfont=dict(color="#000000"))`, `yaxis=dict(tickfont=dict(color="#000000"))`, and `legend=dict(font=dict(color="#000000"))` individually, rather than relying on a single top-level font color to propagate.

## Building the Interactive Maps Page: A Multi-Stage Debugging Process

The Interactive Maps page required embedding QGIS2Web-exported interactive web maps (built separately in QGIS, exported as standalone HTML/JavaScript/OpenLayers applications) inside the Streamlit dashboard. This proved to be the single most debugging-intensive component of the dashboard-building phase, requiring several distinct fixes applied in sequence.

### Bug 1: Local File Protocol Blocked by Browser Security

The first embedding attempt read each exported map's `index.html` file directly from disk in Python and injected its content into Streamlit via `components.html()`, with an added `<base href="file:///...">` tag intended to let the browser resolve the map's relative asset paths (JavaScript libraries, layer data files) against their actual disk location. This approach failed silently — the map area rendered entirely blank, with no error message — because modern browsers block `file://`-protocol resource loading from within an embedded iframe context as a security measure, regardless of how the base path is constructed.

### Bug 2: Streamlit's Static-Serving Configuration Location

The fix required serving the exported map files over genuine HTTP rather than the file system, using Streamlit's built-in static-file-serving feature (enabled via a `.streamlit/config.toml` file with `enableStaticServing = true`, serving files placed in a `static/` folder at the `/app/static/` URL path). This required two rounds of path-confusion debugging: first, the config file was initially created in the wrong directory (the project's outer root folder rather than the `dashboard/` subfolder that Streamlit treats as its working directory when launched via `streamlit run app.py` from within that subfolder) and was therefore silently ignored; second, confirming the correct location required explicitly checking the current working directory with `pwd` before each file-creation step, since terminal navigation errors (`cd` commands run from an already-nested directory, producing a non-existent doubled path) recurred multiple times during this process and needed to be diagnosed via directory-listing commands rather than assumed correct.

### Bug 3: Zoom Level Not Preserving Across Islands

Once static serving was working and interactive maps were loading, a distinct and initially puzzling issue emerged: only the first-loaded island's map (Maldives) displayed at its correctly exported, zoomed-in extent; every other island's map loaded showing the entire world at minimum zoom, requiring the user to manually zoom in to see the actual data. This was investigated systematically rather than assumed to be a QGIS export error: opening each exported `index.html` file directly via double-click (bypassing Streamlit entirely) confirmed every individual export was correctly zoomed when viewed standalone, ruling out an export-configuration problem. A simple Python HTTP server (`python -m http.server`) was used as an intermediate diagnostic step, confirming maps also displayed correctly when served over genuine HTTP outside of Streamlit's iframe context, further narrowing the fault to something specific to the Streamlit embedding itself.

The root cause was ultimately identified as a known OpenLayers behavior when initializing inside a hidden DOM container: the dashboard's original tab-based layout (`st.tabs()`) renders all tab panels' content into the DOM simultaneously, using CSS `display: none` to visually hide inactive tabs rather than omitting them from the page entirely. OpenLayers measures its container's pixel dimensions at map-initialization time to calculate how to fit the map extent to the viewport; a container with `display: none` reports zero width and height at that moment, causing the fit-to-extent calculation to fail silently and fall back to a default world-view zoom. Only the first tab, being visible and correctly sized at initial page load, avoided this failure.

This diagnosis was cross-verified using an external AI assistant as a second-opinion technical review, following a structured prompt describing the exact symptom pattern and previously-attempted fixes; the resulting analysis (independently identifying the same `st.tabs()` hidden-container root cause and OpenLayers zero-dimension measurement behavior) was consistent with the diagnosis reached through direct debugging, providing additional confidence in the fix before implementing it. The corrective decision was made to replace `st.tabs()` with `st.selectbox()` for switching between islands across all interactive map sections: unlike tabs, a selectbox's non-selected options are never rendered into the DOM at all, so the map's container is only ever created once genuinely visible and correctly sized, eliminating the zero-dimension race condition entirely rather than attempting to force a resize after the fact.

A secondary resize fix (`window.addEventListener('load', ...)` triggering `map.updateSize()` after a short delay) was also implemented and applied to all exported map HTML files via a small automation script, as an additional safeguard layer, though the `st.tabs()`-to-`st.selectbox()` change was the change that directly resolved the underlying issue.

## Ecosystem Buffer Maps: Dynamic, Data-Availability-Aware Legends

The Ecosystem Buffer Overview maps required a legend explaining the map's color scheme (mangroves, coral reefs, protected areas, island boundary), but three of the five islands lack one or more of these layers entirely (Lakshadweep has no mangroves or protected areas; Canary Islands has no mangroves or coral reefs, both confirmed as genuine ecological absences in Part 3). Rather than displaying a static legend listing all four possible layer types regardless of which island is selected — which would misleadingly imply all four layers are present for every island — the legend was implemented to dynamically generate itself based on a per-island list of genuinely present layers, so that Lakshadweep's legend shows only "Coral Reefs" and "Island Boundary," and Canary Islands' legend shows only "Protected Areas" and "Island Boundary," directly reflecting what the underlying map actually contains for that specific island.

## Mangrove Trend Maps: A QGIS2Web Export Failure and the Decision to Fall Back to Static Images

An attempt to build interactive QGIS2Web exports for the Mangrove Extent Trend maps (three overlapping year-layers per island, 1996/2010/2020) encountered a persistent `KeyError: 'size_unit'` failure inside qgis2web's internal `olStyleScripts.py` styling-export module, affecting the 1996 and 2010 layers specifically while the 2020 layer for the same islands exported without error. A structured diagnostic prompt was used to investigate the underlying cause with an external AI assistant, given the highly qgis2web-internals-specific nature of the error; the resulting diagnosis attributed the failure to an incomplete symbol-layer property dictionary on the historical layers (likely inherited from an older QGIS session state that did not populate a `size_unit` key qgis2web's exporter expects, versus the 2020 layer's more recently-touched, complete symbol definition), consistent with the qgis2web exporter reading style properties via direct dictionary access rather than a defensive `.get()` call with a fallback default. A practical workaround — copying the 2020 layer's proven-working style onto the 1996 and 2010 layers via QGIS's "Copy Style" / "Paste Style" feature — was identified as the fastest fix, though given the additional time this would require across three affected islands, a decision was made to abandon the interactive QGIS2Web export approach for this specific map category and instead produce static PNG exports directly from QGIS's Print Layout feature, embedding the resulting images in the dashboard via `st.image()` rather than `components.iframe()`. This was documented in the dashboard itself with a brief, honest note explaining the substitution ("shown as a static image ... due to a QGIS2Web export limitation with historical polygon datasets") rather than presenting the change silently.

## Live-Recalculating Interactive Features

Two dashboard sections were built to recalculate results live from underlying data rather than displaying only pre-computed, fixed numbers, adding a genuinely interactive analytical dimension beyond static reporting.

### Compound Vulnerability "What-If" Weighting Slider

The Compound Vulnerability Score, as originally computed, weights physical SLR exposure and coral thermal-stress trend equally (50/50). An interactive slider was added allowing a dashboard user to adjust this weighting themselves (0–100% SLR exposure, with the remainder allocated to coral stress) and see the resulting island ranking recompute and re-sort live using the same underlying normalized 0–1 values used in the original analysis. This required first independently verifying the exact min-max normalized values for both input variables (rather than re-deriving them informally), computed via a short verification script and cross-checked against the values already embedded in the slider's implementation before finalizing the feature — confirming Seychelles remains the highest-ranked island across a wide range of weighting choices, providing the dashboard user direct, hands-on evidence of the finding's robustness to the specific 50/50 weighting choice used in the primary analysis.

### Physical Exposure Live SLR-Threshold Slider

Similarly, the Physical Exposure page's headline statistics (percentage of settlements at or below 1 meter elevation, per island) were originally static, pre-computed figures. A live-recalculating version was built by first exporting every individual settlement's sampled elevation value (rather than only the final aggregate percentage) to a CSV file covering all five islands, then building a slider allowing the threshold to be adjusted between 0.5 and 5.0 meters, with the per-island percentage-at-risk bar chart recomputing directly from the underlying 6,000+-row elevation dataset on each slider movement.

Building this elevation-export script surfaced a data-consistency issue requiring a specific fix: the earlier decision (documented in the Compound Vulnerability analysis) to treat exactly-zero elevation values as invalid/NoData had been verified and justified specifically for the Canary Islands DEM, where spot-checking confirmed genuine NoData artifacts. Applying this same zero-as-NoData rule universally to all five islands during the elevation-export script's first run produced an implausible result — Maldives dropped from an expected 996 settlements with elevation data to only 10 — because Maldives, being a genuine low-lying atoll nation, has many settlements with legitimately near-zero elevation that a blanket NoData rule incorrectly discarded. The script was corrected to apply the zero-as-NoData treatment only to the Canary Islands specifically (the one island where this was empirically verified), leaving zero-elevation values as valid data for the other four islands; re-running the corrected script produced settlement counts matching the previously-established, validated figures for all five islands (996 for Maldives, 244 for Seychelles, 1,323 for Fiji, 36 for Lakshadweep, and a slightly reduced 4,834 for Canary Islands reflecting its genuinely-excluded NoData points), confirming the fix.

## Home Page: Hypothesis-Outcome Summary Cards

The dashboard's home page was extended with a "Three Hypotheses, Three Outcomes" section presenting H1, H2, and H3 as individually color-coded outcome cards (supported / not supported / suggestive-but-inconclusive) immediately below the page's core-finding summary, giving a first-time dashboard visitor an at-a-glance view of the project's three central results before navigating into any individual analysis page — addressing an earlier observation that individual dashboard pages, while each substantively complete, benefited from a stronger top-level orientation summarizing the project's overall shape before a visitor commits to exploring any one page in depth.

## Status of Interactive Map Categories

| Category | Format | Status |
|---|---|---|
| SLR Exposure (5 islands) | Interactive (QGIS2Web) | Complete, zoom-issue resolved |
| Ecosystem Buffer Overview (5 islands) | Interactive (QGIS2Web) | Complete, dynamic per-island legend |
| Mangrove Extent Trend (3 islands) | Static (PNG via QGIS Print Layout) | Complete, substitution documented in-dashboard |
| Settlement Encroachment (map form) | Not built | Deliberately scoped out — numeric NDBI findings already presented as charts on the Governance & Encroachment page; a dedicated spatial map was judged non-essential given time constraints |

## Design Principle Reinforced

This phase reinforced two patterns already established earlier in the project. First, an unexpected or silently-failing result (the blank map from the `file://` protocol block, the world-zoom default from the hidden-container race condition) was investigated to a specific, verified root cause rather than worked around with an untested guess — in the zoom-level case, this included deliberately using a minimal, protocol-independent HTTP server as an isolated diagnostic step to narrow the fault before attempting any fix. Second, when a genuine tooling limitation was identified (the qgis2web historical-layer export bug) and a proper fix would have cost disproportionate additional time relative to its benefit, the decision to substitute a simpler, reliable alternative (static PNG export) was made deliberately and documented transparently within the dashboard itself, rather than either silently omitting the affected map category or spending further disproportionate time forcing the original approach to work.