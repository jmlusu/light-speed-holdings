# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-07-16

## Current State

- **Harness**: Core ECL harness initialized. AGENTS.md, ECL, STATUS, ARCHITECTURE, change lifecycle scripts, and auto-evolve in place.
- **Generator**: Single `company-registry.yaml` → single `templates/agents/agent.md.j2` → `.opencode/agents/*.md`. Uses OpenCode-native format (`mode: subagent` + `permission:` blocks).
- **Tests**: 16 passing, 2 pre-existing failures in `test_model_router.py` (escalation/approval context tier mismatch).
- **Lint**: Clean (`ruff check src/`).
- **Type check**: Clean (`mypy src/`).

## Pre-existing Issues

- `test_escalation_context_uses_premium` and `test_approval_context_uses_premium` fail — `ModelRouter.resolve()` returns `standard` tier for escalation/approval contexts instead of `premium`.
- Unused import `json` in `src/ai_company/cli/models.py:68` (ruff F401).

## Recent Work

- Consolidated to single generator, single template, single registry.
- Adopted ECL harness discipline.
- Added GitHub Actions CI (ruff, mypy, pytest).
