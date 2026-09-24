# White-screen on /jobs when API returns 200 without a jobs key

**ID:** BUG-27
**Date:** 2026-09-25
**Resolved:** closed
**Commit:** `31ff287`
**Issue:** #27

## Symptom

`GET /api/v1/athena/jobs` returns HTTP 200 whose JSON body has no `jobs` key (e.g. a bare array, or a gateway object). The frontend renders a white screen with:
```
TypeError: Cannot read properties of undefined (reading 'length')
    at JobList (JobList.tsx:1100:48)
```

## Root Cause

The AI Studio preview environment serves HTTP 200 with a body lacking the `jobs` key. The frontend trusted the shape blindly — `frontend/src/pages/athena/JobList.tsx:54` did `setJobs(response.jobs)` unchecked, so `jobs` became `undefined`, and `jobs.length` at JobList.tsx:329 threw. A non-2xx is NOT the cause: that path is caught and renders the empty state instead.

Nothing in this repo's backend can produce a wrong-shape 200 (`routes.py` always returns `JobListResponse`; middlewares only emit 429/401). The wrong shape is served by the preview environment.

## Fix

- `frontend/src/lib/athena/api.ts`: `listJobs` now normalises any 200 body (bare array, `{}`, canonical) into a guaranteed `JobListResponse`, with a one-time `console.warn` in dev when the shape is unexpected.
- `frontend/src/pages/athena/JobList.tsx`, `JobDetail.tsx`, `Dashboard.tsx`, `PipelineColumn.tsx`: defensive reads (`?.length ?? 0`).
- `frontend/src/App.tsx` + new `frontend/src/components/athena/RouteError.tsx`: route-level `errorElement` so a bad payload shows a recoverable UI instead of a white screen.
- `frontend/src/lib/athena/api.test.ts`: 5 vitest cases covering the normaliser.
- `scripts/dev-preview.sh`: shape sanity-check on startup prints a warning if the jobs body lacks `jobs`.

## Files Changed

`frontend/src/lib/athena/api.ts`, `frontend/src/lib/athena/api.test.ts`, `frontend/src/pages/athena/JobList.tsx`, `frontend/src/pages/athena/JobDetail.tsx`, `frontend/src/pages/athena/Dashboard.tsx`, `frontend/src/components/athena/PipelineColumn.tsx`, `frontend/src/App.tsx`, `frontend/src/components/athena/RouteError.tsx`, `scripts/dev-preview.sh`

## Diagnostic Commands

```powershell
curl http://127.0.0.1:8000/health
curl -i 'http://127.0.0.1:8000/api/v1/athena/jobs?limit=1'
```
If `/health` is NOT `{"status":"ok","service":"athena"}`, another process owns port 8000 and the proxy is pointed at the wrong service. `curl -i` on /jobs shows the actual body.

## Verification

```powershell
pnpm lint   # exit 0
pnpm test   # 14 passed
pnpm dev:preview  # /jobs renders empty state, not white screen
```

## Pattern

Unchecked `response.jobs` access. Always normalise API responses at the boundary.
