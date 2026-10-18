#!/usr/bin/env pwsh
# Marketing Site Lifecycle Manager
# Manages Vite dev server (1441) and preview server (1440)
# Usage: pwsh scripts/dev/manage-marketing-site.ps1 -Action Start/Stop/Status/Monitor [-Minutes N] [-AllowDirtyWorktree]
#
# Safety rules (2026-10-17 marketing site operations plan):
#   - Never kill processes wholesale (no taskkill /IM node.exe); only stop PIDs
#     recorded in output/marketing-site/*.pid, or (Stop only) the listener on
#     our own ports 1440/1441.
#   - Start/Stop run the dirty-worktree preflight first and fail closed.
#   - Servers run via bun (CI pins bun 1.4.2), not uv.

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Start', 'Stop', 'Status', 'Monitor')]
    [string]$Action,
    [int]$Minutes = 10,
    [switch]$AllowDirtyWorktree
)

# Check we're on Windows
$isWin = ($PSVersionTable.PSVersion.Major -ge 5)
if (-not $isWin) {
    Write-Error "This script requires Windows (PowerShell 5.1)"
    exit 1
}

# Port definitions per CTO ratification 2026-10-10, G-5
$PortDev = 1441     # Vite dev server
$PortPreview = 1440 # Vite preview server

# Runtime paths (output/ is gitignored)
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$RuntimeDir = Join-Path $RepoRoot 'output\marketing-site'
$DevPidFile = Join-Path $RuntimeDir 'vite-dev.pid'
$PreviewPidFile = Join-Path $RuntimeDir 'vite-preview.pid'
$DevLog = Join-Path $RuntimeDir 'vite-dev.log'
$DevErrLog = Join-Path $RuntimeDir 'vite-dev.err.log'
$PreviewLog = Join-Path $RuntimeDir 'vite-preview.log'
$PreviewErrLog = Join-Path $RuntimeDir 'vite-preview.err.log'
$PreflightScript = Join-Path $PSScriptRoot 'Test-MarketingSiteOperationalPreflight.ps1'

function Test-PortBound {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen 2>$null
    if (-not $conn) { return $false }
    $proc = Get-Process -Id $conn.OwningProcess 2>$null
    return ($proc -ne $null)
}

function Test-PortUnbound {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen 2>$null
    return (-not $conn)
}

function Invoke-HTTP-Probe {
    param([int]$Port, [string]$Path, [int]$TimeoutSec = 3)
    $uri = "http://localhost:$Port$Path"
    $resp = Invoke-WebRequest -Uri $uri -Method GET -TimeoutSec $TimeoutSec -UseBasicParsing 2>$null
    return $resp
}

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}
function Write-Ok {
    param([string]$Message)
    Write-Host "    [OK] $Message" -ForegroundColor Green
}
function Write-Warn {
    param([string]$Message)
    Write-Host "    [WARN] $Message" -ForegroundColor Yellow
}
function Write-Fail {
    param([string]$Message)
    Write-Host "    [FAIL] $Message" -ForegroundColor Red
}

function New-RuntimeDir {
    if (-not (Test-Path $RuntimeDir)) {
        New-Item -ItemType Directory -Path $RuntimeDir -Force | Out-Null
    }
}

function Invoke-Preflight {
    if (-not (Test-Path $PreflightScript)) {
        Write-Fail ("Preflight script not found: " + $PreflightScript)
        exit 1
    }
    & $PreflightScript -AllowDirtyWorktree:$AllowDirtyWorktree
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Preflight failed - aborting (fail closed)"
        exit 1
    }
}

function Stop-TrackedProcess {
    param([string]$PidFile, [string]$Label)
    if (-not (Test-Path $PidFile)) { return }
    $procId = 0
    try {
        $procId = [int](Get-Content -Path $PidFile -ErrorAction Stop | Select-Object -First 1)
    } catch {
        $procId = 0
    }
    Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
    if ($procId -le 0) {
        Write-Warn ($Label + ": invalid PID file, removed")
        return
    }
    $p = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if (-not $p) {
        Write-Warn ($Label + ": PID " + $procId + " not running")
        return
    }
    if ($p.ProcessName -notmatch '^(bun|node)') {
        Write-Warn ($Label + ": PID " + $procId + " is now '" + $p.ProcessName + "' - not stopping it")
        return
    }
    # Kill only this PID's process tree (never a whole-image taskkill)
    taskkill /PID $procId /T /F 2>$null | Out-Null
    Write-Ok ($Label + ": PID " + $procId + " stopped")
}

