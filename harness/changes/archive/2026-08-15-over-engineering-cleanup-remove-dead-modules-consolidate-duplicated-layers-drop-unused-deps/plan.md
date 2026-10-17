# Plan

## Technical Approach

Apply the audit cuts in four sequenced batches. Every batch keeps the
verified keep-list intact and ships its package `__init__` slims and test
co-changes in the SAME commit. Batch gates: `ruff check src/ && mypy src/ &&
pytest`; batch 1 additionally regenerates agents and re-checks `generated-check`.

**Batch A — pure deletes (no behavior surface):**
- `src/ai_company/data/{etl_pipeline,growth_metrics,quality_monitoring,catalog}.py`
- `src/ai_company/org_chart/` (whole package; delete `tests/test_org_chart.py`)
- `src/ai_company/prompts/evals/` + `src/ai_company/ai/evals/` (both eval stacks)
- `src/ai_company/prompts/analytics.py`
- `src/ai_company/executor/autonomous.py`
- `src/ai_company/doctor/{doctor,report}.py` (keep `doctor/checks.py`, `cli/doctor.py`)
- 8 empty `src/ai_company/models/*.py` stubs (agent, board, company, department,
  executive, meeting, project, workflow) — NOT `task.py`
- `src/ai_company/utils.py` (0-byte)
- Root debug scripts `tmp_run_checks.py`, `check_scripts.py`, `verify_project.py`
- Dead templates: `agent.md.j2` (root), `board_v2.md.j2`, `specialist_v2.md.j2`,
  `workflow.md.j2`, `config.md.j2`, `department.md.j2`, `sop.md.j2`, `raci.md.j2`
  + drop `workflow`/`config`/`agent` keys from `generator._TEMPLATE_MAP`
  (keep `base`, `board`, `department`? NO — keep `base.md.j2`, `board.md.j2`,
  `executive.md.j2`, `specialist.md.j2`, `postmortem.md.j2`,
  `agents/agent.md.j2`, `agents/operating-standards.md`)

**Batch B — dead members on live modules:**
- `orchestrator/message_bus.py`: remove `purge_completed_tasks`,
  `purge_expired_tasks`, `purge_failed_tasks`, `reconcile_mirror`,
  `sync_pending_approvals`, `get_inbox`, `get_sent`, `get_subtasks`,
  `get_unacknowledged`, `dead_letter_task`, `get_dead_letter_tasks`
  (the lazy imports of `orchestrator/dead_letter` at message_bus.py:567,589
  go with them). Keep `acknowledge_task`.
- `orchestrator/{agent_protocol,dead_letter,approval_prompts}.py` (whole files)
- `llm/cost_tracker.py`: remove `get_daily_summary`, `get_task_summary`,
  `get_summary`, `estimate_cost`; keep `_export_summary`/`_resolve_export_path`/
  `_load_total_budget`/`get_usage_summary` (dashboard cost view reads
  `orchestrator/cost_tracker.json`).
- `llm/client.py`: remove `list_available_providers`, `ChatMessage`
  (providers/base.py); keep `_parse_response` (live at :240,366).
- `llm/circuit_breaker.py`: remove `is_closed` + `reset` (check
  `test_circuit_breaker.py` asserts first).
- `memory/consolidation.py`: remove background-thread mode
  (`start`/`stop`/`_run_loop`/`stats` + `ConsolidationConfig.time_interval_seconds`);
  keep `on_tick()` and the class used by `executor/loop.py:183-187`.
- `dashboard/monitoring.py`: delete the 18 never-set keys and 4 never-rendered
  counters; rework the derived gauges `task_success_rate_pct`/`cycle_success_rate_pct`
  (`monitoring.py:319-352`) and `_live_task_summary` fallback (:600-608) so they
  no longer read removed keys; confirm staging Prometheus config has no alert
  rules on removed names (verified none).

**Batch C — layer consolidation + ml/services cuts:**
- `ml/{anomaly,complexity,performance,predictive_scaling,prompt_optimizer}.py`
  + `model_router.resolve_with_complexity` (and its lazy import); slim
  `ml/__init__.py:7-12` to embeddings-only (keep `EmbeddingEngine` export).
- `services/{hr,legal,marketing,sales,customer_success}.py`; slim
  `services/__init__.py:10-14` to `base` + `client_intake` (keep
  `BaseService`, `ServiceResult`, `ClientIntakeService`, `GovernanceGateError`).
- `data/memory_store.py` (`MemoryStoreDB`) + remove its re-export from
  `data/__init__.py:21,32` (keep the other 11 data re-exports working;
  `run_backfill.py` imports must stay green or it is deleted too).
- Consolidate atomic-write: one canonical helper (base: `utils/file_lock.py`
  `atomic_write`) with a Windows `PermissionError` retry parameter; remove
  `store/file_store.py:_atomic_write` and `executor/daemon.py:_atomic_write_text`.
- Consolidate WS broadcast: one bridge from `dashboard/ws.py`
  (`make_message_bus_broadcast_callback`); replace copies at
  `dashboard/api.py:61-67` and `executor/loop.py:398-416`.
- `dashboard/mobile_api.py:32-66` helpers (`_get_store`/`_load_*`/`_save_*`):
  import from `dashboard/api.py` instead of re-defining (dedup only — module stays).
- Prompt double-wrap fix: `executor/loop.py:521` passes `task.instruction` raw
  instead of `context.build_user_prompt(...)` output; `agent_loop.py:155`
  keeps its single typed wrap. `context.build_system_prompt`/`build_user_prompt`
  become dead after the fix — remove them (keep typed builders in `prompts.py`).

