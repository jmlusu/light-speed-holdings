"""Human-in-the-Loop gate -- wraps ApprovalGate for tool execution.

GAP-004 fix:
- ``request_and_wait()`` returns a ``concurrent.futures.Future`` that
  resolves when the human approves or rejects the request.  Callers can
  either block on the future (with a timeout) or attach a callback for
  fully non-blocking usage.

- ``request_and_wait_sync()`` is a convenience wrapper that blocks the
  calling thread on the future (useful for the executor's synchronous
  ``tick()`` path).

- ``resolve_approved()`` provides a poll-and-resume mechanism: it checks
  whether any pending request has been approved or rejected since the last
  check, resolving the corresponding future without blocking.  This is
  used by the executor's non-blocking tick loop.

GAP-016 / ticket #70 fix:
- When a bash/execute command contains shell metacharacters, the request is
  flagged ``metacharacter_blocked`` and its description carries a warning so
  the human never approves a command the executor can never run.  The resume
  path uses :meth:`HITLGate.is_metacharacter_blocked` to fail such approved
  tasks fast instead of silently retrying them.
"""

from __future__ import annotations

import concurrent.futures
import json
import logging
import threading
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus
from ai_company.security.command_safety import find_shell_metacharacters

logger = logging.getLogger(__name__)

# GAP-016 / ticket #70: warning appended to the approval description when the
# pending bash/execute command contains shell metacharacters. The human sees
# this in the dashboard approvals list and the CLI approval pending view.
_METACHARACTER_WARNING = (
    " [BLOCKED] This command contains shell metacharacters ({meta}) that the "
    "executor rejects (GAP-016). Approving WILL NOT make it run — the task "
    "will fail fast. Rewrite the command as separate tool steps and re-dispatch."
)

# Module-level executor for background polling threads
_poll_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=4, thread_name_prefix="hitl-poll"
)


