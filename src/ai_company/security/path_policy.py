"""Filesystem read-deny policy (F-06 -> R2).

Enforced in the **tool/runner layer** (``ToolRunner``), not in the system
prompt (LLM01: the prompt is not a boundary). Denies agent ``read``,
``grep`` and ``bash`` file access to credential-bearing paths:

- ``*.env`` variants: ``.env``, ``.env.*``, ``*.env`` — **except**
  ``.env.example`` / ``.env.staging.example`` (verify placeholders-only
  before relying on the exemption; see ``docs/security/READ-DENY-POLICY.md``)
- ``auth.json``, ``mcp-auth.json`` (any directory)
- ``opencode.db``, ``opencode.db-wal``, ``opencode.db-shm``,
  ``opencode.db.bak``, ``opencode-.db*``
- ``*.pem``, ``*.key`` (preventive, per the ``security-and-hardening``
  ``.gitignore`` baseline)

Patterns are loaded from ``config/path_deny.yaml`` with code defaults as
fallback (same convention as ``config/tool_allowlist.yaml``). Matching is
case-insensitive on the basename and on every path segment, so
``some/dir/auth.json`` is denied as well as ``auth.json``.

Layering (D-1): this module is the canonical credential/DB deny;
``security/path_allowlist`` delegates its credential/DB deny here and keeps
only allowlist + attribution semantics.
"""

from __future__ import annotations

import fnmatch
import logging
import shlex
from pathlib import Path
from typing import cast

import yaml

logger = logging.getLogger(__name__)
_security_logger = logging.getLogger("ai_company.security.path_policy")

_DEFAULT_PATTERNS: tuple[str, ...] = (
    ".env*",
    "*.env",
    "*.pem",
    "*.key",
    "opencode.db*",
    "opencode-.db*",
)
_DEFAULT_BASENAMES: frozenset[str] = frozenset({"auth.json", "mcp-auth.json"})
_DEFAULT_EXEMPT: frozenset[str] = frozenset({".env.example", ".env.staging.example"})

DENIED_HINT = "Automated permission policy"


def _load_policy(config_path: str | Path | None = None) -> dict[str, list[str] | frozenset[str]]:
    """Load the deny policy YAML, falling back to code defaults."""
    if config_path is None:
        candidate = Path("config/path_deny.yaml")
        if candidate.exists():
            config_path = candidate
    if config_path is not None:
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            logger.info("Loaded path deny policy from %s", config_path)
            return {
                "patterns": [str(p) for p in data.get("denied_patterns", _DEFAULT_PATTERNS)],
                "basenames": frozenset(
                    str(b).lower() for b in data.get("denied_basenames", _DEFAULT_BASENAMES)
                ),
                "exempt": frozenset(
                    str(b).lower() for b in data.get("exempt_basenames", _DEFAULT_EXEMPT)
                ),
            }
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to load path deny policy from %s: %s — using defaults", config_path, exc
            )
    return {
        "patterns": list(_DEFAULT_PATTERNS),
        "basenames": _DEFAULT_BASENAMES,
        "exempt": _DEFAULT_EXEMPT,
    }


_POLICY = _load_policy()

DENIED_PATTERNS: tuple[str, ...] = tuple(_POLICY["patterns"])
DENIED_BASENAMES: frozenset[str] = cast(frozenset[str], _POLICY["basenames"])
EXEMPT_BASENAMES: frozenset[str] = cast(frozenset[str], _POLICY["exempt"])


def _path_segments(path_str: str) -> list[str]:
    """Split a path into segments, accepting both ``/`` and ``\\``."""
    normalized = path_str.replace("\\", "/")
    return [seg for seg in normalized.split("/") if seg not in ("", ".", "..")]


def is_path_denied(path_str: str) -> bool:
    """True when *path_str* resolves to a denied credential-bearing path."""
    if not path_str:
        return False
    segments = _path_segments(path_str)
    if not segments:
        return False
    lowered = [s.lower() for s in segments]
    if lowered[-1] in EXEMPT_BASENAMES:
        return False
    if lowered[-1] in DENIED_BASENAMES:
        return True
    # Any segment that is a denied basename (covers nested auth.json paths).
    if any(seg in DENIED_BASENAMES for seg in lowered):
        return True
    basename = lowered[-1]
    return any(fnmatch.fnmatch(basename, pattern.lower()) for pattern in DENIED_PATTERNS)


def deny_reason(path_str: str) -> str | None:
    """Return the deny explanation for *path_str*, or ``None`` if allowed."""
    if not is_path_denied(path_str):
        return None
    return (
        f"{DENIED_HINT}: read denied for credential-bearing path {path_str!r}. "
        "Credential material must be rotated via the provider console; "
        "see docs/security/CREDENTIAL-ROTATION-RUNBOOK.md."
    )


def find_denied_paths_in_command(command: str) -> list[str]:
    """Inspect a shell command string for denied path arguments.

    Tokenizes with ``shlex`` (same tokenizer as ``ToolRunner``). Flags are
    skipped; every other token is tested with :func:`is_path_denied`. This
    catches both ``read``-equivalent file reads (``cat .env``,
    ``type .env.local``) and direct DB reads (``python -c '...'`` is only
    flagged when a literal denied filename appears as a token).
    """
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    denied: list[str] = []
    for token in tokens:
        if token.startswith("-"):
            continue
        if is_path_denied(token):
            denied.append(token)
    return denied


def check_path_allowed(path_str: str) -> None:
    """Raise :class:`PermissionError` when *path_str* is denied.

    Kept for callers that prefer exceptions over error-dict returns.
    """
    reason = deny_reason(path_str)
    if reason:
        _security_logger.warning("Read-deny triggered for path %s", path_str)
        raise PermissionError(reason)


def denied_basename(path_str: str) -> str:
    """Basename of *path_str* (helper for filtering directory listings)."""
    segments = _path_segments(path_str)
    return segments[-1] if segments else path_str
