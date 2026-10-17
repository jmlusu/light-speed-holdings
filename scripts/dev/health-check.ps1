# Checks if Vite servers are ready by polling the health endpoints
# Returns 0 (success) if servers are healthy, 1 (failure) otherwise

$ProjectRoot = "C:\Users\jmlus\light-speed-holdings"
$maxWaitSeconds = 60
$pollInterval = 2
$startTime = Get-Date
$allReady = $false

Write-Host "Waiting for Vite servers (ports 1440/1441) to become ready..."

while ((Get-Date) - $startTime).TotalSeconds -lt $maxWaitSeconds {
    $devReady = $false
    $previewReady = $false

    # Check Vite dev server on port 1441
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:1441/" -Method GET -TimeoutSec 3 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $devReady = $true
        }
    } catch {
        # Server not ready yet
    }

    # Check Vite preview server on port 1440
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:1440/" -Method GET -TimeoutSec 3 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $previewReady = $true
        }
    } catch {
        # Server not ready yet
    }

    if ($devReady -and $previewReady) {
        $allReady = $true
        break
    }

    Start-Sleep -Seconds $pollInterval
}

if ($allReady) {
    Write-Host "Both Vite servers are ready - port 1440 (preview) and port 1441 (dev)" -ForegroundColor Green
    exit 0
} else {
    Write-Host "ERROR: Not both Vite servers became ready within $maxWaitSeconds seconds" -ForegroundColor Red
    # Print PM2 status for debugging
    pm2 status
    exit 1
}
