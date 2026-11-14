"""Outside-workspace allowlist + attribution logging (GO-5).

Allow (explicit):
- primary workspace ``light-speed-holdings``
- siblings ``athena``, ``social-media-automation-os`` (per-session)
- ``Temp\\opencode`` sandbox-only (scratch; retention owned elsewhere)

Deny by default:
- ``.openmausbot``, ``C:/`` root, DB/auth paths (``opencode.db*``,
  ``auth.json``, ``.local/share/opencode/**``), ``.env`` variants.

Every check emits an attribution record (path + tool + session +
project/directory, never file content) so outside ops are re-measurable
per-repo instead of one "outside" bucket.

D-1 layering: credential/DB deny is canonical in
``security/path_policy`` (delegated here); this module only adds
allowlist + attribution semantics.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.security.path_policy import is_path_denied

logger = logging.getLogger(__name__)

PRIMARY_REPO = "light-speed-holdings"
SIBLING_REPOS = ("athena", "social-media-automation-os")
SANDBOX_DIR = "temp/opencode"  # normalized suffix under AppData/Local

# Allowlist-specific deny substrings (credential/DB denies are delegated to
# path_policy.is_path_denied — single source of truth for .env/auth/db).
_DENIED_SUBSTRINGS = (
    ".openmausbot",
    ".local/share/opencode",
    "tool-output",
)


def _norm(path: str) -> str:
    return (path or "").replace("\\", "/").lower()


@dataclass
class AllowlistConfig:
    primary_repo: str = PRIMARY_REPO
    sibling_repos: tuple[str, ...] = SIBLING_REPOS
    sandbox_suffix: str = SANDBOX_DIR
    allowed_siblings_per_session: bool = True
    sandbox_write_only: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AllowlistConfig":
        data = data or {}
        allow = data.get("allow", {}) if isinstance(data.get("allow"), dict) else {}
        repos = allow.get("sibling_repos") or SIBLING_REPOS
        return cls(
            primary_repo=str(allow.get("primary_repo") or PRIMARY_REPO),
            sibling_repos=tuple(str(r) for r in repos),
            sandbox_suffix=str(allow.get("sandbox_suffix") or SANDBOX_DIR),
            allowed_siblings_per_session=bool(allow.get("allowed_siblings_per_session", True)),
            sandbox_write_only=bool(allow.get("sandbox_write_only", True)),
        )


@dataclass
class PathDecision:
    allowed: bool
    reason: str
    category: str  # primary|sibling|sandbox|denied|outside
    attribution: dict[str, Any] = field(default_factory=dict)


class PathAllowlist:
    """Validator for file paths at the read/edit/write/bash boundary."""

    def __init__(
        self,
        config: AllowlistConfig | None = None,
        *,
        session_id: str = "",
        project_id: str = "",
        directory: str = "",
    ) -> None:
        self.config = config or AllowlistConfig()
        self.session_id = session_id
        self.project_id = project_id
        self.directory = directory
        self.attribution_log: list[dict[str, Any]] = []

    def validate(
        self,
        path: str,
        tool: str = "read",
    ) -> PathDecision:
        """Validate *path* for *tool*; log attribution (never content)."""
        normalized = _norm(path)
        decision = self._decide(normalized, tool)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "project_id": self.project_id,
            "directory": self.directory,
            "tool": tool,
            "path": path,  # path only, never content
            "allowed": decision.allowed,
            "category": decision.category,
            "reason": decision.reason,
        }
        self.attribution_log.append(record)
        if not decision.allowed:
            logger.warning("Outside-allowlist path denied: %s", record)
        decision.attribution = record
        return decision

    def _decide(self, normalized: str, tool: str) -> PathDecision:
        if ".openmausbot" in normalized:
            return PathDecision(False, "denied_openmausbot", "denied")
        # Credential/DB deny delegated to path_policy (single source of
        # truth); reason strings kept generic for audit stability, the
        # specific pattern is recorded in attribution via decision reason.
        if is_path_denied(normalized):
            return PathDecision(False, "denied_db_or_auth_path", "denied")
        # Allowlist-specific substrings (DB-dir probes that are not
        # credential basenames). Credential/.env denies above already
        # cover the .env/auth/opencode.db* basenames.
        if any(s in normalized for s in _DENIED_SUBSTRINGS):
            return PathDecision(False, "denied_db_or_auth_path", "denied")
        # C:/ root probes: drive root or user-home listing with no repo.
        if normalized in ("c:/", "c:", "/") or normalized == "c:/users/jmlus":
            return PathDecision(False, "denied_drive_or_home_root", "denied")
        cfg = self.config
        if f"/{cfg.primary_repo}/" in normalized or normalized.endswith(f"/{cfg.primary_repo}"):
            return PathDecision(True, "primary_workspace", "primary")
        # Sandbox: Temp\opencode — write allowed, read only own session prefix.
        if f"/{cfg.sandbox_suffix}" in normalized or normalized.startswith(cfg.sandbox_suffix):
            if tool in ("edit", "write", "bash") or not cfg.sandbox_write_only:
                return PathDecision(True, "temp_opencode_sandbox", "sandbox")
            # Read of sandbox requires session-prefixed path.
            if self.session_id and f"/{self.session_id}/" in normalized:
                return PathDecision(True, "temp_opencode_sandbox_session", "sandbox")
            return PathDecision(False, "sandbox_read_requires_session_prefix", "sandbox")
        for repo in cfg.sibling_repos:
            if f"/{repo}/" in normalized or normalized.endswith(f"/{repo}"):
                if cfg.allowed_siblings_per_session:
                    return PathDecision(True, f"allowlisted_sibling:{repo}", "sibling")
                return PathDecision(False, f"sibling_not_per_session:{repo}", "sibling")
        return PathDecision(False, "outside_allowlist_default_deny", "outside")


def load_allowlist_config(path: str | Path) -> AllowlistConfig:
    """Load ``config/company/path_allowlist.yaml``; defaults when absent."""
    cfg_path = Path(path)
    if not cfg_path.is_file():
        return AllowlistConfig()
    try:
        import yaml

        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        return AllowlistConfig.from_dict(data)
    except (OSError, Exception):  # noqa: BLE001 - config load must never crash startup
        logger.debug(
            "Path allowlist config unreadable, using defaults: %s", cfg_path, exc_info=True
        )
        return AllowlistConfig()
