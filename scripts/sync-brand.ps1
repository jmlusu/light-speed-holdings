<#
.SYNOPSIS
    Sync canonical brand assets (brand/**) into runtime/web mirrors
    (static/brand/** and public/brand/**). Copy-overlay only; never deletes.

.DESCRIPTION
    brand/ at the repo root is the single source of truth. This script copies
    the canonical subdirectories (tokens, guidelines, logos, print, digital)
    into the two deployment mirrors. Mirror-only content (static/brand/templates,
    static/brand/social, static/brand/BRAND_GUIDELINES.md, public/brand/... ) is
    preserved.

.PARAMETER DryRun
    Preview which files would be copied without writing anything.
#>
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$canonical = Join-Path $root "brand"
$mirrors = @(
    (Join-Path $root "static\brand"),
    (Join-Path $root "public\brand")
)

# Subdirectories that have a canonical source and should exist in every mirror.
$syncDirs = @("tokens", "guidelines", "logos", "print", "digital")

if (-not (Test-Path -LiteralPath $canonical)) {
    throw "Canonical brand directory not found: $canonical"
}

$applied = 0
$skipped = 0

foreach ($mirror in $mirrors) {
    if (-not (Test-Path -LiteralPath $mirror)) {
        Write-Host "Mirror missing, creating: $mirror"
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $mirror -Force | Out-Null
        }
    }

    foreach ($dir in $syncDirs) {
        $src = Join-Path $canonical $dir
        if (-not (Test-Path -LiteralPath $src)) {
            continue
        }
        $dst = Join-Path $mirror $dir
        $count = (Get-ChildItem -LiteralPath $src -Recurse -File).Count
        Write-Host ("{0} {1} -> {2} ({3} files)" -f $(if ($DryRun) { "[dry-run]" } else { "[copy]" }), $src, $dst, $count)
        if (-not $DryRun) {
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
        }
        $applied += $count
    }
}

Write-Host ""
Write-Host "Sync complete. files copied: $applied  ($(if ($DryRun) { 'nothing written' } else { 'mirrors updated' }))"
