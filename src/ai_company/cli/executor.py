"""CLI commands for the autonomous executor.

Includes GAP-017 dead-letter queue commands and daemon mode (S3-06).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(help="Autonomous task execution loop")


@app.command()
def start(
    poll_interval: float = typer.Option(5.0, help="Seconds between polling cycles"),
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
    daemon: bool = typer.Option(False, "--daemon", "-d", help="Run as background daemon"),
    pid_dir: str = typer.Option("logs", help="Directory for PID file (daemon mode)"),
    log_dir: str = typer.Option("logs", help="Directory for log file (daemon mode)"),
    kpi_snapshot_interval: float = typer.Option(
        300.0,
        "--kpi-snapshot-interval",
        help="Seconds between periodic KPI snapshot collections (daemon mode; 0 disables)",
    ),
    governance_interval: float = typer.Option(
        86400.0,
        "--governance-interval",
        help="Seconds between periodic retention enforcement (daemon mode; 0 disables)",
    ),
    db_path: Optional[str] = typer.Option(
        None,
        help="SQLite database path for write-through (default: <data root>/data/ai_company.db)",
    ),
    daily_budget_usd: Optional[float] = typer.Option(
        None,
        "--daily-budget-usd",
        help="Override daily LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    task_budget_usd: Optional[float] = typer.Option(
        None,
        "--task-budget-usd",
        help="Override per-task LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    auto_suspend: bool = typer.Option(
        False,
        "--auto-suspend/--no-auto-suspend",
        help="Stop processing tasks when the daily budget is exhausted.",
    ),
    guardrails_config: str = typer.Option(
        "config/company/guardrails.yaml",
        "--guardrails-config",
        help="Path to operating-guardrails config (default: config/company/guardrails.yaml).",
    ),
) -> None:
    """Start the continuous execution loop.

    With --daemon/-d, runs in the background with PID file management,
    signal handling, and file logging.
    """
    daily_cap, task_cap, do_suspend = _resolve_budgets(
        daily_budget_usd, task_budget_usd, auto_suspend, guardrails_config
    )
    if daemon:
        _start_daemon(
            poll_interval=poll_interval,
            config=config,
            registry=registry,
            pid_dir=pid_dir,
            log_dir=log_dir,
            kpi_snapshot_interval=kpi_snapshot_interval,
            governance_interval=governance_interval,
            db_path=db_path,
            daily_budget_usd=daily_cap,
            task_budget_usd=task_cap,
            auto_suspend=do_suspend,
        )
    else:
        from ai_company.executor.daemon import resolve_database
        from ai_company.executor.loop import Executor

        executor = Executor(
            poll_interval=poll_interval,
            config_path=config,
            registry_path=registry,
            database=resolve_database(db_path),
            daily_budget_usd=daily_cap,
            task_budget_usd=task_cap,
            auto_suspend_on_overspend=do_suspend,
        )
        executor.start()


def _resolve_budgets(
    daily_override: float | None,
    task_override: float | None,
    suspend_override: bool,
    guardrails_config: str,
) -> tuple[float | None, float | None, bool]:
    """Resolve LLM budget caps + auto-suspend flag.

    CLI flags take precedence; otherwise values are read from
    ``config/company/guardrails.yaml``.  When that file is absent or lacks a
    value, the cap stays ``None`` (unlimited) for backward compatibility.
    """
    daily = daily_override
    task = task_override
    suspend = suspend_override

    if daily is None or task is None or not suspend:
        try:
            from ai_company.paths import get_data_root

            cfg_path = Path(guardrails_config)
            if not cfg_path.is_absolute():
                cfg_path = get_data_root() / cfg_path
            import yaml

            with open(cfg_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            budgets = data.get("guardrails", {}).get("llm_budgets", {})
            if isinstance(budgets, dict):
                if daily is None:
                    daily = budgets.get("daily_budget_usd")
                if task is None:
                    task = budgets.get("task_budget_usd")
                if not suspend:
                    suspend = bool(budgets.get("auto_suspend_on_overspend"))
        except (FileNotFoundError, OSError):
            pass

    return daily, task, suspend


def _start_daemon(
    *,
    poll_interval: float,
    config: str,
    registry: str,
    pid_dir: str,
    log_dir: str,
    kpi_snapshot_interval: float,
    governance_interval: float,
    db_path: str | None,
    daily_budget_usd: float | None = None,
    task_budget_usd: float | None = None,
    auto_suspend: bool = False,
) -> None:
    """Launch executor in daemon mode as a detached subprocess (GitHub #56).

    The parent spawns ``python -m ai_company.executor.daemon`` in a fresh
    interpreter with ``DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`` on
    Windows (new session on POSIX) and returns as soon as the child has
    written its PID file — so the daemon survives the shell that launched
    it, and ``executor stop`` / ``executor status`` can find it.
    """
    from ai_company.executor.daemon import launch_detached_daemon

    pid_path = Path(pid_dir) / "executor-daemon.pid"

    try:
        pid = launch_detached_daemon(
            poll_interval=poll_interval,
            config=config,
            registry=registry,
            pid_dir=pid_dir,
            log_dir=log_dir,
            kpi_snapshot_interval=kpi_snapshot_interval,
            governance_interval=governance_interval,
            db_path=db_path,
            daily_budget_usd=daily_budget_usd,
            task_budget_usd=task_budget_usd,
            auto_suspend=auto_suspend,
        )
    except RuntimeError as exc:
        typer.echo(f"Daemon error: {exc}", err=True)
        raise typer.Exit(1) from None

    typer.echo(f"Started executor daemon (PID {pid}, PID file: {pid_path})")


@app.command()
def tick(
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
    db_path: Optional[str] = typer.Option(
        None,
        help="SQLite database path for write-through (default: <data root>/data/ai_company.db)",
    ),
    daily_budget_usd: Optional[float] = typer.Option(
        None,
        help="Override daily LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    task_budget_usd: Optional[float] = typer.Option(
        None,
        help="Override per-task LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    auto_suspend: bool = typer.Option(
        False,
        help="Stop processing tasks when the daily budget is exhausted.",
    ),
    guardrails_config: str = typer.Option(
        "config/company/guardrails.yaml",
        help="Path to operating-guardrails config (default: config/company/guardrails.yaml).",
    ),
) -> None:
    """Process all pending tasks in a single pass."""
    daily_cap, task_cap, do_suspend = _resolve_budgets(
        daily_budget_usd, task_budget_usd, auto_suspend, guardrails_config
    )
    from ai_company.executor.daemon import resolve_database
    from ai_company.executor.loop import Executor

    executor = Executor(
        config_path=config,
        registry_path=registry,
        database=resolve_database(db_path),
        daily_budget_usd=daily_cap,
        task_budget_usd=task_cap,
        auto_suspend_on_overspend=do_suspend,
    )
    count = executor.tick()
    typer.echo(f"Processed {count} task(s).")
    typer.echo(f"Stats: {json.dumps(executor.stats.to_dict(), indent=2)}")


@app.command()
def run_task(
    task_id: str = typer.Argument(..., help="Task ID to execute"),
    config: str = typer.Option("company/models.yaml", help="Path to models config"),
    registry: str = typer.Option("company/agent-registry.json", help="Path to agent registry"),
    db_path: Optional[str] = typer.Option(
        None,
        help="SQLite database path for write-through (default: <data root>/data/ai_company.db)",
    ),
    daily_budget_usd: Optional[float] = typer.Option(
        None,
        help="Override daily LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    task_budget_usd: Optional[float] = typer.Option(
        None,
        help="Override per-task LLM spend cap (USD). Defaults to config/company/guardrails.yaml.",
    ),
    auto_suspend: bool = typer.Option(
        False,
        help="Stop processing tasks when the daily budget is exhausted.",
    ),
    guardrails_config: str = typer.Option(
        "config/company/guardrails.yaml",
        help="Path to operating-guardrails config (default: config/company/guardrails.yaml).",
    ),
) -> None:
    """Execute a single task by ID."""
    daily_cap, task_cap, do_suspend = _resolve_budgets(
        daily_budget_usd, task_budget_usd, auto_suspend, guardrails_config
    )
    from ai_company.executor.daemon import resolve_database
    from ai_company.executor.loop import Executor
    from ai_company.models.task import Task

    executor = Executor(
        config_path=config,
        registry_path=registry,
        database=resolve_database(db_path),
        daily_budget_usd=daily_cap,
        task_budget_usd=task_cap,
        auto_suspend_on_overspend=do_suspend,
    )

    # Load the specific task
    inbox_path = Path(executor.bus.storage_path)
    if not inbox_path.exists():
        typer.echo("No inbox found.")
        raise typer.Exit(1)

    tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
    task_data = next((t for t in tasks if t.get("id") == task_id), None)

    if not task_data:
        typer.echo(f"Task '{task_id}' not found.")
        raise typer.Exit(1)

    task = Task(**task_data)
    typer.echo(f"Executing task: {task.instruction[:80]}...")
    executor._process_task(task)
    typer.echo(f"Done. Stats: {json.dumps(executor.stats.to_dict(), indent=2)}")


@app.command()
def cycle(
    interval: float = typer.Option(60.0, help="Seconds between scheduling cycles"),
    max_cycles: Optional[int] = typer.Option(
        None, help="Stop after N cycles (default: run until interrupted)"
    ),
    config: str = typer.Option("orchestrator/scheduler.yaml", help="Path to scheduler config"),
) -> None:
    """Run the scheduled-cycle daemon (continuous scheduling loop)."""
    from ai_company.orchestrator.message_bus import MessageBus
    from ai_company.orchestrator.scheduler import Scheduler

    scheduler = Scheduler(config_path=config)
    bus = MessageBus()

    typer.echo(
        f"Starting scheduled-cycle daemon (interval={interval}s, "
        f"max_cycles={max_cycles if max_cycles is not None else 'unbounded'})."
    )
    typer.echo("Press Ctrl+C to stop.")

    cycles = scheduler.run_forever(bus, interval_seconds=interval, max_cycles=max_cycles)
    typer.echo(f"Daemon stopped after {cycles} cycle(s).")


@app.command()
def status(
    log_dir: str = typer.Option("logs", help="Directory for daemon status file"),
) -> None:
    """Show executor status and pending tasks."""
    from ai_company.executor.daemon import ExecutorDaemon

    # Check daemon status first
    daemon_status = ExecutorDaemon.get_daemon_status(Path(log_dir) / "executor-daemon.json")
    if daemon_status:
        pid = daemon_status.get("pid")
        state = daemon_status.get("state", "unknown")
        started = daemon_status.get("started_at", "unknown")
        ticks = daemon_status.get("ticks_completed", 0)
        uptime = daemon_status.get("uptime_seconds", 0)
        # A status file that claims "running" for a dead PID is stale —
        # report it honestly so nobody trusts a phantom daemon (GitHub #56).
        if state == "running" and isinstance(pid, int) and not ExecutorDaemon.is_pid_alive(pid):
            state = "not running (stale)"
        typer.echo("Executor Daemon Status")
        typer.echo("=" * 40)
        typer.echo(f"  State: {state}")
        typer.echo(f"  PID: {pid}")
        typer.echo(f"  Started: {started}")
        typer.echo(f"  Ticks completed: {ticks}")
        typer.echo(f"  Uptime: {uptime:.1f}s")
        typer.echo()

    from ai_company.orchestrator.message_bus import MessageBus

    bus = MessageBus()
    inbox_path = Path(bus.storage_path)

    if not inbox_path.exists():
        typer.echo("No inbox found.")
        return

    tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
    status_counts: dict[str, int] = {}
    for t in tasks:
        s = t.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    typer.echo("Task Queue Status")
    typer.echo("=" * 40)
    typer.echo(f"Total tasks: {len(tasks)}")
    for status, count in sorted(status_counts.items()):
        typer.echo(f"  {status}: {count}")

    # Show pending tasks
    pending = [t for t in tasks if t.get("status") == "pending"]
    if pending:
        typer.echo(f"\nPending tasks ({len(pending)}):")
        for t in pending[:10]:
            typer.echo(
                f"  [{t.get('id', '?')[:8]}] -> {t.get('receiver_id', '?')}: {t.get('instruction', '?')[:60]}"
            )


@app.command()
def stop(
    pid_dir: str = typer.Option("logs", help="Directory for PID file (daemon mode)"),
    log_dir: str = typer.Option("logs", help="Directory for status file (daemon mode)"),
) -> None:
    """Stop the executor daemon (graceful shutdown)."""
    from pathlib import Path

    from ai_company.executor.daemon import ExecutorDaemon

    typer.echo("Stopping executor daemon...")
    daemon = ExecutorDaemon(
        executor_factory=lambda: None,
        pid_path=Path(pid_dir) / "executor-daemon.pid",
        log_path=Path(log_dir) / "executor-daemon.log",
        status_path=Path(log_dir) / "executor-daemon.json",
    )
    success = daemon.stop_daemon()
    if success:
        typer.echo("Daemon stop signal sent successfully.")
    else:
        typer.echo("No running daemon found (or already stopped).")
        raise typer.Exit(1)


# ── Dead Letter Queue commands (GAP-017) ─────────────────────────────


@app.command()
def dlq_list() -> None:
    """List all tasks in the dead-letter queue."""
    from ai_company.executor.dead_letter import DeadLetterQueue

    dlq = DeadLetterQueue()
    entries = dlq.list_entries()

    if not entries:
        typer.echo("Dead-letter queue is empty.")
        return

    typer.echo(f"Dead-Letter Queue ({len(entries)} tasks)")
    typer.echo("=" * 60)
    for entry in entries:
        task = entry.get("task", {})
        tid = task.get("id", "?")[:8]
        receiver = task.get("receiver_id", "?")
        instruction = task.get("instruction", "?")[:50]
        reason = entry.get("reason", "?")[:40]
        moved_at = entry.get("moved_at", "?")[:19]
        typer.echo(f"  [{tid}] -> {receiver}: {instruction}")
        typer.echo(f"    reason: {reason}  (moved: {moved_at})")


@app.command()
def dlq_retry(
    task_id: str = typer.Argument(..., help="Task ID to retry (full or prefix)"),
) -> None:
    """Move a task from the DLQ back into the inbox for re-execution."""
    from ai_company.executor.dead_letter import DeadLetterQueue, retry_dlq_task
    from ai_company.orchestrator.message_bus import MessageBus

    dlq = DeadLetterQueue()
    entries = dlq.list_entries()

    # Support prefix matching
    matched_id: str | None = None
    for entry in entries:
        tid = entry.get("task", {}).get("id", "")
        if tid == task_id or tid.startswith(task_id):
            matched_id = tid
            break

    if matched_id is None:
        typer.echo(f"No DLQ entry found matching '{task_id}'.")
        raise typer.Exit(1)

    restored = retry_dlq_task(MessageBus(), dlq, matched_id)
    if restored is None:
        typer.echo("Failed to restore task.")
        raise typer.Exit(1)

    typer.echo(f"Task {matched_id[:8]} restored to inbox as pending.")


@app.command()
def dlq_clear() -> None:
    """Clear all entries from the dead-letter queue."""
    from ai_company.executor.dead_letter import DeadLetterQueue

    dlq = DeadLetterQueue()
    count = dlq.clear()
    typer.echo(f"Cleared {count} entry(ies) from the dead-letter queue.")
