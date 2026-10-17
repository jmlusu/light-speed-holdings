# Plan

## Technical Approach

1. Add `opentelemetry-api` as a core dependency in `pyproject.toml`.
2. Create `src/ai_company/telemetry/` package with:
   - `tracer.py`: `TracerProvider` wrapper, `start_span()` / `start_as_current_span()` convenience, context propagation helpers
   - `bridge.py`: Correlation ID ↔ OTel context bridge (set/get trace_id/span_id from ContextVar, propagate to child tasks)
   - `exporter.py`: `ConsoleSpanExporter` for dev visibility, `InMemorySpanExporter` for testing
3. Initialize tracing in `logging_config.setup_logging()` (opt-in via `AI_COMPANY_OTEL=1` env var).
4. Instrument critical path:
   - `ExecutorLoop._process_task()`: root span per task
   - `AgentLoop.run()`: span per agentic loop
   - `LLMClient.execute_task()`: span per LLM call attempt
   - `ToolRunner.run_plan()`: span per tool execution
5. Bridge correlation ID: `set_correlation_id()` also sets OTel span context; `get_correlation_id()` reads from OTel context when available.
6. Write ADR-016 documenting the decision.
7. Add tests for span creation, context propagation, and console output.

## Impacted Modules And Files

| File | Change |
|------|--------|
| `pyproject.toml` | Add `opentelemetry-api` to dependencies |
| `src/ai_company/telemetry/__init__.py` | Package init, convenience re-exports |
| `src/ai_company/telemetry/tracer.py` | TracerProvider wrapper, span utilities |
| `src/ai_company/telemetry/bridge.py` | Correlation ID ↔ OTel context bridge |
| `src/ai_company/telemetry/exporter.py` | ConsoleSpanExporter, InMemorySpanExporter |
| `src/ai_company/logging_config.py` | Wire tracing init into setup_logging() |
| `src/ai_company/executor/loop.py` | Add root span in _process_task() |
| `src/ai_company/executor/agent_loop.py` | Add span in run(), propagate context to subtasks |
| `src/ai_company/llm/client.py` | Add span in execute_task() |
| `src/ai_company/executor/tool_runner.py` | Add span in run_plan() |
| `docs/adr/016-opentelemetry-tracing.md` | ADR documenting the decision |
| `tests/unit/test_telemetry.py` | Tests for tracer, bridge, exporter |

## Interfaces, Data, Permissions

- **New interface**: `ai_company.telemetry` module — `init_tracing()`, `start_span()`, `get_current_span()`, `set_correlation_id_from_span()`
- **Modified interface**: `logging_config.setup_logging()` gains optional `otel_enabled` parameter
- **No new permissions or security concerns** — OTel API is local-only, no network calls
- **No data model changes** — spans are in-memory, not persisted

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| `opentelemetry-api` adds import overhead | Lazy initialization; tracing only activates when `AI_COMPANY_OTEL=1` |
| Span noise in console output | Default to WARNING+ level for console exporter; configurable |
| Breaking existing correlation ID tests | Bridge preserves existing ContextVar behavior; tests updated to verify both paths |
| Performance overhead from span creation | OTel API is designed for zero-cost when no provider is registered; in-memory exporter is fast |

## Verification Plan

1. `uv run ruff check src/` — lint clean
2. `uv run mypy src/` — type clean
3. `uv run pytest tests/unit/test_telemetry.py -v` — new telemetry tests pass
4. `uv run pytest` — full suite passes (no regressions)
5. Manual: `AI_COMPANY_OTEL=1 python -c "from ai_company.telemetry import init_tracing; init_tracing(); ..."` — verify console span output
6. `.\scripts\lint-ecl.ps1` — ECL structure valid
