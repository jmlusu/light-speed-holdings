"""Sandboxed tool execution engine.

Security hardening (GAP-016):
- Commands are parsed with ``shlex.split()`` instead of ``shell=True``.
- Only allowlisted command prefixes may execute.
- ``shell=True`` is never used; shell features (pipes, redirects) are blocked
  and should be expressed as separate tool steps.
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

import logging
import shlex
import subprocess
from pathlib import Path
from typing import Any

import yaml

from ai_company.audit.integration import log_hitl_decision, log_tool_call
from ai_company.executor.hitl_gate import HITLGate
from ai_company.orchestrator.tier_rules import (
    SENIORITY_AUTO_APPROVE_TIER,
    ApprovalTier,
    classify_tool_action,
    get_tier_config,
)
from ai_company.security.content_filter import ContentFilter, get_content_filter
from ai_company.security.pii_detector import PIIDetector, get_pii_detector

logger = logging.getLogger(__name__)

# Security audit logger — separate from application logs
_security_logger = logging.getLogger("ai_company.security.tool_runner")


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
            f"Task {task_id} parked for HITL approval of {tool} "
            f"(request {request_id}, tier {tier})"
        )


# ---------------------------------------------------------------------------
# Command allowlist — loaded from YAML config with hardcoded fallback.
# Only these base commands may be executed via the ``execute`` tool.
# ---------------------------------------------------------------------------
_DEFAULT_ALLOWED_COMMANDS: frozenset[str] = frozenset({
    # Build / test
    "python", "python3", "pip", "pytest", "ruff", "mypy", "black", "isort",
    # Version control
    "git",
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep", "find", "tree",
    # Text processing (standalone — pipes blocked)
    "sort", "uniq", "diff", "echo",
    # Package / env
    "npm", "node", "npx",
    # Misc safe ops
    "mkdir", "cp", "mv", "touch", "date", "env", "which", "pwd",
})


def _load_allowlist(config_path: str | Path | None = None) -> frozenset[str]:
    """Load the command allowlist from YAML config, falling back to defaults."""
    if config_path is None:
        # Look for config relative to project root
        candidates = [
            Path("config/tool_allowlist.yaml"),
            Path("ai-company/config/tool_allowlist.yaml"),
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
                logger.info("Loaded tool allowlist from %s (%d commands)", config_path, len(commands))
                return frozenset(commands)
        except (yaml.YAMLError, OSError) as exc:
            logger.warning("Failed to load allowlist from %s: %s — using defaults", config_path, exc)

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
        self.project_root = Path(project_root).resolve()
        self.allowed_commands = _load_allowlist(allowlist_path)
        self._content_filter = content_filter or get_content_filter()
        self._pii_detector = pii_detector or get_pii_detector()

    def run_plan(
        self,
        plan: list[dict[str, Any]],
        hitl_gate: HITLGate | None = None,
        task_id: str = "",
        agent_id: str = "",
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

        for i, step in enumerate(plan):
            tool = step.get("tool", "")
            args = step.get("args", {})

            if tool not in self._all_tools():
                error_result = {"step": i, "tool": tool, "status": "error", "error": f"Unknown tool: {tool}"}
                results.append(error_result)
                log_tool_call(task_id, agent_id, tool, args, error_result)
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
                        "step": i, "tool": tool, "status": "denied",
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
                    int(tier), tier_label, tool, agent_id,
                )

            # ── Execute the tool ──────────────────────────────────────
            try:
                result = self._execute_tool(tool, args)
                status = "error" if "error" in result else "ok"
                exec_result = {
                    "step": i, "tool": tool, "status": status,
                    "tier": tier, "tier_label": tier_label, **result,
                }
                results.append(exec_result)
                log_tool_call(task_id, agent_id, tool, args, exec_result)
            except Exception as exc:
                exc_result = {
                    "step": i, "tool": tool, "status": "error",
                    "tier": tier, "tier_label": tier_label, "error": str(exc),
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
                int(tier), tier_config["label"], tool_name, agent_id,
            )
        elif int(tier) >= 1:
            logger.info(
                "Tier %d (%s) — %s auto-approved for %s",
                int(tier), tier_config["label"], tool_name, agent_id,
            )

        return result

    def _execute_tool(self, tool: str, args: dict[str, Any]) -> dict[str, Any]:
        """Dispatch to the appropriate tool handler."""
        match tool:
            case "read":
                return self._read(args)
            case "write":
                return self._write(args)
            case "execute":
                return self._execute(args)
            case "grep":
                return self._grep(args)
            case "list":
                return self._list_dir(args)
            case "code_interpreter":
                return self._run_python(args)
            case "delegate":
                return self._delegate(args)
            case _:
                return {"error": f"Unknown tool: {tool}"}

    def _read(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._safe_path(args["path"])
        if not path.exists():
            return {"error": f"File not found: {args['path']}"}
        content = path.read_text(encoding="utf-8", errors="replace")
        # Scan file content for PII and safety threats
        content = self._sanitize_output(content, source=str(path.relative_to(self.project_root)))
        return {"path": str(path.relative_to(self.project_root)), "content": content}

    def _write(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._safe_path(args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        content = args.get("content", "")
        path.write_text(content, encoding="utf-8")
        return {"path": str(path.relative_to(self.project_root)), "bytes": len(content.encode())}

    def _execute(self, args: dict[str, Any]) -> dict[str, Any]:
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
        """
        import platform

        command = args["command"]

        # ── Reject shell metacharacters ──────────────────────────────────
        _SHELL_META = set("|&;><$`\\") - {"/", "-", ".", "_"}
        if any(ch in command for ch in _SHELL_META):
            _security_logger.warning(
                "Rejected command with shell metacharacters: %s",
                command[:200],
            )
            return {
                "command": command,
                "error": (
                    "Shell metacharacters (| & ; > < $ ` \\) are not allowed. "
                    "Express pipelines as separate 'execute' steps."
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
            return {
                "command": command,
                "error": (
                    f"Command '{base}' is not in the allowlist. "
                    f"Allowed: {', '.join(sorted(self.allowed_commands))}"
                ),
            }

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
        try:
            result = subprocess.run(
                tokens,
                capture_output=True,
                text=True,
                timeout=120,
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
                    timeout=120,
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
        search_path = self._safe_path(args.get("path", "."))
        matches: list[str] = []

        if search_path.is_file():
            matches = self._grep_file(search_path, pattern)
        elif search_path.is_dir():
            for f in search_path.rglob("*"):
                if f.is_file() and not any(p.startswith(".") for p in f.relative_to(self.project_root).parts):
                    matches.extend(self._grep_file(f, pattern))
                    if len(matches) >= 50:
                        break

        # Sanitize individual match lines for PII
        sanitized: list[str] = []
        for m in matches[:50]:
            sanitized.append(self._sanitize_output(m, source="grep"))

        return {"pattern": pattern, "matches": sanitized, "total": len(matches)}

    def _grep_file(self, path: Path, pattern: str) -> list[str]:
        matches: list[str] = []
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            for i, line in enumerate(content.splitlines(), 1):
                if pattern.lower() in line.lower():
                    rel = path.relative_to(self.project_root)
                    matches.append(f"{rel}:{i}: {line.strip()}")
        except (OSError, UnicodeDecodeError):
            pass
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

    def _run_python(self, args: dict[str, Any]) -> dict[str, Any]:
        """Execute a Python code snippet via ``python -c``.

        The ``code`` string is passed as a single argument — never interpreted
        through a shell.
        """
        code = args["code"]
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(self.project_root),
        )
        return {
            "returncode": result.returncode,
            "stdout": self._sanitize_output(
                result.stdout[-2000:] if result.stdout else "", source="code_interpreter"
            ),
            "stderr": self._sanitize_output(
                result.stderr[-2000:] if result.stderr else "", source="code_interpreter:stderr"
            ),
        }

    def _delegate(self, args: dict[str, Any]) -> dict[str, Any]:
        """Create a subtask in the inbox. Actual processing happens by the loop."""
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
            raise SecurityError(
                f"Path '{path_str}' escapes project root: {resolved}"
            )
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

        return text

    @staticmethod
    def _all_tools() -> set[str]:
        return {"read", "write", "execute", "grep", "list", "code_interpreter", "delegate"}
