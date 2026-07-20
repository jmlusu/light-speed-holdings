"""Scheduler for autonomous cycles.

Uses FileStore for atomic persistence of scheduled task configs.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Callable, List, Optional

from pydantic import BaseModel, Field

from ai_company.store.file_store import FileStore

if TYPE_CHECKING:
    from ai_company.orchestrator.message_bus import MessageBus


class ScheduledTask(BaseModel):
    id: str
    name: str
    cron_expression: Optional[str] = None
    interval_minutes: Optional[int] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    enabled: bool = True
    task_template: dict = Field(default_factory=dict)


class Scheduler:
    def __init__(self, config_path: str = "orchestrator/scheduler.yaml"):
        self.config_path = Path(config_path)
        self._store = FileStore(self.config_path.parent, backup=True)
        self._config_name = self.config_path.name
        self.tasks: List[ScheduledTask] = []
        self._load_config()

    def _load_config(self):
        data = self._store.read_yaml(self._config_name)
        if data and isinstance(data, dict):
            self.tasks = [ScheduledTask(**t) for t in data.get("tasks", [])]

    def _save_config(self):
        data = {"tasks": [t.model_dump() for t in self.tasks]}
        self._store.write_yaml(self._config_name, data)

    def add_task(
        self,
        task_id: str,
        name: str,
        interval_minutes: Optional[int] = None,
        task_template: Optional[dict] = None,
    ) -> ScheduledTask:
        task = ScheduledTask(
            id=task_id,
            name=name,
            interval_minutes=interval_minutes,
            task_template=task_template or {},
            next_run=datetime.now() + timedelta(minutes=interval_minutes or 60),
        )
        self.tasks.append(task)
        self._save_config()
        return task

    def remove_task(self, task_id: str) -> bool:
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < original_len:
            self._save_config()
            return True
        return False

    def get_pending_tasks(self) -> List[ScheduledTask]:
        now = datetime.now()
        return [t for t in self.tasks if t.enabled and t.next_run and t.next_run <= now]

    def mark_completed(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                task.last_run = datetime.now()
                if task.interval_minutes:
                    task.next_run = datetime.now() + timedelta(minutes=task.interval_minutes)
        self._save_config()

    def create_pending_tasks(self, bus: "MessageBus") -> list[str]:
        """Check for due scheduled tasks and create inbox tasks for them.

        Returns a list of created task IDs.
        """
        from ai_company.models.task import Task, TaskPriority

        created: list[str] = []
        for scheduled in self.get_pending_tasks():
            template = scheduled.task_template
            task = Task(
                id=str(uuid.uuid4()),
                sender_id="scheduler",
                receiver_id=template.get("receiver_id", "chief-of-staff"),
                instruction=template.get("instruction", f"Scheduled: {scheduled.name}"),
                priority=TaskPriority(template.get("priority", "medium")),
            )
            bus.send_task(task)
            self.mark_completed(scheduled.id)
            created.append(task.id)
        return created

    def list_tasks(self) -> List[ScheduledTask]:
        return self.tasks

    def run_forever(
        self,
        bus: "MessageBus",
        interval_seconds: float = 60.0,
        max_cycles: Optional[int] = None,
        *,
        sleep: "Callable[[float], None]" = time.sleep,
    ) -> int:
        """Run autonomous scheduling cycles on an interval.

        Each cycle checks for due scheduled tasks via
        :meth:`create_pending_tasks` (reusing the same logic the executor
        loop uses) and then sleeps for ``interval_seconds``.

        Args:
            bus: The message bus used to enqueue due tasks.
            interval_seconds: Time to sleep between cycles.
            max_cycles: If set, stop after this many cycles. ``None`` (default)
                runs until interrupted by ``KeyboardInterrupt``.
            sleep: Injectable sleep callable (used for testing). Defaults to
                :func:`time.sleep`.

        Returns:
            The number of cycles executed.
        """
        cycles = 0
        try:
            while True:
                if max_cycles is not None and cycles >= max_cycles:
                    break
                self.create_pending_tasks(bus)
                cycles += 1
                if max_cycles is not None and cycles >= max_cycles:
                    break
                sleep(interval_seconds)
        except KeyboardInterrupt:
            pass
        return cycles
