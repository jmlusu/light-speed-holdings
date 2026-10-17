@echo off
rem Start Vite dev server on port 1441
echo Starting Vite dev server on port 1441...
start "" C:\Users\jmlus\light-speed-holdings\node_modules\.bin\vite.exe dev --host 0.0.0.0
timeout /t 2 /nobreak >nul
echo Vite dev server launched.

rem Start Vite preview server on port 1440
echo Starting Vite preview server on port 1440...
start "" C:\Users\jmlus\light-speed-holdings\node_modules\.bin\vite.exe preview --host 0.0.0.0
timeout /t 2 /nobreak >nul
echo Vite preview server launched.

echo.
echo Marketing sites started:
echo - Dev: http://localhost:1441
echo - Preview: http://localhost:1440
echo.
echo Press Ctrl+C to stop (or close this window).
timeout /t 60 /nobreak >nul