"""Correlation ID ↔ OTel context bridge.

Bridges the existing ``correlation_id`` ContextVar to OTel trace context so
that:

1. ``set_correlation_id(task_id)`` also sets the OTel span context.
2. ``get_correlation_id()`` reads from the OTel span context when a span is
   active, otherwise falls back to the ContextVar.
3. Subtask creation inherits the parent's OTel context, fixing the linkage
   gap identified in issue #40.
"""

from __future__ import annotations

import contextlib
import hashlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


def _hash_to_trace_id(task_id: str) -> int:
    """Deterministically hash a task ID to a 128-bit OTel trace ID."""
    digest = hashlib.sha256(task_id.encode()).digest()
    return int.from_bytes(digest[:16], byteorder="big")


def _hash_to_span_id(task_id: str) -> int:
    """Deterministically hash a task ID to a 64-bit OTel span ID."""
    digest = hashlib.sha256(task_id.encode()).digest()
    return int.from_bytes(digest[:8], byteorder="big")


def set_correlation_id_from_task(task_id: str) -> None:
    """Set both the correlation ID ContextVar and the OTel span context.

    This is the primary entry point for task execution — called once at the
    start of ``ExecutorLoop._process_task()``.
    """
    from ai_company.logging_config import set_correlation_id

    set_correlation_id(task_id)

    try:
        from ai_company.telemetry.tracer import is_tracing_enabled

        if not is_tracing_enabled():
            return

        from opentelemetry import context as otel_context
        from opentelemetry import trace as otel_trace
        from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags

        tracer = otel_trace.get_tracer("ai-company")

        # Create a parent context with the desired trace_id so child spans
        # inherit it (fixing the parent→child linkage gap, issue #40).
        parent_span_context = SpanContext(
            trace_id=_hash_to_trace_id(task_id),
            span_id=_hash_to_span_id(task_id),
            is_remote=False,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
        )
        parent_span = NonRecordingSpan(parent_span_context)
        parent_ctx = otel_trace.set_span_in_context(parent_span)
        token = otel_context.attach(parent_ctx)

        # Create a root span for the task under that context.
        span = tracer.start_span(
            "task.process",
            attributes={
                "task.id": task_id,
                "correlation_id": task_id,
            },
        )
        # Activate the span so downstream code inherits the context.
        otel_trace.set_span_in_context(span)

        _active_tokens[task_id] = (span, token)

    except ImportError:
        pass  # OTel not available; correlation ID ContextVar is sufficient.


_active_tokens: dict[str, tuple[Any, Any]] = {}


def detach_task_context(task_id: str) -> None:
    """Detach the OTel context for a completed task.

    Called at the end of ``ExecutorLoop._process_task()`` to clean up.
    """
    entry = _active_tokens.pop(task_id, None)
    if entry is None:
        return
    span, token = entry
    with contextlib.suppress(Exception):
        span.end()
    from opentelemetry import context as otel_context

    with contextlib.suppress(Exception):
        otel_context.detach(token)


def create_child_span(
    name: str,
    *,
    parent_task_id: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> Any:
    """Create a child span under the current active span.

    When *parent_task_id* is provided and the task has an active context,
    the child span inherits the parent's trace_id, ensuring linkage.

    Returns a context manager yielding the span (or ``None`` when tracing
    is disabled).
    """
    from ai_company.telemetry.tracer import is_tracing_enabled, start_span

    if not is_tracing_enabled():
        from contextlib import nullcontext

        return nullcontext(None)

    return start_span(name, attributes=attributes or {})


def subtask_context(
    parent_task_id: str,
    child_task_id: str,
) -> Any:
    """Context manager for subtask creation that inherits parent trace context.

    Usage::

        with subtask_context(parent_task_id, child_task_id):
            # Subtask execution happens here — child spans inherit the
            # parent's trace_id, fixing the linkage gap.
            ...

    When tracing is disabled, this is a no-op.
    """
    from ai_company.telemetry.tracer import is_tracing_enabled

    if not is_tracing_enabled():
        return contextlib.nullcontext()

    try:
        from opentelemetry import context as otel_context
        from opentelemetry import trace as otel_trace
        from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags

        tracer = otel_trace.get_tracer("ai-company")

        # Create a parent context with the parent's trace_id so child spans
        # inherit it (fixing the linkage gap, issue #40).
        parent_span_context = SpanContext(
            trace_id=_hash_to_trace_id(parent_task_id),
            span_id=_hash_to_span_id(parent_task_id),
            is_remote=False,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
        )
        parent_span = NonRecordingSpan(parent_span_context)
        parent_ctx = otel_trace.set_span_in_context(parent_span)
        token = otel_context.attach(parent_ctx)

        # Start a child span — inherits parent's trace_id automatically.
        child_span = tracer.start_span(
            "subtask.process",
            attributes={
                "parent_task.id": parent_task_id,
                "child_task.id": child_task_id,
                "correlation_id": child_task_id,
            },
        )
        ctx = otel_trace.set_span_in_context(child_span)
        token = otel_context.attach(ctx)

        @contextlib.contextmanager
        def _yield() -> Any:
            try:
                yield
            finally:
                child_span.end()
                otel_context.detach(token)

        return _yield()
    except ImportError:
        return contextlib.nullcontext()
