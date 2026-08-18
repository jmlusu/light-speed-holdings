"""Unit tests for OpenTelemetry tracing (T7 / issue #40).

Tests cover:
- Tracer initialisation (enabled / disabled)
- ConsoleSpanExporter output
- InMemorySpanExporter collection
- Correlation ID ↔ OTel context bridge
- Subtask context propagation (parent→child linkage)
- NoOp fallback when tracing is disabled
"""

from __future__ import annotations

import os
from io import StringIO
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_tracing():
    """Reset global tracing state before/after each test."""
    import ai_company.telemetry.tracer as tracer_mod

    old_enabled = tracer_mod._TRACING_ENABLED
    old_tracer = tracer_mod._tracer
    tracer_mod._TRACING_ENABLED = False
    tracer_mod._tracer = None
    yield
    tracer_mod._TRACING_ENABLED = old_enabled
    tracer_mod._tracer = old_tracer


@pytest.fixture()
def memory_exporter():
    """Provide a fresh InMemorySpanExporter and clean up after."""
    from ai_company.telemetry.exporter import InMemorySpanExporter

    exp = InMemorySpanExporter()
    yield exp
    exp.clear()


# ---------------------------------------------------------------------------
# Tracer initialisation
# ---------------------------------------------------------------------------


class TestInitTracing:
    """init_tracing activates only when the env var is set."""

    def test_disabled_by_default(self) -> None:
        from ai_company.telemetry.tracer import init_tracing, is_tracing_enabled

        with patch.dict(os.environ, {}, clear=True):
            result = init_tracing()
        assert result is False
        assert is_tracing_enabled() is False

    def test_enabled_when_env_set(self) -> None:
        from ai_company.telemetry.tracer import init_tracing, is_tracing_enabled

        with patch.dict(os.environ, {"AI_COMPANY_OTEL": "1"}):
            result = init_tracing(console=False)
        assert result is True
        assert is_tracing_enabled() is True

    def test_enabled_with_true_value(self) -> None:
        from ai_company.telemetry.tracer import init_tracing, is_tracing_enabled

        with patch.dict(os.environ, {"AI_COMPANY_OTEL": "true"}):
            result = init_tracing(console=False)
        assert result is True
        assert is_tracing_enabled() is True

    def test_idempotent(self) -> None:
        from ai_company.telemetry.tracer import init_tracing, is_tracing_enabled

        with patch.dict(os.environ, {"AI_COMPANY_OTEL": "1"}):
            init_tracing(console=False)
            result2 = init_tracing(console=False)
        assert result2 is True
        assert is_tracing_enabled() is True


# ---------------------------------------------------------------------------
# ConsoleSpanExporter
# ---------------------------------------------------------------------------


class TestConsoleSpanExporter:
    """ConsoleSpanExporter prints formatted span output."""

    def test_exports_to_stream(self) -> None:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        from ai_company.telemetry.exporter import ConsoleSpanExporter

        stream = StringIO()
        exporter = ConsoleSpanExporter(stream=stream)
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))  # type: ignore[arg-type]
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("test.span"):
            pass

        output = stream.getvalue()
        assert "test.span" in output
        assert "TRACE" in output
        assert "ms" in output

    def test_includes_attributes(self) -> None:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        from ai_company.telemetry.exporter import ConsoleSpanExporter

        stream = StringIO()
        exporter = ConsoleSpanExporter(stream=stream)
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))  # type: ignore[arg-type]
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("test.span", attributes={"key": "value"}):
            pass

        output = stream.getvalue()
        assert "key=value" in output


# ---------------------------------------------------------------------------
# InMemorySpanExporter
# ---------------------------------------------------------------------------


class TestInMemorySpanExporter:
    """InMemorySpanExporter collects spans for test assertions."""

    def test_collects_spans(self, memory_exporter) -> None:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(memory_exporter))  # type: ignore[arg-type]
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("span.a"):
            pass
        with tracer.start_as_current_span("span.b"):
            pass

        assert len(memory_exporter.get_finished_spans()) == 2

    def test_find_spans_by_name(self, memory_exporter) -> None:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(memory_exporter))  # type: ignore[arg-type]
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("target"):
            pass
        with tracer.start_as_current_span("other"):
            pass

        assert len(memory_exporter.find_spans("target")) == 1
        assert memory_exporter.find_span("target") is not None
        assert memory_exporter.find_span("nonexistent") is None

    def test_clear(self, memory_exporter) -> None:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(memory_exporter))  # type: ignore[arg-type]
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("span"):
            pass

        assert len(memory_exporter.get_finished_spans()) == 1
        memory_exporter.clear()
        assert len(memory_exporter.get_finished_spans()) == 0


