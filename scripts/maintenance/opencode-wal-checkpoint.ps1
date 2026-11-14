<#
.SYNOPSIS
    WAL checkpoint for opencode.db (maintenance window only; dry-run by default).

.DESCRIPTION
    Runs `PRAGMA wal_checkpoint(TRUNCATE)` against opencode.db and reports the
    WAL/DB ratio before and after. Refuses with writers present. Never deletes
    -wal/-shm manually (that IS data loss with uncheckpointed frames).

    A snapshot (opencode-snapshot.ps1) must exist before any checkpoint run.

.EXAMPLE
    pwsh -File scripts/maintenance/opencode-wal-checkpoint.ps1

.EXAMPLE
    pwsh -File scripts/maintenance/opencode-wal-checkpoint.ps1 -Apply
#>
param(
    [string]$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db",
    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$walPath = "$DbPath-wal"

if (-not (Test-Path -LiteralPath $DbPath)) {
    Write-Error "DB not found: $DbPath"; exit 1
}
$dbBytes = (Get-Item -LiteralPath $DbPath).Length
$walBytes = if (Test-Path -LiteralPath $walPath) { (Get-Item -LiteralPath $walPath).Length } else { 0 }
$ratio = if ($dbBytes -gt 0) { [math]::Round($walBytes / $dbBytes * 100, 1) } else { 0 }
Write-Output "WAL/DB: $walBytes / $dbBytes bytes ($ratio%)"

if (-not $Apply) {
    Write-Output "DRY-RUN: would run PRAGMA wal_checkpoint(TRUNCATE). Re-run with -Apply in a maintenance window (OpenCode closed, snapshot taken)."
    exit 0
}

$writers = Get-Process -Name "opencode" -ErrorAction SilentlyContinue
if ($writers) {
    Write-Error "OpenCode process still running. Close it before checkpointing."
    exit 1
}
& sqlite3 "$DbPath" "PRAGMA wal_checkpoint(TRUNCATE); PRAGMA journal_mode; PRAGMA integrity_check;"
$walAfter = if (Test-Path -LiteralPath $walPath) { (Get-Item -LiteralPath $walPath).Length } else { 0 }
Write-Output "WAL after: $walAfter bytes"
