# Satellite Verification of India's Vibrant Villages Programme: A Compositing-Window Robustness Assessment of Border-Village Development

*[Manuscript prepared for double-blind review — author name, affiliation, and self-identifying links are withheld from this file per JOSIS submission guideline 4. See note to author at the end of this document.]*

## Abstract

India's Vibrant Villages Programme (VVP-I) has sanctioned approximately ₹4,800 crore across 2,967 villages in five Himalayan border states and union territories, including 662 Phase-I priority villages since 2022–23, with no independent impact assessment yet conducted — a gap confirmed on the parliamentary record. This study evaluates physical development at 258 geocoded priority villages across three core states (Arunachal Pradesh, Sikkim, Uttarakhand), plus an illustrative sample of seven Himachal Pradesh villages, using Sentinel-2 built-up-index (NDBI) change and VIIRS night-lights radiance change between 2021 and 2025, compared against a matched non-VVP control group of 735 villages in the same fourteen districts. Results are reported under two compositing windows (full-year and summer-matched) to test sensitivity to snow and monsoon-cloud contamination. A full-year composite shows no significant increase in built-up area, whereas a summer-matched composite on the same villages shows a significant increase — a reversal attributable to seasonal contamination rather than a genuine difference in underlying change. The summer-window signal persists under a district-fixed-effects difference-in-differences comparison against the control group, a buffer-radius sweep (250 m/500 m/1 km), and a Holm–Bonferroni correction for multiple testing, though a three-point 2021/2023/2025 extension shows the change concentrated in a 2023–2025 recovery rather than sustained growth since sanction. Night-lights show no absolute increase for treated villages in either window, but a significant positive gap relative to the control group, driven by control-village decline rather than treated-village increase. This instability across compositing windows is reported as a central finding, underscoring the continued absence of independent verification of VVP-I's outcomes.

**Keywords:** Vibrant Villages Programme; border development; securitization theory; satellite verification; NDBI; VIIRS night-lights; remote sensing; robustness testing; difference-in-differences

---

## 1. Introduction

India's border villages have historically been framed in policy discourse as liabilities: remote, sparsely populated, and vulnerable within a contested frontier. The Vibrant Villages Programme (VVP-I), approved by the Union Cabinet in February 2023, reframes 2,967 villages across Arunachal Pradesh, Sikkim, Uttarakhand, Himachal Pradesh, and Ladakh as development priorities rather than security afterthoughts. More than two years after sanction, however, no independent basis exists for determining whether the promised development has occurred. When Parliament was asked directly whether VVP-I's impact had been assessed, the Ministry of Home Affairs replied that no impact assessment had been conducted (Lok Sabha Unstarred Question No. 508, 3 February 2026) [8].

This study addresses that gap directly, testing at the village level whether physical development is observable on the ground following sanction, whether the magnitude of any such change corresponds to state-level budget allocation, whether distance to the border is more closely associated with development than developmental need would predict, and whether any detected change can be attributed specifically to VVP-I rather than to general regional trends. These questions are motivated by securitization theory: if border infrastructure functions primarily as a geopolitical signal rather than a welfare intervention, the pattern of results should follow proximity to the border rather than developmental need [2].

Five research questions follow: does built-up area expand at priority villages since sanction (RQ1); does the magnitude of expansion scale with budget (RQ2); do night-lights corroborate the built-up-area pattern (RQ3); is development concentrated near the border rather than where need is greatest (RQ4); and can any detected change be attributed to VVP-I specifically rather than to general village-level or regional trends (RQ5)? Four hypotheses operationalize these questions: built-up area increases measurably since sanction (H1); this increase scales sub-proportionally with budget (H2); villages closer to the border/Line of Actual Control (LAC) change more than villages farther away within the same state (H3); and any change attributable to VVP-I specifically exceeds the change observed in a matched set of non-priority villages within the same districts and period (H4).

## 2. Literature Review

### 2.1 Securitization Theory and Border Development

Securitization theory holds that framing an issue as a matter of security shifts it from ordinary politics into an "extraordinary" register that unlocks resources and measures that would otherwise be politically infeasible [2]. Border-development spending fits this framing on both registers simultaneously — legitimate as welfare spending, and legitimate as strategic infrastructure — and the two are rarely disentangled in policy discourse. This study treats VVP-I as a test case: whether geographic proximity to the border predicts measurable development more strongly than conventional development indicators would.

### 2.2 The Vibrant Villages Programme: Policy Context and the Accountability Gap

