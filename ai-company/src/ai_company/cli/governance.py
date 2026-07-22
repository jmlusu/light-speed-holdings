"""CLI commands for data governance operations.

Exposes the :class:`~ai_company.data.governance.DataGovernance` engine
via five user-facing commands:

- ``report`` — generate a comprehensive governance status report
- ``retention`` — check data retention status across all tables
- ``compliance`` — run a compliance check for violations
- ``owners`` — list registered data owners
- ``policies`` — list active retention policies
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

app = typer.Typer(help="Data governance — ownership, retention, compliance")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _resolve_db_path(database_path: str) -> str:
    """Resolve a database path, substituting ``{workdir}`` placeholders."""
    return database_path.replace("{workdir}", str(Path.cwd()))


def _init_governance(
    database_path: str,
) -> tuple[Any, Any]:
    """Initialise the Database and DataGovernance instances.

    Returns:
        Tuple of ``(db, governance)`` instances.

    Raises:
        typer.Exit: If the database cannot be opened or schema initialised.
    """
    from ai_company.data.database import Database
    from ai_company.data.governance import DataGovernance

    resolved = _resolve_db_path(database_path)

    try:
        db = Database(resolved)
        db.init_schema()
    except Exception as exc:
        typer.echo(f"Error: Cannot open database at {resolved}: {exc}", err=True)
        raise typer.Exit(1) from exc

    try:
        gov = DataGovernance(db)
    except Exception as exc:
        db.close()
        typer.echo(f"Error: Failed to initialise DataGovernance: {exc}", err=True)
        raise typer.Exit(1) from exc

    return db, gov


def _format_report(report: dict[str, Any]) -> str:
    """Pretty-format a governance report dict for the terminal."""
    lines: list[str] = [
        "Data Governance Report",
        "=====================",
        f"Generated at: {report.get('generated_at', 'unknown')}",
        "",
    ]

    tables = report.get("tables", {})
    if tables:
        lines.append(f"Tables ({len(tables)}):")
        lines.append("-" * 72)
        # Header
        lines.append(
            f"  {'Table':<20} {'Rows':>6} {'Class':<14} {'Owner':<14} "
            f"{'Retn':>5} {'Action':<10} {'Past':>5}"
        )
        lines.append(
            f"  {'-'*19} {'-'*6} {'-'*13} {'-'*13} "
            f"{'-'*4} {'-'*9} {'-'*4}"
        )
        for tbl, stats in sorted(tables.items()):
            lines.append(
                f"  {tbl:<20} {stats['row_count']:>6} "
                f"{stats['classification']:<14} {stats['owner']:<14} "
                f"{stats['retention_days']:>5} {stats['action']:<10} "
                f"{stats['records_past_retention']:>5}"
            )
        lines.append("")

    owners = report.get("owners", [])
    if owners:
        lines.append(f"Data Owners ({len(owners)}):")
        lines.append("-" * 72)
        for o in owners:
            lines.append(f"  {o['owner_id']:<16} — {o['role']} ({o['department']})")
            if o.get("responsibilities"):
                for r in o["responsibilities"]:
                    lines.append(f"    • {r}")
        lines.append("")

    policies = report.get("policies", [])
    if policies:
        lines.append(f"Policies ({len(policies)}):")
        lines.append("-" * 72)
        for p in policies:
            lines.append(
                f"  {p['table']:<20} {p['action']:<10} "
                f"{p['retention_days']:>4}d  [{p['classification']}]  "
                f"Owner: {p['owner']}"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@app.command()
def report(
    database: str = typer.Option(
        "data/ai_company.db",
        "--database",
        "-d",
        help="Path to the SQLite database file",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output raw JSON instead of formatted text",
    ),
) -> None:
    """Generate a comprehensive governance status report.

    Shows table sizes, retention status, ownership mapping, and
    classification distribution across all governed data stores.
    """
    _, gov = _init_governance(database)

    try:
        result = gov.governance_report()
    except Exception as exc:
        typer.echo(f"Error: Failed to generate governance report: {exc}", err=True)
        raise typer.Exit(1) from exc

    if json_output:
        typer.echo(json.dumps(result, indent=2, default=str))
    else:
        typer.echo(_format_report(result))


@app.command()
def retention(
    database: str = typer.Option(
        "data/ai_company.db",
        "--database",
        "-d",
        help="Path to the SQLite database file",
    ),
    apply: bool = typer.Option(
        False,
        "--apply",
        "-a",
        help="Actually apply retention policies (archive/purge/anonymize)",
    ),
    table: str = typer.Option(
        "",
        "--table",
        "-t",
        help="Filter retention status to a specific table",
    ),
) -> None:
    """Check data retention status across all data stores.

    By default, this is a dry-run that shows how many records *would* be
    affected by retention policies. Use ``--apply`` to actually enforce them.
    """
    db, gov = _init_governance(database)

    try:
        report_data = gov.governance_report()
    except Exception as exc:
        typer.echo(f"Error: Failed to read governance state: {exc}", err=True)
        raise typer.Exit(1) from exc

    tables = report_data.get("tables", {})

    if table:
        if table not in tables:
            typer.echo(f"Error: Unknown table '{table}'. Known tables: {', '.join(sorted(tables))}", err=True)
            raise typer.Exit(1)
        filtered = {table: tables[table]}
    else:
        filtered = tables

    if not filtered:
        typer.echo("No governed tables found.")
        return

    total_past = 0
    lines: list[str] = [
        "Data Retention Status",
        "=====================",
        "",
        f"{'Table':<20} {'Rows':>6} {'Retention':>10} {'Past':>6} {'Action':<10}",
        f"{'-'*19} {'-'*6} {'-'*9} {'-'*6} {'-'*9}",
    ]
    for tbl, stats in sorted(filtered.items()):
        past = stats.get("records_past_retention", 0)
        total_past += past
        days = stats.get("retention_days", 0)
        lines.append(
            f"  {tbl:<20} {stats['row_count']:>6} {days:>4}d{'':>6} "
            f"{past:>6} {stats['action']:<10}"
        )

    lines.append("")
    if total_past > 0:
        lines.append(f"  ** {total_past} records past retention across {len(filtered)} table(s).")
    else:
        lines.append("  No records past retention. All tables within policy.")

    typer.echo("\n".join(lines))

    if apply:
        typer.echo("")
        typer.echo("Applying retention policies...")
        try:
            results = gov.apply_retention_policies()
        except Exception as exc:
            typer.echo(f"Error: Failed to apply retention policies: {exc}", err=True)
            raise typer.Exit(1) from exc

        for table_name, count in results.items():
            typer.echo(f"  {table_name:<20} {count} records processed")
        total = sum(results.values())
        typer.echo(f"Total: {total} records processed across {len(results)} table(s).")
    else:
        typer.echo("")
        typer.echo("Dry-run mode. Use --apply to enforce these policies.")

    db.close()


@app.command()
def compliance(
    database: str = typer.Option(
        "data/ai_company.db",
        "--database",
        "-d",
        help="Path to the SQLite database file",
    ),
) -> None:
    """Run a compliance check and report governance violations."""
    _, gov = _init_governance(database)

    try:
        findings = gov.compliance_check()
    except Exception as exc:
        typer.echo(f"Error: Compliance check failed: {exc}", err=True)
        raise typer.Exit(1) from exc

    if not findings:
        typer.echo("Compliance Check: PASSED")
        typer.echo("No violations or warnings found.")
        return

    typer.echo("Compliance Check Results")
    typer.echo("========================")
    typer.echo(f"Total findings: {len(findings)}")
    typer.echo("")

    severities = {"critical": 0, "warning": 0, "info": 0}
    for f in findings:
        sev = f.get("severity", "info")
        severities[sev] = severities.get(sev, 0) + 1

    for sev in ("critical", "warning", "info"):
        count = severities.get(sev, 0)
        if count:
            icon = {"critical": "🔴", "warning": "⚠️", "info": "ℹ️"}.get(sev, "•")
            typer.echo(f"  {icon} {sev.upper()}: {count}")

    typer.echo("")

    for idx, f in enumerate(findings, 1):
        sev = f.get("severity", "info")
        icon = {"critical": "🔴", "warning": "⚠️", "info": "ℹ️"}.get(sev, "•")
        table_name = f.get("table", "?")
        finding_text = f.get("finding", "")
        affected = f.get("records_affected")

        typer.echo(f"  #{idx} [{sev.upper()}] {table_name}")
        typer.echo(f"     {finding_text}")
        if affected is not None:
            typer.echo(f"     Records affected: {affected}")
        typer.echo("")

    typer.echo("Compliance Check: COMPLETED")


@app.command()
def owners(
    database: str = typer.Option(
        "data/ai_company.db",
        "--database",
        "-d",
        help="Path to the SQLite database file",
    ),
    table: str = typer.Option(
        "",
        "--table",
        "-t",
        help="Show the owner for a specific table only",
    ),
) -> None:
    """List registered data owners and their responsibilities."""
    _, gov = _init_governance(database)

    if table:
        owner = gov.get_owner(table)
        if owner is None:
            typer.echo(f"Error: No registered owner for table '{table}'.", err=True)
            raise typer.Exit(1)

        typer.echo(f"Data Owner for '{table}'")
        typer.echo("=" * 40)
        typer.echo(f"  Owner ID:      {owner.owner_id}")
        typer.echo(f"  Department:    {owner.department}")
        typer.echo(f"  Role:          {owner.role}")
        typer.echo(f"  Email:         {owner.email or '(not set)'}")
        if owner.responsibilities:
            typer.echo("  Responsibilities:")
            for r in owner.responsibilities:
                typer.echo(f"    • {r}")
        return

    try:
        owners_list = gov.list_owners()
    except Exception as exc:
        typer.echo(f"Error: Failed to list data owners: {exc}", err=True)
        raise typer.Exit(1) from exc

    if not owners_list:
        typer.echo("No data owners registered.")
        return

    typer.echo(f"Data Owners ({len(owners_list)}):")
    typer.echo("=" * 60)
    for o in owners_list:
        typer.echo(f"  {o['owner_id']:<16} — {o['role']:<20} ({o['department']})")
        if o.get("responsibilities"):
            for r in o["responsibilities"]:
                typer.echo(f"    • {r}")
        typer.echo("")


@app.command("audit-trail")
def audit_trail(
    limit: int = typer.Option(20, "-n", "--limit", help="Maximum events to show"),
    event_type: str = typer.Option("", "--type", "-t", help="Filter by event type"),
    agent_id: str = typer.Option("", "--agent", "-a", help="Filter by agent ID"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output raw JSON"),
) -> None:
    """Show recent audit trail events.

    Reads the JSONL audit log and displays the most recent events,
    optionally filtered by type or agent.
    """
    from ai_company.audit.reader import AuditReader

    audit_path = ".opencode/audit.jsonl"
    reader = AuditReader(audit_path)

    try:
        if agent_id:
            events = reader.read_by_agent(agent_id)
        elif event_type:
            events = reader.read_by_type(event_type)
        else:
            events = reader.read_all()
    except Exception as exc:
        typer.echo(f"Error: Failed to read audit trail: {exc}", err=True)
        raise typer.Exit(1) from exc

    # Apply limit (most recent first)
    events = events[-limit:]
    events.reverse()

    if json_output:
        import json
        typer.echo(json.dumps(
            [e.model_dump() for e in events],
            indent=2, default=str,
        ))
        return

    if not events:
        typer.echo("No audit events found.")
        return

    typer.echo(f"Recent Audit Events ({len(events)} shown):")
    typer.echo("=" * 72)
    for e in events:
        typer.echo(f"  [{e.timestamp}] {e.event_type.value}")
        typer.echo(f"    Agent: {e.agent_id}  Task: {e.task_id}")
        if e.detail:
            detail_preview = e.detail[:100] + "..." if len(e.detail) > 100 else e.detail
            typer.echo(f"    Detail: {detail_preview}")
        typer.echo("")


@app.command("risk-summary")
def risk_summary(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output raw JSON"),
) -> None:
    """Show risk register summary.

    Parses the risk register markdown and displays a summary of risks
    by severity level with status indicators.
    """
    import re
    from pathlib import Path

    risk_file = Path(__file__).parent.parent.parent.parent / "docs" / "RISK-REGISTER.md"
    if not risk_file.exists():
        typer.echo(f"Error: Risk register not found at {risk_file}", err=True)
        raise typer.Exit(1)

    content = risk_file.read_text(encoding="utf-8")

    # Parse risk table rows
    risks: list[dict] = []
    for match in re.finditer(
        r"\|\s*(R\d+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|",
        content,
    ):
        rid, category, description, likelihood, impact, level = match.groups()
        risks.append({
            "id": rid,
            "category": category.strip(),
            "description": description.strip(),
            "likelihood": int(likelihood),
            "impact": int(impact),
            "level": level.strip(),
            "score": int(likelihood) * int(impact),
        })

    if not risks:
        typer.echo("No risks found in register.")
        return

    if json_output:
        import json
        summary = {
            "total_risks": len(risks),
            "by_level": {},
            "risks": risks,
        }
        for r in risks:
            lvl = r["level"]
            summary["by_level"][lvl] = summary["by_level"].get(lvl, 0) + 1
        typer.echo(json.dumps(summary, indent=2))
        return

    # Group by level
    by_level: dict[str, list[dict]] = {}
    for r in risks:
        by_level.setdefault(r["level"], []).append(r)

    typer.echo("Risk Register Summary")
    typer.echo("=" * 60)
    typer.echo(f"Total risks: {len(risks)}")
    typer.echo("")

    level_order = ["Critical", "High", "Medium", "Low"]
    level_icons = {"Critical": "CRIT", "High": "HIGH", "Medium": " MED", "Low": " LOW"}

    for level in level_order:
        items = by_level.get(level, [])
        if not items:
            continue
        icon = level_icons.get(level, level.upper())
        typer.echo(f"  [{icon}] {level}: {len(items)} risks")
        for r in sorted(items, key=lambda x: x["score"], reverse=True):
            typer.echo(f"    {r['id']} ({r['category']}) — score {r['score']}: {r['description'][:60]}")
        typer.echo("")


@app.command()
def policies(
    database: str = typer.Option(
        "data/ai_company.db",
        "--database",
        "-d",
        help="Path to the SQLite database file",
    ),
    table: str = typer.Option(
        "",
        "--table",
        "-t",
        help="Show policy for a specific table only",
    ),
) -> None:
    """List active retention policies across all governed tables.

    Displays per-table retention windows, actions, and classification levels.
    """
    _, gov = _init_governance(database)

    try:
        policies_list = gov.list_policies()
    except Exception as exc:
        typer.echo(f"Error: Failed to list retention policies: {exc}", err=True)
        raise typer.Exit(1) from exc

    if table:
        matching = [p for p in policies_list if p["table"] == table]
        if not matching:
            typer.echo(f"Error: No policy found for table '{table}'.", err=True)
            raise typer.Exit(1)
        policies_list = matching

    if not policies_list:
        typer.echo("No retention policies configured.")
        return

    typer.echo(f"Active Retention Policies ({len(policies_list)}):")
    typer.echo("=" * 72)
    lines: list[str] = []
    for p in policies_list:
        lines.append(
            f"  {p['table']:<20} — {p['action']:<10} "
            f"{p['retention_days']:>4}d  [{p['classification']}]  "
            f"Owner: {p['owner']}"
        )
        if p.get("description"):
            lines.append(f"    {p['description']}")

    typer.echo("\n".join(lines))
