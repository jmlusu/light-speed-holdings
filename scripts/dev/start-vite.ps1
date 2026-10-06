param([switch]$Background)

if ($Background) {
    $logFile = "C:\Users\jmlus\light-speed-holdings\vite-background.log"
    $p = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile", "-Command", " & 'uv' 'run' 'vite' > '" + $logFile + "' 2>&1 " -WorkingDirectory "C:\Users\jmlus\light-speed-holdings" -WindowStyle Hidden
    Write-Host "Vite started in background, PID: $($p.Id)"
    Write-Host "Log file: $logFile"
} else {
    & 'uv' 'run' 'vite'
}