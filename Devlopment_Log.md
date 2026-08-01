# DOUBLE JEOPARDY: The Vulnerability Spiral — Quantifying Compound Coastal Risk and Governance-Evidence Alignment Across Five Island Nations

## Project Overview

DOUBLE JEOPARDY tests whether small island nations face a compounding vulnerability to sea-level rise: high physical exposure combined with degrading natural coastal defenses. Instead of assuming all coastal ecosystems degrade the same way, the project tests each ecosystem type independently — mangroves and coral reefs — across five island nations spanning three ocean basins: Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands. Mangrove and coral trajectories are tracked separately rather than lumped into one "ecosystem buffer" score, then combined with physical exposure into a composite vulnerability assessment.

Beyond the ecological and physical risk numbers, the project also asks a governance question: does formal protected-area designation — the main tool island governments and international bodies point to when they say coastal ecosystem risk is being managed — actually line up with where the verified risk is highest? That turns this from a purely environmental-science project into something closer to a policy-evaluation exercise, testing whether governance response tracks the evidence or is spatially disconnected from it. That's directly relevant to environmental economics, adaptation-finance prioritization, and marine spatial governance.

## Problem Statement

Climate adaptation policy and nature-based-solutions financing tend to treat coastal ecosystems as one protective category, assuming mangroves and coral reefs degrade together and jointly determine a settlement's sea-level-rise exposure. That assumption doesn't get tested very often against independent, multi-temporal evidence at a systematic, cross-national scale. If ecosystems are actually degrading at different rates — or in different directions entirely — then adaptation planning that treats the buffer as one category risks misallocating resources and misjudging which coastal zones are genuinely at risk.

There's a second problem layered on top of the first: formal protected-area status gets treated, in national policy and in international financing frameworks, as a stand-in for effective ecosystem management. But protected-area boundaries are often drawn based on historical, political, or administrative reasons rather than continuously updated risk data. Whether protection status in these five islands actually corresponds to the places with the highest verified ecological and physical vulnerability — or is a "paper park" situation, spatially disconnected from where the risk actually sits — hadn't been tested using independent, satellite-derived evidence before this project.

## Aim

Build a reproducible geospatial framework that (1) independently quantifies physical sea-level-rise exposure and multi-temporal ecosystem trajectory — tracked separately for mangroves and coral reefs — across five island nations, producing a composite, evidence-based vulnerability assessment; and (2) tests whether existing protected-area governance is statistically aligned with that verified vulnerability, or represents a measurable governance-evidence gap.

## Research Questions

**RQ1 (Ecological/Physical)**: Does physical sea-level-rise exposure combine with ecosystem buffer degradation to produce compounding settlement-level vulnerability across five island nations — and does this operate the same way across ecosystem types, or does it depend on which ecosystem is actually degrading in a given location?

**RQ2 (Governance)**: Does the spatial distribution of formal protected-area designation (WDPA) correlate with empirically verified compound vulnerability — pointing to evidence-responsive governance — or is protection status statistically independent of, or even inversely related to, actual satellite-derived ecosystem risk?

## Hypotheses

**H1 (Coral Pathway)**: Coral reef ecosystems will show a statistically detectable increase in thermal bleaching stress over a multi-decadal period, more pronounced in islands with higher physical sea-level-rise exposure.

**H2 (Mangrove Pathway)**: Mangrove ecosystems will show a statistically detectable decline in spatial extent over the same period, as an independent compounding pathway alongside coral degradation. This one gets tested with the same rigor as H1, and reported honestly regardless of what the data actually shows.

**H3 (Governance-Evidence Alignment)**: Islands and coastal zones with higher composite vulnerability scores will show correspondingly higher protected-area coverage, consistent with risk-responsive governance. No relationship, or an inverse one, would itself be a real finding — that protection in this sample isn't empirically risk-driven — and gets reported either way.

## Objectives

- Build a settlement-level physical exposure dataset across five island nations using elevation and slope data, identifying the share of settlements below a one-meter sea-level-rise threshold.
- Build a multi-temporal mangrove extent dataset using the Global Mangrove Watch archive, testing for genuine area-based decline across multiple independent time points rather than one before/after snapshot.
- Build a multi-temporal coral reef thermal stress dataset using satellite-derived Degree Heating Week data, testing for a measurable rise in bleaching-level heat stress over time.
- Combine physical exposure and ecosystem degradation into a composite Compound Vulnerability Score at the island level.
- Quantify formal protected-area (WDPA) coverage at the island and coastal-zone level and test its statistical relationship to the Compound Vulnerability Score.
- Test whether settlement and infrastructure expansion disproportionately shows up within or next to ecosystem buffer zones over time, using satellite-derived built-up area change detection.
- Check every ecosystem-trend finding against multiple independent time points instead of one comparison.
- Package all of this into a reproducible geospatial framework and interactive dashboard that communicates both the vulnerability findings and the governance-alignment analysis in a way that's directly useful for adaptation policy and conservation-finance decisions.

## Methodology Summary

Physical exposure comes from intersecting elevation and slope data with settlement locations across all five islands, then calculating the share of settlements at or below a one-meter elevation threshold. Ecosystem degradation is tracked separately for the two ecosystem types: mangrove extent, using multiple independent time points from the Global Mangrove Watch archive to test for genuine multi-decadal area change; and coral reef condition, using a continuous multi-decadal satellite thermal-stress time series, comparing early-period and recent-period averages. Physical exposure and the two ecosystem signals are then combined into a normalized Compound Vulnerability Score per island.

The governance piece quantifies the extent and density of formally designated protected areas (from the World Database on Protected Areas) per island and, where resolution allows, per coastal zone, then statistically compares that against the Compound Vulnerability Score — testing directly whether higher-risk zones are more, equally, or less likely to be formally protected. That turns the ecological findings into a testable statement about policy effectiveness rather than leaving governance as unexamined commentary at the end.

A later phase tests whether settlement and infrastructure expansion, from satellite-based built-up area change detection, is disproportionately concentrated within or near ecosystem buffer zones — testing whether human response to environmental pressure ends up reinforcing the same vulnerability it's responding to, and whether that encroachment is more common inside or outside formally protected boundaries.

## Study Area

Five island nations spanning three ocean basins: Maldives and Lakshadweep (Indian Ocean), Seychelles (western Indian Ocean), Fiji (South Pacific), and the Canary Islands (eastern Atlantic) — chosen for consistent multi-source data availability plus geographic, geological, and climatic diversity, so the compound vulnerability and governance-alignment framework gets tested across genuinely different island contexts, protection regimes, and administrative systems rather than a single case.

## Expected Outputs

- A settlement-level physical exposure dataset across five island nations.
- A validated multi-temporal mangrove extent dataset.
- A validated multi-decadal coral reef thermal stress dataset.
- A composite Compound Vulnerability Score and risk ranking across all five islands.
- A governance-alignment analysis testing the statistical relationship between protected-area coverage and verified vulnerability, including any "governance-evidence gap" zones — high verified risk with low or no formal protection.
- A settlement/infrastructure encroachment analysis testing the ecosystem-buffer feedback hypothesis, broken down by protection status.
- An interactive geospatial dashboard and open-source codebase, extensible to more islands and ecosystem types.

## Relevance

This project speaks directly to climate adaptation policy, nature-based-solutions financing, ecosystem-services valuation, and marine spatial governance. Its contribution is really two things: first, showing that treating coastal ecosystem protection as one undifferentiated category can hide materially different risk profiles, which means rigorous, ecosystem-specific, multi-temporal verification matters more than an assumed uniform-decline narrative; and second, actually testing — instead of assuming — whether existing conservation governance instruments line up with verified risk, which gives a transferable method for evaluating adaptation-finance and protected-area prioritization decisions in any coastal or island context facing compound climate vulnerability.

