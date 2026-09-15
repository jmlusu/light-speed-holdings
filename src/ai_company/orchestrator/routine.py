"""Pharos routine engine — recurring content routines fired by the daemon.

Implementation of the P0 slice of ADR-020 (docs/adr/020-pharos-content-intelligence.md):
a ``routine:`` scheduler inside the existing executor daemon loop.  Each due
routine enqueues a **fresh** MessageBus Task with a deterministic
``routine_run_id`` (``"{id}-{UTC date}"``) so re-drives are idempotent and the
content loop is observable in the task store.

Design mirrors ``orchestrator/scheduler.py`` (persistent FileStore-backed YAML,
crash-safe mark-before-send) and ``dashboard/kpis/scheduler.py`` (time-gated
``run_due`` used by the daemon loop).

Routine definitions live in ``config/company/routines.yaml``; prompts live
under ``templates/pharos/routines/``.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field

from ai_company.paths import get_project_root
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

DEFAULT_ROUTINES_YAML = "config/company/routines.yaml"
DEFAULT_PROMPT_DIR = "templates/pharos/routines"
DEFAULT_ROUTINE_INTERVAL_SECONDS = 900.0
DEFAULT_RECEIVER_ID = "content_writer"

_UTC = timezone.utc


def _clock_now() -> datetime:
    """UTC-aware ``datetime.now`` helper (injectable in tests via patching)."""
    return datetime.now(_UTC)


class Routine(BaseModel):
    """A single recurring content routine.

    Two schedule modes (mutually exclusive):

    - ``schedule_day`` (ISO weekday, 1=Mon..7=Sun) + ``time_utc`` (HH:MM):
      fires weekly on that day/time in UTC.
    - ``interval_minutes``: fires on a fixed interval from the last run.

    ``next_run`` is persisted in the routines YAML by :class:`RoutineStore` so
    firings survive daemon restarts.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., min_length=1)
    name: str = ""
    receiver_id: str = DEFAULT_RECEIVER_ID
    enabled: bool = True
    schedule_day: int | None = None
    time_utc: str = "04:00"
    interval_minutes: int | None = None
    prompt_file: str = ""
    model: str = ""
    budget_tokens: int | None = None
    outputs: list[str] = Field(default_factory=list)
    research_depth: str = "standard"
    last_run: str = ""
    next_run: str = ""

    @property
    def is_deep_research(self) -> bool:
        """True when this routine requests the deep-research working mode.

        ``research_depth != "standard"`` (e.g. ``"deep"``) flags the fire for
        corroboration-heavy drafting (knowledge graph, memory recall, Pharos
        reference corpus) instead of a single-pass brief.
        """
        return self.research_depth not in ("", "standard")

    def is_daily(self) -> bool:
        """True when this routine fires on a weekly day/time (not interval)."""
        return self.schedule_day is not None and self.interval_minutes is None


def _parse_time_utc(value: str) -> tuple[int, int]:
    """Parse an ``HH:MM`` UTC clock time; defaults to midnight on bad input."""
    try:
        hour, minute = (int(part) for part in value.split(":", 1))
        return hour, minute
    except (ValueError, TypeError):
        logger.warning("Invalid time_utc %r — defaulting to 00:00 UTC", value)
        return 0, 0


def compute_next_run(routine: Routine, after: datetime) -> datetime:
    """Return the next UTC fire time for *routine* strictly after *after*.

    Interval routines advance by ``interval_minutes``; daily routines advance
    to the next matching ISO weekday at ``time_utc`` (skipping today when
    today's slot already passed).
    """
    if routine.interval_minutes and routine.interval_minutes > 0:
        return after + timedelta(minutes=routine.interval_minutes)

    hour, minute = _parse_time_utc(routine.time_utc)
    day = routine.schedule_day
    if day is None:
        logger.warning(
            "Routine %s has neither schedule_day nor interval_minutes — "
            "defaulting to weekly Monday 04:00 UTC",
            routine.id,
        )
        day = 1
    base = after.replace(hour=hour, minute=minute, second=0, microsecond=0)
    candidate = base
    if candidate <= after:
        candidate = base + timedelta(days=1)
    # ISO weekday: Monday=1 .. Sunday=7
    days_ahead = (day - candidate.isoweekday()) % 7
    if days_ahead == 0 and candidate <= after:
        days_ahead = 7
    return candidate + timedelta(days=days_ahead)


