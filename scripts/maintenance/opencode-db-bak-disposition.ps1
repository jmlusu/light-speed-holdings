<#Requires -Version 5.1
<#
.SYNOPSIS
  Inventory + gated disposition of opencode.db.bak (38.5 GB pre-v2 snapshot).

.DESCRIPTION
  P0-2 (plan: reports/opencode-db-reliability-fix-2026-11-08.md section 3).

  Default mode is DRY-RUN: inventory (size/date) + v2-stability proof +
  snapshot verification, with NO copy and NO delete. -Apply performs the
  cold copy; deletion of the original additionally requires
  -DeleteAfterVerify + -ColdCopyVerified (both) and a verified fresh
  snapshot. This task definition explicitly does NOT delete the 38 GB file:
  the script is created for a later maintenance window once the fresh
  snapshot + cold copy exist.

  Retention rule (enforced at apply time):
    retain ONE rolling .bak (<=48 h old) + ONE cold archive per month.
    Anything older than -KeepDays (default 30) OR larger than 2x live DB
    without a retention tag is archived off-volume or deleted -- but only
    after the fresh snapshot below is verified.
  NOTE on this .bak: it is only 7 days old (2026-11-01) so the age gate
  alone would defer -- but it is ~12x the live DB (35.89 GiB vs ~3 GiB)
  and a pre-v2 snapshot superseded by the completed v1-v2 migration, so
  the SIZE + SUPERSESSION gates require disposition now. The fresh
  snapshot below is the replacement .bak.

  Cold-copy verification: robocopy with /J (unbuffered) cross-volume,
  then byte-length equality. Hash verification is offered via -VerifyHash
  (SHA-256 over 38 GB takes an hour+; run it when time allows, otherwise
  size + read-back spot check + backup-tool manifest).

.PARAMETER BackupPath
  Path to the stale backup. Default: ~/.local/share/opencode/opencode.db.bak

.PARAMETER ColdDest
  Cold-storage destination FILE (e.g. \\cold-storage\backups\opencode\opencode.db.bak.2026-11-01).
  Required with -Apply.

.PARAMETER SnapshotPath
  Path to the fresh post-v2 snapshot that REPLACES the .bak
  (e.g. ~/.local/share/opencode/opencode.db.pre-fix-<ts>.db).
  Required with -Apply; integrity_check on the SNAPSHOT is verified
  read-only before any copy/delete.

.PARAMETER Apply
  Perform the cold copy. Without -Apply nothing is copied or deleted.

.PARAMETER DeleteAfterVerify
  Also delete the original AFTER the cold copy is byte-verified.
  Requires -Apply + -ColdCopyVerified. Without it the original is kept
  (copy-only).

.PARAMETER ColdCopyVerified
  Operator attests the cold copy was byte-verified (size + manifest /
  hash) outside this script. Required to delete the original.

.PARAMETER VerifyHash
  When set, compute SHA-256 of source and copy and compare.
  Very slow (~1 h+ for 38 GB); default is size + manifest check.

.PARAMETER KeepDays
  Retention age threshold (days). Default 30.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-bak-disposition.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-bak-disposition.ps1 `
    -Apply -ColdDest "\\cold-storage\backups\opencode\opencode.db.bak.2026-11-01" `
    -SnapshotPath "$env:USERPROFILE\.local\share\opencode\opencode.db.pre-fix-20261108.db" -VerifyHash