Documentation of VVP-I's scope is dispersed across parliamentary replies rather than consolidated in a single source. A complete village-wise annexure was provided in Rajya Sabha Unstarred Question No. 2321 (9 August 2023) [4]. The 75 priority villages of Himachal Pradesh were confirmed in Lok Sabha Question No. 2104 (2023) [5] and Rajya Sabha Question No. 401 (2025) [6], though without a village-level name list. Ladakh's 35 sanctioned villages were confirmed in Lok Sabha Question No. 4360 (2025) [7], again without a published village-level list. Most directly relevant to this study, Lok Sabha Unstarred Question No. 508 (3 February 2026) records the Ministry's confirmation that no impact assessment of VVP-I has been conducted [8]. No government source provides an independent, satellite-verified account of development against the programme's stated scope; this study addresses that gap.

### 2.3 Remote Sensing Approaches to Built-Up Area and Economic Activity Detection

Two indices carry the analytical weight of this study. The Normalized Difference Built-up Index (NDBI), derived from short-wave-infrared and near-infrared reflectance, is a widely used proxy for built-up surface extent in multi-temporal comparison [13]. The VIIRS Day/Night Band measures a related but distinct quantity — night-time radiance associated with electrification and economic activity — with substantially improved dynamic range and spatial resolution relative to its DMSP-OLS predecessor [3]. The two indices have complementary failure modes: NDBI is vulnerable to vegetation phenology and snow cover, VIIRS to cloud cover and sensor saturation at low radiance. Disagreement between the two need not indicate that either is in error; agreement between them is treated as carrying more evidential weight than either index alone.

### 2.4 Compositing-Window Sensitivity in Multi-Temporal Satellite Analysis

Change detection from optical satellite imagery in high-relief terrain is complicated by two related effects: snow cover and cloud frequency vary by both season and elevation, and a compositing choice that is insensitive to this variation can obscure or fabricate an apparent signal of change. Rather than treating this sensitivity as noise to be averaged away, this study tests it directly as a property of the result itself — including the possibility that a finding reverses between two independently defensible compositing windows.

## 3. Data and Methodology

### 3.1 Study Design

The core statistical sample comprises 251 villages across Arunachal Pradesh, Sikkim, and Uttarakhand, the three states for which village-wise official information permits identification. Himachal Pradesh's seven confirmed villages are reported separately as an illustrative case study rather than included in the core sample, and Ladakh is excluded from village-level analysis entirely because of a documented data-availability gap (Section 6.1). Before/after change at treated villages is assessed against a difference-in-differences specification (H4) incorporating district fixed effects — which remove each district's own time-invariant baseline level, not a district-specific trend, since the model's post-period term is shared across all districts and villages — and a matched non-VVP control group of 735 villages in the same fourteen districts, to net out common secular trends unrelated to VVP-I. Two further checks extend the core 2021-versus-2025 comparison: a third, independent time point (2023), and a buffer-radius sweep (250 m and 1 km alongside the primary 500 m) to test whether the choice of extraction buffer, like the choice of compositing window, affects the result.

### 3.2 Data Sources

| Variable | Source | Temporal Coverage |
|---|---|---|
| Village identification | State VVP-I portals; Rajya Sabha/Lok Sabha Q&A annexures | 2023–2025 |
| Village coordinates | OpenStreetMap Nominatim; ISRO Bhuvan Village Geocoding API | Current |
| Non-VVP control village identification | OpenStreetMap Overpass API, district-matched to treated sample | Current |
| Built-up index (NDBI) | Sentinel-2 SR Harmonized | 2021, 2023, 2025 |
| Night-lights radiance | VIIRS DNB monthly composites | 2021, 2023, 2025 |
| Border/LAC geometry | Natural Earth 10 m Admin-0 Boundary Lines | Current |
| Budget/project counts | State-wise VVP-I sanction figures (parliamentary record) | 2023 |

### 3.3 Village-Level Dataset Compilation and Geocoding

Primary geocoding was performed via Nominatim, with ISRO Bhuvan used as a Census-linked fallback. Bhuvan does not filter by state — a test query for the Arunachal Pradesh village "Kharman" initially returned an unrelated, same-named village in Haryana — so manual district-level validation was applied to every result from both sources, and each village list was cross-checked against official aggregate figures before acceptance. Of 559 villages attempted across the four states, 258 were successfully geocoded: 186 of 455 in Arunachal Pradesh, 31 of 46 in Sikkim, 34 of 51 in Uttarakhand, and 7 of 7 in Himachal Pradesh.

### 3.4 Satellite Change Detection

A 500 m buffer around each geocoded village was used to extract mean NDBI and VIIRS night-lights radiance via Google Earth Engine, comparing 2021 against 2025. NDBI was derived from Sentinel-2 Level-2A Surface Reflectance bands B11 (SWIR1) and B8 (NIR), with cloud masking via the QA60 band. Night-lights were derived from VIIRS Day/Night Band monthly composites (NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG).

### 3.5 Compositing-Window Robustness Testing

Both measures were extracted under two compositing windows — full-year and summer-matched (June–September) — designed to isolate genuine change from opposing seasonal artifacts (snow contamination in the full-year composite; monsoon cloud cover in the summer-matched composite). A village with no valid composite in a given window was recorded as null rather than defaulted to zero.