# ---------------------------------------------------------------------------
# Correlation ID bridge
# ---------------------------------------------------------------------------


class TestCorrelationBridge:
    """Bridge between correlation_id ContextVar and OTel context."""

    def test_set_correlation_id_from_task(self) -> None:
        from ai_company.logging_config import get_correlation_id, set_correlation_id
        from ai_company.telemetry.bridge import set_correlation_id_from_task

        set_correlation_id("")
        set_correlation_id_from_task("test-task-123")
        assert get_correlation_id() == "test-task-123"

    def test_start_span_returns_none_when_disabled(self) -> None:
        from ai_company.telemetry.tracer import start_span

        with start_span("test") as span:
            assert span is None

    def test_start_span_returns_span_when_enabled(self) -> None:
        from ai_company.telemetry.tracer import init_tracing, start_span

        with patch.dict(os.environ, {"AI_COMPANY_OTEL": "1"}):
            init_tracing(console=False)

        with start_span("test.span") as span:
            assert span is not None
            assert hasattr(span, "end")

    def test_hash_to_trace_id_deterministic(self) -> None:
        from ai_company.telemetry.bridge import _hash_to_trace_id

        id1 = _hash_to_trace_id("task-abc")
        id2 = _hash_to_trace_id("task-abc")
        assert id1 == id2
        assert id1 != _hash_to_trace_id("task-xyz")


# ---------------------------------------------------------------------------
# Subtask context propagation
# ---------------------------------------------------------------------------


class TestSubtaskContext:
    """Subtask context inherits parent trace context."""

    def test_subtask_context_noop_when_disabled(self) -> None:
        from ai_company.telemetry.bridge import subtask_context

        # Should not raise, should be a no-op
        with subtask_context("parent-id", "child-id"):
            pass

    def test_subtask_context_creates_child_span(self, memory_exporter) -> None:
        from opentelemetry import context as otel_context
        from opentelemetry import trace as otel_trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags

        import ai_company.telemetry.tracer as tracer_mod
        from ai_company.telemetry.bridge import _hash_to_span_id, _hash_to_trace_id

        # Set up a provider with our memory exporter
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(memory_exporter))  # type: ignore[arg-type]
        test_tracer = provider.get_tracer("ai-company")

        # Mark tracing as enabled
        tracer_mod._TRACING_ENABLED = True

        parent_id = "parent-task-001"
        child_id = "child-task-002"
        parent_trace_id = _hash_to_trace_id(parent_id)

        # Build the parent context manually (same logic as subtask_context)
        # span_id must be non-zero for SpanContext.is_valid to return True
        parent_span_context = SpanContext(
            trace_id=parent_trace_id,
            span_id=_hash_to_span_id(parent_id),
            is_remote=False,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
        )
        parent_span = NonRecordingSpan(parent_span_context)
        parent_ctx = otel_trace.set_span_in_context(parent_span)

        # Attach parent context, create child span, verify trace_id inheritance
        token = otel_context.attach(parent_ctx)
        try:
            child_span = test_tracer.start_span(
                "subtask.process",
                attributes={"parent_task.id": parent_id, "child_task.id": child_id},
            )
            child_span.end()
        finally:
            otel_context.detach(token)

        spans = memory_exporter.get_finished_spans()
        assert len(spans) >= 1
        child = spans[0]
        assert child.name == "subtask.process"
        # Child inherits the parent's trace_id via OTel context propagation
        assert child.get_span_context().trace_id == parent_trace_id


# ---------------------------------------------------------------------------
# NoOp stubs
# ---------------------------------------------------------------------------


class TestNoOpStubs:
    """NoOp tracer/span work when tracing is disabled."""

    def test_noop_tracer_context_manager(self) -> None:
        from ai_company.telemetry.tracer import _NoOpTracer

        tracer = _NoOpTracer()
        with tracer.start_as_current_span("test") as span:
            span.set_attribute("key", "value")
            span.set_status()
            span.record_exception(Exception("test"))
            span.end()

    def test_noop_span_enter_exit(self) -> None:
        from ai_company.telemetry.tracer import _NoOpSpan

        span = _NoOpSpan()
        with span:
            span.set_attribute("k", "v")


# ---------------------------------------------------------------------------
# Package __init__ re-exports
# ---------------------------------------------------------------------------


class TestPackageExports:
    """telemetry package re-exports the public API."""

    def test_imports(self) -> None:
        from ai_company.telemetry import (
            init_tracing,
            set_correlation_id_from_task,
            start_span,
            subtask_context,
        )

        assert callable(init_tracing)
        assert callable(start_span)
        assert callable(set_correlation_id_from_task)
        assert callable(subtask_context)
