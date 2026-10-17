# Plan: Fix CEO Dashboard Bugs

## Context

The CEO Dashboard has 5 bugs that cause components to show incorrect or missing data. All bugs are in the data wiring layer — the backend APIs return correct data, but the frontend either discards it or the backend has computation gaps.

## Bugs to Fix

Status: DONE (Stream C frontend), BACKEND (other stream: `feature/cleanup-dummy-tasks`), or DEFERRED.

| # | Bug | Impact | Root Cause | Status |
|---|-----|--------|------------|--------|
| 1 | Cost data discarded on home page | Cost Breakdown shows $0.0000 | `loadDashboard()` fetches costs but never assigns to state | **DONE** (Stream C) |
| 2 | Department Load always shows 0 | All departments show 0 agents | API never cross-references agent registry | BACKEND (other stream) |
| 3 | Cost Efficiency always returns None | Org Health missing 25% weight | `get_cost_summary()` never returns `budget` key | BACKEND (other stream) |
| 4 | No task drill-down on dashboard | Can't click tasks in Recent Tasks | No slide-out panel bound to `taskDetailOpen` on dashboard | **DONE** (Stream C) |
| 5 | Org Health score may be stale | Shows 100 instead of ~60 | Browser cache or WebSocket race condition | DONE (cache half, Stream C); WS race backend (other stream) |

---

## Change 1: Wire Cost Data on Dashboard Home Page — DONE (Stream C)

**File:** `src/ai_company/dashboard/static/js/app.js`

After the `tasks` assignment in `loadDashboard()`, `costs` is now mapped into
`this.costSummary` / `this.budgetPct` / `this.agentCosts` / `this.costAlerts`
using exactly the same shape as `loadCosts()` (Bug 1). No backend change.

**Verification:**
- Start dashboard, navigate to home page
- Cost Breakdown should show actual spend (not $0.0000)
- Cost Trend sparkline should render data points

---

## Change 2: Compute Department Agent Counts — BACKEND, OTHER STREAM

Implemented via `feature/cleanup-dummy-tasks` (`src/ai_company/dashboard/api.py`
`list_departments()` aggregates counts from `company-registry.yaml`). Not
touched in Stream C (DO NOT touch backend).

---

## Change 3: Add Budget to Cost Summary — BACKEND, OTHER STREAM

Implemented via `feature/cleanup-dummy-tasks` (`data_service.py`
`get_cost_summary()` adds `budget`; org-health scorer now returns a real
`cost_efficiency`). Not touched in Stream C.

---

## Change 4: Add Task Drill-Down on Dashboard — DONE (Stream C)

**Files:** `src/ai_company/dashboard/templates/index.html` (+ no app.js change)

- Task rows already call `@click="openTaskDrillDown(t)"`; `openTaskDrillDown`
  reuses the existing `openTaskDetail()` slide-out (`selectedTask` /
  `taskDetailOpen`).
- The slide-out panel + overlay (equivalent to `tasks.html`) is now embedded in
  `index.html` before `{% endblock %}`: header w/ task id + close, status /
  priority badges, receiver / department, instruction + description,
  created / updated, Decompose subtask block, Reassign / Escalate actions.
  Wired with the same Alpine state names so `app.js` needs no changes.
- Overlay + X close via `closeTaskDetail()`.

**Verification:**
- Start dashboard, click on any task in Recent Tasks
- Slide-out panel should open with task details
- Click overlay or X to close

---

## Change 5: Force Org Health Refresh — CACHE HALF DONE (Stream C)

- `sw.js` `CACHE_VERSION` bumped to `jarvis-v2` (activate purges older caches).
- `base.html` loads `app.js?v=2`.
- API traffic is network-first (60s fallback) so org-health is fresh while
  online; no additional cache-busting needed for the browser-cache half.
- WebSocket race half: handled by backend work in `feature/cleanup-dummy-tasks`.
- `ceo-hero-prototype.js` trend loader keeps a `res.ok` guard → graceful when
  `/api/v1/org-health/components/trend` 404s; endpoint corrected from
  `/api/v1/kpis/org-health` to `/api/v1/org-health`.

**Verification:**
- Start dashboard, refresh page
- Org Health should show correct score (~60 AMBER, not 100 GREEN)
- Score should update on each 15-second poll

---

## Files to Modify

| File | Changes |
|------|---------|
| `src/ai_company/dashboard/static/js/app.js` | Wire cost data in `loadDashboard()` (Bug 1) |
| `src/ai_company/dashboard/templates/index.html` | Embed task-detail slide-out panel (Bug 4) |

## Deferred / Not Wired

- `src/ai_company/dashboard/kpis/company_kpis.py` (untracked, Stream C scope)
  stays standalone: it exposes plain functions
  (`COLLECTORS = KPI-001/KPI-002/KPI-005`) which do NOT match the
  `KPICollector` class interface used by `ALL_COLLECTORS` / `collect_all_kpis()`
  in `kpis/__init__.py`. Wiring would not be a one-liner, so both files are
  left as-is. `scripts/compute_company_kpis.py` modifications not reverted.

## Verification

1. `uv run ruff check src/` — no lint errors
2. `uv run mypy src/` — no type errors
3. `uv run pytest tests/ -x` — tests pass
4. Manual: Start dashboard, verify:
   - Cost Breakdown shows actual spend (not $0.0000)
   - Department Load shows agent counts (not all 0)
   - Org Health shows ~60 AMBER (not 100 GREEN)
   - Cost Efficiency shows a score (not --)
   - Clicking a task opens the slide-out panel
