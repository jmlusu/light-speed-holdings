# Plan

## Technical Approach

### 1. Registry path independence (commit `3f587e9`)

- `registry/loader.py` — `load_registry()` resolves project root deterministically (`AI_COMPANY_ROOT` env override with package-root fallback); no CWD-relative paths.
- `registry/__init__.py`, `registry/sync.py` — align resolver/sync entry points with the anchored loader.
- `cli/main.py` — lazy sub-app registration (`_LAZY_SUB_APPS`) so `--help` and hot paths never import every subcommand module.

### 2. Tool vocabulary canonicalization (commit `3f587e9`)

- `generator.py` — `_TOOL_MAP` maps legacy aliases to canonical permission keys (`websearch`/`web_search` → `webfetch`; `code_interpreter` → `bash`; `write` → `edit`; `delegate` → `task`).
- Regenerated `company/agent-registry.json` + all 127 `.opencode/agents/*.md`.

### 3. Template boilerplate dedup (commit `3f587e9`)

- New `templates/agents/operating-standards.md` (5 principles).
- All 5 templates replace inline principles with a `## Shared Standards` reference.
- `generator.py` `_write_shared_standards()` writes `.opencode/operating-standards.md`.
- `executor/context.py` — `SHARED_STANDARDS_FILENAME` + `_load_shared_standards()` fallback in `parse_agent_spec_content()` (backward compatible).

### 4. LLM error classification (commit `f4d2867`)

- `llm/providers/base.py` — `ProviderErrorCategory` enum + `classify_provider_error()` (status-code-first, keyword fallback for transport failures).
- `llm/circuit_breaker.py` — `record_failure(error_category)`, ignores `auth`.
- `llm/client.py` — `record_failure(exc.category.value)` + `get_breaker()`.
- `llm/cost_tracker.py` — bounded in-memory working set (`_MAX_RECORDS = 10_000`), token sanitization (`max(0, int(...))`).
- `executor/agent_loop.py` — breaker success/failure wiring in `_call_llm`.

### 5. Executor/store concurrency (commit `d076303`)

- `models/models.py` — `Task` lease fields (`claimed_by`, `lease_expires_at`).
- `store/file_store.py`, `store/file_lock.py` — atomic-write + platform-locking hardening.
- `executor/loop.py`, `daemon.py`, `dead_letter.py`, `autonomous.py` — lease claiming, DLQ re-enqueue delegation, bounded decision log (deque 1k), atomic history writes.
- `orchestrator/message_bus.py`, `data/{database,governance,task_store}.py` — SQLite mirror + task-store fixes.

### 6. E2E dashboard test migration (commit `5f32e6d`)

- `tests/e2e/test_dashboard_scroll.py`, `test_scroll_fix_verification.py` — replace Alpine internal `_x_dataStack` with public `window.Alpine.$data`.

## Impacted Modules And Files

- Registry: `registry/{loader,sync,__init__}.py`
- CLI: `cli/{main,executor}.py`
- Generator/templates: `generator.py`, `templates/*.md.j2`, `templates/agents/agent.md.j2`, `templates/agents/operating-standards.md` (new)
- LLM: `llm/{client,circuit_breaker,cost_tracker}.py`, `llm/providers/base.py`
- Executor: `executor/{context,agent_loop,loop,daemon,dead_letter,autonomous}.py`
- Store/orchestrator/data: `store/{file_store,file_lock}.py`, `orchestrator/message_bus.py`, `data/{database,governance,task_store}.py`, `models/models.py`
- Generated: `company-registry.yaml`, `company/agent-registry.json`, `.opencode/agents/*.md`, `.opencode/operating-standards.md`
- Tests: `tests/unit/test_{cli_commands,cli_lazy,circuit_breaker,llm,cost_tracker,agent_loop,dead_letter,database,governance_engine}.py`, `tests/e2e/test_{dashboard_scroll,scroll_fix_verification}.py`
- Docs: `docs/AUDIT-FIXES-2026-08-10.md`, `docs/STATUS.md`

## Interfaces, Data, Permissions

- New public API: `ProviderErrorCategory`, `classify_provider_error()`, `CircuitBreaker.record_failure(error_category)`, `LLMClient.get_breaker(provider_id)`, `parse_agent_spec_content()`.
- `Task` model gains `claimed_by` / `lease_expires_at` (default empty — backward compatible).
- No permission or security-boundary changes.

## Spec Gaps Found From Planning

- `cli/executor.py` DLQ delegation depends on the new `DeadLetterQueue.retry_dlq_task` method — the audit commit had to exclude it and let it land with the concurrency commit.

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tool-vocabulary change breaks card validation | Low | High | `_TOOL_MAP` + regenerated cards verified by `agents validate` (127 OK) |
| Shared-standards fallback fails for legacy cards | Low | Medium | `parse_agent_spec_content()` falls back to the shared doc; inline copy still honored first |
| Circuit-breaker behavior change alters retry dynamics | Low | Medium | `auth` excluded only; rate-limit/server/timeout still counted; tests added |
| Concurrency changes race in tests | Medium | Medium | Full suite (1805) green; lease + lock tests added |

## Verification Plan

1. `ruff check src/` — clean
2. `mypy src/` — clean (181 files)
3. `pytest` — 1805 passed, 53 deselected, 0 failures
4. `AgentGenerator().generate_all()` — 127 agents, 0 validation errors
5. `lint-ecl.ps1` — ECL structure consistent
