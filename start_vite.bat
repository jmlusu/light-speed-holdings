REM Marketing Site - standard launch is PM2 (dev :1441 / preview :1440).
REM Authority: docs\organization\app-naming-and-port-assignments.md
REM Stop with: pm2 stop vite-dev  /  pm2 stop vite-preview
pm2 start ecosystem.config.cjs
