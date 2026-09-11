# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [ ] T001 Confirm Plan Review gate is approved (`plan_review: approved` in `harness/changes/active/summary.md`) before implementation starts. Validate with `.\scripts\harness-change.ps1 validate`.

## Batch A — Pure deletes

- [ ] T002 [P] Delete `src/ai_company/data/etl_pipeline.py`, `data/growth_metrics.py`, `data/quality_monitoring.py`, `data/catalog.py`; verify zero imports remain (`Select-String` over `git ls-files '*.py'`).
- [ ] T003 [P] Delete `src/ai_company/org_chart/` package and `tests/test_org_chart.py`; verify `from ai_company.org_chart` appears nowhere; confirm `/api/org-chart` still builds from registry (dashboard/api.py:672).
- [ ] T004 [P] Delete `src/ai_company/prompts/evals/` and `src/ai_company/ai/evals/`; edit `tests/test_prompt_engineering.py` to drop the eval sections (keep executor-prompt + analytics tests); verify `ai_company.ai` and `prompts.evals` have no importers.
- [ ] T005 [P] Delete `src/ai_company/prompts/analytics.py`; remove its section from `tests/test_prompt_engineering.py`.
- [ ] T006 [P] Delete `src/ai_company/executor/autonomous.py` and `tests/unit/test_autonomous_escalation_audit.py`; keep `.github/workflows/autonomous.yml` (uses orchestrator tick / executor start only).
- [ ] T007 [P] Delete `src/ai_company/doctor/doctor.py` and `doctor/report.py`; keep `doctor/checks.py` + `cli/doctor.py` + `tests/unit/test_doctor.py`.
- [ ] T008 [P] Delete 8 empty `src/ai_company/models/*.py` stubs (agent, board, company, department, executive, meeting, project, workflow); KEEP `models/task.py` and `models/models.py`.
- [ ] T009 [P] Delete `src/ai_company/utils.py` (0-byte); keep `utils/` package.
- [ ] T010 [P] Delete root debug scripts `tmp_run_checks.py`, `check_scripts.py`, `verify_project.py`; confirm no references in docs/scripts/CI/harness.
- [ ] T011 [P] Delete dead templates `agent.md.j2`, `board_v2.md.j2`, `specialist_v2.md.j2`, `workflow.md.j2`, `config.md.j2`, `department.md.j2`, `sop.md.j2`, `raci.md.j2`; remove `workflow`/`config`/`agent` keys from `generator.py:_TEMPLATE_MAP`; keep `base.md.j2`, `board.md.j2`, `executive.md.j2`, `specialist.md.j2`, `postmortem.md.j2`, `agents/agent.md.j2`, `agents/operating-standards.md`; then run `AgentGenerator().generate_all()` and confirm `generated-check` (ci.yml) has no drift.
- [ ] T012 Batch A gate: `ruff check src/ && mypy src/ && pytest`.

## Batch B — Dead members on live modules

- [x] T013 Edit `src/ai_company/orchestrator/message_bus.py`: remove `purge_completed_tasks`, `purge_expired_tasks`, `purge_failed_tasks`, `reconcile_mirror`, `sync_pending_approvals`, `get_inbox`, `get_sent`, `get_subtasks`, `get_unacknowledged`, `dead_letter_task`, `get_dead_letter_tasks` (incl. lazy imports at :567,:589); KEEP `acknowledge_task` and the core method set; verify `tests/test_concurrent_inbox.py` still passes.
- [x] T014 [P] Delete `src/ai_company/orchestrator/agent_protocol.py` + `tests/unit/test_agent_protocol.py`; delete `orchestrator/approval_prompts.py` + `tests/unit/test_approval_prompts.py`; delete `orchestrator/dead_letter.py`; keep `executor/dead_letter.py`.
- [x] T015 Edit `src/ai_company/llm/cost_tracker.py`: remove `get_daily_summary`, `get_task_summary`, `get_summary`, `estimate_cost`; keep `_export_summary`/`_resolve_export_path`/`_load_total_budget`/`get_usage_summary`; update `test_cost_tracker_integration.py`, `test_cost_tracker.py`, `test_token_counter.py:130`.
- [x] T016 Edit `src/ai_company/llm/client.py` + `llm/providers/base.py`: remove `list_available_providers` and `ChatMessage`; KEEP `_parse_response` (:240,:366); remove `circuit_breaker.is_closed` + `reset` (adjust `test_circuit_breaker.py` if it asserts them).
- [x] T017 Edit `src/ai_company/memory/consolidation.py`: remove thread mode `start`/`stop`/`_run_loop`/`stats` and `ConsolidationConfig.time_interval_seconds`; keep `on_tick()` and class default used by `executor/loop.py:183-187`; rewrite `tests/integration/test_scheduler_verification.py:124-219`.
- [x] T018 Edit `src/ai_company/dashboard/monitoring.py`: delete 18 never-set metric keys + 4 never-rendered counters; rework derived gauges `task_success_rate_pct`/`cycle_success_rate_pct` (`:319-352`) and `_live_task_summary` fallback (`:600-608`); confirm no Prometheus alert rules reference removed names (`config/prometheus.staging.yml`); delete now-dead `set_metric`/`get_metrics` if callers are gone.
- [x] T019 Batch B gate: `ruff check src/ && mypy src/ && pytest`.

