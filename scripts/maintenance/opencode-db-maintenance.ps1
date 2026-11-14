<#Requires -Version 5.1
<#
.SYNOPSIS
  WAL checkpoint + journal-size maintenance for the OpenCode state DB.

.DESCRIPTION
  P0-1 (plan: reports/opencode-db-reliability-fix-2026-11-08.md section 2).

  Default mode is DRY-RUN: read-only PRAGMA inspection via
  `sqlite3 -readonly` only. With -Apply the script enforces snapshot-first +
  writers-stopped + free-space gates, then runs wal_checkpoint(TRUNCATE) and
  caps WAL growth (journal_size_limit=256 MB).

  NEVER run -Apply while OpenCode writers are active: TRUNCATE while a
  reader holds a snapshot returns busy=1 (safe, retryable) and
  force-closing a writer mid-write leaves WAL uncheckpointed (replayed on
  next open, but do not delete -wal/-shm manually).

.PARAMETER DbPath
  Path to opencode.db. Default: ~/.local/share/opencode/opencode.db

.PARAMETER SnapshotPath
  Path to the pre-change snapshot (opencode.db.pre-checkpoint-<ts>.db).
  Required with -Apply; integrity_check=ok on the SNAPSHOT is verified
  read-only before any write.

.PARAMETER Apply
  Perform the checkpoint. Without -Apply only read-only PRAGMAs run.

.PARAMETER MinFreeGB
  Minimum free space (GB) on the DB volume required with -Apply.
  Default 12 (DB + WAL + snapshot + compact headroom).

