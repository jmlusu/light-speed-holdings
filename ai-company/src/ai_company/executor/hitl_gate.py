"""Human-in-the-Loop gate — wraps ApprovalGate for tool execution."""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timedelta
from typing import Any

from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus


class HITLGate:
    """Requests human approval for dangerous tool operations.

    Creates an ApprovalRequest via the existing ApprovalGate, then polls
    via a background thread until the request is approved, rejected, or
    times out. The calling thread blocks on a threading.Event with timeout
    so it can be interrupted (unlike time.sleep).
    """

    def __init__(
        self,
        approval_gate: ApprovalGate | None = None,
        poll_interval: float = 2.0,
        timeout_minutes: int = 30,
    ) -> None:
        self.gate = approval_gate or ApprovalGate()
        self.poll_interval = poll_interval
        self.timeout_minutes = timeout_minutes
        self._events: dict[str, threading.Event] = {}
        self._results: dict[str, bool] = {}
        self._lock = threading.Lock()

    def request_and_wait(
        self,
        task_id: str,
        agent_id: str,
        tool: str,
        args: dict[str, Any],
    ) -> bool:
        """Create an approval request and wait for human decision.

        Returns True if approved, False if rejected or timed out.
        """
        request_id = f"hitl-{uuid.uuid4().hex[:12]}"
        description = _format_description(tool, args)

        self.gate.request_approval(
            request_id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action=f"tool:{tool}",
            description=description,
            expires_in_minutes=self.timeout_minutes,
        )

        event = threading.Event()
        with self._lock:
            self._events[request_id] = event

        # Background daemon polls for approval status
        poller = threading.Thread(
            target=self._poll_request,
            args=(request_id, event),
            daemon=True,
        )
        poller.start()

        # Wait on event with timeout — doesn't hold the executor event loop
        event.wait(timeout=self.timeout_minutes * 60)

        # Cleanup
        with self._lock:
            self._events.pop(request_id, None)
            result = self._results.pop(request_id, False)

        return result

    def _poll_request(self, request_id: str, event: threading.Event) -> None:
        """Background thread: poll gate until resolved or deadline."""
        deadline = datetime.now() + timedelta(minutes=self.timeout_minutes)
        while datetime.now() < deadline and not event.is_set():
            req = self.gate.get_request(request_id)
            if req and req.status != ApprovalStatus.PENDING:
                with self._lock:
                    self._results[request_id] = req.status == ApprovalStatus.APPROVED
                event.set()
                return
            event.wait(timeout=self.poll_interval)

        # Timed out
        if not event.is_set():
            with self._lock:
                self._results[request_id] = False
            event.set()

    def cancel(self, request_id: str) -> None:
        """Cancel a pending wait without waiting for timeout."""
        with self._lock:
            event = self._events.get(request_id)
            if event:
                self._results[request_id] = False
                event.set()


def _format_description(tool: str, args: dict[str, Any]) -> str:
    """Format a human-readable description of the tool operation for approval."""
    if tool == "write":
        path = args.get("path", "unknown")
        content_len = len(args.get("content", ""))
        return f"Write {content_len} chars to {path}"
    elif tool == "execute":
        return f"Execute: {args.get('command', 'unknown')}"
    elif tool == "code_interpreter":
        code_preview = args.get("code", "")[:200]
        return f"Run Python code: {code_preview}..."
    else:
        return f"{tool}: {json.dumps(args, indent=2)}"