### 3.6 Border-Proximity Analysis

Distance from each village to the nearest relevant Natural Earth Admin-0 boundary segment on Indian territory was computed in GeoPandas. The India–China Line of Actual Control (LAC) is contested and has no internationally agreed alignment; all distances reported in this study are therefore relative and comparative, not an authoritative delineation of the border.

### 3.7 Non-VVP Control Group and Difference-in-Differences Design

A treated-only before/after comparison cannot rule out the alternative explanation that an observed shift reflects conditions shared by all villages in the region irrespective of treatment status — unrelated infrastructure spending, unrelated state initiatives, or weather-driven regrowth after an anomalously low baseline year. To address this, a non-VVP control group was assembled from the same fourteen districts as the treated sample via the OpenStreetMap Overpass API, excluding any village on a VVP-I priority list, and processed through an identical pipeline (500 m buffer, NDBI/VIIRS definitions, before/after windows). The resulting panel was tested as:

*ndbi (or lights) ~ treatment + post + treatment×post + district fixed effects*

with standard errors clustered at the district level (14 clusters). The coefficient of interest is the treatment×post interaction, representing the treated group's change net of the control group's change over the same period, after removing any district-level baseline growth trend captured by the fixed effects. A parallel HC3 heteroskedasticity-robust specification without fixed effects is reported alongside the primary specification, since 14 clusters falls below the 30–40 typically recommended for cluster-robust asymptotics to be fully reliable. A parallel-pre-trends placebo test — of the kind conducted elsewhere using a multi-period pre-treatment panel — could not be run on this design, since the control group's satellite extraction covers only the same single before/after pair as the treated sample; a level-balance check (Mann-Whitney U) at the 2021 baseline is reported instead as a weaker substitute.

### 3.8 Multi-Year Trend Extraction

A two-point 2021-versus-2025 comparison cannot distinguish genuine development from weather-driven variation at either endpoint. A third time point, 2023, was therefore extracted for the same 251-village core sample under both compositing windows, yielding one annual value per village rather than a single before/after delta. A per-village linear trend was fitted across the three years, and a Wilcoxon signed-rank test assessed whether the resulting slopes differed from zero; a village-fixed-effects panel regression (value ~ year, clustered standard errors by village) was applied as a second specification. The 2021–2023 and 2023–2025 sub-intervals were also tested independently to identify whether change was concentrated in one half of the window.

### 3.9 Buffer-Radius Robustness Testing

The 500 m buffer used throughout Sections 3.4–3.8 was tested against two alternative radii — 250 m and 1 km — for the summer-window extraction on the same core sample, with a Wilcoxon signed-rank test performed at each radius. The 250 m and 1 km extractions were run at a later date than the original 500 m extraction; although the target date ranges (2021, 2025) were held fixed, the underlying Sentinel-2 archive had continued to backfill scenes in the interim, confounding a raw village-count comparison across radii with an unrelated archive-timing effect. To isolate buffer radius as the sole varying factor, the comparison was restricted to the subset of villages with valid data at all three radii.

### 3.10 Statistical Testing

Before/after change was tested via the Wilcoxon signed-rank test [12], a paired, non-parametric test appropriate given the sample's non-normal distribution. Spearman's rank correlation [11], robust to non-linear monotonic relationships, was used for the budget correlation (RQ2, descriptive only, given only two states with sufficient valid data) and the border-proximity correlation (H3). The control-group comparison (H4) used the difference-in-differences specification of Section 3.7, with cluster-robust or heteroskedasticity-robust standard errors as reported [1].

## 4. Results

### 4.1 Village Coverage and Sample Composition

258 of 559 attempted villages were successfully geocoded. Arunachal Pradesh's low match rate reflects the absence of many border settlements from civilian geospatial databases — camps and installations administered by border security infrastructure rather than named civilian settlements — a feature of village-level development on a securitized border rather than a gap in the geocoding method itself.

### 4.2 Built-Up Area Change: A Compositing-Window-Sensitive Result

*[Figure 1. Distribution of NDBI change across all geocoded villages, full-year and summer-matched composites.]*

The two compositing windows yield opposite conclusions. Under the full-year composite, the 251-village core sample shows no significant change (Wilcoxon signed-rank, p = 1.000), trending slightly negative at the median. Under the summer-matched composite (n = 154, reflecting seasonal dropout), the same sample shows a highly significant increase (p < 0.000001). This reversal is attributable to snow-cover contamination at the upper and lower bounds of the full-year composite window; the summer-matched window avoids snow but loses all 31 geocoded Sikkim villages to monsoon-season cloud cover.

*[Figure 2. State-wise mean built-up-area change (summer-matched composite), by state.]*

### 4.3 Night-Lights Change: A Stable Null

