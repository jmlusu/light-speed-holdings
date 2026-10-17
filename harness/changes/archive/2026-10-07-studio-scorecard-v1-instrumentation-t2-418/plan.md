# Plan

## Technical Approach

- **P1 Task events (additive):** optional fields on `Task` (`venture_id="studio-core"`, `model_id=""`, `cost_usd=0.0`, `latency_ms`, `manual_intervention=False`, `pause_log=[]`); emit `venture_id`/`model_id`/`cost_usd` at `MessageBus.send_task`/`update_task_status` and executor completion via existing `TaskResult.cost_usd`/`model`; structured `studio_correction` audit event on ApprovalGate overrides with `correlation_id`; bounded label sets only.
- **P2 Studio tracker:** new `company/studio_tracker.yaml` (COO-owned): per venture `stage`, `thesis_approved`, `deploy`, `pauses[]`, plus CFO section (`contracted_arr`, `verified_cost_avoidance`, `capital_consumed`, MWK/USD). Missing gate timestamps → `no_data`, never `0d`.
- **P3 Collector:** new `src/ai_company/dashboard/kpis/studio.py` `StudioScorecardCollector` (ATC / velocity_days / correction_per_1k / capital_efficiency + portfolio per-venture + risk strip inputs), registered in `ALL_COLLECTORS`; 30-day baseline = measurement-only (`status: info`); formulas per scoreboard-v1 §Row 1.
- **P4 Dashboard:** `GET /api/v1/studio-scorecard` (RBAC-gated like other KPI reads) + Studio Scorecard page/section (Row 1 big four, Row 2 portfolio cards, Row 3 risk strip); single data owner, no duplicated hard-codes.
- **P5 Verify telemetry:** staging trigger of each path; structured-log spot check (no secrets/PII); `validate-drift` + `test_doc_drift` green.

## Impacted Modules And Files

- `src/ai_company/models/models.py` — additive `Task` fields only.
- `src/ai_company/orchestrator/message_bus.py` — carry new fields through send/update (no behavior change).
- `src/ai_company/executor/loop.py` (or agent_loop) — populate `model_id`/`cost_usd`/latency on completion where `TaskResult` already has them.
- `src/ai_company/orchestrator/approval.py` — structured correction event on override (additive log line).
- `company/studio_tracker.yaml` — NEW tracker + CFO inputs.
- `src/ai_company/dashboard/kpis/studio.py` — NEW collector; `kpis/__init__.py` — register it.
- `src/ai_company/dashboard/api.py` (+ template under dashboard templates) — NEW endpoint + page/section.
- `tests/unit/test_studio_scorecard.py` — NEW collector tests.
- `harness/changes/active/*` — ECL records only.

## Interfaces, Data, Permissions

- New read API `GET /api/v1/studio-scorecard` under existing dashboard RBAC; no new write endpoints; no permission changes. Tracker YAML is COO-edited config, read-only at runtime.

## Spec Gaps Found From Planning

- None. Action-volume source for correction denominator confirmed as audit/tool-call trail.

## Risks And Mitigations

- `Task` schema change breaks old inbox/SQLite rows → optional fields with defaults; readers use `.get()` with fallbacks.
- Velocity pauses gamed → every pause needs reason + dates; internal delay always counts.
- Capital cited before ratification → collector emits `no_data` + qualifier until CFO inputs present.
- Concurrent sessions editing dashboard files (known hazard) → `git status` snapshot before/after full suite; isolated `--basetemp`.

## Verification Plan

- `uv run ruff check src/` clean; `uv run mypy src/` clean (strict).
- New unit tests green + full non-e2e `pytest` to completion, listed in `validation_results`.
- Manual smoke: collector on empty store → all `no_data`; on seeded tasks → correct ATC/correction math.
- `pwsh scripts/maintenance/validate-drift.ps1` green; `pwsh scripts/maintenance/lint-ecl.ps1` green.
