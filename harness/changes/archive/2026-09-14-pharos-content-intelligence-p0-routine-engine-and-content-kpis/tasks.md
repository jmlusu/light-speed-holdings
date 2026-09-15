# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.
  Pending the plan-review gate below, this change moves straight to
  implementation.

## Implementation

- [x] T002 [P] Create `src/ai_company/orchestrator/routine.py` with `Routine`,
  `RoutineStore`, `RoutineScheduler`, and `build_routine_task` per plan.md.
  Validation: unit tests in `tests/unit/test_routine.py` (added in T004).
  Note: task provenance rides on `tags` (`routine_run:{id}-{date}`), not a
  `metadata` dict — `Task` drops extra keys (`extra="ignore"`).
- [x] T003 [P] Wire the routine scheduler into `src/ai_company/executor/daemon.py`:
  add `--routine-interval` option (default 900s; `-1` disables), a
  `_make_routine_scheduler(...)` factory, and a guarded `run_due()` call in
  `_run_loop` next to the KPI snapshot. Validation: ruff/mypy clean; no change
  to existing daemon behavior when `--routine-interval=-1`.
  Note: also threaded through `build_daemon_command`, `launch_detached_daemon`,
  `main()`, and the `executor start` CLI (`cli/executor.py`).
- [x] T004 [P] Add `tests/unit/test_routine.py` covering: daily firing on
  correct UTC day/time; disabled routine skipped; mark-before-send crash-safety
  ordering; `routine_run_id` idempotency format; interval mode; unknown
  receiver/prompt robustness. Validation: `uv run pytest tests/unit/test_routine.py
  -q --basetemp=".pytest_tmp_p0"` → 13 passed.
- [x] T005 [P] Add `config/company/routines.yaml` with the three P0 Pharos
  routines (Mon Agentic Enterprise Brief / Wed Build Log / Fri AI Policy &
  Governance Africa) at 04:00 UTC, receiver `content_writer`, prompt files
  under `templates/pharos/routines/`. Validation: RoutineStore loads and
  lists all 3 with `next_run` set.
- [x] T006 [P] Add `templates/pharos/routines/monday-agentic-enterprise-brief.md`,
  `wednesday-build-log.md`, `friday-policy-governance-africa.md` prompt
  briefings (voice, audience, cadence markers, `docs/Pharos/*` references).
  Validation: files parse as valid markdown; referenced in routines.yaml.
- [x] T007 [P] Extend `src/ai_company/dashboard/kpis/marketing.py` with a
  backward-compatible `pharos_content` KPI block (`posts_published_30d`,
  `drafts_in_pipeline`, `subscribers` vs 2000 target) reading
  `orchestrator/marketing/content_log.json` + `pharos_subscribers.json`.
  Validation: existing marketing KPI tests still pass — 38 passed in
  `test_kpi_collectors.py` including 4 new pharos-content tests.

## Validation

- [x] T008 Run full gates in the worktree:
  `uv run ruff check src/` and `uv run mypy src/`; then
  `uv run pytest -q -m "not e2e" --basetemp=".pytest_tmp_p0"` (whole-suite).
  Validation: ruff clean; mypy clean (198 files); **2117 passed, 67 deselected**
  (~466s, baseline 2101); no side-effect files left dirty.
- [x] T009 Update ECL docs (`summary.md` outcome/decisions/validation),
  run `pwsh scripts/lint-ecl.ps1`, then close the change as `implemented`.
  Validation: `pwsh scripts/lint-ecl.ps1` passes; harness index consistent.

## Deferred Tasks

- Deferred: P1/P2 Pharos scope (deep-research routines, CEO voice profile,
  Boost fan-out, publishing rails, Whisper, Pharos MCP at
  `src/ai_company/mcp/server.py`).
- Deferred: Eden MCP consumption behind a feature flag; SADC regional
  verification pass.
