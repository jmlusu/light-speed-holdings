"""Tests for deterministic project/data root resolution (S1.1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.paths import (
    AI_COMPANY_ROOT_ENV,
    DASHBOARD_DATA_DIR_ENV,
    get_data_root,
    get_database_path,
    get_project_root,
)


@pytest.fixture(autouse=True)
def _clear_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure tests never inherit real overrides from the environment."""
    monkeypatch.delenv(AI_COMPANY_ROOT_ENV, raising=False)
    monkeypatch.delenv(DASHBOARD_DATA_DIR_ENV, raising=False)


def test_project_root_resolves_to_ai_company(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Root resolution is independent of the CWD."""
    monkeypatch.chdir(tmp_path)
    root = get_project_root()
    assert (root / "pyproject.toml").is_file()


def test_project_root_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AI_COMPANY_ROOT overrides marker-based resolution."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(AI_COMPANY_ROOT_ENV, str(tmp_path))
    assert get_project_root() == tmp_path.resolve()


def test_data_root_defaults_to_project_root(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without DASHBOARD_DATA_DIR the data root is the project root."""
    assert get_data_root() == get_project_root()


def test_data_root_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """DASHBOARD_DATA_DIR relocates the data root."""
    monkeypatch.setenv(DASHBOARD_DATA_DIR_ENV, str(tmp_path))
    assert get_data_root() == tmp_path.resolve()


def test_database_path_anchored_at_data_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The canonical DB path lives under the data root."""
    monkeypatch.setenv(DASHBOARD_DATA_DIR_ENV, str(tmp_path))
    assert get_database_path() == tmp_path.resolve() / "data" / "ai_company.db"
