---
title: "Dashboard Hardening: C4 Task Flow and Reports Views, C5 ReportStore"
slug: "dashboard-hardening-c4-task-flow-and-reports-views-c5-reportstore"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "done"
spec_review: "done"
plan_review: "approved"
modules:
  - "src/ai_company/store/report_store.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/app.py"
  - "src/ai_company/dashboard/static/js/app.js"
files:
  - "src/ai_company/dashboard/templates/reports.html"
  - "src/ai_company/dashboard/templates/task-flow.html"
  - "tests/unit/test_report_store.py"
  - "tests/integration/test_dashboard_api.py"
  - "docs/DASHBOARD-HARDENING-C4-C5-SPEC.md"
tags:
  - "dashboard"
  - "hardening"
  - "reports"
  - "task-flow"
  - "observability"
validation_status: "pass"
created_at: "2026-08-30"
updated_at: "2026-08-30"
session_id: "da757902-5d09-45b2-9b56-84cb0dc7348a"
owner_agent: "jmlus"
claimed_at: "2026-08-30"
---

# Summary

## Outcome

Implemented and verified the two remaining items from the CEO dashboard
hardening plan (C5 `ReportStore` followed by C4 Task Flow + Reports views),
as approved by the CEO in the prior session (C4 Q1=A task-lifecycle
traceability, Q2=A reports viewer, Q3=Task Flow AND Reports pages, Q4=C5-first).

- **C5 `ReportStore`**: a new read-only, queryable layer over agent-produced
  `results/` reports (`loop_result.json` bundles, `experiments/*.jsonl`, root
  `cost_log.jsonl`). Normalizes mixed timestamps (naive-UTC, `Z`, epoch) so
  ordering is correct; exposes `latest(n)` / `oldest(n)` plus bundle/name/agent
  filters. Missing root = empty store; malformed reports are skipped, never
  crash a query.
- **C4 Task Flow view**: `GET /api/v1/tasks/{task_id}/flow` returns the task
  snapshot plus a chronological audit-trail timeline (leveraging the C1
  hash-chained audit trail) with created/updated status-event fallback. The
  `/task-flow` page lets a user trace any task ID and render its lifecycle.
- **C4 Reports view**: `GET /api/v1/reports` (newest-first, `limit`/`agent`
  filters, root `cost_log.jsonl` shard excluded by default for a clean listing)
  and `GET /api/v1/reports/content?path=` (read-only, traversal-guarded to the
  `results/` root). The `/reports` page lists reports newest-first and opens a
  content drawer.

## Decisions

- The codenames "Path-of-RPG" and "FLORA" had no definition anywhere in the
  repo (exhaustive search). The CEO confirmed (chat answers) the recommended
  interpretation: "Path-of-RPG" = task-journey lifecycle traceability (Task Flow
  view); "FLORA" = reports/outcomes viewer (Reports page) built on C5.
- C5 was built first, then C4 UI/API consumed it (approved ordering).
- Reports are strictly read-only; no writes, no persistence-format change, no
  migration of existing `results/`.
- The flat root `cost_log.jsonl` shard (bundle ".") is filtered from the default
  `/api/v1/reports` listing because it is cost records, not reports; it remains
  reachable via `include_cost=true`.
- Report content is served read-only and path-traversal is blocked by resolving
  the requested path and verifying it stays under the reports root (404 on
  escape) — consistent with ADR-013/security posture.
- Every new/modified file belongs to this change; no pre-existing `store/`
  behaviour was changed.

## Validation

- **2026-08-30 (live re-verified at formalization time):**
  - `ruff check src/`: PASS on `store/report_store.py`, `dashboard/api.py`,
    `dashboard/app.py` (and full `src/` clean).
  - `mypy src/`: PASS (strict) on the same three modules.
  - Targeted `test_report_store.py` + `test_dashboard_api.py`: **34 passed**
    (includes 15 ReportStore unit tests and the C4 reports/task-flow integration
    tests: reports page/API, cost-shard exclusion, report-content + traversal
    404, task-flow page/endpoint/not-found).
  - Broader dashboard regression (224 dashboard/report/backlog tests): PASS.
  - Live smoke via TestClient over real `results/` (1787 indexed reports):
    `/api/v1/reports` = 200 (5 returned), `/api/v1/tasks/{id}/flow` = 200,
    `/reports` and `/task-flow` pages render 200 with their markers.

## Next Step

- Full-suite `pytest -m "not e2e"` as the final gate, then close this change
  (`status: completed`) and archive. (The implementing session did not run the
  entire suite within its rollout timeout; it was scoped to the dashboard and
  report suites above.)

## Transition Note

- Created at `phase: validate` because the code was implemented and the targeted
  gates verified in the prior session before this formalization. The full-suite
  gate remains before archive per ECL §4.