def build_routine_task(
    routine: Routine,
    fire_time: datetime,
    instruction: str,
) -> Any:
    """Build a fresh MessageBus ``Task`` for a routine fire.

    The task carries deterministic IDs: ``routine-{id}-{yyyy-mm-dd}`` (daily)
    or ``routine-{id}-{yyyy-mm-dd-hhmm}`` (interval), plus provenance tags
    ``routine:<id>`` and ``routine_run:<routine_run_id>`` so the content loop
    is idempotent and filterable in the task store / KPI collectors.

    ``instruction`` may embed ``{date}`` / ``{routine_id}`` tokens, which are
    substituted here.  Prompt files render those tokens; callers may also pass
    a literal instruction with no tokens.
    """
    from ai_company.models.task import Task, TaskPriority

    stamp = fire_time.strftime("%Y-%m-%d")
    if routine.interval_minutes and routine.interval_minutes > 0:
        task_suffix = fire_time.strftime("%Y-%m-%d-%H%M")
    else:
        task_suffix = stamp
    routine_run_id = f"{routine.id}-{stamp}"

    rendered = instruction
    for token, value in (
        ("{date}", stamp),
        ("{receiver_id}", routine.receiver_id),
        ("{routine_id}", routine.id),
        ("{routine_name}", routine.name),
        ("{routine_run_id}", routine_run_id),
        ("{research_depth}", routine.research_depth),
    ):
        rendered = rendered.replace(token, value)

    tags = [
        "pharos-routine",
        f"routine:{routine.id}",
        f"routine_run:{routine_run_id}",
    ]
    if routine.is_deep_research:
        tags.append("research:deep")

    return Task(
        id=f"routine-{routine.id}-{task_suffix}",
        name=routine.name,
        sender_id="routine-scheduler",
        receiver_id=routine.receiver_id,
        instruction=rendered,
        priority=TaskPriority.MEDIUM,
        tags=tags,
    )


class RoutineStore:
    """Persistent store of routine definitions + firing state (YAML-backed).

    Mirrors ``orchestrator/scheduler.py``'s FileStore usage: definitions are
    loaded from ``config/company/routines.yaml`` and ``last_run``/``next_run``
    are persisted back into the same file so crash recovery never double-fires.
    """

    def __init__(
        self,
        config_path: str | Path | None = None,
        project_root: Path | None = None,
        registry_path: str | Path | None = None,
    ) -> None:
        self.root: Path = project_root or get_project_root()
        if config_path is None:
            config_path = self.root / DEFAULT_ROUTINES_YAML
        self.config_path: Path = Path(config_path)
        self._store = FileStore(self.config_path.parent, backup=True)
        self._config_name = self.config_path.name
        self._registry_path: Path | None = (
            Path(registry_path) if registry_path is not None else None
        )
        self.routines: list[Routine] = []
        self._load()

    def _load(self) -> None:
        """Load routine definitions; seed default ``next_run`` when absent."""
        data = self._store.read_yaml(self._config_name)
        raw_routines = data.get("routines", []) if isinstance(data, dict) else []
        now = datetime.now(_UTC)
        self.routines = []
        for raw in raw_routines:
            try:
                routine = Routine(**raw)
            except Exception:  # noqa: BLE001 - a bad entry must not break the store
                logger.warning("Skipping invalid routine entry: %r", raw)
                continue
            if routine.schedule_day is None and routine.interval_minutes is None:
                routine.schedule_day = 1
                routine.time_utc = "04:00"
            if not routine.next_run:
                routine.next_run = compute_next_run(routine, now).isoformat()
            self.routines.append(routine)
        # Seed a default routine so the content loop works out of the box
        # when no routines.yaml has been configured yet.
        if not self.routines:
            default = Routine(
                id="pharos_default_brief",
                name="Pharos Default Brief",
                receiver_id="content_writer",
                schedule_day=1,
                time_utc="04:00",
                enabled=True,
                prompt_file="templates/pharos/routines/monday-agentic-enterprise-brief.md",
                model="standard",
                budget_tokens=4000,
            )
            default.next_run = compute_next_run(default, now).isoformat()
            self.routines.append(default)

    def _save(self) -> None:
        data = {"routines": [r.model_dump() for r in self.routines]}
        self._store.write_yaml(self._config_name, data)

    def get_due(self, now: datetime) -> list[Routine]:
        """Return enabled routines whose ``next_run`` has elapsed."""
        due: list[Routine] = []
        for r in self.routines:
            if not r.enabled or not r.next_run:
                continue
            try:
                next_fire = datetime.fromisoformat(r.next_run)
            except ValueError:
                logger.warning("Invalid next_run %r for routine %s", r.next_run, r.id)
                continue
            if next_fire.tzinfo is None:
                next_fire = next_fire.replace(tzinfo=_UTC)
            if next_fire <= now:
                due.append(r)
        return due

    def mark_run(self, routine_id: str, fired_at: datetime) -> None:
        """Record a fire and advance ``next_run``; persisted immediately.

        Called BEFORE the task is enqueued (crash-safe ordering: a crash after
        enqueue can only delay the next run, never duplicate work).
        """
        for routine in self.routines:
            if routine.id == routine_id:
                routine.last_run = fired_at.isoformat()
                routine.next_run = compute_next_run(routine, fired_at).isoformat()
        self._save()

    def get(self, routine_id: str) -> Routine | None:
        return next((r for r in self.routines if r.id == routine_id), None)

    def list_routines(self) -> list[Routine]:
        return self.routines

    def is_known_receiver(self, receiver_id: str) -> bool:
        """True when *receiver_id* is a registered agent id.

        Reads ``company-registry.yaml`` (same source the generator uses).
        When the registry is missing/unreadable we log and accept (P0
        tolerance), so a broken registry never blocks the content loop.
        """
        registry = self._registry_path or self.root / "company-registry.yaml"
        if not registry.exists():
            logger.warning(
                "Registry %s missing — cannot validate receiver %r (accepted)",
                registry,
                receiver_id,
            )
            return True
        try:
            from ai_company.registry.loader import load_yaml_cached

            data = load_yaml_cached(registry)
        except Exception:  # noqa: BLE001 - validation is best-effort
            logger.warning("Failed to read registry %s — receiver %r accepted", registry, receiver_id)
            return True
        agents = data.get("agents", []) if isinstance(data, dict) else []
        known = {a.get("id") for a in agents if isinstance(a, dict)}
        return receiver_id in known

    def read_prompt(self, routine: Routine) -> str:
        """Return the routine's instruction text for its fire.

        Reads ``templates/pharos/routines/<prompt_file>`` when present;
        otherwise falls back to a one-line default instruction.  Never raises.
        """
        rel = routine.prompt_file.strip("/")
        path = self.root / rel
        if rel and path.exists():
            try:
                return path.read_text(encoding="utf-8")
            except OSError as exc:
                logger.warning("Failed to read prompt %s: %s", path, exc)
        else:
            logger.warning(
                "Prompt file %s missing for routine %s — using default instruction",
                path,
                routine.id,
            )
        return (
            f"Run routine '{routine.name or routine.id}' for {routine.receiver_id}. "
            f"Today (UTC): {{date}}."
        )


