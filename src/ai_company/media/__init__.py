"""Media processing — transcription and audio utilities for Pharos.

Local-first per ADR-020: transcription runs on this machine when the optional
``faster-whisper`` dependency is installed.  Without it the transcriber returns
a structured ``unavailable`` result so callers/CLIs degrade gracefully instead
of crashing.  Audio never leaves the machine.
"""

from ai_company.media.transcription import Transcriber, TranscriptionResult

__all__ = ["Transcriber", "TranscriptionResult"]
