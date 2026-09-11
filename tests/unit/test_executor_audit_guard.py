"""Unit tests for the executor audit smoke guard (ticket #71).

The canonical trail is append-only by definition: a tick that processes
tasks MUST record at least one audit event (task lifecycle + tool calls).
``_warn_on_silent_audit`` fires when a tick did work but the shared writer's
event counter did not advance — the exact failure mode that left the host
trail at 0 bytes during the OP-16 proof.
"""

from __future__ import annotations

import logging

from ai_company.executor.loop import _warn_on_silent_audit


class _StubWriter:
    def __init__(self, events_written: int = 0) -> None:
        self.events_written = events_written


def test_no_warning_when_tick_processes_nothing(caplog) -> None:
    with caplog.at_level(logging.WARNING, logger="ai_company.executor.loop"):
        _warn_on_silent_audit(processed=0, events_before=0, writer=_StubWriter(0))
    assert not caplog.records


def test_no_warning_when_trail_grew(caplog) -> None:
    with caplog.at_level(logging.WARNING, logger="ai_company.executor.loop"):
        _warn_on_silent_audit(processed=2, events_before=1, writer=_StubWriter(4))
    assert not caplog.records


def test_warning_when_tick_did_work_but_trail_did_not_grow(caplog) -> None:
    with caplog.at_level(logging.WARNING, logger="ai_company.executor.loop"):
        _warn_on_silent_audit(processed=1, events_before=3, writer=_StubWriter(3))
    assert len(caplog.records) == 1
    message = caplog.records[0].getMessage()
    assert "audit trail" in message
    assert "ticket #71" in message


def test_warning_when_writer_is_missing(caplog) -> None:
    with caplog.at_level(logging.WARNING, logger="ai_company.executor.loop"):
        _warn_on_silent_audit(processed=1, events_before=0, writer=None)
    assert len(caplog.records) == 1
    assert "audit trail" in caplog.records[0].getMessage()
