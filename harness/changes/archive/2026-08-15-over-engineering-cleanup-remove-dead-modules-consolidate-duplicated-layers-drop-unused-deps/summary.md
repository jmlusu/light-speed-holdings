---
title: "Over-engineering cleanup: remove dead modules, consolidate duplicated layers, drop unused deps"
slug: "over-engineering-cleanup-remove-dead-modules-consolidate-duplicated-layers-drop-unused-deps"
status: "completed"
location: "archive"
phase: "implement"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules: ["generator", "llm", "ml", "data", "dashboard", "orchestrator", "executor", "security", "services", "memory", "registry"]
files: [
  "src/ai_company/data/etl_pipeline.py",
  "src/ai_company/data/growth_metrics.py",
  "src/ai_company/data/quality_monitoring.py",
  "src/ai_company/data/catalog.py",
  "src/ai_company/data/memory_store.py",
  "src/ai_company/org_chart/",
  "src/ai_company/ml/anomaly.py",
  "src/ai_company/ml/complexity.py",
  "src/ai_company/ml/performance.py",
  "src/ai_company/ml/predictive_scaling.py",
  "src/ai_company/ml/prompt_optimizer.py",
  "src/ai_company/ai/evals/",
  "src/ai_company/prompts/evals/",
  "src/ai_company/prompts/analytics.py",
  "src/ai_company/security/keys.py",
  "src/ai_company/security/secrets_scanner.py",
  "src/ai_company/services/hr.py",
  "src/ai_company/services/legal.py",
  "src/ai_company/services/marketing.py",
  "src/ai_company/services/sales.py",
  "src/ai_company/services/customer_success.py",
  "src/ai_company/executor/autonomous.py",
  "src/ai_company/orchestrator/agent_protocol.py",
  "src/ai_company/orchestrator/dead_letter.py",
  "src/ai_company/orchestrator/approval_prompts.py",
  "src/ai_company/doctor/doctor.py",
  "src/ai_company/doctor/report.py",
  "src/ai_company/dashboard/retention.py",
  "src/ai_company/dashboard/kpi_collector.py",
  "src/ai_company/registry/resolver.py",
  "src/ai_company/generator.py",
  "src/ai_company/model_router.py",
  "src/ai_company/llm/cost_tracker.py",
  "src/ai_company/llm/client.py",
  "src/ai_company/dashboard/monitoring.py",
  "src/ai_company/memory/vector_store.py",
  "src/ai_company/memory/consolidation.py",
  "src/ai_company/utils/file_lock.py",
  "src/ai_company/store/file_store.py",
  "src/ai_company/executor/daemon.py",
  "src/ai_company/executor/loop.py",
  "src/ai_company/executor/agent_loop.py",
  "src/ai_company/dashboard/ws.py",
  "src/ai_company/dashboard/api.py",
  "src/ai_company/dashboard/mobile_api.py",
  "src/ai_company/orchestrator/message_bus.py",
  "templates/",
  "pyproject.toml",
  "uv.lock",
  "tmp_run_checks.py",
  "check_scripts.py",
  "verify_project.py"
]
tags: ["cleanup", "ponytail-audit", "dead-code", "deps", "refactor"]
validation_status: "pass"
created_at: "2026-08-15"
updated_at: "2026-08-15"
---

# Summary

## Outcome

Apply the repo-wide ponytail audit cuts that two independent review rounds
(ceo-advisor, chief-of-staff, cto, then cdo, cio, solution-architect,
software-architect) verified as safe: delete zero-caller modules, slim
package `__init__` re-export chains, remove dead methods and dead metric
keys, drop unused dependencies, and consolidate duplicated atomic-write /
WebSocket / prompt layers. All cuts were verified import-graph-clean and do
not collide with planned work; the Security Hardening change was parked to
open this ticket and resumes afterward.

## Decisions

- Keep the verified live keep-list even though it overlaps audit claims:
  `ml/embeddings.py`, `services/base.py` + `client_intake.py`,
  `doctor/checks.py` + `cli/doctor.py`, `data/governance.py` (retention),
  `dashboard/kpis/` + `data/kpi_pipeline.py`, `MessageBus` core
  (`send_task`, `get_all_tasks`, `get_all_tasks_raw`, `update_task`,
  `claim_task`, `heartbeat_task`, `get_task_by_id`, `count_by_status`,
  `delete_task`, `acknowledge_task`), `numpy` + `sentence-transformers`,
  `cost_tracker._export_summary`/`get_usage_summary`,
  `postmortem.md.j2` + `agents/operating-standards.md`, `autonomous.yml`
  CI workflow.
