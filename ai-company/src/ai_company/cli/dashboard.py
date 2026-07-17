"""CLI command for the CEO dashboard."""

from __future__ import annotations

import webbrowser
from threading import Timer

import typer

app = typer.Typer(help="CEO dashboard")
kpi_app = typer.Typer(help="Department KPI dashboards")

app.add_typer(kpi_app, name="kpi")


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


@kpi_app.command("list")
def kpi_list() -> None:
    """List all departments with KPIs."""
    from pathlib import Path

    import yaml

    kpi_path = Path(__file__).parent.parent.parent / "company" / "config" / "kpis.yaml"
    if not kpi_path.exists():
        typer.echo("KPI config not found at company/config/kpis.yaml")
        raise typer.Exit(1)

    with open(kpi_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    departments = data.get("departments", {})
    if not departments:
        typer.echo("No departments configured.")
        return

    typer.echo("Department KPIs")
    typer.echo("=" * 60)
    for dept_id, dept in departments.items():
        kpis = dept.get("kpis", [])
        typer.echo(f"\n  {dept.get('name', dept_id)} ({len(kpis)} KPIs)")
        for kpi in kpis:
            target = kpi.get("target", "N/A")
            unit = kpi.get("unit", "")
            freq = kpi.get("frequency", "")
            typer.echo(f"    - {kpi['name']}: target {target} {unit} ({freq})")


@kpi_app.command("show")
def kpi_show(
    department: str = typer.Argument(..., help="Department ID (e.g. engineering)"),
) -> None:
    """Show KPIs for a specific department."""
    from pathlib import Path

    import yaml

    kpi_path = Path(__file__).parent.parent.parent / "company" / "config" / "kpis.yaml"
    if not kpi_path.exists():
        typer.echo("KPI config not found at company/config/kpis.yaml")
        raise typer.Exit(1)

    with open(kpi_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    departments = data.get("departments", {})
    if department not in departments:
        typer.echo(f"Department '{department}' not found.")
        typer.echo(f"Available: {', '.join(departments.keys())}")
        raise typer.Exit(1)

    dept = departments[department]
    kpis = dept.get("kpis", [])

    typer.echo(f"\n{dept.get('name', department)} — KPI Dashboard")
    typer.echo("=" * 60)
    for kpi in kpis:
        target = kpi.get("target", "N/A")
        unit = kpi.get("unit", "")
        freq = kpi.get("frequency", "")
        typer.echo(f"\n  {kpi['name']}")
        typer.echo(f"    Target:    {target} {unit}")
        typer.echo(f"    Frequency: {freq}")
        typer.echo(f"    ID:        {kpi['id']}")
        if kpi.get("description"):
            typer.echo(f"    Desc:      {kpi['description']}")
    typer.echo("")
