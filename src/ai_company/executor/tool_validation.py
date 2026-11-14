"""Tool-call argument validation — fail-fast schema checks (P1-T4 / T-02).

Malformed tool-call JSON (NULL/missing ``path``, ``command``…) was
recorded as a full tool error and retried blindly (>=149
occurrences). This validator runs *before* execution and returns a
structured rejection naming the missing key with a one-line shape
example, so the model can self-correct in one step.

The required-arg table matches **this repo's ToolRunner** calling
convention (``path``/``content``/``command``). The harness-side
``oldString``/``newString`` edit semantics (no-op rejection,
anchor-uniqueness pre-check) are supported when those keys are
present: an edit call carrying ``oldString``/``newString`` with
``oldString == newString`` is rejected locally, converting a wasted
harness round-trip into a cheap check.
"""

from __future__ import annotations

import hashlib as _hashlib
import random as _random
import shutil as _shutil
import time as _time
from collections.abc import Callable as _Callable
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from typing import Any

# Required-arg tables: tool -> ordered list of (key, shape_example).
# Only keys that handlers index directly are hard-required; absent
# optional keys (content, url, receiver…) fall back to handler
# defaults today and remain valid.
_REQUIRED_ARGS: dict[str, list[tuple[str, str]]] = {
    "read": [("path", '{"path": "src/app.py"}')],
    "edit": [("path", '{"path": "src/app.py", "content": "..."}')],
    "write": [("path", '{"path": "src/app.py", "content": "..."}')],
    "bash": [("command", '{"command": "python -m pytest"}')],
    "grep": [("pattern", '{"pattern": "TODO", "path": "src/"}')],
    "list": [],
    "webfetch": [],
    "task": [],
}


def required_args_for(tool: str) -> list[str]:
    """Return the required argument keys for *tool* (empty if unknown)."""
    return [key for key, _example in _REQUIRED_ARGS.get(tool, [])]


def validate_tool_args(tool: str, args: dict[str, Any]) -> tuple[bool, str]:
    """Validate *args* for *tool*.

    Returns ``(is_valid, message)``. On failure ``message`` names the
    missing key and shows the expected shape. ``None`` and
    empty-string values count as missing (the NULL-``filePath``
    cases in the harness).
    """
    if tool not in _REQUIRED_ARGS:
        return True, "no schema registered for tool"
    # Harness shape uses ``filePath``; this repo's handlers use ``path``.
    # Accept either so a valid harness call is not rejected as missing.
    if "path" not in args:
        for alias in ("filePath", "file_path"):
            candidate = args.get(alias)
            if isinstance(candidate, str) and candidate.strip():
                args = {**args, "path": candidate}
                break
    for key, example in _REQUIRED_ARGS[tool]:
        value = args.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, f"Missing key: {key}. Expected shape: {example}"
    # Edit semantics (harness-style keys): reject no-ops before dispatch.
    if tool == "edit":
        old = args.get("oldString")
        new = args.get("newString")
        if isinstance(old, str) and isinstance(new, str) and old == new:
            return False, (
                "Edit no-op rejected: oldString == newString. "
                "Re-read the exact region and provide a different newString."
            )
    return True, "valid"


def edit_rejection_hint(old_string: str, candidate_content: str | None) -> str | None:
    """Return a pre-check hint for an edit against cached content, if any.

    ``None`` means the edit may proceed. A non-``None`` hint means the
    call should be rejected locally instead of paying a harness
    round-trip: zero matches → re-read; multiple matches → widen the
    anchor. Exact-match authority stays with the edit tool.
    """
    if not old_string or candidate_content is None:
        return None
    count = candidate_content.count(old_string)
    if count == 0:
        return (
            "Edit pre-check: oldString not found in the content read this "
            "session. Re-read the exact region (anchor + verify) and retry."
        )
    if count > 1:
        line_numbers = [
            str(i + 1)
            for i, line in enumerate(candidate_content.splitlines())
            if old_string in line
        ][:3]
        locations = ", ".join(line_numbers) if line_numbers else "unknown"
        return (
            f"Edit pre-check: oldString matches {count} locations "
            f"(lines {locations}). Add surrounding context to make it unique."
        )
    return None


# ---------------------------------------------------------------------------
# P1 tool fixes T-01/T-03/T-04/T-06/T-07/T-08/T-11 (toolfix implementation)
#
# The section below adds the structured pre-flight, retry, cap and dedup
# helpers consumed by ToolRunner and tool_summarizer.  The tuple-based
# ``validate_tool_args`` above stays the canonical schema entry point.
# ---------------------------------------------------------------------------

