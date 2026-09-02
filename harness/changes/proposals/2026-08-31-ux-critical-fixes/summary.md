---
title: "UX Critical Fixes: Scroll Preservation, Loading States, Error Feedback"
slug: "ux-critical-fixes"
status: "proposed"
location: "proposals"
phase: "plan"
intake_status: "done"
spec_review: "pending"
plan_review: "pending"
modules:
  - "src/ai_company/dashboard/static/js/app.js"
  - "src/ai_company/dashboard/templates/base.html"
  - "src/ai_company/dashboard/templates/index.html"
  - "src/ai_company/dashboard/templates/tasks.html"
  - "src/ai_company/dashboard/static/js/kanban-board.js"
  - "src/ai_company/dashboard/static/js/charts.js"
  - "src/ai_company/dashboard/ws.py"
  - "tests/e2e/test_scroll_preservation.py"
  - "tests/unit/test_dashboard_ws.py"
tags:
  - "ux"
  - "dashboard"
  - "customer-satisfaction"
validation_status: "unknown"
created_at: "2026-08-31"
updated_at: "2026-08-31"
---

# UX Critical Fixes: Scroll Preservation, Loading States, Error Feedback

## Priority
P0 — Directly addresses user-reported "buggy and unstable" dashboard (tracked issues DASH-001 through DASH-008 in `knowledge/technology/dashboard-known-issues.md`).

## Outcome
Eliminate the primary UX pain points the CEO and support team reported:
1. Scroll position lost on every auto-refresh (DASH-001)
2. No loading indicators during data fetch (DASH-003)
3. Failed API calls show no user-facing error (DASH-004)
4. WebSocket reconnect flicker (DASH-002)
5. Toast notification spam (DASH-005)
6. Kanban drag interrupted by refresh (DASH-006)
7. Chart redraw flicker (DASH-007)
8. No manual refresh per section (DASH-008)

## Scope
Multiple files across dashboard frontend + WebSocket layer. Exceeds 2 files — ECL required.

## Deliverables
1. **Scroll preservation** — Robust save/restore in `app.js:946-1014` (`loadDashboard()`)
   - Save position before `Promise.all`, restore after DOM update (2nd frame)
   - Edge case: user manual scroll during refresh → don't fight (`_onScroll` listener tuning)
   - E2E test: scroll to bottom → auto-refresh → position retained
2. **Loading states** — Add `loading` state object to Alpine.js, skeleton/shimmer components
3. **Error feedback** — Extend `errors` object, error banner with retry + "last updated" timestamp
4. **WS resilience** — Exponential backoff + jitter, connection quality states, manual reconnect
5. **Toast queue** — Max 3 visible, critical persist until dismissed
6. **Drag-and-drop** — Pause polling during Kanban drag
7. **Chart coalescing** — `requestAnimationFrame` single redraw per frame
8. **Manual refresh** — Per-section refresh buttons

## Risks
- Scroll fixes interact with Alpine.js reactivity; must test all views (KPI cards, tables, Kanban, charts, org chart)
- WebSocket backoff must not break existing `ws.py` broadcast tests
- Coalescing chart updates risks missing a data point if frame drops — acceptable per Pixel-Perfect spec

## Verification
- `ruff check src/` — 0 errors
- `mypy src/` — 0 errors
- `pytest tests/ -m "not e2e"` — full suite green
- New Playwright E2E: `tests/e2e/test_scroll_preservation.py`
- Manual staging verification by `ux-research-lead`

## Owner
`frontend-engineer` (lead: `lead-frontend`) with `ux-research-lead` verification.
