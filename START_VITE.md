# Starting the Vite Development Server

## From Windows PowerShell

```powershell
cd C:\Users\jmlus\light-speed-holdings
npm run dev
```
This starts Vite on port 1441 (default, from vite.config.ts:87).

## Starting the Preview Server

```powershell
npm run preview
```
This starts Vite preview on port 1440 (from vite.config.ts:114).

## Verification

```powershell
curl http://127.0.0.1:1441  # Should return 200 OK with LightSpeed Holdings page
curl http://127.0.0.1:1440  # Should return 200 OK (preview build)
```

## Keeping the Server Alive

- Run Vite in a persistent terminal window (do not close)
- Or use `start /b npm run dev` to run in background
- Or use a process manager like pm2:
  ```powershell
  pnpm install -g pm2
  pm2 start "npm run dev" --name "vite-dev"
  pm2 save
  pm2 startup
  ```

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl → Connection refused` | Vite not running | Run `npm run dev` |
| Error about port 8420/8421 | CEO Dashboard conflict | Check vite.config.ts dashboardPortGuard; ensure no other process on those ports |
| `EADDRINUSE` | Another process on port 1441 | Kill the other process, or change vite.config.ts port env var |
