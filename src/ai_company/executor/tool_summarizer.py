"""Tool result summarization — compress tool outputs for token efficiency."""

from __future__ import annotations

import hashlib
import logging
import re
from typing import Any, Callable

from ai_company.llm.client import LLMClient
from ai_company.llm.token_counter import count_tokens

logger = logging.getLogger(__name__)

# ── PowerShell / stack-trace compression ──

# Markers that indicate a verbose PowerShell or Python stack trace
_PS_ERROR_PHRASES = (
    "at line:",
    "in position",
    "call stack:",
    "parameter binding",
    "\u001b[",  # ANSI escape
    "traceback (most recent call last):",
)

_PS_ERROR_FRAME_PREFIXES = (
    "at ",
    "in ",
    'file "',
    "raise ",
    "self.",
)


def _compress_powershell_error(stderr: str, max_chars: int = 400) -> str:
    """Compress a verbose PowerShell/Python error to its essential lines.

    Keeps: first error line, error category, exit code hint.
    Removes: stack frames, ANSI escapes, repeated blank lines, positional noise.
    """
    if not stderr:
        return ""

    lines = stderr.splitlines()
    compressed: list[str] = []
    seen_blank = False

    for line in lines:
        stripped = line.strip()

        # Skip ANSI escape sequences entirely
        if "\u001b[" in line:
            # Extract plain text from ANSI-wrapped line
            stripped = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", line).strip()
            if not stripped:
                continue

        # Skip blank lines (collapse consecutive blanks)
        if not stripped:
            if seen_blank:
                continue
            seen_blank = True
            compressed.append("")
            continue
        seen_blank = False

        # Skip stack-frame noise
        low = stripped.lower()
        if any(phrase in low for phrase in _PS_ERROR_PHRASES) or low.startswith(
            _PS_ERROR_FRAME_PREFIXES
        ):
            continue

        compressed.append(stripped)

        # Hard cap to avoid pathological cases
        if len(compressed) >= 12:
            break

    result = "\n".join(compressed).strip()

    # Truncate to max_chars
    if len(result) > max_chars:
        result = result[:max_chars] + "... [error truncated]"

    return result


# ── Repeated-error deduplication ──

# In-process cache of seen error fingerprints → compressed forms.
# Bounded to avoid memory growth in long sessions.
_MAX_ERROR_CACHE = 200
_error_fingerprints: dict[str, tuple[str, int]] = {}


