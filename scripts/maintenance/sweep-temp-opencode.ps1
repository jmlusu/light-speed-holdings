<#
.SYNOPSIS
    Temp sweeper for AppData\Local\Temp\opencode (7-day cutoff; dry-run default).

.DESCRIPTION
    Deletes contents older than 7 days (baseline: 31,217 files, only 228 fresh).
    Never deletes the directory itself or files open by a running OpenCode
    (locked files are logged + retried next run). Schedule weekly after first run.

.EXAMPLE
    pwsh -File scripts/maintenance/sweep-temp-opencode.ps1

.EXAMPLE
    pwsh -File scripts/maintenance/sweep-temp-opencode.ps1 -Apply
#>
param(
    [switch]$Apply,
    [int]$KeepDays = 7,
    [string]$Root = "$env:LOCALAPPDATA\Temp\opencode"
)

$ErrorActionPreference = "Continue"

if (-not (Test-Path -LiteralPath $Root)) {
    Write-Output "Temp dir not found: $Root"; exit 0
}
$cutoff = (Get-Date).AddDays(-$KeepDays)
$all = Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue | Sort-Object FullName
$stale = $all | Where-Object { $_.LastWriteTime -lt $cutoff }
$staleBytes = ($stale | Measure-Object Length -Sum).Sum
Write-Output ("total={0} stale={1} staleBytes={2}" -f $all.Count, $stale.Count, $staleBytes)

if (-not $Apply) {
    Write-Output "DRY-RUN. Re-run with -Apply to delete."
    exit 0
}
foreach ($file in $stale) {
    try {
        Remove-Item -LiteralPath $file.FullName -Force -ErrorAction Stop
    } catch {
        Write-Output "SKIPPED (locked): $($file.FullName) - $($_.Exception.Message)"
    }
}
Write-Output "Sweep complete."
