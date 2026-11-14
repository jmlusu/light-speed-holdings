"""Sandboxed tool execution engine.

Security hardening (GAP-016):
- Commands are parsed with ``shlex.split()`` instead of ``shell=True``.
- Only allowlisted command prefixes may execute.
- ``shell=True`` is never used; shell features (pipes, redirects) are blocked
  and should be expressed as separate tool steps.
- Metacharacter detection is shared with the HITL gate
  (``security.command_safety``) so un-runnable commands are flagged at
  approval time (ticket #70).
- Allowlist is configurable via YAML file (config/tool_allowlist.yaml).
- Rejected commands are logged for security auditing.
- Path sandboxing resolves symlinks to prevent traversal attacks.
- Tool outputs are scanned for content safety threats and PII before
  being returned to the caller (GAP-016 extension).

GAP-003 fix (tier rules integration):
- Before each tool execution, ``check_tier_rules()`` classifies the action
  using ``orchestrator.tier_rules.classify_tool_action()``.
- Tier 0 (auto): execute immediately.
- Tier 1 (notify): execute and log the notification.
- Tier 2 (single approver): HITL unless agent seniority >= threshold.
- Tier 3 (two-person) and Tier 4 (CEO only): always require HITL.
"""

from __future__ import annotations

import contextlib
import logging
import os
import shlex
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

from ai_company.audit.integration import log_hitl_decision, log_tool_call
from ai_company.executor.hitl_gate import HITLGate
from ai_company.executor.ps_linter import check_powershell_command
from ai_company.executor.read_cache import SessionReadCache
from ai_company.executor.tool_validation import (
    GREP_MATCH_CAP as _GREP_MATCH_CAP,
)
from ai_company.executor.tool_validation import (
    call_with_retry,
    cap_grep_line,
    check_edit_preflight,
    classify_tool_error,
    depth_limit_fallback,
    grep_backend,
    resolve_file_path_arg,
    truncate_to_cap,
    validate_tool_args,
)
from ai_company.orchestrator.tier_rules import (
    SENIORITY_AUTO_APPROVE_TIER,
    ApprovalTier,
    classify_tool_action,
    get_tier_config,
)
from ai_company.security.command_safety import find_shell_metacharacters
from ai_company.security.content_filter import ContentFilter, get_content_filter
from ai_company.security.egress import check_shell_egress, validate_egress_url
from ai_company.security.path_policy import deny_reason, find_denied_paths_in_command
from ai_company.security.pii_detector import PIIDetector, get_pii_detector
from ai_company.security.redact import redact_secrets
from ai_company.store import repo_write


def log_permission_deny(
    task_id: str,
    agent_id: str,
    tool: str,
    args: Any,
    *,
    reason: str = "permission_denied",
) -> None:
    """Best-effort PERMISSION_DENIED audit + security log for deny paths.

    Tests patch ``tool_runner.log_permission_deny`` to assert the audit
    hook fires on path-escape and allowlist/content deny. Kept module-
    level (single import point) so the mock target is stable.
    """
    _security_logger.warning(
        "PERMISSION_DENIED %s %s: %s (reason=%s)", task_id, agent_id, tool, reason
    )
    try:
        log_tool_call(
            task_id,
            agent_id,
            tool,
            args if isinstance(args, dict) else {"raw": str(args)},
            {"status": "error", "error": f"permission denied: {reason}"},
        )
    except Exception:  # noqa: BLE001 - audit must never crash dispatch
        return


try:
    from ai_company.telemetry import start_span as _start_span
except ImportError:  # pragma: no cover — OTel optional

    @contextlib.contextmanager
    def _start_span(_name: str, **_kwargs: object) -> Iterator[None]:  # type: ignore
        yield


logger = logging.getLogger(__name__)

# Security audit logger — separate from application logs
_security_logger = logging.getLogger("ai_company.security.tool_runner")

# Canonical runtime tool vocabulary (matches executor/context.py card parsing).
# Legacy names (write, execute, delegate, web_search) are accepted as
# backward-compatible aliases that dispatch to the same handler.
_CANONICAL_TOOLS: frozenset[str] = frozenset(
    {"read", "edit", "grep", "list", "bash", "webfetch", "task"}
)

_TOOL_ALIASES: dict[str, str] = {
    "write": "edit",
    "execute": "bash",
    "delegate": "task",
    "web_search": "webfetch",
    "websearch": "webfetch",
}


class SecurityError(Exception):
    """Raised when a tool tries to escape the project sandbox."""


