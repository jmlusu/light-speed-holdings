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

import contextlib
import logging
import os
import socket
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.audit.integration import get_writer, init_audit, log_task_status
from ai_company.executor.agent_loop import AgentLoop, LoopConfig
from ai_company.executor.context import (
    AgentContext,
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
from ai_company.memory.integration import (
    extract_post_task_knowledge,
    init_memory,
    recall_context,
    record_task_outcome,
)
from ai_company.memory.metrics import LearningMetricsCollector, TaskMetrics
from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.approval import ApprovalStatus
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.notifier import ApprovalNotifier
from ai_company.orchestrator.scheduler import Scheduler
from ai_company.orchestrator.suspend_store import SuspendedState, SuspendStore
from ai_company.store.file_store import FileStore
from ai_company.telemetry import (
    detach_task_context,
    set_correlation_id_from_task,
    subtask_context,
)

logger = logging.getLogger(__name__)


def _warn_on_silent_audit(processed: int, events_before: int, writer: Any) -> None:
    """Emit a warning when a tick did real work but the audit trail did not grow.

    Smoke guard (ticket #71): the canonical trail is append-only by
    definition — a tick that processes tasks MUST record at least one event
    (task lifecycle + tool calls). Zero growth means the write path is
    silently misconfigured (wrong data root, decoy target, disabled writer),
    which is exactly how the OP-16 proof ended up with a 0-byte trail.
    """
    if processed <= 0:
        return
    events_after = writer.events_written if writer is not None else 0
    if events_after > events_before:
        return
    logger.warning(
        "Tick processed %d task(s) but the audit trail recorded 0 new events — "
        "canonical audit trail may be misconfigured (ticket #71).",
        processed,
    )


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

        # Cost tracking (strict caps from config/company/guardrails.yaml)
        self.cost_tracker = CostTracker(
            results_dir=results_dir,
            database=database,
            daily_budget_usd=daily_budget_usd,
            task_budget_usd=task_budget_usd,
        )

        # OB5: the LLM client shares the executor's CostTracker so every
        # usage record flows through the single JSONL + SQLite mirror path
        # (see CostTracker.record_usage) instead of a second direct write.
        self.llm = LLMClient(
            config_path=config_path,
            registry_path=registry_path,
            cost_tracker=self.cost_tracker,
        )
        self.runner = ToolRunner()
        self.hitl = HITLGate()

        # Async approval engine (issue #42): suspend-to-disk + notifications
        self._suspend_store = SuspendStore()
        self._notifier = ApprovalNotifier()

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

        # Continuous learning metrics
        self._metrics_collector = LearningMetricsCollector()
        self._task_metrics_buffer: list[TaskMetrics] = []
        self._tick_metrics_count = 0

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
        # Audit smoke guard (ticket #71): record how many events the shared
        # writer has appended so we can detect a tick that processes tasks
        # without growing the canonical trail.
        audit_writer = get_writer()
        audit_events_before = audit_writer.events_written if audit_writer is not None else 0

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
        consolidation_result = self._consolidation_scheduler.on_tick()

        # Continuous-learning metrics: capture consolidation stats + periodic snapshot
        if consolidation_result:
            with contextlib.suppress(Exception):
                self._metrics_collector.record_consolidation(
                    entries_pruned=int(consolidation_result.get("entries_pruned", 0)),
                    episodic_digested=int(consolidation_result.get("episodic_digested", 0)),
                )
        try:
            # Snapshot every 25 ticks to keep the trend window fresh without IO spam
            if self._tick_metrics_count >= 25:
                self._metrics_collector.compute_snapshot(store=self._memory)
                self._tick_metrics_count = 0
            else:
                self._tick_metrics_count = self._tick_metrics_count + 1
        except Exception:  # noqa: BLE001 - metrics are best-effort
            logger.debug("Metrics snapshot failed", exc_info=True)

        # Audit smoke guard: warn if this tick did work but recorded nothing
        # (append-only trail must grow on every processed task).
        _warn_on_silent_audit(processed, audit_events_before, get_writer())

        return processed

    def _resume_parked_tasks(self) -> int:
        """Resume tasks parked in WAITING_APPROVAL once HITL resolves.

        Returns the number of tasks resumed (approved or rejected) this tick.
        Approved tasks are re-processed with ``preapproved=True`` so the
        previously gated step executes without re-requesting approval —
        EXCEPT requests flagged ``metacharacter_blocked`` (GAP-016 / #70):
        the approved command can never pass the executor's shell filter, so
        the task is failed fast with an explicit message instead of silently
        retrying until max iterations.  Rejected tasks are marked FAILED.
        Still-pending requests are left parked — the executor does NOT block
        waiting for them.

        Two sources of parked tasks are reconciled against the SSOT approvals
        store (ticket #57):

        - **Index-backed**: ``task_id -> request_id`` entries loaded from
          ``pending_approvals.json``.  Entries whose task no longer exists in
          the inbox are pruned so they cannot linger pinning a stale request.
        - **Index-lost (healing)**: an inbox task in ``WAITING_APPROVAL``
          with no index entry (crash before the index persisted, or a
          rotated/reset index) is healed by looking up the latest approval
          decision for its ``task_id`` directly in the approvals store.
        """
        resumed = 0
        inbox_tasks = self.bus.get_all_tasks()
        inbox_ids = {t.id for t in inbox_tasks}
        # Tasks acted on in pass 1 must not be re-healed by pass 2 (they are
        # popped from the index by the time pass 2 runs, so the index check
        # alone would let them through).
        acted_this_tick: set[str] = set()

        # Pass 1 — index-backed entries.
        for task_id, request_id in list(self._pending_approvals.items()):
            if task_id not in inbox_ids:
                logger.info(
                    "Pruning stale pending-approval index entry for task %s "
                    "(task no longer exists in the inbox).",
                    task_id,
                )
                self._pending_approvals.pop(task_id, None)
                self._persist_pending_approvals()
                continue

            decision = self.hitl.resume_approved(request_id)
            if decision is None:
                continue  # still awaiting human decision — stay parked

            resumed += 1
            acted_this_tick.add(task_id)
            self._pending_approvals.pop(task_id, None)
            self._persist_pending_approvals()
            task = self.bus.get_task_by_id(task_id)
            if task is None:
                continue

            if decision:
                self._resume_approved_task(task, request_id)
            else:
                logger.info("HITL rejected for task %s — failing.", task_id)
                self._complete_task(task, TaskStatus.FAILED, "Human approval denied")
                self.stats.tasks_failed += 1
                # Clean up suspended state on rejection (issue #42).
                self._suspend_store.delete(task_id)
                try:
                    self._notifier.notify_resolved(
                        request_id=request_id,
                        task_id=task_id,
                        decision="rejected",
                    )
                except Exception:  # noqa: BLE001
                    logger.debug(
                        "Resolution notification failed for task %s", task_id, exc_info=True
                    )

        # Pass 2 — SSOT healing for parked tasks whose index entry was lost.
        parked_tasks = [t for t in inbox_tasks if t.status == TaskStatus.WAITING_APPROVAL.value]
        for task in parked_tasks:
            if task.id in self._pending_approvals or task.id in acted_this_tick:
                continue
            request = self.hitl.gate.get_latest_request_for_task(task.id)
            if request is None or request.status == ApprovalStatus.PENDING:
                continue  # no decision recorded yet — stay parked

            resumed += 1
            if request.status == ApprovalStatus.APPROVED:
                self._resume_approved_task(task, request.id)
            else:
                logger.info(
                    "HITL %s for task %s — failing (index lost).",
                    request.status.value,
                    task.id,
                )
                self._complete_task(task, TaskStatus.FAILED, "Human approval denied")
                self.stats.tasks_failed += 1
                # Clean up suspended state on rejection (issue #42).
                self._suspend_store.delete(task.id)
                try:
                    self._notifier.notify_resolved(
                        request_id=request.id,
                        task_id=task.id,
                        decision=request.status.value,
                    )
                except Exception:  # noqa: BLE001
                    logger.debug(
                        "Resolution notification failed for task %s", task.id, exc_info=True
                    )
        return resumed

    def _resume_approved_task(self, task: Task, request_id: str) -> None:
        """Re-process a parked task whose HITL request was approved.

        Unless the approved command is flagged ``metacharacter_blocked``
        (GAP-016 / #70), the task is moved back to ``pending`` so the atomic
        claim re-acquires ownership, then re-run with ``preapproved=True`` so
        the previously gated step executes directly.

        When a suspended state file exists on disk (issue #42), the agent
        loop restores conversation history and continues from the parked
        iteration instead of starting over.
        """
        if self.hitl.is_metacharacter_blocked(request_id):
            logger.warning(
                "HITL approved an un-runnable command for task %s "
                "(shell metacharacters) — failing fast instead of retrying.",
                task.id,
            )
            self._complete_task(
                task,
                TaskStatus.FAILED,
                "HITL approval cannot be honored: the approved command contains "
                "shell metacharacters the executor cannot run (GAP-016). Rewrite "
                "the command as separate tool steps and re-dispatch.",
            )
            self.stats.tasks_failed += 1
            # Clean up suspended state for failed task.
            self._suspend_store.delete(task.id)
            return

        # Load suspended state for async resume (issue #42).
        resumed_state = self._suspend_store.load(task.id)

        logger.info(
            "HITL approved for task %s — resuming (suspended=%s).",
            task.id,
            resumed_state is not None,
        )
        resumed = self.bus.resume_task(task.id, "waiting_approval")
        if resumed is None:
            logger.warning(
                "Task %s could not be resumed — another executor already "
                "claimed it (CAS guard, ADR-015). Skipping.",
                task.id,
            )
            self._suspend_store.delete(task.id)
            return
        self._process_task(task, preapproved=True, resumed_state=resumed_state)

        # Clean up suspended state after successful resume.
        self._suspend_store.delete(task.id)

        # Fire resolution notification (issue #42).
        try:
            self._notifier.notify_resolved(
                request_id=request_id,
                task_id=task.id,
                decision="approved",
            )
        except Exception:  # noqa: BLE001 - notification must not block
            logger.debug("Resolution notification failed for task %s", task.id, exc_info=True)

    def _park_task(
        self,
        task: Task,
        parked: HITLParked,
        *,
        suspend_state: SuspendedState | None = None,
    ) -> None:
        """Park a task in WAITING_APPROVAL and record its HITL request id.

        The task is transitioned to ``waiting_approval`` so the executor's
        ``tick()`` loop skips it on subsequent passes (``get_pending_tasks``
        only returns ``pending`` tasks) and continues with other work.  The
        original ``in_progress`` status is overwritten to ``waiting_approval``
        so it is not mistaken for an active task.

        When *suspend_state* is provided (issue #42), the agent loop state
        is persisted to disk so the task can resume from where it left off
        instead of re-executing from scratch.  An approval notification is
        also fired via WebSocket + optional webhook.
        """
        # Persist suspended state for async resume (issue #42).
        if suspend_state is not None:
            suspend_state.task_id = task.id
            try:
                self._suspend_store.save(task.id, suspend_state)
            except Exception:  # noqa: BLE001 - suspend must not block parking
                logger.exception(
                    "Failed to save suspended state for task %s; task will resume from scratch",
                    task.id,
                )

        self._pending_approvals[task.id] = parked.request_id
        self._persist_pending_approvals()
        self.bus.update_task_status(task.id, TaskStatus.WAITING_APPROVAL.value)
        log_task_status(
            task.id,
            task.receiver_id,
            TaskStatus.IN_PROGRESS.value,
            TaskStatus.WAITING_APPROVAL.value,
        )

        # Fire approval notification (issue #42): WebSocket broadcast +
        # optional webhook POST.  Best-effort; never blocks parking.
        try:
            self._notifier.notify_parked(
                request_id=parked.request_id,
                task_id=task.id,
                agent_id=task.receiver_id,
                tool=parked.tool,
                description=f"Tier {parked.tier} approval needed for {parked.tool}",
                tier=parked.tier,
            )
        except Exception:  # noqa: BLE001 - notification must not block parking
            logger.debug("Approval notification failed for task %s", task.id, exc_info=True)

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

        Also fans out to the LearningCollector for continuous learning.
        """
        from ai_company.dashboard.ws import make_message_bus_broadcast_callback

        dashboard_cb = make_message_bus_broadcast_callback()

        # Learning collector fan-out (best-effort, never breaks dashboard)
        try:
            from ai_company.memory.learning_collector import LearningCollector

            _collector = LearningCollector()

            def _combined_callback(task_dict: dict[str, Any], event: str) -> None:
                # Dashboard broadcast (original behavior)
                if dashboard_cb is not None:
                    dashboard_cb(task_dict, event)
                # Learning capture (new behavior)
                _collector.on_task_event(task_dict, event)

            return _combined_callback
        except Exception:  # noqa: BLE001 - learning is optional, dashboard is primary
            return dashboard_cb

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

    def _process_task(
        self,
        task: Task,
        *,
        preapproved: bool = False,
        resumed_state: SuspendedState | None = None,
    ) -> None:
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
            resumed_state: Optional ``SuspendedState`` from a previous park.
                When provided the agent loop restores conversation history
                and continues from the parked iteration (issue #42).
        """
        # Bridge correlation ID to OTel trace context (T7 / issue #40).
        set_correlation_id_from_task(task.id)
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
            recalled_memories: list[dict[str, Any]] = []
            try:
                recalled_memories = recall_context(task.instruction, limit=5)
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
            # agent_loop.run() re-wraps the instruction with priority framing,
            # so the raw instruction is passed here (T026: fixes a double-wrap
            # where the task text was embedded twice).
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
                    resumed_state=resumed_state,
                    memories=recalled_memories,
                )
            except HITLParked as exc:
                # GAP-004: a HITL-gated step raised HITLParked — park the task
                # and continue to the next one instead of blocking on approval.
                # Capture the agent loop's state for suspension (issue #42).
                suspend_state = self.agent_loop._park_state
                self._park_task(task, exc, suspend_state=suspend_state)
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
                if record.tool in ("delegate", "task") and record.status == "ok":
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

            # 6b. Extract post-task knowledge (semantic + procedural)
            #     Heuristic-based, zero LLM cost. Failure must not abort task.
            try:
                extract_post_task_knowledge(
                    task_id=task.id,
                    agent_id=task.receiver_id,
                    instruction=task.instruction,
                    status="completed" if result.done and not result.error else "failed",
                    result_summary=result.final_response or "",
                    tool_results=result.tool_results,
                )
            except Exception:  # noqa: BLE001 - extraction is best-effort
                logger.debug("Post-task extraction failed for task %s", task.id, exc_info=True)

            # 7. Mark completed, timed out, or failed
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
            elif getattr(result, "timed_out", False):
                # O7: max-iterations exhaustion is a distinct outcome from a
                # hard failure — persist TIMEOUT so dashboards/operators can
                # distinguish the iteration cap being hit from a real error.
                error_msg = result.error or "Loop did not complete"
                self._complete_task(task, TaskStatus.TIMEOUT, error_msg)
                self.stats.tasks_failed += 1
                record_task_outcome(
                    task_id=task.id,
                    agent_id=task.receiver_id,
                    instruction=task.instruction,
                    status="timeout",
                    result_summary=error_msg,
                    tools_used=[r.tool for r in result.tool_results if r.tool],
                )
                logger.error("  TIMEOUT: %s", error_msg[:80])
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

            # 8. Record continuous-learning metrics (best-effort)
            try:
                status_str = (
                    "completed"
                    if result.done and not result.error
                    else ("timeout" if getattr(result, "timed_out", False) else "failed")
                )
                metrics = TaskMetrics(
                    task_id=task.id,
                    agent_id=task.receiver_id,
                    status=status_str,
                    iterations=result.iterations,
                    total_tokens=result.total_tokens,
                    total_cost_usd=result.total_cost_usd,
                    memory_recall_count=len(recalled_memories),
                    memory_avg_similarity=(
                        sum(m.get("similarity", 0) for m in recalled_memories)
                        / len(recalled_memories)
                        if recalled_memories
                        else 0.0
                    ),
                    tool_names=[r.tool for r in result.tool_results if r.tool],
                )
                self._metrics_collector.record_task(metrics)
                self._task_metrics_buffer.append(metrics)
            except Exception:  # noqa: BLE001 - metrics are best-effort
                logger.debug("Metrics recording failed for task %s", task.id, exc_info=True)
        finally:
            stop_heartbeat.set()
            detach_task_context(task.id)

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
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        FileStore(task_dir, backup=False).write_json("loop_result.json", log_data)

    def _create_subtask_from_record(self, parent_task: Task, record: Any) -> None:
        """Create a subtask from a ToolCallRecord with the task/delegate tool."""
        result_data = record.result
        receiver = result_data.get("receiver", "")
        instruction = result_data.get("instruction", "")
        if not receiver or not instruction:
            return

        child_task_id = str(uuid.uuid4())

        # Fix parent→child linkage (T7 / issue #40): subtask inherits
        # the parent's OTel trace context so the trace tree is unbroken.
        with subtask_context(parent_task.id, child_task_id):
            subtask = Task(
                id=child_task_id,
                sender_id=parent_task.receiver_id,
                receiver_id=receiver,
                instruction=instruction,
                priority=TaskPriority.MEDIUM,
            )
            self.bus.send_task(subtask)
            logger.info("  Delegated subtask to %s", receiver)
