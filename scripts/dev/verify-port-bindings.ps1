# Port-binding identity audit (CTO ratification 2026-10-10, G-5).
#
# For each ratified port, reports which process actually owns the listener and
# verifies the §5 health contract of the app that should own it:
#   1441 (vite dev) / 1440 (vite preview) -> node/vite; GET / must be HTML.
#       An HTML response that is JSON `status` means the Dashboard is
#       cross-serving on a Marketing Site port -> FAIL.
#   8420 (dashboard prod) / 8421 (dashboard dev) -> python/uvicorn;
#       GET /health must be JSON with a `status` field (ADR-012: auth-exempt).
#       An HTML response there means the Marketing Site is cross-serving on a
#       dashboard port -> FAIL.
# A port with no listener is reported as "unbound" and is not a violation
# (nothing is running there).
#
# Windows only (Get-NetTCPConnection). Local, read-only: TCP table inspection
# + HTTP GET probes; no auth, no writes, no secrets.
#
# Usage:
#   pwsh scripts/dev/verify-port-bindings.ps1            # owner + contract probe
#   pwsh scripts/dev/verify-port-bindings.ps1 -SkipHttp  # owner map only
# Exit code 0 = all consistent, 1 = mismatch/cross-serving, 2 = unsupported.

[CmdletBinding()]
param(
    [switch]$SkipHttp
)

$ErrorActionPreference = 'SilentlyContinue'

# --- platform gate -----------------------------------------------------------
$onWindows = $true
if ($PSVersionTable.PSVersion.Major -ge 6) { $onWindows = [bool]$IsWindows }
if (-not $onWindows) {
    Write-Error "verify-port-bindings.ps1 requires Windows (Get-NetTCPConnection). Use netstat/ss + the same contract rules on other hosts."
    exit 2
}
if (-not (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue)) {
    Write-Error "Get-NetTCPConnection is unavailable on this host."
    exit 2
}

# --- ratified assignments ----------------------------------------------------
$ViteFamily  = @('node', 'nodejs', 'vite')
$DashFamily  = @('python', 'python3', 'py', 'uv', 'uvicorn', 'gunicorn', 'hypercorn', 'uwsgi')
$Checks = @(
    @{ Port = 1441; App = 'Marketing Site dev';     Family = 'vite';      Names = $ViteFamily; Probe = 'html' },
    @{ Port = 1440; App = 'Marketing Site preview'; Family = 'vite';      Names = $ViteFamily; Probe = 'html' },
    @{ Port = 8420; App = 'Dashboard prod';         Family = 'dashboard'; Names = $DashFamily; Probe = 'json' },
    @{ Port = 8421; App = 'Dashboard dev';          Family = 'dashboard'; Names = $DashFamily; Probe = 'json' }
)

$failures = 0
$rows = @()

foreach ($check in $Checks) {
    $port = $check.Port
    $row = [ordered]@{
        Port     = $port
        Expected = $check.Family
        Owner    = '-'
        Pid      = '-'
        Contract = if ($SkipHttp) { 'skipped' } else { 'n/a' }
        Result   = 'OK'
    }

    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
            Select-Object -First 1

    if (-not $conn) {
        $row.Owner = 'unbound'
        $row.Result = 'OK (unbound)'
        $rows += [pscustomobject]$row
        continue
    }

    $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
    $procName = if ($proc) { $proc.ProcessName.ToLowerInvariant() } else { 'unknown' }
    $row.Pid = $conn.OwningProcess
    $row.Owner = $procName

    $identityOk = $check.Names -contains $procName
    if (-not $identityOk) {
        $row.Result = 'FAIL (identity)'
        $failures++
        Write-Host "FAIL  :$port ($($check.App)) owned by '$procName' (expected $($check.Family) family: $($check.Names -join '/'))"
    }

    if ($SkipHttp) { $rows += [pscustomobject]$row; continue }

    # --- §5 contract probe ---------------------------------------------------
    $uri = if ($check.Probe -eq 'json') { "http://localhost:$port/health" } else { "http://localhost:$port/" }
    try {
        $resp = Invoke-WebRequest -Uri $uri -Method GET -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        $ctype = [string]$resp.Headers['Content-Type']
        $body = [string]$resp.Body
        if (-not $body) { $body = [string]$resp.Content }

        $looksJson = $ctype -match 'application/json' -or $body.TrimStart().StartsWith('{')
        $looksHtml = $ctype -match 'text/html' -or $body.TrimStart().StartsWith('<')

        if ($check.Probe -eq 'json') {
            if ($looksHtml -and -not $looksJson) {
                $row.Contract = 'HTML on /health'
                $row.Result = 'FAIL (cross-serving)'
                $failures++
                Write-Host "FAIL  :$port ($($check.App)) returned HTML on /health - Marketing Site is serving a dashboard port"
            }
            elseif ($body -match '"status"\s*:') {
                $row.Contract = 'JSON status'
                if ($row.Result -eq 'OK') { $row.Result = 'OK' }
            }
            else {
                $row.Contract = 'JSON without status'
                $row.Result = 'FAIL (contract)'
                $failures++
                Write-Host "FAIL  :$port ($($check.App)) /health response has no JSON status field"
            }
        }
        else {
            if ($looksJson -and -not $looksHtml) {
                $row.Contract = 'JSON on /'
                $row.Result = 'FAIL (cross-serving)'
                $failures++
                Write-Host "FAIL  :$port ($($check.App)) returned JSON on / - Dashboard is serving a Marketing Site port"
            }
            elseif ($looksHtml) {
                $row.Contract = 'HTML'
                if ($row.Result -eq 'OK') { $row.Result = 'OK' }
            }
            else {
                $row.Contract = 'not HTML'
                $row.Result = 'FAIL (contract)'
                $failures++
                Write-Host "FAIL  :$port ($($check.App)) / did not return HTML"
            }
        }
    }
    catch {
        $row.Contract = 'probe failed'
        $row.Result = 'FAIL (probe)'
        $failures++
        Write-Host "FAIL  :$port ($($check.App)) listener present but $uri unreachable: $($_.Exception.Message)"
    }

    $rows += [pscustomobject]$row
}

Write-Host ''
$rows | Format-Table -AutoSize | Out-String | Write-Host

if ($failures -gt 0) {
    Write-Host "verify-port-bindings: $failures failure(s) - port boundary violated (CTO ratification 2026-10-10)."
    exit 1
}
Write-Host 'verify-port-bindings: all four ports consistent with the ratified boundary (bound-correct or unbound).'
exit 0
