# Plan

## Technical Approach

P0 wires a `routine:` scheduler into the existing daemon loop using the same
time-gated pattern as `KPISnapshotScheduler` (`dashboard/kpis/scheduler.py`),
with a persistent routine store for crash-safe firing. Each fire enqueues a
fresh MessageBus Task for a valid registry receiver; idempotency and
observability ride on Task `tags` (`pharos-routine`, `routine:{id}`,
`routine_run:{id}-{UTC date}`) — the `Task` model drops arbitrary `metadata`
dicts (`extra="ignore"`).

New module `src/ai_company/orchestrator/routine.py`:

- `Routine(BaseModel)`: `id`, `name`, `receiver_id` (must exist in the
  registry), `enabled` (default True), `schedule` (day-of-week ISO or
  `interval_minutes`), `time_utc` (HH:MM, optional for daily), `prompt_file`
  (path under `templates/pharos/routines/`), `model` / `budget_tokens`
  (metadata, P0 passthrough), `outputs` (optional), `metadata` (mutable dict).
- `RoutineStore(FileStore)`: loads `config/company/routines.yaml`; keeps
  per-routine `last_run`/`next_run` (UTC ISO) persisted in the same YAML via
  FileStore (mirrors `orchestrator/scheduler.py` state handling). `get_due(now)`
  returns enabled routines whose `next_run` elapsed; `mark_run(routine, now)`
  advances `next_run` (daily: next matching day+time in UTC; interval:
  `now + interval_minutes`). Crash-safety: persist `mark_run` BEFORE the
  caller sends the task.
- `build_routine_task(routine, now, prompt_text)` → `Task` with
  `id="routine-{id}-{yyyymmdd[-hhmm for interval]}"`, `instruction` from the
  prompt file (token `{date}` → today's date), `receiver_id`, priority MEDIUM,
  `tags=["pharos-routine", "routine:{id}", "routine_run:{id}-{yyyymmdd}"]`.
- `RoutineScheduler(interval_seconds, bus, store, clock)`: like
  `KPISnapshotScheduler` — `run_due(now)` checks `interval_seconds`, delegates
  `store.get_due(now)`, builds+enqueues via bus, `store.mark_run` first if the
  bus enqueue succeeds (fires are best-effort and never raise).

Daemon wiring in `src/ai_company/executor/daemon.py`:

- New `--routine-interval` CLI param (default e.g. 900s; `-1` disables), a
  `_make_routine_scheduler(...)` factory, and a guarded
  `self._routine_scheduler.run_due()` call in `_run_loop` alongside the KPI
  snapshot, wrapped in try/except like existing best-effort schedulers.

Config + prompts:

- `config/company/routines.yaml` — P0 Pharos definitions:
  - `pharos_agentic_enterprise_brief` (Mon 04:00 UTC, `content_writer`,
    `templates/pharos/routines/monday-agentic-enterprise-brief.md`)
  - `pharos_build_log` (Wed 04:00 UTC, `content_writer`,
    `templates/pharos/routines/wednesday-build-log.md`)
  - `pharos_policy_governance` (Fri 04:00 UTC, `content_writer`,
    `templates/pharos/routines/friday-policy-governance-africa.md`)
- Three prompt files under `templates/pharos/routines/*.md`, each with a
  briefing instruction (voice, audience, cadence markers) referencing
  `docs/Pharos/*` for the agent to follow.

Content KPIs (P0, lightweight):

- Extend `src/ai_company/dashboard/kpis/marketing.py` with a `pharos_content`
  block: `posts_published_30d`, `drafts_in_pipeline`, `subscribers` (vs target
  2000), sourced from `orchestrator/marketing/content_log.json` +
  `orchestrator/marketing/pharos_subscribers.json` (both `_load_json`, tolerant
  of missing files). Existing marketing KPI keys untouched (backward-compatible).

## Impacted Modules And Files

- `src/ai_company/orchestrator/routine.py` (new)
- `src/ai_company/executor/daemon.py` (wire `--routine-interval` + scheduler)
- `src/ai_company/dashboard/kpis/marketing.py` (pharos_content KPIs)
- `config/company/routines.yaml` (new)
- `templates/pharos/routines/*.md` (new, 3 prompts)
- `harness/changes/active/{spec,plan,tasks,summary}.md` + `reviews/review.md`
- `docs/STATUS.md`
- `tests/unit/test_routine.py` (new)

## Interfaces, Data, Permissions

- Read: `config/company/routines.yaml`, `config/company/agent-registry.yaml`
  alias → `company-registry.yaml` (receiver validation),
  `templates/pharos/routines/*.md`, `orchestrator/marketing/content_log.json`,
  `orchestrator/marketing/pharos_subscribers.json`.
- Write: routines.yaml `last_run`/`next_run` via FileStore; MessageBus task
  enqueue (`orchestrator/message_bus.py`).
- No authz changes (daemon runs with existing executor permissions; routine
  tasks are normal bus tasks).

## Spec Gaps Found From Planning

- Worktree registry (feature/cleanup-dummy-tasks) has no `thought-leadership-*`
  agents; P0 receiver is `content_writer` (valid registry id). Pharos-specific
  agents remain on `research/swot-baseline` and are out of P0 scope.
- The legacy `scheduler.cycles` key is not consumed by Python; P0 adds its own
  `RoutineStore` + YAML instead of reusing `Scheduler` (no coupling to dead config).

## Risks And Mitigations

- Double-fire after crash → mark `next_run` BEFORE enqueue (crash-safe ordering).
- Unknown receiver id → validate against `company-registry.yaml` at store load;
  invalid routines skipped with a warning, never raised.
- Prompt file missing → routine logs a warning and skips the fire (best-effort).
- KPI shape regression → pharos_content is an additive key; targeted marketing
  KPI tests must still pass.
- Daemon startup regression → scheduler factory is optional; `--routine-interval=-1`
  keeps the previous behavior.

## Verification Plan

1. `uv run ruff check src/`
2. `uv run mypy src/`
3. `uv run pytest -q -m "not e2e" --basetemp=".pytest_tmp_p0"` (new
   `tests/unit/test_routine.py` included; whole-suite gate).
4. `pwsh scripts/lint-ecl.ps1` (harness/docs gate).
5. Manual: `uv run ai-company --help` still lists commands; daemon dry check
   via test coverage of `run_due` (no long-running daemon spawn in tests).