function Stop-PortOwner {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $conn) { return }
    $ownerId = [int](@($conn.OwningProcess)[0])
    $p = Get-Process -Id $ownerId -ErrorAction SilentlyContinue
    if (-not $p) { return }
    if ($p.ProcessName -notmatch '^(bun|node)') {
        Write-Warn ("Port " + $Port + " is held by '" + $p.ProcessName + "' (PID " + $ownerId + ") - not a Vite process, leaving it alone")
        return
    }
    taskkill /PID $ownerId /T /F 2>$null | Out-Null
    Write-Ok ("Port " + $Port + ": stopped PID " + $ownerId + " (" + $p.ProcessName + ")")
}

function Start-Servers {
    Write-Step "Starting Marketing Site Vite servers..."
    Invoke-Preflight

    $bun = Get-Command bun -ErrorAction SilentlyContinue
    if (-not $bun) {
        Write-Fail "bun not found on PATH (CI pins bun 1.4.2)"
        exit 1
    }
    New-RuntimeDir

    # Stop only processes this script started earlier
    Stop-TrackedProcess -PidFile $DevPidFile -Label "tracked dev server"
    Stop-TrackedProcess -PidFile $PreviewPidFile -Label "tracked preview server"

    # Fail closed: if our ports are still occupied, require an explicit Stop
    $devConn = Get-NetTCPConnection -LocalPort $PortDev -State Listen -ErrorAction SilentlyContinue
    $previewConn = Get-NetTCPConnection -LocalPort $PortPreview -State Listen -ErrorAction SilentlyContinue
    if ($devConn -or $previewConn) {
        if ($devConn) { Write-Fail ("Port " + $PortDev + " still bound after cleanup") }
        if ($previewConn) { Write-Fail ("Port " + $PortPreview + " still bound after cleanup") }
        Write-Fail "Run with -Action Stop first, then retry"
        exit 1
    }

    Write-Step ("Starting Vite dev server on port " + $PortDev)
    $devProc = Start-Process -FilePath $bun.Source -ArgumentList 'run', 'dev' -WorkingDirectory $RepoRoot -PassThru -RedirectStandardOutput $DevLog -RedirectStandardError $DevErrLog -WindowStyle Hidden
    Set-Content -Path $DevPidFile -Value $devProc.Id
    Write-Ok ("Vite dev started (PID " + $devProc.Id + ")")

    Write-Step ("Starting Vite preview on port " + $PortPreview)
    $previewProc = Start-Process -FilePath $bun.Source -ArgumentList 'run', 'preview' -WorkingDirectory $RepoRoot -PassThru -RedirectStandardOutput $PreviewLog -RedirectStandardError $PreviewErrLog -WindowStyle Hidden
    Set-Content -Path $PreviewPidFile -Value $previewProc.Id
    Write-Ok ("Vite preview started (PID " + $previewProc.Id + ")")

    # Wait for ports to bind (up to 30s)
    $waitCount = 0
    while ($waitCount -lt 30) {
        if ((Test-PortBound $PortDev) -and (Test-PortBound $PortPreview)) { break }
        Start-Sleep -Seconds 1
        $waitCount++
    }

    if ($waitCount -ge 30) {
        Write-Warn "Ports did not bind within 30s, but probing anyway"
    }

    # Probe both ports
    $devResp = Invoke-HTTP-Probe $PortDev "/"
    $previewResp = Invoke-HTTP-Probe $PortPreview "/"

    if ($devResp) {
        if ($devResp.StatusCode -eq 200) {
            Write-Ok ("Port " + $PortDev + ": HTTP 200")
        } else {
            Write-Warn ("Port " + $PortDev + ": status " + $devResp.StatusCode)
        }
    } else {
        Write-Warn ("Port " + $PortDev + ": no HTTP response")
    }

    if ($previewResp) {
        if ($previewResp.StatusCode -eq 200) {
            Write-Ok ("Port " + $PortPreview + ": HTTP 200")
        } else {
            Write-Warn ("Port " + $PortPreview + ": status " + $previewResp.StatusCode)
        }
    } else {
        Write-Warn ("Port " + $PortPreview + ": no HTTP response")
    }

    Write-Ok "Marketing Site servers started"
}