## Batch C — Layer consolidation + ml/services cuts

- [x] T020 Edit `src/ai_company/ml/`: delete `anomaly.py`, `complexity.py`, `performance.py`, `predictive_scaling.py`, `prompt_optimizer.py`; remove `resolve_with_complexity` (+ lazy import at model_router.py:584); slim `ml/__init__.py:7-12` to embeddings-only (keep `EmbeddingEngine`); trim `tests/unit/test_ml.py` to the embeddings section (lines ~27-130).
- [x] T021 Delete `src/ai_company/services/{hr,legal,marketing,sales,customer_success}.py`; slim `services/__init__.py:10-14` to `base` + `client_intake`; trim `tests/unit/test_services.py`; smoke-test `cli/client.py` import.
- [x] T022 Delete `src/ai_company/data/memory_store.py` (MemoryStoreDB); remove its re-export from `data/__init__.py:21,32`; surgically remove `TestMemoryStoreDB` from `tests/unit/test_data_pipeline.py` (keep live-class tests); keep `run_backfill.py` imports working.
- [x] T023 Consolidate atomic-write to one helper: add Windows `PermissionError` retry param to `utils/file_lock.py:atomic_write`; remove `store/file_store.py:_atomic_write` and `executor/daemon.py:_atomic_write_text`; route callers (`executor/autonomous.py` is deleted; `data/governance.py:374,409`, `store/file_store.py`, `executor/daemon.py:409,522`).
- [x] T024 Consolidate WS broadcast to `dashboard/ws.py:make_message_bus_broadcast_callback`; remove copies at `dashboard/api.py:61-67` and `executor/loop.py:398-416`; verify `test_websocket_integration.py` passes.
- [x] T025 Dedup `dashboard/mobile_api.py:32-66` store/load/save helpers by importing from `dashboard/api.py`; module stays (ADR-014 target, 14 endpoints); verify mobile endpoint tests pass.
- [x] T026 Fix prompt double-wrap: `executor/loop.py:521` passes `task.instruction` raw; remove now-dead `context.build_system_prompt`/`build_user_prompt` (`executor/context.py:340,407`); keep typed builders in `executor/prompts.py`; update `tests/unit/test_executor.py:71-81,140`.
- [x] T027 Batch C gate: `ruff check src/ && mypy src/ && pytest` + smoke memory init (`executor/loop.py:180` → `init_memory`) and `ai-company client --help`.

## Batch D — Deps + security (after Security Hardening resumes/closes)

- [x] T028 Edit `pyproject.toml`: drop `scikit-learn`, `scipy`, `networkx`; keep `numpy` + `sentence-transformers`; regen `uv.lock` (same commit) and verify `--frozen` installs (Dockerfile:21, ci.yml, autonomous.yml:47, governance.yml:23).
- [x] T029 (DEFERRED — blocked on parked Security Hardening change) AFTER the parked Security Hardening change is resumed and closed: delete `src/ai_company/security/keys.py` (+ `tests/unit/test_api_key_manager.py`) and `security/secrets_scanner.py` + wrappers (`command_has_shell_metacharacters`, `filter_content`, `detect_and_mask_pii`, `migrate_file_based_entries`); keep `encryption_key_manager`, `memory_encryption`, `encrypt_legacy_entries`, `rbac`, `find_shell_metacharacters`, `PIIDetector`, `get_content_filter`; update README + `docs/DEVELOPER-GUIDE.md` security promises.
- [x] T030 Batch D gate (deps portion; T029 deferred): `ruff check src/ && mypy src/ && pytest` — clean; full suite at pre-existing 211-212 baseline.

## Documentation (land across batches in lockstep)

- [x] T031 Update Developer-GUIDE MD (ML module → embeddings-only, ARCHITECTURE.md structure), README (ML bullet), SOP finance summary (get_usage_summary), agent registry (sales-owner role); update AGENT-REGISTRY-TABLE from registry.yaml fix; update .ai-company/constitution 06-GENERATOR-STANDARDS.md close-out note.

## Validation

- [ ] T032 Run full ECL close-out: `.\scripts\harness-change.ps1 validate`, update `docs/STATUS.md` per ECL section 7, record gate outcomes in `summary.md` Validation, set `validation_status: "pass"`, close via `.\scripts\harness-change.ps1 close completed`, then resume the parked Security Hardening change (`.\scripts\harness-change.ps1 resume <id>`) and confirm it still validates.

## Deferred Tasks

- Resume parked change `2026-08-15-security-hardening-...` after this change lands.
- Rebuild the evals feature (if wanted later) from scratch — both eval stacks removed.
- Optionally adopt `networkx` later for `graph/engine.py` BFS (declared unused dep dropped; hand-rolled BFS stays).
