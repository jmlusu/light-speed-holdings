# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Open ECL change and record resolved clarifications in `harness/changes/active/spec.md`.

## Implementation

- [x] T002 [P] WS-A: repoint `_LAZY_SUB_APPS` in `src/ai_company/cli/main.py` (memory -> lsmem, add knowledge -> legacy) and update `tests/unit/test_cli_commands.py`; validate: `ai-company memory --help`, `ai-company knowledge --help`, `pytest tests/unit/test_cli_commands.py`. **Done 2026-09-26; full suite 2563 passed.**
- [x] T003 [P] WS-B: persist audit chain head in `src/ai_company/lsmem/audit.py` + tamper-tail tests in `tests/memory/`; validate: pytest new audit tests. **Done 2026-09-26; `tests/memory/test_audit_chain_head.py` green.**
- [x] T004 [P] WS-A docs: legacy examples -> `knowledge` in `README.md`, `docs/USER-GUIDE.md`, `docs/ux/CLI-DESIGN.md`, `docs/DECISION-FRAMEWORK.md`, `config/company/scheduler.yaml`. **Done 2026-09-26; follow-up fixed invalid `--type`/`--query` flags in DECISION-FRAMEWORK/USER-GUIDE/CLI-DESIGN.**
- [x] T005 [P] WS-C: write `docs/LS-MEM-USER-GUIDE.md` (§27 backup/restore/export/migrate/rebuild/corruption/uninstall); validate: lint-ecl + links resolve. **Done 2026-09-26.**
- [x] T006 [P] WS-C: write `docs/security/LS-MEM-SECURITY-VERIFICATION.md` (§33 20 answers + test evidence + deviation note). **Done 2026-09-26; §6 audit pending WS-E.**

## Validation

- [x] T007 WS-E: independent `ciso` security audit; fix or document findings; record sign-off in report. **Done 2026-09-26; APPROVE-WITH-FINDINGS, 11 findings documented/deferred, 10 citation fixes, zero source changes; recorded in `docs/security/LS-MEM-SECURITY-VERIFICATION.md` §6; §7 holds 4 CEO/HITL items.**
- [x] T008 WS-F: gates `uv run ruff check src/` && `uv run mypy src/` && `uv run pytest`; CLI lifecycle + skill-script smoke. **Done 2026-09-26 (gate of record): ruff clean; format clean on touched files; mypy success (230 files); pytest 2566 passed / 2 skipped / 67 deselected; `memory status|knowledge stats|memory --help` exit 0; skill scripts memory-status/memory-search exit 0.**
- [x] T009 Close ECL: update `docs/STATUS.md`, reindex/archive, `pwsh scripts/lint-ecl.ps1`, single commit of LS-MEM files. **STATUS.md updated 2026-09-26; reindex + validate + lint-ecl green while active; close + archive lint green; single LS-MEM commit lands immediately after archive (no push).**

## Deferred Tasks

- None.
