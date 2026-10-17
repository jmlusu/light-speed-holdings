"""Tests for the single-source package version (ticket #64).

The dashboard previously hardcoded ``"0.2.0"`` in ``app.py`` and
``monitoring.py`` while ``pyproject.toml`` moved to ``0.5.0``. Every version
consumer must now derive from :func:`ai_company.version.get_version`.
"""

from __future__ import annotations

import importlib.metadata
import tomllib
from pathlib import Path

import pytest

import ai_company.version as version_mod
from ai_company.paths import get_project_root
from ai_company.version import get_version


def _pyproject_version() -> str:
    """Read the canonical version from ``pyproject.toml``."""
    pyproject = Path(get_project_root()) / "pyproject.toml"
    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)
    return data["project"]["version"]


def test_version_matches_pyproject() -> None:
    """The derived version agrees with pyproject.toml (not the stale 0.2.0)."""
    version_mod.get_version.cache_clear()
    try:
        assert get_version() == _pyproject_version()
        assert get_version() != "0.2.0"
    finally:
        version_mod.get_version.cache_clear()


def test_version_uses_installed_metadata_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    """Installed distribution metadata is authoritative when present."""
    version_mod.get_version.cache_clear()
    monkeypatch.setattr(
        version_mod.importlib.metadata,
        "version",
        lambda name: "9.9.9",
    )
    try:
        assert get_version() == "9.9.9"
    finally:
        version_mod.get_version.cache_clear()


def test_version_falls_back_to_pyproject_when_not_installed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A source checkout (no installed metadata) still reports pyproject's version."""

    def _raise(name: str) -> str:
        raise importlib.metadata.PackageNotFoundError(name)

    version_mod.get_version.cache_clear()
    monkeypatch.setattr(version_mod.importlib.metadata, "version", _raise)
    try:
        assert get_version() == _pyproject_version()
    finally:
        version_mod.get_version.cache_clear()


def test_fastapi_app_version_derived_from_single_source() -> None:
    """The FastAPI app's ``version`` field must derive from get_version()."""
    from ai_company.dashboard.app import create_app

    app = create_app()
    assert app.version == get_version()
    assert app.version != "0.2.0"