**Batch D — deps + security (last):**
- `pyproject.toml`: drop `scikit-learn`, `scipy`, `networkx`; keep `numpy` +
  `sentence-transformers`. Regen `uv.lock` (same commit) for `--frozen` flows.
- `security/keys.py` + `security/secrets_scanner.py` + wrappers
  (`command_has_shell_metacharacters`, `filter_content`,
  `detect_and_mask_pii`, `migrate_file_based_entries`) — ONLY after the parked
  Security Hardening change is resumed and closed; then run in a non-overlapping
  change and update README + `docs/DEVELOPER-GUIDE.md` security promises.

## Impacted Modules And Files

- Deletions: see Technical Approach per batch.
- Package `__init__` edits (same commit as deletions): `ml/__init__.py`,
  `services/__init__.py`, `data/__init__.py`.
- Source edits: `generator.py` (`_TEMPLATE_MAP`), `model_router.py`,
  `orchestrator/message_bus.py`, `llm/{client,cost_tracker,circuit_breaker}.py`,
  `llm/providers/base.py`, `memory/{consolidation,vector_store}.py`,
  `dashboard/{monitoring,api,ws,mobile_api}.py`, `executor/{loop,agent_loop,daemon}.py`,
  `store/file_store.py`, `utils/file_lock.py`.
- Tests to edit/delete: `test_data_pipeline.py` (surgical), `test_org_chart.py`
  (delete), `test_ml.py` (keep embeddings section), `test_services.py`,
  `test_prompt_engineering.py` (evals+analytics sections), `test_agent_protocol.py`
  (delete), `test_approval_prompts.py` (delete), `test_autonomous_escalation_audit.py`
  (delete), `test_kpi_analytics.py`, `test_kpi_collectors.py`,
  `test_pipeline.py:164-201`, `test_scheduler_verification.py:124-219`,
  `test_cost_tracker_integration.py`, `test_cost_tracker.py`, `test_token_counter.py:130`,
  `test_api_key_manager.py` (delete), `test_circuit_breaker.py` (if reset asserts),
  `test_executor.py:71-81,140`.
- Docs to update in lockstep: README (ML + secrets-scanner bullets),
  `docs/DEVELOPER-GUIDE.md:319-333,351`, `docs/ARCHITECTURE.md`,
  `docs/sop/operations-sop.md:131`, `docs/sop-cost-management.md`,
  `docs/sop/finance-sop.md:290`, `docs/sop-incident-response*.md`,
  `docs/research/org-health-telemetry-sources.md:28`,
  `docs/AGENT-REGISTRY-TABLE.md:58-60`, `docs/PROMPT-ENGINEERING-GUIDE.md`,
  `.ai-company/constitution/06-GENERATOR-STANDARDS.md`, plus a deliberate-deferral
  note for anomaly/predictive vision (`CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md:646`).
- `pyproject.toml` + `uv.lock`.

## Interfaces, Data, Permissions

- No public API/CLI contract changes: `ai-company --help` and every subcommand
  surface is unchanged (deleted modules were not registered commands).
- `orchestrator/cost_tracker.json` write path is preserved (dashboard cost views).
- `/metrics` sheds never-populated series only; derived gauges reworked; no
  alert rules reference removed names.
- `org_chart.yaml` continues to be written by `builder/__init__.py:125-144`
  (unaffected); `/api/org-chart` builds from the registry via graph engine.
- No data migrations: removed stores were never written by live code except
  the two-dead_letter collision (`.opencode/dead_letter.json`), which the cut
  resolves in favor of `executor/dead_letter.py`.

## Spec Gaps Found From Planning

- Audit listed 7 dead templates; verified count is 8 (add `department.md.j2`).
- Audit claimed `registry/resolver.py` was a 0-byte stub; it is live — NOT cut.
- Audit claimed `vector_store._fallback_search` dead; it is the default recall
  path — NOT cut.
- Audit claimed `oauth2.py`/`token_bucket.py` dead; they are live+documented — NOT cut.
- `set_metric()` becomes fully dead after `data/{etl_pipeline,quality_monitoring}.py`
  are removed — fold into Batch B monitoring cleanup.

## Risks And Mitigations

- `__init__` re-export chains break at import time if slims don't ship in the
  same commit → mitigate: each batch pairs deletions with its `__init__` edit;
  smoke-test memory init (`executor/loop.py:180` → `init_memory`) and
  `cli/client.py` after Batch C.
- Derived monitoring gauges zero out if keys removed without rework →
  mitigate: rework `monitoring.py:319-352,600-608` in the same change.
- `uv.lock` drift breaks `--frozen` CI/Docker → mitigate: regen lock in Batch D.
- `security/keys.py` overlaps the parked Security Hardening change → mitigate:
  sequence Batch D after that change closes.
- Test breakage surface (~16 files) → mitigate: run `pytest` per batch; use
  surgical test edits (several files also cover live classes).
- `execute_task`/`execute_task_stream` become production-orphaned after evals
  cut → accept: they remain tested public API on `LLMClient`; future evals
  feature rebuilds from scratch.

## Verification Plan

- Per batch: `ruff check src/` && `mypy src/` && `pytest` (AGENTS.md section 6).
- Batch A: `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"`
  and confirm `generated-check` (ci.yml) has no drift.
- Batch C: smoke memory init path and `ai-company client --help`.
- Batch D: `make lock` (uv.lock) then a `--frozen` install check.
- Final: `.\scripts\harness-change.ps1 validate`, update `docs/STATUS.md`
  per ECL section 7, resume the parked Security Hardening change.
- Record outcomes in `summary.md` Validation section and set
  `validation_status: "pass"` before close.
