"""LS-MEM CLI — Typer entrypoint for `ai-company memory` commands."""

import json
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from .audit import AuditLogger
from .classification import ClassificationLayer
from .engine import EngineConfig, LSMEMEngine
from .gateway import GatewayConfig, PermissionGateway
from .redaction import SecretScanner
from .scoring import MemoryScorer

app = typer.Typer(name="memory", help="LS-MEM — LightSpeed Memory Engine")
console = Console()


def get_engine(
    workspace: Optional[Path] = None,
    config_path: Optional[Path] = None,
) -> LSMEMEngine:
    """Create and initialize engine."""
    # Resolve workspace
    if workspace is None:
        workspace = Path.cwd()

    # Resolve config
    if config_path is None:
        config_path = workspace / ".lightspeed" / "memory" / "config.yaml"

    # Load config
    config = EngineConfig()
    if config_path.exists():
        import yaml

        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        # Merge user config (simple shallow merge for now)
        for key, value in user_config.items():
            if hasattr(config, key) and isinstance(getattr(config, key), dict):
                getattr(config, key).update(value)
            else:
                setattr(config, key, value)

    # Resolve DB path
    db_dir = workspace / ".lightspeed" / "memory"
    db_path = db_dir / "memory.db"

    # Initialize components
    scanner = SecretScanner()
    classifier = ClassificationLayer()
    gateway = PermissionGateway(GatewayConfig.from_dict(config.gateway))

    audit_db = db_dir / "audit" / "audit.db"
    auditor = AuditLogger(
        audit_db,
        retention_days_crud=config.audit.get("retention_days_crud", 90),
        retention_days_gateway=config.audit.get("retention_days_gateway", 365),
    )

    scorer = MemoryScorer()

    engine = LSMEMEngine(
        db_path=db_path,
        config=config,
        scanner=scanner,
        classifier=classifier,
        gateway=gateway,
        auditor=auditor,
        scorer=scorer,
    )

    return engine


