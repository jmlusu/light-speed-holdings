# ADR-014: URL-Prefix API Versioning (`/api/v1`)

**Status:** Accepted
**Date:** 2026-08-14
**Deciders:** Human operator (via wayfinder grilling ticket #66)
**Technical Domain:** Dashboard API

## Context

The dashboard REST API accumulated roughly 40 endpoints on an unversioned
`/api` root (`src/ai_company/dashboard/api.py`), alongside `/api/mobile`
(`mobile_api.py`) and the `/ws/dashboard` WebSocket (`ws.py`). New endpoints
kept landing on the unversioned root, and there was no convention for how the
API contract evolves or how a breaking change would be signalled.

The API is consumed entirely in-repo:

- the bundled dashboard frontend (`src/ai_company/dashboard/static/js/app.js`),
- the legacy PWA and mobile client (`static/js/mobile.js`, `static/js/service-worker.js`),
- the test suite (integration, performance, dashboard, unit),
- documentation (`docs/API-REFERENCE.md`, `docs/api/MOBILE-API.md`, `docs/api/PUSH-NOTIFICATIONS.md`).

There are no external or third-party consumers, and none are planned this year.

The package is pre-1.0 (0.5.0). Issue #64 established a single source for the
release version: the OpenAPI `version` field derives from the installed package
metadata via `get_version()`. That is the *release* version — it says nothing
about the API contract surface.

## Decision

Version the dashboard API by URL prefix.

1. **Version segment `v1`, major-only** (not `v1.0`):
   - main REST: `/api/*` → `/api/v1/*`
   - mobile: `/api/mobile/*` → `/api/v1/mobile/*`
   - WebSocket: `/ws/dashboard` → `/ws/v1/dashboard`
2. **Ops/infra probes stay unversioned:** `/health`, `/ready`, `/metrics`
   remain at the root. They are Kubernetes/Prometheus probes scraped at fixed
   paths, not version-loyal business surface.
3. **Hard-break migration:** existing `/api/*` paths are removed in the same
   change. No redirect, no deprecated alias. Every consumer is in-repo and
   migrates in the same change; completeness is verified by the full test suite
   plus a repo-wide grep for `"/api/` and `"/ws/dashboard`.
4. **Version bump policy:** the URL major changes only on a breaking contract
   change. Non-breaking additions stay under the current major. Because all
   consumers are internal, a breaking change migrates consumers and retires the
   old major in the same release — no parallel version hosting.
5. **URL version ≠ package version.** The URL segment is the contract major;
   the OpenAPI `version` keeps reflecting the package (pyproject, per #64).
   Package minor/patch releases and all pre-1.0 releases leave the URL alone.

## Consequences

- **Positive:** a legible convention for contract evolution; new endpoints land
  under `/api/v1` instead of an unversioned root; version intent is visible in
  logs, docs, and browser devtools; a v2 escape hatch exists without pretending
  it is needed today; establishing the prefix pre-1.0 is cheap and avoids a
  painful carve-out later.
- **Negative / risk:** a one-time migration churn across the frontend, legacy
  PWA, test suite, and docs; the hard break means any missed consumer breaks
  until migrated (acceptable — everything is in-repo and the suite gates it);
  the `/ws/dashboard` path change breaks any externally bookmarked URL (none
  exist today).
- **Neutral:** ops endpoints unaffected; no dependency, schema, or storage
  changes.

## Links

- Wayfinder ticket "Decide /api/v1 URL versioning" (#66) — the grilling session
  that produced this decision.
- ADR-013 (browser session tokens) — adjacent dashboard API surface, same day.
- Issue #64 "Refresh stale API version metadata" — single source for the OpenAPI
  release version.
- API reference: `docs/API-REFERENCE.md`.
