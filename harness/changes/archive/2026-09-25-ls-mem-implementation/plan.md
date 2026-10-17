# Plan

## Technical Approach

1. Implement modules in dependency order: classification → redaction →
   engine (schema/CRUD/FTS5) → audit → gateway → scoring → injector →
   bridge → vector → CLI.
2. Wire injector into `src/ai_company/executor/loop.py` with graceful
   fallback when memory is unavailable.
3. Build tests bottom-up: unit (engine CRUD, redaction, git safety, dual-path
   hash) → integration (gateway, audit, bridge, injector, CLI e2e) →
   offline/optional-provider suites.
4. Remediate reviewer consensus: verify each claim on disk, fix what is real
   (mypy, tests, bridges bugs), refute what is stale with evidence.
5. Close process gap with retrospective ECL archives (Phase 3 + this).

## Impacted Modules And Files

- New: `src/ai_company/lsmem/` (11 files), `tests/memory/` (7 test files + hash report).
- Modified: `src/ai_company/executor/loop.py` (injector wiring).
- Skills: `.agents/skills/ls-memory/SKILL.md`, `.opencode/skills/ls-memory/SKILL.md` (hash-identical pair).

## Interfaces, Data, Permissions

- Gateway API: `evaluate(...)` → `GatewayDecision`; `submit_human_approval`;
  `get_pending_approvals()` (list of dicts keyed by `approval_token`).
- Audit API: `log(...)`, `verify_chain()`, `export("jsonl")`.
- Storage: `.lightspeed/memory/` (gitignored); schema per Phase 3 data model.

## Spec Gaps Found From Planning

- Typer version drift in CLI option declarations (fixed during validation).
- FTS5 tokenizer options unsupported by SQLite 3.45.1 (fixed: `unicode61
  remove_diacritics 1` only; dropped `tokenchars`).

## Risks And Mitifications

- Risk: soft-delete semantics leak forgotten memory into retrieval.
  Mitigation: search filters non-ACTIVE; CLI e2e asserts post-forget search
  exclusion.
- Risk: audit tamper on last event. Mitigation: recorded as known follow-up
  (persisted chain head not yet implemented).

## Verification Plan

- `uv run ruff check src/ai_company/lsmem/`
- `uv run mypy src/ai_company/lsmem/`
- `uv run python -X utf8 -m pytest tests/memory/ -q`
- `pwsh scripts/lint-ecl.ps1`