@app.command()
def remember(
    content: Annotated[str, typer.Argument(help="Memory content to store")],
    type: Annotated[
        str,
        typer.Option(
            ..., "--type", "-t", help="Memory type (observation, decision, architecture, etc.)"
        ),
    ],
    title: Annotated[str, typer.Option(..., "--title", help="Memory title")],
    project: Annotated[str, typer.Option("--project", "-p", help="Project name")] = "default",
    created_by: Annotated[str, typer.Option("--created-by", help="Creator identifier")] = "cli",
    source: Annotated[
        str, typer.Option("--source", help="Source (agent, human, import, etc.)")
    ] = "cli",
    classification: Annotated[
        str, typer.Option("--classification", "-c", help="Classification level")
    ] = "INTERNAL",
    confidence: Annotated[float, typer.Option("--confidence", help="Confidence 0.0-1.0")] = 0.5,
    tags: Annotated[Optional[str], typer.Option("--tags", help="Comma-separated tags")] = None,
    ttl_days: Annotated[
        Optional[int], typer.Option("--ttl", help="TTL in days (default per type)")
    ] = None,
) -> None:
    """Store a new memory."""
    try:
        engine = get_engine()
        tags_list = [t.strip() for t in tags.split(",")] if tags else None

        record = engine.remember(
            content=content,
            type=type,
            title=title,
            project=project,
            created_by=created_by,
            source=source,
            classification=classification,
            confidence=confidence,
            tags=tags_list,
            ttl_days=ttl_days,
        )
        console.print(
            f"[green]✓[/green] Stored memory [bold]{record.id}[/bold] (tier {record.tier}, {record.classification})"
        )
        console.print(f"  Title: {record.title}")
        console.print(f"  Project: {record.project}")
        console.print(f"  Correlation: {record.correlation_id}")
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]✗[/red] Unexpected error: {e}")
        raise typer.Exit(1) from e
    finally:
        engine.close()


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Search query")],
    project: Annotated[
        Optional[str], typer.Option("--project", "-p", help="Filter by project")
    ] = None,
    type: Annotated[Optional[str], typer.Option("--type", "-t", help="Filter by type")] = None,
    classification: Annotated[
        Optional[str], typer.Option("--classification", "-c", help="Filter by classification")
    ] = None,
    limit: Annotated[int, typer.Option("--limit", "-l", help="Max results")] = 15,
    min_tier: Annotated[int, typer.Option("--min-tier", help="Minimum tier (1-3)")] = 1,
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Search memories via FTS5."""
    engine = get_engine()
    try:
        results = engine.search(
            query=query,
            project=project,
            type_filter=type,
            classification_filter=classification,
            limit=limit,
            min_tier=min_tier,
        )

        if json_output:
            data = [
                {
                    "id": r.id,
                    "type": r.type,
                    "title": r.title,
                    "content": r.content[:200],
                    "project": r.project,
                    "classification": r.classification,
                    "tier": r.tier,
                    "created_at": r.created_at,
                }
                for r in results
            ]
            console.print(JSON(json.dumps(data, indent=2)))
        else:
            if not results:
                console.print("[yellow]No results found[/yellow]")
                return

            table = Table(title=f"Search Results for '{query}' ({len(results)} found)")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Type", style="magenta")
            table.add_column("Title", style="green")
            table.add_column("Project", style="blue")
            table.add_column("Class", style="yellow")
            table.add_column("Tier", justify="center")
            table.add_column("Created", style="dim")

            for r in results:
                tier_color = {1: "cyan", 2: "green", 3: "bold magenta"}.get(r.tier, "white")
                table.add_row(
                    r.id[:8] + "...",
                    r.type,
                    r.title[:50],
                    r.project,
                    r.classification,
                    f"[{tier_color}]{r.tier}[/{tier_color}]",
                    r.created_at[:19].replace("T", " "),
                )
            console.print(table)

        console.print(
            f"\n[dim]Correlation IDs: {', '.join(set(r.correlation_id for r in results))}[/dim]"
        )
    finally:
        engine.close()


@app.command()
def get(
    record_id: Annotated[str, typer.Argument(help="Memory ID to retrieve")],
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Get a memory by ID."""
    engine = get_engine()
    try:
        record = engine.get(record_id)
        if not record:
            console.print(f"[red]Memory not found: {record_id}[/red]")
            raise typer.Exit(1)

        if json_output:
            console.print(
                JSON(
                    json.dumps(
                        {
                            "id": record.id,
                            "type": record.type,
                            "title": record.title,
                            "content": record.content,
                            "source": record.source,
                            "project": record.project,
                            "created_by": record.created_by,
                            "created_at": record.created_at,
                            "updated_at": record.updated_at,
                            "classification": record.classification,
                            "confidence": record.confidence,
                            "tags": record.tags,
                            "ttl_days": record.ttl_days,
                            "stale_at": record.stale_at,
                            "superseded_by": record.superseded_by,
                            "pinned": record.pinned,
                            "constitutional_block": record.constitutional_block,
                            "verified_by": record.verified_by,
                            "tier": record.tier,
                            "approved_for_external_use": record.approved_for_external_use,
                            "external_approval_token": record.external_approval_token,
                            "status": record.status,
                            "deleted_at": record.deleted_at,
                            "delete_actor": record.delete_actor,
                            "correlation_id": record.correlation_id,
                        },
                        indent=2,
                    )
                )
            )
        else:
            console.print(f"[bold]ID:[/bold] {record.id}")
            console.print(f"[bold]Type:[/bold] {record.type}")
            console.print(f"[bold]Title:[/bold] {record.title}")
            console.print(f"[bold]Content:[/bold] {record.content}")
            console.print(f"[bold]Project:[/bold] {record.project}")
            console.print(f"[bold]Classification:[/bold] {record.classification}")
            console.print(f"[bold]Tier:[/bold] {record.tier}")
            console.print(f"[bold]Status:[/bold] {record.status}")
            console.print(f"[bold]Created:[/bold] {record.created_at}")
            console.print(f"[bold]Correlation:[/bold] {record.correlation_id}")
    finally:
        engine.close()


