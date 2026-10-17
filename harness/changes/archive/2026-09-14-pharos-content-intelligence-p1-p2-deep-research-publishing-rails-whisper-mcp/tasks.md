# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Approach the user with the 4 scope questions (MCP transport / Whisper packaging / publishing rails / deep-research scope); record resolved answers in `spec.md` Resolved Clarifications.

## Implementation

- [x] T002 Add `research_depth` field (`standard`|`deep`, default `standard`) to `Routine` in `src/ai_company/orchestrator/routine.py`; keep existing YAML parsing backward-compatible (extra fields may appear, `extra="ignore"`). Validation: `Routine(research_depth="deep")` round-trips; default stays `standard`. — DONE: field + `is_deep_research` + `{research_depth}` token + `research:deep` tag; 3 new tests in `test_routine.py`.
- [x] T003 Add 2 deep-research routines (`pharos_deep_research_brief` Sat `schedule_day: 6`, `pharos_sadc_research_scan` Thu `schedule_day: 4`) with `research_depth: deep` to `config/company/routines.yaml` (Sat chosen to avoid double-fire with the existing Monday brief). Validation: `RoutineStore().list_routines()` returns them; `pytest tests/unit/test_routine.py`. — DONE.
- [x] T004 Add 2 deep-research prompt templates under `templates/pharos/routines/` (deep-research brief + SADC research scan) referencing knowledge graph / memory / docs-Pharos corpus. Validation: templates read via `RoutineStore.read_prompt`. — DONE: `templates/pharos/routines/deep-research-brief.md`, `sadc-research-scan.md`.
- [x] T005 Implement `src/ai_company/publishing/` package: `queue.py` (FileStore-backed `PublishQueue` at `results/pharos/publish_queue.json`, enqueue/list/mark_posted/mark_failed with optional bus mirror), `formats.py` (`format_linkedin`, `format_substack`), `publishers.py` (`LinkedInPublisher`, `SubstackPublisher` with env-gated live HTTP + dry-run receipt). Validation: `tests/unit/test_publishing.py`. — DONE (11 tests green).
- [x] T006 Register `publishing` lazy subapp in `src/ai_company/cli/main.py` (`_LAZY_SUB_APPS`) + `src/ai_company/cli/publishing.py` with `enqueue`/`list`/`show`/`publish` commands (opt-in `--live` POST, dry-run default). Validation: `ai-company publishing --help` passes. — DONE.
- [x] T007 Implement `src/ai_company/media/transcription.py` (`Transcriber` with lazy faster-whisper import, `is_available()`, graceful `unavailable` result) + `src/ai_company/cli/media.py` `transcribe` command. Validation: `tests/unit/test_transcription.py`. — DONE (5 tests green).
- [x] T008 Add `pharos-whisper = ["faster-whisper>=1.0"]` to `[project.optional-dependencies]` in `pyproject.toml` and refresh `uv.lock` (ECL lockfile atomicity). Validation: `uv lock` records the extra. — DONE: `uv lock` resolved faster-whisper v1.2.1 under the extra; `provides-extras` includes `pharos-whisper`.
- [x] T009 Implement `src/ai_company/mcp/__init__.py` + `server.py`: stdlib stdio JSON-RPC 2.0 server (initialize / tools/list / tools/call / ping), X-API-Key→RBAC gating (read `run`, `publish_queue` `approve`), content-filter + PII pass, AuditWriter logging every call. Validation: `tests/unit/test_mcp_server.py`. — DONE (20 tests green incl. auth, traversal-block, PII mask, audit).
- [x] T010 Implement MCP CLI entrypoint (`src/ai_company/cli/mcp.py`, lazy subapp `mcp`) for `ai-company mcp stdio` (+ `mcp tools`). Validation: `ai-company mcp --help`. — DONE.

## Validation

- [x] T011 Run focused tests: `uv run pytest tests/unit/test_publishing.py tests/unit/test_transcription.py tests/unit/test_mcp_server.py tests/unit/test_routine.py -q --basetemp=".pytest_tmp_p1"` — all pass (58/58).
- [x] T012 Run full gates: `uv run ruff check src/`; `uv run mypy src/`; `uv run pytest -q -m "not e2e" --basetemp=".pytest_tmp_p1"` — all green (ruff clean; mypy clean 209 files; 2162 passed / 67 deselected).
- [ ] T013 Update `summary.md` (outcome/decisions/validation), `docs/STATUS.md`, run `pwsh scripts/lint-ecl.ps1` and `.\scripts\harness-change.ps1 validate`, then close `completed`.

## Deferred Tasks

- None.