## Current Status

Project Concept Finalized
Version 1.0

---

# Development Log — Part 1: Project Setup and Data Architecture Design

## Status
Complete. Covers the initial project structure decisions made once the research question and five-island study area were locked in, before any data acquisition started.

---

## Starting Point

With the research question set — does physical sea-level-rise exposure compound with ecosystem buffer degradation across five islands, and does that differ by ecosystem type — the first real decision was how to structure the project folder in a way that actually fit this study's needs, instead of just reusing a generic template.

## Folder Structure: Category-Based, Not Island-Based

Two options were on the table before writing any acquisition code: organize by island (a Maldives folder, a Seychelles folder, each holding all its own data types), or organize by data category (a settlements folder, a mangroves folder, each holding all five islands' files).

Went with category-based, for a reason tied directly to the methodology. Since the core analysis needs to compare the same variable across all five islands at once — coral bleaching stress across islands, encroachment rates across islands — an island-based structure would mean digging into five separate folders every time a cross-island script runs, and it's easy to end up with an inconsistent naming convention in one island's folder versus another's. Category-based keeps every version of a given dataset together, so a cross-island script is just a loop over island names reading from one folder, and it's immediately obvious if any island's file is missing from a category, since all five should be sitting right next to each other.

The top-level structure ended up as:

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

## One Deliberate Inconsistency

Worth flagging one departure from the category-based rule: the raw multi-temporal Global Mangrove Watch archives (1996, 2010, 2020 snapshots) live in their own `mangroves/` folder, separate from the cleaned per-island files inside `ecosystem_buffers/`. That's practical, not sloppy — the raw GMW shapefiles are enormous (roughly 900–950MB per year, covering the whole globe) and get processed once into much smaller per-island, per-year extracts. Keeping the giant source archives physically apart from the small final files made it easy to later exclude the bulky raw archives from version control while still tracking the lightweight outputs, without scattering folder-level exceptions everywhere.

## Environment Setup

Reused the `gpie2` conda environment already set up and tested in prior work, instead of starting fresh. That environment had already been fixed for a nasty numerical-computing issue (a corrupted Intel MKL backend, resolved by installing NumPy and SciPy with the `nomkl` OpenBLAS backend instead), and reusing it meant not risking that same failure mode showing up again in a clean environment. Two files carried straight over: `auth_sentinelhub.py` (the Sentinel Hub OAuth module) and the `.env` file with Copernicus Data Space credentials, since the API access patterns and credentials were identical to what this project would also need for its own Sentinel-2 work.

## Why This Mattered Later

This upfront structure paid off once multi-temporal analysis started: because every mangrove-year file, every coral time series file, and every island's settlement file sat in a predictable, category-consistent spot, later scripts looping across all five islands (elevation exposure, mangrove area comparison, coral stress trends) could be written generically, with the island name as the only thing changing between iterations, instead of five near-duplicate scripts hardcoded to five different folder layouts.

---

*Continued in Part 2: Core Dataset Acquisition and Cleanup (Settlements, Tourism, Infrastructure).*

---

# Development Log — Part 2: Core Dataset Acquisition and Cleanup (Settlements, Tourism, Infrastructure)

## Status
Complete. Covers acquisition and cleaning of the three OpenStreetMap-derived datasets that form the human-activity baseline: settlements, tourism infrastructure, and general infrastructure.

---

## Source and Acquisition

All three datasets came from OpenStreetMap via Overpass Turbo queries filtered to each island's extent, producing one raw GeoJSON export per island per category — fifteen files total. OSM was the practical choice for consistency and free access across all five islands, which span five different national administrative systems (Maldives, India, Seychelles, Fiji, Spain) where no single government dataset covers all five the same way.

## The Column-Bloat Problem

Every raw OSM export came in with an absurd number of columns — commonly 200 to 240 — most of it irrelevant: place-name translations into dozens of languages (`name:ta`, `name:zh-Latn-pinyin`, `wikipedia:ur`, and so on), Wikidata cross-references, contact info, and other OSM tagging noise that has nothing to do with a settlement's identity, population, or location. Keeping all of that meant carrying dead weight in every file for no analytical benefit, and made manual inspection during development a pain.

The same cleaning pattern got applied to all fifteen files: read with `geopandas`, trimmed down to the columns that actually mattered (settlements: name, place type, population, geometry; tourism: name, tourism type, amenity type, geometry; infrastructure: name, man-made feature type, amenity type, power infrastructure type, geometry), and saved as a new `_clean.gpkg`, leaving the raw GeoJSON untouched. Settlement files went from up to 240 columns down to 4 or 5, without losing a single row or any field that was actually needed.

## Bug: Sea Features Mislabeled as Settlements

While validating the cleaned settlement files, the Maldives and Lakshadweep bounding boxes both looked implausibly large — way outside the expected island extent. Two rows turned out to be the culprit in both files: "Arabian Sea" and "Laccadive Sea." Not settlements at all — OSM features for named bodies of water that got swept up by the Overpass Turbo place-type query, since OSM's `place` tagging is applied inconsistently across contributors and occasionally includes large water-body labels alongside genuine settlements.

Found this by computing each settlement's centroid coordinates, sorting by longitude, and checking the extreme values at both ends — the two sea-name entries stuck out immediately, sitting far outside the real settlement cluster. Removed both rows directly from the cleaned `.gpkg` files (Maldives: 998 → 996 rows; Lakshadweep: 38 → 36 rows) without needing to re-pull from OpenStreetMap.

## Bug: Invalid Geometry in Tourism Data

Cleaning the Canary Islands tourism dataset, `geopandas.read_file()` threw `GEOSException: Invalid number of points in LinearRing found 2 - must be 0 or >= 4` — a hard crash meaning at least one polygon had fewer than the four coordinate pairs needed for a valid ring. Known defect pattern in crowd-sourced OSM polygon data.

Fixed by passing `on_invalid="ignore"` to `geopandas.read_file()`, which drops unreadable geometries instead of raising, followed by an explicit check for any null geometries after the read. That confirmed exactly two invalid rows in the Canary tourism file (10,877 → 10,875 valid rows after dropping them). The same `on_invalid="ignore"` + null-geometry check became a standard step in every later vector-cleaning script, since this class of malformed-polygon defect could plausibly show up in any OSM file.

## Duplicate and Naming Cleanup

A few naming inconsistencies showed up here, part of a pattern that recurred throughout the project of manually re-run exports producing near-duplicate files under slightly different names. Fiji's protected-area-adjacent file existed twice, as `FIJI_INFRAA_SLR.gpkg` (typo, extra "A") and `FIJI_INFRA_SLR.gpkg`, identical in size — deleted the typo'd copy. Same handling pattern used every time this came up elsewhere in the project: check file sizes or row counts to confirm whether the copies actually differ, then delete confirmed duplicates rather than leaving ambiguous near-identical files sitting around.

## Final Status of This Phase

| Dataset | Islands Covered | Typical Column Reduction |
|---|---|---|
| Settlements | 5 (2 outlier rows removed from 2 islands) | ~240 → 4–5 |
| Tourism | 5 (2 invalid rows removed from 1 island) | ~200–490 → 4 |
| Infrastructure | 5 | ~200 → 4 |

All fifteen files confirmed clean, correctly bounded, and free of invalid geometries by the end of this phase — the human-activity baseline used through the rest of the project, including the encroachment analysis much later.

---

*Continued in Part 3: Ecosystem Data (Mangroves, Coral Reefs, Protected Areas).*

---

# Development Log — Part 3: Ecosystem Data (Mangroves, Coral Reefs, Protected Areas)

## Status
Complete. Covers the three ecosystem-buffer datasets central to the project's core hypothesis testing: mangrove extent, coral reef extent, and protected areas.

---

## Two Different Source Types

Unlike settlements/tourism/infrastructure (uniformly from OSM across all five islands), the ecosystem-buffer data came from two structurally different sources depending on the island, which meant two separate cleaning pipelines instead of one shared script.

Fiji, Lakshadweep, and Seychelles mangrove/coral data came from WCMC's Global Mangrove Watch and coral reef atlases — identifiable right away from the uppercase column convention: `LAYER_NAME`, `METADATA_I`, `NAME`, `FAMILY`, `GENUS`, `SPECIES`, `DATA_TYPE`, `GIS_AREA_K`, `REP_AREA_K`. Maldives and Canary Islands data for the same two categories came from OSM instead, same lowercase `place`/`natural`/`tourism` schema as the settlements data. So every mangrove/coral cleaning script needed to know (or detect) which source format a given island used and apply the right column-selection logic — a `WCMC_KEEP_COLUMNS` list versus an OSM-style one, not one universal set.

## Bug: The Maldives "Coral" File Wasn't Coral Data

The biggest data-quality problem in this phase: `coral_maldives.gpkg` had 4,230 rows and 79 columns on first inspection. Looking at the column list, a bunch had nothing to do with coral reefs — `cuisine`, `spa`, `restaurant`, `rooms`, `payment:visa`, `payment:mastercard`, `opening_hours`, `parking`. This wasn't a filtered coral-reef dataset — it was basically an unfiltered general OSM export for the Maldives region that happened to be named like it was coral-specific.

Filtered it down using OSM's reef tagging convention (`natural == "reef"`), which correctly picked out 2,921 of the 4,230 rows as genuine coral reef polygons — the other 1,309 were unrelated tourism/hospitality/amenity points that had gotten mixed into the same export. A `reef` attribute column with a single consistent value (`"coral"`) across the correctly-tagged rows confirmed the filter had isolated the right feature type. Doing this filtering step before any column cleanup meant downstream analysis wasn't quietly diluted by thousands of irrelevant tourism records.

## Real Ecological Absences, Not Data Gaps

Two islands came back with zero results for specific ecosystem categories, and both got investigated and confirmed as genuine absences rather than acquisition failures — the standard applied throughout the project: any zero result is a hypothesis to check, not an error to silently paper over.

Lakshadweep returned zero mangrove features across every source checked. That fits — mangroves are ecologically rare in this specific archipelago, a small coral-atoll chain without the muddy intertidal delta conditions mangroves usually need. Accepted as a real finding.

The Canary Islands returned zero coral reef features, which fits its subtropical, volcanic, cooler-water Atlantic setting — outside the warm tropical shallow-water range coral needs. This got reinforced later when a Global Mangrove Watch bounding-box query for an unrelated multi-temporal analysis also came back empty for the Canary Islands even after deliberately widening the search box, giving independent cross-confirmation that this island's coastal ecology genuinely differs from the tropical islands rather than pointing to a systematic acquisition problem specific to one dataset.

## Protected Areas: Swapping Out a Weak Source

The protected-area dataset originally used for four islands (Maldives, Canary Islands, Seychelles, Fiji) came from OpenStreetMap via the QuickOSM plugin, and on inspection had an implausibly small number of features per island — as few as one protected area for Fiji, four for Maldives. That looked like incomplete coverage rather than genuinely sparse protection, since these regions are known to have plenty of formally gazetted marine and terrestrial protected areas.

Switched to the World Database on Protected Areas (WDPA), the authoritative global dataset from UNEP-WCMC. The full WDPA download (about 4.15GB, split by the provider into three sequentially numbered zip archives due to shapefile attribute-table size limits) was extracted, and each of the three polygon shapefiles was filtered per island using `geopandas.read_file()`'s `bbox` parameter — reading only the relevant subset off disk rather than loading the whole multi-gigabyte global file into memory, the same memory-efficient approach already needed elsewhere in the project for datasets this size. Results from all three archive parts were then combined per island.

Feature counts jumped substantially: Maldives 4 → 93, Fiji 1 → 126 (after combining two sub-queries needed to cover Fiji's territory, which straddles the antimeridian), Seychelles 4 → 49, Canary Islands 258 → 385. Lakshadweep independently confirmed zero WDPA-registered protected areas, matching its earlier zero result from OpenStreetMap — cross-source confirmation this is a real finding about Lakshadweep, not a source-specific artifact. The old QuickOSM-derived files were deleted and replaced with WDPA-derived ones across all four islands where WDPA data existed.

Raw WDPA features carried 34 columns each, covering the full range of standard metadata (governance type, ownership type, management authority, IUCN category, verification status, and more). Trimmed to nine columns actually relevant here: name, designation, designation type, IUCN category, legal status, status year, and both reported and GIS-calculated area — enough to assess protection type and extent without carrying administrative metadata nothing in this project actually uses.

## Final Status of This Phase

| Dataset | Islands With Data | Confirmed Genuine Absences |
|---|---|---|
| Mangroves | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |
| Coral Reefs | Maldives, Fiji, Lakshadweep, Seychelles | Canary Islands |
| Protected Areas (WDPA) | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |

This phase set the ecosystem-buffer baseline used both for the project's static ecosystem context and, later, as the foundation for the full multi-temporal analysis in Part 5.

---

*Continued in Part 4: Terrain, Population, and Cyclone Track Data.*

---

# Development Log — Part 4: Terrain, Population, and Cyclone Track Data

## Status
Complete. Covers the remaining baseline datasets: elevation and slope (terrain), population density, and historical cyclone tracks.

---

## Terrain: Elevation and Slope

Elevation data (Copernicus DEM) came in for all five islands already in the correct EPSG:4326 coordinate system — no reprojection needed there.

Slope data needed fixing for three of the five islands (Canary, Fiji, Lakshadweep), which arrived in EPSG:3857 instead of the project's standard EPSG:4326. Reprojected using `rasterio`'s `calculate_default_transform` and `reproject` with bilinear resampling — appropriate for continuous elevation-derived data, unlike the nearest-neighbor resampling categorical data like land cover would need. Seychelles didn't have a slope file at all; instead of treating it as a separate missing dataset, generated it directly from the already-validated Seychelles elevation raster using GDAL's `gdaldem slope` command, producing a correctly-projected slope raster without pulling in any new external source.

Checked elevation values against known geography as a sanity check rather than just trusting the numbers. Canary Islands topped out around 3,696m, which lines up with Mount Teide (Spain's highest peak, about 3,715m). Seychelles topped out around 904m, matching its granite mountain terrain (Morne Seychellois). Maldives and Lakshadweep both stayed in a roughly 0–20m range throughout, consistent with being low-lying coral atoll nations. This cross-check gave confidence the elevation data was processed correctly and hadn't gotten silently corrupted or misaligned somewhere along the way.

## Population: Checked Against Real Numbers

Population density rasters (WorldPop, 2020) were acquired for four of five islands (Fiji, Seychelles, Maldives, and Canary Islands — the last one clipped from Spain's national population raster). Lakshadweep didn't get population data in this phase; the only access method found at the time meant downloading a raster covering the whole of India, which felt impractical for the small area actually needed, so it got deferred as lower priority.

Each acquired raster was validated by summing all pixel values to get a total estimated population, then checking that against independently known real-world figures — not just assumed correct because the script ran without errors. All four matched reasonably closely: Canary Islands came out around 2.09 million against an actual figure of roughly 2.2 million; Fiji around 896,000 against roughly 900,000; Seychelles around 98,000 against roughly 100,000; Maldives around 540,000, in line with its known range. Treated this validation step as essential, not optional — a dataset that processes cleanly isn't the same thing as a dataset that's correct.

One large raster (Fiji's population file) initially failed with `rasterio.errors.RasterioIOError: cannot allocate 884736000 bytes` on a standard full-array read. Fixed by reading in tiled blocks via `rasterio`'s `block_windows` iterator instead of loading the whole array at once, accumulating sum/min/max incrementally across blocks — same memory-efficient pattern needed elsewhere in this project for other unusually large files.

## Cyclone Tracks: IBTrACS and a Wind-Speed Consolidation Problem

Historical cyclone track data came from IBTrACS (International Best Track Archive for Climate Stewardship), NOAA's standard global cyclone dataset combining reports from over a dozen meteorological agencies. Filtered the full global shapefile per island using the same bounding-box `geopandas.read_file(bbox=...)` approach used for WDPA.

Four of five islands came back with genuine cyclone records: Fiji (143), Lakshadweep (4), Maldives (5), Seychelles (2). Canary Islands, checked twice under two separately named filtering attempts, came back with zero — accepted as a real finding, consistent with the Canary Islands sitting outside the typical Atlantic tropical cyclone formation and travel corridor.

Found a data-quality issue here too: the intended wind-speed field, `WMO_WIND` (wind speed as assessed by the WMO-designated regional authority for a given basin), was populated for only a minority of records — just 1 of 5 for Maldives, 31 of 143 for Fiji. Since IBTrACS separately reports wind-speed estimates from various national agencies (`USA_WIND`, `REU_WIND`, `BOM_WIND`, `TOK_WIND`, `CMA_WIND`, `HKO_WIND`, and others, each populated only for storms that agency tracked), used `pandas`' `bfill(axis=1)` across a prioritized list of these agency columns to pick the first available non-null value per record regardless of which agency reported it. That improved Fiji's usable wind-speed coverage from 31 to 87 of 143 records. Coverage for the three smaller-sample islands (Maldives, Seychelles, Lakshadweep) stayed limited, but that's the underlying scarcity of recorded storms there, not a shortcoming of the consolidation method — confirmed by running the same multi-agency check against those islands and finding nothing extra beyond what the initial four-agency check had already caught.

The consolidated wind-speed field, plus a reduced column set (storm ID, season, name, timestamp, nature, position, consolidated wind speed, distance-to-land), got saved as a new `_final.gpkg` per island, replacing the much wider raw IBTrACS export (over 150 columns, most of them per-agency fields with no data for most storms) as the working dataset for everything downstream.

## Final Status of This Phase

| Dataset | Islands With Full Coverage | Notes |
|---|---|---|
| Elevation | All 5 | Cross-checked against known peak elevations |
| Slope | All 5 | 3 islands reprojected; Seychelles generated from elevation |
| Population | 4 of 5 | Lakshadweep deferred; all 4 checked against real-world totals |
| Cyclone Tracks | 4 of 5 | Canary Islands genuinely absent; wind-speed consolidated across agencies |

This phase closed out the full baseline dataset inventory needed before starting the project's core multi-temporal and cross-dataset analyses, covered next.

---

*Continued in Part 5: Multi-Temporal Analysis Core (Mangrove Time Series, Coral Bleaching Stress, Physical Exposure, Compound Vulnerability Score).*

---

# Development Log — Part 5: Multi-Temporal Analysis Core (Mangrove Time Series, Coral Bleaching Stress, Physical Exposure, Compound Vulnerability Score)

## Status
Complete. The project's central analytical work: building genuinely multi-temporal ecosystem trend data instead of relying on single before/after snapshots, quantifying physical exposure, and combining both into a composite vulnerability measure.

---

## Why Multi-Temporal

The ecosystem-buffer data from Part 3 was only a single point in time. Testing whether mangroves or coral reefs were actually degrading needed data at multiple, well-separated points — a single before/after comparison is too easy to have been driven by noise or an unusual reference period, where a finding that holds across multiple independent time points is a lot more convincing.

## Mangrove Time Series: Three Points

The Global Mangrove Watch (GMW) archive provides pre-processed, ready-to-use annual mangrove extent snapshots, so extent didn't need to be derived from raw imagery by hand. Three time points: 1996 (earliest available baseline), 2010 (midpoint), and 2020 (most recent single-year snapshot available at the time) — a 24-year span with a check in the middle rather than one big 24-year jump that could hide whether change was gradual or concentrated in a shorter window.

Worth noting the GMW archive provides files both as single-year snapshots (e.g. `gmw_v3_2020_vec.zip`) and as change-detection products spanning a date range (e.g. `gmw_v3_f1996_t2020_vec.zip`, "f" for "from," "t" for "to"). Since the plan here was to independently derive area change from three separately-verified snapshots rather than lean on GMW's own change-detection algorithm, the three single-year files got used, not the pre-computed change file.

Each global GMW shapefile (roughly 894–948MB) was filtered per island using the same `bbox`-based approach already used for WDPA and IBTrACS, avoiding a full global-dataset load. That produced per-island, per-year mangrove extent files for the four islands where mangroves are present (Lakshadweep confirmed absent in Part 3).

### Bug: Feature Count Isn't a Valid Area Proxy

An early comparison across the three time points used raw polygon feature counts as a quick change indicator, and it looked like a real decline for Fiji — 5,608 features in 1996 versus 4,810 in 2020, an apparent 14.2% drop. Didn't take that at face value, since feature count and actual mapped area aren't the same thing: one large contiguous mangrove area can be represented as a single polygon in one year's data and as several smaller adjacent polygons in another year, purely from differences in how the satellite classification algorithm segments that year's imagery — no actual area change involved.

Tested this directly by reprojecting all three years for each of the three mangrove-present islands into an equal-area CRS (EPSG:6933 — appropriate for area calculation, unlike geographic coordinates, which distort area depending on latitude) and summing total area in km² instead of feature counts. Got a materially different, more reliable result: Fiji's mangrove area was essentially stable across all three points (485.72 km² in 1996, 487.97 in 2010, 488.41 in 2020 — a net increase of 0.6%), and Maldives and Seychelles both showed less than 0.01 km² of change across the full 24-year span. So the apparent decline from feature counts was a segmentation artifact between different years' source imagery, not a real reduction in mangrove extent — mangrove extent held essentially stable across all three tested islands over nearly a quarter-century, which directly shaped how the project later framed its hypothesis testing.

## Coral Reef Condition: A Thermal Stress Time Series

Coral degradation shows up mainly as bleaching — a health/condition change from thermal stress — rather than a measurable drop in mapped physical extent, so this needed a different data source and metric than the mangrove analysis. The Allen Coral Atlas, considered first, turned out to be only a single-snapshot composite (built from 2018–2020 imagery), not a genuine multi-year time series, so it didn't fit the temporal-trend requirement here.

NOAA Coral Reef Watch's Degree Heating Week (DHW) product was the right fit instead: a continuous daily satellite-derived measure of accumulated thermal stress, available from 1985 to the present, where values above 4°C-weeks are linked to significant coral bleaching and above 8°C-weeks to severe bleaching and coral mortality. This measures the physiological stress driver directly rather than trying to detect area loss, which makes sense given coral reef structures can physically persist for years after a bleaching event even after the living coral itself has died.

### Bug: Access Denied, Then the Wrong Variable Name

Access went through NOAA's ERDDAP server, queried via constructed URL requests rather than manual download, matching the API-based pattern used everywhere else in this project. First attempt failed with HTTP 403 Forbidden — the server was rejecting Python's default `requests` user-agent string as a bot request. Fixed by explicitly setting a browser-style `User-Agent` header (`"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`), after which the server started accepting requests (returning a 500 instead of a 403 — access granted, different problem remaining).

The 500 error (`destinationVariableName=CRW_DHW wasn't found in datasetID=noaacrwdhwDaily`) meant the wrong variable name had been requested. Checked the dataset's actual metadata page directly and found the correct name, `degree_heating_week`, which fixed the request once swapped in.

### Bug: A Coordinate That Landed on Solid Ground

Four of five islands returned valid, non-null DHW series right away using representative offshore coordinates. The Canary Islands point initially chosen came back entirely empty (305 of 305 values null) — traced to the coordinate falling on or too close to land, or otherwise on an invalid pixel in the 5km-resolution grid, plausible given how small the Canary Islands' landmass is relative to that grid resolution. Tested three alternative offshore coordinates with a quick single-month request each rather than repeating a full 24-year download for every candidate; one south of Gran Canaria returned a valid value, and got used to re-pull the full Canary Islands series successfully.

### DHW Trend Result

Comparing an early reference period (1996–2000 average) against a recent one (2016–2020), four islands showed rising thermal stress: Maldives (+0.17°C-weeks), Fiji (+0.10), Lakshadweep (+0.08), and most significantly Seychelles (+0.68, with a single maximum recorded reading of 10.47°C-weeks — in the range for severe bleaching and mortality). Canary Islands showed a slight decrease (−0.05), the only island of the five not trending upward, in line with its distinct Atlantic climate regime relative to the four Indian Ocean and Pacific islands.

## Physical Exposure: Settlement-Level Sea-Level-Rise Risk

Physical exposure came from sampling the elevation raster at each settlement's centroid (via `rasterio`'s `sample` method) across all five islands, then calculating the share of settlements at or below a one-meter sea-level-rise threshold. Wide, geographically consistent spread: 99.1% of Maldives settlements at risk, 78.3% Seychelles, 77.8% Lakshadweep, 32.0% Fiji, 12.1% Canary Islands — directly reflecting the low-atoll-versus-volcanic-terrain distinction already established through the elevation cross-check in Part 4.

## Compound Vulnerability Score

Combined the two independently validated risk signals — physical SLR exposure and coral thermal-stress trend — normalizing each to a common 0–1 scale (min-max across the five islands) and averaging with equal weighting. Mangrove trend wasn't included as a weighted input here, since the multi-temporal analysis hadn't found any measurable decline to weight in.

Resulting ranking: Seychelles highest (0.880), then Maldives (0.651), Lakshadweep (0.467), Fiji (0.217), Canary Islands (0.000, the reference minimum by construction). This is exactly the project's central methodological point made concrete: Maldives has substantially higher physical exposure alone (99.1% versus Seychelles' 78.3%), yet Seychelles comes out with the higher overall score once ecosystem degradation gets folded in — exposure alone would have picked the wrong island as highest-risk.

## Final Status of This Phase

| Analysis | Result |
|---|---|
| Mangrove extent (1996/2010/2020) | Stable across all 3 tested islands; no decline detected |
| Coral thermal stress (1996–2020) | Increasing in 4 of 5 islands; Seychelles most severe |
| Physical SLR exposure | Wide variation, 12.1%–99.1% of settlements at risk |
| Compound Vulnerability Score | Seychelles ranked highest; Canary Islands lowest |

---

*Continued in Part 6: Governance Alignment Test, Settlement Encroachment Analysis, and Final Synthesis.*

---

# Development Log — Part 6: Governance Alignment Test, Settlement Encroachment Analysis, and Final Synthesis

## Status
Complete. The two final analytical pieces — testing whether protected-area governance lines up with verified risk, and whether settlement is encroaching into ecosystem buffer zones over time — plus a synthesis of the full project.

---

## Adding a Governance Dimension

After the core ecological and physical vulnerability analysis wrapped up, a deliberate extension got added to connect the project more directly to policy evaluation rather than leaving it as a purely natural-science exercise. Instead of treating protected-area designation as background context, a specific testable hypothesis got formulated: that formal protection status (WDPA coverage) should, if governance is genuinely risk-responsive, correlate positively with the Compound Vulnerability Score from Part 5.

## Bug: Comparing Land Area to Marine EEZs

A first attempt at a simple protected-area-to-land-area ratio gave a nonsense result for Seychelles — 1005.69, meaning the calculated protected area exceeded island land area by over a thousand-fold. Traced this to the WDPA dataset including Seychelles' Exclusive Economic Zone (one of the largest in the world relative to national landmass, over a million km² of ocean), which the bounding-box filtering from Part 3 had swept up along with the land-based protected areas. Comparing that vast marine figure against a tiny land-area denominator was never going to produce anything interpretable.

Fixed by restricting the protected-area calculation to a 10km coastal buffer around each island's boundary, instead of the full captured WDPA extent — the reasoning being that a settlement's actual exposure to nearby ecosystem protection is meaningfully tied to nearby coastal protection, not to an offshore marine protected area potentially hundreds of kilometers away. Implemented by buffering each island's boundary geometry by 10km (after reprojecting to an equal-area CRS) and intersecting that buffer with each island's WDPA polygons before summing area. Much more interpretable ratios came out of this — Seychelles dropped from 1005.69 to 11.32, still the highest of the five but no longer absurd, with Maldives at 3.90, Canary Islands at 2.32, Fiji at 0.42, and Lakshadweep at 0.00 (matching its confirmed zero WDPA coverage from Part 3).

## Governance-Alignment Result

Ran a Pearson correlation between each island's Compound Vulnerability Score and its coastal-buffer WDPA ratio (`scipy.stats.pearsonr`). Came out to r=0.727 — a moderately strong positive relationship, with Seychelles (highest vulnerability) also showing the highest protection ratio — but a p-value of 0.164, missing the conventional 0.05 threshold. Reported this honestly as suggestive, not confirmatory: the direction fits risk-responsive governance, but five islands just isn't enough statistical power to be confident about it — the same small-sample-size limitation that showed up in a comparably small country-sample earlier in this line of work.

## Settlement Encroachment: Satellite-Derived Built-Up Area Change

The last analytical piece tested whether settlement and infrastructure expansion was concentrated within or near ecosystem buffer zones over time, using the Normalized Difference Built-up Index (NDBI) — built the same way as NDVI but tuned to detect built-up/urban surface instead of vegetation, calculated from Sentinel-2 shortwave-infrared and near-infrared bands. Applied to the three mangrove-present islands (Maldives, Seychelles, Fiji), comparing a 2016 baseline against a 2024 recent period.

### Bug: Empty Results, No Error

The first attempt, using a full calendar-year aggregation window (`P1Y`) per island, returned HTTP 200 success but an empty data array (`"data": []`) with `"geometryPixelCount": null` for every request across all three islands and both periods — a silent failure, not an obvious error, which needed direct inspection of the raw JSON to catch rather than trusting the request's success status alone.

Two changes together fixed it: switched the aggregation window from a full year (`P1Y`) to six months (`P6M`), based on the same lesson from this project's earlier NO₂/NDVI acquisition work that certain Sentinel Hub interval lengths behave inconsistently depending on data type; and added an explicit `maxCloudCoverage: 30` filter, since persistently empty results across a full year for tropical island locations also fit cloud cover blocking any usable clear-sky observation. After both changes, all six requests (three islands × two periods) came back populated.

### Encroachment Result

Comparing average NDBI between the two periods: both Maldives (+0.0461) and Seychelles (+0.1135) showed a clear increase, matching genuine settlement/infrastructure expansion near ecosystem buffer zones between 2016 and 2024. Seychelles' change was the bigger of the two, and notably crossed from a negative average (vegetation-dominated) in 2016 to a positive one (built-up-dominated) in 2024. Fiji showed effectively no change (−0.0008), consistent with the stability already seen in its mangrove extent data.

## Final Synthesis

Across every analytical piece, Seychelles kept coming up as the island with the strongest evidence of a compounding, self-reinforcing vulnerability pattern: highest Compound Vulnerability Score (driven largely by the most severe coral thermal-stress trend of any island tested), highest coastal protected-area ratio (a governance response that, while not statistically confirmed given the small sample, points the right direction), and the most pronounced encroachment signal of the three islands tested for that. Fiji, by contrast, stayed consistently stable across every temporal measure — stable mangrove extent, the smallest coral thermal-stress increase among the four islands showing any increase at all, and effectively no encroachment — a genuinely low-change comparison case against Seychelles' consistently high-change profile.

The mangrove-decline hypothesis (H2), tested with the same rigor and multi-point validation as everything else here, wasn't supported by the evidence in any of the three islands where it could be tested. Reporting that honestly rather than adjusting or downplaying it feels like a real contribution in its own right — it shows ecosystem buffer degradation isn't uniform across ecosystem types, and coral reefs in this five-island sample are measurably more vulnerable to ongoing environmental pressure than mangroves over the same multi-decadal period, which matters for how conservation and adaptation resources get prioritized.

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

Every zero-result or unexpected finding along the way — Lakshadweep's absent mangroves, Canary Islands' absent corals and cyclones, the mangrove-decline hypothesis not holding up — got investigated and either confirmed as genuine or traced back to a specific, fixable cause, rather than assumed to be a bug or quietly worked around. Where a hypothesis just didn't pan out, that got written up as a real finding rather than reframed to fit the original expectation.

---

# Development Log — Addendum: Cyclone Damage Proxy as Supporting Evidence

## Status
Complete. Added after the six core parts above were already written. Covers cyclone-driven satellite damage detection as supporting evidence, plus a data-availability constraint that turned up while working on it.

---

## Context and Why It Got Added

The core analysis centers on sea-level rise and ecosystem buffer degradation, with cyclone activity treated as background rather than a primary pillar — a scope call made after data from an earlier, differently-framed version of this island-nations project (originally built around cyclone impact specifically) showed meaningful cyclone-intensity variation only for Fiji, with the other four islands' historical storm records too weak and low-intensity to detect a genuine damage signal.

Rather than throwing that earlier cyclone-related work away once the project's framing shifted toward sea-level rise and ecosystem degradation, kept it as a smaller, clearly-scoped supporting addition instead of re-expanding the core analytical structure. Two Sentinel-2 NDVI before/after comparisons from that earlier project phase — Fiji's two strongest historically recorded cyclones, Winston (2016) and Yasa (2020) — were still sitting in the data folder, unaffected by the later project rename.

## Trying to Extend This to the Other Four Islands

Before settling on Fiji as the only island with cyclone damage evidence, tried extending the same satellite damage-detection approach to Maldives, Seychelles, and Lakshadweep, using each island's single strongest recorded cyclone from the IBTrACS data already established in Part 4. That meant first pinning down each island's peak-intensity event and its date, since the before/after imagery window depends on knowing when the event actually happened.

## Ran Into a Satellite-Record Start-Date Wall

Building the acquisition script surfaced something that hadn't come up explicitly before this: Sentinel-2, the satellite used for all NDVI analysis in this project, launched in 2015 — no imagery exists before that. Checking each of the three candidate islands' strongest recorded cyclone against this cutoff showed all three predated Sentinel-2 entirely: Maldives' strongest recorded cyclone was in 2006, Seychelles' in 1996, Lakshadweep's in 1997. No valid "before" imagery could exist for any of them no matter how the request was built, since the satellite simply didn't exist yet.

Built this check directly into the acquisition script as an explicit pre-condition (checking the cyclone year against a 2016 cutoff before attempting any request), instead of letting the script run and return an uninformative empty response that would need separate diagnosis — same pattern used elsewhere in this project of building known constraints into the acquisition logic up front. Running it confirmed all three islands got skipped immediately, each with an explicit printed reason.

## How This Got Reported

Didn't treat this as a gap to paper over — for example, by swapping in a weaker, later cyclone for one of the affected islands just to produce some result. It's a genuine structural limit of satellite-based verification: any remote-sensing method is bounded by when its satellite platform actually started operating, and events before that can't be verified by that method no matter how the request is configured. Documented transparently as a scope limit on this one supplementary analysis specifically — it doesn't touch the project's core sea-level-rise or ecosystem-degradation findings, which don't depend on Sentinel-2's coverage window the same way.

## Final Cyclone Damage Proxy Status

| Island | Cyclone Damage Evidence | Reason |
|---|---|---|
| Fiji | Available (Winston 2016, Yasa 2020) | Both events post-date Sentinel-2 availability |
| Maldives | Not available | Strongest recorded cyclone (2006) predates Sentinel-2 |
| Seychelles | Not available | Strongest recorded cyclone (1996) predates Sentinel-2 |
| Lakshadweep | Not available | Strongest recorded cyclone (1997) predates Sentinel-2 |
| Canary Islands | Not applicable | No cyclone events recorded in this region (Part 4) |

The two Fiji results — a clear NDVI decline (−0.0246) after Cyclone Winston (150 knots, Category 5-equivalent) versus no clear decline (+0.0049) after Cyclone Yasa (115 knots) — stand as supporting evidence that satellite-detectable vegetation damage in this sample only shows up at extreme storm intensity, which fits the broader ecosystem stability already seen in Fiji's mangrove data. Kept it framed that way — as one island's result — rather than extrapolated to the other four.

This case was a bit different from the rest of the project's debugging pattern: most of the earlier work was about verifying data was correct once it had already been acquired (checking bounding boxes, validating population totals, confirming real ecological absences). This one needed catching a structural limit of the acquisition method itself — a satellite's fixed launch date — before even attempting the acquisition, instead of only finding out through an empty result after the fact.

---

# Development Log — Part 7: Dashboard Development, Interactive Maps, and Live-Data Features

## Status
Complete (more additions possible later). Covers the move from finished data analysis to a public-facing Streamlit dashboard: page architecture, styling, QGIS-based interactive map integration, and several debugging efforts specific to embedding QGIS2Web exports inside Streamlit.

---

## Dashboard Architecture

Built a multi-page Streamlit dashboard with a category-based page structure mirroring the project's analytical structure rather than its data-acquisition structure: Study Design, Ecological Findings, Physical Exposure, Compound Vulnerability, Governance & Encroachment, Explore Trends, Interactive Maps, and Methodology & Data. Set up a shared `styles.py` module early — all CSS and a color palette dictionary (`PALETTE`) imported by every page — so a single visual change (adjusting saturation, say) could propagate across the whole dashboard without touching each page individually. That decision paid off directly when the palette got revised twice later for more contrast.

## Styling: From Muted to Bold

The first color palette (soft blues and greens, moderate font weights) ended up looking faint and lacking presence for a dashboard meant to make a strong impression. Revised it to darker, higher-contrast tones (navy `#072a4d`, cyan `#0096c7`, forest green `#1b4332`) with heavier font weights across headers, metrics, and card labels (700–900, versus 400–600 before). Implemented as one change to `styles.py` rather than page-by-page edits — directly validating the earlier call to centralize styling.

Also caught a recurring visibility bug with `st.expander()`: the expander headers and disclosure-triangle icons were rendering too close to the background color to actually see, which is a real problem since an invisible expand/collapse icon gives no hint the section is interactive. Fixed with a targeted CSS rule forcing the expander icon's `fill`, `stroke`, and `color` to explicit black across several possible DOM selectors (`svg`, `path`, `::marker`), since Streamlit's internal expander markup wasn't fully predictable and needed covering a few selector variants to make sure the fix stuck regardless of the exact rendering path.

## Plotly Text-Color Bug

Several Plotly charts (Compound Vulnerability Score bar chart, governance-alignment scatter, NDBI encroachment bar chart) initially rendered with axis labels and legend text almost invisible against the dashboard background, even though the chart's top-level `font` color looked set. Turned out Plotly's `layout.font` doesn't automatically cascade to axis tick labels — those need their own `tickfont` color per axis — and legend text needs its own `legend.font` color too, rather than inheriting from the general layout font. Fixed every affected chart by setting `xaxis=dict(tickfont=dict(color="#000000"))`, `yaxis=dict(tickfont=dict(color="#000000"))`, and `legend=dict(font=dict(color="#000000"))` individually instead of relying on one top-level color to propagate.

## Building the Interactive Maps Page

The Interactive Maps page needed to embed QGIS2Web-exported interactive maps (built in QGIS, exported as standalone HTML/JavaScript/OpenLayers apps) inside the Streamlit dashboard. This was, hands down, the most debugging-intensive part of building the dashboard.

### Bug 1: Local File Protocol Blocked by the Browser

First attempt read each exported map's `index.html` directly off disk in Python and injected it into Streamlit via `components.html()`, with a `<base href="file:///...">` tag meant to let the browser resolve relative asset paths (JS libraries, layer data) against their actual disk location. Rendered as a blank map area, no error message. Modern browsers block `file://`-protocol loading from inside an embedded iframe as a security measure, regardless of how the base path is set — that's what was happening.

### Bug 2: Static-Serving Config in the Wrong Place

Fixed by serving the exported map files over real HTTP instead of the file system, using Streamlit's built-in static-file-serving feature (`.streamlit/config.toml` with `enableStaticServing = true`, serving files from a `static/` folder at `/app/static/`). Took two rounds of path confusion to get right: first the config file got created in the outer project root instead of the `dashboard/` subfolder Streamlit actually treats as its working directory when launched via `streamlit run app.py` from inside it, so it was silently ignored; second, pinning down the correct location meant explicitly checking `pwd` before each file-creation step, since a couple of terminal navigation mistakes (running `cd` from an already-nested directory, producing a doubled path that didn't exist) kept happening and needed directory-listing commands to diagnose rather than just assuming the path was right.

*A note on where this ended up: the final deployed dashboard actually serves these maps through GitHub Pages rather than through Streamlit's own static-file serving described above. That local-dev fix genuinely worked at the time; exactly why the switch to GitHub Pages happened later isn't something I have a clean note on — it's possible Streamlit's static serving didn't carry over cleanly once the app moved to Streamlit Community Cloud, which is a known rough edge on that platform, but I can't say that with certainty. Flagging it here as the honest current state rather than guessing at a tidy explanation.*

### Bug 3: Zoom Level Not Preserving Across Islands

Once static serving was working and maps were loading, a separate and genuinely confusing issue showed up: only the first-loaded island's map (Maldives) displayed at its correctly exported zoom level; every other island loaded showing the entire world at minimum zoom, needing a manual zoom-in to see any actual data.

Investigated this properly instead of assuming it was a QGIS export problem. Opening each exported `index.html` directly (bypassing Streamlit) confirmed every individual export was correctly zoomed on its own, ruling out an export-configuration issue. Used a bare Python HTTP server (`python -m http.server`) as an intermediate check, and the maps displayed correctly served over real HTTP outside Streamlit's iframe too — narrowing the fault down to something specific about the Streamlit embedding itself.

Root cause turned out to be a known OpenLayers behavior with hidden DOM containers: the dashboard's original `st.tabs()` layout renders every tab panel's content into the DOM at once, using CSS `display: none` to visually hide inactive tabs rather than leaving them out of the page entirely. OpenLayers measures its container's pixel dimensions when the map initializes, to calculate how to fit the map extent to the viewport — a `display: none` container reports zero width and height at that moment, so the fit-to-extent calculation silently fails and falls back to a default world view. Only the first tab, visible and correctly sized at page load, avoided this.

Cross-checked this diagnosis with an external AI tool as a second opinion, describing the exact symptom pattern and what had already been tried — it independently landed on the same `st.tabs()` hidden-container / OpenLayers zero-dimension explanation, which matched what direct debugging had already found and gave more confidence before implementing the fix. Went with replacing `st.tabs()` with `st.selectbox()` for switching between islands across every interactive map section: unlike tabs, a selectbox's non-selected options never get rendered into the DOM at all, so the map container only ever gets created once it's genuinely visible and correctly sized — no zero-dimension race condition to work around.

Also added a secondary resize safeguard (`window.addEventListener('load', ...)` triggering `map.updateSize()` after a short delay) across all the exported map HTML files via a small automation script, though the `st.tabs()` → `st.selectbox()` swap was what actually fixed it.

## Ecosystem Buffer Maps: Legends That Match What's Actually There

The Ecosystem Buffer Overview maps needed a legend explaining the color scheme (mangroves, coral reefs, protected areas, island boundary), but three of the five islands are missing one or more of those layers entirely (Lakshadweep has no mangroves or protected areas; Canary Islands has no mangroves or coral reefs — both confirmed genuine ecological absences in Part 3). Instead of one static legend listing all four layer types for every island regardless of what's actually there — which would misleadingly imply all four are present everywhere — built the legend to generate itself per island based on which layers are genuinely present, so Lakshadweep's legend shows only "Coral Reefs" and "Island Boundary," and Canary Islands' shows only "Protected Areas" and "Island Boundary."

## Mangrove Trend Maps: A qgis2web Export Failure

Trying to build interactive QGIS2Web exports for the Mangrove Extent Trend maps (three overlapping year-layers per island, 1996/2010/2020) hit a persistent `KeyError: 'size_unit'` inside qgis2web's internal `olStyleScripts.py` styling module — affecting the 1996 and 2010 layers specifically, while the 2020 layer for the same islands exported fine. Used a structured diagnostic prompt with an external AI tool to dig into this, given how specific to qgis2web internals the error was; the diagnosis pointed to an incomplete symbol-layer property dictionary on the historical layers (likely carried over from an older QGIS session that never populated a `size_unit` key qgis2web's exporter expects, versus the 2020 layer's more recently-touched, complete symbol definition) — consistent with the exporter reading style properties via direct dictionary access instead of a defensive `.get()` with a fallback.

A practical fix existed (copy the 2020 layer's working style onto the 1996 and 2010 layers via QGIS's Copy Style / Paste Style), but given the extra time that would take across three affected islands, decided to drop the interactive QGIS2Web approach for this specific map category and produce static PNG exports from QGIS's Print Layout instead, embedded via `st.image()` rather than `components.iframe()`. Documented the swap directly in the dashboard with a short, honest note explaining it ("shown as a static image ... due to a QGIS2Web export limitation with historical polygon datasets") rather than making the change silently.

## Live-Recalculating Features

Two dashboard sections recalculate results live from the underlying data instead of just showing fixed, pre-computed numbers.

### Compound Vulnerability "What-If" Weighting Slider

The Compound Vulnerability Score, as originally computed, weighs physical SLR exposure and coral thermal-stress trend equally (50/50). Added a slider letting a dashboard user adjust that weighting themselves (0–100% SLR exposure, remainder to coral stress) and watch the island ranking recompute and re-sort live, using the same underlying normalized 0–1 values from the original analysis. Double-checked the exact min-max normalized values for both inputs with a short verification script before finalizing this, rather than just trusting values already sitting in the slider code — confirmed Seychelles stays the highest-ranked island across a wide range of weighting choices, giving a dashboard visitor hands-on evidence the finding isn't just an artifact of the specific 50/50 split used in the main analysis.

### Physical Exposure Live SLR-Threshold Slider

Similarly, the Physical Exposure page's headline numbers (percent of settlements at or below 1m elevation, per island) were originally static. Built a live version by first exporting every individual settlement's sampled elevation value (not just the final aggregate percentage) to a CSV covering all five islands, then adding a slider between 0.5 and 5.0 meters, with the per-island at-risk percentage recomputing directly from the underlying 6,000+ row elevation dataset on every slider move.

Building this elevation-export script surfaced a data-consistency issue that needed a specific fix: the earlier decision (from the Compound Vulnerability work) to treat exactly-zero elevation values as invalid/NoData had been verified and justified specifically for the Canary Islands DEM, where spot-checking confirmed genuine NoData artifacts there. Applying that same zero-as-NoData rule to all five islands in the elevation-export script's first run gave an implausible result — Maldives dropped from an expected 996 settlements with elevation data down to just 10 — because Maldives, being a genuine low-lying atoll nation, has plenty of settlements with legitimately near-zero elevation that a blanket NoData rule wrongly threw out. Corrected the script to apply zero-as-NoData only to the Canary Islands specifically (the one island where it was actually verified), leaving zero-elevation values as valid everywhere else; re-running it matched the previously established, validated settlement counts across all five islands (996 Maldives, 244 Seychelles, 1,323 Fiji, 36 Lakshadweep, and a slightly reduced 4,834 for Canary Islands reflecting its genuinely excluded NoData points).

## Home Page: Hypothesis-Outcome Summary Cards

Extended the home page with a "Three Hypotheses, Three Outcomes" section — H1, H2, and H3 as individually color-coded outcome cards (supported / not supported / suggestive-but-inconclusive) right below the page's core-finding summary. Gives a first-time visitor an at-a-glance view of the project's three central results before they navigate into any individual page, which felt like it was missing before — the individual pages were each substantively complete, but there wasn't a strong top-level orientation summarizing the project's overall shape before someone commits to digging into any one page.

## Status of Interactive Map Categories

| Category | Format | Status |
|---|---|---|
| SLR Exposure (5 islands) | Interactive (QGIS2Web) | Complete, zoom issue resolved |
| Ecosystem Buffer Overview (5 islands) | Interactive (QGIS2Web) | Complete, dynamic per-island legend |
| Mangrove Extent Trend (3 islands) | Static (PNG via QGIS Print Layout) | Complete, substitution documented in-dashboard |
| Settlement Encroachment (map form) | Not built | Deliberately scoped out — the numeric NDBI findings are already presented as charts on the Governance & Encroachment page; a dedicated spatial map wasn't essential given time constraints |

Two things kept showing up in this phase that are worth naming directly. First, an unexpected or silently-failing result (the blank map from the `file://` block, the world-zoom default from the hidden-container issue) got investigated to an actual root cause instead of patched with an untested guess — in the zoom case, that meant deliberately using a minimal, protocol-independent HTTP server as an isolated check before touching any code. Second, when a real tooling limitation turned up (the qgis2web historical-layer export bug) and a proper fix would've cost more time than it was worth, the decision to fall back to something simpler and reliable (static PNG export) got made deliberately and documented openly in the dashboard, instead of either quietly dropping that map category or burning disproportionate time forcing the original approach to work.

---

Went back through the Research Paper and Project Journal today specifically hunting for anything that could get challenged if someone actually checked it, starting with every reference in the bibliography. Four of the eight citations had real problems, not just typos: the "Pieraccini, M., et al. (2017)" entry had the wrong title attached entirely, matching a different 2022 conference paper by different authors — found the actual 2017 Pieraccini paper (Aquatic Conservation: Marine and Freshwater Ecosystems, 27(1), 177–196) and swapped it in. The mangrove dataset paper was credited to "Duncan, C." when the real lead author is Bunting, P. — checked the MDPI listing directly to confirm. Ferrario et al. was dated 2016 in the reference list but the paper is actually from 2014. Fixed all three, plus added the missing author name (Beth Pike) to the Marine Conservation Institute citation, which was otherwise already correct.

Beyond references, went through the methodology looking for gaps a reviewer would poke at. The physical exposure numbers are built on a 1-meter elevation threshold sampled from a 30-meter global DEM, and nowhere did the paper acknowledge that this DEM's own vertical uncertainty is non-trivial at that fine a threshold — added a limitations paragraph on this. The Compound Vulnerability Score's 50/50 weighting between exposure and coral stress was never justified in the paper, even though the dashboard's own what-if slider already tests the full weighting range and confirms Seychelles stays top-ranked regardless — that robustness result just wasn't written down anywhere, so it got added to section 3.6/4.4.

The bigger piece of work: built a population-weighted version of the exposure metric, not just settlement-count-based. Turned out more involved than expected. Lakshadweep's population data was never acquired originally because downloading all of India's population raster seemed impractical, but the actual file needed (WorldPop's constrained, UN-adjusted version) was only ~470MB, not the huge unconstrained one — got it and clipped it straight down to Lakshadweep's boundary. Fiji then broke the script twice: first because its population raster inherited the same antimeridian bounding-box issue as the WDPA data, giving it an enormous, mostly-empty pixel grid; then, after splitting into east/west-of-dateline windows (matching what was already done for WDPA), it turned out the elevation data only ever covered Fiji's western islands — Viti Levu and Vanua Levu. The Lau Islands past the dateline were never in the DEM extract at all. Ran the numbers with that gap explicitly reported rather than silently absorbed: about 21,800 people, roughly 2.4% of Fiji's population, fall outside elevation coverage and are excluded from Fiji's percentage.

The population-weighted results turned out genuinely interesting, not just a defensive addition — the ranking changes completely from the settlement-based version. Lakshadweep, third by settlement count, becomes the highest population-weighted exposure island at 87.5%, while Maldives drops from 99.1% settlement-based to 64.5% population-weighted. Added this as its own results subsection with both figures side by side, plus a paragraph on what the ranking shift actually means.

Also ran a Mann-Kendall trend test on the full 24-year coral DHW time series per island, since the paper's original coral trend was based on comparing two 5-year period averages rather than testing the whole series. The formal trend test only reaches statistical significance for Maldives (p=0.011) and Seychelles (p=0.025) — the two islands the compound vulnerability finding actually depends on — while Fiji and Lakshadweep's smaller increases don't hold up as significant across the full series. Reported this directly rather than keeping the vaguer "four of five islands" framing, since the two islands that matter most for the paper's central claim are exactly the two where the trend is statistically solid.

Also computed the actual 95% confidence interval on the governance-alignment correlation (r=0.727, n=5) instead of just calling it "moderately strong" — it comes out to [-0.43, 0.98], which makes the small-sample caveat concrete instead of asserted.

Once all of that was in the paper, went through the dashboard page by page to make sure it didn't contradict anything the paper now says. A few things needed catching up: the physical exposure page didn't have the population-weighted numbers anywhere, so added a comparison chart there alongside the original settlement-based one. The coral trend page still said "four of five islands showing an increase" without the Mann-Kendall significance breakdown, so that got tightened up to match what the paper now says specifically about which two islands are statistically solid. The methodology page had a line saying Lakshadweep's population data was "confirmed genuinely absent" — that's no longer true and needed rewriting once the WorldPop-constrained file got found. Six new static figures also got built for the paper (physical exposure by island, the population-weighted comparison, mangrove extent over time, the coral trend lines, the governance scatter, and the weighting-sensitivity curve) since the paper had really only ever had one chart for a project with this much analysis behind it — those got added to both the paper and directly beneath the matching interactive charts on the dashboard, shown by default rather than tucked behind a dropdown, so a reader can see the exact figure that's cited in the paper without it duplicating the interactive version