@app.command()
def forget(
    record_id: Annotated[str, typer.Argument(help="Memory ID to soft-delete")],
    actor: Annotated[str, typer.Option("--actor", help="Actor performing deletion")] = "cli",
) -> None:
    """Soft-delete a memory (forget)."""
    engine = get_engine()
    try:
        success = engine.forget(record_id, actor)
        if success:
            console.print(f"[green]✓[/green] Forgot memory [bold]{record_id}[/bold]")
        else:
            console.print(f"[red]✗[/red] Memory not found or already deleted: {record_id}")
            raise typer.Exit(1)
    finally:
        engine.close()


@app.command()
def purge(
    record_id: Annotated[str, typer.Argument(help="Memory ID to hard-delete")],
    actor: Annotated[str, typer.Option("--actor", help="Actor performing deletion")] = "cli",
    confirm: Annotated[bool, typer.Option("--confirm", help="Confirm hard deletion")] = False,
) -> None:
    """Hard-delete a memory (purge). Requires --confirm."""
    engine = get_engine()
    try:
        success = engine.purge(record_id, actor, confirm=confirm)
        if success:
            console.print(f"[green]✓[/green] Purged memory [bold]{record_id}[/bold]")
        else:
            console.print(f"[red]✗[/red] Memory not found: {record_id}")
            raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from e
    finally:
        engine.close()


@app.command()
def restore(
    record_id: Annotated[str, typer.Argument(help="Memory ID to restore")],
    actor: Annotated[str, typer.Option("--actor", help="Actor performing restore")] = "cli",
) -> None:
    """Restore a soft-deleted (forgotten) memory."""
    engine = get_engine()
    try:
        success = engine.restore(record_id, actor)
        if success:
            console.print(f"[green]✓[/green] Restored memory [bold]{record_id}[/bold]")
        else:
            console.print(f"[red]✗[/red] Memory not found or not archived: {record_id}")
            raise typer.Exit(1)
    finally:
        engine.close()


@app.command()
def pin(
    record_id: Annotated[str, typer.Argument(help="Memory ID to pin/unpin")],
    actor: Annotated[str, typer.Option("--actor", help="Actor performing pin")] = "cli",
    unpin: Annotated[bool, typer.Option("--unpin", help="Unpin instead of pin")] = False,
) -> None:
    """Pin or unpin a memory (exempt from age pruning)."""
    engine = get_engine()
    try:
        success = engine.pin(record_id, actor, pinned=not unpin)
        if success:
            action = "unpinned" if unpin else "pinned"
            console.print(f"[green]✓[/green] {action.capitalize()} memory [bold]{record_id}[/bold]")
        else:
            console.print(f"[red]✗[/red] Memory not found: {record_id}")
            raise typer.Exit(1)
    finally:
        engine.close()


@app.command()
def verify(
    record_id: Annotated[str, typer.Argument(help="Memory ID to verify/unverify")],
    actor: Annotated[str, typer.Option("--actor", help="Actor performing verification")] = "cli",
    unverify: Annotated[bool, typer.Option("--unverify", help="Remove verification")] = False,
) -> None:
    """Mark memory as human-verified (Tier 3) or remove verification."""
    engine = get_engine()
    try:
        success = engine.verify(record_id, actor, verified=not unverify)
        if success:
            action = "unverified" if unverify else "verified"
            console.print(
                f"[green]✓[/green] Memory [bold]{record_id}[/bold] {action} (Tier {'1' if unverify else '3'})"
            )
        else:
            console.print(f"[red]✗[/red] Memory not found: {record_id}")
            raise typer.Exit(1)
    finally:
        engine.close()