class RoutineScheduler:
    """Time-gated wrapper around routine firing for the daemon loop.

    Mirrors ``KPISnapshotScheduler``: ``run_due`` checks the interval gate,
    then fires every due routine (best-effort, never raises).  ``interval_seconds
    <= 0`` disables routine collection entirely.
    """

    def __init__(
        self,
        interval_seconds: float = DEFAULT_ROUTINE_INTERVAL_SECONDS,
        bus: Any | None = None,
        store: RoutineStore | None = None,
        *,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self.interval_seconds = interval_seconds
        self._bus = bus
        self._store = store or RoutineStore()
        self._clock = clock or time.time
        self._last_run: float = 0.0

    @property
    def store(self) -> RoutineStore:
        return self._store

    def run_due(self, now: float | None = None) -> int:
        """Fire all due routines; return the number of tasks enqueued.

        ``0`` means nothing fired (too soon, disabled, or no due routines).
        Never raises: per-routine failures are logged and skipped.
        """
        if self.interval_seconds <= 0:
            return 0
        current = now if now is not None else self._clock()
        if current - self._last_run < self.interval_seconds:
            return 0
        self._last_run = current

        if self._bus is None:
            logger.warning("Routine scheduler has no message bus — nothing fired")
            return 0

        # fire_time used for both due-check and scheduling bookkeeping.
        fire_time = datetime.fromtimestamp(current, tz=_UTC)
        due = self.store.get_due(fire_time)
        fired = 0
        for routine in due:
            if not self.store.is_known_receiver(routine.receiver_id):
                logger.warning(
                    "Skipping routine %s: receiver %r is not a registered agent",
                    routine.id,
                    routine.receiver_id,
                )
                continue
            instruction = self.store.read_prompt(routine)
            try:
                task = build_routine_task(routine, fire_time, instruction)
                # Crash-safe ordering: persist the schedule advance BEFORE the
                # enqueue (see RoutineStore.mark_run docstring).
                self.store.mark_run(routine.id, fire_time)
                self._bus.send_task(task)
                fired += 1
                logger.info(
                    "Fired routine %s -> task %s (receiver=%s)",
                    routine.id,
                    task.id,
                    routine.receiver_id,
                )
            except Exception:  # noqa: BLE001 - firing is best-effort
                logger.exception("Failed to fire routine %s", routine.id)
        return fired

    def reset(self) -> None:
        """Force the next ``run_due`` call to check routines."""
        self._last_run = 0.0


__all__ = [
    "DEFAULT_PROMPT_DIR",
    "DEFAULT_RECEIVER_ID",
    "DEFAULT_ROUTINE_INTERVAL_SECONDS",
    "DEFAULT_ROUTINES_YAML",
    "Routine",
    "RoutineScheduler",
    "RoutineStore",
    "build_routine_task",
    "compute_next_run",
]