*[Figure 3. Distribution of VIIRS night-lights change (summer-matched composite).]*

Night-lights show no significant absolute change in either window (full-year p = 0.050, borderline; summer-matched p = 0.9999, a clean null). Because night-lights are not subject to vegetation or snow phenology, this consistency across windows supports treating night-lights as the more temporally stable of the two proxies on this test alone.

*[Figure 4. State-wise mean night-lights change (summer-matched composite), by state.]*

### 4.4 Budget vs. Outcome: A Two-State Descriptive Comparison (RQ2)

*[Figure 5. State-level mean built-up-area change plotted against sanctioned VVP-I budget.]*

Arunachal Pradesh (mean NDBI change +0.0284; sanctioned budget ₹2,749.74 crore across 2,082 projects) and Uttarakhand (mean NDBI change +0.0293; sanctioned budget ₹270.58 crore across 200 projects) were the only two states with sufficient valid summer-window coverage for comparison. A roughly tenfold difference in sanctioned budget corresponds to an essentially equal measured change. With only two data points, no formal statistical test is possible, but the pattern is consistent with H2's prediction that the physical-development signal scales sub-proportionally with budget.

### 4.5 Border-Proximity Testing (H3)

*[Figure 6. Distance-to-border versus NDBI change and night-lights change, both compositing windows.]*

Built-up-area change showed no significant correlation with distance to the border/LAC in either window (full-year ρ = 0.049, p = 0.443; summer-matched ρ = 0.038, p = 0.641) — a stable null across windows. Night-lights showed a more complex pattern: a significant negative correlation in the full-year window (ρ = −0.252, p < 0.0001, consistent with H3's prediction of greater change nearer the border), but no significant relationship in the summer-matched window (ρ = −0.070, p = 0.266).

An earlier version of this analysis computed village-to-border distance by projecting all villages into a single Universal Transverse Mercator zone (44N), which is accurate only near its own central meridian (81°E); this study's villages span approximately 77–97°E, so that method systematically overstated distance for villages farther from 81°E (up to approximately 3% for Arunachal Pradesh's easternmost villages, negligible for Uttarakhand). Distance is now computed geodesically on the WGS84 ellipsoid, removing this zone dependency. The correction shifts every ρ and p-value by a small amount but changes no conclusion: no correlation that was non-significant becomes significant, and the one significant correlation (full-year night-lights) remains significant.

A related methodological point concerns what "distance to border/LAC" measures. It is computed as distance to the nearest India-related boundary segment in the underlying dataset, not specifically the China boundary. Checked directly against the core sample, 220 of 251 villages (88%) are in fact nearest to the China boundary; 19 (predominantly Tawang and West Kameng, Arunachal Pradesh) are nearest to Bhutan, 8 (North Sikkim and Pithoragarh, Uttarakhand) are nearest to Nepal, and 4 (Anjaw, Arunachal Pradesh) are nearest to Myanmar. For this 12% of the sample, H3 measures proximity to a different country's frontier rather than the LAC specifically — a defensible operationalization for a general border-securitization hypothesis, since these remain border villages in the broader sense the programme itself uses, but not a literal LAC-proximity test for that subset. This is discussed further as a limitation in Section 6.2.

### 4.6 Control-Group Difference-in-Differences: Two Effects That Hold, Against an Unbalanced Baseline (H4)

*[Figure 8. District-fixed-effects difference-in-differences coefficient (treated-vs-control gap in change) with 95% confidence intervals, NDBI and night-lights, both compositing windows.]*

Against the matched 735-village control group, the summer-window NDBI gap holds: difference-in-differences coefficient = +0.0322, 95% CI [+0.0146, +0.0498], cluster-robust p = 0.00033 (HC3 no-fixed-effects comparison: +0.0271, p = 0.0124), estimated from 220 treated villages with a valid reading in at least one period against 250 control villages with a valid summer-window reading (of 735). The full-year gap remains non-significant (+0.0088, p = 0.275, n = 190 control villages with valid full-year data), consistent with Section 4.2.

For night-lights, the corrected control group changes the substantive conclusion, not merely its precision. A gap now appears in both windows: summer +0.1413, 95% CI [+0.0442, +0.2385], cluster-robust p = 0.0044 (HC3: same coefficient, p = 0.0019, in agreement); full-year +0.1653, 95% CI [+0.0105, +0.3202], cluster-robust p = 0.0364, though the HC3 no-fixed-effects specification does not agree (p = 0.1033). This does not reflect an absolute rise in treated-village night-lights — the treated-only Wilcoxon test on the identical summer window (Section 4.3) is a clean null (p = 0.9999) — but rather a decline in control-village night-lights over the same period while treated villages remained approximately flat. The finding is more accurately characterized as "treated villages held steady while the surrounding non-priority region declined" than as "treated villages became brighter."