.PARAMETER WalCapMB
  journal_size_limit in MB. Default 256 (256*1024*1024 bytes).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-maintenance.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-maintenance.ps1 `
    -Apply -SnapshotPath "$env:USERPROFILE\.local\share\opencode\opencode.db.pre-checkpoint-20261108.db"

.NOTES
  Scheduling (after a successful -Apply):
    - PRAGMA wal_checkpoint(PASSIVE) every 5 min (daemon cadence).
    - PRAGMA wal_checkpoint(TRUNCATE) hourly.
    - Alert if wal > 10% x DB for >15 min.
  Rollback: close DB, restore the snapshot via .backup reverse copy,
  re-run PRAGMA integrity_check. Never delete -wal/-shm manually.
#>
[CmdletBinding()]
param(
  [string]$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db",
  [string]$SnapshotPath = "",
  [switch]$Apply,
  [double]$MinFreeGB = 12,
  [int]$WalCapMB = 256
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-FileSize($p) {
  if (Test-Path -LiteralPath $p) { return (Get-Item -LiteralPath $p).Length }
  return -1
}

function Invoke-ReadonlySql([string]$db, [string]$sql) {
  # Read-only path: sqlite3 -readonly + PRAGMA-only statements.
  # Uses & with a single argument string; no wal_checkpoint(TRUNCATE/any) here.
  $out = & sqlite3 -readonly $db $sql 2>&1
  return @($out)
}

function Invoke-WriteSql([string]$db, [string]$sql) {
  # Write path: only called from the -Apply branch after gates pass.
  # Each statement is executed on its own connection by sqlite3 CLI.
  $out = & sqlite3 $db $sql 2>&1
  return @($out)
}

Write-Host "=== opencode-db-maintenance ==="
Write-Host "DbPath     : $DbPath"
Write-Host "Mode       : $(if ($Apply) { 'APPLY (writes checkpoint)' } else { 'DRY-RUN (read-only PRAGMA only)' })"
Write-Host ""

if (-not (Test-Path -LiteralPath $DbPath)) {
  Write-Error "DB not found: $DbPath"
  exit 1
}
if (-not (Get-Command sqlite3 -ErrorAction SilentlyContinue)) {
  Write-Error "sqlite3 CLI not found on PATH; install sqlite3 (same build that produced reports/opencode-db-audit-2026-11-08.md)."
  exit 1
}

# ---- Read-only pre-flight (always safe) -------------------------------
Write-Host "--- File sizes (pre) ---"
foreach ($suffix in "", "-wal", "-shm") {
  $len = Get-FileSize "$DbPath$suffix"
  Write-Host ("  {0}{1} : {2} bytes" -f $DbPath, $suffix, $len)
}
$drive = Get-PSDrive -Name ([IO.Path]::GetPathRoot((Resolve-Path -LiteralPath $DbPath).Path).TrimEnd('\','/')) -ErrorAction SilentlyContinue
if ($null -ne $drive) {
  Write-Host ("  Volume free : {0:N2} GB (need >= {1:N2} GB for -Apply)" -f ($drive.Free/1GB), $MinFreeGB)
}

Write-Host ""
Write-Host "--- Read-only PRAGMA (sqlite3 -readonly) ---"
$preflight = @(
  "PRAGMA journal_mode;",
  "PRAGMA page_size;",
  "PRAGMA page_count;",
  "PRAGMA freelist_count;",
  "PRAGMA auto_vacuum;",
  "PRAGMA journal_size_limit;",
  "PRAGMA integrity_check;"
)
foreach ($sql in $preflight) {
  $res = Invoke-ReadonlySql $DbPath $sql
  Write-Host ("  {0,-28} -> {1}" -f $sql, ($res -join " | "))
}
# Counts (read-only, mutation-neutral). Wrapped so a missing table does not abort pre-flight.
try {
  $counts = Invoke-ReadonlySql $DbPath "SELECT 'session='||(SELECT COUNT(*) FROM session)||' message='||(SELECT COUNT(*) FROM message)||' part='||(SELECT COUNT(*) FROM part);"
  Write-Host ("  counts (readonly) -> {0}" -f ($counts -join " | "))
} catch {
  Write-Host "  counts (readonly) -> (skipped: $($_.Exception.Message))"
}

if (-not $Apply) {
  Write-Host ""
  Write-Host "DRY-RUN complete. No checkpoint/vacuum/journal_size_limit was executed."
  Write-Host "To apply in a maintenance window (writers stopped), pass:"
  Write-Host "  -Apply -SnapshotPath <fresh snapshot .db>   (snapshot integrity is verified before any write)"
  exit 0
}

# ---- -Apply gates -------------------------------------------------------
Write-Host ""
Write-Host "--- APPLY gates ---"
if ([string]::IsNullOrWhiteSpace($SnapshotPath)) {
  Write-Error "-Apply requires -SnapshotPath <fresh snapshot .db>. Refusing to checkpoint without a snapshot."
  exit 1
}
if (-not (Test-Path -LiteralPath $SnapshotPath)) {
  Write-Error "Snapshot not found: $SnapshotPath (take it first via: sqlite3 `"$DbPath`" `".backup '$SnapshotPath'`")."
  exit 1
}
Write-Host "  Snapshot present: $SnapshotPath"
$snapCheck = Invoke-ReadonlySql $SnapshotPath "PRAGMA integrity_check;"
Write-Host ("  Snapshot integrity_check -> {0}" -f ($snapCheck -join " | "))
if (($snapCheck -join "") -notmatch "ok") {
  Write-Error "Snapshot integrity_check is not ok. Refusing to checkpoint."
  exit 1
}
$writers = @(Get-Process opencode -ErrorAction SilentlyContinue)
if ($writers.Count -gt 0) {
  Write-Error ("Refusing -Apply: {0} OpenCode writer process(es) still running (PIDs {1}). Stop OpenCode first; TRUNCATE would return busy=1." -f $writers.Count, (($writers | ForEach-Object { $_.Id }) -join ","))
  exit 1
}
Write-Host "  Writers: none (OpenCode processes absent)."
$drive = Get-PSDrive -Name ([IO.Path]::GetPathRoot((Resolve-Path -LiteralPath $DbPath).Path).TrimEnd('\','/')) -ErrorAction SilentlyContinue
if ($null -ne $drive -and ($drive.Free/1GB) -lt $MinFreeGB) {
  Write-Error ("Refusing -Apply: free space {0:N2} GB < {1:N2} GB minimum. Free disk first (see opencode-db-bak-disposition.ps1)." -f ($drive.Free/1GB), $MinFreeGB)
  exit 1
}
Write-Host "  Free space: OK"

# ---- Apply: TRUNCATE + caps (writers stopped, snapshot verified) -------
Write-Host ""
Write-Host "--- Apply: wal_checkpoint(TRUNCATE) with 5x retry ---"
$busy = $true
for ($attempt = 1; $attempt -le 5; $attempt++) {
  $res = Invoke-WriteSql $DbPath "PRAGMA wal_checkpoint(TRUNCATE);"
  Write-Host ("  attempt {0}: {1}" -f $attempt, ($res -join " | "))
  # busy|log|checkpointed; expect busy=0
  $first = ($res | Select-Object -First 1)
  if ($first -match "^0\|") { $busy = $false; break }
  if ($attempt -lt 5) { Write-Host "  busy=1 (a reader still attached); sleeping 2s..."; Start-Sleep -Seconds 2 }
}
if ($busy) {
  Write-Error "wal_checkpoint(TRUNCATE) still busy after 5 attempts. Do not delete WAL manually; keep writers stopped and retry."
  exit 1
}
$capBytes = [int64]$WalCapMB * 1024 * 1024
Write-Host "--- Apply: WAL growth caps ---"
Invoke-WriteSql $DbPath "PRAGMA journal_size_limit = $capBytes;" | ForEach-Object { Write-Host "  journal_size_limit -> $_" }
Invoke-WriteSql $DbPath "PRAGMA synchronous = NORMAL;" | ForEach-Object { Write-Host "  synchronous -> $_" }
Invoke-WriteSql $DbPath "PRAGMA temp_store = MEMORY;" | ForEach-Object { Write-Host "  temp_store -> $_" }
Invoke-WriteSql $DbPath "PRAGMA cache_size = -64000;" | ForEach-Object { Write-Host "  cache_size -> $_" }

Write-Host ""
Write-Host "--- Verify after (read-only) ---"
Invoke-ReadonlySql $DbPath "PRAGMA journal_mode;" | ForEach-Object { Write-Host "  journal_mode -> $_" }
Invoke-ReadonlySql $DbPath "PRAGMA journal_size_limit;" | ForEach-Object { Write-Host "  journal_size_limit -> $_" }
Invoke-ReadonlySql $DbPath "PRAGMA integrity_check;" | ForEach-Object { Write-Host "  integrity_check -> $_" }
foreach ($suffix in "", "-wal", "-shm") {
  $len = Get-FileSize "$DbPath$suffix"
  Write-Host ("  {0}{1} : {2} bytes (post)" -f $DbPath, $suffix, $len)
}
Write-Host ""
Write-Host "APPLY complete. Expect: opencode.db-wal toward 0; opencode.db ~= unchanged total (freelist ~8 MB; win is durability + backup fidelity, not reclaim)."
