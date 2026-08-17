---
title: "Phase B: OpenTelemetry Tracing (#40)"
slug: "phase-b-opentelemetry-tracing-40"
status: "completed"
location: "archive"
phase: "plan"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules:
  - "ai_company.telemetry"
  - "ai_company.executor.loop"
  - "ai_company.executor.agent_loop"
  - "ai_company.llm.client"
  - "ai_company.executor.tool_runner"
  - "ai_company.logging_config"
files:
  - "src/ai_company/telemetry/__init__.py"
  - "src/ai_company/telemetry/tracer.py"
  - "src/ai_company/telemetry/bridge.py"
  - "src/ai_company/telemetry/exporter.py"
  - "pyproject.toml"
  - "docs/adr/016-opentelemetry-tracing.md"
tags:
  - "observability"
  - "tracing"
  - "opentelemetry"
  - "phase-b"
validation_status: "unknown"
created_at: "2026-08-17"
updated_at: "2026-08-17"
---

# Summary

## Outcome

Adopt OpenTelemetry API for distributed tracing across the task execution pipeline. Bridge existing correlation IDs to OTel trace context. Fix parent→child linkage gap where subtask creation spawns unlinked correlation IDs. Console exporter for dev; OTLP opt-in for production.

## Decisions

- ADR-016: OTel API (not full SDK) as the tracing interface; lightweight in-memory exporter as default
- Correlation ID ContextVar maps to OTel span trace_id/span_id
- 100% span coverage on critical path: executor→agent loop→LLM call→tool execution
- No OTLP exporter in core deps; optional `opentelemetry-exporter-otlp` extra

## Validation

- Pending (see tasks.md)

## Next Step

- Execute tasks T001–T008, then validate gates (ruff, mypy, pytest).