class HITLParked(Exception):
    """Raised by :meth:`ToolRunner.run_plan` when a step needs HITL and the
    caller requested non-blocking behaviour (GAP-004).

    The executor catches this, transitions the task to ``WAITING_APPROVAL``,
    and continues to the next task.  The human decision is later checked via
    :meth:`HITLGate.resume_approved` using ``request_id``.
    """

    def __init__(
        self,
        task_id: str,
        agent_id: str,
        tool: str,
        request_id: str,
        tier: int,
    ) -> None:
        self.task_id = task_id
        self.agent_id = agent_id
        self.tool = tool
        self.request_id = request_id
        self.tier = tier
        super().__init__(
            f"Task {task_id} parked for HITL approval of {tool} (request {request_id}, tier {tier})"
        )


# ---------------------------------------------------------------------------
# Command allowlist — loaded from YAML config with hardcoded fallback.
# Only these base commands may be executed via the ``execute`` tool.
# ---------------------------------------------------------------------------
_DEFAULT_ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        # Media generation (ComfyUI MCP — ADR-018)
        "comfyui-mcp",
        "comfyui",
        # Build / test
        "python",
        "python3",
        "pip",
        "pytest",
        "ruff",
        "mypy",
        "black",
        "isort",
        # Version control
        "git",
        # File inspection
        "ls",
        "cat",
        "head",
        "tail",
        "wc",
        "grep",
        "rg",
        "find",
        "tree",
        # Text processing (standalone — pipes blocked)
        "sort",
        "uniq",
        "diff",
        "echo",
        # Package / env
        "npm",
        "node",
        "npx",
        # Misc safe ops
        "mkdir",
        "cp",
        "mv",
        "touch",
        "date",
        "env",
        "which",
        "pwd",
    }
)


def _load_allowlist(config_path: str | Path | None = None) -> frozenset[str]:
    """Load the command allowlist from YAML config, falling back to defaults."""
    if config_path is None:
        # Look for config relative to project root
        candidates = [
            Path("config/tool_allowlist.yaml"),
        ]
        for candidate in candidates:
            if candidate.exists():
                config_path = candidate
                break

    if config_path is not None:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            commands = data.get("allowed_commands", [])
            if commands:
                logger.info(
                    "Loaded tool allowlist from %s (%d commands)", config_path, len(commands)
                )
                return frozenset(commands)
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to load allowlist from %s: %s — using defaults", config_path, exc
            )

    return _DEFAULT_ALLOWED_COMMANDS


