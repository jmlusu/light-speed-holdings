"""Local-first audio transcription for Pharos (ADR-020 P1).

The transcriber lazily imports ``faster_whisper`` so the core package never
depends on it.  When the optional extra ``pharos-whisper`` is not installed the
``transcribe`` path returns a structured ``unavailable`` result instead of
raising, and ``is_available()`` is False.  Audio is processed on the local
machine only.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Outcome of a transcription attempt.

    ``status`` is ``transcribed`` (success), ``unavailable`` (faster-whisper
    not installed / no model), or ``error`` (input/transcription failure).
    ``text``/``segments`` are populated only on success.
    """

    status: str
    text: str = ""
    language: str = ""
    segments: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""


class Transcriber:
    """Transcribes audio via faster-whisper when available.

    The model is loaded lazily on first use and cached, so CLI/executor
    callers only pay the import+model cost when they actually transcribe.
    """

    def __init__(
        self,
        *,
        model_size: str = "small",
        device: str = "auto",
        compute_type: str = "int8",
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model: Any | None = None
        self._available: bool | None = None

    def is_available(self) -> bool:
        """Return True when faster-whisper can be imported."""
        if self._available is None:
            self._available = self._import_engine() is not None
        return self._available

    def _import_engine(self) -> Any | None:
        """Return the faster_whisper module or None without raising."""
        try:
            import faster_whisper

            return faster_whisper
        except ImportError:
            return None

    def _get_model(self) -> Any:
        """Build/cache the WhisperModel instance (raises when unavailable)."""
        engine = self._import_engine()
        if engine is None:
            raise RuntimeError(
                "faster-whisper is not installed. Install the optional extra: "
                "uv sync --extra pharos-whisper"
            )
        if self._model is None:
            self._model = engine.WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self._model

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        language: str | None = None,
    ) -> TranscriptionResult:
        """Transcribe *audio_path* locally.

        Returns ``status="unavailable"`` when faster-whisper is missing (never
        raises for that condition) and ``status="error"`` for input/processing
        failures.
        """
        path = Path(audio_path)
        if not path.exists():
            return TranscriptionResult(status="error", error=f"Audio file not found: {path}")

        if not self.is_available():
            return TranscriptionResult(
                status="unavailable",
                error=(
                    "faster-whisper not installed (extra 'pharos-whisper'). "
                    "Local transcription is disabled; install it or handle audio another way."
                ),
            )

        try:
            model = self._get_model()
            segments_iter, info = model.transcribe(str(path), language=language)
            segments: list[dict[str, Any]] = []
            for segment in segments_iter:
                segments.append(segment._asdict() if hasattr(segment, "_asdict") else {})

            language_out = getattr(info, "language", language or "")
            return TranscriptionResult(
                status="transcribed",
                text="\n".join(str(s.get("text", "")).strip() for s in segments if s.get("text")),
                language=language_out or "",
                segments=segments,
            )
        except Exception as exc:  # noqa: BLE001 - surface as a structured error
            logger.exception("Local transcription failed for %s", path)
            return TranscriptionResult(status="error", error=str(exc))

    def close(self) -> None:
        """Release the cached model reference (memory-friendly for CLIs)."""
        self._model = None
        self._available = None


__all__ = ["Transcriber", "TranscriptionResult"]