#: End-to-end tool-output cap (T-11): larger completed outputs are truncated
#: with a spill marker instead of flooding the next iteration's context.
OUTPUT_CAP_BYTES: int = 50 * 1024

#: A single ripgrep JSON record larger than this is truncated, never an
#: error (the 140x "record exceeded 65536 bytes" class, T-04).
GREP_RECORD_CAP_BYTES: int = 64 * 1024

#: One grep match line is truncated to this many characters at the producer.
GREP_LINE_CAP_CHARS: int = 500

#: Maximum grep matches returned to the model, with a narrow-your-pattern
#: footer (T-04/T-11).
GREP_MATCH_CAP: int = 100

_FILE_PATH_KEYS: tuple[str, ...] = ("filePath", "path", "file_path")

#: Retry schedule: 0.5 s, 2 s, 8 s (factor 4) + up to 25% jitter.
_RETRY_BASE_SECONDS: float = 0.5
_RETRY_FACTOR: float = 4.0
_RETRY_JITTER_FRACTION: float = 0.25


def resolve_file_path_arg(args: dict[str, Any]) -> str | None:
    """First non-empty path argument across ``filePath``/``path``/``file_path``.

    ``None`` when every key is absent, ``None``, non-string, or blank —
    the NULL ``filePath`` case from the analytics report.
    """
    for key in _FILE_PATH_KEYS:
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


# --- Edit pre-flight (T-01) -------------------------------------------------


@_dataclass
class EditPreflightResult:
    """Outcome of checking an ``oldString``/``newString`` edit on fresh bytes."""

    ok: bool
    error_code: str | None = None
    message: str = ""
    match_count: int = 0
    locations: list[int] = _field(default_factory=list)
    replaced_content: str | None = None


def _line_number_at(content: str, index: int) -> int:
    """1-based line number of the character at ``index``."""
    return content.count("\n", 0, index) + 1


def check_edit_preflight(
    *,
    current_content: str,
    old_string: str,
    new_string: str,
) -> EditPreflightResult:
    """Validate an edit against freshly re-read file content (T-01).

    Distinct codes so callers skip instead of retry-looping: ``NOOP``
    (old == new, 154 errors), ``EDIT_NOT_FOUND`` (0 matches, 588 errors),
    ``EDIT_AMBIGUOUS`` (>1 matches, 74 errors; first 3 locations are
    returned so context can be widened in one step).
    """
    if not old_string:
        return EditPreflightResult(
            ok=False,
            error_code="VALIDATION_REJECTED",
            message="Schema validation rejected edit call: missing required "
            "argument(s): oldString.",
        )
    if old_string == new_string:
        return EditPreflightResult(
            ok=False,
            error_code="NOOP",
            message=(
                "NOOP: oldString == newString; edit skipped without dispatch. "
                "Change the content or drop the call."
            ),
            match_count=current_content.count(old_string),
        )
    count = current_content.count(old_string)
    if count == 0:
        anchor_hint = "re-read the exact region and copy oldString from fresh bytes"
        probe = old_string.strip().splitlines()[0][:20] if old_string.strip() else ""
        if probe:
            for line in current_content.splitlines():
                if probe in line:
                    anchor_hint = f"closest matching line: {line.strip()[:80]!r}"
                    break
        return EditPreflightResult(
            ok=False,
            error_code="EDIT_NOT_FOUND",
            message=f"EDIT_NOT_FOUND: oldString not found; {anchor_hint}.",
            match_count=0,
        )
    if count > 1:
        locations: list[int] = []
        start = 0
        for _ in range(min(count, 3)):
            idx = current_content.find(old_string, start)
            if idx == -1:
                break
            locations.append(_line_number_at(current_content, idx))
            start = idx + len(old_string)
        return EditPreflightResult(
            ok=False,
            error_code="EDIT_AMBIGUOUS",
            message=(
                f"EDIT_AMBIGUOUS: oldString matches {count} locations "
                f"(lines {', '.join(str(n) for n in locations)}); "
                "widen oldString with >=3 lines of surrounding context."
            ),
            match_count=count,
            locations=locations,
        )
    return EditPreflightResult(
        ok=True,
        match_count=1,
        locations=[_line_number_at(current_content, current_content.find(old_string))],
        replaced_content=current_content.replace(old_string, new_string, 1),
    )


# --- PowerShell pre-flight view (T-05; enforcement in ps_linter) ------------


@_dataclass(frozen=True)
class AntipatternHit:
    """One AGENTS.md §17 antipattern found in a ``bash`` command string."""

    pattern: str
    matched: str


