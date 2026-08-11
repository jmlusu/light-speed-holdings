# Plan

## Technical Approach

- Executed Sprint 7: tool vocabulary sync, HITL expiry sweep, mypy strict warn_return_any, test coverage hardening, doc reconciliation.

## Impacted Modules And Files

- `src/ai_company/executor/tool_runner.py`, `hitl_gate.py`, `prompts.py`
- `src/ai_company/orchestrator/approval.py`, `tier_rules.py`
- `src/ai_company/executor/daemon.py`
- `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/STATUS.md`, `AGENTS.md`

## Interfaces, Data, Permissions

- Canonical tool vocabulary: `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`.
- HITL expiry sweep integrated into daemon governance cadence.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Verified via ruff, mypy strict, and unit test suites.

## Verification Plan

- `uv run ruff check src/ tests/`
- `uv run mypy src/`
- `uv run pytest tests/unit/ -q`
