# Plan: Remove Dummy Tasks & Wire Real Organizational Data

## Context
The CEO dashboard shows dummy/test data (7 test tasks) and demo data (10 Acme Corp tasks) in the "Recent Tasks" widget. The user wants to eliminate all simulated data and wire everything to reflect real organizational activity.

## Data Flow (Current)
```
Task Creation (API/CLI/Scheduler)
    ↓
MessageBus.send_task()
    ↓
┌─────────────────┬──────────────────┐
│ SQLite (primary)│ inbox.json (fallback)│
│ data/ai_company.db │ .opencode/inbox.json │
└─────────────────┴──────────────────┘
    ↓
Dashboard API → GET /api/v1/tasks
    ↓
Frontend → tasks.slice(0, 10) → "Recent Tasks" widget
```

## Changes

> Detection contract is the approved spec (see spec.md): a task is demo/test
> iff `proj-acme-chatbot` appears in id or instruction, instruction starts with
> `Test `, or the id starts with `test-`/`verify-`. The receiver name is NOT a
> marker — the real `test-agent` is legitimate routing.

### 1. Detection + Cleanup in TaskStore
**File:** `src/ai_company/data/task_store.py`
- `is_test_task()` implements the refined markers in Python.
- SQL predicates `_ACME_DEMO_PREDICATE`, `_TEST_INSTRUCTION_PREDICATE`,
  `_TEST_ID_PREDICATE`, `_TEST_TASK_WHERE` mirror `is_test_task` using
  case-sensitive `instr()`/`GLOB` (not `LIKE`) so real lowercase `test ...`
  instructions are never deleted.
- `cleanup_test_tasks()` deletes rows matching `_TEST_TASK_WHERE` and returns
  the count.
- `test_task_breakdown()` returns per-class counts
  (`acme_demo`/`test_instruction`/`test_id`/`total`).
- `purge_all_tasks()` removes every row.

### 2. Cleanup CLI Command
**File:** `src/ai_company/cli/dashboard.py`
- `ai-company dashboard cleanup` (with `--db-path` and `--purge-all`).
- Default mode prints per-class test/demo counts then removes them.
- Purge mode removes all tasks.

### 3. Filter Test Tasks at API Read Time
**File:** `src/ai_company/dashboard/api.py`
- `_read_all_tasks(*, include_test=False)` filters demo/test tasks out by
  default using `TaskStore.is_test_task` (SQLite-first, inbox-file fallback).
- `GET /api/v1/tasks` and `GET /api/v1/tasks/paginated` accept `include_test`
  query param (default `false`) and pass it through.

### 4. Block Test Data at CLI Creation Points
**File:** `src/ai_company/cli/specialists.py`
- Task creation already guards with `TaskStore.is_test_task`.

**File:** `src/ai_company/cli/client.py`
- `create_engagement` builds a probe instruction mirroring the
  `ClientIntakeService` template and rejects it with `typer.Exit(1)` if it
  matches the detection contract.

### 5. Block Test Data at Scheduler + Service Base
**File:** `src/ai_company/orchestrator/scheduler.py`
- `create_pending_tasks` skips templates whose rendered task matches
  `TaskStore.is_test_task`.

**File:** `src/ai_company/services/base.py`
- `create_task` raises `ValueError` for instructions matching the detection
  contract — central choke point that also covers onboarding.

### 6. T003 scripts kept + fixed (classification decision)
**File:** `scripts/restore_acme_tasks.py`
- Kept: it is the demo-data seed utility used to exercise cleanup/API filters.
- Fixed: every created task now carries a `[proj-acme-chatbot-...]` marker;
  validates each task against `is_test_task`; prints a cleanup warning.

**File:** `scripts/backfill_decompositions.py`
- Kept: it is a real-data backfill from `dashboard/backfill/*.json`.
- Fixed: uses `init_database(get_database_path())` and skips demo/test
  subtasks via the `is_test_task` guard.

### 7. Run Database Cleanup
- Execute cleanup against `data/ai_company.db` (reports actual counts).
- Verified against a sandbox copy seeded with the documented baseline
  (7 test + 10 Acme = 17 removed, 3 real survive incl. a `test-agent`-routed
  task).

## Verification
1. Unit tests for detection, cleanup, breakdown, purge, API filtering,
   scheduler/service guards, and client CLI guard:
   `uv run pytest tests/unit -k "task or dummy or is_test" --basetemp=<tmp>`
2. Run `ruff check src/` — no lint errors
3. Run `mypy src/` — no type errors
4. Run full `pytest -q -m "not e2e"` — no regressions
5. `ai-company dashboard cleanup` — removes only test/demo rows
6. `GET /api/v1/tasks` default hides demo/test; `?include_test=true` restores
