---
title: "Audit fixes and runtime hardening"
slug: "audit-fixes-and-runtime-hardening"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["registry", "generator", "llm", "executor", "store"]
files: ["src/ai_company/generator.py", "src/ai_company/executor/context.py", "src/ai_company/registry/loader.py", "src/ai_company/registry/sync.py", "src/ai_company/registry/__init__.py", "src/ai_company/cli/main.py", "src/ai_company/cli/executor.py", "src/ai_company/llm/providers/base.py", "src/ai_company/llm/circuit_breaker.py", "src/ai_company/llm/client.py", "src/ai_company/llm/cost_tracker.py", "src/ai_company/executor/agent_loop.py", "src/ai_company/executor/loop.py", "src/ai_company/executor/daemon.py", "src/ai_company/executor/dead_letter.py", "src/ai_company/executor/autonomous.py", "src/ai_company/store/file_store.py", "src/ai_company/store/file_lock.py", "src/ai_company/orchestrator/message_bus.py", "src/ai_company/data/database.py", "src/ai_company/data/governance.py", "src/ai_company/data/task_store.py", "src/ai_company/models/models.py", "templates/base.md.j2", "templates/executive.md.j2", "templates/specialist.md.j2", "templates/board.md.j2", "templates/agents/agent.md.j2", "tests/unit/test_cli_commands.py", "tests/unit/test_cli_lazy.py", "tests/unit/test_circuit_breaker.py", "tests/unit/test_llm.py", "tests/unit/test_cost_tracker.py", "tests/unit/test_agent_loop.py", "tests/unit/test_dead_letter.py", "tests/unit/test_database.py", "tests/unit/test_governance_engine.py", "tests/e2e/test_dashboard_scroll.py", "tests/e2e/test_scroll_fix_verification.py"]
tags: ["audit", "hardening", "circuit-breaker", "concurrency", "tool-vocabulary", "registry", "templates"]
validation_status: "pass"
created_at: "2026-08-10"
updated_at: "2026-08-10"
---

# Summary

## Outcome

Audit-driven hardening shipped in 4 commits:

- `3f587e9` — Audit fixes: registry loading anchored to the package root (`AI_COMPANY_ROOT` override, CWD-independent), lazy CLI sub-app registration, canonical tool-vocabulary across all 127 agent cards (`websearch`/`web_search` → `webfetch`, `code_interpreter` → `bash`, `write` → `edit`, `delegate` → `task`), and Operating Principles deduplicated into a shared `operating-standards.md`. Documented in `docs/AUDIT-FIXES-2026-08-10.md`.
- `f4d2867` — LLM error classification: new `ProviderErrorCategory` enum + `classify_provider_error()` in `llm/providers/base.py`; circuit breaker now records failures by category and ignores `auth` (no self-healing path, so auth failures never blacklist a provider); `get_breaker()` accessor; loop wiring in `agent_loop.py`; bounded cost-tracker working set with token sanitization.
- `d076303` — Executor/store concurrency: task lease fields (`claimed_by`, `lease_expires_at`), store locking/atomic-write hardening, DLQ re-enqueue delegation, bounded in-memory state (cost log 10k, decision log 1k), SQLite mirror fixes.
- `5f32e6d` — E2E dashboard tests migrated from Alpine internal `_x_dataStack` to the public `Alpine.$data` API.

## Decisions

- Tool vocabulary reduced to one canonical set per OpenCode v2 permission keys; generated cards are the source of truth.
- Only Operating Principles were deduplicated — Success Metrics and Escalation stay type-specific (executive/specialist/board/default) to avoid capability loss.
- Provider failures are classified for breaker/retry decisions; `auth` failures never trip the circuit breaker.
- In-memory logs are bounded; the authoritative trail persists to JSONL/SQLite on disk.
- Known gap (pre-existing, out of scope): `executor/tool_runner.py` still carries `code_interpreter` and has no `web_search` implementation — runtime tools now lag the advertised card permissions. Flagged for follow-up.

## Validation

- `ruff check src/` — clean
- `mypy src/` — clean (181 files)
- `pytest` — 1805 passed, 53 deselected (e2e), 0 failures
- pre-commit hooks — all passed on each of the 4 commits
- `AgentGenerator().generate_all()` — 127 agents, 0 validation errors

## Next Step

- Close change: update `docs/STATUS.md`, archive, run `lint-ecl.ps1`.
