"""Storage sub-commands — SQLite-first core (ADR-011).

SQLite is the canonical operational store; ``.opencode/*`` JSON remains the
human-readable interchange. The ``import-opencode`` command offers the opt-in,
non-destructive mirror of legacy JSON data into SQLite.
"""

from __future__ import annotations

from pathlib import Path

import typer

from ai_company.paths import get_data_root

app = typer.Typer(
    help="Storage operations — SQLite-first core, opt-in mirroring",
    no_args_is_help=True,
)


@app.command("import-opencode")
def import_opencode(
    data_root: str = typer.Option(
        "",
        help="Data root override (default: resolved project root)",
    ),
    database: str = typer.Option(
        "",
        help="SQLite DB path (default: <data root>/data/ai_company.db)",
    ),
) -> None:
    """Mirror legacy ``.opencode/*`` JSON data into SQLite (non-destructive).

    Imports ``.opencode/inbox.json`` tasks and ``.opencode/audit.jsonl``
    audit events into the SQLite store (idempotent ``INSERT OR REPLACE``).
    Source files are never modified or deleted — they remain the
    human-readable interchange. See ADR-011.
    """
    from ai_company.data.audit_store import AuditStore
    from ai_company.data.database import Database
    from ai_company.data.task_store import TaskStore

    root = Path(data_root) if data_root else get_data_root()
    db_path = Path(database) if database else root / "data" / "ai_company.db"
    db = Database(db_path=db_path)
    db.init_schema()

    tasks = TaskStore(db).import_json(root / ".opencode" / "inbox.json")
    events = AuditStore(db).import_jsonl(root / ".opencode" / "audit.jsonl")

    typer.echo(f"Imported {tasks} task(s) and {events} audit event(s) into {db_path}")
    typer.echo(f"Source {root / '.opencode'} left unchanged")
