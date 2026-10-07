# BORDER_OPTICS — Deep Project Audit

**Scope:** every file in the project — all code under `src/` and `pages/`, `app.py`, `utils/`, `tests/`, every output file under `outputs/` and `data/processed/`, every figure/map, every documentation file (`README.md`, `DATA_DICTIONARY.md`, `ANALYSIS_FREEZE.md`, `BO_Executive_Summary.md`, `FIELD_VERIFICATION_SHORTLIST.md/.csv`, `CITATION.cff`, the RTI draft), and every reference link in `BO_Research_Paper.md`.

**Method:** staged the entire project from your device, re-ran the actual analysis scripts and reproduced their numbers independently (not just read the code), traced roughly 180 individual statistics in the paper back to the output file each one should come from, viewed every figure and compared it against its caption, and fetched every reference URL. `tests/test_data_integrity.py` (12 automated checks) passes on your current data.

This report only lists things that are **currently** wrong, inconsistent, or unverifiable — nothing about future additions.

---

## A. Confirmed problems — worth fixing

**A1. Wrong number in the paper's own history note (§4.6).**
The paper says the pre-fix control list had "**753 villages... 106 duplicate coordinate rows**... giving Entry 22's 735 village list." But `753 − 106 = 647`, not 735 — the arithmetic doesn't even work. Your own `BO_Development_Log.md` (line 736) says the real number was **18** duplicates: "a new 735-village list (**753 minus 18 cross-district duplicates**)." `753 − 18 = 735` checks out. The paper's "106" appears to be a mixed-up figure from a later, different fix round. Nowhere in the dev log does "106" appear at all.

**A2. Moran's I p-value in the paper doesn't match the project's own script output (§6.10 table, §6.11 text).**
Paper: "full year lights change... I = 0.076... p = 0.004." Your own `outputs/spatial_moran_h3_correction_results.json` reproduces **p = 0.003**, deterministically, from `spatial_moran_and_h3_correction.py` — and that JSON file literally has a self-check block already flagging this exact mismatch (`"published_claim": "§6.11 claims I=0.076, p=0.004"` vs `"reproduced_p": 0.003`). Two more numbers in the same sentence are also off: summer NDBI's permutation null mean is stated as −0.002, actual is −0.0042; full-year lights' SD is stated as 0.020, actual is 0.0183. Side note: `pages/8_Methodology_Limitations.py` (line 205) already has the **correct** 0.003 — only the paper text and its §6.10 table entry need fixing.

**A3. Abstract double-counts Himachal Pradesh.**
Abstract: "...at **258** individually geocoded villages across three core states (Arunachal Pradesh, Sikkim, Uttarakhand)... an illustrative sample of **7** villages in Himachal Pradesh." As worded, this reads like 258 belongs to the three-state group. It doesn't — 258 is the four-state total (251 in the three core states + 7 in HP). §3.1 and §4.1 both correctly say the three-state core sample is 251. The Abstract needs rewording so 258 isn't attached only to "three core states."

**A4. Figure 5 (`outputs/figures/02_state_change_vs_budget.png`) is missing Sikkim.**
The text right next to it (§4.4) says "All three core states have valid summer window NDBI coverage now" and gives Sikkim's number (−0.0347). The actual chart only has two bars — **Arunachal Pradesh and Uttarakhand**. Sikkim isn't plotted at all. This chart looks like it was never regenerated after the Sikkim data fix.

**A5. Figure 6 (`outputs/figures/03_h3_border_distance_vs_lights.png`) is missing NDBI entirely.**
Caption says "Distance to border versus **NDBI change and night lights change**, both compositing windows" — four results. The actual image only has two panels, and **both are night-lights**, not NDBI. The filename itself (`..._vs_lights.png`) confirms it was built lights-only, then captioned as if it covered both.

**A6. Ground-truth SAR number is slightly overstated (§4.10).**
Paper: SAR shows "no clear signal either way at any of the three [case-study] villages (**changes under 0.15 dB**...)." Checked directly against `data/processed/border_optics_treated_sar_fullyear.csv`: Kaho's VH change is **0.192 dB**, above the stated 0.15 dB bound (the other five of six VV/VH values across the three villages are indeed under 0.15 dB — only this one isn't).

**A7. Kaho/Walong hostel mixed up, in two places.**
`BO_Executive_Summary.md` and `pages/8_Methodology_Limitations.py` (line 295) both say "**a hostel at Kaho**." Your own paper (§6.6, §7.2, §7.3) is specific: the 30-bed girls' hostel is at **Walong** (along with the terminal building); Kaho's confirmed projects are a basketball court, solar lights, and a school library.

