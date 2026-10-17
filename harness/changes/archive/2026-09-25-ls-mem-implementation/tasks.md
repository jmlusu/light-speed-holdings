# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Confirm handoff §34 sequence, Phase 3 data model, and reviewer consensus blockers.

## Implementation

- [x] T002 Implement `src/ai_company/lsmem/` modules (engine, classification, redaction, gateway, audit, injector, scoring, bridge, vector, cli).
- [x] T003 Wire injector into `src/ai_company/executor/loop.py` with fallback paths.
- [x] T004 Ensure dual skill paths `.agents/skills/ls-memory/` and `.opencode/skills/ls-memory/` are hash-identical.
- [x] T005 Build `tests/memory/` suite (engine CRUD, redaction, git safety, dual-path, integration: gateway/audit/bridge/injector/CLI, offline, ollama-optional).

## Validation

- [x] T006 Remediate consensus blockers: mypy 38→0, verify executor wiring/vector/threat-model claims, fix bridge FTS bugs, convert 37 typer Option calls.
- [x] T007 Run gates: `uv run ruff check src/ai_company/lsmem/`, `uv run mypy src/ai_company/lsmem/`, `uv run python -X utf8 -m pytest tests/memory/ -q`, `pwsh scripts/lint-ecl.ps1`.

## Deferred Tasks

- None.
