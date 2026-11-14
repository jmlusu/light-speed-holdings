"""PowerShell anti-pattern pre-flight lint (P1-T3 / T-05).

AGENTS.md §17 documents the PowerShell 5.1 directives, but 1,500+
repeated stdout errors after documentation show awareness is not
enforcement. This module is the runtime enforcement point: the
ToolRunner scans every ``bash`` command before execution and rejects
known-broken patterns with the §17-compliant rewrite instead of
paying a shell round-trip.

Patterns (FAIL):
- ``Select-Object -First/-Last <negative>`` (PowerShell 5.1 rejects
  negative ``-First``/``-Last``; use ``-Skip``/slicing instead)
- ``&&`` as statement separator (PS 5.1 token error; use ``;`` + ``&``)
- Bash heredocs (``python << 'PYEOF'``) in PowerShell commands
- ``python3`` on Windows (use ``python``)
- ``$(...)`` inside double-quoted ``--jq`` arguments (PowerShell
  expands them before ``gh`` sees the string; use single-quoted
  single-field expressions or a temp ``.ps1`` file)
"""

from __future__ import annotations

import re

# (antipattern_id, compiled_pattern, compliant_rewrite_hint)
_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "select_negative",
        re.compile(r"Select-Object\s+-(First|Last)\s+-\d+", re.IGNORECASE),
        "Use a positive count, e.g. '| Select-Object -First 30'. "
        "For a tail slice use '@(...)[-n..-1]' instead of -Last -n.",
    ),
    (
        "double_ampersand",
        re.compile(r"&&"),
        "PowerShell 5.1 rejects '&&'. Use ';' + '&', e.g. \"cd 'path'; & command\".",
    ),
    (
        "bash_heredoc",
        re.compile(r"<<\s*'?[A-Z]"),
        "Bash heredocs do not work in PowerShell. "
        "Write the body to a temp .ps1 file and run 'powershell -File <path>'.",
    ),
    (
        "python3_windows",
        re.compile(r"\bpython3\b"),
        "On Windows, 'python3' is not recognised. Use 'python'.",
    ),
    (
        "jq_dollar_subshell",
        re.compile(r"--jq\s+.*\$\("),
        "PowerShell expands $(...) inside double-quoted --jq. "
        "Use a single-quoted single-field expression, e.g. --jq '.state', "
        "or a temp .ps1 file for expressions needing literals.",
    ),
]


def check_powershell_command(command: str) -> tuple[bool, str]:
    """Check *command* for PowerShell anti-patterns.

    Returns ``(is_safe, message)``; on a hit ``message`` names the
    anti-pattern and the compliant rewrite. Empty commands pass (the
    executor's own validation handles them).
    """
    if not command or not command.strip():
        return True, "safe"
    for pattern_id, pattern, hint in _PATTERNS:
        if pattern.search(command):
            return False, f"POWERSHELL_ANTIPATTERN[{pattern_id}]: {hint}"
    return True, "safe"


def antipattern_ids(command: str) -> list[str]:
    """Return the ids of all anti-patterns present in *command*."""
    if not command or not command.strip():
        return []
    return [pid for pid, pattern, _hint in _PATTERNS if pattern.search(command)]
