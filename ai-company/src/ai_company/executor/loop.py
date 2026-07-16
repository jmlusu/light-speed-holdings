"""Execution loop — polls inbox.json and processes tasks autonomously."""

from __future__ import annotations

import json
import shutil
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.executor.context import (
    build_system_prompt,
    build_user_prompt,
    parse_agent_spec,
)
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.tool_runner import ToolRunner
from ai_company.llm.client import LLMClient
from ai_company.llm.providers.base import LLMProviderError, LLMResponseError
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.message_bus import MessageBus


class ExecutorStats:
    """Runtime statistics for the executor."""

    def __init__(self) -> None:
        self.tasks_processed: int = 0
        self.tasks_succeeded: int = 0
        self.tasks_failed: int = 0
        self.start_time: datetime | None = None

    @property
    def uptime_seconds(self) -> float:
        if self.start_time is None:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        return {
            "tasks_processed": self.tasks_processed,
            "tasks_succeeded": self.tasks_succeeded,
            "tasks_failed": self.tasks_failed,
            "uptime_seconds": round(self.uptime_seconds, 1),
            "running": self.start_time is not None,
        }


class Executor:
    """Processes tasks from the inbox using LLM + tool execution.

    Supports two modes:
    - tick(): Single-pass — process all pending tasks once and return.
    - start(): Continuous polling — runs tick() in a loop.
    """

    def __init__(
        self,
        poll_interval: float = 5.0,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
        agents_dir: str = ".opencode/agents",
        results_dir: str = "results",
    ) -> None:
        self.poll_interval = poll_interval
        self.agents_dir = agents_dir
        self.results_dir = Path(results_dir)

        # Core components
        self.bus = MessageBus()
        self.llm = LLMClient(config_path=config_path, registry_path=registry_path)
        self.runner = ToolRunner()
        self.hitl = HITLGate(ApprovalGate())

        # Stats
        self.stats = ExecutorStats()
        self.running = False

    def start(self) -> None:
        """Start continuous polling loop. Call stop() to halt."""
        self.running = True
        self.stats.start_time = datetime.now()
        print(f"Executor started. Polling every {self.poll_interval}s.")
        print("Press Ctrl+C to stop.\n")

        try:
            while self.running:
                count = self.tick()
                if count > 0:
                    print(f"  Processed {count} task(s).")
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the polling loop."""
        self.running = False
        print(f"\nExecutor stopped. {self.stats.tasks_processed} tasks processed.")

    def tick(self) -> int:
        """Process all pending tasks in a single pass. Returns count processed."""
        pending = self._get_pending_tasks()
        for task in pending:
            self._process_task(task)
        return len(pending)

    def _get_pending_tasks(self) -> list[Task]:
        """Load all pending tasks from inbox.json."""
        inbox_path = Path(self.bus.storage_path)
        if not inbox_path.exists():
            return []

        try:
            raw = json.loads(inbox_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

        tasks: list[Task] = []
        for item in raw:
            if item.get("status") == "pending":
                try:
                    tasks.append(Task(**item))
                except Exception:
                    continue
        return tasks

    def _process_task(self, task: Task) -> None:
        """Execute a single task through the full pipeline."""
        self.stats.tasks_processed += 1
        print(f"\n[{task.id[:8]}] Processing: {task.instruction[:60]}...")

        # 1. Mark in_progress
        self._update_task_status(task, TaskStatus.IN_PROGRESS)

        # 2. Load agent spec card
        agent_ctx = parse_agent_spec(task.receiver_id, self.agents_dir)

        # 3. Build prompts
        system_prompt = build_system_prompt(agent_ctx)
        user_prompt = build_user_prompt(task.instruction, task.priority.value)

        # 4. Call LLM with retry
        try:
            response = self.llm.execute_task(
                agent_name=task.receiver_id,
                task_instruction=user_prompt,
                priority=task.priority.value,
                context=None,
                system_prompt=system_prompt,
            )
        except LLMResponseError as exc:
            print(f"  LLM FAILED after retries: {exc}")
            self._complete_task(task, TaskStatus.FAILED, str(exc))
            self.stats.tasks_failed += 1
            return
        except LLMProviderError as exc:
            print(f"  Provider error: {exc}")
            self._complete_task(task, TaskStatus.FAILED, str(exc))
            self.stats.tasks_failed += 1
            return

        # 5. Execute tool plan
        plan = response.get("plan", [])
        step_results = self.runner.run_plan(
            plan=plan,
            hitl_gate=self.hitl,
            task_id=task.id,
            agent_id=task.receiver_id,
        )

        # 6. Handle delegated tasks
        for step in step_results:
            if step.get("tool") == "delegate" and step.get("status") == "ok":
                self._create_subtask(task, step)

        # 7. Save artifacts to results/{task_id}/
        self._save_artifacts(task, response, step_results)

        # 8. Mark completed
        result_text = response.get("result", "Task completed successfully.")
        self._complete_task(task, TaskStatus.COMPLETED, result_text)
        self.stats.tasks_succeeded += 1
        print(f"  COMPLETED: {result_text[:80]}")

    def _update_task_status(self, task: Task, status: TaskStatus) -> None:
        """Update a task's status in inbox.json."""
        inbox_path = Path(self.bus.storage_path)
        if not inbox_path.exists():
            return

        try:
            tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        for t in tasks:
            if t.get("id") == task.id:
                t["status"] = status.value
                break

        inbox_path.write_text(json.dumps(tasks, indent=2, default=str), encoding="utf-8")

    def _complete_task(self, task: Task, status: TaskStatus, result: str) -> None:
        """Mark a task as completed/failed with result."""
        inbox_path = Path(self.bus.storage_path)
        if not inbox_path.exists():
            return

        try:
            tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        now = datetime.now().isoformat()
        for t in tasks:
            if t.get("id") == task.id:
                t["status"] = status.value
                t["result"] = result
                t["completed_at"] = now
                break

        inbox_path.write_text(json.dumps(tasks, indent=2, default=str), encoding="utf-8")

    def _save_artifacts(
        self,
        task: Task,
        response: dict[str, Any],
        step_results: list[dict[str, Any]],
    ) -> None:
        """Save execution artifacts to results/{task_id}/."""
        task_dir = self.results_dir / task.id
        task_dir.mkdir(parents=True, exist_ok=True)

        # Save execution log
        log_path = task_dir / "execution_log.json"
        log_data = {
            "task_id": task.id,
            "agent": task.receiver_id,
            "instruction": task.instruction,
            "response": response,
            "step_results": step_results,
            "timestamp": datetime.now().isoformat(),
        }
        log_path.write_text(json.dumps(log_data, indent=2, default=str), encoding="utf-8")

        # Copy artifact files if they exist on disk
        for artifact_path in response.get("artifacts", []):
            src = Path(artifact_path)
            if src.exists() and src.is_file():
                dest = task_dir / src.name
                try:
                    shutil.copy2(src, dest)
                except OSError:
                    pass

    def _create_subtask(self, parent_task: Task, step: dict[str, Any]) -> None:
        """Create a subtask in the inbox from a delegate tool step."""
        receiver = step.get("receiver", "")
        instruction = step.get("instruction", "")
        if not receiver or not instruction:
            return

        subtask = Task(
            id=str(uuid.uuid4()),
            sender_id=parent_task.receiver_id,
            receiver_id=receiver,
            instruction=instruction,
            priority=TaskPriority.MEDIUM,
        )
        self.bus.send_task(subtask)
        print(f"  Delegated subtask to {receiver}")