def _fingerprint_error(text: str) -> str:
    """Stable fingerprint for an error string (ignores volatile numbers/paths)."""
    # Normalize: strip numbers, hex addresses, absolute paths, timestamps
    normalized = re.sub(r"0x[0-9a-fA-F]+", "0x?", text)
    normalized = re.sub(r"\d{4,}", "N", normalized)  # long numbers (timestamps, line nums)
    normalized = re.sub(r"[A-Z]:\\[^\s]+", "PATH", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def _dedupe_error(error_text: str) -> str:
    """If this exact error (normalized) was already seen, return a short reference."""
    fp = _fingerprint_error(error_text)
    cached = _error_fingerprints.get(fp)
    if cached is not None:
        text, count = cached
        _error_fingerprints[fp] = (text, count + 1)
        return f"(repeat of earlier error #{count + 1}; same root cause)"
    if len(_error_fingerprints) >= _MAX_ERROR_CACHE:
        _error_fingerprints.pop(next(iter(_error_fingerprints)))
    _error_fingerprints[fp] = (error_text[:200], 1)
    return error_text


def _reset_error_cache() -> None:
    """Reset dedup cache (for tests / new sessions)."""
    _error_fingerprints.clear()


def summarize_tool_result(
    tool: str,
    result: dict[str, Any],
    max_tokens: int = 500,
    llm: LLMClient | None = None,
) -> str:
    """Summarize a tool result for token-efficient feedback.

    Args:
        tool: The tool name.
        result: The tool result dictionary.
        max_tokens: Maximum tokens for the summary.
        llm: Optional LLM client for intelligent summarization.

    Returns:
        Summarized result string.
    """
    summarizer = TOOL_SUMMARIZERS.get(tool, _summarize_generic)
    return summarizer(result, max_tokens, llm)


def _summarize_read(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a read tool result."""
    path = result.get("path", "unknown")
    content = result.get("content", "")
    error = result.get("error")

    if error:
        compressed = _dedupe_error(_compress_powershell_error(str(error)))
        return f"read({path}) → ERROR: {compressed}"

    lines = content.split("\n")
    line_count = len(lines)
    char_count = len(content)

    # For code files, show first/last few lines and key structures
    if path.endswith((".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c")):
        return _summarize_code_file(path, content, max_tokens)

    # For other files, truncate with indicator
    if char_count > max_tokens * 4:
        preview = (
            content[: max_tokens * 2]
            + f"\n... [{line_count} lines, {char_count} chars total] ...\n"
            + content[-max_tokens * 2 :]
        )
        return f"read({path}) → {preview}"

    return f"read({path}) → {content}"


def _summarize_code_file(path: str, content: str, max_tokens: int) -> str:
    """Summarize a code file showing structure."""
    lines = content.split("\n")
    line_count = len(lines)

    # Extract key structures (functions, classes, imports)
    key_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped.startswith(("def ", "class ", "async def ", "function ", "const ", "export "))
            or stripped.startswith("import ")
            or stripped.startswith("from ")
            or (
                stripped
                and not stripped.startswith("#")
                and ":" in stripped
                and "=" not in stripped
            )
        ):
            key_lines.append(f"  L{i + 1}: {stripped[:80]}")

    summary = f"read({path}) → {line_count} lines"
    if key_lines:
        summary += "\nKey structures:\n" + "\n".join(key_lines[:15])
        if len(key_lines) > 15:
            summary += f"\n  ... and {len(key_lines) - 15} more"

    # Truncate if needed
    if count_tokens(summary) > max_tokens:
        summary = summary[: max_tokens * 4] + "... [truncated]"

    return summary


def _summarize_edit(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize an edit tool result."""
    path = result.get("path", "unknown")
    bytes_written = result.get("bytes", 0)
    error = result.get("error")

    if error:
        return f"edit({path}) → ERROR: {error}"

    return f"edit({path}) → OK ({bytes_written} bytes written)"


def _summarize_bash(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a bash tool result with aggressive PowerShell error compression."""
    command = result.get("command", "unknown")
    returncode = result.get("returncode", -1)
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")
    error = result.get("error")

    if error:
        compressed = _dedupe_error(_compress_powershell_error(str(error)))
        return f"bash({command}) → ERROR: {compressed}"

    status = "OK" if returncode == 0 else f"FAILED (exit {returncode})"

    output_parts = []
    if stdout:
        stdout_short = stdout[: max_tokens * 2]
        if len(stdout) > max_tokens * 2:
            stdout_short += f"\n... [{len(stdout)} chars truncated] ..."
        output_parts.append(f"stdout: {stdout_short}")
    if stderr:
        # Always compress stderr — it's almost always the bloat source
        compressed_err = _compress_powershell_error(stderr, max_chars=max_tokens * 2)
        compressed_err = _dedupe_error(compressed_err)
        if compressed_err:
            output_parts.append(f"stderr: {compressed_err}")

    output_str = "; ".join(output_parts) if output_parts else "no output"
    return f"bash({command}) → {status}; {output_str}"


def _summarize_grep(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a grep tool result."""
    pattern = result.get("pattern", "unknown")
    matches = result.get("matches", [])
    total = result.get("total", 0)
    error = result.get("error")

    if error:
        return f"grep({pattern}) → ERROR: {error}"

    if not matches:
        return f"grep({pattern}) → No matches found"

    # Show first few matches
    match_preview = "\n".join(matches[:5])
    if len(matches) > 5:
        match_preview += f"\n... and {len(matches) - 5} more matches"

    return f"grep({pattern}) → {total} matches:\n{match_preview}"


def _summarize_list(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a list tool result."""
    path = result.get("path", "unknown")
    entries = result.get("entries", [])
    error = result.get("error")

    if error:
        return f"list({path}) → ERROR: {error}"

    if not entries:
        return f"list({path}) → Empty directory"

    # Count files vs dirs
    dirs = [e for e in entries if e.startswith("d ")]
    files = [e for e in entries if e.startswith("f ")]

    preview = "\n".join(entries[:10])
    if len(entries) > 10:
        preview += f"\n... and {len(entries) - 10} more entries"

    return f"list({path}) → {len(dirs)} dirs, {len(files)} files:\n{preview}"


def _summarize_webfetch(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a webfetch tool result."""
    url = result.get("url", "unknown")
    content = result.get("content", "")
    error = result.get("error")

    if error:
        return f"webfetch({url}) → ERROR: {error}"

    if len(content) > max_tokens * 4:
        content = content[: max_tokens * 2] + f"\n... [{len(content)} chars truncated] ..."

    return f"webfetch({url}) → {content}"


def _summarize_task(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Summarize a task/delegate tool result."""
    receiver = result.get("receiver", "unknown")
    instruction = result.get("instruction", "")
    error = result.get("error")

    if error:
        return f"task({receiver}) → ERROR: {error}"

    instr_preview = instruction[:100] + ("..." if len(instruction) > 100 else "")
    return f"task({receiver}) → delegated: {instr_preview}"


def _summarize_generic(result: dict[str, Any], max_tokens: int, llm: LLMClient | None) -> str:
    """Generic fallback summarizer."""
    error = result.get("error")
    if error:
        compressed = _dedupe_error(_compress_powershell_error(str(error)))
        return f"ERROR: {compressed}"

    # Remove internal fields and truncate
    filtered = {
        k: v for k, v in result.items() if k not in ("step", "tool", "status", "tier", "tier_label")
    }
    import json

    text = json.dumps(filtered, default=str)

    if count_tokens(text) > max_tokens:
        text = text[: max_tokens * 4] + "... [truncated]"

    return text


def build_summarized_feedback(
    step_results: list[dict[str, Any]],
    iteration: int,
    max_iterations: int,
    max_tokens_per_tool: int = 500,
    llm: LLMClient | None = None,
) -> str:
    """Build iteration feedback with summarized tool results.

    This replaces build_iteration_feedback from prompts.py with token-efficient summaries.
    """
    parts: list[str] = [
        f"=== Tool Execution Results (iteration {iteration}/{max_iterations}) ===",
        "",
    ]

    has_errors = False
    has_denials = False

    for i, result in enumerate(step_results):
        tool = result.get("tool", "unknown")
        status = result.get("status", "unknown")
        parts.append(f"Step {i + 1}: {tool} — status: {status}")

        if status == "error":
            has_errors = True
            error_msg = result.get("error", "unknown error")
            parts.append(f"  Error: {error_msg}")
        elif status == "denied":
            has_denials = True
            parts.append(f"  Denied: {result.get('error', 'human approval denied')}")
        else:
            # Use summarized result
            summary = summarize_tool_result(tool, result, max_tokens_per_tool, llm)
            parts.append(f"  {summary}")
        parts.append("")

    # Context-aware guidance
    remaining = max_iterations - iteration
    parts.append(f"=== Remaining budget: {remaining} iteration(s) ===")
    parts.append("")

    if has_errors or has_denials:
        parts.extend(
            [
                "IMPORTANT: One or more tool calls failed or were denied.",
                "Before your next action, consider:",
                "1. Can you work around the failure with a different approach?",
                "2. Is the task still achievable with the remaining tools?",
                "3. Should you report partial progress and mark done?",
                "",
            ]
        )

    parts.extend(
        [
            "Based on these results, decide your next action.",
            'If the task is complete, set "done": true and provide your final result.',
            "Otherwise, respond with your next plan of tool calls.",
        ]
    )

    return "\n".join(parts)


# Tool-specific summarization strategies (defined after functions to avoid forward references)

_ToolSummarizer = Callable[[dict[str, Any], int, LLMClient | None], str]

TOOL_SUMMARIZERS: dict[str, _ToolSummarizer] = {
    "read": _summarize_read,
    "edit": _summarize_edit,
    "bash": _summarize_bash,
    "grep": _summarize_grep,
    "list": _summarize_list,
    "webfetch": _summarize_webfetch,
    "task": _summarize_task,
}
