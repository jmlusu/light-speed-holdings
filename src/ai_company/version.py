"""Single source of truth for the ``ai-company`` package version.

Historically the dashboard duplicated a hardcoded ``"0.2.0"`` literal in
``app.py`` (FastAPI ``version=``) and ``monitoring.py`` (the ``/health``
payload) while ``pyproject.toml`` moved ahead — the two drifted and health
reports advertised a stale API version (ticket #64).

This module derives the version from one place:

1. Installed distribution metadata (``importlib.metadata.version("ai-company")``),
   which is authoritative when the package is installed.
2. ``pyproject.toml`` at the deterministic project root (via
   :func:`ai_company.paths.get_project_root`) as the fallback when the
   distribution is not installed (e.g. running from a source checkout).
3. ``"0.0.0"`` as a last resort so callers never raise.

All dashboard consumers import :func:`get_version` instead of embedding a
version literal.
"""

from __future__ import annotations

import functools
import importlib.metadata
import tomllib
from pathlib import Path

from ai_company.paths import get_project_root

_PACKAGE_NAME = "ai-company"
_UNKNOWN_VERSION = "0.0.0"


@functools.lru_cache(maxsize=1)
def get_version() -> str:
    """Return the package version, derived from a single source.

    Prefers the installed distribution metadata and falls back to the
    ``project.version`` key in ``pyproject.toml`` so a source checkout
    reports the same version as an installed one.
    """
    try:
        return importlib.metadata.version(_PACKAGE_NAME)
    except importlib.metadata.PackageNotFoundError:
        pass

    try:
        pyproject = _read_pyproject_version()
        if pyproject:
            return pyproject
    except (OSError, tomllib.TOMLDecodeError):
        pass

    return _UNKNOWN_VERSION


def _read_pyproject_version() -> str | None:
    """Return the ``project.version`` value from the project ``pyproject.toml``."""
    pyproject_path = Path(get_project_root()) / "pyproject.toml"
    if not pyproject_path.is_file():
        return None
    with pyproject_path.open("rb") as fh:
        data = tomllib.load(fh)
    version = data.get("project", {}).get("version")
    return str(version) if version else None


__all__ = ["get_version"]
