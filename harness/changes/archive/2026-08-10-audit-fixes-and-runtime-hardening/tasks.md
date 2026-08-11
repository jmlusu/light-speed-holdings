# Tasks

## Setup / Intake

- [x] T001 Review audit checklist and 2026-08-10 code review findings.
- [x] T002 Write `spec.md` and `plan.md`; approve plan review.

## Implementation

- [x] T010 Anchor registry loading to the package root in `src/ai_company/registry/loader.py`; add `AI_COMPANY_ROOT` override; align `registry/sync.py` and `registry/__init__.py`.
- [x] T011 Add lazy sub-app registration (`_LAZY_SUB_APPS`) to `src/ai_company/cli/main.py`.
- [x] T012 Add `_TOOL_MAP` to `src/ai_company/generator.py`; canonicalize tool vocabulary; regenerate `company/agent-registry.json` + all 127 `.opencode/agents/*.md`.
- [x] T013 Deduplicate Operating Principles into `templates/agents/operating-standards.md`; update all 5 templates; wire `_write_shared_standards()` and `parse_agent_spec_content()` fallback in `executor/context.py`.
- [x] T020 Add `ProviderErrorCategory` + `classify_provider_error()` to `src/ai_company/llm/providers/base.py`.
- [x] T021 Update `CircuitBreaker.record_failure(error_category)` (ignore `auth`), `LLMClient` (category + `get_breaker()`), `CostTracker` (bounded working set + token sanitization), and `executor/agent_loop.py` breaker wiring.
- [x] T030 Add task lease fields to `Task`; harden `store/file_store.py` + `store/file_lock.py`; update `executor/loop.py`, `daemon.py`, `dead_letter.py`, `autonomous.py` (lease claiming, DLQ delegation, bounded decision log, atomic history writes); fix SQLite mirror in `message_bus.py` + `data/{database,governance,task_store}.py`.
- [x] T040 Delegate `cli/executor.py` DLQ retry to `DeadLetterQueue.retry_dlq_task`.
- [x] T050 Migrate E2E scroll tests to `window.Alpine.$data`.

## Tests

- [x] T060 Add `tests/unit/test_circuit_breaker.py` (new) and `tests/unit/test_cli_lazy.py` (new); expand `test_llm.py`, `test_cost_tracker.py`, `test_agent_loop.py`, `test_dead_letter.py`, `test_database.py`, `test_governance_engine.py`; fix `test_cli_commands.py` for CWD-independent registry loading.

## Validation

- [x] T070 Run gates: `ruff check src/` && `mypy src/` && `pytest` — ruff/mypy clean, 1805 passed / 53 deselected / 0 failures.
- [x] T071 Run `AgentGenerator().generate_all()` — 127 agents, 0 validation errors.
- [x] T072 Update `docs/STATUS.md` and ECL summary; run `lint-ecl.ps1`.

## Deferred Tasks

- Sync `executor/tool_runner.py` runtime tool set with canonical card permissions (implement `webfetch`/`web_search`, remove `code_interpreter`) — pre-existing gap flagged in `docs/AUDIT-FIXES-2026-08-10.md`.