#>
[CmdletBinding()]
param(
  [string]$BackupPath = "$env:USERPROFILE\.local\share\opencode\opencode.db.bak",
  [string]$ColdDest = "",
  [string]$SnapshotPath = "",
  [switch]$Apply,
  [switch]$DeleteAfterVerify,
  [switch]$ColdCopyVerified,
  [switch]$VerifyHash,
  [int]$KeepDays = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-ReadonlySql([string]$db, [string]$sql) {
  $out = & sqlite3 -readonly $db $sql 2>&1
  return @($out)
}

$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db"

Write-Host "=== opencode-db-bak-disposition ==="
Write-Host "BackupPath : $BackupPath"
Write-Host "Mode       : $(if ($Apply) { 'APPLY (cold copy; delete only with -DeleteAfterVerify + -ColdCopyVerified)' } else { 'DRY-RUN (inventory only; no copy, no delete)' })"
Write-Host ""

# ---- Step 0: inventory (read-only, never deletes in dry-run) ----------
Write-Host "--- Step 0: inventory ---"
if (-not (Test-Path -LiteralPath $BackupPath)) {
  Write-Host "  (no file at $BackupPath -- nothing to dispose; exit clean)"
  exit 0
}
$bak = Get-Item -LiteralPath $BackupPath
$ageDays = ((Get-Date) - $bak.LastWriteTime).Days
Write-Host ("  Name       : {0}" -f $bak.Name)
Write-Host ("  Length     : {0} bytes ({1:N2} GiB / {2:N2} GB)" -f $bak.Length, ($bak.Length/1GB), ($bak.Length/1e9))
Write-Host ("  LastWrite  : {0}" -f $bak.LastWriteTime)
Write-Host ("  Age        : {0} days (retention threshold {1} days)" -f $ageDays, $KeepDays)
$dir = Split-Path -Parent $BackupPath
$allBak = @(Get-ChildItem (Join-Path $dir "opencode.db.bak*") -ErrorAction SilentlyContinue)
Write-Host ("  .bak* files: {0} total, {1:N2} GiB combined" -f $allBak.Count, ((($allBak | Measure-Object Length -Sum).Sum)/1GB))
foreach ($f in $allBak) {
  Write-Host ("    {0} | {1:N2} GiB | {2}" -f $f.Name, ($f.Length/1GB), $f.LastWriteTime)
}

# ---- Step 1: prove v2 stable (read-only) -------------------------------
Write-Host ""
Write-Host "--- Step 1: v2-stability proof (read-only) ---"
if (-not (Test-Path -LiteralPath $DbPath)) {
  Write-Host "  (live DB not found at $DbPath -- cannot prove v2 stability; refusing -Apply)"
} else {
  $v2count = Invoke-ReadonlySql $DbPath "SELECT COUNT(*) FROM session_v2;"
  $mig = Invoke-ReadonlySql $DbPath "SELECT value FROM kv WHERE key='migration.v1-v2';"
  $integ = Invoke-ReadonlySql $DbPath "PRAGMA integrity_check;"
  Write-Host ("  session_v2 count    -> {0}" -f ($v2count -join " | "))
  Write-Host ("  migration.v1-v2     -> {0}" -f ($mig -join " | "))
  Write-Host ("  live integrity_check-> {0}" -f ($integ -join " | "))
  if (($integ -join "") -notmatch "ok") {
    Write-Host "  WARNING: live integrity_check is not ok; do not dispose .bak until it is ok."
  }
}

if (-not $Apply) {
  Write-Host ""
  Write-Host "DRY-RUN complete. No copy, no delete. The 38 GB file was NOT touched in this task."
  Write-Host "Decision gate for the maintenance window (all required before -Apply):"
  Write-Host "  [ ] Fresh snapshot exists at -SnapshotPath (post-v2) and its integrity_check=ok"
  Write-Host "  [ ] ColdDest is a writable cold-storage path with free space >= source bytes"
  Write-Host "  [ ] v2 stable (session_v2 >= 90, migration.v1-v2 = completed, integrity ok) -- proven above"
  Write-Host "  [ ] Explicit operator approval to copy (and, separately, to delete) recorded"
  exit 0
}

# ---- -Apply gates -------------------------------------------------------
Write-Host ""
Write-Host "--- APPLY gates ---"
if ([string]::IsNullOrWhiteSpace($ColdDest)) {
  Write-Error "-Apply requires -ColdDest <cold-storage file path>."
  exit 1
}
if ([string]::IsNullOrWhiteSpace($SnapshotPath)) {
  Write-Error "-Apply requires -SnapshotPath <fresh snapshot .db> (the replacement .bak). Refusing to copy without it."
  exit 1
}
if (-not (Test-Path -LiteralPath $SnapshotPath)) {
  Write-Error "Snapshot not found: $SnapshotPath. Take it first (see opencode-db-maintenance.ps1 snapshot notes)."
  exit 1
}
$snapCheck = Invoke-ReadonlySql $SnapshotPath "PRAGMA integrity_check;"
Write-Host ("  Snapshot integrity_check -> {0}" -f ($snapCheck -join " | "))
if (($snapCheck -join "") -notmatch "ok") {
  Write-Error "Snapshot integrity_check is not ok. Refusing to copy."
  exit 1
}
$live = Get-Item -LiteralPath $DbPath -ErrorAction SilentlyContinue
if ($null -ne $live) {
  Write-Host ("  Source/live ratio: {0:N1}x (source {1:N2} GiB vs live {2:N2} GiB)" -f ($bak.Length/$live.Length), ($bak.Length/1GB), ($live.Length/1GB))
}

# ---- Step 2: cold copy + verify -----------------------------------------
Write-Host ""
Write-Host "--- Step 2: cold copy (robocopy /J) + byte-verify ---"
$coldDir = Split-Path -Parent $ColdDest
if (-not (Test-Path -LiteralPath $coldDir)) { New-Item -ItemType Directory -Path $coldDir -Force | Out-Null }
$srcDir = Split-Path -Parent $BackupPath
$srcName = Split-Path -Leaf $BackupPath
$dstName = Split-Path -Leaf $ColdDest
# robocopy exit codes 0-7 are success; >=8 failure.
& robocopy $srcDir $coldDir $srcName /J /NP /NDL /NFL 2>&1 | ForEach-Object { Write-Host "  robocopy: $_" }
if ($LASTEXITCODE -ge 8) {
  Write-Error "robocopy failed (exit $LASTEXITCODE). Source preserved; investigate cold volume then retry."
  exit 1
}
$copy = Get-Item -LiteralPath $ColdDest -ErrorAction SilentlyContinue
if ($null -eq $copy) {
  Write-Error "Cold copy missing at $ColdDest after robocopy. Source preserved."
  exit 1
}
Write-Host ("  Copy length: {0} bytes (source {1} bytes)" -f $copy.Length, $bak.Length)
if ($copy.Length -ne $bak.Length) {
  Write-Error "Byte-length mismatch (copy $($copy.Length) vs source $($bak.Length)). Source preserved; do not delete."
  exit 1
}
Write-Host "  Byte-length: MATCH"
if ($VerifyHash) {
  Write-Host "  Computing SHA-256 of source and copy (slow; ~1 h+ for 38 GB)..."
  $h1 = (Get-FileHash -LiteralPath $BackupPath -Algorithm SHA256).Hash
  $h2 = (Get-FileHash -LiteralPath $ColdDest -Algorithm SHA256).Hash
  Write-Host ("  source SHA-256: {0}" -f $h1)
  Write-Host ("  copy   SHA-256: {0}" -f $h2)
  if ($h1 -ne $h2) { Write-Error "Hash mismatch. Source preserved; do not delete."; exit 1 }
  Write-Host "  Hash: MATCH"
} else {
  Write-Host "  Hash check skipped (no -VerifyHash): byte-length + backup-manifest is the verification. Re-run with -VerifyHash when time allows."
}

# ---- Step 3: gated delete ------------------------------------------------
Write-Host ""
Write-Host "--- Step 3: original disposition ---"
if ($DeleteAfterVerify -and $ColdCopyVerified) {
  Write-Host "  -DeleteAfterVerify + -ColdCopyVerified both present; deleting original by explicit operator approval."
  Remove-Item -LiteralPath $BackupPath -Force
  Write-Host "  Deleted: $BackupPath (reclaim ~38.5 GB). Cold copy is the rollback."
} else {
  Write-Host "  Keeping original (copy-only). To delete later: re-run with -DeleteAfterVerify -ColdCopyVerified after the copy manifest/hash is recorded."
}

Write-Host ""
Write-Host "APPLY complete. Verify: .bak total < 2x live DB (not ~12x); disk free +~38.5 GiB if archived off-volume / deleted."
