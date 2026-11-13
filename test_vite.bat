@echo off
cd C:\Users\jmlus\light-speed-holdings
set PORT=1441
set VITE_TURNSTILE_SITE_KEY=0x4AAAAAAE404z2CBA0ZUphI
echo Starting Vite dev server on port %PORT%...
npx vite --mode development > vite_output.txt 2>&1 &
echo Vite PID: %!
timeout /t 5 /nobreak >nul
echo Testing connectivity to http://127.0.0.1:%PORT%...
curl -s http://127.0.0.1:%PORT%/
echo.
echo Testing connectivity to http://localhost:%PORT%...
curl -s http://localhost:%PORT%/
echo.
timeout /t 30 /nobreak >nul
echo Terminating Vite...
taskkill /F /IM node.exe 2>nul
echo Done.
