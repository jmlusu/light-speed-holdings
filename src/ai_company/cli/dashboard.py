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
    ctx: typer.Context,
    port: int = typer.Option(8420, help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't auto-open browser"),
) -> None:
    """Start the CEO dashboard web server.

    Args:
        ctx: Typer invocation context (used to detect subcommands).
        port: Port to serve on.
        host: Host to bind to.
        no_open: Don't auto-open the browser.
    """
    if ctx.invoked_subcommand is not None:
        return

    # ADR-012: ``open`` auth mode bypasses the API-key guard, so it may only
    # bind to a loopback interface.
    import os

    from ai_company.dashboard.app import is_loopback_host

    if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open" and not is_loopback_host(host):
        typer.echo(
            "Error: DASHBOARD_AUTH_MODE=open is only allowed on loopback hosts "
            "(127.0.0.1 / ::1). Refusing to start.",
            err=True,
        )
        raise typer.Exit(1)

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


@app.command("backfill")
def backfill(
    db_path: str = typer.Option(
        "",
        "--db-path",
        help="SQLite database path (default: <project root>/data/ai_company.db)",
    ),
) -> None:
    """Import operational telemetry files into the SQLite data layer.

    Idempotent (INSERT OR REPLACE) import of tasks, audit events, LLM cost
    records, KPI history, and escalations from the project's legacy files into
    SQLite so the dashboard renders real data. Safe to re-run.

    Args:
        db_path: SQLite database path (default: <project root>/data/ai_company.db).
    """

    from ai_company.data import (
        AuditStore,
        CostAnalytics,
        EscalationStore,
        KPIPipeline,
        TaskStore,
        init_database,
    )
    from ai_company.paths import get_audit_path, get_database_path, get_project_root

    # Source telemetry files live under the project root (independent of the
    # data root override, which only relocates the runtime SQLite database).
    root = get_project_root()
    db = init_database(db_path or str(get_database_path()))

    typer.echo(f"Backfilling SQLite data layer at {db.path}")
    typer.echo("=" * 60)

    counts: dict[str, int] = {}

    # Tasks (.opencode/inbox.json)
    try:
        counts["tasks"] = TaskStore(db).import_json(root / ".opencode" / "inbox.json")
    except Exception as exc:  # noqa: BLE001 - report per-source failures
        typer.echo(f"  [skip] tasks: {exc}")
    typer.echo(f"  tasks:        {counts.get('tasks', 0)}")

    # Audit events (<data root>/.opencode/audit — canonical, tickets #59 / #71)
    try:
        counts["audit_events"] = AuditStore(db).import_jsonl(str(get_audit_path()))
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  [skip] audit_events: {exc}")
    typer.echo(f"  audit_events: {counts.get('audit_events', 0)}")

    # LLM cost records (results/cost_log.jsonl)
    try:
        counts["cost_records"] = CostAnalytics(db).import_from_jsonl(
            root / "results" / "cost_log.jsonl"
        )
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  [skip] cost_records: {exc}")
    typer.echo(f"  cost_records: {counts.get('cost_records', 0)}")

    # Escalations (orchestrator/escalation.yaml)
    try:
        counts["escalations"] = EscalationStore(db).import_from_yaml(
            root / "orchestrator" / "escalation.yaml"
        )
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  [skip] escalations: {exc}")
    typer.echo(f"  escalations:  {counts.get('escalations', 0)}")

    # KPI history (dashboard/kpi_history/*_history.ndjson)
    kpi_history_dir = root / "dashboard" / "kpi_history"
    kpi_total = 0
    if kpi_history_dir.exists():
        pipeline = KPIPipeline(db)
        for ndjson in sorted(kpi_history_dir.glob("*_history.ndjson")):
            department = ndjson.name.replace("_history.ndjson", "")
            try:
                kpi_total += pipeline.import_from_ndjson(department, ndjson)
            except Exception as exc:  # noqa: BLE001
                typer.echo(f"  [skip] kpi {department}: {exc}")
    typer.echo(f"  kpi_entries:  {kpi_total}")

    typer.echo("=" * 60)
    typer.echo("Backfill complete. Start the dashboard to serve this data.")
    if db_path:
        typer.echo(
            "Note: the running dashboard reads its own configured data root; "
            "point DASHBOARD_DATA_DIR at the db's parent to use it."
        )


