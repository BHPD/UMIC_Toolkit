<#
.SYNOPSIS
    Build the UMIC Toolkit .exe locally for debugging (not used by CI).

.DESCRIPTION
    Uses a throwaway virtual environment and output folders in %TEMP%, so nothing
    is written to the repository (apart from the git-ignored *.egg-info folder
    of the editable install). The venv is reused between runs and is only
    reinstalled when requirements*.txt or pyproject.toml change, or with
    -Reinstall. Use -Upgrade to pull in newer package versions.

    The build uses the same requirements and build.spec as the release
    workflow (.github/workflows/release.yml), named "UMIC Toolkit debug".

.EXAMPLE
    .\_testing\build_exe_debug.ps1              # build
    .\_testing\build_exe_debug.ps1 -Run         # build, then run the exe in this console
    .\_testing\build_exe_debug.ps1 -RunOnly     # run the last build without rebuilding
    .\_testing\build_exe_debug.ps1 -Upgrade     # upgrade packages to the latest allowed versions
    .\_testing\build_exe_debug.ps1 -Python 3.12 -Reinstall
    .\_testing\build_exe_debug.ps1 -Cleanup     # remove venv and build output
#>
param(
    [string]$Python = "",          # e.g. "3.12"; default: newest installed Python >= 3.12
    [switch]$Run,                  # run the exe after building
    [switch]$RunOnly,              # only run the previous build
    [switch]$Reinstall,            # recreate the venv
    [switch]$Upgrade,              # upgrade packages in the existing venv
    [switch]$DebugLog,             # PyInstaller --log-level DEBUG
    [switch]$Cleanup               # delete venv + build output and exit
)

$ErrorActionPreference = "Stop"
$repo     = Split-Path -Parent $PSScriptRoot
$root     = Join-Path $env:TEMP "umic-toolkit-debug-build"
$venv     = Join-Path $root "venv"
$workPath = Join-Path $root "build"
$distPath = Join-Path $root "dist"
$name     = "UMIC Toolkit debug"
$exe      = Join-Path $distPath "$name\$name.exe"

function Run-Exe {
    if (-not (Test-Path $exe)) { throw "No build found at: $exe" }
    Write-Host "`n=== Running $exe (close the window to return) ===" -ForegroundColor Cyan
    # Run in this console so print output and tracebacks from the frozen app are visible
    & $exe
    Write-Host "Exit code: $LASTEXITCODE"
}

