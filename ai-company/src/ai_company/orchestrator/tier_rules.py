"""Rules for mapping tool actions to approval tiers.

Each tool action is classified into one of five tiers:
    Tier 0 (Auto-Approve): read-only operations; no human approval needed.
    Tier 1 (Notify): low-risk writes; auto-approved but humans are notified.
    Tier 2 (Single Approver): code changes, test execution; one human must approve.
    Tier 3 (Two-Person Rule): production deployments, database changes; two humans must approve.
    Tier 4 (CEO Only): financial/legal/security actions; CEO must approve.

The classification considers the tool type, arguments (sensitive paths, commands),
the requesting agent's seniority, and the current task context.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Any

# ---------------------------------------------------------------------------
# Approval tiers
# ---------------------------------------------------------------------------


class ApprovalTier(IntEnum):
    """Approval tiers from fully automatic (0) to CEO-only (4).

    Higher number = stricter approval requirements.
    """

    AUTO_APPROVE = 0
    NOTIFY = 1
    SINGLE_APPROVER = 2
    TWO_PERSON = 3
    CEO_ONLY = 4


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Path fragments that automatically escalate to CEO-only (Tier 4).
SENSITIVE_PATHS: tuple[str, ...] = (
    "/secrets/",
    "/secret/",
    "/.env",
    "config/secrets.yaml",
    "config/credentials",
    "private_key",
    "security/",
    "audit/",
    "legal/",
    "compliance/",
)

# Path fragments that escalate to Two-Person Rule (Tier 3).
PRODUCTION_PATHS: tuple[str, ...] = (
    "/production/",
    "/prod/",
    "deploy/",
    "terraform/",
    "k8s/",
    "k8/",
    "helm/",
    "docker-compose",
    "Dockerfile",
    "Makefile",
    "scripts/deploy",
)

# Path fragments that require single approver (Tier 2).
CODE_PATHS: tuple[str, ...] = (
    "src/",
    "tests/",
    "app/",
    "lib/",
    "handler/",
    "service/",
    "repository/",
    "controller/",
    "routes/",
    "api/",
    "requirements",
    "pyproject.toml",
    "pom.xml",
    "package.json",
)

# Path fragments for config/low-risk writes (Tier 1).
# These are paths where a write action is inherently low-risk.
CONFIG_PATHS: tuple[str, ...] = (
    "config/",
    ".github/",
    ".vscode/",
    "docs/",
    # Explicit file patterns — we match suffixes for these so that
    # "CHANGELOG.md" is recognised as low-risk.
    ".md",
    ".rst",
    # Config-file extensions that are clearly not source code.
    "setup.cfg",
    "tox.ini",
    ".editorconfig",
    ".gitignore",
    ".gitattributes",
)

# Commands that escalate to CEO-only (Tier 4).
DANGEROUS_COMMANDS: tuple[str, ...] = (
    "rm -rf",
    "drop table",
    "drop database",
    "truncate table",
    "delete from",
    "sudo rm",
    "shutdown",
    "reboot",
    "chmod 777",
    "chown -R",
    "dd if=",
    "> /dev/",  # Dangerous redirect
    ":(){ :|:& };:",  # Fork bomb
    "curl.*|.*sh",  # Pipe-to-shell
    "chmod -R 777",
    "mv /",  # Moving root (or glob that matches root-level)
    "rm /",  # Removing root
    "> /etc/",
    "> /boot/",
    "format",
)

# Commands that escalate to Two-Person Rule (Tier 3).
PRODUCTION_COMMANDS: tuple[str, ...] = (
    "docker push",
    "kubectl apply",
    "helm upgrade",
    "terraform apply",
    "terraform destroy",
    "aws ecs update-service",
    "gcloud run deploy",
    "az webapp deploy",
    "npm publish",
    "twine upload",
    "pip install --upgrade",  # Global package upgrade
    "yarn publish",
    "git push --tags",  # Can trigger deploy pipelines
    "bundle exec cap",
    "fly deploy",
    "vercel --prod",
    "netlify deploy --prod",
)

# Path fragments for sensitive secret checks.
SECRET_PATH_FRAGMENTS: tuple[str, ...] = (
    "secret",
    "credential",
    "password",
    "token",
    "key",
    "cert",
    "pem",
    "pfx",
    "jks",
    "keystore",
    "vault",
    ".pem",
    ".key",
)

# Seniority level thresholds.
# Each entry maps seniority -> the highest tier the agent can bypass.
# e.g., "executive" can auto-approve tiers <= 2 (SINGLE_APPROVER).
SENIORITY_AUTO_APPROVE_TIER: dict[str, int] = {
    "junior": 0,  # Must go through approval for anything beyond auto
    "mid": 1,  # Can auto-approve notify-level
    "senior": 1,  # Same as mid (for now)
    "lead": 2,  # Can auto-approve single-approver
    "executive": 2,  # Can auto-approve single-approver
}

# Default tiers for each tool type.
TOOL_DEFAULT_TIERS: dict[str, ApprovalTier] = {
    "read": ApprovalTier.AUTO_APPROVE,
    "list": ApprovalTier.AUTO_APPROVE,
    "grep": ApprovalTier.AUTO_APPROVE,
    "write": ApprovalTier.SINGLE_APPROVER,
    "execute": ApprovalTier.SINGLE_APPROVER,
    "code_interpreter": ApprovalTier.SINGLE_APPROVER,
    "delegate": ApprovalTier.NOTIFY,
    "edit": ApprovalTier.SINGLE_APPROVER,
    "glob": ApprovalTier.AUTO_APPROVE,
    "search": ApprovalTier.AUTO_APPROVE,
    "ping": ApprovalTier.AUTO_APPROVE,
    "view": ApprovalTier.AUTO_APPROVE,
}

# Per-tier configuration.
TIER_CONFIG: dict[ApprovalTier, dict[str, Any]] = {
    ApprovalTier.AUTO_APPROVE: {
        "label": "Auto-Approve",
        "description": "No human approval needed; operation runs immediately.",
        "required_approvers": 0,
        "timeout_minutes": 0,
        "notify": False,
        "notify_channels": [],
    },
    ApprovalTier.NOTIFY: {
        "label": "Notify",
        "description": "Low-risk write; auto-approved but humans are notified.",
        "required_approvers": 0,
        "timeout_minutes": 0,
        "notify": True,
        "notify_channels": ["slack", "email"],
    },
    ApprovalTier.SINGLE_APPROVER: {
        "label": "Single Approver",
        "description": "Code or test change; one human must approve.",
        "required_approvers": 1,
        "timeout_minutes": 240,  # 4 hours
        "notify": True,
        "notify_channels": ["slack", "email"],
    },
    ApprovalTier.TWO_PERSON: {
        "label": "Two-Person Rule",
        "description": "Production or DB change; two humans must approve.",
        "required_approvers": 2,
        "timeout_minutes": 120,  # 2 hours
        "notify": True,
        "notify_channels": ["slack", "email", "pager"],
    },
    ApprovalTier.CEO_ONLY: {
        "label": "CEO Only",
        "description": "Financial, legal, or security action; CEO must approve.",
        "required_approvers": 1,
        "timeout_minutes": 60,  # 1 hour
        "notify": True,
        "notify_channels": ["slack", "email", "pager", "sms"],
    },
}


# ---------------------------------------------------------------------------
# Classification logic
# ---------------------------------------------------------------------------


# Argument keys that are expected to carry a filesystem path.
_PATH_KEYS: frozenset[str] = frozenset(
    {"path", "file_path", "filePath", "filename", "files", "target", "destination", "source"}
)

# Documentation file suffixes.  A documentation file is a design artifact,
# not a code/deploy/secret operation — directory-name fragments must not
# escalate it to Tier 2/3/4.
_DOC_SUFFIXES: tuple[str, ...] = (".md", ".rst")

# Explicit secret-file indicators that escalate to Tier 4 even for
# documentation-looking paths.  These are concrete secret-file references
# (never a design-doc path), so they keep their protection unconditionally.
SECRET_FILE_PATTERNS: tuple[str, ...] = (
    "/.env",
    "/secrets/",
    "/secret/",
    "config/secrets.yaml",
    "config/credentials",
    "private_key",
)


def _is_documentation_file(candidate_lower: str) -> bool:
    """True when the candidate is a documentation artifact (markdown/rst or under docs/)."""
    return candidate_lower.endswith(_DOC_SUFFIXES) or "docs/" in candidate_lower


def _check_sensitive_path(args: dict[str, Any], tool: str = "") -> int:
    """Return the target tier classification based on path arguments.

    Unlike a pure escalation function, this returns the *appropriate* tier
    for the most sensitive path found. Config-only paths (Tier 1) can
    lower the default write tier (2), while sensitive/production paths
    raise it.

    Documentation artifacts (``.md``/``.rst`` files or paths under ``docs/``)
    are design deliverables: directory-name fragments such as ``security/``,
    ``api/`` or ``deploy/`` describe the *topic* of the document, not an
    operation on code/secrets/production, so they do not escalate.  Explicit
    secret-file indicators (``.env``, ``/secrets/``, ``config/credentials``,
    ``private_key``, ...) escalate to Tier 4 unconditionally.

    For ``write``/``edit`` only values under path-bearing keys are inspected —
    free-form prose (e.g. a write ``content`` body that mentions ``security/``
    or ``Vault/K8s``) is not treated as a path.  For ``execute``/
    ``code_interpreter`` every string is inspected because commands and code
    embed file paths inline (e.g. ``cat config/secrets/api_key.txt``).

    Returns:
        - 4 if the path matches a CEO-only pattern
        - 3 if the path matches a production/Tier-3 pattern
        - 2 if the path matches a code/Tier-2 pattern (same as write default)
        - 1 if the path matches a config/Tier-1 pattern (de-escalates write)
        - 0 if no special path pattern is matched
    """
    # Collect string arguments that could be file paths.
    candidates: list[str] = []
    if tool in ("execute", "code_interpreter"):
        # Commands/code embed paths inline — inspect every string value.
        for v in args.values():
            if isinstance(v, str):
                candidates.append(v)
            elif isinstance(v, list):
                candidates.extend(x for x in v if isinstance(x, str))
            elif isinstance(v, dict):
                candidates.extend(x for x in v.values() if isinstance(x, str))
    else:
        # File-writing tools: only values under path-bearing keys are
        # inspected — content prose is never treated as a path.
        for key, v in args.items():
            if key not in _PATH_KEYS:
                continue
            if isinstance(v, str):
                candidates.append(v)
            elif isinstance(v, list):
                candidates.extend(x for x in v if isinstance(x, str))
            elif isinstance(v, dict):
                candidates.extend(x for x in v.values() if isinstance(x, str))

    max_tier = 0
    for candidate in candidates:
        candidate_lower = candidate.lower()
        is_doc = _is_documentation_file(candidate_lower)

        # Explicit secret-file indicators ALWAYS escalate (Tier 4), even for
        # documentation-looking paths (e.g. ``private_key.md``, ``docs/.env``).
        for pattern in SECRET_FILE_PATTERNS:
            if pattern.lower() in candidate_lower:
                max_tier = max(max_tier, 4)

        if is_doc:
            # Documentation artifacts are design deliverables — directory-name
            # fragments do not escalate them.  The config/doc de-escalation
            # below still applies so they land at Tier 1 (Notify).
            if max_tier < 2:
                for pattern in CONFIG_PATHS:
                    pattern_lower = pattern.lower()
                    # Suffix patterns like ".md" match the end of a filename.
                    if pattern_lower.startswith("."):
                        if candidate_lower.endswith(pattern_lower):
                            max_tier = max(max_tier, 1)
                    # Directory/file patterns like "docs/" match anywhere.
                    elif pattern_lower in candidate_lower:
                        max_tier = max(max_tier, 1)
            continue

        # Check sensitive/secret paths (Tier 4).
        for pattern in SENSITIVE_PATHS:
            if pattern.lower() in candidate_lower:
                max_tier = max(max_tier, 4)

        # Check production paths (Tier 3).
        for pattern in PRODUCTION_PATHS:
            if pattern.lower() in candidate_lower:
                max_tier = max(max_tier, 3)

        # Check code paths (Tier 2).
        for pattern in CODE_PATHS:
            if pattern.lower() in candidate_lower:
                max_tier = max(max_tier, 2)

        # Check config paths (Tier 1) — only if nothing more specific matched.
        if max_tier < 2:
            for pattern in CONFIG_PATHS:
                pattern_lower = pattern.lower()
                # Suffix patterns like ".md" match the end of a filename.
                if pattern_lower.startswith("."):
                    if candidate_lower.endswith(pattern_lower):
                        max_tier = max(max_tier, 1)
                # Directory/file patterns like "config/" match anywhere in the path.
                elif pattern_lower in candidate_lower:
                    max_tier = max(max_tier, 1)

    return max_tier


def _check_command_sensitivity(command: str) -> int:
    """Return the escalation tier for a command string.

    Returns:
        - 4 for dangerous commands
        - 3 for production commands
        - 0 otherwise
    """
    cmd_lower = command.lower().strip()

    # Check dangerous commands (Tier 4).
    for pattern in DANGEROUS_COMMANDS:
        if pattern.lower() in cmd_lower:
            return 4

    # Check production commands (Tier 3).
    for pattern in PRODUCTION_COMMANDS:
        if pattern.lower() in cmd_lower:
            return 3

    return 0


def classify_tool_action(
    tool: str,
    args: dict[str, Any],
    agent_id: str = "",
    task_context: dict[str, Any] | None = None,
) -> ApprovalTier:
    """Classify a tool action into an approval tier.

    The classification considers:
    - The default tier for the tool type
    - Path sensitivity (writes to sensitive/production paths escalate)
    - Command sensitivity (``rm -rf``, ``drop table``, etc. escalate)
    - Agent seniority (executives can bypass lower tiers)
    - Task context (high-risk tasks may force stricter tiers)

    Parameters
    ----------
    tool:
        The tool name (e.g. ``read``, ``write``, ``execute``).
    args:
        The arguments dict for the tool action.
    agent_id:
        The agent performing the action (used for seniority lookup).
    task_context:
        Optional task-level metadata (e.g. ``{"risk_level": "high"}``).

    Returns
    -------
    ApprovalTier
        The approval tier for this action.
    """
    context = task_context or {}

    # Get the default tier for this tool.
    default_tier = TOOL_DEFAULT_TIERS.get(tool, ApprovalTier.SINGLE_APPROVER)
    raw_tier = int(default_tier)

    # Path-based analysis (applies to write, edit, code_interpreter, execute).
    # The path tier can both escalate (for sensitive paths) and de-escalate
    # (for config/doc paths that are inherently low-risk).
    if tool in ("write", "edit", "code_interpreter", "execute"):
        path_tier = _check_sensitive_path(args, tool=tool)
        if path_tier > 0:
            # Path tier fully determines the raw tier for sensitive/production
            # paths (escalate) and for config/doc paths (de-escalate).
            raw_tier = path_tier

    # Command-based escalation (applies to execute).
    if tool == "execute" and "command" in args:
        cmd = args["command"]
        if isinstance(cmd, str):
            command_tier = _check_command_sensitivity(cmd)
            raw_tier = max(raw_tier, command_tier)

    # Task-level risk context can escalate the tier by one level.
    risk_level = context.get("risk_level", "low")
    if risk_level == "high" and raw_tier >= 2:
        raw_tier = max(raw_tier, 3)
    elif risk_level == "critical":
        raw_tier = max(raw_tier, 4)

    # Seniority can de-escalate for known seniority values.
    seniority = context.get("seniority", "")
    if seniority and seniority in SENIORITY_AUTO_APPROVE_TIER:
        max_auto_approve = SENIORITY_AUTO_APPROVE_TIER[seniority]
        # Only de-escalate if the raw tier is within the agent's authority.
        if raw_tier <= max_auto_approve:
            raw_tier = min(raw_tier, ApprovalTier.NOTIFY if raw_tier > 0 else 0)

    # Clamp to valid range.
    return ApprovalTier(max(0, min(raw_tier, 4)))


def get_tier_config(tier: ApprovalTier) -> dict[str, Any]:
    """Get configuration for a specific approval tier.

    Parameters
    ----------
    tier:
        The approval tier to retrieve configuration for.

    Returns
    -------
    dict[str, Any]
        A dictionary with keys: ``label``, ``description``, ``required_approvers``,
        ``timeout_minutes``, ``notify``, ``notify_channels``.
    """
    return TIER_CONFIG.get(tier, TIER_CONFIG[ApprovalTier.SINGLE_APPROVER])
