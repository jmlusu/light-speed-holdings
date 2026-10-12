# Ports Monitoring Session — 2026-10-07

Session record for the Vite dev/preview port monitoring run of 2026-10-07. Operational rules
derived from it live in AGENTS.md §12; the tracked issues live permanently in AGENTS.md §16.

## Monitoring session (22:15–22:29, 10+ min)

20 probe cycles, 120 HTTP probes: both ports stayed listening; 119/120 probes HTTP 200 across
`/`, `/insights`, `/solutions` on each port; `dev.log` and `preview.log` scans: **0 error matches**;
no crashes, no port drift, no EADDRINUSE.

Ports probed: development `npm run dev` on **http://localhost:1441**, production preview
`npm run preview` (serves `dist/`) on **http://localhost:1440**.

## Issues found and fixed

1. **Dev cold-start probe timeout (1 failure — cycle 1, `:1441/` returned ERR).** The first
   request after `npm run dev` exceeded the 15 s probe timeout while Vite optimized the
   1676-module dependency graph. Re-measured cold start: port binds in ~2.5 s, first request
   completes in ~6.3 s and returns 200; subsequent requests ~8 ms.
   **Fix:** automated health checks and QA probes must tolerate the first dev request (retry once
   after the `VITE ready in ...` log line, allow ≥30 s timeout). No code change required;
   reproduced deterministically (warm dep cache ≈ 6 s, cold ≈ >15 s).

2. **Port conflict / server startup failure.** If ports 1440/1441 are already in use (e.g.,
   leftover `node.exe` processes from a previous session), the Vite dev server will fall back to
   the next available port (e.g., 1442) or fail to bind.
   **Fix:** kill any lingering `node.exe` processes before restarting servers, then verify ports
   are free (`netstat -an | findstr "1440 1441"` shows no listeners) and restart with
   `npm run dev` (1441) or `npm run preview` (1440).

Servers were stopped and ports 1440/1441 released after the session.
