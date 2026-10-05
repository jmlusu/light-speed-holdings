<#
.SYNOPSIS
    Sync canonical brand assets (brand/**) into runtime/web mirrors
    (static/brand/** and public/brand/**). Copy-overlay; -Prune deletes
    mirror-only-in-sync-dir files; -Verify reports drift. Never touches
    mirror-only paths (static/brand/templates, static/brand/social,
    mirror-only top-level files).

.DESCRIPTION
    brand/ at the repo root is the single source of truth. This script copies
    the canonical subdirectories (logo, tokens, guidelines, logos, print, digital)
    into the two deployment mirrors. Mirror-only content (static/brand/templates,
    static/brand/social, static/brand/BRAND_GUIDELINES.md, public/brand/... )
    is preserved.

.PARAMETER DryRun
    Preview prune/copy without writing anything.

.PARAMETER Prune
    Delete files in the six sync directories that do not exist in canonical
    (removes drift and historic nested-copy damage).

.PARAMETER Verify
    Hash-compare every canonical sync-dir file against both mirrors and
    report drift + any nested duplicate directories. Exits 1 on drift.
#>
param(
    [switch]$DryRun,
    [switch]$Prune,
    [switch]$Verify
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$canonical = Join-Path $root "brand"
$mirrors = @(
    (Join-Path $root "static\brand"),
    (Join-Path $root "public\brand")
)

# Subdirectories that have a canonical source and should exist in every mirror.
# "logo" = new canonical logo system (Directive §6); "logos" = legacy suite.
$syncDirs = @("logo", "tokens", "guidelines", "logos", "print", "digital")

# Mirror-only content that prune must never delete.
$mirrorOnly = @("templates", "social")

if (-not (Test-Path -LiteralPath $canonical)) {
    throw "Canonical brand directory not found: $canonical"
}

function Get-FileHashSafe([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
}

$applied = 0
$pruned = 0
$drift = @()
$nested = @()

if ($Verify) {
    foreach ($mirror in $mirrors) {
        if (-not (Test-Path -LiteralPath $mirror)) {
            $drift += "MISSING MIRROR: $mirror"
            continue
        }
        # Nested duplicate dirs: dir name == parent name (historic Copy-Item bug).
        $nested += Get-ChildItem -LiteralPath $mirror -Directory -Recurse |
            Where-Object { $_.Name -eq $_.Parent.Name } |
            Sort-Object FullName |
            ForEach-Object { $_.FullName }
        foreach ($dir in $syncDirs) {
            $src = Join-Path $canonical $dir
            if (-not (Test-Path -LiteralPath $src)) { continue }
            $dst = Join-Path $mirror $dir
            foreach ($file in (Get-ChildItem -LiteralPath $src -Recurse -File | Sort-Object FullName)) {
                $rel = $file.FullName.Substring($src.Length)
                $mirrorFile = Join-Path $dst $rel
                if (-not (Test-Path -LiteralPath $mirrorFile)) {
                    $drift += "MISSING: $dst$rel"
                } elseif ((Get-FileHashSafe $file.FullName) -ne (Get-FileHashSafe $mirrorFile)) {
                    $drift += "DRIFT: $dst$rel"
                }
            }
        }
    }
    if ($nested.Count) {
        Write-Host "NESTED DUPLICATES:"
        $nested | ForEach-Object { Write-Host "  $_" }
    }
    if ($drift.Count) {
        $drift | ForEach-Object { Write-Host $_ }
        Write-Host "Verify FAILED: $($drift.Count) problem(s)."
        exit 1
    }
    Write-Host "Verify OK: mirrors match canonical ($($syncDirs -join ', ')); no nested dirs."
    exit 0
}

foreach ($mirror in $mirrors) {
    if (-not (Test-Path -LiteralPath $mirror)) {
        Write-Host "Mirror missing, creating: $mirror"
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $mirror -Force | Out-Null
        }
    }

    if ($Prune) {
        # Remove nested duplicates first (historic bug: Copy-Item merged src dir
        # into existing dst, creating dst/<dir>/<dir>).
        $nestedDirs = Get-ChildItem -LiteralPath $mirror -Directory -Recurse |
            Where-Object { $_.Name -eq $_.Parent.Name -and $syncDirs -contains $_.Name } |
            Sort-Object FullName
        foreach ($d in $nestedDirs) {
            Write-Host "[prune] nested: $($d.FullName)"
            if (-not $DryRun) { Remove-Item -LiteralPath $d.FullName -Recurse -Force }
            $pruned++
        }
        foreach ($dir in $syncDirs) {
            $dst = Join-Path $mirror $dir
            if (-not (Test-Path -LiteralPath $dst)) { continue }
            $src = Join-Path $canonical $dir
            $canonicalFiles = @()
            if (Test-Path -LiteralPath $src) {
                $canonicalFiles = Get-ChildItem -LiteralPath $src -Recurse -File |
                    ForEach-Object { $_.FullName.Substring($src.Length) }
            }
            $extra = Get-ChildItem -LiteralPath $dst -Recurse -File |
                Where-Object { $canonicalFiles -notcontains $_.FullName.Substring($dst.Length) } |
                Sort-Object FullName
            foreach ($f in $extra) {
                Write-Host "[prune] $($f.FullName)"
                if (-not $DryRun) { Remove-Item -LiteralPath $f.FullName -Force }
                $pruned++
            }
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
            # Copy CONTENTS, not the dir itself: copying $src into an existing
            # $dst nests it as $dst/<dir>/<dir>.
            if (-not (Test-Path -LiteralPath $dst)) {
                New-Item -ItemType Directory -Path $dst -Force | Out-Null
            }
            Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force
        }
        $applied += $count
    }
}

Write-Host ""
Write-Host ("Sync complete. files copied: {0}  pruned: {1}  ({2})" -f `
    $applied, $pruned, $(if ($DryRun) { 'nothing written' } else { 'mirrors updated' }))
