@echo off
cd "C:\Users\jmlus\.local\share\opencode\worktree\9930fa\glowing-engine"
npx tsc --noEmit 2>&1
echo.
echo.
exit %errorlevel%