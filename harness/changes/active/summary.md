---
title: "Remove Dummy Tasks & Wire Real Organizational Data"
slug: "cleanup-dummy-tasks"
status: "in_progress"
location: "active"
phase: "implement"
intake_status: "done"
spec_review: "done"
plan_review: "approved"
modules:
  - "src/ai_company/data/task_store.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/data_service.py"
  - "src/ai_company/dashboard/monitoring.py"
  - "src/ai_company/cli/dashboard.py"
  - "src/ai_company/cli/client.py"
  - "src/ai_company/cli/onboarding.py"
  - "src/ai_company/cli/specialists.py"
  - "src/ai_company/orchestrator/scheduler.py"
  - "src/ai_company/services/base.py"
  - "src/ai_company/services/onboarding.py"
  - "scripts/backfill_decompositions.py"
  - "scripts/restore_acme_tasks.py"
files:
  - "harness/changes/active/plan.md"
  - "harness/changes/active/spec.md"
  - "harness/changes/active/tasks.md"
  - "tests/unit/test_task_cleanup.py"
tags:
  - "dashboard"
  - "cleanup"
  - "demo-data"
validation_status: "pass"
created_at: "2026-08-28"
updated_at: "2026-08-29"
---

# Summary

## Outcome

Partially implemented. The goal is to eliminate dummy/demo task data (7 seeded
test tasks + 10 Acme Corp `proj-acme-chatbot` demo tasks) from the CEO dashboard
"Recent Tasks" widget, and add a `ai-company dashboard cleanup` CLI command.

## Decisions

- Demo/test detection must key on demonstrable markers only:
  `proj-acme-chatbot` in instruction/id, instruction starting with `Test `,
  and task ids starting with `test-`/`verify-`.
- Routing a task to the real `test-agent` receiver is legitimate and must NOT
  mark it as dummy. The earlier over-broad receiver-name heuristic was removed
  because it false-positived on the real `test-agent` and broke the test suite.
- SQL cleanup predicates use case-sensitive `instr()`/`GLOB` (not `LIKE`) so
  real lowercase `test ...` instructions are never deleted at the DB level.
- `GET /api/v1/tasks` and `/api/v1/tasks/paginated` accept an `include_test`
  query param (default `false`); `_read_all_tasks(include_test=...)` is the
  single read filter (SQLite-first, inbox-file fallback).
- `scripts/restore_acme_tasks.py` and `scripts/backfill_decompositions.py`
  both BELONG to this feature and are kept with fixes: all restore tasks carry
  the `proj-acme-chatbot` marker (one previously lacked it and would survive
  cleanup); backfill now uses the guaranteed DB path and skips demo/test
  subtasks.
- `monitoring.py` `event_type != "task_completed"` alignment is correct:
  `AuditEventType.TASK_COMPLETED` is the canonical `"task_completed"`.

## Validation

- Detection contract unit tests (positive matrix, negatives incl. `test_`-id,
  uppercase id, lowercase `test ...` instruction, and a real task routed to
  the `test-agent` receiver): `tests/unit/test_task_cleanup.py` — 29 passed.
- Cleanup/breakdown/purge, `_read_all_tasks`, endpoint `include_test` contrast,
  scheduler guard, `BaseService.create_task` guard, client CLI guard — covered
  in the same file.
- Targeted dashboard/scheduler regression set (142 tests): all PASS.
- T004 sandbox proof (isolated copy of the documented baseline): seeded
  20 tasks (10 acme_demo + 3 `Test ` + 4 test-/verify- ids + 3 real, incl. a
  `test-agent`-routed real task). API default showed only the 3 real tasks;
  `include_test=true` showed all 20. `dashboard cleanup` removed exactly 17:
  `acme_demo 10, test_instruction 3, test_id 4` — `Tasks: 20 -> 3`; the 3 real
  tasks survived, including the `test-agent`-routed one.
- Live `data/ai_company.db` currently holds 0 tasks (drained by the running
  executor daemon), so the live cleanup run has nothing to remove and the
  documented 17-task state only exists re-seeded. Live run deferred until the
  in-flight full `pytest tests/` completes to avoid racing a concurrent writer.
- ruff check / mypy / full pytest: pending final validation.

## Next Step

Finish final validation: `ruff check src/`, `mypy src/`, full `pytest -q -m
"not e2e"` once the concurrent full-suite run finishes; run `dashboard cleanup`
against the live DB and record actual counts; then close the change.


## Transition Note

- In progress: refined-marker cleanup + guards + API filter implemented;
  unit tests (29) + sandbox T004 proof complete; ECL docs updated. Remaining:
  final ruff/mypy/full-pytest, live-DB cleanup run after the concurrent
  `pytest tests/` finishes, then close.
