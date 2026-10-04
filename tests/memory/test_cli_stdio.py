"""Regression tests: LS-MEM CLI stdio hardening for legacy Windows consoles."""

import io
import sys

from src.ai_company.lsmem import cli as lsmem_cli


class _FakeStream:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def reconfigure(self, **kwargs: str) -> None:
        self.calls.append(kwargs)


def test_ensure_utf8_stdio_configures_streams(monkeypatch) -> None:
    out = _FakeStream()
    err = _FakeStream()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(sys, "stderr", err)

    lsmem_cli._ensure_utf8_stdio()

    expected = [{"encoding": "utf-8", "errors": "replace"}]
    assert out.calls == expected
    assert err.calls == expected


def test_ensure_utf8_stdio_tolerates_streams_without_reconfigure(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    monkeypatch.setattr(sys, "stderr", io.StringIO())

    lsmem_cli._ensure_utf8_stdio()


def test_ensure_utf8_stdio_swallows_reconfigure_errors(monkeypatch) -> None:
    class _BrokenStream:
        def reconfigure(self, **kwargs: str) -> None:
            raise ValueError("stream closed")

    monkeypatch.setattr(sys, "stdout", _BrokenStream())
    monkeypatch.setattr(sys, "stderr", _BrokenStream())

    lsmem_cli._ensure_utf8_stdio()
