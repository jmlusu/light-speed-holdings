"""Sandboxed tool execution engine.

Security hardening (GAP-016):
- Commands are parsed with ``shlex.split()`` instead of ``shell=True``.
- Only allowlisted command prefixes may execute.
- ``shell=True`` is never used; shell features (pipes, redirects) are blocked
  and should be expressed as separate tool steps.
"""

from __future__ import annotations

import logging
import shlex
import subprocess
from pathlib import Path
from typing import Any

from ai_company.audit.integration import log_hitl_decision, log_tool_call
from ai_company.executor.hitl_gate import HITLGate

logger = logging.getLogger(__name__)


class SecurityError(Exception):
    """Raised when a tool tries to escape the project sandbox."""


# ---------------------------------------------------------------------------
# Command allowlist — only these base commands may be executed via the
# ``execute`` tool.  Add entries here as new legitimate tools are onboarded.
# ---------------------------------------------------------------------------
ALLOWED_COMMANDS: frozenset[str] = frozenset({
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


class ToolRunner:
    """Executes tool plan steps from the LLM response.

    All file operations are restricted to PROJECT_ROOT.
    Approval is determined by the tier system (tier_rules.classify_tool_action)
    rather than a hardcoded tool list.
    """

    def __init__(self, project_root: str | Path = ".") -> None:
        self.project_root = Path(project_root).resolve()

    def run_plan(
        self,
        plan: list[dict[str, Any]],
        hitl_gate: HITLGate | None = None,
        task_id: str = "",
        agent_id: str = "",
        seniority: str = "",
        risk_level: str = "",
    ) -> list[dict[str, Any]]:
        """Execute each step in the plan.

        Returns a list of step results. The HITL gate classifies each tool
        action into a tier and handles approval accordingly. If HITL denies
        a step, execution continues with remaining steps.
        """
        results: list[dict[str, Any]] = []

        for i, step in enumerate(plan):
            tool = step.get("tool", "")
            args = step.get("args", {})

            if tool not in self._all_tools():
                error_result = {"step": i, "tool": tool, "status": "error", "error": f"Unknown tool: {tool}"}
                results.append(error_result)
                log_tool_call(task_id, agent_id, tool, args, error_result)
                continue

            if hitl_gate is not None:
                approved = hitl_gate.request_and_wait(
                    task_id=task_id,
                    agent_id=agent_id,
                    tool=tool,
                    args=args,
                    seniority=seniority,
                    risk_level=risk_level,
                )
                log_hitl_decision(task_id, agent_id, tool, approved)
                if not approved:
                    denied_result = {"step": i, "tool": tool, "status": "denied", "error": "Human approval denied"}
                    results.append(denied_result)
                    log_tool_call(task_id, agent_id, tool, args, denied_result)
                    continue

            try:
                result = self._execute_tool(tool, args)
                status = "error" if "error" in result else "ok"
                exec_result = {"step": i, "tool": tool, "status": status, **result}
                results.append(exec_result)
                log_tool_call(task_id, agent_id, tool, args, exec_result)
            except Exception as exc:
                exc_result = {"step": i, "tool": tool, "status": "error", "error": str(exc)}
                results.append(exc_result)
                log_tool_call(task_id, agent_id, tool, args, exc_result)

        return results

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
        * The first token (the base command) must appear in ``ALLOWED_COMMANDS``.
        * Shell features such as ``|``, ``&&``, ``;``, ``>``, ``<`` are
          rejected — express those as separate tool steps instead.
        * On Windows, commands that are ``cmd.exe`` built-ins (e.g. ``echo``)
          are executed via ``cmd /c`` for compatibility, but only after the
          allowlist check passes.
        """
        import platform

        command = args["command"]

        # ── Reject shell metacharacters ──────────────────────────────────
        _SHELL_META = set("|&;><$`\\") - {"/", "-", ".", "_"}
        if any(ch in command for ch in _SHELL_META):
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
        if base not in ALLOWED_COMMANDS:
            return {
                "command": command,
                "error": (
                    f"Command '{base}' is not in the allowlist. "
                    f"Allowed: {', '.join(sorted(ALLOWED_COMMANDS))}"
                ),
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
            # back to cmd /c <command> — the allowlist check has already
            # passed, so this is safe.
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["cmd", "/c", command],
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
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
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

        return {"pattern": pattern, "matches": matches[:50], "total": len(matches)}

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
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
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

    @staticmethod
    def _all_tools() -> set[str]:
        return {"read", "write", "execute", "grep", "list", "code_interpreter", "delegate"}
