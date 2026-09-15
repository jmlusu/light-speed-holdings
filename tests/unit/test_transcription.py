"""Unit tests for the local-first Pharos transcriber (ADR-020 P1)."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

from ai_company.media.transcription import Transcriber


class FakeSegment:
    def _asdict(self) -> dict:  # type: ignore[no-untyped-def]
        return {"start": 0.0, "end": 1.2, "text": " Hello world "}


class FakeInfo:
    language = "en"


class FakeModel:
    def transcribe(self, path: str, language: str | None = None):  # type: ignore[no-untyped-def]
        return iter([FakeSegment()]), FakeInfo()


def test_unavailable_when_faster_whisper_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(Transcriber, "_import_engine", lambda self: None)
    audio = tmp_path / "clip.mp3"
    audio.write_bytes(b"fake")
    transcriber = Transcriber()
    assert transcriber.is_available() is False
    result = transcriber.transcribe(audio)
    assert result.status == "unavailable"
    assert "pharos-whisper" in result.error


def test_missing_file_returns_error(tmp_path: Path) -> None:
    transcriber = Transcriber()
    result = transcriber.transcribe(tmp_path / "nope.mp3")
    assert result.status == "error"
    assert "not found" in result.error


def test_transcribe_success_with_fake_engine(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Drive a successful transcription using a fake faster_whisper module."""
    fake = types.ModuleType("faster_whisper")
    fake.WhisperModel = lambda *a, **k: FakeModel()  # type: ignore[assignment]
    monkeypatch.setitem(sys.modules, "faster_whisper", fake)

    audio = tmp_path / "clip.wav"
    audio.write_bytes(b"fake audio")
    transcriber = Transcriber()
    result = transcriber.transcribe(audio)
    assert result.status == "transcribed"
    assert result.text == "Hello world"
    assert result.language == "en"
    assert len(result.segments) == 1


def test_close_releases_model(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = types.ModuleType("faster_whisper")
    fake.WhisperModel = lambda *a, **k: object()  # type: ignore[assignment]
    monkeypatch.setitem(sys.modules, "faster_whisper", fake)

    transcriber = Transcriber()
    transcriber._model = object()  # simulate a loaded model
    transcriber._available = True
    transcriber.close()
    assert transcriber._model is None
    assert transcriber._available is None


def test_faster_whisper_not_imported_at_module_load(tmp_path: Path) -> None:
    """Importing the media package must not import faster_whisper."""
    assert "faster_whisper" not in list(sys.modules)
