"""Deterministic project-root and data-root resolution.

The dashboard and its KPI collectors historically resolved the project root
relative to the process working directory (``Path(__file__).resolve().parents[3]``
or ``"."``), which made real operational data invisible depending on where the
server was launched.  This module is the single source of truth for resolving
the ``ai-company`` project root and the runtime data root.

Resolution order for the project root:

1. ``AI_COMPANY_ROOT`` environment variable (explicit override).
2. The nearest ancestor of this package containing a project marker
   (``company-registry.yaml`` or ``pyproject.toml``).
3. The current working directory (last-resort fallback).

The data root defaults to the project root and can be overridden with
``DASHBOARD_DATA_DIR`` for deployments that keep runtime state elsewhere.
"""

from __future__ import annotations

import os
from pathlib import Path

AI_COMPANY_ROOT_ENV = "AI_COMPANY_ROOT"
DASHBOARD_DATA_DIR_ENV = "DASHBOARD_DATA_DIR"

# Files that uniquely identify the ai-company project root.  The package tree
# walks upward until one of these is found.
_PROJECT_MARKERS = ("company-registry.yaml", "pyproject.toml")


def get_project_root() -> Path:
    """Return the ai-company project root, independent of the CWD.

    Honour ``AI_COMPANY_ROOT`` when set, then walk up from this package looking
    for a project marker, finally falling back to the current working directory.
    """
    env_root = os.environ.get(AI_COMPANY_ROOT_ENV)
    if env_root:
        return Path(env_root).resolve()

    pkg = Path(__file__).resolve().parent
    for candidate in (pkg, *pkg.parents):
        if any((candidate / marker).is_file() for marker in _PROJECT_MARKERS):
            return candidate

    return Path.cwd().resolve()


def get_data_root() -> Path:
    """Return the root that runtime data files live under.

    Defaults to :func:`get_project_root`; override with ``DASHBOARD_DATA_DIR``.
    """
    data_dir = os.environ.get(DASHBOARD_DATA_DIR_ENV)
    if data_dir:
        return Path(data_dir).resolve()
    return get_project_root()


def get_database_path() -> Path:
    """Return the canonical SQLite database path for the data root.

    Anchored at ``data/ai_company.db`` under :func:`get_data_root` so the
    dashboard and the ``backfill`` CLI always share one database regardless
    of the CWD.
    """
    return get_data_root() / "data" / "ai_company.db"


__all__ = [
    "AI_COMPANY_ROOT_ENV",
    "DASHBOARD_DATA_DIR_ENV",
    "get_data_root",
    "get_database_path",
    "get_project_root",
]