class ToolRunner:
    """Executes tool plan steps from the LLM response.

    All file operations are restricted to PROJECT_ROOT.
    Approval is determined by the tier system (tier_rules.classify_tool_action)
    rather than a hardcoded tool list.

    Security (GAP-016 extension):
    - All tool outputs are scanned for content safety threats via
      :class:`ContentFilter` and PII via :class:`PIIDetector`.
    - Threats are logged and dangerous content is replaced with a
      placeholder before being returned.
    """

    def __init__(
        self,
        project_root: str | Path = ".",
        allowlist_path: str | Path | None = None,
        content_filter: ContentFilter | None = None,
        pii_detector: PIIDetector | None = None,
    ) -> None:
        import time as _time

        self.project_root = Path(project_root).resolve()
        self.allowed_commands = _load_allowlist(allowlist_path)
        self._content_filter = content_filter or get_content_filter()
        self._pii_detector = pii_detector or get_pii_detector()
        # Injectable sleep for webfetch retry backoff (tests patch it).
        self._sleep = _time.sleep
        # Per-session read-dedup pointer cache (executor canonical;
        # llm/hot_file_cache is the content LRU for injection, not this).
        self._read_cache = SessionReadCache()
        self._read_step = 0

    def run_plan(
        self,
        plan: list[dict[str, Any]],
        hitl_gate: HITLGate | None = None,
        task_id: str = "",
        agent_id: str = "",
        session_id: str = "",
        seniority: str = "",
        risk_level: str = "",
        *,
        non_blocking: bool = False,
        preapproved: bool = False,
    ) -> list[dict[str, Any]]:
        """Execute each step in the plan with tier-based approval gating.

        For each tool step, ``check_tier_rules()`` classifies the action into
        an approval tier.  The tier determines whether the step can execute
        immediately, requires HITL approval, or is outright denied.

        Args:
            non_blocking: GAP-004 — when a gated step needs HITL, raise
                :class:`HITLParked` (carrying the request id) instead of
                blocking the caller.  The executor parks the task and moves on.
            preapproved: GAP-004 — when True, a step that would normally
                require HITL executes directly (used by the executor's resume
                path after the human approved the parked request).

        Returns a list of step results. Each result dict contains at minimum:
        ``step``, ``tool``, ``status``, and ``tier`` keys.
        """
        results: list[dict[str, Any]] = []
        blocking = hitl_gate is not None

        with _start_span(
            "tool.execute",
            attributes={
                "task_id": task_id,
                "agent_id": agent_id,
                "steps": len(plan) if isinstance(plan, list) else 0,
                "seniority": seniority,
                "risk_level": risk_level,
            },
        ):
            # GAP-019: LLM output is untyped — a malformed plan (a bare string
            # instead of a list of tool steps) must not crash the loop.  Surface
            # it as an error result so the model can self-correct on the next
            # iteration instead of raising ``'str' object has no attribute 'get'``.
            if not isinstance(plan, list):
                malformed_plan = {
                    "step": 0,
                    "tool": "plan",
                    "status": "error",
                    "error": (
                        "Malformed plan: expected a list of tool steps, "
                        f"got {type(plan).__name__}. Respond with a JSON array of "
                        '{"tool": ..., "args": {...}} steps.'
                    ),
                }
                results.append(malformed_plan)
                log_tool_call(task_id, agent_id, "plan", {}, malformed_plan)
                return results

            for i, step in enumerate(plan):
                if not isinstance(step, dict):
                    malformed_step = {
                        "step": i,
                        "tool": "plan",
                        "status": "error",
                        "error": (
                            f"Malformed step at index {i}: expected a dict, "
                            f"got {type(step).__name__}. Respond with a JSON array "
                            'of {"tool": ..., "args": {...}} steps.'
                        ),
                    }
                    results.append(malformed_step)
                    log_tool_call(task_id, agent_id, "plan", {}, malformed_step)
                    continue

                tool = step.get("tool", "")
                args = step.get("args", {})

                # GAP-019 (extended): LLM output is untyped — a step whose
                # ``args`` is a bare string instead of a dict (e.g. the model
                # emitted a path directly) must not crash tier classification
                # with ``'str' object has no attribute 'values'``.  Surface it
                # as an error result so the model can self-correct.
                if not isinstance(args, dict):
                    malformed_args = {
                        "step": i,
                        "tool": tool,
                        "status": "error",
                        "error": (
                            "Malformed step: 'args' must be a JSON object, "
                            f"got {type(args).__name__}. Respond with "
                            '{"tool": ..., "args": {...}} steps.'
                        ),
                    }
                    results.append(malformed_args)
                    log_tool_call(task_id, agent_id, tool, args, malformed_args)
                    continue

                if tool not in self._all_tools():
                    error_result = {
                        "step": i,
                        "tool": tool,
                        "status": "error",
                        "error": f"Unknown tool: {tool}",
                    }
                    results.append(error_result)
                    log_tool_call(task_id, agent_id, tool, args, error_result)
                    continue

                # ── P1-T4 schema fail-fast (before tier/dispatch) ───────
                # Canonical entry is validate_tool_args; normalize the
                # harness filePath alias to path so handlers (which index
                # args["path"]) dispatch on the unified shape.
                _resolved_path = resolve_file_path_arg(args)
                if _resolved_path is not None and "path" not in args:
                    args = {**args, "path": _resolved_path}
                _valid, _validation_msg = validate_tool_args(tool, args)
                if not _valid:
                    validation_result = {
                        "step": i,
                        "tool": tool,
                        "status": "error",
                        "error": _validation_msg,
                        "validation_rejected": True,
                        "error_code": "VALIDATION_REJECTED",
                    }
                    results.append(validation_result)
                    log_tool_call(task_id, agent_id, tool, args, validation_result)
                    continue

                # ── GAP-003: Tier classification & authorization ─────────
                tier_info = self.check_tool_authorization(
                    tool_name=tool,
                    args=args,
                    agent_id=agent_id,
                    seniority=seniority,
                    risk_level=risk_level,
                    task_id=task_id,
                )
                tier = tier_info["tier"]
                needs_hitl = tier_info["needs_hitl"]
                tier_label = tier_info["tier_label"]

                # ── HITL approval path ───────────────────────────────────
                if needs_hitl and blocking and not preapproved:
                    assert hitl_gate is not None  # guaranteed by ``blocking``
                    if non_blocking:
                        # GAP-004: park instead of blocking.  Raise HITLParked so
                        # the executor can transition the task to WAITING_APPROVAL
                        # and continue to the next task.  The SAME shared
                        # ApprovalGate hook (ciso's GAP-003 tier enforcement) is
                        # used to create the request — no duplicate gate.
                        assert hitl_gate is not None  # guaranteed by ``blocking``
                        request_id = hitl_gate.request_and_park(
                            task_id=task_id,
                            agent_id=agent_id,
                            tool=tool,
                            args=args,
                        )
                        log_hitl_decision(task_id, agent_id, tool, None)
                        raise HITLParked(
                            task_id=task_id,
                            agent_id=agent_id,
                            tool=tool,
                            request_id=request_id,
                            tier=tier,
                        )
                    approved = hitl_gate.request_and_wait_sync(
                        task_id=task_id,
                        agent_id=agent_id,
                        tool=tool,
                        args=args,
                    )
                    log_hitl_decision(task_id, agent_id, tool, approved)
                    if not approved:
                        denied_result = {
                            "step": i,
                            "tool": tool,
                            "status": "denied",
                            "error": f"Human approval denied (tier: {tier_label})",
                            "tier": tier,
                        }
                        results.append(denied_result)
                        log_tool_call(task_id, agent_id, tool, args, denied_result)
                        continue

                elif needs_hitl and not blocking and not preapproved:
                    # ``blocking`` is False only when no hitl_gate was supplied.
                    # There is no gate to queue the approval with, so we cannot
                    # enforce the HITL requirement. The safest behaviour is to
                    # proceed with execution (the tier classification still records
                    # that HITL *would* have been required) and surface a warning.
                    # NOTE: when a gate *is* present this branch is never reached
                    # (it is handled by the ``needs_hitl and blocking`` path
                    # above), so the tier-classification security behaviour is
                    # fully preserved for production callers.
                    logger.warning(
                        "Tier %d (%s) requires HITL for %s by %s but no "
                        "hitl_gate was provided — executing without approval",
                        int(tier),
                        tier_label,
                        tool,
                        agent_id,
                    )

                # ── Execute the tool ──────────────────────────────────────
                try:
                    result = self._execute_tool(
                        tool,
                        args,
                        task_id=task_id,
                        agent_id=agent_id,
                        session_id=session_id,
                    )
                    # T-06 depth fallback: a deterministic depth-limit error
                    # becomes explicit direct execution (never retried).
                    if (
                        tool in ("task", "delegate")
                        and "error" in result
                        and classify_tool_error(str(result.get("error", ""))) == "DEPTH_LIMIT"
                    ):
                        fallback = depth_limit_fallback(
                            receiver=str(args.get("receiver", "")),
                            instruction=str(args.get("instruction", "")),
                            agent_id=agent_id,
                        )
                        result = {**fallback}
                    status = "error" if "error" in result else "ok"
                    exec_result = {
                        "step": i,
                        "tool": tool,
                        "status": status,
                        "tier": tier,
                        "tier_label": tier_label,
                        **result,
                    }
                    results.append(exec_result)
                    log_tool_call(task_id, agent_id, tool, args, exec_result)
                except Exception as exc:  # noqa: BLE001 - tool failure captured in result
                    # T-06 depth fallback (exception form of the limit).
                    if (
                        tool in ("task", "delegate")
                        and classify_tool_error(str(exc)) == "DEPTH_LIMIT"
                    ):
                        fallback_exc = depth_limit_fallback(
                            receiver=str(args.get("receiver", "")),
                            instruction=str(args.get("instruction", "")),
                            agent_id=agent_id,
                        )
                        exc_result = {
                            "step": i,
                            "tool": tool,
                            "status": "ok",
                            "tier": tier,
                            "tier_label": tier_label,
                            **fallback_exc,
                        }
                        results.append(exc_result)
                        log_tool_call(task_id, agent_id, tool, args, exc_result)
                        continue
                    exc_result = {
                        "step": i,
                        "tool": tool,
                        "status": "error",
                        "tier": tier,
                        "tier_label": tier_label,
                        "error": str(exc),
                    }
                    results.append(exc_result)
                    log_tool_call(task_id, agent_id, tool, args, exc_result)

        return results

    @staticmethod
    def check_tool_authorization(
        tool_name: str,
        args: dict[str, Any],
        agent_id: str = "",
        seniority: str = "",
        risk_level: str = "",
        task_id: str = "",
    ) -> dict[str, Any]:
        """Authorize a tool action against the 5-tier approval matrix.

        This is the GAP-003 enforcement entry point. It delegates tier
        classification to :meth:`check_tier_rules` (which is itself backed by
        ``orchestrator.tier_rules`` — the project's 5-tier approval matrix) and
        additionally enforces the *agent's authorized tier*: an agent whose
        seniority maps to a maximum auto-approve tier below the action's
        classified tier will always require HITL, regardless of context.

        Returns a dict with keys:
            ``tier`` (int), ``tier_label`` (str), ``needs_hitl`` (bool),
            ``description`` (str), ``authorized`` (bool).
        """
        tier_info = ToolRunner.check_tier_rules(
            tool_name=tool_name,
            args=args,
            agent_id=agent_id,
            seniority=seniority,
            risk_level=risk_level,
            task_id=task_id,
        )

        # The agent's authorized ceiling (highest tier it may auto-approve).
        max_auto = SENIORITY_AUTO_APPROVE_TIER.get(seniority, 0)
        authorized = int(tier_info["tier"]) <= max_auto

        # If the action exceeds the agent's authorized tier, force HITL.
        if not authorized and not tier_info["needs_hitl"]:
            tier_info["needs_hitl"] = True

        tier_info["authorized"] = authorized
        return tier_info

    @staticmethod
    def check_tier_rules(
        tool_name: str,
        args: dict[str, Any],
        agent_id: str = "",
        seniority: str = "",
        risk_level: str = "",
        task_id: str = "",
    ) -> dict[str, Any]:
        """Classify a tool action and determine if HITL approval is required.

        This is the GAP-003 integration point.  It wraps
        ``tier_rules.classify_tool_action()`` and maps the resulting
        ``ApprovalTier`` into an actionable decision:

        * Tier 0 (auto-approve): no HITL needed, execute immediately.
        * Tier 1 (notify): no HITL needed, execute and notify.
        * Tier 2 (single approver): HITL unless agent seniority is at or
          above the threshold in ``SENIORITY_AUTO_APPROVE_TIER``.
        * Tier 3 (two-person rule): always HITL.
        * Tier 4 (CEO only): always HITL.

        Returns a dict with keys:
            ``tier`` (int), ``tier_label`` (str), ``needs_hitl`` (bool),
            ``description`` (str).
        """
        context: dict[str, Any] = {}
        if seniority:
            context["seniority"] = seniority
        if risk_level:
            context["risk_level"] = risk_level

        tier = classify_tool_action(
            tool=tool_name,
            args=args,
            agent_id=agent_id,
            task_context=context if context else None,
        )
        tier_config = get_tier_config(tier)
        needs_hitl = tier_config["required_approvers"] > 0

        # Seniority can de-approve for Tier 2 if the agent has enough authority
        if tier == ApprovalTier.SINGLE_APPROVER and needs_hitl:
            max_auto = SENIORITY_AUTO_APPROVE_TIER.get(seniority, 0)
            if max_auto >= int(tier):
                needs_hitl = False

        result = {
            "tier": int(tier),
            "tier_label": tier_config["label"],
            "needs_hitl": needs_hitl,
            "description": tier_config["description"],
        }

        if needs_hitl:
            logger.info(
                "Tier %d (%s) — HITL required for %s by %s",
                int(tier),
                tier_config["label"],
                tool_name,
                agent_id,
            )
        elif int(tier) >= 1:
            logger.info(
                "Tier %d (%s) — %s auto-approved for %s",
                int(tier),
                tier_config["label"],
                tool_name,
                agent_id,
            )

        return result

    def _execute_tool(
        self,
        tool: str,
        args: dict[str, Any],
        *,
        task_id: str = "",
        agent_id: str = "",
        session_id: str = "",
    ) -> dict[str, Any]:
        """Dispatch to the appropriate tool handler (legacy aliases included)."""
        match tool:
            case "read":
                return self._read(args, task_id=task_id, agent_id=agent_id, session_id=session_id)
            case "edit" | "write":
                return self._write(
                    args,
                    task_id=task_id,
                    agent_id=agent_id,
                    session_id=session_id,
                )
            case "bash" | "execute":
                return self._execute(
                    args,
                    task_id=task_id,
                    agent_id=agent_id,
                    session_id=session_id,
                )
            case "grep":
                return self._grep(args)
            case "list":
                return self._list_dir(args)
            case "webfetch" | "web_search" | "websearch":
                return self._webfetch(args)
            case "task" | "delegate":
                return self._delegate(args)
            case _:
                return {"error": f"Unknown tool: {tool}"}

    def _read(
        self,
        args: dict[str, Any],
        *,
        task_id: str = "",
        agent_id: str = "",
        session_id: str = "",
    ) -> dict[str, Any]:
        raw_path = args.get("path") or resolve_file_path_arg(args) or ""
        # Credential deny (F-06) — canonical path_policy, fail-closed.
        denied = deny_reason(str(raw_path))
        if denied:
            log_permission_deny(task_id, agent_id, "read", args, reason="read_deny_path")
            return {"error": denied}
        try:
            path = self._safe_path(str(raw_path))
        except SecurityError as exc:
            log_permission_deny(task_id, agent_id, "read", args, reason="path_escape")
            return {"error": str(exc)}
        if not path.exists():
            return {"error": f"File not found: {args['path']}"}
        if path.is_dir():
            return {"error": f"Not a file: {raw_path}"}
        self._read_step += 1
        hit = self._read_cache.get(str(path), self._read_step)
        if hit is not None:
            return {
                "path": str(path.relative_to(self.project_root)),
                "content": hit.pointer().get("note", ""),
                "cached": True,
                "ref": f"step-{hit.ref_step}",
                "sha256": hit.sha256,
            }
        raw_bytes = path.read_bytes()
        if b"\x00" in raw_bytes[:8192]:
            return {
                "error": f"Binary file not readable as text: {raw_path}",
                "error_code": "BINARY",
            }
        content = raw_bytes.decode("utf-8", errors="replace")
        # Scan file content for PII and safety threats
        content = self._sanitize_output(content, source=str(path.relative_to(self.project_root)))
        capped = truncate_to_cap(content)
        content = capped.text
        self._read_cache.put(str(path), content, self._read_step)
        return {
            "path": str(path.relative_to(self.project_root)),
            "content": content,
            "sha256": repo_write.sha256_digest(path),
        }

    def _write(
        self,
        args: dict[str, Any],
        *,
        task_id: str = "",
        agent_id: str = "",
        session_id: str = "",
    ) -> dict[str, Any]:
        raw_path = args.get("path") or resolve_file_path_arg(args) or ""
        denied = deny_reason(str(raw_path))
        if denied:
            log_permission_deny(task_id, agent_id, "write", args, reason="read_deny_path")
            return {"error": denied}
        try:
            path = self._safe_path(str(raw_path))
        except SecurityError as exc:
            log_permission_deny(task_id, agent_id, "write", args, reason="path_escape")
            return {"error": str(exc)}

        # Harness-style edit (oldString/newString): pre-flight against
        # fresh bytes (T-01). Content-overwrite edits skip this.
        if "oldString" in args or "newString" in args:
            old_string = str(args.get("oldString", ""))
            new_string = str(args.get("newString", ""))
            if not path.exists():
                return {"error": f"File not found: {raw_path}", "error_code": "EDIT_NOT_FOUND"}
            current = path.read_text(encoding="utf-8", errors="replace")
            preflight = check_edit_preflight(
                current_content=current,
                old_string=old_string,
                new_string=new_string,
            )
            if not preflight.ok:
                return {
                    "error": preflight.message,
                    "error_code": preflight.error_code or "VALIDATION_REJECTED",
                }
            content = preflight.replaced_content or ""
        else:
            content = args.get("content", "")
        path.parent.mkdir(parents=True, exist_ok=True)
        # P0: optimistic concurrency — if the caller provides the digest it
        # read (via the ''sha256'' field on a prior ''read''), refuse the write
        # when the on-disk content changed underneath it (409 Conflict).
        expected_digest = args.get("sha256") or None
        try:
            result = repo_write.write_file(
                path,
                content,
                expected_digest=expected_digest,
                owner=session_id or task_id or agent_id,
            )
        except repo_write.RepoWriteConflict as exc:
            return {
                "path": str(path.relative_to(self.project_root)),
                "status": "error",
                "conflict": True,
                "error": (
                    f"409 Conflict: {exc.expected[:12]} != {exc.actual[:12]}. "
                    "The file changed since it was read; re-read it and retry."
                ),
                "before_hash": exc.expected,
                "after_hash": exc.actual,
            }
        if result["owner_conflict"]:
            return {
                "path": str(path.relative_to(self.project_root)),
                "status": "error",
                "owner_conflict": True,
                "error": (
                    "The file is claimed by another active session/task and cannot be overwritten."
                ),
                "before_hash": result["before_hash"],
                "after_hash": result["after_hash"],
            }
        self._read_cache.invalidate(str(path))
        return {
            "path": str(path.relative_to(self.project_root)),
            "bytes": len(content.encode()),
            "sha256": result["after_hash"],
            "before_hash": result["before_hash"],
            "changed": result["before_hash"] != result["after_hash"],
        }

    def _execute(
        self,
        args: dict[str, Any],
        *,
        task_id: str = "",
        agent_id: str = "",
        session_id: str = "",
    ) -> dict[str, Any]:
        """Execute a shell command safely (GAP-016 fix).

        * Commands are tokenized with ``shlex.split()`` — ``shell=True`` is
          **never** used.
        * The first token (the base command) must appear in ``allowed_commands``.
        * Shell features such as ``|``, ``&&``, ``;``, ``>``, ``<`` are
          rejected — express those as separate tool steps instead.
        * On Windows, commands that are ``cmd.exe`` built-ins (e.g. ``echo``)
          are executed via ``cmd /c`` for compatibility, but only after the
          allowlist check passes and with tokenized arguments.
        * Rejected commands are logged for security auditing.

        ``task_id``/``agent_id``/``session_id`` are accepted for call-site
        identity context; the ``bash`` tool is audit-only for the P0
        concurrency work (no lock/CAS on its file effects, per decision Q3).
        """
        import platform

        command = args["command"]

        # ── PowerShell antipattern pre-flight (T-05) ───────────────────
        ps_ok, ps_msg = check_powershell_command(command)
        if not ps_ok:
            return {"command": command, "error": ps_msg}

        # ── Credential deny in shell args (F-06) ────────────────────────
        denied_paths = find_denied_paths_in_command(command)
        if denied_paths:
            log_permission_deny(task_id, agent_id, "bash", args, reason="command_path_deny")
            return {
                "command": command,
                "error": f"permission denied: denied path {denied_paths[0]}",
            }

        # ── Reject shell metacharacters ──────────────────────────────────
        # Shared with the HITL gate (security.command_safety) so an approval
        # request for an un-runnable command is flagged BEFORE the human sees
        # it — execution itself remains fail-closed regardless of approval.
        metacharacters = find_shell_metacharacters(command)
        if metacharacters:
            _security_logger.warning(
                "Rejected command with shell metacharacters %s: %s",
                ", ".join(metacharacters),
                command[:200],
            )
            return {
                "command": command,
                "error": (
                    "Shell metacharacters (| & ; > < $ ` \\) are not allowed. "
                    "Express pipelines as separate 'bash' steps."
                ),
            }

        # ── Tokenize ────────────────────────────────────────────────────
        try:
            tokens = shlex.split(command)
        except ValueError as exc:
            return {"command": command, "error": f"Invalid command syntax: {exc}"}

        if not tokens:
            return {"command": command, "error": "Empty command"}

        base = Path(tokens[0]).name  # strip any path prefix

        # ── Allowlist check ──────────────────────────────────────────────
        if base not in self.allowed_commands:
            _security_logger.warning(
                "Rejected disallowed command '%s' from user input: %s",
                base,
                command[:200],
            )
            log_permission_deny(task_id, agent_id, "bash", args, reason="allowlist_deny")
            return {
                "command": command,
                "error": (
                    f"Command '{base}' is not in the allowlist. "
                    f"Allowed: {', '.join(sorted(self.allowed_commands))}"
                ),
            }

        # ── Shell egress (P2-T6) ────────────────────────────────────────
        # Runs AFTER the allowlist check so that a disallowed binary
        # (e.g. curl) is attributed to the allowlist (tests pin this
        # message); egress still guards every allowlisted command.
        egress_ok, egress_reason = check_shell_egress(command)
        if not egress_ok:
            return {"command": command, "error": f"egress denied: {egress_reason}"}

        # ── Resolve symlinks in arguments to prevent traversal ──────────
        resolved_tokens = [tokens[0]]  # Keep command name as-is
        for token in tokens[1:]:
            if token.startswith("-"):
                # Skip flags (they aren't paths)
                resolved_tokens.append(token)
            else:
                # Resolve the token as a potential path
                try:
                    resolved = (self.project_root / token).resolve()
                    # Verify it stays within project root
                    resolved.relative_to(self.project_root)
                    resolved_tokens.append(token)  # Keep original for command
                except ValueError:
                    _security_logger.warning(
                        "Rejected command with path traversal: %s -> %s",
                        token,
                        resolved,
                    )
                    return {
                        "command": command,
                        "error": f"Path argument '{token}' escapes project root",
                    }

        # ── Execute safely ───────────────────────────────────────────────
        logger.info("Executing allowed command: %s", command)
        timeout_val = int(os.getenv("TOOL_RUNNER_TIMEOUT", "120"))
        try:
            result = subprocess.run(
                tokens,
                capture_output=True,
                text=True,
                timeout=timeout_val,
                cwd=str(self.project_root),
            )
        except FileNotFoundError:
            # On Windows, some commands (echo, mkdir, etc.) are cmd.exe
            # built-ins and don't exist as standalone executables.  Fall
            # back to cmd /c with tokenized arguments — the allowlist
            # check has already passed, so this is safe.
            if platform.system() == "Windows":
                # SECURITY FIX: Use tokenized arguments instead of raw string
                # to prevent shell injection via cmd /c
                cmd_tokens = ["cmd", "/c"] + tokens
                result = subprocess.run(
                    cmd_tokens,
                    capture_output=True,
                    text=True,
                    timeout=timeout_val,
                    cwd=str(self.project_root),
                )
            else:
                raise

        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": self._sanitize_output(
                result.stdout[-2000:] if result.stdout else "", source=f"cmd:{base}"
            ),
            "stderr": self._sanitize_output(
                result.stderr[-2000:] if result.stderr else "", source=f"cmd:{base}:stderr"
            ),
        }

    def _grep(self, args: dict[str, Any]) -> dict[str, Any]:
        pattern = args["pattern"]
        try:
            search_path = self._safe_path(args.get("path", "."))
        except SecurityError as exc:
            return {"pattern": pattern, "error": str(exc)}
        matches: list[str] = []

        if search_path.is_file():
            matches = self._grep_file(search_path, pattern)
        elif search_path.is_dir():
            for f in search_path.rglob("*"):
                if f.is_file() and not any(
                    p.startswith(".") for p in f.relative_to(self.project_root).parts
                ):
                    matches.extend(self._grep_file(f, pattern))
                    if len(matches) >= _GREP_MATCH_CAP:
                        break

        # T-04 caps: per-line 500 chars; 100-match cap; scan carries the
        # truncated count so truncation is never silent. Sanitize via
        # _sanitize_output (PII/content filter + secret redact).
        capped = [cap_grep_line(m) for m in matches]
        shown = capped[:_GREP_MATCH_CAP]
        sanitized: list[str] = []
        for m in shown:
            sanitized.append(self._sanitize_output(m, source="grep"))

        return {
            "pattern": pattern,
            "matches": sanitized,
            "total": len(matches),
            "backend": grep_backend(),
            "truncated_lines": len(capped) - len(shown),
        }

    def _grep_file(self, path: Path, pattern: str) -> list[str]:
        matches: list[str] = []
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            for i, line in enumerate(content.splitlines(), 1):
                if pattern.lower() in line.lower():
                    rel = path.relative_to(self.project_root)
                    matches.append(f"{rel}:{i}: {line.strip()}")
        except (OSError, UnicodeDecodeError) as exc:
            logger.debug("Grep file skipped (unreadable): %s: %s", path, exc)
        return matches

    def _list_dir(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._safe_path(args.get("path", "."))
        if not path.is_dir():
            return {"error": f"Not a directory: {args.get('path', '.')}"}

        entries: list[str] = []
        for item in sorted(path.iterdir()):
            rel = item.relative_to(self.project_root)
            prefix = "d " if item.is_dir() else "f "
            entries.append(f"{prefix}{rel}")

        return {"path": str(path.relative_to(self.project_root)), "entries": entries[:100]}

    def _webfetch(self, args: dict[str, Any]) -> dict[str, Any]:
        """Fetch a URL and return sanitized text content.

        Restricted to ``http``/``https`` with a hard size cap; content is
        scanned for PII and safety threats before being returned.
        Egress allowlist (F-07) runs before fetch; fetch itself retries
        transient 429/5xx with backoff via :func:`call_with_retry`.
        """
        url = args.get("url", "")
        if not isinstance(url, str) or not url:
            return {"url": str(url), "error": "Only http:// and https:// URLs are allowed"}
        allowed, reason = validate_egress_url(url)
        if not allowed:
            return {"url": url, "error": f"egress denied: {reason}", "error_code": "EGRESS_DENIED"}
        result, attempts_used, _delays = call_with_retry(
            lambda: self._fetch_once(url),
            max_attempts=3,
            sleep=self._sleep,
        )
        if "error" in result:
            code = classify_tool_error(
                str(result.get("error", "")),
                result.get("http_status") if isinstance(result.get("http_status"), int) else None,
            )
            return {"url": url, **result, "attempts": attempts_used, "error_code": code}
        return {
            "url": result.get("url", url),
            "content": self._sanitize_output(result.get("content", ""), source="webfetch"),
            "attempts": attempts_used,
        }

    def _fetch_once(self, url: str) -> dict[str, Any]:
        """Single webfetch attempt; injectable via mock in tests."""
        import urllib.request

        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                raw = resp.read(64 * 1024).decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - fetch failure surfaced as error
            status = getattr(exc, "code", None)
            return {
                "error": f"Fetch failed: {exc}",
                **({"http_status": status} if isinstance(status, int) else {}),
            }
        return {"url": url, "content": raw}

    def _delegate(self, args: dict[str, Any]) -> dict[str, Any]:
        """Return a delegate action dict for the loop to create a subtask in the inbox."""
        return {
            "action": "delegate",
            "receiver": args.get("receiver", ""),
            "instruction": args.get("instruction", ""),
        }

    def _safe_path(self, path_str: str) -> Path:
        """Resolve a path and ensure it stays within PROJECT_ROOT."""
        resolved = (self.project_root / path_str).resolve()
        try:
            resolved.relative_to(self.project_root)
        except ValueError:
            raise SecurityError(f"Path '{path_str}' escapes project root: {resolved}") from None
        return resolved

    def _sanitize_output(self, text: str, source: str = "tool") -> str:
        """Scan tool output for content safety threats and PII.

        Args:
            text: Raw output from tool execution.
            source: Label for logging (e.g. tool name or file path).

        Returns:
            Sanitized text with threats blocked and PII masked.
        """
        if not text:
            return text

        # Content safety filter (injection, XSS, execution attempts)
        filter_result = self._content_filter.scan(text)
        if not filter_result.is_safe:
            _security_logger.warning(
                "Content threat blocked in %s output: threats=%s level=%s",
                source,
                filter_result.threats_detected,
                filter_result.threat_level.value,
            )
            text = filter_result.filtered

        # PII detection and masking
        pii_result = self._pii_detector.scan(text)
        if pii_result.has_pii:
            _security_logger.info(
                "PII detected and masked in %s output: types=%s count=%d",
                source,
                {t.value for t in pii_result.pii_types_found},
                len(pii_result.matches),
            )
            text = pii_result.masked

        # Secret redaction (F-05, canonical redact.py) — full [REDACTED]
        # for credential-shaped values before persistence/return. PII
        # detector handles PII shapes; redact handles secret shapes.
        redacted_text, hits = redact_secrets(text)
        if hits:
            _security_logger.info("Secret redacted in %s output: %s", source, ",".join(hits))
            text = redacted_text

        return text

    @staticmethod
    def _all_tools() -> set[str]:
        return set(_CANONICAL_TOOLS) | set(_TOOL_ALIASES)
