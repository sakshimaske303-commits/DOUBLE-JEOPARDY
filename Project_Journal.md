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