@app.command()
def status(
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Show engine status and statistics."""
    engine = get_engine()
    try:
        stats = engine.status()

        if json_output:
            console.print(JSON(json.dumps(stats, indent=2)))
        else:
            console.print("[bold]LS-MEM Engine Status[/bold]")
            console.print(f"  Total memories: {stats['total']}")
            console.print(
                f"  Active: {stats['active']} | Archived: {stats['archived']} | Superseded: {stats['superseded']} | Expired: {stats['expired']} | Purged: {stats['purged']}"
            )
            console.print(f"  Pinned: {stats['pinned']}")
            console.print(f"  FTS entries: {stats['fts_count']}")
            console.print(f"  DB size: {stats['db_size_bytes']:,} bytes")
            console.print(f"  Integrity: {'✓ OK' if stats['integrity_ok'] else '✗ FAIL'}")

            console.print("\n[bold]By Type:[/bold]")
            for t, c in sorted(stats.get("by_type", {}).items()):
                console.print(f"  {t}: {c}")

            console.print("\n[bold]By Classification:[/bold]")
            for c, n in sorted(stats.get("by_classification", {}).items()):
                console.print(f"  {c}: {n}")

            console.print("\n[bold]By Tier:[/bold]")
            for t, n in sorted(stats.get("by_tier", {}).items()):
                console.print(f"  Tier {t}: {n}")
    finally:
        engine.close()


@app.command()
def lifecycle() -> None:
    """Apply lifecycle rules (mark stale/expired)."""
    engine = get_engine()
    try:
        counts = engine.apply_lifecycle()
        console.print(
            f"[green]✓[/green] Lifecycle applied: {counts['stale_archived']} stale archived, {counts['expired']} expired"
        )
    finally:
        engine.close()


@app.command()
def rebuild_fts() -> None:
    """Rebuild FTS5 index."""
    engine = get_engine()
    try:
        count = engine.rebuild_fts()
        console.print(f"[green]✓[/green] FTS5 rebuilt: {count} entries indexed")
    finally:
        engine.close()


@app.command()
def export(
    project: Annotated[
        Optional[str], typer.Option("--project", "-p", help="Filter by project")
    ] = None,
    include_restricted: Annotated[
        bool, typer.Option("--include-restricted", help="Include RESTRICTED memories")
    ] = False,
    output: Annotated[
        Optional[Path], typer.Option("--output", "-o", help="Output file (JSON Lines)")
    ] = None,
    actor: Annotated[str, typer.Option("--actor", help="Actor performing export")] = "cli",
) -> None:
    """Export memories (local file, re-scans secrets)."""
    engine = get_engine()
    try:
        records = engine.export(project=project, include_restricted=include_restricted, actor=actor)

        if output:
            with open(output, "w") as f:
                for r in records:
                    f.write(
                        json.dumps(
                            {
                                "id": r.id,
                                "type": r.type,
                                "title": r.title,
                                "content": r.content,
                                "source": r.source,
                                "project": r.project,
                                "created_by": r.created_by,
                                "created_at": r.created_at,
                                "updated_at": r.updated_at,
                                "classification": r.classification,
                                "confidence": r.confidence,
                                "tags": r.tags,
                                "ttl_days": r.ttl_days,
                                "stale_at": r.stale_at,
                                "superseded_by": r.superseded_by,
                                "pinned": r.pinned,
                                "constitutional_block": r.constitutional_block,
                                "verified_by": r.verified_by,
                                "tier": r.tier,
                                "approved_for_external_use": r.approved_for_external_use,
                                "external_approval_token": r.external_approval_token,
                                "status": r.status,
                                "deleted_at": r.deleted_at,
                                "delete_actor": r.delete_actor,
                                "correlation_id": r.correlation_id,
                            }
                        )
                        + "\n"
                    )
            console.print(
                f"[green]✓[/green] Exported {len(records)} memories to [bold]{output}[/bold]"
            )
        else:
            for r in records:
                console.print(f"{r.id}\t{r.type}\t{r.classification}\t{r.title[:60]}")
            console.print(f"\n[dim]Total: {len(records)} records[/dim]")
    finally:
        engine.close()


@app.command()
def integrity() -> None:
    """Run SQLite integrity check."""
    engine = get_engine()
    try:
        ok = engine.integrity_check()
        if ok:
            console.print("[green]✓[/green] Database integrity OK")
        else:
            console.print("[red]✗[/red] Database integrity FAILED")
            raise typer.Exit(1)
    finally:
        engine.close()


@app.command()
def audit(
    event_types: Annotated[
        Optional[str], typer.Option("--type", "-t", help="Comma-separated event types")
    ] = None,
    start: Annotated[Optional[str], typer.Option("--start", help="Start date (ISO 8601)")] = None,
    end: Annotated[Optional[str], typer.Option("--end", help="End date (ISO 8601)")] = None,
    actor: Annotated[Optional[str], typer.Option("--actor", help="Filter by actor")] = None,
    correlation_id: Annotated[
        Optional[str], typer.Option("--correlation", help="Filter by correlation ID")
    ] = None,
    limit: Annotated[int, typer.Option("--limit", "-l", help="Max results")] = 100,
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Query audit log."""
    engine = get_engine()
    if engine.auditor is None:
        console.print("[red]Audit log unavailable (audit not initialized)[/red]")
        raise typer.Exit(1)
    try:
        event_types_list = event_types.split(",") if event_types else None
        events = engine.auditor.query(
            event_types=event_types_list,
            start=start,
            end=end,
            actor=actor,
            correlation_id=correlation_id,
            limit=limit,
        )

        if json_output:
            console.print(
                JSON(
                    json.dumps(
                        [
                            {
                                "event_id": e.event_id,
                                "event_type": e.event_type,
                                "timestamp": e.timestamp,
                                "actor": e.actor,
                                "correlation_id": e.correlation_id,
                                "details": e.details,
                                "payload_hash": e.payload_hash,
                                "prev_hash": e.prev_hash,
                            }
                            for e in events
                        ],
                        indent=2,
                    )
                )
            )
        else:
            if not events:
                console.print("[yellow]No audit events found[/yellow]")
                return

            table = Table(title=f"Audit Log ({len(events)} events)")
            table.add_column("Event ID", style="cyan", no_wrap=True)
            table.add_column("Type", style="magenta")
            table.add_column("Timestamp", style="dim")
            table.add_column("Actor", style="blue")
            table.add_column("Correlation", style="green")

            for e in events:
                table.add_row(
                    e.event_id[:8] + "...",
                    e.event_type,
                    e.timestamp[:19].replace("T", " "),
                    e.actor,
                    e.correlation_id[:8] + "...",
                )
            console.print(table)
    finally:
        engine.close()


@app.command()
def permission(
    action: Annotated[str, typer.Argument(help="Action: list, approve, deny")],
    approval_token: Annotated[Optional[str], typer.Option("--token", help="Approval token")] = None,
    approved_by: Annotated[str, typer.Option("--by", help="Approver identity")] = "human",
    approved: Annotated[bool, typer.Option("--approve/--deny", help="Approve or deny")] = True,
) -> None:
    """Request/approve external access via permission gateway."""
    engine = get_engine()
    try:
        if action == "list":
            pending = engine.gateway.get_pending_approvals()
            if not pending:
                console.print("[yellow]No pending approvals[/yellow]")
                return

            table = Table(title="Pending Approvals")
            table.add_column("Token", style="cyan", no_wrap=True)
            table.add_column("Agent", style="magenta")
            table.add_column("Provider", style="blue")
            table.add_column("Operation", style="green")
            table.add_column("Destination", style="yellow")
            table.add_column("Classification", style="red")

            for p in pending:
                table.add_row(
                    p["approval_token"][:8] + "...",
                    p["agent_id"],
                    p["provider"],
                    p["operation"],
                    p["destination"],
                    p["classification"],
                )
            console.print(table)

        elif action in ("approve", "deny"):
            if not approval_token:
                console.print("[red]✗[/red] --token required for approve/deny")
                raise typer.Exit(1)

            decision = engine.gateway.submit_human_approval(
                approval_token=approval_token,
                approved_by=approved_by,
                approved=(action == "approve"),
            )

            if decision.allowed:
                console.print(f"[green]✓[/green] Approved (token: {approval_token[:8]}...)")
            else:
                console.print(f"[red]✗[/red] Denied: {decision.reason}")
        else:
            console.print(f"[red]✗[/red] Unknown action: {action}")
            raise typer.Exit(1)
    finally:
        engine.close()


if __name__ == "__main__":
    app()
