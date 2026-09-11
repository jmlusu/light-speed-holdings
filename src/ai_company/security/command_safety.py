"""Shell command safety helpers shared by the executor and the HITL gate.

GAP-016: commands are executed tokenized via ``shlex.split()`` with
``shell=True`` never used, so any command containing shell metacharacters
is rejected at execution time.  The HITL gate reuses the *same* detection
at approval time so a human never approves a command the executor can
never run (ticket #70).
"""

from __future__ import annotations

# Characters that would change command semantics if a shell were involved.
# A command containing any of these is rejected by ``ToolRunner._execute``
# (GAP-016) and must be expressed as separate tool steps instead.
SHELL_METACHARACTERS: frozenset[str] = frozenset("|&;><$`\\")


def find_shell_metacharacters(command: str) -> list[str]:
    """Return the sorted, de-duplicated metacharacters present in *command*.

    Returns an empty list when the command is clean.  Deterministic order
    makes the result stable for warnings, tests, and log messages.
    """
    return sorted({ch for ch in command if ch in SHELL_METACHARACTERS})


def command_has_shell_metacharacters(command: str) -> bool:
    """True when *command* contains any shell metacharacter (GAP-016)."""
    return bool(find_shell_metacharacters(command))