This comparison carries an important caveat, more consequential for night-lights than for NDBI. Treated and control villages differ significantly at the 2021 baseline in three of four outcome/window combinations: NDBI summer (treated mean −0.2461 vs. control mean −0.2442, n = 154/250, Mann-Whitney p = 0.00073); night-lights full-year (treated mean 0.4282 vs. control mean 0.4082, n = 251/190, p < 0.00001, the most imbalanced combination, and the one where the two specifications disagree on significance); and night-lights summer (treated mean 0.4017 vs. control mean 0.3656, n = 251/250, p = 0.0165). Only NDBI full-year shows no significant baseline imbalance (treated −0.1846 vs. control −0.2214, n = 251/190, p = 0.125). This is consistent with priority villages having been selected in part for remoteness, but it means every difference-in-differences estimate rests on a level-difference check rather than a confirmed shared pre-trend, since a genuine multi-period pre-treatment panel was not available for the control group (Section 3.7). The full-year night-lights result should accordingly be treated as specification-dependent rather than settled. At the district level, the NDBI summer gap is positive in 2 of 3 districts with sufficient summer-window coverage on both sides, and the night-lights summer gap is positive in 4 of 5 such districts.

### 4.7 Multi-Year Trend: A Non-Monotonic Recovery Pattern

*[Figure 9. Mean NDBI and night-lights radiance at 2021, 2023, and 2025, core sample, both compositing windows, error bars ±1 SE.]*

Extending the comparison to a third year reveals that the 2021-versus-2025 result is not a steady trend. In the summer-matched window, mean NDBI declines from 2021 to 2023 (mean change = −0.0231, Wilcoxon p = 1.000, a non-significant decline) before rising sharply from 2023 to 2025 (mean change = +0.0222, p < 0.000001). The overall three-year linear trend is not significant (mean per-village slope = −0.0002/year; Wilcoxon p = 0.442; panel regression p = 0.728). The full-year window shows the same decline-then-recovery shape (p = 0.000001 for the 2023–2025 increase), though the two specifications disagree on the overall trend (Wilcoxon p = 1.000; panel regression p = 0.000001), reflecting the panel regression's greater sensitivity to the later recovery relative to the earlier decline. The headline 2021-versus-2025 comparison reported in Section 4.2 should therefore be read as a 2023-to-2025 recovery rather than sustained growth since sanction.

### 4.8 Buffer-Radius Sensitivity: A Stable Result Once Sample Composition Is Matched

*[Figure 10. NDBI Wilcoxon p-value (log scale) at 250 m, 500 m, and 1 km buffer radii, all-valid-villages sample versus the matched 154-village subsample, summer window.]*

Taken at face value, the significant 500 m result (n = 154, p < 0.000001) does not replicate at 250 m (n = 251, p = 0.126) or 1 km (n = 251, p = 0.899). This apparent disagreement, however, is an artifact of a Sentinel-2 archive-backfill effect rather than a genuine buffer-radius effect: the 250 m and 1 km extractions, run at a later date, gained complete data for 97 core-sample villages (66 in Arunachal Pradesh, 31 in Sikkim) that were null at 500 m (Section 3.9). Restricting the comparison to the 154-village subsample with valid data at all three radii resolves the disagreement: all three radii are significant and directionally consistent (250 m, p = 0.000009; 500 m, p < 0.000001; 1 km, p = 0.001471), indicating the result is not an artifact of the 500 m buffer choice used elsewhere in this study.

### 4.9 Robustness Summary

*[Figure 7. Significance across all four core tests, both compositing windows, p-value (log scale), reference line at p = 0.05.]*

Two distinct patterns emerge across the four core tests under both compositing windows. H1 (built-up change) and the H3 night-lights correlation both cross the p = 0.05 threshold between windows — non-significant full-year and significant summer-matched for H1, and the reverse for the H3 night-lights correlation — indicating compositing-window dependence. The H3 NDBI-proximity test, by contrast, remains non-significant in both windows (p = 0.443 full-year; p = 0.641 summer-matched), a genuinely stable null rather than a result that merely failed to flip. This distinction matters for interpretation: an unstable result remains provisional regardless of which window is preferred, whereas a null result stable across windows carries more confidence precisely because it does not depend on the compositing choice. Layering the three additional checks from Sections 4.6–4.8 onto the summer-matched NDBI result specifically, it passes a control-group comparison, a buffer-radius sweep once sample composition is held fixed, and is shown to be concentrated in the second half of the study window rather than the first — narrowing, though not fully resolving, what the surviving signal represents.

