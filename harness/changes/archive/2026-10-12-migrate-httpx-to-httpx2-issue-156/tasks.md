# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Close previous active ECL change (merge-conflict resolution) via `harness-change.ps1 close completed` after full non-e2e suite (2584 passed) — archived as `2026-10-12-resolve-merge-conflicts-main-branch-build`.
- [x] T002 Create this change via `harness-change.ps1 new`; record spec/plan/task docs.

## Implementation

- [x] T003 Dependencies: `uv add "httpx2>=2.12"`; remove `"httpx<0.29.0"` from `pyproject.toml:24`; `uv lock` + `uv sync --extra dev`; confirm httpx remains in lock only via huggingface-hub/safety. Validation: `uv tree` / uv.lock grep.
- [x] T004 `.pre-commit-config.yaml` mypy hook `additional_dependencies`: `httpx` -> `httpx2`. Validation: `pre-commit run mypy --all-files` resolves `import httpx2`.
- [x] T005 src alias swap `import httpx` -> `import httpx2 as httpx` in 10 files (providers x3, oauth2, client, model_router, agent_loop, publishers, cli/main, doctor/checks). Validation: `rg '^\s*import httpx\b' src/` -> zero.
- [x] T006 `doctor/checks.py:128` required-package list `"httpx"` -> `"httpx2"`. Validation: doctor unit tests green.
- [x] T007 tests alias swap + literal patch retarget: `tests/unit/conftest.py:66` alias + `:71` -> `"httpx2.get"`; `test_doctor.py:41,51,295`; `test_omniroute_integration.py:29,726,767,779,794`; `test_llm.py`; `test_oauth2.py:14`; `test_llm_streaming.py:9`. Leave `conftest.py:103-104` module-path targets unchanged. Validation: `rg '"httpx\.' tests/` -> zero literal `"httpx.` patch strings.
- [x] T008 Docs: `docs/ARCHITECTURE.md:242`, `.ai-company/constitution/02-ARCHITECTURE.md:549` dependency tables; `docs/DEPLOYMENT-GUIDE.md:148,207` healthcheck examples -> httpx2 (Dockerfile itself uses curl, unchanged). Historical docs untouched.

## Validation

- [x] T009 Gates: `uv run ruff check src/ tests/` + `uv run mypy src/` + `uv run pytest -m "not e2e"` all pass.
- [x] T010 Confirm `StarletteDeprecationWarning` absent from full-suite output (baseline run had exactly 1 occurrence).
- [x] T011 `uv audit --frozen` (or repo's audit command equivalent) passes; httpx in lock documented as transitive-only.
- [x] T012 `pwsh scripts/maintenance/lint-ecl.ps1` passes; record validation_results in summary.md; close change.

## Deferred Tasks

- None.
