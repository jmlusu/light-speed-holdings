"""Execution loop -- polls inbox.json and processes tasks autonomously.

GAP-017 hardening:
- On each ``tick()`` the executor scans for stale ``in_progress`` tasks
  (older than 30 minutes) and moves them to the dead-letter queue before
  processing new work.

GAP-001 fix:
- All inbox.json I/O now goes through ``MessageBus`` methods exclusively.
  The executor no longer reads or writes the inbox file directly.

Lease hardening:
- Tasks are claimed atomically (``claim_task``) so two executors can never
  run the same task, and a daemon thread refreshes the lease (heartbeat)
  while a long-running agent loop executes so stale-detection never races
  live work.
- HITL parking is persisted to ``.opencode/pending_approvals.json`` so a
  restart never strands a parked task.
- Per-task isolation: one task's failure cannot abort the whole tick.
"""

from __future__ import annotations

import asyncio
import logging
import os
import socket
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.audit.integration import init_audit, log_task_status
from ai_company.executor.agent_loop import AgentLoop, LoopConfig
from ai_company.executor.context import (
    AgentContext,
    build_user_prompt,
    parse_agent_spec,
)
from ai_company.executor.dead_letter import (
    DeadLetterQueue,
    detect_stale_tasks,
)
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.tool_runner import HITLParked, ToolRunner
from ai_company.llm.client import LLMClient
from ai_company.llm.cost_tracker import CostTracker
from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.memory.integration import init_memory, recall_context, record_task_outcome
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.approval import ApprovalGate
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.scheduler import Scheduler
from ai_company.store.file_store import FileStore
from ai_company.utils.logging import set_correlation_id

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

    All inbox I/O goes through ``MessageBus`` (GAP-001 fix).

    GAP-003 fix: ToolRunner classifies each tool action via tier_rules
    before requesting HITL approval.

    GAP-004 fix: Non-blocking HITL approval — the executor polls for
    resolved approvals on each tick, allowing other tasks to proceed
    while awaiting human decisions.
    """

    def __init__(
        self,
        poll_interval: float = 5.0,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
        agents_dir: str = ".opencode/agents",
        results_dir: str = "results",
        database: Any = None,
        daily_budget_usd: float | None = None,
        task_budget_usd: float | None = None,
        auto_suspend_on_overspend: bool = False,
        worker_id: str | None = None,
        lease_seconds: int = 1800,
    ) -> None:
        self.poll_interval = poll_interval
        self.agents_dir = agents_dir
        self.results_dir = Path(results_dir)
        self.database = database
        self.auto_suspend_on_overspend = auto_suspend_on_overspend

        # Lease / claim identity: this executor's stable worker id and the
        # lease it requests when claiming a pending task.  A daemon heartbeat
        # refreshes the lease while the agent loop runs.
        self.worker_id = worker_id or f"executor-{socket.gethostname()}-{os.getpid()}"
        self.lease_seconds = lease_seconds if lease_seconds > 0 else 1800

        # Core components (database enables the SQLite write-through mirror)
        self.bus = MessageBus(
            broadcast_callback=self._make_broadcast_callback(),
            database=database,
        )
        self.llm = LLMClient(config_path=config_path, registry_path=registry_path)
        self.runner = ToolRunner()
        self.hitl = HITLGate(ApprovalGate())

        # Cost tracking (strict caps from config/company/guardrails.yaml)
        self.cost_tracker = CostTracker(
            results_dir=results_dir,
            database=database,
            daily_budget_usd=daily_budget_usd,
            task_budget_usd=task_budget_usd,
        )

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

        # Multi-turn agentic loop (strict caps propagated to per-iteration guard)
        # max_iterations is configurable via AI_COMPANY_MAX_ITERS for local
        # model runs; defaults to the 10-iteration completion cap.
        try:
            max_iterations = int(os.environ.get("AI_COMPANY_MAX_ITERS", "10"))
        except ValueError:
            max_iterations = 10
        self.agent_loop = AgentLoop(
            llm=self.llm,
            runner=self.runner,
            cost_tracker=self.cost_tracker,
            hitl_gate=self.hitl,
            config=LoopConfig(
                max_iterations=max_iterations,
                daily_budget_usd=daily_budget_usd,
                task_budget_usd=task_budget_usd,
            ),
            # GAP-004: do not block the executor thread on HITL — park instead.
            non_blocking_hitl=True,
        )

        # Stats
        self.stats = ExecutorStats()
        self.running = False

        # Audit trail
        init_audit(database=database)

        # GAP-004: pending HITL approvals queue (non-blocking).
        # Maps task_id -> HITL request_id for tasks parked in WAITING_APPROVAL.
        # Persisted so a restart never strands a parked task.
        self._pending_store = FileStore(Path(".opencode"), backup=True)
        self._pending_name = "pending_approvals.json"
        self._pending_approvals = self._load_pending_approvals()

    def start(self) -> None:
        """Start continuous polling loop. Call stop() to halt."""
        self.running = True
        self.stats.start_time = datetime.now()
        logger.info("Executor started. Polling every %ss.", self.poll_interval)
        logger.info("Press Ctrl+C to stop.")

        try:
            while self.running:
                count = self.tick()
                if count > 0:
                    logger.info("Processed %d task(s).", count)
                import time

                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the polling loop."""
        self.running = False
        logger.info("Executor stopped. %d tasks processed.", self.stats.tasks_processed)

    def tick(self) -> int:
        """Process all pending tasks in a single pass. Returns count processed.

        Before processing, stale ``in_progress`` tasks are detected and
        moved to the dead-letter queue (GAP-017).  Parked tasks awaiting
        HITL approval (GAP-004) are resumed if a human decision has been
        recorded; otherwise they are left parked so the loop can continue.
        """
        # Convert due scheduled tasks into inbox tasks
        self.scheduler.create_pending_tasks(self.bus)

        # GAP-017 -- move stale tasks to dead-letter queue
        stale = detect_stale_tasks(self.bus, self.dlq)
        if stale:
            logger.warning("Moved %d stale task(s) to dead-letter queue.", len(stale))

        # GAP-004 -- resume any parked tasks whose HITL request resolved.
        self._resume_parked_tasks()

        # Guardrail: auto-suspend when the daily LLM budget is exhausted.
        # The per-task cap is already enforced inside AgentLoop (check_budget);
        # this guard stops the executor from processing further tasks for the
        # rest of the day, satisfying the auto-suspend requirement (#15 / Q9a).
        if self.auto_suspend_on_overspend and self.cost_tracker.daily_budget_exceeded():
            logger.warning(
                "Daily LLM budget exhausted ($%s); auto-suspending task processing.",
                self.cost_tracker.daily_budget,
            )
            return 0

        # GAP-001 fix: use MessageBus.get_pending_tasks() instead of direct I/O.
        # Each task is claimed atomically inside _process_task (pending ->
        # in_progress + lease); a task already claimed by another worker is
        # skipped. Per-task isolation guarantees one bad task can never abort
        # the whole tick.
        pending = self.bus.get_pending_tasks()
        processed = 0
        for task in pending:
            try:
                self._process_task(task)
                processed += 1
            except Exception:  # noqa: BLE001 - per-task isolation
                logger.exception("Task %s crashed the executor; isolated.", task.id)

        # GAP-005: Run memory consolidation periodically
        self._consolidation_scheduler.on_tick()

        return processed

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
            self._persist_pending_approvals()
            task = self.bus.get_task_by_id(task_id)
            if task is None:
                continue

            if decision:
                logger.info("HITL approved for task %s — resuming.", task_id)
                # Move the parked task back to pending so the atomic claim
                # can re-acquire ownership, then re-run it executing the
                # gated step directly (preapproved).
                self.bus.update_task_status(task.id, TaskStatus.PENDING.value)
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
        self._persist_pending_approvals()
        self.bus.update_task_status(task.id, TaskStatus.WAITING_APPROVAL.value)
        log_task_status(
            task.id,
            task.receiver_id,
            TaskStatus.IN_PROGRESS.value,
            TaskStatus.WAITING_APPROVAL.value,
        )
        logger.info(
            "Task %s parked (WAITING_APPROVAL) for HITL request %s",
            task.id,
            parked.request_id,
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

    def _load_pending_approvals(self) -> dict[str, str]:
        """Load the persisted ``task_id -> HITL request_id`` mapping at startup.

        Lets a restarted executor resume tasks that were parked before the
        crash once the human decision is recorded.
        """
        data = self._pending_store.read_json(self._pending_name)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
        return {}

    def _persist_pending_approvals(self) -> None:
        """Atomically persist the pending-approval mapping (best-effort)."""
        try:
            self._pending_store.write_json(self._pending_name, dict(self._pending_approvals))
        except Exception:  # noqa: BLE001 - persistence must not break execution
            logger.exception("Failed to persist pending approvals")

    def _start_heartbeat(self, task_id: str) -> threading.Event:
        """Start a daemon thread that refreshes the task lease until stopped.

        The heartbeat fires every ``lease_seconds / 3`` so the lease never
        expires while a long-running agent loop is still making progress;
        stale-detection therefore only reclaims genuinely dead tasks.  The
        returned ``Event`` must be set when processing finishes.
        """
        stop = threading.Event()
        interval = max(self.lease_seconds / 3.0, 1.0)

        def _beat() -> None:
            while not stop.wait(interval):
                try:
                    if not self.bus.heartbeat_task(task_id, self.worker_id, self.lease_seconds):
                        # Task is no longer in_progress/owned (e.g. it was
                        # completed or parked mid-run) -- stop beating.
                        stop.set()
                except Exception:  # noqa: BLE001 - a heartbeat failure never crashes
                    logger.debug("Heartbeat failed for task %s", task_id, exc_info=True)

        thread = threading.Thread(
            target=_beat,
            name=f"heartbeat-{task_id[:8]}",
            daemon=True,
        )
        thread.start()
        return stop

    def _process_task(self, task: Task, *, preapproved: bool = False) -> None:
        """Execute a single task through the multi-turn agentic loop.

        The task ID is installed as the correlation ID so that all log
        entries produced during execution (agent loop, LLM calls, tool
        calls) can be traced back to the originating task (GAP-018).

        The task is claimed atomically (``pending`` -> ``in_progress`` with a
        lease); if another worker already claimed it, this call is a no-op.
        A daemon heartbeat refreshes the lease while the loop runs so
        stale-detection never reclaims live work.

        Args:
            preapproved: GAP-004 — when True, any HITL-gated step is executed
                directly because the human already approved the parked request.
        """
        set_correlation_id(task.id)
        self.stats.tasks_processed += 1
        logger.info("[%s] Processing: %s...", task.id[:8], task.instruction[:60])

        # 1. Claim the task atomically (pending -> in_progress + lease).
        #    Only the winning worker runs it; losers skip.
        claimed = self.bus.claim_task(task.id, self.worker_id, self.lease_seconds)
        if claimed is None:
            logger.debug(
                "Task %s not claimable (already claimed/completed); skipping.",
                task.id,
            )
            return
        task = claimed
        log_task_status(task.id, task.receiver_id, "pending", TaskStatus.IN_PROGRESS.value)

        # Lease heartbeat: refresh the claim while the loop runs so
        # stale-detection never races live work.
        stop_heartbeat = self._start_heartbeat(task.id)
        try:
            # 2. Recall relevant memory BEFORE execution (best-effort, no network
            #    required — falls back to keyword search; never blocks the task).
            try:
                recall_context(task.instruction, limit=5)
            except Exception:  # noqa: BLE001 - pragma: no cover - defensive: recall must never break execution
                logger.debug("Memory recall failed for task %s", task.id, exc_info=True)

            # 3. Load agent spec card (falls back to defaults on failure so a
            #    malformed spec card can never abort the task).
            try:
                agent_ctx = parse_agent_spec(task.receiver_id, self.agents_dir)
            except Exception:  # noqa: BLE001 - per-task isolation
                logger.exception(
                    "Spec parse failed for %s; using defaults.",
                    task.receiver_id,
                )
                agent_ctx = AgentContext(name=task.receiver_id, role="", type="Unknown")

            # 3. Build user prompt
            try:
                user_prompt = build_user_prompt(task.instruction, task.priority.value)
            except Exception:  # noqa: BLE001 - per-task isolation
                user_prompt = task.instruction

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
            except HITLParked as exc:
                # GAP-004: a HITL-gated step raised HITLParked — park the task
                # and continue to the next one instead of blocking on approval.
                self._park_task(task, exc)
                return
            except Exception as exc:  # noqa: BLE001 - loop must never crash on a task
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

            # 5. Handle delegated tasks from tool results (isolated so a bad
            #    record cannot abort the parent task).
            for record in result.tool_results:
                if record.tool == "delegate" and record.status == "ok":
                    try:
                        self._create_subtask_from_record(task, record)
                    except Exception:  # noqa: BLE001 - per-task isolation
                        logger.exception(
                            "Subtask creation failed for task %s",
                            task.id,
                        )

            # 6. Save artifacts (atomic write; failure must not abort the task)
            try:
                self._save_loop_artifacts(task, result)
            except Exception:  # noqa: BLE001 - artifacts are best-effort
                logger.exception("Artifact save failed for task %s", task.id)

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
        finally:
            stop_heartbeat.set()

    def _complete_task(self, task: Task, status: TaskStatus, result: str) -> None:
        """Mark a task as completed/failed via MessageBus (GAP-001 fix)."""
        old_status = task.status.value
        self.bus.update_task_status(task.id, status.value, result=result)
        log_task_status(task.id, task.receiver_id, old_status, status.value)

    def _save_loop_artifacts(self, task: Task, result: Any) -> None:
        """Save agentic loop execution artifacts to results/{task_id}/."""
        task_dir = self.results_dir / task.id
        task_dir.mkdir(parents=True, exist_ok=True)

        # Save loop result (atomic write via FileStore so a crash mid-write
        # can never leave a truncated loop_result.json behind).
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
        FileStore(task_dir, backup=False).write_json("loop_result.json", log_data)

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
