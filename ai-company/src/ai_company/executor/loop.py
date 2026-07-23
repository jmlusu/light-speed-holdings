"""Execution loop -- polls inbox.json and processes tasks autonomously.

GAP-017 hardening:
- On each ``tick()`` the executor scans for stale ``in_progress`` tasks
  (older than 30 minutes) and moves them to the dead-letter queue before
  processing new work.

GAP-001 fix:
- All inbox.json I/O now goes through ``MessageBus`` methods exclusively.
  The executor no longer reads or writes the inbox file directly.

AI-1: SQLite TaskStore backend (feature flag ``TASK_STORE_BACKEND=sqlite``).
- When enabled the executor uses :class:`TaskStore` instead of
  :class:`MessageBus`, providing INSERT OR REPLACE semantics and
  atomic SQL transactions.

AI-3: Compare-and-swap tick via ``claim_next_pending()``.
- The executor now atomically claims one pending task at a time instead
  of fetching all pending and iterating — eliminating the check-then-act
  race condition.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.audit.integration import init_audit, log_task_status
from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.memory.integration import init_memory, recall_context, record_task_outcome
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
from ai_company.executor.tool_runner import HITLParked, ToolRunner
from ai_company.llm.client import LLMClient
from ai_company.llm.cost_tracker import CostTracker
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.scheduler import Scheduler
from ai_company.utils.logging import new_correlation_id

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
    - tick(): Single-pass -- process all pending tasks once and return.
    - start(): Continuous polling -- runs tick() in a loop.

    All inbox I/O goes through ``MessageBus`` (GAP-001 fix) or the
    SQLite-backed ``TaskStore`` (AI-1 feature flag).

    GAP-003 fix: ToolRunner classifies each tool action via tier_rules
    before requesting HITL approval.

    GAP-004 fix: Non-blocking HITL approval — the executor polls for
    resolved approvals on each tick, allowing other tasks to proceed
    while awaiting human decisions.

    AI-1: When ``TASK_STORE_BACKEND=sqlite`` (or unset), the executor
    tries to use the SQLite-backed TaskStore.  Falls back to MessageBus
    if the database is unavailable.

    AI-3: ``tick()`` now uses ``claim_next_pending()`` — an atomic
    compare-and-swap — instead of ``get_pending_tasks()`` + iterate,
    eliminating the check-then-act race condition.
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

        # AI-1: Core components — TaskStore (SQLite) or MessageBus (JSON)
        self.bus = self._create_task_store()
        self.llm = LLMClient(config_path=config_path, registry_path=registry_path)
        self.runner = ToolRunner()
        self.hitl = HITLGate(ApprovalGate())

        # Cost tracking
        self.cost_tracker = CostTracker(results_dir=results_dir)

        # Scheduler for autonomous cycles
        self.scheduler = Scheduler()

        # Memory
        self._memory = init_memory()

        # GAP-005: Memory consolidation scheduler
        self._consolidation_config = ConsolidationConfig()
        self._consolidation_scheduler = ConsolidationScheduler(
            store=self._memory,
            config=self._consolidation_config,
        )

        # Dead-letter queue (GAP-017)
        self.dlq = DeadLetterQueue()

        # Multi-turn agentic loop
        self.agent_loop = AgentLoop(
            llm=self.llm,
            runner=self.runner,
            cost_tracker=self.cost_tracker,
            hitl_gate=self.hitl,
            config=LoopConfig(max_iterations=10),
            # GAP-004: do not block the executor thread on HITL — park instead.
            non_blocking_hitl=True,
        )

        # Stats
        self.stats = ExecutorStats()
        self.running = False

        # Audit trail
        init_audit()

        # GAP-004: pending HITL approvals queue (non-blocking).
        # Maps task_id -> HITL request_id for tasks parked in WAITING_APPROVAL.
        self._pending_approvals: dict[str, str] = {}

    # ── AI-1: Task backend factory ───────────────────────────────────

    @staticmethod
    def _create_task_store() -> Any:
        """Create the task backend.

        If ``TASK_STORE_BACKEND`` is ``"sqlite"`` (or unset when SQLite is
        available), a SQLite-backed :class:`TaskStore` is returned.  If the
        database cannot be initialised, the JSON-backed :class:`MessageBus`
        is used as a fallback.

        The returned object exposes the same public API used by the
        executor: ``send_task``, ``get_pending_tasks``,
        ``claim_next_pending``, ``get_task_by_id``, ``update_task_status``,
        and ``get_all_tasks``.
        """
        backend = os.environ.get("TASK_STORE_BACKEND", "sqlite").lower()
        if backend == "sqlite":
            try:
                from ai_company.data import TaskStore, init_database

                db = init_database()
                store = TaskStore(db)
                logger.info("Using SQLite TaskStore backend.")
                return store  # type: ignore[return-value]
            except Exception:
                logger.warning(
                    "SQLite backend unavailable — falling back to MessageBus.",
                    exc_info=True,
                )

        logger.info("Using JSON MessageBus backend.")
        return MessageBus(broadcast_callback=Executor._make_broadcast_callback())

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
                import time
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
        moved to the dead-letter queue (GAP-017).  Parked tasks awaiting
        HITL approval (GAP-004) are resumed if a human decision has been
        recorded; otherwise they are left parked so the loop can continue.

        AI-3: Uses ``claim_next_pending()`` — an atomic compare-and-swap
        — to claim one task at a time instead of fetching all pending and
        iterating.  This eliminates the check-then-act race condition.
        """
        # Convert due scheduled tasks into inbox tasks
        self.scheduler.create_pending_tasks(self.bus)

        # GAP-017 -- move stale tasks to dead-letter queue
        self._detect_stale_tasks()

        # GAP-004 -- resume any parked tasks whose HITL request resolved.
        self._resume_parked_tasks()

        # AI-3: Atomic compare-and-swap — claim one pending task at a time.
        processed = 0
        while True:
            task = self.bus.claim_next_pending()
            if task is None:
                break
            self._process_task(task)
            processed += 1

        # GAP-005: Run memory consolidation periodically
        self._consolidation_scheduler.on_tick()

        return processed

    def _detect_stale_tasks(self) -> None:
        """Detect and move stale ``in_progress`` tasks to the dead-letter queue.

        Dispatches to either the SQLite-native ``TaskStore.detect_stale_tasks``
        or the file-based ``dead_letter.detect_stale_tasks`` depending on
        which backend is in use.
        """
        from ai_company.data.task_store import TaskStore

        if isinstance(self.bus, TaskStore):
            stale = self.bus.detect_stale_tasks(self.dlq)
        else:
            # MessageBus — use the MessageBus-backed detector
            stale = detect_stale_tasks(self.bus, self.dlq)

        if stale:
            logger.warning("Moved %d stale task(s) to dead-letter queue.", len(stale))

    def _resume_parked_tasks(self) -> int:
        """Resume tasks parked in WAITING_APPROVAL once HITL resolves.

        Returns the number of tasks resumed (approved or rejected) this tick.
        Approved tasks are re-processed with ``preapproved=True`` so the
        previously gated step executes without re-requesting approval.
        Rejected tasks are marked FAILED.  Still-pending requests are left
        parked — the executor does NOT block waiting for them.
        """
        resumed = 0
        for task_id, request_id in list(self._pending_approvals.items()):
            decision = self.hitl.resume_approved(request_id)
            if decision is None:
                continue  # still awaiting human decision — stay parked

            resumed += 1
            self._pending_approvals.pop(task_id, None)
            task = self.bus.get_task_by_id(task_id)
            if task is None:
                continue

            if decision:
                logger.info("HITL approved for task %s — resuming.", task_id)
                # Re-run the task, executing the gated step directly.
                self._process_task(task, preapproved=True)
            else:
                logger.info("HITL rejected for task %s — failing.", task_id)
                self._complete_task(task, TaskStatus.FAILED, "Human approval denied")
                self.stats.tasks_failed += 1
        return resumed

    def _park_task(self, task: Task, parked: HITLParked) -> None:
        """Park a task in WAITING_APPROVAL and record its HITL request id.

        The task is transitioned to ``waiting_approval`` so the executor's
        ``tick()`` loop skips it on subsequent passes (``get_pending_tasks``
        only returns ``pending`` tasks) and continues with other work.  The
        original ``in_progress`` status is overwritten to ``waiting_approval``
        so it is not mistaken for an active task.
        """
        self._pending_approvals[task.id] = parked.request_id
        self.bus.update_task_status(task.id, TaskStatus.WAITING_APPROVAL.value)
        log_task_status(
            task.id, task.receiver_id, TaskStatus.IN_PROGRESS.value,
            TaskStatus.WAITING_APPROVAL.value,
        )
        logger.info(
            "Task %s parked (WAITING_APPROVAL) for HITL request %s",
            task.id, parked.request_id,
        )

    @staticmethod
    def _make_broadcast_callback() -> Any:
        """Return a sync callback that pushes task events to WebSocket clients.

        GAP-006: the executor mutates task status through ``MessageBus``; by
        wiring this callback the same events are broadcast live to connected
        dashboard clients.  Uses the dashboard's sync→async bridge so it is a
        no-op when no event loop (CLI) is running.
        """
        from ai_company.dashboard.ws import broadcast_task_update

        def _callback(task_dict: dict[str, Any], event: str) -> None:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(broadcast_task_update(task_dict, event))
            except RuntimeError:
                # No running event loop (CLI / executor thread) — skip.
                logger.debug("No event loop; WS broadcast skipped for '%s'", event)

        return _callback

    def _process_task(self, task: Task, *, preapproved: bool = False) -> None:
        """Execute a single task through the multi-turn agentic loop.

        A new correlation ID is generated for each task so that all log
        entries produced during execution can be traced back to the
        originating task.

        Args:
            preapproved: GAP-004 — when True, any HITL-gated step is executed
                directly because the human already approved the parked request.
        """
        new_correlation_id()
        self.stats.tasks_processed += 1
        logger.info("[%s] Processing: %s...", task.id[:8], task.instruction[:60])

        # 1. Mark in_progress via MessageBus (GAP-001 fix)
        self.bus.update_task_status(task.id, TaskStatus.IN_PROGRESS.value)
        log_task_status(task.id, task.receiver_id, "pending", TaskStatus.IN_PROGRESS.value)

        # 2. Recall relevant memory BEFORE execution (best-effort, no network
        #    required — falls back to keyword search; never blocks the task).
        try:
            recall_context(task.instruction, limit=5)
        except Exception:  # pragma: no cover - defensive: recall must never break execution
            logger.debug("Memory recall failed for task %s", task.id, exc_info=True)

        # 3. Load agent spec card
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
                preapproved=preapproved,
            )
        except Exception as exc:
            # GAP-004: a HITL-gated step raised HITLParked — park the task and
            # continue to the next one instead of blocking on human approval.
            from ai_company.executor.tool_runner import HITLParked

            if isinstance(exc, HITLParked):
                self._park_task(task, exc)
                return

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
            # R3: Auto-retry on failure if retries remain
            self._maybe_retry(task)
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
            # R3: Auto-retry on failure if retries remain
            self._maybe_retry(task)

    def _complete_task(self, task: Task, status: TaskStatus, result: str) -> None:
        """Mark a task as completed/failed via MessageBus (GAP-001 fix)."""
        old_status = task.status.value
        self.bus.update_task_status(task.id, status.value, result=result)
        log_task_status(task.id, task.receiver_id, old_status, status.value)

    def _maybe_retry(self, task: Task) -> None:
        """R3: Schedule automatic retry with exponential backoff if retries remain.

        Delay progression: 30s, 60s, 120s, ... (30 * 2^retry_count).
        Only retries for the JSON-backed MessageBus (SQLite has native support).
        """
        from ai_company.orchestrator.message_bus import MessageBus

        if not isinstance(self.bus, MessageBus):
            return  # SQLite TaskStore handles retries differently

        # Re-fetch the task to get the latest retry_count
        fresh_task = self.bus.get_task_by_id(task.id)
        if fresh_task is None:
            return

        if fresh_task.retry_count < fresh_task.max_retries:
            delay = 30 * (2 ** fresh_task.retry_count)  # 30s, 60s, 120s, ...
            self.bus.retry_task(task.id, delay_seconds=delay)
            logger.info(
                "Task %s scheduled for retry in %.0fs (attempt %d/%d)",
                task.id, delay, fresh_task.retry_count + 1, fresh_task.max_retries,
            )

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
