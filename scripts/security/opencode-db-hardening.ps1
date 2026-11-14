#Requires -Version 5.1
<#
.SYNOPSIS
  opencode.db ACL lockdown + encryption hardening (F-01/F-02, fix plan -4/-5).

.DESCRIPTION
  Removes the orphaned SID S-1-5-21-...-1003 (RX) from the opencode data
  directory, breaks inheritance to owner-only, and enables BitLocker (or
  warns for EFS fallback). Read-only by default: without -Execute, the
  script prints the current state + the exact commands it *would* run and
  performs NO destructive ACL changes. With -Execute it prompts for
  confirmation via SupportsShouldProcess before every mutating step
  (-WhatIf also works for a full dry run).

  Host changes are NOT inside the workspace (data lives in
  %USERPROFILE%\.local\share\opencode) - but NO file outside the
  workspace is created by default: icacls snapshots go to the current
  workspace root. The script itself is a runbook, not an auto-fix.

.NOTES
  Reference: reports/opencode-db-security-fix-2026-11-08.md -4/-5.
  BitLocker/EFS/Manage-BDE steps require an elevated (admin) shell.
  Do NOT run with an admin shell merely to inspect - use the read-only
  default mode for status checks.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [switch]$Execute,
  [string]$OpencodeDir = (Join-Path $env:USERPROFILE ".local\share\opencode"),
  [string]$OrphanedSid = "S-1-5-21-2913538908-3024988640-2666040046-1003",
  [string]$SnapshotDir = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$DbFiles = @(
  (Join-Path $OpencodeDir "opencode.db"),
  (Join-Path $OpencodeDir "opencode.db.bak"),
  (Join-Path $OpencodeDir "auth.json"),
  (Join-Path $OpencodeDir "mcp-auth.json")
)

function Show-AclState {
  param([string]$Label, [string]$Path)
  Write-Host ""
  Write-Host "--- $Label : $Path ---" -ForegroundColor Cyan
  if (-not (Test-Path $Path)) {
    Write-Host "(does not exist)"
    return
  }
  icacls $Path
}

# -- 1. Read-only baseline (always runs, no changes) -----------------------
Write-Host "=== BASELINE (read-only - no changes are made without -Execute) ===" -ForegroundColor Green
Show-AclState "Data directory" $OpencodeDir
foreach ($f in $DbFiles) { Show-AclState "Credential file" $f }
Write-Host ""
Write-Host "--- EFS status (cipher /c - expect U = unencrypted) ---" -ForegroundColor Cyan
cipher /c (Join-Path $OpencodeDir "opencode.db")
Write-Host ""
Write-Host "--- BitLocker status (needs admin; failure here is not fatal) ---" -ForegroundColor Cyan
try { manage-bde -status C: } catch { Write-Host "BitLocker status unavailable: $($_.Exception.Message)" }
Write-Host ""
Write-Host "Plaintext backup present: $(Test-Path (Join-Path $OpencodeDir 'opencode.db.bak')) (expect False after F-03)"

if (-not $Execute) {
  Write-Host ""
  Write-Host "DRY RUN complete. Re-run with -Execute (elevated shell) to apply changes." -ForegroundColor Yellow
  Write-Host "This script never auto-executes destructive ACL/encryption changes."
  Write-Host ""
  Write-Host "Commands that -Execute WOULD run (see -WhatIf for PowerShell confirmation flow):" -ForegroundColor Yellow
  Write-Host "  icacls `"$OpencodeDir`" /remove `"$OrphanedSid`" /T /Q"
  Write-Host "  icacls `"$OpencodeDir`" /inheritance:r"
  Write-Host "  icacls `"$OpencodeDir`" /grant:r ... (owner/SYSTEM/Administrators, see script)"
  Write-Host "  manage-bde C: -protectors -add -type RecoveryPassword; manage-bde -turnon C:"
  Write-Host "  (or fallback) cipher /e /s:`"$OpencodeDir`""
  return
}

# -- 2. Snapshot ACLs BEFORE any change (evidence) -------------------------
if ($PSCmdlet.ShouldProcess($OpencodeDir, "snapshot current ACLs")) {
  $stamp = Get-Date -Format "yyyy-MM-dd"
  $snapDir = Join-Path $SnapshotDir ".\icacls-snapshots"
  New-Item -ItemType Directory -Force -Path $snapDir | Out-Null
  icacls $OpencodeDir | Out-File (Join-Path $snapDir "icacls-before-$stamp.txt") -Encoding utf8
  icacls (Join-Path $OpencodeDir "opencode.db") | Out-File (Join-Path $snapDir "icacls-db-before-$stamp.txt") -Encoding utf8
  Write-Host "ACL snapshots saved to $snapDir"
}

# -- 3. Remove orphaned SID (F-01) -----------------------------------------
if ($PSCmdlet.ShouldProcess($OpencodeDir, "remove orphaned SID $OrphanedSid (recursive)")) {
  icacls $OpencodeDir /remove $OrphanedSid /T /Q
  Write-Host "Removed orphaned SID (if it was present)."
}

# -- 4. Break inheritance; assert owner-only (F-01) -------------------------
if ($PSCmdlet.ShouldProcess($OpencodeDir, "owner-only lockdown (inheritance:r + grant:r)")) {
  icacls $OpencodeDir /inheritance:r
  icacls $OpencodeDir /grant:r "JRMTHINKPAD\jmlus:(OI)(CI)F" "NT AUTHORITY\SYSTEM:(OI)(CI)F" "BUILTIN\Administrators:(OI)(CI)F"
  foreach ($f in $DbFiles) {
    if (Test-Path $f) {
      icacls $f /inheritance:r
      icacls $f /grant:r "JRMTHINKPAD\jmlus:F" "NT AUTHORITY\SYSTEM:F" "BUILTIN\Administrators:F"
    }
  }
  Write-Host "ACL lockdown applied."
}

# -- 5. Encryption at rest (F-02: BitLocker preferred) ---------------------
if ($PSCmdlet.ShouldProcess("C:", "enable BitLocker (requires admin + restart)")) {
  manage-bde C: -protectors -add -type RecoveryPassword
  manage-bde -turnon C:
  Write-Host "BitLocker enable requested (restart required). Otherwise use EFS fallback: cipher /e /s:`"$OpencodeDir`""
}

# -- 6. Verification (read-only; acceptance criteria = no ...-1003, E / On) --
Write-Host ""
Write-Host "=== VERIFICATION (read-only) ===" -ForegroundColor Green
Show-AclState "Data directory (after)" $OpencodeDir
foreach ($f in $DbFiles) { Show-AclState "Credential file (after)" $f }
cipher /c (Join-Path $OpencodeDir "opencode.db")
manage-bde -status C: 2>$null | Select-Object -First 5
Test-Path (Join-Path $OpencodeDir "opencode.db.bak")
