# ADR-016: OpenTelemetry Tracing for the Task Execution Pipeline

**Status:** Accepted
**Date:** 2026-08-17
**Deciders:** CTO, Observability Engineer
**Technical Domain:** Observability & Tracing

## Context

Requirement T7 (from the original system spec) demands OTel spans with 100%
trace coverage and parent→child correlation across the task execution pipeline.
Today the runtime uses correlation IDs (a `ContextVar` set per-task in
`ExecutorLoop._process_task()`) and structured JSON logging that includes the
correlation ID on every log record. This provides single-request tracing within
one process but has two gaps:

1. **No OTel spans.** There is no trace tree — only flat correlation IDs in log
   lines. Observability tooling (Jaeger, Grafana Tempo, OTel Collector) cannot
   ingest or visualize the execution flow.
2. **Subtask linkage gap.** When a tool-initiated action creates a subtask, it
   spawns a new correlation ID rather than inheriting the parent's. The trace
   breaks at that boundary.

Issue #40 asks whether to add OTel spans + an exporter or stick with
correlation-ID JSON logs. The blocking issues (#34 event-bus evolution, #36
storage/memory engine) are both closed.

## Decision

Adopt the **OpenTelemetry API** (not the full SDK) as the tracing interface for
the task execution pipeline. Concretely:

### 1. Dependency posture

- `opentelemetry-api` is a **core dependency** (always installed). It provides
  the `Span`, `Tracer`, `Context` interfaces with zero runtime cost when no
  provider is registered.
- `opentelemetry-sdk` is **not** a core dependency. It is added only when an
  operator opts into OTLP export (via an optional extra or a staging/Docker
  dependency).
- A lightweight **in-memory exporter** (`InMemorySpanExporter`) ships in-tree
  for dev visibility and test assertions.

### 2. Opt-in activation

Tracing activates only when the environment variable `AI_COMPANY_OTEL=1` is
set. When unset, the `NoOpTracer` from `opentelemetry-api` is used — zero
span creation cost, zero memory overhead. This preserves the single-machine,
no-external-services posture of ADR-010.

### 3. Correlation ID bridge

The existing `correlation_id` ContextVar is **bridged** to OTel trace context:

- `set_correlation_id(task_id)` also sets the OTel span context so that the
  task ID becomes the `trace_id` (truncated/hashed to 128-bit).
- `get_correlation_id()` reads from OTel context when a span is active,
  otherwise falls back to the ContextVar.
- Subtask creation **inherits** the parent span context via
  `context.attach(parent_context)`, fixing the linkage gap.

### 4. Instrumentation points (100% critical-path coverage)

| Location | Span name | Key attributes |
|----------|-----------|----------------|
| `ExecutorLoop._process_task()` | `task.process` | `task.id`, `task.agent_id`, `task.priority` |
| `AgentLoop.run()` | `agent.loop` | `agent.name`, `iteration`, `task_id` |
| `LLMClient.execute_task()` | `llm.execute` | `provider`, `model`, `attempt`, `task_id` |
| `ToolRunner.run_plan()` | `tool.execute` | `tool.name`, `task_id`, `tier` |

### 5. Console exporter

A `ConsoleSpanExporter` prints each completed span to stderr in a
human-readable format (operation name, duration, attributes). This is the
default when `AI_COMPANY_OTEL=1` and no OTLP endpoint is configured.

### 6. OTLP exporter (future, optional)

When `opentelemetry-exporter-otlp` is installed and
`AI_COMPANY_OTEL_ENDPOINT` is set, the tracer switches to OTLP gRPC export.
This is not a core dependency — it is added via `pip install
ai-company[otel]` or in Docker/staging images.

## Consequences

- **Positive:** Full trace tree for every task execution; parent→child linkage
  fixed; OTel-compatible output for ingestion by Jaeger/Tempo/OTel Collector;
  zero cost when disabled; existing correlation ID consumers unchanged.
- **Negative / risk:** One additional core dependency (`opentelemetry-api`,
  ~200 KB). Mitigated by lazy initialization and zero-cost NoOp when disabled.
- **Neutral:** Existing structured JSON logs and audit trail continue unchanged.
  The OTel spans are an additional signal, not a replacement.

## Links

- Ticket: #40 Decide the OpenTelemetry tracing design
- Requirement: T7 (100% trace coverage, parent→child correlation)
- ADR-010: T1 Event-Bus Alignment (single-machine posture)
- ADR-002: JSON MessageBus
- Related: `logging_config.py` (correlation ID ContextVar), `audit/integration.py`
