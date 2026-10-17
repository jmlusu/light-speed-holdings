---
title: "Pharos Content Intelligence P0 - Routine Engine and Content KPIs"
slug: "pharos-content-intelligence-p0-routine-engine-and-content-kpis"
status: "completed"
location: "archive"
phase: "implement"
intake_status: "done"
spec_review: "approved"
plan_review: "approved"
modules:
  - "src/ai_company/orchestrator/routine.py"
  - "src/ai_company/executor/daemon.py"
  - "src/ai_company/dashboard/kpis/marketing.py"
  - "src/ai_company/cli/executor.py"
files:
  - "config/company/routines.yaml"
  - "templates/pharos/routines/monday-agentic-enterprise-brief.md"
  - "templates/pharos/routines/wednesday-build-log.md"
  - "templates/pharos/routines/friday-policy-governance-africa.md"
  - "harness/changes/active/spec.md"
  - "harness/changes/active/plan.md"
  - "harness/changes/active/tasks.md"
  - "docs/STATUS.md"
  - "tests/unit/test_routine.py"
  - "tests/unit/test_kpi_collectors.py"
tags:
  - "pharos"
  - "content-intelligence"
  - "scheduler"
  - "routines"
  - "marketing-kpi"
validation_status: "pass"
created_at: "2026-09-13"
updated_at: "2026-09-14"
---

# Summary

## Outcome

P0 of ADR-020 ("Pharos Content Intelligence"): a `routine:` scheduler inside
the existing executor daemon loop that fires configured Pharos content
routines (Mon Agentic Enterprise Brief / Wed Build Log / Fri AI Policy &
Governance Africa) as fresh, idempotent MessageBus Tasks, plus a
backward-compatible `pharos_content` KPI block in the marketing collector.
Establishes the governed content-intelligence loop (research → draft → publish
→ measure) on infrastructure the company already owns.

## Decisions

- A new `RoutineStore`/`RoutineScheduler` (`orchestrator/routine.py`), not the
  legacy `Scheduler`/`scheduler.cycles` file (which the Python scheduler does
  not consume). Firing pattern mirrors `KPISnapshotScheduler` in the daemon loop.
- Daily routines persist `next_run` (UTC) in `config/company/routines.yaml`;
  `mark_run` is persisted BEFORE the bus enqueue (crash-safe, no double-fire).
- Provenance rides on Task `tags` (`pharos-routine`, `routine:{id}`,
  `routine_run:{id}-{UTC date}`) with task id `routine-{id}-{yyyymmdd}` (daily)
  or `routine-{id}-{yyyymmdd-hhmm}` (interval). The `Task` model drops arbitrary
  `metadata` dicts (`extra="ignore"`), so plan.md's `metadata.routine_run_id`
  framing was reconciled to `tags` in the implementation.
- P0 receiver is `content_writer` (valid registry id on this branch); Pharos-
  specific agents only exist on `research/swot-baseline` and are out of P0 scope.
- `pharos_content` KPIs are additive to the marketing collector; existing keys
  untouched.

## Validation

- **T002-T007 implemented.** `src/ai_company/orchestrator/routine.py`
  (Routine/RoutineStore/RoutineScheduler/build_routine_task/_clock_now); daemon
  `--routine-interval` (default 900s, `-1` disables) threaded through
  `build_daemon_command`, `launch_detached_daemon`, `executor start` CLI, and
  `main()`; `config/company/routines.yaml` with the 3 Pharos routines; three
  prompt templates under `templates/pharos/routines/`; `pharos_content` KPI
  block + 4 new collector tests.
- **T008 gates (worktree, all green):** `uv run ruff check src/` clean;
  `uv run mypy src/` clean (198 files); `uv run pytest -q -m "not e2e"
  --basetemp=".pytest_tmp_p0"` → **2117 passed, 67 deselected** in ~466s
  (baseline was 2101; +13 routine tests, +3 KPI tests). No side-effect files
  left dirty by the run.
- **T009:** ECL docs reconciled (`summary.md`, `tasks.md`), `docs/STATUS.md`
  updated with the 2026-09-13 entry, `pwsh scripts/lint-ecl.ps1` passes, change
  closed as `implemented`.

## Next Step

- P1/P2 Pharos scope remains Deferred in `tasks.md` (deep-research routines,
  CEO voice profile, Boost fan-out, publishing rails, Whisper, Pharos MCP at
  `src/ai_company/mcp/server.py`; Eden MCP consumption behind a feature flag).