**A8. `pages/2_Theoretical_Foundations.py` (live dashboard) describes a resolved problem as still ongoing.**
It currently says monsoon cloud "eliminated nearly all valid observations for Sikkim in that window," producing "an unstable, composite-window-dependent change estimate." This contradicts the paper (§4.2/§6.4: both windows now agree, both null, no longer window-sensitive) **and** contradicts two other pages in the same dashboard — `pages/6_Explore_Trends.py` and `pages/8_Methodology_Limitations.py` — which both correctly say this was resolved by the Entry 21–22 re-extraction.

**A9. `pages/8_Methodology_Limitations.py` says two checks are still open that your paper says are done.**
Dashboard: "Two checks from the original plan remain open: whether either correlation is linear... and a cross-check against the three-point 2021/2023/2025 extraction." Paper §7.6: "...are **both done now too** (Development Log Entry 27)," with full results given. The dashboard page wasn't updated after Entry 27.

**A10. ~30% of your control villages never had their district membership verified.**
`select_control_villages.py`'s district-boundary lookup (`fetch_district_polygon`) has no retry logic and silently returns `None` on any failure, falling back to a rough ~65km bounding-box match instead of a real administrative-boundary check. Right now, in your committed `border_optics_control_villages.csv`, **219 of 732 control villages (~30%) have `district_verified = False`** — all of them concentrated in exactly three districts: Tawang (AP, 78 rows), North district (Sikkim, 93 rows), and Pithoragarh (UK, 48 rows). One likely cause for Sikkim specifically: your treated-village data's district field there is the bare string `"North"`, which is an ambiguous place-name lookup. This matters because your whole control-group DiD design (§3.7/§4.6) is built on district fixed effects and clustering standard errors by district — an unverified district label for a third of the control group is a real, currently undocumented data-quality gap (it isn't mentioned in the dev log, `ANALYSIS_FREEZE.md`, or `DATA_DICTIONARY.md` beyond noting the column exists).

**A11. `DATA_DICTIONARY.md` has several concrete inaccuracies against the actual files:**
- Says "8 of 10 districts show a positive gap" — your study uses **14** districts throughout, never 10; this is a leftover reference to a robustness-check description that doesn't match anything currently in the paper.
- Claims the summer-matched treated files carry a generic `before_image_count`/`after_image_count` column pair — the real files only have the per-metric versions (`ndbi_before_image_count` etc.); the generic pair doesn't exist there.
- `border_optics_control_villages.csv`'s actual `district_verified` column (see A10) isn't listed in its column table at all, even though other sections reference "the same meaning as in `border_optics_control_villages.csv`" for a meaning that's never actually given.
- The DiD panel files (`border_optics_did_panel_fullyear/summer.csv`) actually also contain `district` and `state` columns that aren't documented.
- Says the multi-year files have "one row per core-sample village" — they actually have **258** rows (251 core + 7 Himachal), not just the core sample.
- Says the multiyear-slopes files have "same rows" as the multiyear files — the slopes files actually drop Himachal, leaving **251** rows, not 258.
- Says the 250m/1000m buffer files have "same columns as" `border_optics_village_results_summer_analyzed.csv` — the buffer files are missing the `ndbi_change`/`lights_change` columns that file has.

**A12. Stale code comment in `extended_robustness_checks.py` contradicts its own output.**
A comment and a printed line still say the full-year night-lights control-group DiD is "the only control-group result still significant after Entry 22." That's no longer true — Entry 25 sent that exact result to null, and your dev log documents the reversal in detail. The saved numeric output is correctly null; only the script's own narration text is stale.

**A13. Three parliamentary reference links go to a dead-end search page, not the cited document.**
The reference-list entries for Lok Sabha Q. 2104, Rajya Sabha Q. 401, and Lok Sabha Q. 4360 all link to `sansad.in/ls/questions/questions-and-answers` (or `/rs/`) — a bare search form with no way to land on the cited question from the link alone. Your other two parliamentary citations (RS 2321, LS 508) link straight to the specific PDF. For LS 2104 specifically, the real direct PDF was found and confirmed: `https://www.mha.gov.in/MHA1/Par2017/pdfs/par2023-pdfs/LS14032023/2104.pdf` (dated 14 March 2023, confirms the "Himachal Pradesh – 75 villages" figure your paper cites from it).

**A14. `FIELD_VERIFICATION_SHORTLIST.md`/`.csv` is stale — and this is the one document meant to drive real phone/field verification.**
- It still excludes Sikkim from ranking because "the summer-matched window has zero usable images for every Sikkim village" — that was true before Entry 22, not now (Sikkim has valid summer data for all 31 villages, matching the paper's −0.0347 figure).
- Its top-3 villages/values for Arunachal Pradesh and Uttarakhand don't match your current summer-window data at all — e.g. it lists "Ramu (+0.131), Katuk (+0.112), Nisuk (+0.105)" for AP, but the current data's actual top 3 are **Passik (+0.085), Pagam (+0.079), Ramu (+0.078)** — none of the listed values are even close.
- For Himachal Pradesh, the third-ranked village is even wrong in **sign**: the shortlist says "Chango (+0.004)," current data shows Chango at **−0.013**.
This is an operational document — someone could end up calling or visiting the wrong village based on it.

**A15. `ANALYSIS_FREEZE.md` contradicts itself on the git commit hash, and the hash is wrong anyway.**
It says: "Left blank here deliberately... this file was written from a working copy without direct git access to confirm the exact current hash" — then immediately gives a hash (`a1bfe9e...`) right below that sentence. That hash also doesn't match your repository's actual current `main` branch tip (`ebab143...`). Separately, the file's own header freeze-date (2026-09-13) was never bumped even though item 10 in the same file, and Dev Log Entry 35, both describe edits made to this file after that date.

---

## B. Lower-confidence — worth a manual second look

**B1.** Independently recomputing the pre-fix (735-village) control list's coordinate-duplicate count gives **21** duplicates implicating **22** treated villages — one more than the paper's stated "20 duplicates / 21 treated villages" (§4.6). Flagged as lower-confidence only because it depends on exactly replicating a historical, live-Overpass-API-based run rather than a static file; still, it's off by exactly one in a specific, re-checkable count and worth confirming by hand.

**B2.** Minor: `scl_vs_qa60_comparison.py`'s console print says "n/**258** villages" when the population actually being compared is the 251-village core sample. Doesn't affect the saved JSON (correctly 251/251) — just the printed message.

---

## C. Checked and ruled out (false leads — nothing to fix)

- One pass of this audit initially flagged seven "orphaned" old-numbered Streamlit page files (e.g. an old `pages/1_Theoretical_Foundations.py`, `4_Statistical_Validation.py` with stale "753 villages" text) as duplicate sidebar entries. **I double-checked your actual device directly — these do not exist in `D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\BORDER_OPTICS\pages\`.** Your `pages/` folder on disk has exactly the 8 correctly-numbered files it should. Those old-named files were leftover copies sitting only in my own cloud workspace from an earlier session, not real files in your project — false alarm, nothing to do here.

---

## D. Checked and found solid (no issues)

- **Core statistics code**: `did_model.py`'s DiD specification (treatment×post term correctly isolated, district FE, clustered SEs), the wild cluster bootstrap (genuinely exhaustive 2^14 = 16,384 sign-flip enumeration, not a random sample), Holm–Bonferroni (correct family of exactly 8 p-values), the Moran's I formula itself, the power-analysis degrees-of-freedom (250 for H1, 13 for H4), the placebo test's 2019→2021 window, and the randomization-inference/leave-one-out procedures — all correctly implemented, reproduced independently to match `statsmodels` and the saved output files.
- **~180 individual statistics** traced from the paper to their source output files — the overwhelming majority matched exactly or within ordinary rounding; the only real mismatches found are A1, A2, A6, and B1 above.
- **Acquisition-pipeline bug fixes** your dev log claims (the Sikkim same-day re-extraction, the control-village 50m + official-name-list dedup logic itself, the SCL snow-class fix) are all genuinely and correctly implemented in the current code — independently re-verified, not just taken on the dev log's word (aside from the district-verification gap in A10, which is a separate, still-open data-quality issue within that same pipeline).
- **Citations**: LS Unstarred Question No. 508 (fetched directly — confirmed word-for-word, including the "No impact assessment has been carried out" reply) and LS Question No. 2104 (fetched directly — confirmed) check out exactly. Zha et al. 2003, Elvidge et al. 2017, Wilcoxon 1945, Spearman 1904, Dutilleul 1993, Angrist & Pischke, and the Natural Earth dataset link all check out.
- **10 of the 12 numbered figures**, plus all 5 static map renders, visually match their captions and the surrounding paper text correctly (only Figures 5 and 6 — A4/A5 above — don't).