@app.command("cleanup")
def cleanup(
    purge_all: bool = typer.Option(
        False, "--purge-all", help="Delete ALL tasks (not just test/demo)"
    ),
    db_path: str = typer.Option("", "--db-path", help="SQLite database path"),
) -> None:
    """Remove test and demo tasks from the database.

    By default, removes tasks matching the refined demo/test markers
    (``proj-acme-chatbot`` in id/instruction, ``Test `` instruction prefix,
    ``test-``/``verify-`` id prefixes) and prints per-class counts. Agents
    whose id merely starts with ``test`` (e.g. the real ``test-agent``) are
    NOT a marker. Use --purge-all to remove everything.
    """
    from ai_company.data import TaskStore, init_database
    from ai_company.paths import get_database_path

    db = init_database(db_path or str(get_database_path()))
    store = TaskStore(db)

    before = store.count()

    if purge_all:
        deleted = store.purge_all_tasks()
        typer.echo(f"Purged all {deleted} tasks from database.")
    else:
        counts = store.test_task_breakdown()
        deleted = store.cleanup_test_tasks()
        typer.echo(f"Removed {deleted} test/demo tasks:")
        typer.echo(f"  acme_demo        (proj-acme-chatbot): {counts['acme_demo']}")
        typer.echo(f"  test_instruction ('Test ' prefix):     {counts['test_instruction']}")
        typer.echo(f"  test_id          (test-/verify- ids):   {counts['test_id']}")

    after = store.count()
    typer.echo(f"Tasks: {before} -> {after}")

    if after == 0:
        typer.echo("\nDatabase is clean. Only real organizational tasks will appear.")


@app.command("queue")
def queue(
    json_output: bool = typer.Option(
        False, "--json", help="Emit the snapshot as JSON (scripting friendly)"
    ),
) -> None:
    """Show task backlog / queue observability snapshot (read-only, C3).

    Print queue depth, per-status spread, oldest pending age, stale-pending
    count, and dead-letter depth for the task inbox.  Does not mutate the
    queue.
    """
    import json as _json

    from ai_company.dashboard.backlog import backlog_summary

    summary = backlog_summary()
    if json_output:
        typer.echo(_json.dumps(summary, indent=2, default=str))
        return

    def _fmt_age(age_s: float | None) -> str:
        if age_s is None:
            return "—"
        if age_s < 60:
            return f"{int(age_s)}s"
        if age_s < 3600:
            return f"{int(age_s // 60)}m {int(age_s % 60)}s"
        return f"{int(age_s // 3600)}h {int((age_s % 3600) // 60)}m"

    by_status = summary["by_status"]
    typer.echo("Task Backlog / Queue")
    typer.echo("=" * 60)
    typer.echo(f"Total tasks:        {summary['total']}")
    if by_status:
        for status in sorted(by_status):
            typer.echo(f"  {status:<16} {by_status[status]}")
    else:
        typer.echo("  (empty queue)")
    typer.echo("-" * 60)
    typer.echo(f"Oldest pending age: {_fmt_age(summary['oldest_pending_age_s'])}")
    typer.echo(
        f"Stale pending (>{summary['stale_threshold_s']:.0f}s): {summary['stale_pending_count']}"
    )
    typer.echo(f"Dead-letter queue:  {summary['dead_letter_count']}")
    typer.echo(f"Inbox:              {summary['inbox_path']}")


@kpi_app.command("list")
def kpi_list() -> None:
    """List all departments with KPIs."""
    import yaml

    from ai_company.paths import get_project_root

    kpi_path = get_project_root() / "company" / "config" / "kpis.yaml"
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
    """Show KPIs for a specific department.

    Args:
        department: Department ID (e.g. engineering).
    """
    import yaml

    from ai_company.paths import get_project_root

    kpi_path = get_project_root() / "company" / "config" / "kpis.yaml"
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
