"""
Scheduler for autonomous cycles.
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field


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
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: List[ScheduledTask] = []
        self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self.tasks = [ScheduledTask(**t) for t in data.get("tasks", [])]

    def _save_config(self):
        data = {"tasks": [t.model_dump() for t in self.tasks]}
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)

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

    def list_tasks(self) -> List[ScheduledTask]:
        return self.tasks