def find_powershell_antipatterns(command: str) -> list[AntipatternHit]:
    """Ids of §17 antipatterns in *command* (empty list when clean).

    Thin view over :mod:`ai_company.executor.ps_linter` so the runtime
    pre-flight and the static scanner share one pattern table.
    """
    from ai_company.executor.ps_linter import antipattern_ids

    return [AntipatternHit(pattern=pid, matched=command[:80]) for pid in antipattern_ids(command)]


# --- Retry classification + backoff (T-07, T-08) -----------------------------


RETRYABLE_ERROR_CODES: frozenset[str] = frozenset(
    {"RATE_LIMITED", "TRANSPORT_ERROR", "TARGET_UNREACHABLE"}
)

_INFRA_ABORT_MARKERS: tuple[str, ...] = (
    "subagent killed",
    "session closed",
    "childprocess",
    "child process",
    "child_process",
    "orphaned",
)

_USER_CANCEL_MARKERS: tuple[str, ...] = (
    "user cancelled",
    "user canceled",
    "cancelled by user",
    "canceled by user",
)


def classify_tool_error(error_text: str, http_status: int | None = None) -> str:
    """Map free-text tool errors to stable codes (T-08).

    Splits the old single "aborted/cancelled" bucket into
    ``USER_CANCELLED`` (agent/human-initiated) vs ``INFRA_ABORTED``
    (subagent killed, session torn down, child-process kill).
    """
    text = error_text.lower()
    if http_status == 429 or "429" in text or "rate limit" in text or "too many requests" in text:
        return "RATE_LIMITED"
    if "subagent depth limit" in text or "depth limit reached" in text:
        return "DEPTH_LIMIT"
    if any(marker in text for marker in _USER_CANCEL_MARKERS):
        return "USER_CANCELLED"
    if any(marker in text for marker in _INFRA_ABORT_MARKERS):
        return "INFRA_ABORTED"
    if "aborted" in text or text.strip() == "abort":
        return "INFRA_ABORTED"
    if "cancelled" in text or "canceled" in text:
        return "USER_CANCELLED"
    if http_status is not None and 500 <= http_status < 600:
        return "TRANSPORT_ERROR"
    if "connection refused" in text or "connection reset" in text or "eof" in text:
        return "TARGET_UNREACHABLE"
    if "name or service not known" in text or "name resolution" in text:
        return "TARGET_UNREACHABLE"
    if "transport" in text or "temporarily unavailable" in text or "timed out" in text:
        return "TRANSPORT_ERROR"
    if http_status is not None and 400 <= http_status < 500:
        return "BAD_REQUEST"
    if "bad request" in text:
        return "BAD_REQUEST"
    if "missing required" in text or "validation rejected" in text:
        return "VALIDATION_REJECTED"
    return "UNKNOWN_ERROR"


def is_retryable_error(error_text: str, http_status: int | None = None) -> bool:
    """True when re-invoking the same call could plausibly succeed."""
    return classify_tool_error(error_text, http_status) in RETRYABLE_ERROR_CODES


def compute_backoff_delay(
    attempt: int,
    *,
    base_seconds: float = _RETRY_BASE_SECONDS,
    retry_after: float | None = None,
    rng: _random.Random | None = None,
) -> float:
    """Exponential backoff before retry ``attempt`` (0-based) + jitter.

    Schedule ``base * 4**attempt`` (0.5 s, 2 s, 8 s); a server-provided
    ``Retry-After`` floor wins.  ``rng`` is injectable for determinism.
    """
    exp = base_seconds * (_RETRY_FACTOR ** max(attempt, 0))
    delay = max(exp, retry_after if retry_after is not None else 0.0)
    jitter = (rng if rng is not None else _random).uniform(0.0, delay * _RETRY_JITTER_FRACTION)
    return delay + jitter


def call_with_retry(
    operation: _Callable[[], dict[str, Any]],
    *,
    max_attempts: int = 3,
    base_seconds: float = _RETRY_BASE_SECONDS,
    sleep: _Callable[[float], None] = _time.sleep,
    rng: _random.Random | None = None,
) -> tuple[dict[str, Any], int, list[float]]:
    """Call ``operation`` with backoff+jitter on retryable errors (T-07).

    ``operation`` returns a dict; a non-empty ``"error"`` value (plus
    optional ``"http_status"``/``"retry_after"``) drives classification.
    Returns ``(result, attempts_used, delays_slept)``; the final result
    carries ``"attempts"`` and, on persistent error, ``"error_code"``.
    """
    delays: list[float] = []
    result: dict[str, Any] = {}
    attempts_used = 0
    for attempt in range(max(1, max_attempts)):
        attempts_used = attempt + 1
        result = operation()
        error = result.get("error")
        if not error:
            result["attempts"] = attempts_used
            return result, attempts_used, delays
        http_status = result.get("http_status")
        code = classify_tool_error(
            str(error), http_status if isinstance(http_status, int) else None
        )
        result["error_code"] = code
        if code not in RETRYABLE_ERROR_CODES or attempts_used >= max_attempts:
            result["attempts"] = attempts_used
            return result, attempts_used, delays
        retry_after = result.get("retry_after")
        delay = compute_backoff_delay(
            attempt,
            base_seconds=base_seconds,
            retry_after=float(retry_after) if isinstance(retry_after, (int, float)) else None,
            rng=rng,
        )
        delays.append(delay)
        sleep(delay)
    result["attempts"] = attempts_used
    return result, attempts_used, delays


