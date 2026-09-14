# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] Create ADR-016 documenting the OpenTelemetry tracing decision → `docs/adr/016-opentelemetry-tracing.md`
- [x] T003 [P] Add `opentelemetry-api` dependency to `pyproject.toml`
- [x] T004 Create telemetry package: `src/ai_company/telemetry/__init__.py`, `tracer.py`, `bridge.py`, `exporter.py`
- [x] T005 Wire tracing init into `logging_config.setup_logging()` with opt-in env var `AI_COMPANY_OTEL`
- [x] T006 Instrument critical path: executor loop (root span), agent loop (iteration spans), LLM client (call spans), tool runner (tool spans)
- [x] T007 Fix parent→child linkage: propagate OTel context in subtask creation via bridge.py
- [x] T008 Write tests in `tests/unit/test_telemetry.py` covering span creation, context propagation, console output

## Validation

- [x] T009 Run `uv run ruff check src/` — lint clean
- [x] T010 Run `uv run mypy src/` — type clean
- [x] T011 Run `uv run pytest tests/unit/test_telemetry.py -v` — new tests pass
- [x] T012 Run `uv run pytest` — full suite passes (no regressions)
- [x] T013 Run `.\scripts\lint-ecl.ps1` — ECL structure valid

## Deferred Tasks

- None.
