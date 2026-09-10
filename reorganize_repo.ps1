# DOUBLE JEOPARDY -- repository folder reorganization
# Run this from PowerShell with your current directory set to the repo root
# (D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\DOUBLE_JEOPARDY). Filenames are NOT
# changed, only which folder each file lives in.

cd D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\DOUBLE_JEOPARDY

# 1. Create the new folders
New-Item -ItemType Directory -Force -Path "paper" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\acquisition" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\processing" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\analysis" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\figures" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\validation" | Out-Null
New-Item -ItemType Directory -Force -Path "scripts\local_fixes" | Out-Null

# 2. Paper / write-ups -> paper/
$paperFiles = @(
    "DJ_Research_Paper.md", "DJ_Research_Paper.pdf",
    "DJ_Research_Paper_EarthArXiv_Submission.pdf",
    "DJ_Executive_Summary.md", "DJ_Executive_Summary.pdf",
    "DJ_Development_Log.md", "DJ_Development_Log.pdf"
)
foreach ($f in $paperFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "paper\" -Force }
}

# 3. Data acquisition scripts -> scripts/acquisition/
$acquisitionFiles = @(
    "auth_sentinelhub.py",
    "download_all_island_cyclone_damage.py",
    "download_coral_bleaching_stress.py",
    "download_cyclone_damage_proxy.py",
    "download_lakshadweep_population.py",
    "download_ndbi_encroachment.py",
    "download_ndbi_encroachment_raster.py"
)
foreach ($f in $acquisitionFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "scripts\acquisition\" -Force }
}

# 4. Data cleaning / filtering / prep scripts -> scripts/processing/
$processingFiles = @(
    "clean_wdpa.py", "compute_wdpa_area.py", "consolidate_wind_speed.py",
    "export_canary_check.py", "export_settlement_elevations_full.py",
    "filter_gmw_1996.py", "filter_gmw_2010.py", "filter_gmw_mangroves.py",
    "filter_wdpa_islands.py", "normalize_wdpa.py", "precompute_elevations.py",
    "wdpa_coastal_buffer.py"
)
foreach ($f in $processingFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "scripts\processing\" -Force }
}

# 5. Core analysis scripts (the ones that produce the paper's actual numbers) -> scripts/analysis/
$analysisFiles = @(
    "analyze_ndbi_change.py", "compound_vulnerability_score.py",
    "coral_trend_test.py", "governance_correlation_test.py",
    "mangrove_3point_comparison.py", "population_weighted_exposure.py",
    "slr_exposure_analysis.py"
)
foreach ($f in $analysisFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "scripts\analysis\" -Force }
}

# 6. Map / figure generation scripts -> scripts/figures/
$figureFiles = @(
    "build_ecosystem_buffer_map.py", "build_encroachment_map.py",
    "build_interactive_plots.py", "build_slr_exposure_map.py",
    "fix_map_resize.py", "map1_slr_fiji.py", "map1_vulnerability_score.py",
    "research_paper_figures.py"
)
foreach ($f in $figureFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "scripts\figures\" -Force }
}

# 7. Debug / verify / validate scripts -> scripts/validation/
$validationFiles = @(
    "debug_bounds.py", "debug_ndbi.py", "explore_wdpa.py",
    "test_canary_coords.py", "validate_all_datasets.py",
    "verify_canary_dhw.py", "verify_canary_slr_number.py",
    "verify_normalization.py"
)
foreach ($f in $validationFiles) {
    if (Test-Path $f) { Move-Item -Path $f -Destination "scripts\validation\" -Force }
}

# 8. local_fix_scripts/ folder -> scripts/local_fixes/ (then remove the old empty folder)
if (Test-Path "local_fix_scripts") {
    Get-ChildItem "local_fix_scripts" -File | Move-Item -Destination "scripts\local_fixes\" -Force
    Remove-Item "local_fix_scripts" -Force -ErrorAction SilentlyContinue
}

# 9. Clean up Python bytecode cache (already in .gitignore, safe to delete)
if (Test-Path "__pycache__") { Remove-Item "__pycache__" -Recurse -Force }

Write-Host ""
Write-Host "Done. New top-level layout:"
Get-ChildItem -Directory | Select-Object Name
Write-Host ""
Write-Host "Files left loose at repo root (should only be README.md, LICENSE, CITATION.cff, requirements.txt, .gitignore):"
Get-ChildItem -File | Select-Object Name