The eight headline p-values reported across this section (four tests × two windows) are not corrected for multiple testing in the main text, since they address distinct research questions. As an additional check, a family-wise Holm–Bonferroni correction (α = 0.05) was applied across all eight raw p-values using `src/analysis/holm_correction.py` (`statsmodels.stats.multitest.multipletests`, method="holm"). Both results significant in the uncorrected analysis remain significant after correction: the summer-window NDBI result's raw p = 9.29 × 10⁻¹⁵ becomes a Holm-adjusted p = 7.43 × 10⁻¹⁴, and the full-year lights-proximity result's raw p = 5.48 × 10⁻⁵ becomes a Holm-adjusted p = 3.83 × 10⁻⁴. None of the remaining six results become significant; five adjust to 1.000, and the sixth (full-year night-lights change, raw p = 0.050) adjusts to p = 0.300. This correction does not establish either finding as causal, but it rules out the possibility that either result reflects a false positive arising from running eight tests concurrently. The robustness tests of Sections 4.6–4.8 were designed after this correction was applied, not as additional tests drawn from the same family.

## 5. Discussion

The central finding of this study is not a specific magnitude of increase or decrease in physical development, but the instability of the one metric that initially appeared significant, and the more precise picture obtained once that instability was stress-tested against a control group, a multi-year extension, and a buffer-radius sweep. A single-date, single-window spectral comparison alone cannot support an unequivocal conclusion about built-up-area change in high-relief Himalayan terrain, where both snow cover and monsoon cloud can reverse a result's sign. Night-lights — the more temporally stable of the two proxies on treated-only terms — show no confirmed absolute increase under either window, yet show a significant treated-versus-control gap in both windows once measured against the corrected control group (Section 4.6), a gap driven by control-village decline rather than treated-village increase, and weaker in the full-year window once specification and baseline-imbalance caveats are taken into account. Comparing expenditure directly against outcome (Section 4.4), a tenfold difference in investment did not correspond to a tenfold difference in measured change.

The summer-matched NDBI gain nonetheless survives every stress test applied in this study: a comparison against a matched control group in districts not themselves treated by VVP-I, a buffer-radius sweep confirming it is not an artifact of the specific 500 m buffer used elsewhere, and a Holm–Bonferroni correction for multiple testing. It does not, however, confirm the steady, sustained growth VVP-I's own framing would predict. The three-point trend extension (Section 4.7) shows the 2021–2025 change concentrated in the later half of the window (2023–2025), consistent with a late-window acceleration rather than continuous development since sanction, though the data cannot determine whether the earlier (2021–2023) period reflects weather variation or a genuinely slower start. The control-group comparison strengthens the case that the surviving signal is specific to VVP-I priority villages rather than a regional trend, but the baseline-imbalance check (Section 4.6) shows treated and control villages differ significantly at the 2021 starting point in three of four outcome/window combinations, meaning the difference-in-differences estimate should be read as a control-group-adjusted comparison rather than a fully clean natural experiment — a caveat that qualifies, but does not by itself invalidate, the estimated effect.

Combined with a stable null result for border proximity and an unstable, window-dependent result for night-lights, the evidence does not support a confident claim that VVP-I's investment has produced development at the scale the sanctioned budget implies, nor that development has been prioritized by border proximity rather than developmental need. What the evidence does support, once checked against a control group and a buffer-radius sweep, is a real increase in built-up area at priority villages relative to before the programme — concentrated in the more recent half of the study period rather than sustained since sanction — alongside the continued absence of any official impact assessment to independently corroborate this pattern. A programme of this scale and strategic significance has not been evaluated independently; the additional nuance introduced by this study's robustness checks is offered as a reason that gap matters, not as a way of avoiding a conclusion.

## 6. Limitations

### 6.1 Village Coverage Gaps

Ladakh's 35 sanctioned villages are excluded entirely from village-level analysis, since no publicly indexed source reports their names; closing this gap would require a Right to Information (RTI) request not pursued within this study's scope. Himachal Pradesh is represented only by an illustrative sample of 7 of 51 inhabited priority villages and is excluded from the core statistical sample. The block-level assignment of 19 villages in Uttarakhand's Pithoragarh district remains unresolved between two candidate blocks.

### 6.2 Border Geometry as Cartographic Approximation

All border-distance figures in this study rely on the Natural Earth cartographic boundary line, a simplified representation of a Line of Actual Control whose precise alignment is not internationally agreed. These figures should be read as relative and comparative rather than authoritative.

A related point, detailed in Section 4.5, is that "distance to border/LAC" measures distance to the nearest India-related boundary segment in the underlying dataset, not specifically the China boundary. For 31 of 251 core-sample villages (12%), the nearest segment is the Bhutan, Nepal, or Myanmar boundary rather than the China/LAC boundary. This is a defensible operationalization for a general border-securitization hypothesis but not a literal LAC-proximity test for that subset, and is a further reason not to treat H3 as a clean confirmatory result in either direction, alongside its already largely null findings (Section 4.5).

### 6.3 Budget-Correlation Scope and Ecological Inference (RQ2)