def depth_limit_fallback(
    *,
    receiver: str = "",
    instruction: str = "",
    agent_id: str = "",
) -> dict[str, Any]:
    """Direct-execution envelope for a depth-limited delegate call (T-06).

    Retrying a deterministic depth limit is futile; the fallback is
    explicit direct execution with the substitution logged.  The
    ``subagent_depth: 2`` config change is *not* applied here:
    ``opencode.json`` is root config (AGENTS.md §18) and the proposal
    lives in ``reports/opencode-db-toolfix-subagent-depth-2026-11-08.md``.
    """
    return {
        "action": "execute_directly",
        "receiver": receiver,
        "instruction": instruction,
        "error_code": "DEPTH_LIMIT",
        "fallback": "direct_execution",
        "message": (
            f"Subagent depth limit reached; {agent_id or 'agent'} executes "
            f"{receiver or 'request'} directly (fallback logged)."
        ),
    }


# --- Output caps + dedup (T-04, T-11) ----------------------------------------


@_dataclass
class TruncationResult:
    """Result of :func:`truncate_to_cap`."""

    text: str
    truncated: bool = False
    original_bytes: int = 0


def truncate_to_cap(text: str, cap_bytes: int = OUTPUT_CAP_BYTES) -> TruncationResult:
    """Truncate ``text`` to a byte budget with head/tail sampling (T-11)."""
    original = len(text.encode("utf-8", errors="ignore"))
    if original <= cap_bytes:
        return TruncationResult(text=text, truncated=False, original_bytes=original)
    head_chars = int(cap_bytes * 0.75)
    tail_chars = int(cap_bytes * 0.25)
    marker = (
        f"\n... [output truncated: {original} bytes total, cap {cap_bytes} bytes; "
        "re-run the tool with a narrower pattern/path] ...\n"
    )
    head = text[:head_chars]
    tail = text[-tail_chars:] if tail_chars > 0 else ""
    truncated = head + marker + tail
    while len(truncated.encode("utf-8", errors="ignore")) > cap_bytes and len(head) > 0:
        head = head[: max(0, len(head) - 256)]
        truncated = head + marker + tail
    return TruncationResult(text=truncated, truncated=True, original_bytes=original)


def cap_grep_line(line: str, cap_chars: int = GREP_LINE_CAP_CHARS) -> str:
    """Truncate one grep match line; overlong records never error (T-04)."""
    if len(line.encode("utf-8", errors="ignore")) > GREP_RECORD_CAP_BYTES:
        return line[:cap_chars] + "… [line truncated]"
    if len(line) > cap_chars:
        return line[:cap_chars] + "…"
    return line


class ToolOutputDeduper:
    """Per-session dedup of identical file reads (T-11).

    The second read of the same path with the same content hash is a
    pointer (``"unchanged since step N"``), not the full content.
    """

    def __init__(self) -> None:
        self._seen: dict[tuple[str, str], int] = {}

    def check(self, path: str, sha256: str, step: int) -> tuple[bool, int | None]:
        """Register a read; returns ``(is_duplicate, first_step_or_None)``."""
        key = (path, sha256)
        first = self._seen.get(key)
        if first is not None:
            return True, first
        self._seen[key] = step
        return False, None

    def reset(self) -> None:
        """Clear the cache (new sessions / tests)."""
        self._seen.clear()


def content_sha256(text: str) -> str:
    """Stable sha256 hex digest for dedup keys."""
    return _hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


# --- Ripgrep backend selection (T-03) -----------------------------------------


def grep_backend() -> str:
    """Best available grep backend: ``"rg"`` > ``"git-grep"`` > ``"python"``."""
    if _shutil.which("rg") is not None:
        return "rg"
    if _shutil.which("git") is not None:
        return "git-grep"
    return "python"