class HITLGate:
    """Requests human approval for dangerous tool operations.

    Creates an ApprovalRequest via the existing ApprovalGate, then polls
    via a background thread until the request is approved, rejected, or
    times out.  The result is delivered through a ``Future``.

    Args:
        approval_gate: The underlying approval gate.
        poll_interval: Seconds between polls of the approval status.
        timeout_minutes: Maximum time to wait for a human decision.
    """

    def __init__(
        self,
        approval_gate: ApprovalGate | None = None,
        poll_interval: float = 2.0,
        timeout_minutes: int = 30,
    ) -> None:
        self.gate = approval_gate or ApprovalGate.get_instance()
        self.poll_interval = poll_interval
        self.timeout_minutes = timeout_minutes
        self._futures: dict[str, concurrent.futures.Future[bool]] = {}
        self._lock = threading.Lock()
        # Tracks request_id -> (task_id, tool) for pending non-blocking requests
        self._pending_requests: dict[str, tuple[str, str]] = {}

    def request_and_wait(
        self,
        task_id: str,
        agent_id: str,
        tool: str,
        args: dict[str, Any],
    ) -> concurrent.futures.Future[bool]:
        """Create an approval request and return a Future for the result.

        The Future resolves to ``True`` if approved, ``False`` if rejected
        or timed out.  A background thread polls the approval gate and
        resolves the future when a decision is made.

        Callers may:
        - ``future.result(timeout=...)`` to block with a timeout.
        - ``future.add_done_callback(fn)`` for fully non-blocking use.
        """
        request_id = f"hitl-{uuid.uuid4().hex[:12]}"
        description = _format_description(tool, args)
        # GAP-016 / ticket #70: surface un-runnable commands to the human at
        # approval time instead of approving work the executor can never run.
        blocked_meta = _command_metacharacters(tool, args)
        if blocked_meta:
            description += _METACHARACTER_WARNING.format(meta=", ".join(blocked_meta))
            logger.warning(
                "HITL request %s for task %s requests an un-runnable command "
                "(shell metacharacters: %s) — flagged and warned at approval time",
                request_id,
                task_id,
                ", ".join(blocked_meta),
            )

        self.gate.request_approval(
            request_id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=f"tool:{tool}",
            description=description,
            expires_in_minutes=self.timeout_minutes,
            metacharacter_blocked=bool(blocked_meta),
        )

        future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        with self._lock:
            self._futures[request_id] = future
            self._pending_requests[request_id] = (task_id, tool)

        # Submit the polling work to a background thread pool
        _poll_executor.submit(self._poll_request, request_id, future)

        logger.info(
            "HITL request %s created for task %s tool %s (timeout=%dm)",
            request_id,
            task_id,
            tool,
            self.timeout_minutes,
        )
        return future

    def request_and_wait_sync(
        self,
        task_id: str,
        agent_id: str,
        tool: str,
        args: dict[str, Any],
    ) -> bool:
        """Blocking convenience wrapper around ``request_and_wait()``.

        Returns True if approved, False if rejected or timed out.
        """
        future = self.request_and_wait(task_id, agent_id, tool, args)
        try:
            return future.result(timeout=self.timeout_minutes * 60)
        except concurrent.futures.TimeoutError:
            logger.warning("HITL request timed out for task %s", task_id)
            return False
        except Exception:
            logger.exception("HITL request failed for task %s", task_id)
            return False

    def request_and_park(
        self,
        task_id: str,
        agent_id: str,
        tool: str,
        args: dict[str, Any],
    ) -> str:
        """Create an approval request WITHOUT blocking (GAP-004).

        This is the non-blocking counterpart used by the executor so it can
        park a task and move on to the next one while the human decides.
        It registers the request with the SAME underlying ``ApprovalGate``
        hook that tier enforcement (GAP-003) and the blocking
        ``request_and_wait`` paths use — no separate gate is created.

        Returns the ``request_id`` so the caller can later resume via
        :meth:`resume_approved`.
        """
        request_id = f"hitl-{uuid.uuid4().hex[:12]}"
        description = _format_description(tool, args)
        # GAP-016 / ticket #70: surface un-runnable commands to the human at
        # approval time instead of approving work the executor can never run.
        blocked_meta = _command_metacharacters(tool, args)
        if blocked_meta:
            description += _METACHARACTER_WARNING.format(meta=", ".join(blocked_meta))
            logger.warning(
                "HITL request %s parked for task %s with an un-runnable command "
                "(shell metacharacters: %s) — flagged and warned at approval time",
                request_id,
                task_id,
                ", ".join(blocked_meta),
            )

        self.gate.request_approval(
            request_id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=f"tool:{tool}",
            description=description,
            expires_in_minutes=self.timeout_minutes,
            metacharacter_blocked=bool(blocked_meta),
        )

        with self._lock:
            self._pending_requests[request_id] = (task_id, tool)

        logger.info(
            "HITL request %s parked for task %s tool %s (timeout=%dm)",
            request_id,
            task_id,
            tool,
            self.timeout_minutes,
        )
        # GAP-008: persist the escalation/park decision to the audit trail.
        _audit_hitl(task_id=task_id, agent_id=agent_id, tool=tool, approved=None)
        return request_id

    def resume_approved(self, request_id: str) -> bool | None:
        """Check a parked request's decision without blocking (GAP-004).

        The decision is read from the persisted approval store (reloaded
        from disk first), NOT from the in-memory ``_pending_requests`` map,
        so a request parked by a previous executor process can still be
        resumed after a restart — the ``_pending_requests`` map is empty in
        a fresh process and cannot be the source of truth.

        Returns:
            ``True`` if approved, ``False`` if rejected or expired,
            ``None`` if still pending or the request id is unknown.  Does
            NOT resolve a future (parked requests have none); it simply
            reports the current decision so the executor can resume or
            leave the task parked.
        """
        with self._lock:
            tracked = request_id in self._pending_requests
        # Reload from disk first so a decision written by another process
        # (e.g. the CLI operator, or the daemon's governance sweep marking
        # this request EXPIRED) is observed instead of stale in-memory state.
        self.gate.reload()
        req = self.gate.get_request(request_id)
        if req is None:
            # No longer in the store. If we created it this process (the
            # store was reset/rotated underneath us) treat it as failed;
            # otherwise the id is unknown so leave the task parked.
            return False if tracked else None
        if req.status == ApprovalStatus.APPROVED:
            with self._lock:
                self._pending_requests.pop(request_id, None)
            return True
        if req.status == ApprovalStatus.REJECTED:
            with self._lock:
                self._pending_requests.pop(request_id, None)
            return False
        if req.expires_at and req.expires_at < datetime.now(timezone.utc):
            with self._lock:
                self._pending_requests.pop(request_id, None)
            return False
        return None

    def is_metacharacter_blocked(self, request_id: str) -> bool:
        """True when the request's tool call can never pass the executor's
        shell-metacharacter filter (GAP-016 / ticket #70).

        Reads the persisted flag (reloading from disk first, mirroring
        :meth:`resume_approved`) so a decision written by another process is
        observed.  Returns ``False`` for unknown requests — an absent flag on
        legacy records is treated as "not flagged" so old approvals keep
        their existing resume behaviour.
        """
        self.gate.reload()
        req = self.gate.get_request(request_id)
        if req is None:
            return False
        return bool(req.metacharacter_blocked)

    def _poll_request(
        self,
        request_id: str,
        future: concurrent.futures.Future[bool],
    ) -> None:
        """Background thread: poll gate until resolved or deadline."""
        # Use UTC for deadline to handle timezone-aware expires_at consistently
        from datetime import timezone

        deadline = datetime.now(timezone.utc) + timedelta(minutes=self.timeout_minutes)

        while datetime.now(timezone.utc) < deadline:
            if future.cancelled():
                return

            # Reload from disk so an external decision (approval/rejection
            # or the daemon's EXPIRED sweep) is seen instead of stale memory.
            self.gate.reload()
            req = self.gate.get_request(request_id)
            if req and req.status != ApprovalStatus.PENDING:
                approved = req.status == ApprovalStatus.APPROVED
                self._resolve(request_id, approved)
                return

            # Sleep in short intervals so we can react to cancellation
            _interruptible_sleep(self.poll_interval, future)

        # Timed out
        if not future.done():
            self._resolve(request_id, False)

    def _resolve(self, request_id: str, approved: bool) -> None:
        """Resolve the future for a request and clean up."""
        with self._lock:
            future = self._futures.pop(request_id, None)
            task_tool = self._pending_requests.pop(request_id, None)
        # GAP-008: persist the human decision to the audit trail.
        if task_tool is not None:
            _audit_hitl(task_id=task_tool[0], agent_id="", tool=task_tool[1], approved=approved)
        if future and not future.done():
            future.set_result(approved)

    def cancel(self, request_id: str) -> None:
        """Cancel a pending wait."""
        with self._lock:
            future = self._futures.pop(request_id, None)
            self._pending_requests.pop(request_id, None)
        if future and not future.done():
            future.set_result(False)

    def resolve_approved(self, request_id: str) -> bool | None:
        """Poll the gate for a single request and resolve its future if done.

        Returns:
            ``True`` if approved, ``False`` if rejected or timed out,
            ``None`` if still pending.  Safe to call multiple times.
        """
        future: concurrent.futures.Future[bool] | None
        with self._lock:
            future = self._futures.get(request_id)
            if future is None or future.done():
                return None

        # Reload from disk so a decision persisted by the daemon (e.g. an
        # EXPIRED sweep) is observed instead of stale in-memory state.
        self.gate.reload()
        req = self.gate.get_request(request_id)
        if req is None:
            self._resolve(request_id, False)
            return False

        if req.status == ApprovalStatus.APPROVED:
            self._resolve(request_id, True)
            return True
        elif req.status == ApprovalStatus.REJECTED:
            self._resolve(request_id, False)
            return False
        elif req.expires_at:
            # Handle both naive and aware datetimes for comparison
            now = datetime.now()
            if req.expires_at.tzinfo is not None:
                from datetime import timezone

                now = now.replace(tzinfo=timezone.utc)
            if req.expires_at < now:
                self._resolve(request_id, False)
                return False

        return None

    def resolve_all_pending(self) -> dict[str, bool]:
        """Poll all pending non-blocking requests and resolve any that are done.

        Returns a dict of ``{request_id: approved}`` for requests that were
        resolved during this call.  Requests still pending are not included.
        """
        resolved: dict[str, bool] = {}
        with self._lock:
            request_ids = list(self._pending_requests.keys())

        for request_id in request_ids:
            result = self.resolve_approved(request_id)
            if result is not None:
                resolved[request_id] = result
        return resolved

    def has_pending_requests(self) -> bool:
        """Return True if there are any non-blocking requests awaiting resolution."""
        with self._lock:
            return bool(self._pending_requests)


