"""OpenTelemetry tracing for the task execution pipeline.

Provides a thin wrapper around the OTel API/SDK that activates only when
``AI_COMPANY_OTEL=1`` is set.  When disabled, NoOp tracers are used — zero
span-creation cost.

Quick start::

    from ai_company.telemetry import init_tracing, start_span

    init_tracing()  # call once at startup
    with start_span("my.operation", attributes={"key": "value"}):
        ...
"""

from ai_company.telemetry.bridge import (
    create_child_span,
    detach_task_context,
    set_correlation_id_from_task,
    subtask_context,
)
from ai_company.telemetry.exporter import ConsoleSpanExporter, InMemorySpanExporter
from ai_company.telemetry.tracer import (
    get_current_span_context,
    get_tracer,
    init_tracing,
    is_tracing_enabled,
    start_span,
)

__all__ = [
    "ConsoleSpanExporter",
    "InMemorySpanExporter",
    "create_child_span",
    "detach_task_context",
    "get_current_span_context",
    "get_tracer",
    "init_tracing",
    "is_tracing_enabled",
    "set_correlation_id_from_task",
    "start_span",
    "subtask_context",
]
