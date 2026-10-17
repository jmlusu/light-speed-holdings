"""Hardening configuration loader (``company/config/hardening.yaml``).

Loads ops reliability thresholds for the hardening layer, merging the YAML
file over the catalog defaults (``docs/HARDENING-PATTERN-CATALOG.md`` §4) so
the file is the single source of truth at runtime while the catalog stays the
source of truth in code.

The org-health *domain* config (``config/org_health.yaml``) stays separate —
it owns band/component domain thresholds; this module owns *ops* reliability
parameters.
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

import yaml

from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)

# Catalog defaults (§4 of docs/HARDENING-PATTERN-CATALOG.md). New subsystems
# (`daemon`, `scheduler`, `message_bus`, `audit`) are added by their tickets.
HARDENING_DEFAULTS: dict[str, Any] = {
    "org_health": {
        "call_timeout_s": 3.0,
        "compute_timeout_s": 15.0,
        "worker_pool_size": 4,
        "dedup_window_s": 5.0,
        "breaker": {
            "failure_threshold": 3,
            "recovery_timeout_s": 60.0,
            "success_threshold": 1,
        },
    },
}


def load_hardening_config(project_root: Any = None) -> dict[str, Any]:
    """Return the hardening config merged over catalog defaults.

    A missing file, YAML error, or non-mapping document falls back to the
    defaults with a warning — the hardening layer must never crash on a config
    problem.
    """
    from pathlib import Path

    root = Path(project_root) if project_root else get_project_root()
    path = root / "company" / "config" / "hardening.yaml"
    if not path.is_file():
        return deepcopy(HARDENING_DEFAULTS)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("Failed to load hardening config %s: %s", path, exc)
        return deepcopy(HARDENING_DEFAULTS)
    if not isinstance(raw, dict):
        logger.warning("Hardening config %s is not a mapping; using defaults", path)
        return deepcopy(HARDENING_DEFAULTS)
    return _deep_merge(deepcopy(HARDENING_DEFAULTS), raw)


def get_hardening_value(config: dict[str, Any], dotted_path: str, default: Any = None) -> Any:
    """Look up a nested value by dotted path.

    Example: ``get_hardening_value(cfg, "org_health.breaker.failure_threshold")``.
    """
    node: Any = config
    for part in dotted_path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* onto *base* (later wins)."""
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _deep_merge(base[key], value)
        else:
            base[key] = value
    return base
