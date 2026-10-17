"""Media commands — local-first audio transcription for Pharos."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ai_company.media.transcription import Transcriber

app = typer.Typer(help="Media operations — audio transcription (local-first)")
console = Console()


@app.command("transcribe")
def transcribe(
    audio: str = typer.Argument(..., help="Path to an audio file"),
    model_size: str = typer.Option(
        "small", help="Whisper model size (tiny/base/small/medium/large-v3)"
    ),
    language: str = typer.Option(None, help="Optional hint for audio language (e.g. en, ny)"),
    out: str = typer.Option("", help="Write transcript to this file instead of stdout"),
) -> None:
    """Transcribe an audio file locally with faster-whisper.

    Requires the optional ``pharos-whisper`` extra (``uv sync --extra pharos-whisper``).
    Without it, the command prints an explicit unavailable message.

    Args:
        audio: Path to an audio file.
        model_size: Whisper model size.
        language: Optional language hint.
        out: Write transcript to a file.
    """
    if not Path(audio).exists():
        console.print(f"[red]Audio file not found:[/red] {audio}")
        raise typer.Exit(1)

    transcriber = Transcriber(model_size=model_size)
    if not transcriber.is_available():
        console.print(
            "[yellow]Local transcription unavailable.[/yellow]\n"
            "Install the extra with: uv sync --extra pharos-whisper"
        )
        transcriber.close()
        raise typer.Exit(1)

    with console.status(f"Transcribing {audio} (model={model_size})..."):
        result = transcriber.transcribe(audio, language=language or None)
    transcriber.close()

    if result.status != "transcribed":
        console.print(f"[red]Transcription failed:[/red] {result.error}")
        raise typer.Exit(1)

    if out:
        Path(out).write_text(result.text, encoding="utf-8")
        console.print(f"[green]Wrote[/green] {out} ({len(result.text)} chars)")
    else:
        console.print(result.text)


__all__ = ["app"]