def _format_description(tool: str, args: dict[str, Any]) -> str:
    """Format a human-readable description of the tool operation for approval."""
    if tool in ("write", "edit"):
        path = args.get("path", "unknown")
        content_len = len(args.get("content", ""))
        return f"Write {content_len} chars to {path}"
    elif tool in ("execute", "bash"):
        return f"Execute: {args.get('command', 'unknown')}"
    elif tool in ("webfetch", "web_search", "websearch"):
        return f"Fetch: {args.get('url', 'unknown')}"
    else:
        return f"{tool}: {json.dumps(args, indent=2)}"


def _command_metacharacters(tool: str, args: dict[str, Any]) -> list[str]:
    """Return the shell metacharacters present in a bash/execute command.

    Returns ``[]`` for non-command tools or when no command string is
    present.  Uses the same detection as ``ToolRunner._execute``
    (``security.command_safety``) so approval-time flags and execution-time
    rejection can never disagree.
    """
    if tool not in ("execute", "bash"):
        return []
    command = args.get("command", "")
    if not isinstance(command, str):
        return []
    return find_shell_metacharacters(command)


def _interruptible_sleep(seconds: float, future: concurrent.futures.Future[bool]) -> None:
    """Sleep for *seconds* but wake early if *future* is cancelled."""
    import time

    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if future.cancelled():
            return
        time.sleep(0.25)


def _audit_hitl(
    task_id: str,
    agent_id: str,
    tool: str,
    approved: bool | None = None,
) -> None:
    """Best-effort audit hook for an HITL/escalation decision (GAP-008).

    Imported lazily and wrapped in try/except so a failure in the audit
    subsystem can never break the approval flow itself.
    """
    try:
        from ai_company.audit.integration import log_hitl_decision

        log_hitl_decision(
            task_id=task_id,
            agent_id=agent_id,
            tool=tool,
            approved=approved,
        )
    except Exception:  # pragma: no cover - defensive
        logger.debug("audit hook skipped for HITL decision", exc_info=True)
