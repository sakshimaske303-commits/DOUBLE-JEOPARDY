# DOUBLE JEOPARDY: The Vulnerability Spiral

## Project Journal

## Project Overview

DOUBLE JEOPARDY is a geospatial framework built to test whether small island nations face a compounding vulnerability to climate change: high physical exposure to sea-level rise, layered with degrading natural coastal defenses. Rather than treating "ecosystem buffer" as one undifferentiated category, this project deliberately tests two ecosystem types independently — mangroves and coral reefs — across five island nations spanning three ocean basins: Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands.

Beyond ecological and physical risk, the project extends into a governance dimension, testing whether formal protected-area designation — the main policy tool through which governments claim to manage coastal ecosystem risk — is actually aligned with where verified vulnerability is highest, or whether it reflects a "paper park" gap between policy and evidence.

## Problem Statement

Climate adaptation policy and conservation financing frequently assume that mangroves and coral reefs degrade together under environmental pressure, and jointly determine a coastal settlement's exposure to sea-level rise. This assumption is rarely tested against independent, multi-temporal evidence at a systematic, cross-national scale. A second, related problem is that formal protected-area status is often treated as a proxy for effective ecosystem management, even though protected-area boundaries are frequently drawn on historical or administrative grounds rather than continuously updated risk data.

## Aim

To build a reproducible geospatial framework that independently quantifies physical sea-level-rise exposure and ecosystem degradation — tested separately for mangroves and coral reefs — across five island nations, and to test whether existing protected-area governance is statistically aligned with this empirically verified vulnerability.

## Research Questions

**RQ1**: Does physical sea-level-rise exposure combine with ecosystem buffer degradation to produce compounding settlement-level vulnerability — and does this operate uniformly across ecosystem types, or does it depend on which specific ecosystem is degrading?

**RQ2**: Does the spatial distribution of formal protected-area designation correlate with empirically verified compound vulnerability, or is it statistically independent of actual, satellite-derived ecosystem risk?

## Hypotheses

**H1 (Coral Pathway)**: Coral reef ecosystems will show a measurable increase in thermal bleaching stress over a multi-decadal period, more pronounced in islands with higher physical exposure.

**H2 (Mangrove Pathway)**: Mangrove ecosystems will show a measurable decline in spatial extent over the same period, contributing an independent compounding pathway alongside coral degradation.

**H3 (Governance Alignment)**: Islands with higher compound vulnerability scores will show correspondingly higher formal protected-area coverage, consistent with risk-responsive governance.

## Data Sources

The project integrates ten independently-sourced datasets across all five islands: settlements, tourism infrastructure, and general infrastructure (OpenStreetMap); mangrove extent (Global Mangrove Watch, three independent years — 1996, 2010, 2020); coral reef extent (WCMC Ocean Data Viewer and OpenStreetMap); coral thermal stress (NOAA Coral Reef Watch Degree Heating Week, a continuous 1996–2020 time series); protected areas (World Database on Protected Areas); elevation and slope (Copernicus DEM); population (WorldPop); and historical cyclone tracks (IBTrACS).

All datasets were acquired via reproducible, API-based or memory-efficient bounding-box-filtered pipelines rather than manual download, consistent with the project's emphasis on transparency and reproducibility.

## Methodology

### Phase 1 — Baseline Dataset Construction

Settlement, tourism, and infrastructure data were acquired from OpenStreetMap for all five islands and standardized into a consistent, minimal-column format. Ecosystem-buffer data (mangroves, coral reefs, protected areas) were acquired from a mix of scientific atlas sources (WCMC) and OpenStreetMap depending on island, requiring two parallel cleaning pipelines. Terrain, population, and cyclone-track data completed the baseline, with population and elevation figures independently validated against known real-world totals and geography before being trusted for analysis.

Two islands were confirmed to genuinely lack specific ecosystems rather than simply missing data for them: Lakshadweep has no recorded mangroves, and the Canary Islands has no recorded coral reefs — both consistent with the islands' underlying ecology (a small coral atoll without intertidal delta conditions, and a subtropical volcanic Atlantic setting outside typical coral habitat range, respectively) and confirmed independently across multiple data sources rather than accepted from a single query.

Protected-area coverage was substantially upgraded during this phase from an initial low-quality OpenStreetMap source (which implausibly showed as few as one protected area for some islands) to the World Database on Protected Areas, the authoritative global source — increasing coverage from single digits to 49–385 features per island depending on location.

### Phase 2 — Multi-Temporal Ecosystem Analysis

Rather than relying on a single before/after snapshot, mangrove extent was tracked across three independent time points (1996, 2010, 2020) and measured by true area in an equal-area projection rather than polygon count, since satellite classification algorithms can segment the same physical extent into a different number of polygons across years without any genuine change in area. This produced a clear result: mangrove extent has remained essentially stable across all three tested islands (Maldives, Seychelles, Fiji) over the full 24-year span, with no measurable decline in any case.

