#!/usr/bin/env pwsh
# Marketing Site Lifecycle Manager
# Manages Vite dev server (1441) and preview server (1440)
# Usage: pwsh scripts/dev/manage-marketing-site.ps1 -Action Start/Stop/Status/Monitor [-Minutes N]

# Check we're on Windows
$isWin = ($PSVersionTable.PSVersion.Major -ge 5)
if (-not $isWin) {
    Write-Error "This script requires Windows (PowerShell 5.1)"
    exit 1
}

# Port definitions per CTO ratification 2026-10-10, G-5
$PortDev = 1441   # Vite dev server
$PortPreview = 1440  # Vite preview server

function Test-PortBound {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen 2>$null
    if (-not $conn) { return False }
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
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}
function Write-Ok {
    Write-Host "    [OK] $Message" -ForegroundColor Green
}
function Write-Warn {
    Write-Host "    [WARN] $Message" -ForegroundColor Yellow
}
function Write-Fail {
    Write-Host "    [FAIL] $Message" -ForegroundColor Red
}

function Start-Servers {
    Write-Step ("Starting Marketing Site Vite servers...")

    # Kill any lingering node processes
    cmd /c "taskkill /F /IM node.exe" 2>$null

    # Start Vite dev server on 1441
    Write-Step ("Starting Vite dev server on port " + $PortDev)
    & 'uv' 'run' 'vite' > $null 2>&1 &

    # Start Vite preview on 1440
    Write-Step ("Starting Vite preview on port " + $PortPreview)
    & 'uv' 'run' 'vite' --preview > $null 2>&1 &

    # Wait for ports to bind (up to 30s)
    $waitCount = 0
    while ($waitCount -lt 30) {
        if (Test-PortBound $PortDev -and Test-PortBound $PortPreview) { break }
        Start-Sleep -Seconds 1
        $waitCount++
    }

    if ($waitCount -ge 30) {
        Write-Warn ("Ports did not bind within 30s, but proceeding anyway")
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

    Write-Ok ("Marketing Site servers started")
}

function Stop-Servers {
    Write-Step ("Stopping Marketing Site Vite servers...")

    # Kill node processes
    cmd /c "taskkill /F /IM node.exe" 2>$null

    # Wait for ports to become unbound (up to 15s)
    $waitCount = 0
    while ($waitCount -lt 15) {
        if (Test-PortUnbound $PortDev -and Test-PortUnbound $PortPreview) { break }
        Start-Sleep -Seconds 1
        $waitCount++
    }

    if ($waitCount -ge 15) {
        Write-Warn ("Ports did not become unbound within 15s")
    } else {
        Write-Ok ("Both ports unbound")
    }
}

function Get-Status {
    Write-Step ("Checking Marketing Site server status...")

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
    param([int]$Minutes = 1)

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
            Write-Host ("Monitor check " + $checkCount + ": " + (if ($ok) {'OK'} else {'FAIL'}))
        }

        Start-Sleep -Seconds 10
    }

    Write-Ok ("Monitoring complete (" + $Minutes + " minutes elapsed)")
}

# Parse action parameter
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
