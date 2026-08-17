"""OpenTelemetry tracing for the task execution pipeline.

Provides a thin wrapper around the OTel API/SDK that activates only when
``AI_COMPANY_OTEL=1`` is set.  When disabled, NoOp tracers are used — zero
span-creation cost.

Usage::

    from ai_company.telemetry import init_tracing, start_span

    init_tracing()  # call once at startup
    with start_span("my.operation", attributes={"key": "value"}):
        ...
"""

from __future__ import annotations

import hashlib
import logging
import os
from contextlib import contextmanager
from typing import Any, Iterator

logger = logging.getLogger(__name__)

# OTel imports — gracefully degrade to NoOp when the SDK is not installed.
_TRACING_ENABLED = False
_tracer: Any = None  # opentelemetry.trace.Tracer or NoOpTracer


def _hash_task_id_to_trace_id(task_id: str) -> int:
    """Deterministically hash a task ID string to a 128-bit OTel trace ID."""
    digest = hashlib.sha256(task_id.encode()).digest()
    return int.from_bytes(digest[:16], byteorder="big")


def init_tracing(
    service_name: str = "ai-company",
    *,
    console: bool | None = None,
) -> bool:
    """Initialise the global OTel tracer.  Idempotent.

    Activates only when ``AI_COMPANY_OTEL=1`` (or ``true``/``yes``).  When
    *console* is ``None`` the console exporter is enabled automatically in
    non-OTLP mode (i.e. when ``AI_COMPANY_OTEL_ENDPOINT`` is not set).

    Returns ``True`` when tracing was activated, ``False`` when it is a no-op.
    """
    global _TRACING_ENABLED, _tracer

    if _TRACING_ENABLED:
        return True

    env_val = os.environ.get("AI_COMPANY_OTEL", "").lower().strip()
    if env_val not in ("1", "true", "yes"):
        _tracer = _NoOpTracer()
        return False

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    except ImportError:
        logger.warning(
            "AI_COMPANY_OTEL is set but opentelemetry-sdk is not installed. "
            "Install it with: pip install opentelemetry-sdk"
        )
        _tracer = _NoOpTracer()
        return False

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    endpoint = os.environ.get("AI_COMPANY_OTEL_ENDPOINT", "")

    if endpoint:
        # OTLP export — requires opentelemetry-exporter-otlp
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                OTLPSpanExporter,
            )

            exporter = OTLPSpanExporter(endpoint=endpoint)
            provider.add_span_processor(SimpleSpanProcessor(exporter))
            logger.info("OTel tracing active → OTLP endpoint %s", endpoint)
        except ImportError:
            logger.warning(
                "AI_COMPANY_OTEL_ENDPOINT is set but "
                "opentelemetry-exporter-otlp is not installed. "
                "Falling back to console exporter."
            )
            if console is not False:
                from ai_company.telemetry.exporter import ConsoleSpanExporter

                provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))  # type: ignore[arg-type]
    else:
        # Console export (dev mode)
        if console is not False:
            from ai_company.telemetry.exporter import ConsoleSpanExporter

            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))  # type: ignore[arg-type]

    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer(service_name)
    _TRACING_ENABLED = True
    logger.info("OTel tracing active → console (dev)")
    return True


def is_tracing_enabled() -> bool:
    """Return whether OTel tracing was successfully initialised."""
    return _TRACING_ENABLED


def get_tracer() -> Any:
    """Return the configured OTel tracer (or NoOpTracer)."""
    return _tracer


@contextmanager
def start_span(
    name: str,
    *,
    attributes: dict[str, Any] | None = None,
    trace_id: int | None = None,
    links: Any | None = None,
) -> Iterator[Any]:
    """Context manager that creates an OTel span.

    When tracing is disabled this is a no-op (yields ``None``).
    """
    if not _TRACING_ENABLED or _tracer is None:
        yield None
        return

    kwargs: dict[str, Any] = {}
    if attributes:
        kwargs["attributes"] = attributes
    if links:
        kwargs["links"] = links

    with _tracer.start_as_current_span(name, **kwargs) as span:
        yield span


def get_current_span_context() -> Any | None:
    """Return the current OTel span context, or ``None`` if no span is active."""
    if not _TRACING_ENABLED:
        return None
    from opentelemetry import trace as otel_trace

    span = otel_trace.get_current_span()
    ctx = span.get_span_context()
    if ctx and ctx.is_valid:
        return ctx
    return None


# ---------------------------------------------------------------------------
# NoOp stubs (used when tracing is disabled)
# ---------------------------------------------------------------------------


class _NoOpSpan:
    """Minimal stub returned when tracing is disabled."""

    def __enter__(self) -> _NoOpSpan:
        return self

    def __exit__(self, *_args: Any) -> None:
        pass

    def set_attribute(self, _key: str, _value: Any) -> None:
        pass

    def set_status(self, *_args: Any) -> None:
        pass

    def record_exception(self, _exc: BaseException) -> None:
        pass

    def end(self) -> None:
        pass


class _NoOpTracer:
    """Minimal stub tracer returned when tracing is disabled."""

    @contextmanager
    def start_as_current_span(
        self, _name: str, **_kwargs: Any
    ) -> Iterator[_NoOpSpan]:
        yield _NoOpSpan()