Only two states provided sufficient valid data for the budget-outcome comparison, which is accordingly reported descriptively rather than confirmatively. A further limitation is a level mismatch: the comparison uses a state-level sanctioned budget figure against a village-level sampled mean, where the budget figure describes the state's entire VVP-I portfolio rather than the specific villages geocoded in this study. The comparison should be read as suggestive rather than as a like-for-like test.

### 6.4 Compositing-Window Sensitivity

The built-up-area and border-proximity findings are, at their core, sensitive to compositing-window choice rather than stable across it. This instability is reported directly, rather than resolved by selecting whichever window yields a cleaner result, and is treated as a general limitation of single-date spectral comparison in this terrain.

### 6.5 Geocoding Coverage and Selection Bias

258 of 559 villages (46%) were successfully geocoded, with a disproportionate shortfall in Arunachal Pradesh (269 of 455 villages not geocoded). Villages absent from OSM/Bhuvan records may plausibly be smaller, more remote, or less well documented administratively. To test this, a Mann-Whitney U test was conducted for Arunachal Pradesh, where population and household counts were available for the full raw village list regardless of geocoding outcome: no significant difference was found between geocoded and non-geocoded villages in population (matched mean 135.0 vs. unmatched 145.7, p = 0.310) or households (matched mean 25.8 vs. unmatched 28.8, p = 0.540). This does not rule out selection bias related to village size, but does not provide positive evidence of it. The equivalent check could not be performed for Sikkim or Uttarakhand, where the raw village lists lacked population and household fields.

### 6.6 No Ground-Truth Validation

This study relies solely on satellite-derived measures. No dated, independently confirmed record of a completed VVP-I project (such as a specific road or building, verified by an official, dated press release) was identified that could serve as a positive control for NDBI and VIIRS sensitivity at 500 m resolution. This gap is carried forward explicitly to Future Work (Section 7.3) rather than treated as resolved.

### 6.7 Baseline Imbalance in the Control-Group Comparison

The H4 comparison (Section 4.6) found that treated and control villages differ significantly at the 2021 baseline in three of four outcome/window combinations (NDBI summer; night-lights full-year and summer), with night-lights full-year the most imbalanced (p < 0.00001) and the one combination where the fixed-effects and no-fixed-effects specifications disagree on significance — a pattern consistent with, though not proof of, the fixed-effects specification partially absorbing a baseline gap the no-fixed-effects specification cannot. District fixed effects address district-level baseline differences, not village-level selection into the treated group itself, and a genuine pre-treatment placebo test could not be conducted for lack of a multi-period pre-treatment panel for the control group. The difference-in-differences estimates should accordingly be read as control-group-adjusted rather than as a fully clean natural experiment, with the full-year night-lights result treated as the more fragile of the two night-lights findings given both this imbalance and its specification-dependent significance.

### 6.8 Non-Monotonic Multi-Year Pattern

The reported 2021-versus-2025 summer NDBI increase (Section 4.7) is concentrated in the second half of a three-point extension, following a 2021-to-2023 decline, rather than representing sustained growth across the full window. This result should be read in conjunction with Section 4.7 rather than as evidence of a steady trend, and reflects a comparison made partway through a rollout that was not yet complete at either endpoint.

### 6.9 Archive-Timing Confound in the Buffer-Radius Comparison

The 250 m and 1 km buffer extractions in Section 4.8 were run at a later date than the original 500 m extraction. Because the Sentinel-2 archive continued to backfill scenes in the interim, complete data became available for 97 core-sample villages that were null at 500 m but valid at 250 m and 1 km — an archive-timing effect, not a buffer-radius effect. This is addressed by the matched-subsample comparison in Section 4.8, though a fully clean re-extraction would require all three radii to be extracted on the same date.

## 7. Future Work

The following extensions are presented separately from the Discussion and Limitations sections to distinguish work completed within this study from work that remains open.

### 7.1 SAR-Based Change Detection

Sentinel-1 synthetic aperture radar (SAR) backscatter or coherence change is unaffected by cloud cover and the optical snow-contamination confound that motivated this study's compositing-window check. SAR would not by itself resolve the disagreement between the full-year and summer-matched optical results, but would provide an independent third measurement unaffected by either artifact, potentially clarifying which optical window is more reliable.

### 7.2 Building-Footprint or Sub-500 m Structural Analysis

The 500 m NDBI buffer aggregates built-up surface, bare rock, agricultural land, and natural vegetation into a single value, a coarse proxy for village-level investment in specific roads, buildings, or small installations. Structure-level detection using high-resolution optical imagery (e.g., PlanetScope) or open building-footprint datasets could substitute for this area-averaged index.

### 7.3 Ground-Truth Positive-Control Validation

No dated, independently verified completed VVP-I project was identified within the 258-village geocoding sample (Section 6.6). Identifying one or more such projects from a specific, dated press release or news report, and testing whether the corresponding village's NDBI/VIIRS signal shows a detectable change, would directly validate the assumptions underlying this study's satellite-based approach.

