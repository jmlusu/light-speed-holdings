"""Span exporters for dev visibility and test assertions.

- ``ConsoleSpanExporter``: prints each completed span to stderr in a
  human-readable format (operation name, duration, attributes).
- ``InMemorySpanExporter``: collects spans in a list for test assertions.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

logger = logging.getLogger(__name__)


class ConsoleSpanExporter:
    """Prints completed spans to stderr for dev visibility."""

    def __init__(self, stream: Any = None) -> None:
        self._stream = stream or sys.stderr

    def export(self, spans: Any) -> None:
        """Export a batch of completed spans."""
        for span in self._format_spans(spans):
            print(span, file=self._stream, flush=True)

    def shutdown(self) -> None:
        pass

    def force_flush(self, _timeout_millis: int = 30_000) -> bool:
        return True

    def _format_spans(self, spans: Any) -> list[str]:
        lines: list[str] = []
        for span in spans:
            ctx = span.get_span_context()
            trace_id = format(ctx.trace_id, "032x") if ctx else "0" * 32
            span_id = format(ctx.span_id, "016x") if ctx else "0" * 16
            name = span.name
            duration_ms = self._duration_ms(span)

            attrs = dict(span.attributes) if span.attributes else {}
            attr_str = ""
            if attrs:
                parts = [f"{k}={v}" for k, v in sorted(attrs.items())]
                attr_str = " " + " ".join(parts)

            status_code = ""
            if hasattr(span, "status") and span.status:
                status_code = f" [{span.status.status_code.name}]"

            line = (
                f"[TRACE {trace_id[:12]}] "
                f"{name}{status_code} "
                f"({duration_ms:.1f}ms) "
                f"span={span_id[:8]}"
                f"{attr_str}"
            )
            lines.append(line)
        return lines

    def _duration_ms(self, span: Any) -> float:
        """Compute span duration in milliseconds from start/end timestamps."""
        start = getattr(span, "start_time", None)
        end = getattr(span, "end_time", None)
        if start and end and end > start:
            return float((end - start) / 1e6)  # nanoseconds → milliseconds
        return 0.0


class InMemorySpanExporter:
    """Collects spans in memory for test assertions."""

    def __init__(self) -> None:
        self.spans: list[Any] = []

    def export(self, spans: Any) -> None:
        """Export a batch of completed spans."""
        self.spans.extend(spans)

    def shutdown(self) -> None:
        pass

    def force_flush(self, _timeout_millis: int = 30_000) -> bool:
        return True

    def clear(self) -> None:
        """Reset collected spans."""
        self.spans.clear()

    def get_finished_spans(self) -> list[Any]:
        """Return all finished spans."""
        return list(self.spans)

    def find_spans(self, name: str) -> list[Any]:
        """Return spans matching the given operation name."""
        return [s for s in self.spans if s.name == name]

    def find_span(self, name: str) -> Any | None:
        """Return the first span matching the given operation name."""
        matches = self.find_spans(name)
        return matches[0] if matches else None