function Stop-Servers {
    Write-Step "Stopping Marketing Site Vite servers..."
    Invoke-Preflight

    Stop-TrackedProcess -PidFile $DevPidFile -Label "tracked dev server"
    Stop-TrackedProcess -PidFile $PreviewPidFile -Label "tracked preview server"

    # Wait for ports to release (up to 10s)
    $waitCount = 0
    while ($waitCount -lt 10) {
        if ((Test-PortUnbound $PortDev) -and (Test-PortUnbound $PortPreview)) { break }
        Start-Sleep -Seconds 1
        $waitCount++
    }

    # Port-based fallback: stop ONLY the listener on our own site ports
    Stop-PortOwner -Port $PortDev
    Stop-PortOwner -Port $PortPreview

    # Wait for ports to become unbound (up to 15s)
    $waitCount = 0
    while ($waitCount -lt 15) {
        if ((Test-PortUnbound $PortDev) -and (Test-PortUnbound $PortPreview)) { break }
        Start-Sleep -Seconds 1
        $waitCount++
    }

    if ($waitCount -ge 15) {
        Write-Warn "Ports did not become unbound within 15s"
    } else {
        Write-Ok "Both ports unbound"
    }
}

function Get-Status {
    Write-Step "Checking Marketing Site server status..."

    $devBound = Test-PortBound $PortDev
    $previewBound = Test-PortBound $PortPreview

    if ($devBound -and $previewBound) {
        Write-Ok ("Port " + $PortDev + ": bound (Vite dev)")
        Write-Ok ("Port " + $PortPreview + ": bound (Vite preview)")

        $devResp = Invoke-HTTP-Probe $PortDev "/"
        if ($devResp -and $devResp.StatusCode -eq 200) {
            Write-Ok ("Port " + $PortDev + ": HTTP 200 response")
        } else {
            Write-Warn ("Port " + $PortDev + ": no HTTP 200 response")
        }

        $previewResp = Invoke-HTTP-Probe $PortPreview "/"
        if ($previewResp -and $previewResp.StatusCode -eq 200) {
            Write-Ok ("Port " + $PortPreview + ": HTTP 200 response")
        } else {
            Write-Warn ("Port " + $PortPreview + ": no HTTP 200 response")
        }
    } else {
        if (-not $devBound) { Write-Warn ("Port " + $PortDev + ": unbound") }
        if (-not $previewBound) { Write-Warn ("Port " + $PortPreview + ": unbound") }
    }
}

function Monitor-Servers {
    param([int]$Minutes = 10)

    Write-Step ("Monitoring Marketing Site servers for " + $Minutes + " minute(s)...")

    $endTime = (Get-Date).AddMinutes($Minutes)
    $checkCount = 0

    while ((Get-Date) -lt $endTime) {
        $checkCount++
        $devBound = Test-PortBound $PortDev
        $previewBound = Test-PortBound $PortPreview

        $ok = $true
        if (-not $devBound) { $ok = $false; Write-Host ("Alert: Port " + $PortDev + " unbound") }
        if (-not $previewBound) { $ok = $false; Write-Host ("Alert: Port " + $PortPreview + " unbound") }

        if ($ok) {
            $devResp = Invoke-HTTP-Probe $PortDev "/"
            $previewResp = Invoke-HTTP-Probe $PortPreview "/"

            if (-not $devResp -or $devResp.StatusCode -ne 200) {
                $ok = $false; Write-Host ("Alert: Port " + $PortDev + " no HTTP 200")
            }
            if (-not $previewResp -or $previewResp.StatusCode -ne 200) {
                $ok = $false; Write-Host ("Alert: Port " + $PortPreview + " no HTTP 200")
            }
        }

        # Report every 30 seconds
        if ($checkCount % 3 -eq 0) {
            $state = if ($ok) { 'OK' } else { 'FAIL' }
            Write-Host ("Monitor check " + $checkCount + ": " + $state)
        }

        Start-Sleep -Seconds 10
    }

    Write-Ok ("Monitoring complete (" + $Minutes + " minutes elapsed)")
}

# Dispatch action
if ($Action -eq 'Start') {
    Start-Servers
} elseif ($Action -eq 'Stop') {
    Stop-Servers
} elseif ($Action -eq 'Status') {
    Get-Status
} elseif ($Action -eq 'Monitor') {
    Monitor-Servers -Minutes $Minutes
} else {
    Write-Fail ("Unknown action: " + $Action + ". Use Start, Stop, Status, or Monitor.")
    exit 1
}
