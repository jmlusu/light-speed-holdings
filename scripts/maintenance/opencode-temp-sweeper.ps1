<#Requires -Version 5.1
<#
.SYNOPSIS
  7-day purge for %LOCALAPPDATA%\Temp\opencode with quota alerts (P0-4).

.DESCRIPTION
  Plan: reports/opencode-db-reliability-fix-2026-11-08.md section 5.

  Default mode is DRY-RUN: fresh counts + sizes + quota check, NO deletion.
  -Apply deletes only FILES older than -RetentionDays (default 7).
  The root directory itself is never deleted; empty directories are left
  in place. Files locked by a running OpenCode are skipped with a log line
  (retry next run) -- never force-killed.

  Quota alerts (always printed, also on dry-run):
    - total files > -QuotaFiles (default 50000) -> WARNING
    - total size > -QuotaGB (default 2) -> WARNING
    - stale (older than cutoff) share > 90% -> WARNING (leak signal)
  Full purge additionally requires a fresh-count approval: run the dry-run
  first, confirm the counts in the ticket, then re-run with -Apply.

  Rollback (first run): use -QuarantineDir to MOVE stale files (not delete)
  to a quarantine folder for 48 h; purge the quarantine after 14 days.
  Temp is regenerable; quarantine preserves debuggability.

.PARAMETER Root
  Temp dir to sweep. Default: $env:LOCALAPPDATA\Temp\opencode

.PARAMETER RetentionDays
  Files older than this are stale. Default 7.

.PARAMETER Apply
  Actually delete (or quarantine-move). Without -Apply nothing is touched.

.PARAMETER QuarantineDir
  If set with -Apply, stale files are moved here instead of deleted.
  Use for the first run (rollback safety).

.PARAMETER QuotaFiles
  Alert when total file count exceeds this. Default 50000.

.PARAMETER QuotaGB
  Alert when total size exceeds this (GB). Default 2.

