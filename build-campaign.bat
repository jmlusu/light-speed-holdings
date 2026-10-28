@echo off
REM --------------------------------------------------------------------------
REM LightSpeed Holdings Limited (TM) - one-click campaign build
REM
REM Runs scripts/build_campaign.py from the repository root, using the managed
REM uv environment. Same engine as /build-campaign and /generate-all-assets.
REM
REM Usage:
REM   build-campaign.bat
REM   build-campaign.bat artifacts\campaigns\<slug>
REM   build-campaign.bat <slug> --skip-video
REM --------------------------------------------------------------------------
setlocal
cd /d "%~dp0"

uv run python scripts\build_campaign.py %*
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
  echo.
  echo build-campaign failed with exit code %RC%.
)

exit /b %RC%
