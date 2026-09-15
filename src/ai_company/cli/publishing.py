"""Publishing rails commands — queue, list, and publish Pharos artifacts."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from ai_company.publishing.formats import format_linkedin, format_substack
from ai_company.publishing.publishers import LinkedInPublisher, SubstackPublisher
from ai_company.publishing.queue import PublishQueue

app = typer.Typer(help="Publishing rails — LinkedIn / Substack publish queue")
console = Console()

_PUBLISHERS = {
    "linkedin": LinkedInPublisher(),
    "substack": SubstackPublisher(),
}


@app.command("enqueue")
def enqueue(
    platform: str = typer.Option(..., help="Platform: linkedin | substack"),
    title: str = typer.Option(..., help="Artifact title"),
    body: str = typer.Option(..., help="Artifact body (platform body or markdown)"),
    external_url: str = typer.Option("", help="Optional external URL to attach"),
    mirror_bus: bool = typer.Option(
        False,
        "--mirror-bus",
        help="Mirror the record to the agent task store (pharos-publish task)",
    ),
) -> None:
    """Add a platform-ready artifact to the publish queue.

    Args:
        platform: Platform (linkedin | substack).
        title: Artifact title.
        body: Artifact body.
        external_url: Optional external URL to attach.
        mirror_bus: Mirror to the agent task store.
    """
    from ai_company.orchestrator.message_bus import MessageBus

    queue = PublishQueue()
    bus = MessageBus() if mirror_bus else None
    record = queue.enqueue(
        platform,
        title,
        body,
        bus=bus,
        external_url=external_url,
    )
    console.print(f"[green]Enqueued[/green] {record.id}: '{record.title}' → {platform}")


@app.command("list")
def list_queue(
    status: str = typer.Option("all", help="Filter by status: queued | posted | failed | all"),
) -> None:
    """List publish queue records.

    Args:
        status: Filter by status.
    """
    queue = PublishQueue()
    records = queue.list(status=None if status == "all" else status)
    if not records:
        console.print("No publish records.")
        return

    table = Table(title=f"Publish Queue ({len(records)} records)")
    table.add_column("ID", style="cyan")
    table.add_column("Status")
    table.add_column("Platform")
    table.add_column("Title")
    table.add_column("Created (UTC)")
    for r in records:
        table.add_row(r.id, r.status, r.platform, r.title, r.created_at)
    console.print(table)


@app.command("show")
def show(record_id: str = typer.Argument(..., help="Publish record id")) -> None:
    """Preview a queued artifact as its platform would see it.

    Args:
        record_id: Publish record id.
    """
    queue = PublishQueue()
    record = queue.get(record_id)
    if record is None:
        console.print(f"[red]Unknown record:[/red] {record_id}")
        raise typer.Exit(1)

    console.print(f"[bold]{record.title}[/bold]  ({record.platform}, {record.status})")
    console.print("─" * 40)
    if record.platform == "linkedin":
        formatted = format_linkedin(record.title, record.body)
        console.print(formatted["text"])
        console.print(
            f"\n[dim]{formatted['char_count']} chars, "
            f"{formatted['word_count']} words (truncated={formatted['truncated']})[/dim]"
        )
    elif record.platform == "substack":
        formatted = format_substack(record.title, record.body)
        console.print(formatted["markdown"])
        console.print(
            f"\n[dim]{formatted['word_count']} words (truncated={formatted['truncated']})[/dim]"
        )


@app.command("publish")
def publish(
    record_id: str = typer.Argument(..., help="Publish record id"),
    live: bool = typer.Option(
        False,
        "--live",
        "-L",
        help=(
            "Force a live POST even when no platform credentials are configured. "
            "Primarily for explicit opt-in operators/tests."
        ),
    ),
) -> None:
    """Publish a queued artifact to its platform.

    Dry-run by default: without platform credentials the adapter returns a
    receipt instead of POSTing.  Pass ``--live`` to force a real request
    (only meaningful when ``PHAROS_*_API_URL`` / ``PHAROS_*_TOKEN`` are set).

    Args:
        record_id: Publish record id.
        live: Force a live POST.
    """
    queue = PublishQueue()
    record = queue.get(record_id)
    if record is None:
        console.print(f"[red]Unknown record:[/red] {record_id}")
        raise typer.Exit(1)

    publisher = _PUBLISHERS.get(record.platform)
    if publisher is None:
        console.print(f"[red]No publisher for platform:[/red] {record.platform}")
        raise typer.Exit(1)

    result = publisher.publish(record, force_live=live)
    if result.status == "posted":
        queue.mark_posted(record_id, external_url=result.url)
        console.print(f"[green]Posted[/green] {record_id} → {result.url or record.platform}")
    elif result.status == "failed":
        queue.mark_failed(record_id, notes=result.error)
        console.print(f"[red]Failed[/red] {record_id}: {result.error}")
        raise typer.Exit(1)
    else:  # dry_run
        console.print(
            f"[yellow]Dry run: no credentials for {record.platform}.[/yellow] "
            f"Set PHAROS_{record.platform.upper()}_API_URL / "
            f"PHAROS_{record.platform.upper()}_TOKEN to enable live posting."
        )


__all__ = ["app"]
