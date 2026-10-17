# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (T7 from spec, issue #40)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Requirement T7 demands OTel spans with 100% trace coverage and parent→child correlation. Today: correlation IDs + structured JSON logging, no OTel spans, subtask creation spawns a new correlation ID (linkage gap). Issue #40.
- Current behavior: `correlation_id` is a ContextVar set per-task in `ExecutorLoop._process_task()`. Subtasks (tool-initiated task dispatch) spawn a new correlation ID, breaking parent→child trace linkage. No OTel integration exists.
- Source of evidence: `logging_config.py` (correlation ID ContextVar), `executor/loop.py:528` (set_correlation_id), `audit/integration.py` (audit events carry correlation_id), issue #40 body.

## User Scenarios And Success

- Primary user/system scenario: An operator observing task execution sees a complete trace tree: task → agent loop iterations → LLM calls → tool executions, all linked by parent→child span relationships.
- Success criteria:
  - Every task produces a root OTel span with `trace_id` matching the task's correlation ID
  - LLM calls, tool executions, and agent loop iterations produce child spans
  - Subtask creation propagates parent trace context (no orphaned correlation IDs)
  - Console exporter prints trace tree in dev mode
  - All existing tests pass; new telemetry tests cover span creation and context propagation
- Acceptance criteria:
  - `opentelemetry-api` is a core dependency
  - `src/ai_company/telemetry/` package exists with tracer, bridge, exporter
  - Critical path instrumented: executor loop, agent loop, LLM client, tool runner
  - `ruff check src/ && mypy src/ && pytest` all pass

## Non-Goals

- OTLP exporter (optional extra, not core)
- Full OTel SDK with metric readers, log correlation, or Prometheus exporter
- Dashboard trace visualization (future work)
- Sampling configuration (100% by default; no sampling config needed yet)

## Constraints

- Single-machine, no external services (ADR-010)
- Must not break existing correlation ID behavior in logs/audit trail
- Minimal dependency footprint: `opentelemetry-api` only (no SDK in core)
- Python 3.12+

## Assumptions

- `opentelemetry-api` is stable and compatible with Python 3.12
- In-memory exporter is sufficient for dev; OTLP can be added as optional extra later
- Existing `correlation_id` consumers continue working unchanged

## Open Questions

- None (resolved via ADR-016 design).

## Resolved Clarifications

- Q: OTel spans vs correlation-ID JSON logs? A: OTel spans with correlation ID bridge. Logs remain; spans add trace tree.
- Q: Full SDK or API-only? A: API-only with lightweight in-memory exporter. SDK added only when OTLP is needed.
- Q: How to fix parent→child linkage? A: Propagate OTel context via `contextvars`; subtask creation inherits parent span context.
