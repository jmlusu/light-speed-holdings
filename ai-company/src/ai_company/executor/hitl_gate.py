"""Human-in-the-Loop gate — wraps ApprovalGate for tool execution."""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Any

from ai_company.orchestrator.approval import ApprovalGate, ApprovalStatus


class HITLGate:
    """Requests human approval for dangerous tool operations.

    Creates an ApprovalRequest via the existing ApprovalGate, then polls
    until the request is approved, rejected, or times out.
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

        # Poll until resolved or expired
        deadline = datetime.now() + timedelta(minutes=self.timeout_minutes)
        while datetime.now() < deadline:
            req = self.gate.get_request(request_id)
            if req and req.status != ApprovalStatus.PENDING:
                return req.status == ApprovalStatus.APPROVED
            time.sleep(self.poll_interval)

        return False  # Timed out → denied


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