### 7.4 RTI Follow-Through for Himachal Pradesh and Ladakh

This study deliberately did not pursue RTI requests for the missing village-wise annexures for Himachal Pradesh and Ladakh (documented in the accompanying development log). Pursuing these requests would close the two largest known primary-source gaps in this study's coverage.

### 7.5 A Genuine Pre-Treatment Panel for the Control Group

The control-group comparison (Sections 3.7, 4.6, 6.7) lacks a multi-period pre-treatment panel, precluding a genuine parallel-pre-trends placebo test. Extracting 2019 and 2020 values for the 735 control villages, and ideally for the treated sample as well, would close this gap directly.

## 8. Conclusion

This study cannot confidently conclude that the pace of development implied by VVP-I's sanctioned budget, or the sustained annual progress the programme's framing anticipates, has been achieved at priority villages across India's five border states and union territories. This is not a finding of no evidence: the one indicator showing a large increase does so in only one of two defensible measurement windows, and the more temporally stable indicator shows no absolute increase of its own under either window, while nonetheless showing a positive gap relative to a control group in both — a gap driven by control-group decline rather than treated-village increase. The surviving NDBI finding is corroborated by three independent checks: a district-fixed-effects comparison against 735 district-matched non-VVP villages, a buffer-radius sweep confirming it is not an artifact of a single 500 m radius, and a three-point 2021/2023/2025 extension showing the change concentrated in a 2023–2025 recovery rather than sustained growth since sanction. A roughly tenfold difference in sanctioned budget across the two states with comparable data corresponded to no comparable difference in measured outcome. Given the scale and strategic framing of this programme, its continuation without the independent impact assessment that the parliamentary record confirms has never been conducted warrants scrutiny; any future assessment should apply the same standard used here — multiple compositing windows, a control group, and a multi-year comparison — rather than relying on whichever single-window, single-year, uncontrolled result is most convenient to report.

## References

[1] J. D. Angrist and J.-S. Pischke. 2009. *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press, Princeton, NJ.

[2] B. Buzan, O. Wæver, and J. de Wilde. 1998. *Security: A New Framework for Analysis*. Lynne Rienner Publishers, Boulder, CO.

[3] C. D. Elvidge, K. Baugh, M. Zhizhin, F. C. Hsu, and T. Ghosh. 2017. VIIRS night-time lights. *International Journal of Remote Sensing* 38, 21 (2017), 5860–5879. https://doi.org/10.1080/01431161.2017.1342050

[4] Ministry of Home Affairs. 2023. *Rajya Sabha Unstarred Question No. 2321: Vibrant Villages Programme*. Government of India, New Delhi. Reply dated 9 August 2023.

[5] Ministry of Home Affairs. 2023. *Lok Sabha Question No. 2104: Vibrant Villages Programme*. Government of India, New Delhi.

[6] Ministry of Home Affairs. 2025. *Rajya Sabha Question No. 401: Vibrant Villages Programme*. Government of India, New Delhi.

[7] Ministry of Home Affairs. 2025. *Lok Sabha Question No. 4360: Vibrant Villages Programme*. Government of India, New Delhi.

[8] Ministry of Home Affairs. 2026. *Lok Sabha Unstarred Question No. 508: Vibrant Villages Programme*. Government of India, New Delhi. Reply dated 3 February 2026.

[9] Natural Earth. 2024. *1:10m Cultural Vectors — Admin 0 Boundary Lines*. https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-boundary-lines/

[10] OpenStreetMap Contributors. 2024. *Overpass API*. https://overpass-api.de/

[11] C. Spearman. 1904. The proof and measurement of association between two things. *American Journal of Psychology* 15, 1 (1904), 72–101. https://doi.org/10.2307/1412159

[12] F. Wilcoxon. 1945. Individual comparisons by ranking methods. *Biometrics Bulletin* 1, 6 (1945), 80–83. https://doi.org/10.2307/3001968

[13] Y. Zha, J. Gao, and S. Ni. 2003. Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. *International Journal of Remote Sensing* 24, 3 (2003), 583–594. https://doi.org/10.1080/01431160304987

---

*Note to author (remove before submission): this file is a JOSIS-targeted reformatting of `BO_Research_Paper.md`, prepared to satisfy JOSIS submission guideline 2 (word-limit, ACM-numeric-citation, and structural requirements) without editing the original narrative-style paper, per your instruction. Figure image references were converted to bracketed captions since JOSIS submissions are prepared in the journal's LaTeX/Word template rather than Markdown with embedded relative image paths — you will need to re-insert the actual figures (`outputs/figures/01_ndbi_change_distribution.png` through `10_buffer_sensitivity.png`) into whichever template file you build from this content. See the accompanying chat message for the two other JOSIS checklist items (3 and 4) that need your direct attention before submission, independent of this formatting fix.*
