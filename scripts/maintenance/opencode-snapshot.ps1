<#
.SYNOPSIS
    Controlled snapshot of the OpenCode Desktop database (maintenance window only).

.DESCRIPTION
    Takes a WAL-consistent backup via `sqlite3 ".backup"` to an operator-specified
    path (encrypted volume, owner-only ACL), verifies it with
    `PRAGMA integrity_check`, and refuses to run while OpenCode holds writers.

    Run only in a maintenance window with OpenCode closed; the pre-fix snapshot
    is the rollback artifact for every DB-mutating step (WAL checkpoint,
    orphan sweep, retention VACUUM). The snapshot is secrets-bearing and is
    pruned with the retention window.

.EXAMPLE
    pwsh -File scripts/maintenance/opencode-snapshot.ps1 -DestinationPath "C:\secure-archive\opencode-pre-fix-2026-11-08.db"

.EXAMPLE
    pwsh -File scripts/maintenance/opencode-snapshot.ps1 -DestinationPath "C:\secure-archive\opencode-pre-fix-2026-11-08.db" -DbPath "C:\Users\jmlus\.local\share\opencode\opencode.db" -WhatIf
#>
param(
    [Parameter(Mandatory = $true)][string]$DestinationPath,
    [string]$DbPath = "$env:USERPROFILE\.local\share\opencode\opencode.db",
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $DbPath)) {
    Write-Error "DB not found: $DbPath"; exit 1
}

$writers = Get-Process -Name "opencode" -ErrorAction SilentlyContinue | Where-Object {
    $_.Id -ne $PID
}
if ($writers -and -not $WhatIf) {
    Write-Error "OpenCode process still running (PID $($writers.Id -join ', ')). Close it before snapshot."
    exit 1
}

$dbBytes = (Get-Item -LiteralPath $DbPath).Length
$walPath = "$DbPath-wal"
$walBytes = if (Test-Path -LiteralPath $walPath) { (Get-Item -LiteralPath $walPath).Length } else { 0 }
Write-Output "Source DB: $DbPath ($dbBytes bytes), WAL: $walBytes bytes"

if ($DestinationPath -like "*light-speed-holdings*") {
    Write-Error "Refusing to snapshot secrets-bearing data into the project repository. Use an encrypted volume path."
    exit 1
}

if ($WhatIf) {
    Write-Output "WHATIF: .backup '$DbPath' -> '$DestinationPath' (+ integrity_check on snapshot)"
    exit 0
}
$destDir = Split-Path -Parent $DestinationPath
if ($destDir -and -not (Test-Path -LiteralPath $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}
& sqlite3 "$DbPath" ".backup '$DestinationPath'"
if ($LASTEXITCODE -ne 0) {
    Write-Error "sqlite3 .backup failed with exit $LASTEXITCODE"; exit 1
}
& sqlite3 $DestinationPath "PRAGMA integrity_check;"
Write-Output "Snapshot complete: $DestinationPath"
Write-Output "Next: ACL-lockdown the snapshot (owner-only) and confirm the destination volume is encrypted (BitLocker/EFS)."
