"""Execution loop — polls inbox.json and processes tasks autonomously.

GAP-017 hardening:
- On each ``tick()`` the executor scans for stale ``in_progress`` tasks
  (older than 30 minutes) and moves them to the dead-letter queue before
  processing new work.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.audit.integration import init_audit, log_task_status
from ai_company.memory.integration import init_memory, record_task_outcome
from ai_company.executor.context import (
    build_user_prompt,
    parse_agent_spec,
)
from ai_company.executor.agent_loop import AgentLoop, LoopConfig
from ai_company.executor.dead_letter import (
    DeadLetterQueue,
    detect_stale_tasks,
)
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.tool_runner import ToolRunner
from ai_company.llm.client import LLMClient
from ai_company.llm.cost_tracker import CostTracker
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.scheduler import Scheduler

logger = logging.getLogger(__name__)


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

        # Cost tracking
        self.cost_tracker = CostTracker(results_dir=results_dir)

        # Scheduler for autonomous cycles
        self.scheduler = Scheduler()

        # Memory
        self._memory = init_memory()

        # Dead-letter queue (GAP-017)
        self.dlq = DeadLetterQueue()

        # Multi-turn agentic loop
        self.agent_loop = AgentLoop(
            llm=self.llm,
            runner=self.runner,
            cost_tracker=self.cost_tracker,
            hitl_gate=self.hitl,
            config=LoopConfig(max_iterations=10),
        )

        # Stats
        self.stats = ExecutorStats()
        self.running = False

        # Audit trail
        init_audit()

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
        """Process all pending tasks in a single pass. Returns count processed.

        Before processing, stale ``in_progress`` tasks are detected and
        moved to the dead-letter queue (GAP-017).
        """
        # Convert due scheduled tasks into inbox tasks
        self.scheduler.create_pending_tasks(self.bus)

        # GAP-017 — move stale tasks to dead-letter queue
        stale = detect_stale_tasks(Path(self.bus.storage_path), self.dlq)
        if stale:
            logger.warning("Moved %d stale task(s) to dead-letter queue.", len(stale))

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
        """Execute a single task through the multi-turn agentic loop."""
        self.stats.tasks_processed += 1
        logger.info("[%s] Processing: %s...", task.id[:8], task.instruction[:60])

        # 1. Mark in_progress
        self._update_task_status(task, TaskStatus.IN_PROGRESS)

        # 2. Load agent spec card
        agent_ctx = parse_agent_spec(task.receiver_id, self.agents_dir)

        # 3. Build user prompt
        user_prompt = build_user_prompt(task.instruction, task.priority.value)

        # 4. Run multi-turn agentic loop
        try:
            result = self.agent_loop.run(
                agent=agent_ctx,
                user_prompt=user_prompt,
                agent_name=task.receiver_id,
                task_id=task.id,
                priority=task.priority.value,
            )
        except Exception as exc:
            logger.error("Agent loop failed: %s", exc)
            self._complete_task(task, TaskStatus.FAILED, str(exc))
            self.stats.tasks_failed += 1
            record_task_outcome(
                task_id=task.id,
                agent_id=task.receiver_id,
                instruction=task.instruction,
                status="failed",
                result_summary=str(exc),
            )
            return

        # 5. Handle delegated tasks from tool results
        for record in result.tool_results:
            if record.tool == "delegate" and record.status == "ok":
                self._create_subtask_from_record(task, record)

        # 6. Save artifacts
        self._save_loop_artifacts(task, result)

        # 7. Mark completed or failed
        if result.done and not result.error:
            self._complete_task(task, TaskStatus.COMPLETED, result.final_response)
            self.stats.tasks_succeeded += 1
            record_task_outcome(
                task_id=task.id,
                agent_id=task.receiver_id,
                instruction=task.instruction,
                status="completed",
                result_summary=result.final_response,
                tools_used=[r.tool for r in result.tool_results if r.tool],
            )
            logger.info("  COMPLETED: %s", result.final_response[:80])
        else:
            error_msg = result.error or "Loop did not complete"
            self._complete_task(task, TaskStatus.FAILED, error_msg)
            self.stats.tasks_failed += 1
            record_task_outcome(
                task_id=task.id,
                agent_id=task.receiver_id,
                instruction=task.instruction,
                status="failed",
                result_summary=error_msg,
                tools_used=[r.tool for r in result.tool_results if r.tool],
            )
            logger.error("  FAILED: %s", error_msg[:80])

    def _update_task_status(self, task: Task, status: TaskStatus) -> None:
        """Update a task's status in inbox.json and set ``updated_at``."""
        inbox_path = Path(self.bus.storage_path)
        if not inbox_path.exists():
            return

        try:
            tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        now = datetime.now().isoformat()
        old_status = ""
        for t in tasks:
            if t.get("id") == task.id:
                old_status = t.get("status", "")
                t["status"] = status.value
                t["updated_at"] = now
                if not t.get("created_at"):
                    t["created_at"] = now
                break

        inbox_path.write_text(json.dumps(tasks, indent=2, default=str), encoding="utf-8")
        log_task_status(task.id, task.receiver_id, old_status, status.value)

    def _complete_task(self, task: Task, status: TaskStatus, result: str) -> None:
        """Mark a task as completed/failed with result and timestamps."""
        inbox_path = Path(self.bus.storage_path)
        if not inbox_path.exists():
            return

        try:
            tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        now = datetime.now().isoformat()
        old_status = ""
        for t in tasks:
            if t.get("id") == task.id:
                old_status = t.get("status", "")
                t["status"] = status.value
                t["result"] = result
                t["updated_at"] = now
                t["completed_at"] = now
                if not t.get("created_at"):
                    t["created_at"] = now
                break

        inbox_path.write_text(json.dumps(tasks, indent=2, default=str), encoding="utf-8")
        log_task_status(task.id, task.receiver_id, old_status, status.value)

    def _save_loop_artifacts(self, task: Task, result: Any) -> None:
        """Save agentic loop execution artifacts to results/{task_id}/."""
        task_dir = self.results_dir / task.id
        task_dir.mkdir(parents=True, exist_ok=True)

        # Save loop result
        log_path = task_dir / "loop_result.json"
        log_data = {
            "task_id": task.id,
            "agent": task.receiver_id,
            "final_response": result.final_response,
            "iterations": result.iterations,
            "total_tokens": result.total_tokens,
            "total_cost_usd": result.total_cost_usd,
            "done": result.done,
            "error": result.error,
            "tool_results": [
                {"step": r.step, "tool": r.tool, "status": r.status, "iteration": r.iteration}
                for r in result.tool_results
            ],
            "timestamp": datetime.now().isoformat(),
        }
        log_path.write_text(json.dumps(log_data, indent=2, default=str), encoding="utf-8")

    def _create_subtask_from_record(self, parent_task: Task, record: Any) -> None:
        """Create a subtask from a ToolCallRecord with delegate tool."""
        result_data = record.result
        receiver = result_data.get("receiver", "")
        instruction = result_data.get("instruction", "")
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
        logger.info("  Delegated subtask to %s", receiver)
