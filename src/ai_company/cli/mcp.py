"""Pharos MCP server commands — run the stdio JSON-RPC server."""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(help="Pharos Content Intelligence MCP server")
console = Console()


@app.command()
def stdio() -> None:
    """Serve the Pharos MCP protocol over stdio (newline-delimited JSON-RPC).

    Reads requests from stdin and writes responses to stdout — the transport
    MCP clients (Claude/Desktop, OpenCode, etc.) speak by default. Set
    ``DASHBOARD_RUN_KEY`` / ``DASHBOARD_APPROVE_KEY`` / ``DASHBOARD_ADMIN_KEY``
    to enable RBAC; read tools require ``run``, ``publish_queue`` requires
    ``approve``. Set ``PHAROS_DOCS_DIR`` to point at the docs/Pharos corpus.
    """
    from ai_company.mcp.server import PharosMcpServer

    server = PharosMcpServer()
    raise SystemExit(server.run_stdio())


@app.command("tools")
def list_tools() -> None:
    """Print the MCP tool surface exposed by the server."""
    from ai_company.mcp.server import PharosMcpServer

    server = PharosMcpServer()
    for tool in server._tool_schemas():
        console.print(f"[bold]{tool['name']}[/bold] — {tool['description']}")


__all__ = ["app"]
