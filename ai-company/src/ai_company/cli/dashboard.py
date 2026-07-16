"""CLI command for the CEO dashboard."""

from __future__ import annotations

import webbrowser
from threading import Timer

import typer

app = typer.Typer(help="CEO dashboard")


def _open_browser(port: int) -> None:
    webbrowser.open(f"http://localhost:{port}")


@app.callback(invoke_without_command=True)
def dashboard(
    port: int = typer.Option(8420, help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't auto-open browser"),
) -> None:
    """Start the CEO dashboard web server."""
    import uvicorn

    if not no_open:
        Timer(1.5, _open_browser, args=[port]).start()

    typer.echo(f"Starting CEO dashboard at http://{host}:{port}")
    typer.echo("Press Ctrl+C to stop.\n")
    uvicorn.run(
        "ai_company.dashboard.app:app",
        host=host,
        port=port,
        log_level="info",
    )