Coral reef condition was tracked differently, using satellite-derived thermal stress (Degree Heating Week) rather than mapped extent, since coral degradation manifests primarily as bleaching rather than area loss. This continuous 1996–2020 time series showed a rising thermal-stress trend in four of five islands, most severely in Seychelles, whose maximum recorded value falls within the range associated with severe bleaching and coral mortality.

### Phase 3 — Physical Exposure and the Compound Vulnerability Score

Physical exposure was quantified by sampling elevation at every settlement's location across all five islands and calculating the proportion at or below a standard one-meter sea-level-rise threshold, producing a wide range from 12.1% (Canary Islands) to 99.1% (Maldives), directly reflecting the geological difference between low-lying coral-atoll nations and volcanic, mountainous terrain.

Physical exposure and coral thermal-stress trend were then normalized to a common 0–1 scale and combined into a single Compound Vulnerability Score per island. This produced the project's central finding: Seychelles ranks as the highest-overall-risk island (score 0.880) despite having lower physical exposure than the Maldives, because its coral degradation trend is the most severe recorded across the sample — directly demonstrating that physical exposure alone is an incomplete measure of true climate vulnerability.

### Phase 4 — Governance Alignment

Protected-area coverage was quantified within a 10-kilometer coastal buffer around each island (rather than using total captured protected-area extent, which for some islands included vast, only loosely-relevant offshore marine zones), and statistically compared against the Compound Vulnerability Score using a Pearson correlation. This produced a moderately strong positive relationship (r=0.727) — Seychelles, the highest-vulnerability island, also shows the highest coastal protection ratio — but the relationship did not reach conventional statistical significance (p=0.164), a limitation directly attributable to the small five-island sample size rather than to any flaw in the underlying logic. This is reported as a suggestive, not confirmatory, finding.

### Phase 5 — Settlement Encroachment

Using satellite-derived built-up area change (Sentinel-2, comparing 2016 against 2024), the project tested whether settlement expansion was concentrated near ecosystem buffer zones for the three mangrove-present islands. Both Maldives and Seychelles showed a clear increase in built-up density, with Seychelles' change the most pronounced — notably shifting from a vegetation-dominated to a built-up-dominated signal over the eight-year period. Fiji showed effectively no change, consistent with its stability across every other measure tested in this project.

### Phase 6 — Supporting Evidence: Cyclone Damage

As supporting evidence alongside the project's core sea-level-rise and ecosystem-degradation findings, satellite-derived vegetation damage (NDVI, before/after) was tested for Fiji's two strongest recorded cyclones, the only island with both meaningful cyclone-intensity variation and events recent enough to fall within the operational record of the satellite platform used. A clear vegetation decline followed the more extreme of the two events (Cyclone Winston, Category-5 equivalent), while no comparable decline followed the moderate event (Cyclone Yasa) — consistent with the broader pattern of ecosystem resilience observed in Fiji throughout this project.

## Final Findings

Coral reef ecosystems show a genuine, measurable degradation signal across most of the study sample, supporting Hypothesis H1. Mangrove ecosystems, tested with equal rigor across three independent time points, show no comparable decline in any tested island — a result that does not support Hypothesis H2, and is reported as a substantive finding in its own right rather than adjusted to fit the project's original framing. This asymmetry between ecosystem types is itself one of the project's core contributions: ecosystem buffer degradation is not a uniform phenomenon, and conservation resources may need to be prioritized differently across ecosystem types rather than allocated under an assumption of uniform risk.

The governance-alignment test (H3) finds a directionally encouraging but statistically inconclusive relationship between vulnerability and protection — a limitation of sample size rather than of the underlying evidence, and reported transparently as such.

Physical exposure alone is shown, directly and quantitatively, to be an insufficient measure of true climate risk: the island with the highest exposure (Maldives) is not the island with the highest overall compound vulnerability (Seychelles) once ecosystem degradation is properly accounted for — the project's central, headline result.

## Deliverables

A fully reproducible, cross-national geospatial data-acquisition and analysis pipeline spanning ten datasets and five island nations; a validated multi-temporal mangrove and coral dataset; a composite Compound Vulnerability Score with full cross-island ranking; a governance-alignment analysis; a settlement-encroachment analysis; a multi-page interactive Streamlit dashboard combining live-recalculating features, interactive QGIS-based maps, and static visualizations; and a complete open-source codebase.

## Limitations

The governance-alignment finding is limited by a small five-island sample, providing insufficient statistical power to confirm a relationship that is nonetheless directionally consistent with risk-responsive governance. Lakshadweep population data was not acquired due to an impractically large source-file requirement and is deferred rather than estimated. Cyclone-damage supporting evidence was only possible for Fiji, since satellite verification is inherently bounded by the operational start date of the Sentinel-2 platform (2015), and the other four islands' strongest historically recorded cyclones predate this record.