# --- Lock: only one run at a time (they share the venv and output folders) ---
New-Item -ItemType Directory -Force $root | Out-Null
try {
    $lock = [IO.File]::Open((Join-Path $root "build.lock"), 'OpenOrCreate', 'ReadWrite', 'None')
} catch {
    throw "Another build_exe_debug.ps1 run is using $root. Wait for it to finish and try again."
}
try {  # released in the finally block at the end of the script

if ($Cleanup) {
    $lock.Dispose(); $lock = $null
    Remove-Item -Recurse -Force $root
    Write-Host "Removed $root"
    return
}
if ($RunOnly) { Run-Exe; return }

# --- Python environment -----------------------------------------------------
$reqFiles = @("requirements.txt", "requirements-build.txt") | ForEach-Object { Join-Path $repo $_ }
$reqHash  = ($reqFiles + (Join-Path $repo "pyproject.toml") | ForEach-Object { (Get-FileHash $_).Hash }) -join ""
$hashFile = Join-Path $venv "requirements.hash"
$venvPy   = Join-Path $venv "Scripts\python.exe"

$needInstall = $Reinstall -or -not (Test-Path $venvPy) -or
               -not (Test-Path $hashFile) -or ((Get-Content $hashFile -Raw).Trim() -ne $reqHash)

if ($needInstall) {
    if (Test-Path $venv) { Remove-Item -Recurse -Force $venv }
    $pyArgs = if ($Python) { @("-$Python") } else { @() }
    Write-Host "=== Creating venv in $venv ===" -ForegroundColor Cyan
    & py @pyArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
    if ($LASTEXITCODE -ne 0) { throw "Python 3.12 or newer is required (use -Python 3.12)." }
    & py @pyArgs -m venv $venv
    & $venvPy -m pip install --upgrade pip --quiet
}
if ($needInstall -or $Upgrade) {
    Write-Host "=== Installing requirements ===" -ForegroundColor Cyan
    # requirements.txt contains "-e .", which pip resolves relative to the current folder
    Push-Location $repo
    try {
        $pipArgs = @("-m", "pip", "install", "-r", $reqFiles[0], "-r", $reqFiles[1])
        if ($Upgrade) { $pipArgs += "--upgrade" }
        & $venvPy @pipArgs
        if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
    } finally { Pop-Location }
    Set-Content -Path $hashFile -Value $reqHash
} else {
    Write-Host "=== Reusing venv $venv (requirements unchanged; -Upgrade for newer versions) ===" -ForegroundColor Cyan
}
& $venvPy --version

# --- Same import check as the release workflow ------------------------------
Push-Location $repo
try {
    & $venvPy -c "import importlib, main; [getattr(importlib.import_module(m), c) for _, m, c, _ in main.MODULES]; print('modules OK')"
    if ($LASTEXITCODE -ne 0) { throw "Module import check failed" }

    # --- Build ----------------------------------------------------------------
    Write-Host "`n=== Building with PyInstaller (takes a few minutes) ===" -ForegroundColor Cyan
    $env:UMIC_VERSION = "debug"
    $pyiArgs = @("build.spec", "--clean", "--noconfirm", "--workpath", $workPath, "--distpath", $distPath)
    if ($DebugLog) { $pyiArgs += @("--log-level", "DEBUG") }
    $sw = [Diagnostics.Stopwatch]::StartNew()
    & (Join-Path $venv "Scripts\pyinstaller.exe") @pyiArgs
    $buildExit = $LASTEXITCODE
    Remove-Item Env:UMIC_VERSION
} finally {
    Pop-Location
}
if ($buildExit -ne 0) { throw "PyInstaller failed (exit code $buildExit)" }

# --- Summary --------------------------------------------------------------
# Each label is on its own line and each path/command alone on the next, so it can be copied as-is.
$outputDir = Join-Path $distPath $name
$sizeMB = [math]::Round(((Get-ChildItem $outputDir -Recurse -File | Measure-Object Length -Sum).Sum) / 1MB)
$warn   = Join-Path $workPath "build\warn-build.txt"
Write-Host "`n=== Done in $([math]::Round($sw.Elapsed.TotalMinutes, 1)) min ===" -ForegroundColor Green
Write-Host "`nBuild folder ($sizeMB MB; this folder is what a release zips):" -ForegroundColor Cyan
Write-Host "  $outputDir"
Write-Host "Exe:" -ForegroundColor Cyan
Write-Host "  $exe"
Write-Host "Missing-module report (imports PyInstaller could not resolve; mostly optional):" -ForegroundColor Cyan
Write-Host "  $warn"

# --- Sanity check: files the app loads at runtime -----------------------------
$internal = Join-Path $distPath "$name\_internal"
$expected = [ordered]@{
    'assets\licenses.txt'                                  = 'license window'
    'third_party\GPL-3.0.txt'                              = 'bundled license texts'
    'imaging_metadata_converter\models\imaging.yaml'       = 'biomero-converter metadata model'
    'linkml_runtime\linkml_model\model\schema\types.yaml'  = 'LinkML schemas (metadata model)'
    'openslide_bin'                                        = 'OpenSlide native library'
    'rsciio\emd'                                           = 'Velox EMD reader'
}
$missing = $expected.Keys | Where-Object { -not (Test-Path (Join-Path $internal $_)) }
if ($missing) {
    Write-Host "`nWARNING: files missing from the build:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  $_  ($($expected[$_]))" -ForegroundColor Red }
} else {
    Write-Host "Runtime files: all $($expected.Count) checked files present" -ForegroundColor Green
}

if ($Run) {
    Run-Exe
} else {
    $script = $PSCommandPath
    Write-Host "`nThe exe was built but not started. Copy one of these lines into PowerShell:" -ForegroundColor Yellow
    Write-Host "Run the exe in this console (errors stay visible):" -ForegroundColor Cyan
    Write-Host "  & `"$exe`""
    Write-Host "Same, through this script (works from any folder):" -ForegroundColor Cyan
    Write-Host "  & `"$script`" -RunOnly"
    Write-Host "Open the build folder in Explorer:" -ForegroundColor Cyan
    Write-Host "  explorer `"$outputDir`""
    Write-Host "Open the missing-module report:" -ForegroundColor Cyan
    Write-Host "  notepad `"$warn`""
}

} finally {
    if ($lock) { $lock.Dispose() }
}
