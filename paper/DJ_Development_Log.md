# DOUBLE JEOPARDY: Do Coastal Rules Reach the People at Risk? Comparing Five Island Jurisdictions

Development log

## Index

1. [Entry 1](#entry-1)
2. [Entry 2](#entry-2)
3. [Entry 3](#entry-3)
4. [Entry 4](#entry-4)
5. [Entry 5](#entry-5)
6. [Entry 6](#entry-6)
7. [Entry 7](#entry-7)
8. [Entry 8](#entry-8)
9. [Entry 9](#entry-9)
10. [Entry 10](#entry-10)
11. [Entry 11](#entry-11)
12. [Entry 12](#entry-12)
13. [Entry 13](#entry-13)
14. [Entry 14](#entry-14)
15. [Entry 15](#entry-15)
16. [Entry 16](#entry-16)
17. [Entry 17](#entry-17)
18. [Entry 18](#entry-18)
19. [Entry 19](#entry-19)

## Entry 1

### Project Overview

DOUBLE JEOPARDY started from one concern: low islands face a rising sea at the same time as the reefs and mangroves that shelter them come under stress. I did not want to treat all coastal ecosystems as one buffer, so I tracked mangroves and coral reefs as separate pathways across 5 island groups in 3 ocean basins: the Maldives, Lakshadweep, Seychelles, Fiji and the Canary Islands. The plan was to combine the coral signal with physical exposure into one compound score and to report mangroves on their own.

I also wanted a governance side. Governments and international bodies point to protected areas as evidence that coastal risk is being managed, so I wanted to check whether protected-area coverage actually sits where the measured risk is highest, or whether the two are unrelated. That question links the work to adaptation finance, environmental economics and marine spatial governance.

### Problem Statement

Climate finance and coastal planning often treat coastal ecosystems as a single protective category and assume that mangroves and reefs decline together. I had not found this tested with independent, multi-year data across several countries. If the two follow different paths, treating them as one buffer can send money and attention to the wrong places.

The second issue is protected areas. Designation is often read as a sign that an ecosystem is being managed, but boundaries are frequently drawn for historical or administrative reasons rather than current risk. I wanted to use satellite evidence to check whether protection in these 5 island groups follows ecological and physical vulnerability, or exists mainly on paper.

### Aim

Build a reproducible geospatial framework that measures sea-level exposure, tracks mangrove and reef change at several time points across the 5 island groups, combines them into a compound vulnerability assessment, and then tests whether protected-area coverage matches that assessment.

### Research Questions

1. Does sea-level exposure combine with ecosystem decline to raise overall risk across the 5 island groups, and does the pattern differ between mangroves and coral reefs?
2. Does official WDPA protected-area coverage follow the risk measured from satellite data, or is it independent of it?

### Hypotheses

- H1: Coral thermal stress has increased over the study period, especially on the more exposed islands.
- H2: Mangrove extent has declined over the same period, as a separate trend.
- H3: Island groups with higher compound vulnerability have more protected-area coverage. A null or opposite result would be reported as a finding too.

### Objectives

- Build a settlement-level exposure dataset from elevation and slope data, counting settlements at or below 1 m.
- Measure mangrove area change from the Global Mangrove Watch archive at several dates rather than one before/after pair.
- Track reef heat stress from satellite Degree Heating Week data.
- Combine exposure and ecosystem change into a Compound Vulnerability Score for each island group.
- Compare WDPA protected-area coverage with that score.
- Measure built-up change near ecosystem buffers with a satellite index.
- Package the scripts as a reproducible pipeline with an interactive dashboard.

### Methodology Summary

Exposure comes from elevation and slope data crossed with settlement locations, giving the share of settlements at or below 1 m. Mangroves are measured from several independent Global Mangrove Watch snapshots, and coral from a multi-decade satellite thermal stress series, comparing early and recent period means. The compound score combines exposure with the coral signal. Mangroves stay out of it and are reported separately, so that a flat input does not sit in the formula as a constant.

For governance, protected-area coverage from the World Database on Protected Areas is compared statistically with the compound score, to see whether high-risk places are more, equally or less likely to be protected. A later phase uses a satellite built-up index to check whether construction is expanding into or next to ecosystem buffers, and whether this happens more inside or outside protected boundaries.

### Study Area

The Maldives and Lakshadweep (Indian Ocean atolls), Seychelles (western Indian Ocean), Fiji (South Pacific) and the Canary Islands (eastern Atlantic). I chose them for consistent data across several sources and for their differences in geology, climate, law and administration, so the framework is tested on very different islands rather than on one case.

### Expected Outputs

- Settlement-level exposure dataset for all 5 island groups
- Multi-date mangrove extent dataset
- Multi-decade reef thermal stress dataset
- Compound Vulnerability Score and ranking
- Governance alignment analysis, looking for places with high risk and little protection
- Built-up encroachment analysis split by protection status
- Interactive dashboard and an open codebase that can be extended to other islands and ecosystems

### Relevance

The work speaks to adaptation policy, nature-based solutions finance, ecosystem service valuation and marine spatial governance. It tests two assumptions instead of taking them as given: that coastal ecosystems decline as one unit, and that conservation governance follows measured risk. The same method can be applied to other coastal and island settings.

---

## Entry 2

### Status
Complete. Covers the 3 OpenStreetMap datasets used as the baseline for human activity: settlements, tourism nd infrastructure.

---

### Source and Acquisition

I grabbed all 3 datasets from OpenStreetMap. (So I ran specific Overpass Turbo queries filtered exactly to each island's borders, which gave me one raw GeoJSON export per island for each distinct category to create fifteen total files). So I chose OSM because it was practical. It gives me consistent, free data across 5 different national administrative systems: Maldives, India, Seychelles, Fiji, n Spain. (No single government office provides a dataset tht covers all 5 islands in the same format, so I had to use OSM to keep my framework uniform).

### Bug: Sea Features Mislabeled as Settlements

So I found a weird bug while checking my clean settlement files. (My bounding boxes for the Maldives nd Lakshadweep data looked way too massive nd extended way outside the actual island borders). 2 specific rows caused this mess in both files. They were labeled "Arabian Sea" n "Laccadive Sea." (These entries were obviously not real human settlements at all, but random OSM features for large water bodies that got accidentally dragged into my Overpass Turbo place type query because online contributors tag things inconsistently). It happens a lot on OSM.

Caught this mistake by a quick check. Calculated the centroid coordinates for every single settlement, sorted everything by longitude, n checked the extreme values at both ends. (The 2 sea name rows stuck out like a sore thumb immediately because their coordinates were sitting far away from the actual settlement clusters). So, I chose to delete both rows directly from my cleaned .gpkg files. (My Maldives file dropped from 998 to 996 rows, nd my Lakshadweep data went from 38 down to 36 rows). This fixed the bug completely without making me re pull anything from OpenStreetMap.

### Bug: Invalid Geometry in Tourism Data

Hit a crash. (While I was trying to read the Canary Islands tourism dataset, geopandas.read_file() suddenly threw a bad GEOSException error about an invalid number of points in a LinearRing). The file only had 2 points instead of the 4 pairs needed to make a proper loop. (People who edit crowd sourced OpenStreetMap data frequently make these broken, half finished polygon lines by mistake).

I chose to pass on_invalid="ignore" right inside the geopandas.read_file() command so my script drops unreadable geometries instead of dying. Then I ran an explicit check. (I wanted to count if there were any null geometries left after the read, and I found exactly 2 invalid rows in the Canary tourism file). My rows dropped from 10,877 down to 10,875 valid ones. Made this exact setup a standard step for all my later vector cleaning scripts. (Broken polygon defects can show up anywhere when u use open source OSM files, so adding this check keeps my pipeline safe).

### Final Status of This Phase

| Dataset | Islands Covered | Notes |
|---|---|---|
| Settlements | 5 | 2 sea-name rows removed (Maldives, Lakshadweep) |
| Tourism | 5 | 2 invalid geometries removed (Canary Islands) |
| Infrastructure | 5 | – |

All fifteen files confirmed clean, correctly bounded, nd free of invalid geometries by the end of this phase. That's the human activity baseline used through the rest of the project, including the encroachment analysis much later.

---

## Entry 3

### Status
Complete. Covers the 3 ecosystem buffer datasets used for hypothesis testing: mangrove extent, coral reef extent nd protected areas.

---

### 2 Different Source Types

My ecosystem buffer data was not like my settlement data. (While I got all settlement, tourism, nd infrastructure layers uniformly from OSM for all 5 islands, the ecosystem buffer data came from 2 completely different source structures depending on the island, which forced me to write 2 separate cleaning pipelines instead of using one shared script).

Found tht Fiji, Lakshadweep, n Seychelles mangrove nd coral data came straight from WCMC's Global Mangrove Watch nd coral reef atlases. (You can identify these files right away because they use a loud uppercase column convention like LAYER_NAME, METADATA_I, NAME, FAMILY, GENUS, SPECIES, DATA_TYPE, GIS_AREA_K, nd REP_AREA_K). But the data for the Maldives n Canary Islands came from OSM. It used the exact same lowercase place, natural, n tourism schema tht I found in my settlement files. (So I had to make sure every mangrove n coral cleaning script could detect which source format a given island was using to apply the correct column selection logic). Had to create a specific WCMC_KEEP_COLUMNS list for the 1st group nd a separate OSM style list for the 2nd group instead of using one universal set.

### Bug: The Maldives "Coral" File Wasn't Coral Data

Found a serious data quality problem here. (When I 1st opened the coral_maldives.gpkg file, it had 4,230 rows n 79 columns, but looking at the column names made me realize a bunch of fields had absolutely nothing to do with real coral reefs). The columns were filled with random words like cuisine, spa, restaurant, rooms, payment:visa, payment:mastercard, opening_hours, and parking. This file was not a filtered coral dataset at all. (It was basically an unfiltered general OSM export for the whole Maldives region tht someone had jst named like it was coral specific data).

So, I chose to filter it down myself. I used the official OSM reef tagging convention by running natural == "reef" on the table. (This step correctly picked out 2,921 of the 4,230 rows as actual coral reef polygons, meaning the other 1,309 rows were just unrelated tourism, hospitality, and amenity points that got mixed into the same export by mistake). A reef attribute column with a single consistent value like "coral" across the correctly tagged rows proved to me tht my filter isolated the right feature type. (Doing this filtering step before any column cleanup ensured that my downstream analysis was not quietly ruined by thousands of irrelevant tourism records).

### Real Ecological Absences, Not Data Gaps

Got zero results for 2 islands. (When I was pulling specific ecosystem data, these 2 places came back completely empty, but I chose to investigate n found out they were real absences instead of data download failures). So now I double check every zero result before treating it as an error.

My Lakshadweep data showed zero mangrove features. This makes sense. (Mangroves are very rare in this specific archipelago because it is jst a small coral atoll chain tht lacks the muddy intertidal delta conditions tht mangrove trees actually need to grow).

So I also found zero coral reefs for the Canary Islands. (This fits its subtropical, volcanic, cooler water Atlantic setting perfectly because the island sits way outside the warm tropical shallow water temperature range tht corals need). I got independent cross confirmation for this later. Ran a separate Global Mangrove Watch bounding box query for another multi temporal analysis, n it came back totally empty for the Canary Islands even after I deliberately made the search box much wider. (This proved to me that this island's coastal ecology is a different animal from the tropical islands, nd it was not a systematic acquisition problem with my download script).

### Protected Areas: Swapping Out a Weak Source

So I hit an issue with protected areas. (For 4 islands, Maldives, Canary Islands, Seychelles, n Fiji, I originally got the protection dataset from OpenStreetMap using the QuickOSM plugin, but on checking I found an implausibly small number of features like just one protected area for Fiji n 4 for Maldives). This data felt completely wrong. Knew these regions hve plenty of officially gazetted marine n terrestrial protected areas, so it was jst bad coverage.

So, I switched my source. I chose to use the World Database on Protected Areas instead because it is the main global dataset from UNEP WCMC. Filtered it to each island's bounding box nd merged the parts into one file per island.

My feature counts jumped up a lot. (After I fixed my data source, the Maldives count went from 4 to 93, Fiji jumped from 1 to 126 because I combined 2 sub queries to cover its territory tht straddles the antimeridian, Seychelles grew from 4 to 49, n the Canary Islands went from 258 up to 385 features). The old OSM layer was clearly incomplete. I found tht Lakshadweep had zero WDPA registered protected areas. (This matched my earlier zero result from OpenStreetMap perfectly, giving me solid cross source proof tht this is a real fact abt Lakshadweep instead of some random database glitch). Replaced the OSM layer with WDPA for all 4 islands.

### Final Status of This Phase

| Dataset | Islands With Data | Confirmed Real Absences |
|---|---|---|
| Mangroves | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |
| Coral Reefs | Maldives, Fiji, Lakshadweep, Seychelles | Canary Islands |
| Protected Areas (WDPA) | Maldives, Seychelles, Fiji, Canary Islands | Lakshadweep |

This phase set the ecosystem buffer baseline used both for the project's static ecosystem context n, later, as the foundation for the full multi temporal analysis in Entry 5.

---

## Entry 4

### Status
Complete. Covers the remaining baseline layers: elevation nd slope, population density nd historical cyclone tracks.

---

### Terrain: Elevation nd Slope

I got my elevation data from Copernicus DEM.

3 slope files (Canary, Fiji, Lakshadweep) came in EPSG:3857 nd were reprojected to EPSG:4326 with bilinear resampling. Seychelles had no slope file, so I generated it from the Seychelles elevation raster with GDAL's gdaldem slope.

So I cross checked elevation values manually. (Matched my raster data against real geography maps as a sanity check because I did not want to jst blindly trust random numbers on my screen). My Canary Islands file maxed out at around 3,696 meters. (This lines up nicely with Mount Teide, which is Spain's highest peak sitting at roughly 3,715 meters). The Seychelles data hit a top peak of around 904 meters. (This fits its steep granite mountain geography like Morne Seychellois perfectly). On the other hand, the Maldives and Lakshadweep layers stayed strictly in a super low 0 to 20 meters range. (This matches exactly wht you expect for low lying coral atoll nations on any map). This quick matching test gave me high confidence. My height layers were processed correctly and did not get silently corrupted or shifted.

### Population: Checked Against Real Numbers

So I downloaded the 2020 WorldPop density rasters. (So I managed to get good data for 4 out of my 5 targets: Fiji, Seychelles, Maldives, n the Canary Islands, where I clipped the last one directly from Spain's big national population map). But Lakshadweep did not get any population data in this phase. (The only online download option I found meant pulling a massive multi gigabyte raster covering the entire country of India, which was impractical for such a small area). So I left it for later.

So I validated each raster by myself. (I chose to sum up every single pixel value in the files to calculate a total population estimate, then I checked those sums directly against real world figures instead of jst assuming the data was correct because the code ran fine). My verification showed good numbers. The Canary Islands file gave me 2.09 million against the actual 2.2 million count. (Fiji gave me around 896,000 instead of 900,000, Seychelles calculated to 98,000 against the real 100,000, nd the Maldives raster hit 540,000 which is exactly inside its known real range). So I treated this step as highly essential. A file processing cleanly does not mean the data inside is correct.

### Cyclone Tracks: IBTrACS n a Wind Speed Consolidation Problem

I got historical cyclone track data from IBTrACS. (This is NOAA's standard global cyclone dataset that mixes reports from more than a dozen different meteorological offices). I chose to filter down the full global shapefile per island using the exact same bounding box geopandas.read_file(bbox=...) approach tht I already used for my WDPA files.

4 out of my 5 islands returned real storm data. (I found that Fiji had 143 tracks, Lakshadweep had 4, Maldives had 5, and Seychelles had 2 entries in the final count). These numbers matched my expectations. But the Canary Islands file came back with absolutely zero rows. (Checked this specific place twice under 2 separately named filtering attempts in my script, but it is a true result because the Canary Islands sit entirely outside the typical Atlantic tropical cyclone formation n travel corridor). I logged it as a real geographical finding.

So I found another bad data quality issue here. (The wind speed column I wanted to use, called WMO_WIND, was completely blank for most of my records since it only had data for 1 out of 5 storms in the Maldives nd 31 out of 143 for Fiji). But I noticed tht IBTrACS separately logs wind estimates from different local national agencies like USA_WIND, REU_WIND, BOM_WIND, TOK_WIND, CMA_WIND, n HKO_WIND. So, I chose to use pandas' bfill(axis=1) trick across a prioritized list of these agency columns. (This automatically grabs the very 1st available non null wind value for each storm row no matter which country's office tracked it originally). Managed to improve Fiji's useful wind speed data from 31 up to 87 out of 143 rows. My data counts for the other 3 small islands (Maldives, Seychelles, nd Lakshadweep) stayed low, but tht is jst because those places hve a real natural scarcity of storms rather than a bug in my coding consolidation method. (Confirmed this fact by running the exact same multi agency check script against those islands nd found absolutely nothing extra beyond wht my 1st 4 agency check caught).

### Final Status of This Phase

| Dataset | Islands With Full Coverage | Notes |
|---|---|---|
| Elevation | All 5 | Cross checked against known peak elevations |
| Slope | All 5 | 3 islands reprojected; Seychelles generated from elevation |
| Population | 4 of 5 | Lakshadweep deferred; all 4 checked against real world totals |
| Cyclone Tracks | 4 of 5 | Canary Islands confirmed absent; wind speed consolidated across agencies |

This phase closed out the full baseline dataset inventory needed before starting the project's core multi temporal nd cross dataset analyses, covered nxt.

---

## Entry 5

### Status
Complete. Covers the core analysis: ecosystem trends across several dates instead of a single before nd after snapshot, the exposure numbers nd the 1st compound score.

---

### Why Multi Temporal

My old data from Entry 3 only showed a single snapshot in time. (So I realized tht if I really want to test whether mangroves or coral reefs are declining, I absolutely need dataset layers recorded across multiple, well separated years). A single comparison is a bad idea. (It is too easy for a simple before n after check to look fake because of random noise or an unusual reference starting period). A trend finding tht holds true across several independent time blocks on a timeline is simply a lot more convincing to examiners.

### Mangrove Time Series: 3 Points

I used the Global Mangrove Watch archive, which gives pre processed annual mangrove extent snapshots. I chose 3 specific time points for my project: 1996 which is the earliest baseline available, 2010 for the exact midpoint, nd 2020 as the most recent single year data block. (This covers a proper 24-year span with a clear check right in the middle because a single big 24-year jump completely hides whether the loss was gradual or jst happened suddenly in a tiny window).

Noticed one detail in the GMW folder. (The database provides files both as single year snapshots like gmw_v3_2020_vec.zip n as change detection vectors spanning a date range like gmw_v3_f1996_t2020_vec.zip where f means from nd t means to). So I had to make a choice. I chose to independently derive the total area change by my own scripts using the 3 separately verified snapshots. (So I did not want to blindly lean on GMW's own pre computed change detection algorithm, so I downloaded n ran the 3 single year files instead of touching their mixed pre computed change file). This way every step of the area calculation is in my own scripts.

Extracted per island, per year files from each global shapefile with the same bbox approach as the WDPA files. Lakshadweep was skipped, since Entry 3 already showed it has no mangroves.

#### Bug: Feature Count Isn't a Valid Area Proxy

So I ran an early data check. (I used raw polygon feature counts across the 3 time points as a quick way to see changes, n it looked like Fiji had a massive drop because it went from 5,608 features in 1996 down to 4,810 in 2020 which looks like a 14.2% loss). Did not trust this number. I knew that feature counts nd actual mapped areas are completely different things on a map. (For example, one large continuous mangrove forest can show up as a single polygon in one year, but it can easily break into several small adjacent polygons in another year purely because of how the satellite classification algorithm decides to slice that specific imagery). There might be zero real area change. Had to write a better test.

I tested this issue directly. (So I reprojected all 3 years for each of the 3 mangrove islands into an equal area CRS called EPSG:6933 because it is appropriate for real area calculations unlike standard geographic coordinates which badly distort shapes depending on ur latitude). Then I summed the total area in square kilometers instead of using polygon counts. So I got a totally different, more reliable result. (Fiji's mangrove area was basically stable across all 3 points sitting at 485.72 square kilometers in 1996, then 487.97 in 2010, n 488.41 in 2020 which means a small net increase of just 0.6%). My calculations for the Maldives nd Seychelles also showed less than 0.01 square kilometers of real change over the full 24-year span. So the fake decline from feature counts was jst a segmentation artifact between different years' imagery. The actual mangrove extent held essentially stable across all 3 tested islands over nearly a quarter century, which directly changed how I framed my hypothesis testing later in the project log.

### Coral Reef Condition: A Thermal Stress Time Series

Coral degradation shows up as bleaching. (Basically, it is a health nd condition change coming from heavy thermal stress instead of a simple drop in the mapped physical boundary line, so I absolutely needed a totally different data source nd metric than my mangrove tracking setup). I considered using the Allen Coral Atlas 1st, but it turned out to be jst a single snapshot composite built from 2018 to 2020 pictures instead of a real multi year timeline layer. It did not fit a trend analysis.

(Found tht NOAA Coral Reef Watch’s Degree Heating Week product was the perfect match because it gives a continuous daily satellite derived measure of accumulated heat stress from 1985 up to the present day). (DHW above 4 °C-weeks is linked to significant bleaching, nd above 8 °C-weeks to severe bleaching nd mortality). This metric measures the actual biological stress driver directly. It makes complete sense because hard coral reef structures can physically stand there in the ocean for years after a bad heating event even when the living animals inside are already dead.

#### Bug: A Coordinate That Landed on Solid Ground

4 islands worked perfectly right away. (Got valid, non null DHW series numbers for them using representative offshore coordinates that I picked out from my map grid). But my Canary Islands data failed. The 1st coordinate point I chose came back entirely empty because 305 out of 305 values were totally null. (I traced this bug nd found my coordinate was falling exactly on the landmass or way too close to a beach pixel in their 5km resolution grid, which happens easily because the Canary Islands are very small).

Tested 3 alternative offshore coordinates. (I ran a quick single month request for each new candidate point instead of lazily repeating a full 24-year download for every single location). One point sitting just south of Gran Canaria returned a valid value. (I immediately used this working coordinate to re pull the full Canary Islands time series successfully without any errors).

#### DHW Trend Result

I compared 2 different time blocks. (So I took an early reference period from 1996 to 2000 n calculated its average against a recent period spanning 2016 to 2020 to check for changes). 4 islands had rising thermal stress. (My calculations showed the Maldives went up by +0.17°C weeks, Fiji hit +0.10, Lakshadweep got +0.08, and the Seychelles jumped up by a massive +0.68 with a single max reading of 10.47°C weeks which sits right in the dangerous range for severe bleaching n coral death).

But my Canary Islands data looked totally different. (It actually showed a slight decrease of −0.05, making it the only island out of my full group of 5 that was not trending upward on the heat charts). I checked why this happened. (I realized this fits perfectly with its distinct Atlantic climate regime because it operates completely differently compared to the other 4 Indian Ocean n Pacific islands in my folder).

### Physical Exposure: Settlement Level Sea Level Rise Risk

So I calculated the physical exposure numbers nxt. (I chose to sample my elevation raster right at each settlement's center point using rasterio's sample method across all 5 islands so I could find the percentage of villages sitting at or below the one meter sea level rise mark). This gave me a very clear picture. (My data showed a massive geographical spread where 99.1% of Maldives settlements are in high danger, followed by 78.3% for Seychelles, 77.8% for Lakshadweep, 32.0% for Fiji, nd just 12.1% for the Canary Islands). The gap between them is huge. (These results directly show the big difference between flat coral atoll islands nd tall volcanic mountain grounds tht I already saw during my height checks back in Entry 4).

### Compound Vulnerability Score

Mixed the 2 risk signals. (So I took my independently checked physical sea level rise exposure numbers nd my coral thermal stress trend data, scaled each of them onto a basic 0–1 range using min max across the 5 islands, n simply averaged them with equal weighting). I chose to leave the mangrove trend out of this formula entirely. (My long term data analysis did not find any real area loss for mangroves, so there was basically no measurable drop to weight in anyway).

My final list ranking came out. I found that Seychelles scored highest at 0.880, followed by Maldives at 0.651, Lakshadweep at 0.467, Fiji at 0.217, and the Canary Islands sitting at 0.000 as the reference minimum by construction. At this stage this looked like the project's main argument. (See, the Maldives has a much higher physical risk by itself with 99.1% versus Seychelles' 78.3%, but Seychelles wins the highest total danger spot once u actually mix in the bad coral reef dying trends). Looking at water lines alone is a trap. (If I only looked at physical exposure, I would hve picked the completely wrong island as the most dangerous zone).

### Final Status of This Phase

| Analysis | Result |
|---|---|
| Mangrove extent (1996/2010/2020) | Stable across all 3 tested islands; no decline detected |
| Coral thermal stress (1996–2020) | Increasing in 4 of 5 islands; Seychelles most severe |
| Physical SLR exposure | Wide variation, 12.1%–99.1% of settlements at risk |
| Compound Vulnerability Score | Seychelles ranked highest; Canary Islands lowest |

---

## Entry 6

### Status
Complete. Covers the governance test (does protected area coverage match the risk scores), the built up encroachment analysis nd a synthesis of the results at this stage.

---

### Adding a Governance Dimension

Added a phase to connect the results to policy. Instead of treating protected area boundaries as jst some unexamined backdrop maps, I formulated a specific testable hypothesis. (So I think tht official protection marks like WDPA coverage should go up in places where my Compound Vulnerability Score from Entry 5 is high, if the governments are actually listening to data).

### Bug: Comparing Land Area to Marine EEZs

My 1st test failed. (Tried to calculate a simple protected area to land area ratio, but my script gave me a totally nonsense result of 1005.69 for the Seychelles which basically means the protected zone size went over the actual island land size by more than a thousand times). Traced this bug down into the code. (Found tht the massive WDPA dataset accidentally included the entire Seychelles Exclusive Economic Zone because my simple bounding box filter from Entry 3 swept up over a million square kilometers of open ocean along with the real land based parks). Comparing tht gigantic sea number against a tiny island land area denominator was nvr going to give me any real, readable results.

(So I restricted my protected area calculation to a strict 10km coastal buffer around each island's boundary instead of using the full captured WDPA extent because a settlement's actual exposure is tied to nearby coastal protection nd not to some random offshore marine park hundreds of kilometers away). This made much more sense. Implemented this by buffering each island's boundary geometry by 10km after reprojecting to an equal area CRS. (Then I intersected tht fresh buffer zone with each island's WDPA polygons before summing the total area). After tht, Seychelles dropped from 1005.69 down to a clean 11.32. (It is still the highest value of my 5 islands but it is no longer totally absurd, while my Maldives score hit 3.90, Canary Islands got 2.32, Fiji sat at 0.42, n Lakshadweep landed on 0.00 which matches its verified zero coverage from Entry 3).

### Governance Alignment Result

So I ran a Pearson correlation test next. (So I took my Compound Vulnerability Score for each island and checked it against its coastal buffer WDPA ratio using the scipy.stats.pearsonr function in my Python script). The output gave me r=0.727. This means I found a moderately strong positive relationship. (See, my data shows tht Seychelles has the highest vulnerability nd also carries the highest protection ratio, which looks like a good pattern). But my p value came out to 0.164. (This means my test missed the conventional 0.05 statistical threshold completely so it is not 100% solid proof). I logged this straight as suggestive rather than confirmatory. The direction definitely looks like risk responsive governance. But 5 islands jst do not give enough statistical power to be fully confident abt it, which is the exact same small sample size limitation tht ruined a comparably small country sample earlier in my old project work.

#### Bug: A NoData Artifact Hiding Inside My Canary Islands Number

Went back n double checked something tht had been bugging me a little. (My Canary Islands physical exposure number of 12.1% from Entry 5 jst felt off compared to how flat nd low lying its elevation profile looked in my earlier height checks, so I decided to open up the raw per point raster sample results instead of jst trusting the summary percentage). Good thing I did tht. (Dug through the point by point output n found tht 649 out of my full 5,483 raster sample points for the Canary Islands were actually NoData values sitting right at the coastline edge of my raster grid, but my earlier script was silently counting a chunk of those NoData points as if they were real, valid at risk settlement points instead of throwing them out first). Tht is a real bug, not jst noise in the numbers.

Fixed it by properly excluding those 649 NoData points before doing the percentage math. (Once I recalculated using only the properly valid raster samples, the Canary Islands physical exposure number dropped all the way down from 12.1% to a much more realistic 0.3%, which actually fits its flat volcanic coastline way better than tht old inflated figure ever did). Because this feeds directly into my Compound Vulnerability Score formula from earlier in this entry, I had to rerun tht whole calculation too. My corrected scores came out as Seychelles at 0.895, Maldives at 0.651, Lakshadweep at 0.481, nd Fiji at 0.263, with the Canary Islands still sitting at 0.000 as the reference minimum (the ranking order stays exactly the same, Seychelles is still on top, jst the individual numbers shifted a little bit). This also meant redoing my Pearson correlation test right above since it leans on these same vulnerability scores. (My corrected governance alignment result came out as r=0.718 nd p=0.172, which is basically the same moderately strong, not quite statistically significant pattern as before, jst slightly adjusted).

### Settlement Encroachment: Satellite Derived Built Up Area Change

Coded the last analytical part nxt. (Chose to test if new houses n infrastructure expansions are crowding right inside or close to the fragile ecosystem buffer zones over a long time timeline by using the Normalized Difference Built up Index). This is called NDBI for short. (So I built it the exact same way people make standard NDVI but I tuned my code parameters to detect built up urban surfaces instead of green trees nd grass by calculating values directly from Sentinel-2 shortwave infrared and near infrared bands). Applied this index math strictly to the 3 islands where mangroves are actually growing: Maldives, Seychelles, nd Fiji. (My script compared an old 2016 baseline satellite dataset directly against a recent 2024 time period to map out the new construction expansion).

#### Bug: Empty Results, No Error

My 1st data pull failed quietly. (So I used a full calendar year aggregation window called P1Y for each island, which returned an HTTP 200 success code but gave me a totally empty data array like "data": [] nd a "geometryPixelCount": null field for every single request across all 3 islands nd both periods). (So I had to read the raw JSON text directly to catch this bug because I couldn't just blindly trust the green request success status alone).

Made 2 changes to fix it. Switched the aggregation window length from a full year down to 6 months using P6M. (I chose this because of a lesson from my older NO₂ nd NDVI data work where certain Sentinel Hub interval lengths behave inconsistently depending on your specific data type). Then I did one more step. I added an explicit maxCloudCoverage: 30 filter line to my request script. (Persistent empty values across a full year for tropical islands usually mean heavy cloud cover is blocking any usable clear sky satellite observations). Both edits worked perfectly together. All 6 of my requests (meaning 3 islands multiplied by 2 time periods) came back fully populated with numbers.

#### Encroachment Result

Compared the average NDBI values. (Looked closely at the data between my 2 selected time blocks and found tht both Maldives went up by +0.0461 n Seychelles grew by +0.1135 to show a clear increase matching real house nd infrastructure expansion right near the ecosystem buffer zones between 2016 nd 2024). Seychelles showed the largest growth jump. (My data reveals it actually crossed completely from a negative average in 2016 which means vegetation dominated lands straight into a positive value in 2024 showing it is now built up dominated ground). But Fiji showed basically zero shift sitting at −0.0008. (This dead flat trend lines up perfectly with the overall stability tht I already saw earlier when checking its mangrove extent dataset).

### Final Synthesis

Seychelles kept popping up everywhere. (Across every analytical piece I coded, this specific place showed the absolute strongest proof of a compounding, self reinforcing vulnerability pattern because it carried the highest Compound Vulnerability Score driven by the worst coral thermal stress trends). It also has the highest coastal protected area ratio. (Even though I could not statistically confirm this governance response with my small sample size, the policy direction looks correct). It also gave me the biggest house building encroachment signal.

Fiji was the opposite story. (My data shows it stayed completely stable across every single temporal measure over the decades with flat mangrove boundaries, the smallest coral heat stress increase among all working islands, n zero infrastructure encroachment). It serves as a low change reference case against Seychelles' high change profile.

My mangrove decline hypothesis was not supported. (I tested H2 the same way as everything else, nd the data did not support it on any of the 3 islands with mangroves). No real mangrove loss. (My data clearly shows that nature buffer degradation is not uniform across different ecosystem types at all because coral reefs in my 5 island sample are measurably more vulnerable to heat stress than mangroves over this multi decadal timeline).

### Complete Project Data Inventory

| Category | Coverage |
|---|---|
| Settlements, Tourism, Infrastructure | 5 islands each |
| Mangroves (multi temporal, 3 time points) | 3 islands (Lakshadweep and Canary Islands confirmed absent) |
| Coral Reefs (extent) | 4 islands (Canary Islands confirmed absent) |
| Coral Thermal Stress (24-year time series) | 5 islands |
| Protected Areas (WDPA) | 4 islands (Lakshadweep confirmed absent) |
| Elevation, Slope | 5 islands each |
| Population | 4 islands (Lakshadweep deferred) |
| Cyclone Tracks | 4 islands (Canary Islands confirmed absent) |
| Settlement Encroachment (NDBI) | 3 islands (mangrove present islands only) |

Investigated every single zero result. (Whenever I hit an unexpected finding along the way, like Lakshadweep's completely absent mangroves, the Canary Islands' absent corals and cyclones, or my mangrove decline hypothesis not holding up, I chose to dig deep n confirmed them as real geographical facts or traced them back to a specific, fixable data cause). Where a hypothesis didnt hold, I wrote it down as a result.

---

## Entry 7

### Status
Supplementary. Tried satellite based cyclone damage detection as supporting evidence; the Sentinel-2 record limits it to Fiji.

---

### Context n Why It Got Added

My core analysis centers on sea level rise and ecosystem buffer degradation. (Made a deliberate scope call to treat cyclone activity as a background factor rather than a primary pillar because data from an earlier, differently framed version of this island nations project showed meaningful cyclone intensity variation only for Fiji, with the other 4 islands' historical storm records being too weak and low intensity to detect any real damage signal on a satellite map). This earlier version was originally built around cyclone impacts specifically.

So I did not want to throw away tht earlier cyclone related work once my project's framing shifted toward water lines nd coral death. (I chose to keep it as a smaller, clearly scoped supporting addition inside my folders instead of messing up nd re expanding my core analytical structure). 2 Sentinel-2 NDVI before and after comparisons from tht older project phase were still in my data folder. (These cover Fiji's 2 strongest recorded cyclones, Winston in 2016 n Yasa in 2020).

### Trying to Extend This to the Other 4 Islands

I tried an extra test 1st. (Before I finally settled on Fiji as my only island with clear cyclone damage evidence, I tried extending the exact same satellite damage detection approach to the Maldives, Seychelles, n Lakshadweep using each island's single strongest recorded storm from the IBTrACS database tht I already set up in Entry 4). 1st, I had to pin down each island's peak intensity event name nd its exact calendar date. (I needed to do this step because building a proper before nd after satellite imagery window completely depends on knowing the exact day when the storm actually hit the beach).

### Ran Into a Satellite Record Start Date Wall

Sentinel-2, which I use for all NDVI work in this project, launched in 2015, so no imagery exists before tht. Then I checked the historical dates for my 3 candidate islands' strongest recorded cyclones against this satellite launch cutoff line. (My data matching showed tht all 3 storms happened way before Sentinel-2 was even built: the Maldives' biggest cyclone hit back in 2006, Seychelles faced its worst one in 1996, nd Lakshadweep had its massive peak storm in 1997). No valid "before" satellite imagery could evr exist for any of these islands. This data scarcity completely killed tht line of analysis.

### How This Got Reported

I didnt swap in a later, weaker cyclone to get a result. It is a structural limit of satellite based verification. (Any remote sensing method u try is strictly bounded by when its satellite hardware platform actually started operating in space, n events before tht date cannot be verified by that method). So I wrote it down as a scope limit for this one supplementary analysis. (It does not touch my project's core sea level rise or ecosystem degradation findings because those calculations do not depend on Sentinel-2's coverage window the same way at all). My primary results stay fully safe.

### Final Cyclone Damage Proxy Status

| Island | Cyclone Damage Evidence | Reason |
|---|---|---|
| Fiji | Available (Winston 2016, Yasa 2020) | Both events post date Sentinel-2 availability |
| Maldives | Not available | Strongest recorded cyclone (2006) predates Sentinel-2 |
| Seychelles | Not available | Strongest recorded cyclone (1996) predates Sentinel-2 |
| Lakshadweep | Not available | Strongest recorded cyclone (1997) predates Sentinel-2 |
| Canary Islands | Not applicable | No cyclone events recorded in this region (Entry 4) |

Analyzed the 2 Fiji results nxt. (My numbers showed a clear NDVI decline of −0.0246 after Cyclone Winston which hit at 150 knots as a Category 5 equivalent storm). For Yasa I originally reported zero clear decline, +0.0049, but on a later check I realised tht number came from pairing the earliest pre cyclone reading I had (September, more than 3 months before Yasa even made landfall) with the earliest post reading, instead of the pre/post windows actually closest to Yasa's 17 Dec date. Redone with the closest pre window (late Oct–Nov) nd closest post window (Jan), Yasa actually shows a decline of about −0.0275, bigger than Winston's, not smaller. So the "satellite detectable vegetation damage only shows up at extreme storm intensity" line doesn't hold up nd I'm dropping it. (Also doesn't match the broader ecosystem stability I saw in Fiji's mangrove dataset the way I originally thought it did: tht mangrove finding still stands on its own, it just isn't corroborated by this cyclone comparison anymore). Keeping both numbers here as supplementary Fiji only evidence same as before, still not extrapolating to the other 4 islands, just correcting wht the comparison itself actually shows.

---

## Entry 8

### Status
Went back through my data quality checklist once more. Found something I missed the 1st time. Turns out the Canary Islands zero elevation fix from Entry 6 wasnt the full story after all. Fiji had the exact same problem sitting there this whole time.

### Fiji Never Got the Same Check Canary Got

So back in Entry 6 I caught tht Canary's zero elevation DEM readings were a NoData artifact nd not real terrain, nd fixed it (12.1% → 0.3%). (But I never actually asked if any other island had this same problem hiding in it). Went back nd counted it properly this time. 649 of Canary's 5,483 points read exactly 0.0m, tht's 11.8%, the number I already caught before. Fiji has 414 of 1,323 points reading exactly 0.0m too. Tht's 31.3%. An even bigger spike than Canary's own number. Same kind of volcanic, mountainous terrain where real settlements sitting at sea level jst dont make geological sense. I hadnt touched Fiji's number at all before this. So its reported exposure of 32.0% was carrying this same artifact the whole time nd I never noticed.

Went nd checked wht kind of settlement points these actually were before assuming anything. (Islet, village, hamlet, archipelago, a real mix of place types, not jst big place label centroids sitting over open water). So it's not an easy "the label point fell in the ocean" explanation. A real DEM shouldnt return a literal, bit exact 0.0 for 31% of points on a mountainous island. A real elevation distribution near sea level would show a gradient, 0.3m, 0.8m, 1.4m, nd so on, not a spike sitting exactly on zero. Also found tht map1_slr_fiji.py, the script tht makes the standalone Fiji map figure, was ALREADY excluding Fiji's zero readings on its own. Completely independent of the main pipeline, which never did this. So 2 parts of my own project were quietly disagreeing with each other this whole time nd I never noticed either.

Fixed it by adding fiji to the same nodata exclusion set already used for canary. Did this across precompute_elevations.py, dashboard/precompute_elevations.py, slr_exposure_analysis.py, nd export_settlement_elevations_full.py. Corrected Fiji's settlement based exposure from 32.0% down to 1.0% (909 valid points left after dropping the 414 NoData ones, only 9 truly at risk). This is a much bigger correction than Canary's, proportionally speaking. But Fiji was already my 2nd lowest exposure island before this fix, so it doesnt flip anything in the ranking order. Jst makes the "volcanic islands have way less exposure than atolls" story even more lopsided than wht I'd already reported.

One open point. Maldives (99.0% of points exactly 0.0m) nd Lakshadweep (77.8%) show this SAME zero heavy pattern. I did NOT apply the same fix to them. (The difference is tht Maldives nd Lakshadweep are real low lying coral atolls). Near sea level elevation across most of the land is the expected geology there, not some anomaly the way it is on a volcanic island. So the same statistical red flag doesnt carry the same weight for those 2. But I also cant say for sure none of their zero readings are DEM artifacts either. Havent done a pixel level QGIS check on either of them the way I did for Canary. Leaving this open for now.

### This Changed the Compound Score nd Governance Test Too

Since Fiji's exposure number feeds straight into the Compound Vulnerability Score, had to rerun tht too. Fiji's score dropped from 0.263 to 0.106. Ranking order didnt change though (Seychelles still highest, Canary still the reference minimum at 0.000). Fiji jst moved further down within where it already was. Reran the weighting sensitivity sweep too nd confirmed the Seychelles vs Maldives crossover point (abt 76.8% physical exposure weighting) is completely unaffected. Fiji was never the min or max input either the physical exposure or coral normalization got scaled against anyway.

### Fixed the Lakshadweep Zero Hiding Inside My Governance Correlation

While I was back in tht part of the pipeline, caught another thing tht'd been bugging me. Lakshadweep's WDPA coastal ratio is reported as 0.00 because I flat out dont hve a protected area dataset for it. (I already documented tht correctly as missing data back in Entry 3). But I was still feeding tht placeholder zero into the Pearson correlation like it was a real 5th data point. Tht's not "reporting a caveat," tht's letting a made up number quietly bias an already tiny 5 point correlation. Fixed governance_correlation_test.py to drop Lakshadweep from the correlation itself (n=4) nd report its vulnerability score separately, unpaired against any WDPA number. New result: r=0.862, p=0.138 (up from r=0.718, p=0.172 with the old n=5 version tht still counted Lakshadweep's fake zero). Still not statistically significant at this sample size. Still the same "suggestive, not confirmed" story. Jst computed the right way this time.

### Switched the Coral Trend Test to the Seasonal Mann-Kendall Version

Also realized my Mann-Kendall trend test on the 24-year DHW series was using the plain, original version, run straight on raw monthly values. DHW is seasonal by nature though. near zero most months, then spiking during the warm season. So the plain test's independence assumption jst doesnt hold for data shaped like tht. Switched coral_trend_test.py over to pymannkendall's seasonal_test(period=12), which compares same calendar month values across years instead. New p values came out as: Maldives 0.0046 (was 0.011), Seychelles 0.0069 (was 0.025), Fiji 0.2437 (was 0.184), Lakshadweep 0.3725 (was 0.386), Canary 0.6196 (was 0.641). Nothing flips. Maldives nd Seychelles are still the only 2 significant, everything else still isnt. The seasonal test is the right one for this data, nd the result didnt change.

### Other Fixes

- The NDBI "settlement encroachment" section (paper §3.8/4.7, dashboard) was worded like it measured change right near mangrove/reef buffer zones. It doesnt. It's jst a single mean NDBI value over a broad bounding box around each island's main settled area. Reworded it throughout to say wht it actually measures instead of wht it sounds like it measures. The numbers themselves (Fiji −0.0008, Maldives +0.0461, Seychelles +0.1135) didnt change. Jst the framing around them.
- Also went through nd fixed "5 island nations" → "5 islands" everywhere in this log (including my own title above). Lakshadweep is a Union Territory of India nd the Canary Islands are an autonomous community of Spain. Neither one is a nation. The paper, README, nd executive summary already said "5 islands" correctly. This log was the only place still calling them nations.
- Also fixed population_weighted_exposure.py to mask against each island's real boundary polygon instead of jst a rectangular bounding box. A bbox can pull in open water pixels for an irregular archipelago (Fiji, Seychelles) tht a real island boundary wouldnt. Havent rerun this one against the actual population/elevation rasters yet though (not something I can regenerate without redownloading the source data). So the population weighted percentages in the paper are still the old bbox only version for now. Flagged tht clearly in the Limitations section instead of changing numbers I havent actually recomputed.

### Where This Leaves Things

Central finding is completely unchanged. Seychelles still comes out as the highest compound risk island despite Maldives having higher raw physical exposure, nd tht's still robust across the full weighting sweep. Wht changed is Fiji's specific exposure nd compound score numbers (more accurate now, not less favorable to anything I was trying to protect), the governance correlation is now computed the right way instead of quietly including a placeholder zero, nd the coral significance test is running the statistically correct version for seasonal data. None of this came from rerunning any acquisition scripts against new data. It all came from actually rereading my own code against wht it claimed to do, same way the Winston/Yasa correction in Entry 7 did.

## Entry 9

### Status
Finally got my hands on the real population nd elevation rasters for all 5 islands. So I reran population_weighted_exposure.py's v5 boundary polygon version properly for the 1st time. The numbers tht came out were wrong in a totally new way this time. Took a full afternoon of step by step checking to figure out why. Writing it all down here since this is exactly wht Entry 8 left as pending.

---

### 1st Run Looked Very Wrong

So I ran the script nd got numbers way too low compared to real world population figures I already know. Maldives came out at only 6.5% captured. Lakshadweep at 7.3%. Real Maldives population is around 520,000 to 540,000 people, so tht 6.5% is nowhere close to right. Knew right away this was a new bug, not a real correction. Did NOT want to jst push these numbers into the paper without digging further.

### Ruled Out the Easy Explanations 1st

Checked the boring stuff 1st because tht's usually where the actual bug hides. CRS on the population raster nd the boundary files matched (EPSG:4326 both sides), so it wasnt a reprojection mixup. Then checked whether geometry_mask()'s default behaviour (only counts a pixel if its exact center point falls inside the polygon) was dropping population off narrow atoll islands thinner than one pixel. Added all_touched=True so it counts any pixel the polygon touches at all instead of jst the center. Helped a tiny bit (Maldives went from 6.5% to 6.8%, Lakshadweep from 7.3% to 6.3%, actually got slightly worse for Lakshadweep). But nowhere close to fixing the real problem.

Then checked if the boundary files were jst missing the big population centers entirely. Tested Male, Hulhumale, nd Kavaratti (the 3 biggest population centers across these islands) directly against the polygon geometries using a simple point in polygon check. All 3 came back True. Sitting right inside a polygon with basically zero distance to the boundary. So the boundary files do contain these specific islands. Tht theory was wrong too.

### Bug: Trying to Find Exactly Where the Population Was Disappearing

Ran a clean diagnostic split into 3 separate numbers. The raw total population in the whole raster (540,542 for Maldives, matches real world figures fine). The bbox only total with no polygon mask at all (also 540,542, exact same number, so the bbox window by itself isnt losing anything). Nd the bbox+polygon mask total (206,037). So the loss was happening 100% at the polygon mask step nd nowhere else in the pipeline. Only 16,516 out of 12,625,431 pixels in the whole window were even getting marked as land by the mask. Tht's 0.13%. Way too small for an island tht's supposed to have around 298 sq km of real land.

### Tested Whether the Boundary Polygons Were Jst Slightly Off Position

Next thought, maybe the polygons are basically right but shifted a little, so buffering them outward a small amount should recover most of the missing population fast. Tried buffering by 200m, 500m, 1000m, 2000m, nd 5000m nd watched how much population got captured at each step. If this was a small positioning bug I expected capture to jump up fast at a small buffer then flatten out. Instead it climbed slowly nd steadily all the way out to 5km (Maldives went 38% → 40% → 42% → 50% → 68% → 93%), never jumping anywhere. Tht kind of slow steady climb doesnt look like a simple offset bug. Looks more like the polygons are jst plain too small or missing pieces, nd buffering keeps bumping into more real (but unmapped) island area the further out u go.

### Checked If the Population Raster Itself Was Coarse nd Blurry

Had one more theory before blaming the boundary files completely. Wht if the population raster itself was originally coarser (like the common 1km WorldPop resolution) nd got resampled up to this 100m grid without proper handling. So the numbers technically sit on a 100m grid but really represent blurry ~1km blocks tht spill onto water. Zoomed into the actual pixel values right around Male nd Kavaratti to check this. Turned out to be completely wrong. The values change smoothly nd realistically from pixel to pixel (110, 376, 498, 707, 689...), with zero pixels matching their neighbour 10 pixels away. This is real, fine grain data, not blurred blocks. So the population raster itself is fine nd this theory is dead too.

### Root Cause: The Boundary Polygon Files Are Just Incomplete

Finally jst measured the actual land area covered by the boundary polygon files nd compared it against real world island area figures. Tht's wht settled it. Maldives' boundary file only adds up to abt 118 sq km of total polygon area. Real Maldives land area is close to 298 sq km. So more than half of Maldives' real islands are jst not in this file at all.

Lakshadweep was a more confusing case at 1st. Its polygon file's total area (34.14 sq km) is actually close to the real number (abt 32 sq km), so I expected it to capture population fine. But it still only captured 13% of the real population even with all_touched=True on. Tht tells me the individual islands tht ARE in the file are drawn smaller or older than their real current built up extent (probably an old or generalised coastline, not matching wht's actually built nd populated today), rather than whole islands being missing the way Maldives is missing them.

Either way, both islands come back to the same root cause. The boundary shape files I have are jst not a reliable, complete map of where people actually live. The masking code is doing exactly wht it's supposed to do with wht it's given. It's the input data tht isnt good enough yet.

### Decision: Not Swapping v4 for v5 Numbers Yet

Pushing the current v5 output into the paper would replace a limitation I'd already disclosed (v4's bbox numbers, which slightly over count because a box can include some open water) with a WORSE nd undisclosed problem (v5 badly under counting real people, by around 60% for Maldives). Tht's a step backward, not a fix, even though the code itself is working correctly now.

So I'm keeping the v4 (bbox) numbers in the paper exactly as they are. Nothing in the actual reported table changed. Wht I did change is the wording in 3 places (population_weighted_exposure.py's own top note, the paper's Limitations section, nd the executive summary checklist), so all 3 now explain the real reason clearly. The boundary polygon files are incomplete, tht's been checked nd confirmed, nd fixing it properly needs a better set of island boundary shapes, not another round of code changes. This closes out wht Entry 8 left as an open item. Jst not with the ending I was hoping for. The plain answer this time is "found the real reason, still cant use it yet."

## Entry 10

### The Zero Reading Flag From Entry 8 Turned Out to Matter After All

Entry 8 flagged Maldives (99.0% of points reading exactly 0.0m) nd Lakshadweep (77.8%) as showing the same zero heavy pattern as Canary/Fiji, but left it as an open item since I hadnt done a pixel level check on either one. Finally went nd did tht check properly this time. Opened `data/terrain/maldives_elevation.tif` nd `lakshadweep_elevation.tif` in QGIS nd looked at the actual pixel grid, not jst the settlement sample points. Nd it's not jst 99% of settlement points reading zero, it's abt 99.99% of the ENTIRE raster reading exactly 0.0. Wall to wall. No gradient anywhere. Tht's not "low lying atoll terrain," tht's a coverage gap. The file never actually downloaded real elevation data for either island in the 1st place.

Redownloaded the underlying Copernicus DEM GLO-30 tiles directly from ESA's public archive (18 tiles for Maldives, 8 for Lakshadweep) nd rebuilt each island's raster from the complete tile set (`*_elevation_v2.tif`). 2 Maldives tiles nd 3 Lakshadweep tiles came back 404. A real gap in wht's publicly available, not something on my end. So even the corrected files still hve a residual coverage gap: 177 of 996 Maldives settlements (17.8%) nd 8 of 36 Lakshadweep settlements (22.2%) still sit in unretrievable tiles.

Since these 2 ARE real low lying coral atolls, I couldnt jst reuse the blanket "zero = bad reading" rule I used for Canary/Fiji. A real settlement here can legitimately sit at or near 0m, so dropping every exact zero would delete real at risk points right along with the artifacts. Instead built a 5x5 pixel neighborhood check. A 0.0 reading only gets treated as a void if its whole surrounding window is ALSO flat 0.0 (a signature no real terrain produces). Otherwise it stays as an actual reading. As a sanity check, looked up Malé's published average elevation (abt 2.4m, above the 1m threshold). Matches wht the corrected data now shows, not the original.

Recomputed against the remaining 819 Maldives nd 28 Lakshadweep settlements. Physical exposure moves from 99.1% nd 77.8% down to 14.5% nd 7.1%. This changes the paper's central result in a way Entry 8's Fiji fix nd Entry 9's population mask investigation never touched. **Seychelles, not Maldives, now has the highest settlement based physical exposure in the sample**, not jst the highest compound score. The "physical exposure alone would've picked the wrong island" framing I wrote back when I 1st got these numbers (Entry 5) doesnt hold anymore. Exposure alone now points to the same island the compound score always did.

### Same Fix Applied to the Population Weighted Side, nd How Entry 9's Decision Got Undone by Accident

Since population_weighted_exposure.py samples the exact same elevation.tif files, it needed the identical fix. Switched Maldives/Lakshadweep over to `_elevation_v2.tif` nd added a raster level version of the same 5x5 void check (population sitting on a detected gap patch excluded from both numerator nd denominator, same as how Fiji's Lau Islands population is already handled).

1st run after this fix gave a number tht immediately looked wrong again. Lakshadweep's total population came out to only 8,893, against a real population near 64,000. Recognized the smell of this right away from Entry 9 nd went looking for wht I already knew about, the v5 boundary polygon incompleteness. Turned out Entry 9's decision to "keep v4, not v5" was only ever written down in comments nd the paper's wording. Never actually added code tht enforced it. `population_weighted_exposure()` was calling `load_boundary_geoms()` unconditionally whenever the boundary file loaded without throwing an outright exception, which it does every single time, despite the polygons themselves being known incomplete. So every run since Entry 9, including this one, was silently using the broken v5 masking instead of the v4 bbox method the paper actually reports. Entry 9 diagnosed the disease correctly. The prescription jst never made it into the actual script.

Fixed it properly this time with an explicit `APPLY_BOUNDARY_MASK = False` flag instead of a decision tht only lives in a comment. Reran: Seychelles, Fiji, nd Canary Islands (none of which this bug touched) came back identical to the numbers already in the paper (17.6%, 2.1%, 1.6%). Good sign the fix didnt disturb anything tht wasnt already broken. Maldives moved from an artifact inflated 64.5% to 16.9%. Lakshadweep from an artifact inflated 87.5% to 2.2%.

### Where This Actually Leaves the Central Finding

With both fixes in, all 3 independent measures (settlement based exposure, population weighted exposure, nd the compound vulnerability score) now agree Seychelles is the highest risk island. Tht's a real change from how I'd been framing this project. I used to argue "physical exposure alone would mislead u, the compound score catches wht exposure misses." Tht argument doesnt work anymore since exposure isnt misleading here either. The accurate version of the finding now is convergence, not correction. Every independent way of measuring risk lands on the same island. Went through nd reframed the paper, executive summary, README, nd every dashboard page tht referenced the old numbers to say this properly instead of leaving the disproven "exposure would mislead u" argument sitting next to numbers tht no longer support it.

Recomputed the downstream stuff tht depends on the compound score too. The governance correlation (H3) came out at r=0.965, p=0.035 (up from r=0.862, p=0.138), which crosses into conventional statistical significance for the 1st time. Still only n=4 though, so I'm not letting myself read "significant" as "settled." A single data point could still move both numbers a lot at this sample size, nd said so directly everywhere this result gets reported. The weighting sensitivity sweep also changed. The ~76.8% Maldives overtakes Seychelles crossover point from Entry 8 is gone entirely. Seychelles now leads across the full 0–100% range, no crossover anywhere, which is a cleaner robustness result than before.

Fixed every place carrying the old numbers tht I could find: `slr_exposure_analysis.py`, `population_weighted_exposure.py`, `compound_vulnerability_score.py`, `governance_correlation_test.py`, `research_paper_figures.py`, `precompute_elevations.py`, `export_settlement_elevations_full.py`, `build_interactive_plots.py`, the paper, the executive summary, the README, nd every dashboard page (`app.py` nd the numbered pages under `dashboard/pages/`) tht had the old Maldives/Seychelles ranking baked into its prose or chart data. None of this came from new data collection. Same as Entry 8, it all came from going back over my own code nd checking it actually did wht I assumed it did. This time starting from a QGIS pixel check I should've done back in Entry 8 instead of leaving it as an open item.

## Entry 11

### Softened the Governance Significance Wording

Asked myself the harder question after tht. Not "is the repo synced" but "is this actually good enough for a real journal." The n=4 governance correlation is the weak spot a reviewer would flag fastest. r=0.965, p=0.035 is technically under 0.05, but calling it "reaches statistical significance" the way I had it worded sounds more confident than 4 data points can really back up. Went thru the paper, executive summary, nd README nd changed every instance of tht phrasing to "crosses the conventional 0.05 threshold" instead. Didnt touch a single number, jst the framing around it, so a reader doesnt walk away thinking this is settled when it isnt.

### Spatial Averaging the Coral DHW Series Instead of 1 Pixel

The coral thermal stress series was always sampled from a single representative coordinate per island, which I'd already disclosed as a limitation but never actually tested against a spatial average. Built a small box (±0.15°) around the same coordinate nd pulled the average across every valid pixel in tht box instead of jst 1 pixel, then reran the seasonal Mann-Kendall trend test on the new series.

Nd the answer held up. Maldives p=0.0011 (was 0.0046), Seychelles p=0.0194 (was 0.0069), both still significant. Fiji, Lakshadweep, nd Canary Islands all still come back not significant, same as before. Canary's actual mean value shifted a lot (0.714 down to 0.478, since the box around it only had 46% valid ocean pixels), but the trend conclusion didnt move at all. So this is a real, tested robustness check now instead of jst an acknowledged gap sitting in the limitations section.

### The Boundary Polygon Problem From Entry 9, Finally Actually Fixed

Entry 9 diagnosed this nd gave up on it. The boundary files were jst incomplete, nd fixing it properly needed better island shapes, not more code. Went back nd actually tried to get better shapes this time.

1st attempt only kept coastline ways tht were already closed loops on their own. Worked great for Maldives (304 sq km, real figure is abt 298), but came back WORSE than the old broken file for Seychelles, Fiji, Canary, nd Lakshadweep, all of them smaller than before. Turns out most real coastlines arent 1 closed way, theyre several segments joined end to end, nd only tiny simple atoll islets happen to be 1 closed way each.

2nd attempt tried also pulling in multipolygon relations, thinking bigger islands might be tagged tht way instead. Came back with 0 results every single time. Not tht kind of data here.

Realized the actual fix nd redid it properly. Fed every coastline way, open or closed, into shapely's polygonize() function, which stitches together anything sharing an endpoint into whatever closed loops it can find. Tht fixed Maldives nd Seychelles right away, both landed close to real figures. Fiji stayed broken tho, because I'd split it into 8 smaller download tiles to avoid server timeouts, nd Fiji's 2 biggest islands are bigger than any single tile, so their coastline ring got cut in half across 2 separate downloads nd never closed. Fixed tht by combining ways from every tile 1st, then running polygonize() once across the whole combined set instead of tile by tile. Canary nd Lakshadweep also needed a small padding buffer added around each search box so a ring jst barely touching the edge didnt get cut off.

Even after all tht, Fiji stayed stuck at abt 13,000 sq km against a real figure near 18,274. Reran it with longer delays between requests thinking it was a rate limit issue, nd got the EXACT same number again, down to the decimal. Tht told me it wasnt a network problem, it was a real gap in the raw coastline data itself, small spots where 2 mapped segments jst dont technically touch. Switched to OSM's official pre built "land polygons" dataset for Fiji specifically, which already has this exact kind of gap cleaned up before its published. Tht got Fiji to 18,820 sq km, finally close to the real number.

Checked every island's final number against an actual cited source afterward instead of jst eyeballing it. Maldives 317.57 vs 300.00 (World Bank), Seychelles 449.55 vs 460.00 (World Bank), Fiji 18,820.57 vs 18,272 (Wikipedia geography page), Canary Islands 7,432.61 vs 7,447 (Wikipedia), Lakshadweep 30.84 vs 32 (the official Lakshadweep government site). All 5 within abt 6% of a real, citable number. Entry 9's "not fixed yet, needs better shapes" is finally closed out for real this time.

### Rerunning Population Weighted Exposure With the New Shapes

Swapped population_weighted_exposure.py over to point at the new boundary files nd flipped APPLY_BOUNDARY_MASK back to True (Entry 9 hd this forced off, for a very good reason back then). Running it now to see the actual new numbers. If it worked, Lakshadweep's total population shouldnt come out anywhere near the ~8,893 it did last time when the mask was silently broken, it should land somewhere close to the real ~64,000. Waiting on tht result before touching anything in the actual paper.

## Entry 12

### The Result Came Back Different

Ran the v2 population weighted script (the 1 pointed at the new, actually validated boundary shapes) nd waited. Lakshadweep 1st, since tht was the number I was most worried abt. It came back close to the real population, not tht broken ~8,893 anymore. So the mask itself is working now, tht part I was confident abt.

Then I looked at the full table. Seychelles nd Maldives, on population weighted exposure specifically, had flipped. Maldives came out at abt 14.9%, Seychelles at abt 14.2%. Jst barely, but Maldives was ahead. Every single version of this paper, since the very start, has said Seychelles is the highest exposure island on every measure. Nd now 1 of those measures didnt agree anymore.

1st reaction was jst "did I break something." So I didnt jst update the paper. Had to choose between updating the paper straight away or verifying 1st. Picked verify 1st. This is exactly the kind of thing where jst trusting a new number bc it came out of a "fixed" script would be the wrong move.

### Checking It Myself Before Touching a Single Word of the Paper

Went back to raw basics. Pulled the actual population raster nd the new boundary file for jst Seychelles nd Maldives, wrote a tiny separate script tht redid the exact same masking logic by hand (geometry_mask, all_touched=True, same as the real script), nd summed up the population by hand.

Seychelles matched exactly. 94,175 people inside the mask, same number the real script reported, down to the digit. Maldives came out close too, abt 498,819, matching within a small margin. So the population side of this isnt some fluke or rounding bug, its reproducible from scratch.

Cldnt fully check the elevation/at risk half the same way tho, bc those raster files (nearly 1GB nd 1.5GB) were too big to pull across for this kind of quick check. So tht part wasnt checked by hand.

But the mechanism made sense too, not jst the numbers. The whole point of fixing the boundary mask was to stop counting open water next to an island as if it were populated land. Maldives is a spread out archipelago with a lot of water between its islands inside the old bounding box. So a tighter, more accurate boundary would naturally pull the Maldives number down less than expected, or in this case just enough for it to land ahead of Seychelles once Seychelles' own number also came down for the same reason. Not a bug. Jst the fix doing exactly wht it was supposed to do.

### Updating the Write-Ups

Once the verification above was done, I updated the write-ups.

So updated the paper, the executive summary, nd the README. Not jst swapping numbers in a table either. Had to go thru every sentence tht said "Seychelles is highest on every measure" or "all measures agree" nd actually rewrite the claim to be accurate. Settlement based exposure nd the compound score still say Seychelles, tht part didnt change. Population weighted exposure specifically now says Maldives, narrowly, like a near tie (abt 0.7 percentage points apart) rather than some clean win. Wrote down the old number, the new number nd why, same as every other correction.

Table ended up like this in the end: Seychelles 14.2%, Maldives 14.9%, Lakshadweep 2.1%, Fiji 1.6%, Canary Islands 1.4%. All 5 numbers moved down from wht the paper hd before, which makes sense since the old bounding box version was always going to be counting some extra water as land.

### Dashboard Too

Realized halfway thru tht the Streamlit dashboard hd the exact same old numbers baked into it in a bunch of spots, the homepage, the physical exposure page, the compound vulnerability page. Even 1 of the actual chart images (fig3, settlement vs population weighted) was generated from a script tht still hd the old hardcoded 17.6/16.9/etc values in it. So fixed the dict in tht script too nd regenerated the chart image itself, not jst the text around it.

### Checking for Stale Code After the Change

Went thru the whole project again, this time specifically looking for anything still out of sync now tht the population weighted numbers hd changed. Found 1 real problem this time, not jst a wording thing. The actual population_weighted_exposure.py sitting at the root of the repo, the real 1, not the local_fix_scripts copy, still hd APPLY_BOUNDARY_MASK set to False nd was still pointing at the old boundary files. So if anyone actually ran the canonical script in this repo right now, theyd get the old numbers, not wht the paper says. Exactly the kind of stale code vs paper mismatch I was checking for in Entry 11. Fixed it myself, flipped the flag, updated all 5 paths to the new boundary files, nd rewrote the docstring to explain the full history instead of jst deleting it.

Found 2 more real gaps while scanning. 1st, the coral DHW spatial averaging robustness check I'd already done earlier was never written into the paper. The paper still said "this is future work" in 3 different places, which was jst flat out wrong, I hd already done it nd it hd already held up. 2nd, the land area numbers I used to validate the boundary shapes, World Bank nd Wikipedia nd the Lakshadweep gov site, were named in the text but never actually added as real references in the References list.

### Closing Both Gaps

For the coral 1, went nd reran the actual numbers myself 1 more time to be sure before writing anything down, since I didnt want to just copy from memory nd get a digit wrong. Confirmed Maldives p=0.0011, Seychelles p=0.0194, both still significant under the spatial average, nd Fiji/Lakshadweep/Canary all still not significant (p=0.517, 0.810, nd 0.382). Every 1 of them matched the original single point conclusion exactly. Rewrote the 3 spots in the paper nd 2 spots in the executive summary tht said "future work" to instead say wht actually happened nd wht the result was.

For the references, swapped out the informal "Wikipedia" mentions for real sources. Fiji nd Canary Islands land area now cite the World Bank nd Instituto Canario de Estadística instead, since Wikipedia isnt a citable source for a paper. Added all 5 as proper entries in the References section, nd updated the numbers in the text itself to match the real, slightly more precise figures from those sources (298 for Maldives instead of 300, 18,270 for Fiji instead of 18,272, tht kind of small correction).

## Entry 13

### Status
Went back through the whole project (10 October 2026), followed by code and documentation fixes that did not require rerunning the analysis. The analysis was then rerun with the corrected code (Entry 14).

### What I found
- **Seychelles exposure was a NoData artifact.** 188 of the 244 Seychelles settlements read −32767 m, the elevation raster's NoData value, and were counted as "at or below 1 m". The Seychelles raster is 99.97% NoData (its own statistics file reports 0.034% valid pixels). On the 56 settlements with a real reading, exposure is 3 of 56 (5.4%). This is also why Seychelles showed the same 78.3% at the 0.5, 1.0 and 1.5 m thresholds.
- **Lakshadweep's 2 at-risk settlements were outside the DEM.** North Islet and Sand Cay (about 12.35°N) lie north of the re-downloaded DEM, read 0.0, and passed the 5×5 void test. From the available tiles Lakshadweep exposure is 0 of 26.
- **The "404 tile" explanation was wrong.** Rebuilding the Maldives DEM from the raw tiles reproduced the 177 excluded / 819 kept / 14.5% result exactly, but none of the 177 excluded points lie in a missing tile. Copernicus only publishes tiles that contain land; the excluded points are settlement nodes on 0 m water pixels. 96 of the 119 Maldives at-risk points are also exact 0.0 water pixels.
- **Downstream effects.** With Seychelles corrected, the compound score of Seychelles (0.68) and Maldives (0.65) are nearly tied and the top island changes at about 52% exposure weight; the governance correlation falls from r = 0.965 (p = 0.035) to r = 0.75 (p = 0.25). Even as reported, removing Seychelles alone gives r = 0.51.
- **NDBI encroachment.** The bounding boxes are 99.7% (Maldives) and 85% (Seychelles) ocean, and the Statistical API values had no cloud or water mask. The project's own cloud-masked NDBI rasters for the same boxes give a land-only change of −0.0003 for Seychelles, not +0.1135.
- **WDPA coverage.** The coastal ratio used the old, incomplete boundary files and summed overlapping WDPA polygons (overlaps inflate Seychelles by about 57% and Canary by about 82%).
- **Fiji settlement coordinates.** Six Fiji settlements (Lau Group, Vanua Levu Group, Taveuni, Vanua Levu, Korolevu Island, Rabi) were stored at about 0° longitude because their point was averaged across the 180° meridian.
- **Verified as correct:** all seasonal Mann-Kendall p-values (single cell and box average), the DHW period changes, and the mangrove areas reproduced exactly.

### Code changes
- New `scripts/common/dem_sampling.py`: one DEM rule for all five islands. Each settlement is classified as valid, snapped_to_land (point on a 0 m water pixel; elevation = median of land pixels within about 60 m), water_no_land_nearby, nodata or out_of_extent. NoData and out-of-extent points can no longer be counted as at risk. It also corrects the six Fiji longitudes.
- `slr_exposure_analysis.py` rewritten on that module; reports coverage and status counts per island, the main rule and a strict rule (water-pixel points excluded), and writes per-settlement CSVs. `export_settlement_elevations_full.py` and `scripts/processing/precompute_elevations.py` now call the single implementation; `dashboard/precompute_elevations.py` uses the same module.
- `population_weighted_exposure.py`: NoData, NaN and 0 m water pixels are removed before resampling (average resampling of land pixels only); population with no usable elevation is excluded and reported; large windows are processed in 1° chunks; results go to `data/population_weighted_exposure.csv`.
- New `scripts/acquisition/download_copernicus_dem_tiles.py`: downloads GLO-30 tiles for any island over the full settlement extent and builds a VRT mosaic (Seychelles is too large for an in-memory merge).
- `wdpa_coastal_buffer.py`: validated v2 boundaries, dissolved WDPA polygons, a new share-of-coastal-zone metric, a strict IUCN I–IV variant, and Lakshadweep reported as missing rather than zero. `filter_wdpa_islands.py` now also reads the WDPA points file.
- `compound_vulnerability_score.py` and `governance_correlation_test.py` read their inputs from CSVs (no hand-typed numbers), report the weighting crossover, Spearman's rho and leave-one-out correlations.
- `coral_trend_test.py`: adds calendar-month seasonal Mann-Kendall, annual-maximum Mann-Kendall and a results CSV. New `download_dhw_reef_cells.py` averages DHW over the 5 km cells that contain mapped reef.
- New `ndbi_land_change.py`: land-only NDBI change from the cloud-masked rasters, near-ecosystem zone, block-bootstrap interval.
- Figures: coral figure redrawn as one panel per island with annual maxima; governance figure no longer plots Lakshadweep at zero; weighting-sweep subtitle computed from the data; population figure reads the CSV; new `study_area_map.py` draws the study areas from the project's own data. SLR webmaps show settlements without a usable elevation in grey with the reason, instead of "−32767 m".
- New `scripts/run_all.py` runs the full pipeline in order.

### Documentation changes
Research question and hypotheses stated in Section 1 of the paper; study-area map added as Figure 1; corrected the 404 explanation, the GMW epoch description, the seasonal-test description and the "24-year" wording (the series covers 25 calendar years, 1996–2020); Canary Islands disclosed as having no mapped reefs; conclusion no longer asserts misallocation. Executive Summary no longer claims that exposure alone misranks islands. New `DATA_SOURCES_AND_LICENSES.md`.

## Entry 14

### Status
Reran everything with the Entry 13 fixes plus a bare earth elevation model (10–11 October 2026). Numbers are now frozen. The paper, Executive Summary, README, CITATION.cff, dashboard and both portfolio pages were rewritten from the new CSVs, nd the dashboard now reads its numbers straight from `data/` so it can't go stale again.

### Why a Second Elevation Model
Entry 13 fixed the NoData problem, but the 1st clean run on Copernicus GLO-30 still bothered me. Copernicus is a surface model. On a palm covered atoll it measures the top of the canopy nd the roofs, not the ground, nd my whole threshold is 1 m. So I added DeltaDTM v1.1 (Pronk et al. 2024), which is Copernicus with trees nd buildings removed using ICESat-2 nd GEDI lidar. Same 1 arc second grid as Copernicus, heights above EGM2008, about 0.4–0.5 m error against airborne lidar.

The 4TU download page was down for storage maintenance, so I exported the tiles from the Earth Engine community catalogue copy instead (`projects/sat-io/open-datasets/DELTARES/deltadtm_v1-1`): 77 tiles, one Drive export each, with `scripts/acquisition/export_deltadtm_gee.py`. `prepare_deltadtm_tiles.py` checks each tile's bounds against the Copernicus tile it replaces nd builds one VRT per island. It's now the 1st step of `run_all.py`.

### The Seychelles Granite Hill Bug
1st DeltaDTM run, a few Seychelles points looked wrong when I opened the per point file. Petite Sœur, Grande Sœur, Île Marianne: Copernicus 30–76 m, DeltaDTM close to 0 m. These are small forested granite islands. A 50 m tree canopy is not a thing there, so DeltaDTM was reading a hill as sea level. DeltaDTM is clipped at 30 m nd only meant for the coastal zone, so I added one rule: where Copernicus is above 30 m, DeltaDTM is not used nd the point counts as high terrain. Same rule in the population script. Also: where DeltaDTM is empty nd Copernicus is above 10 m, tht's "above 10 m", which is wht an empty cell means in this product. Reran once more, then froze the numbers.

### Coral: Mean Over Reef nd the Serial Correlation Correction
The coral side changed too. Instead of 1 5 km cell per island, the series is now the mean over every DHW cell tht touches mapped reef (`download_dhw_reef_cells.py`). And the seasonal Mann-Kendall test is now the version corrected for serial correlation (Hirsch & Slack 1984), on calendar month means, 300 months. DHW is a 12 week running sum, so one warm spell shows up in 3 nd 4 months in a row, nd the plain test counts each of them as new evidence. With the correction, no island is significant: Seychelles p = 0.14 (uncorrected 0.0008), Maldives 0.31, Fiji 0.55, Lakshadweep 0.90. "Significant for Maldives nd Seychelles" had been a headline result since version 1. But the uncorrected p is wrong for this kind of series.

### Decisions (frozen)
1. People (WorldPop) at or below 1 m is the main exposure measure. OSM points are mostly island nd islet names, so they're kept as a 2nd measure, renamed "named places".
2. DeltaDTM is the main elevation model; Copernicus is reported next to it everywhere.
3. Coral = mean DHW over reef cells + corrected seasonal Mann-Kendall.
4. Canary Islands' reef input to the compound score is 0 (no reef).
5. Compound score is descriptive. The top island depends on the weighting nd I say so.
6. Governance is descriptive (n = 4).
7. NDBI is supplementary, land pixels only.
8. Cyclone tracks (IBTrACS) dropped from the analysis; the Sentinel-2 record doesn't reach the big cyclones anyway.
9. EGM2008 is treated as mean sea level nd this is stated as an approximation.

### Final Numbers
People at or below 1 m, DeltaDTM (Copernicus in brackets): Maldives 11.82% (8.88), Lakshadweep 6.40% (0.79), Seychelles 2.07% (0.43), Fiji 0.28% (0.21), Canary Islands 0.19% (0.15). Named places at or below 1 m on DeltaDTM: Maldives 28.8%, Seychelles 24.7%, Fiji 4.7%, Lakshadweep 3.8%, Canary Islands 0.26%.

Reef heat stress change, 1996–2000 to 2016–2020: Seychelles +0.52, Fiji +0.29, Maldives +0.07, Lakshadweep +0.05 °C-weeks. Mangroves flat (Fiji 485.7 → 488.4 km²).

Compound score at equal weights: Seychelles 0.581, Maldives 0.512, Lakshadweep 0.267, Fiji 0.256, Canary 0.000. The top flips to Maldives at 54% exposure weight. So the "Seychelles is top at every weighting" result from version 1 is gone, It was only ever true because both of version 1's inputs happened to be highest for Seychelles.

Governance: share of the 10 km coastal zone protected, Seychelles 71.4%, Canary 50.4%, Fiji 12.2%, Maldives 1.3%, Lakshadweep no record. r = −0.01 (95% interval −0.96 to 0.96), without Seychelles −0.95. The 0.965 from version 1 is gone.

NDBI on land: Maldives +0.055 (0.040 to 0.072), Seychelles −0.001, Fiji −0.011.

### What I Changed in the Write-Ups
- Dashboard: new `dashboard/results.py` loads every number from the CSVs; all pages rewritten on top of it. Trends page now shows the reef cell mean with period means instead of OLS lines. The slider data (`dashboard/static/settlement_elevations.csv`) is rebuilt by `run_all.py`.
- Paper rewritten for version 2, with a new Section 2.5 on surface vs bare earth models nd a Section 6.1 tht lists every version 1 result tht didn't hold nd why.
- Executive Summary, README, CITATION.cff (version 2.0.0) nd `DATA_SOURCES_AND_LICENSES.md` (DeltaDTM added) rewritten.

## Entry 15

### Status
Second full check of the whole project (20 October 2026), followed by corrections that did not need the large rasters. The exposure, coral and mangrove numbers did not change. The compound score, the weighting crossover and the governance correlation did.

### Corrections
| Change | Before | After | Why |
|---|---|---|---|
| Compound score scaling | Coral input scaled across the 4 reef islands, Canary set to 0 afterwards | Both inputs scaled across all 5 island groups (Canary raw coral input 0) | The paper (Section 3.6) said five; the code did four, so Lakshadweep got the same coral input (0) as an island with no reef |
| Compound scores (equal weights) | Seychelles 0.581, Maldives 0.512, Lakshadweep 0.267, Fiji 0.256 | Seychelles 0.581, Maldives 0.563, Lakshadweep 0.320, Fiji 0.282 | Follows from the scaling fix |
| Top-island crossover | 54% exposure weight | 52% | Same |
| Governance correlation | r = −0.01 (−0.96 to 0.96), LOO up to 0.55; ratio r = 0.64 | r = −0.10 (−0.97 to 0.95), LOO up to 0.42; ratio r = 0.57 | Uses the corrected scores |
| "Uncorrected" coral p-values | Ordinary seasonal test on the raw 30-day samples (Seychelles 0.0008, Maldives 0.07) | Ordinary seasonal test on the same 300 monthly means as the corrected test (Seychelles 0.002, Maldives 0.049) | Like-for-like comparison; only the serial-correlation correction now differs |
| Land-area validation (Section 6.3) | Maldives 317.6 km², Seychelles 449.6, Fiji 18,820.6, Canary 7,432.6 | 292.9, 443.9, 18,819.3, 7,434.1 (EPSG:6933, overlaps merged) | The earlier figures were not reproducible from the current boundary files; new `scripts/validation/boundary_area_validation.py` writes them. All still within 4% of the reference figures |
| DeltaDTM description | "cells above 10 m are left empty" | Coastal product meant for land below about 10 m, values clipped at 30 m | The tiles hold values up to 30 m |
| Named places, two DEMs | Not stated that DeltaDTM drops some points | Stated; on the common point set Seychelles still leads on Copernicus (8.4% vs 4.4%) | Different denominators (Seychelles 154 vs 162) |
| NDBI | "for the 3 islands" | The three windows named (Malé area, Mahé, western Viti Levu); possible effect of Hulhumalé reclamation noted | The analysis never covered whole countries |
| WDPA note | – | 25 of the Maldives' 93 records are UNESCO-MAB zones, stated | Coverage definitions differ |

## Entry 16

### Status
New analysis (23 October 2026): do the statutory coastal setbacks of the five governments cover the buildings that stand on low land? Added as Sections 3.9 and 4.8 of the paper, with Figure 9. Nothing else in the results changed.

### Why
The governance part of the study only asked whether protected area coverage follows risk, with n = 4. A setback is the one coastal rule that decides where people may build, and buildings give hundreds of thousands of observations instead of four. The 100 m WorldPop grid is too coarse for a 20–25 m rule, so I used building footprints.

### What I Did
- Downloaded Overture Maps buildings (release 2026-08-19.0) for the five study areas (`scripts/acquisition/download_buildings_overture.py`) and reduced them to one representative point per footprint (`scripts/processing/export_building_points.py`): Maldives 124,936, Lakshadweep 9,464, Seychelles 53,565, Fiji 284,279 (OpenStreetMap only), Canary Islands 880,740.
- `scripts/analysis/setback_calibration.py` samples elevation with the same DeltaDTM/Copernicus rule as the population analysis, measures distance to the edge of the validated island polygons, and compares it with each setback. Added to `run_all.py`; it skips if the building files are absent.
- Figures: `outputs/plots/fig9_setback_calibration.png` (coverage curve, written by the analysis script) and `fig10_setback_close_ups.png` (`scripts/figures/setback_example_maps.py`, close-ups of the densest low-lying cluster per island); interactive `setback_coverage_curve.html` added to `build_interactive_plots.py`.
- Checked the legal texts: Ley 22/1988 de Costas art. 23 (100 m, 20 m on urban land); Seychelles S.I. 91 of 2023 reg. 13 (25 m from the high water mark, 10 m with permission); Maldives tourism environment regulation cl. 2.10 (5 m from the vegetation line, resort islands only; nothing found for inhabited islands); Lakshadweep ICRZ 2019 20 m no development zone (secondary sources only, primary text still to check); Fiji none found.

### Results
| Island group | At or below 1 m | Setback | Low buildings outside every setback | 90% of low buildings within |
|---|---:|---|---:|---:|
| Maldives | 13.4% | none (inhabited) | 99.4% | 225 m |
| Lakshadweep | 4.7% | 20 m | 93.2% | 345 m |
| Seychelles | 4.6% | 25 m | 92.0% | 427 m |
| Fiji | 0.5% | none | 99.8% | 463 m |
| Canary Islands | 0.02% | 100 m / 20 m | 15.1% | 122 m |

The building shares follow the population shares from Section 4.1, which is a useful cross-check. 45% of the low Seychelles buildings and 39% of the Fijian ones are on DeltaDTM cells below 0 m (south-east Mahé, Praslin, La Digue, Kadavu); dropping them changes the "outside every setback" share by under three points.

### Still To Do
- Check the primary text of the ICRZ 2019 notification for the Lakshadweep width.
- Look at the 4,478 Maldivian buildings that fall more than 50 m outside the island polygons (largest cluster in Addu Atoll); some islands may be missing from boundaries_v2.

## Entry 17

### Status
Validation checks (23 October 2026). Went through the parts of the analysis that rest on my own code and checked them against independent calculations. Nothing in the results changed.

### What I Checked
- **Coral trend p-values.** Wrote the seasonal Mann-Kendall test and the Hirsch-Slack correction again from scratch in NumPy (`scripts/validation/coral_trend_check.py`) nd ran it on the same monthly series. The uncorrected p-values match pyMannKendall exactly. The corrected ones match to within 0.005 (Maldives 0.316 vs 0.313, Seychelles 0.144 vs 0.143, Fiji 0.553 vs 0.550, Lakshadweep 0.905 vs 0.900). None of them comes near 0.05, so H1 stays where it was.
- **Setback distances.** The setback script measures distance on a flat approximation around each island's mean latitude. Checked about 13,000 sampled buildings against ellipsoidal distances (Vincenty) to the same shoreline (`scripts/validation/setback_distance_check.py`). Median difference: 0.07 m Maldives, 0.17 m Lakshadweep, 0.04 m Seychelles, 0.40 m Fiji, 3.8 m Canary Islands. Fewer than 0.1% of sampled buildings change side of a 20, 25 or 100 m line.
- **Boundary reader.** The setback script reads the GeoPackages with its own small parser instead of GeoPandas. The land areas it gives (292.9, 443.9, 18,819.3, 7,434.1, 30.8 km²) are the same as the ones `boundary_area_validation.py` gets with GeoPandas, so the parser reads the polygons correctly.
- **Elevation rules.** The named places, population nd building analyses read elevation in different ways (point, 100 m cell, building point), but they use the same rules for NoData, 0 m water cells, the 10 m nd 30 m Copernicus cut-offs nd negative values. Wrote them down as one table in Section 3.3 of the paper.

### Other Changes
- `run_all.py` now ends with "COMPLETE RUN" or "PARTIAL RUN" nd exits with an error code if any step failed, so old outputs can't be mistaken for fresh ones. The two validation scripts are part of the run.
- Paper: one sentence on what the study adds (Section 1), the elevation rule table (3.3), the coral check (3.5), nd the distance check, the mapped-boundary wording nd the one-point-per-building note (6.7).

## Entry 18

### Status
Policy coding (1 November 2026). Until now I only compared the setback widths. Wanted to compare the five governments' coastal rules as a whole nd see how they changed over time.

### What I Did
- **Coded the rules by hand.** Went through the coastal nd environmental laws for Spain/Canary Islands, India/Lakshadweep, Seychelles, the Maldives nd Fiji. For each one I checked six types of instrument: a building setback, statutory coastal zones, an impact assessment law, a national coastal plan, a body that only deals with the coast, nd a climate framework law. The count of these is the policy density. The setback width is the intensity. I took this split from Knill, Schulze nd Tosun (2012). It's all in `data/policy_coding/` with a codebook, nd next to every value I wrote down where I got it from nd whether I read the actual legal text or only a summary.
- **Made a timeline.** 23 dated changes from 1988 to 2025, each marked as expansion, dismantling, a shift between levels of government, reform or implementation. Some of these I didn't know before I started. Spain's 2013 reform loosened parts of the 1988 Ley de Costas (longer concessions, 12 settlements taken out of the public domain), nd in 2023 Spain handed coastal management functions to the Canary Islands government. In the Maldives, the 2024 reclamation amendment nd the 2025 replacement of the Environmental Protection Agency go in the opposite direction to everything else on the list.
- **Put the rules next to the buildings.** `scripts/analysis/coastal_policy_coding.py` compares density nd intensity with the share of low buildings each setback reaches (Entry 16). Lakshadweep comes second in density (5 of 6) but its setback reaches 6.8% of its low buildings. The Maldives has 2 of 6 nd reaches none. If I had only counted laws, these two would look very far apart.
- **Added regime type.** `scripts/acquisition/download_vdem_owid.py` downloads the V-Dem electoral democracy index, nd the timeline shows the score in the year of each change. Rules were added under scores from 0.13 (Fiji, 2011, under military rule) to 0.89 (Spain, 1988), nd relaxed at 0.88 (Spain) nd 0.56–0.58 (Maldives), so regime type doesn't sort the changes here. With five countries I can only describe this, not test it.
- **Wrote a policy brief.** Two pages on why distance rules don't work on atolls nd what to use instead (`paper/DJ_Policy_Brief.md`).

### Open Points
- I did the coding alone, so there's no second coder to compare with.
- Where I couldn't find an instrument I coded 0, but that doesn't prove it doesn't exist, especially for the Maldives nd Fiji.
- The Lakshadweep setback width nd the Maldivian changes of 2024–2025 come from secondary sources.

## Entry 19

### Status
Review of the policy side (7 November 2026). Had the whole project checked from scratch on a copy of the folder. Every headline number reproduced, but the policy claims went further than the design allows. Reframed them; no exposure, coral, mangrove or compound-score number changed.

### What the Review Found
- **The setback "reach" was not a policy outcome.** At the same 20 m width, low buildings within the line are 5.2% in the Maldives (no rule), 6.8% in Lakshadweep (rule), 5.6% in Seychelles nd 6.9% in Fiji (no rule). So the share is set by where the low land lies, not by whether a rule exists. On top of that, the code set reach to 0% wherever there was no setback, while the same islands showed 99.4% nd 99.8% "outside every setback", which don't add up to 100.
- **The buildings mostly predate the rules.** A setback decides where new buildings go. Seychelles adopted its 25 m line in 2023, so most of today's buildings can't tell me anything about it. The measure shows whether a rule is drawn where low buildings stand (design fit), not compliance.
- **The Canary 85% rests on 192 buildings**, many on port quays, with 100 m applied to all of them. Under the 20 m rule for land already urban in 1988 it is 52%.
- **Smaller points.** India's V-Dem in 2011 is 0.67, not 0.71. The Executive Summary had the corrected coral p-values in the wrong island order. The Discussion said 80–140 m where the data give 80–136 m.

### What I Changed
- **The question.** RQ2 now asks whether the coastal siting rules are written in units that match where the low buildings stand, nd whether instrument counts track that fit. "Reach", "more rules did not help" and "the case where a setback works" are gone from the paper, Executive Summary, policy brief, README, dashboard nd portfolios.
- **The code.** `coastal_policy_coding.py` no longer forces 0%; where there is no setback it reports none, nd every island gets the share of low buildings within the same 20 m and 100 m widths. Figure 11 now shows the 20 m width on every island instead of "reach".
- **The design.** A case-selection table (status, who sets the rule, island type, population, legal reference line) and a plain statement that the five were chosen for ecological range, so this is a structured comparison, not a controlled one. The Maldives–Lakshadweep pair is described with its differences (population, reclamation, tourism, entry permits).
- **Literature.** New Section 2.6 on setbacks and policy design (Sanò et al. 2011; Hall 1993; Howlett 2011), and George nd Bennett (2005) for the comparison.
- **Limits written in.** Coverage is design fit, not compliance; the Canary figure is fragile; four of six density items are Authority and no Treasure item is coded; Maldivian nd Fijian items have no primary text, so their low density may partly be source access; width is not stringency.
- **Lakshadweep 2019.** Read the 2011 Island Protection Zone notification. Lakshadweep was managed through Integrated Islands Management Plans, not a fixed no development width. If those plans restricted building near the shore more than the 20 m zone, the 2019 change is dismantling, not reform. Not verified yet, so it stays coded as reform with the caveat in the paper.
- **Low land instead of buildings.** New `scripts/analysis/setback_lowland_coverage.py` lays a 30–60 m grid over every island nd measures the share of land at or below 1 m within each width. On the atolls nd Seychelles a 20–25 m setback covers 19–26% of the low land, against 5–8% of the low buildings, nd 100 m covers 63–70%. Fiji's low land is far inland (7% within 20 m), the Canaries' is a narrow strip (48% within 20 m). With a rule (Lakshadweep 21.8%) or without (Maldives 19.3%), the 20 m share is nearly the same.

### Open Points
- Verify the IIMP rules for Lakshadweep and the Maldivian and Fijian "not found" items in primary texts.
- Canary Islands: separate port service zones and land urban in 1988 if the cadastre layers can be obtained.