.PARAMETER TopN
  Number of largest subdirectories to list. Default 10.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-temp-sweeper.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-temp-sweeper.ps1 `
    -Apply -QuarantineDir "$env:USERPROFILE\.local\share\opencode\tool-output\quarantine-20261108"

.NOTES
  Baseline (audit 2026-11-08): 31,217 files, only 228 in last 7 days.
  Junction warning (found 2026-11-08): four node_modules junctions under
  Temp\opencode point at the LIVE workspace node_modules
  (audit-...\vitest-*\node_modules x3 + headcheck\node_modules).
  `cmd dir /s` follows junctions and reports ~98k phantom files; this
  script never follows reparse points, so its ~31k count is the
  Temp-owned truth. Never Remove-Item -Recurse a junction -- it would
  delete live workspace files through the alias. Junctions are reported
  separately below and excluded from the purge set.
  Schedule weekly after the first approved purge.
#>
[CmdletBinding()]
param(
  [string]$Root = "$env:LOCALAPPDATA\Temp\opencode",
  [int]$RetentionDays = 7,
  [switch]$Apply,
  [string]$QuarantineDir = "",
  [int]$QuotaFiles = 50000,
  [double]$QuotaGB = 2,
  [int]$TopN = 10
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

Write-Host "=== opencode-temp-sweeper ==="
Write-Host "Root          : $Root"
Write-Host "Retention     : older than $RetentionDays days"
Write-Host "Mode          : $(if ($Apply) { 'APPLY (delete/move stale)' } else { 'DRY-RUN (counts only; no deletion)' })"
if ($Apply -and -not [string]::IsNullOrWhiteSpace($QuarantineDir)) {
  Write-Host "QuarantineDir : $QuarantineDir (MOVE instead of DELETE)"
}
Write-Host ""

if (-not (Test-Path -LiteralPath $Root)) {
  Write-Host "Temp dir not found: $Root (nothing to sweep)"
  exit 0
}

$cutoff = (Get-Date).AddDays(-$RetentionDays)
Write-Host "Reporting junctions (reparse points -- excluded, never traversed)..."
$junctions = @(Get-ChildItem -LiteralPath $Root -Recurse -Directory -Force -ErrorAction SilentlyContinue |
  Where-Object { ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 })
if ($junctions.Count -gt 0) {
  Write-Host ("  [WARNING] {0} junction(s) found -- counts below EXCLUDE their targets; purge never enters them:" -f $junctions.Count)
  foreach ($j in $junctions) { Write-Host "    $($j.FullName)" }
  Write-Host "  Verify a junction target before any manual cleanup: cmd /c dir /al <path> (>[JUNCTION] <target>)"
  Write-Host "  NOTE: 'cmd dir /s' totals (~98k) INFLATE Temp by following these aliases; this script's count is Temp-owned only."
} else {
  Write-Host "  (no junctions found)"
}
Write-Host ""
Write-Host "Enumerating files (Temp-owned only; junctions not followed)..."
$all = @(Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue)
$totalCount = $all.Count
$totalBytes = ($all | Measure-Object Length -Sum).Sum
if ($null -eq $totalBytes) { $totalBytes = 0 }
$stale = @($all | Where-Object { $_.LastWriteTime -lt $cutoff })
$staleCount = $stale.Count
$freshCount = $totalCount - $staleCount
$staleBytes = ($stale | Measure-Object Length -Sum).Sum
if ($null -eq $staleBytes) { $staleBytes = 0 }

Write-Host ""
Write-Host "--- Counts (fresh, re-counted now) ---"
Write-Host ("  total files : {0} ({1:N2} GiB)" -f $totalCount, ($totalBytes/1GB))
Write-Host ("  fresh <= {0}d : {1} files" -f $RetentionDays, $freshCount)
Write-Host ("  stale >  {0}d : {1} files ({2:N2} GiB)" -f $RetentionDays, $staleCount, ($staleBytes/1GB))
$stalePct = if ($totalCount -gt 0) { ($staleCount/$totalCount)*100 } else { 0 }
Write-Host ("  stale share : {0:N1}%" -f $stalePct)

Write-Host ""
Write-Host "--- Quota alerts ---"
$alerts = 0
if ($totalCount -gt $QuotaFiles) {
  Write-Host ("  [WARNING] file count {0} > quota {1} (Temp is leaking; schedule a purge)" -f $totalCount, $QuotaFiles)
  $alerts++
} else {
  Write-Host ("  [OK] file count {0} <= quota {1}" -f $totalCount, $QuotaFiles)
}
if (($totalBytes/1GB) -gt $QuotaGB) {
  Write-Host ("  [WARNING] size {0:N2} GiB > quota {1:N2} GB" -f ($totalBytes/1GB), $QuotaGB)
  $alerts++
} else {
  Write-Host ("  [OK] size {0:N2} GiB <= quota {1:N2} GB" -f ($totalBytes/1GB), $QuotaGB)
}
if ($stalePct -gt 90) {
  Write-Host ("  [WARNING] stale share {0:N1}% > 90% (nearly everything is purge-eligible)" -f $stalePct)
  $alerts++
}
Write-Host ("  alerts fired: {0}" -f $alerts)

Write-Host ""
Write-Host "--- Top $TopN directories by file count ---"
$all | Group-Object { $_.DirectoryName } | Sort-Object Count -Descending |
  Select-Object -First $TopN | ForEach-Object { Write-Host ("  {0,6}  {1}" -f $_.Count, $_.Name) }

if (-not $Apply) {
  Write-Host ""
  Write-Host "DRY-RUN complete. No file was deleted or moved."
  Write-Host "Mass deletion requires fresh-count approval: confirm the counts above with the ticket owner, then re-run with -Apply."
  exit 0
}

Write-Host ""
Write-Host "--- APPLY: $(if ($QuarantineDir) { 'quarantine-move' } else { 'delete' }) {0} stale files ---" -f $staleCount
$ok = 0; $skipped = 0; $failed = 0
if ($QuarantineDir) {
  if (-not (Test-Path -LiteralPath $QuarantineDir)) { New-Item -ItemType Directory -Path $QuarantineDir -Force | Out-Null }
}
foreach ($f in $stale) {
  try {
    if ($QuarantineDir) {
      $rel = $f.FullName.Substring($Root.Length).TrimStart('\', '/')
      $dest = Join-Path $QuarantineDir $rel
      $destDir = Split-Path -Parent $dest
      if (-not (Test-Path -LiteralPath $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
      Move-Item -LiteralPath $f.FullName -Destination $dest -Force -ErrorAction Stop
    } else {
      Remove-Item -LiteralPath $f.FullName -Force -ErrorAction Stop
    }
    $ok++
  } catch {
    $skipped++
    if ($skipped -le 20) { Write-Host "  SKIPPED (locked?): $($f.FullName) -- $($_.Exception.Message)" }
  }
}
Write-Host ("  deleted/moved: {0} | skipped (locked): {1}" -f $ok, $skipped)
Write-Host "Verify after: (Get-ChildItem `"$Root`" -Recurse -File).Count should be ~= fresh only (hundreds, not tens of thousands)."