- `__init__` re-export chains (`ml/`, `services/`, `data/`) are slimmed in
  the SAME commit as the module deletions — they are the highest-risk
  coupling.
- Dead template set is 8 (incl. `department.md.j2`); the map keys
  `workflow`/`config`/`agent` come out of `_TEMPLATE_MAP` in the same
  change.
- Dead monitoring keys are removed with a deliberate rework of the derived
  gauges (`task_success_rate_pct`/`cycle_success_rate_pct`) and the
  `_live_task_summary` fallback that read them.
- `security/keys.py` + `secrets_scanner.py` land AFTER the parked Security
  Hardening change is resumed and closed (non-overlapping change).
- `ml/{anomaly,performance,predictive_scaling,prompt_optimizer,complexity}`
  are deleted as unused; the 90-day anomaly/predictive vision stays as a
  documented deliberate deferral, not a silent drop.
- Deps `scikit-learn`, `scipy`, `networkx` dropped; `uv.lock` regenerated
  in the same change or all `--frozen` flows fail.

## Validation

- Batch A gate passed: 116 passed / 1 pre-existing failure
  (`/api/v1/company-kpis` 404 from the parked Security Hardening change).
- Batch B gate passed: `ruff check src/` and `mypy src/` clean; 178 passed
  across the Batch B test surface (executor, message-bus, consolidation,
  cost-tracker, token-counter, circuit-breaker, scheduler, full-pipeline,
  monitoring/`/metrics` tests). Remaining full-suite failures are the
  pre-existing 212 from the parked Security Hardening prefix rename
  (`/api/v1` -> `/api`) + `hitl_gate` edits, not this change.
- T018 scope notes: removed the 18 never-set metric keys and the 4
  never-rendered counter increments (`agent_loop_runs_total`,
  `agent_loop_iterations_total`, `dead_letter_moved_total`,
  `executor_loop_ticks_total`). `messages_published_total` in
  `orchestrator/message_bus.py` is intentionally left (plan scoped exactly
  4 counters; `message_bus.py` overlaps the parked Security Hardening
  change). Derived gauge `task_success_rate_pct` now computes from live
  inbox state; `cycle_success_rate_pct` removed (no live data source);
  `set_metric`/`get_metrics` deleted (no callers).
- Batch C gate passed: `ruff check src/` and `mypy src/` clean (150 source
  files); 1451 passed / 212 failed full suite, where the 212 failures are
  exactly the pre-existing baseline (parked Security Hardening `/api/v1` ->
  `/api` prefix rename 404s, `hitl_gate` datetime-awareness bug,
  `websocket_broadcast` no-event-loop case) — no new failure categories
  introduced. Smokes: `init_memory` import OK; `ai-company client --help`
  renders.
- T023 scope notes: `utils/file_lock.py:atomic_write` gained a Windows
  `PermissionError` retry loop (`retries=5`); `store/file_store.py`
  `_atomic_write` replaced by `_write_content` routing through
  `utils.file_lock.atomic_write` (backup `.bak` snapshot preserved); the
  separate `store/file_lock.py` module is out of scope (used by
  `file_store.py` + tests). `executor/daemon.py` `_atomic_write_text`
  removed.
- T024 scope notes: `_bus_broadcast` (api.py) and
  `_make_broadcast_callback` (loop.py) now delegate to
  `dashboard/ws.py:make_message_bus_broadcast_callback`; dead
  `_schedule_broadcast` (api.py) removed; unused `asyncio` import dropped
  from loop.py.
- T026 scope notes: `loop.py` passes `task.instruction` raw (fixes
  double-wrap through `build_user_prompt_typed`); `context.py`
  `build_system_prompt`/`build_user_prompt` deleted; `test_executor.py`
  updated to the typed builders in `prompts.py`.

## Next Step

- Run the Plan Review gate (`plan_review: approved`), then execute the task
  list in sequencing order, gating each batch on
  `ruff check src/ && mypy src/ && pytest` per AGENTS.md section 6.
- Batch B complete -> proceed to Batch C (T020-T027).
- Batch C complete -> proceed to Batch D (T028-T030). T029 is gated on the
  parked Security Hardening change being resumed and closed first.
- Batch D deps portion complete (T028, T030): `scikit-learn`, `scipy`,
  `networkx` dropped from `pyproject.toml`; `uv.lock` regenerated in the
  same change; `uv sync --frozen` and `--frozen --extra dev` both resolve.
  They remain only as transitive deps (`sentence-transformers` →
  scikit-learn/scipy; `torch` → networkx), never imported by project code.
  T029 (`security/keys.py` + `secrets_scanner.py`) is DEFERRED — it stays
  gated on the parked Security Hardening change (see Deferred Tasks).

