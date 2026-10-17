"""Tests for deterministic project/data root resolution (S1.1)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from ai_company.paths import (
    AI_COMPANY_ROOT_ENV,
    DASHBOARD_DATA_DIR_ENV,
    get_data_root,
    get_database_path,
    get_project_root,
    state_path,
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


# ── state_path (D-6 runtime-state relocation) ────────────────────────────


def test_state_path_maps_legacy_str(tmp_path: Path) -> None:
    """Legacy orchestrator/ inputs map to data/orchestrator/ (str -> str)."""
    assert (
        state_path("orchestrator/approvals.yaml", base=tmp_path)
        == "data/orchestrator/approvals.yaml"
    )


def test_state_path_preserves_path_type(tmp_path: Path) -> None:
    """Path inputs return Path outputs."""
    resolved = state_path(Path("orchestrator/escalation.yaml"), base=tmp_path)
    assert resolved == Path("data/orchestrator/escalation.yaml")


def test_state_path_passes_through_new_form(tmp_path: Path) -> None:
    """Already-relocated inputs are returned unchanged."""
    assert (
        state_path("data/orchestrator/scheduler.yaml", base=tmp_path)
        == "data/orchestrator/scheduler.yaml"
    )


def test_state_path_passes_through_absolute(tmp_path: Path) -> None:
    """Absolute paths bypass mapping (test-provided locations stay literal)."""
    abs_path = tmp_path / "orchestrator" / "dead_letter.jsonl"
    assert state_path(abs_path, base=tmp_path) == abs_path


def test_state_path_normalizes_backslashes(tmp_path: Path) -> None:
    """Windows-style separators are normalized to POSIX form."""
    assert (
        state_path("orchestrator\\approvals.yaml", base=tmp_path)
        == "data/orchestrator/approvals.yaml"
    )


def test_state_path_migrates_legacy_tree(tmp_path: Path) -> None:
    """A legacy tree under base is moved to data/orchestrator/ on first use."""
    legacy = tmp_path / "orchestrator"
    legacy.mkdir()
    (legacy / "approvals.yaml").write_text("requests: []", encoding="utf-8")

    resolved = state_path("orchestrator/approvals.yaml", base=tmp_path)

    assert resolved == "data/orchestrator/approvals.yaml"
    assert (tmp_path / "data" / "orchestrator" / "approvals.yaml").is_file()
    assert not legacy.exists()


def test_state_path_merges_when_both_trees_exist(tmp_path: Path) -> None:
    """When both trees exist, legacy-only entries merge into the new tree."""
    legacy = tmp_path / "orchestrator"
    target = tmp_path / "data" / "orchestrator"
    legacy.mkdir()
    target.mkdir(parents=True)
    (legacy / "only_legacy.yaml").write_text("a: 1", encoding="utf-8")
    (target / "only_new.yaml").write_text("b: 2", encoding="utf-8")

    state_path("orchestrator/scheduler.yaml", base=tmp_path)

    assert (target / "only_legacy.yaml").is_file()
    assert (target / "only_new.yaml").is_file()
    assert not legacy.exists()


def test_state_path_failed_merge_rolls_back_and_keeps_legacy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed child move rolls back the partial merge; legacy stays intact."""
    legacy = tmp_path / "orchestrator"
    target = tmp_path / "data" / "orchestrator"
    legacy.mkdir()
    target.mkdir(parents=True)
    first = legacy / "first.yaml"
    locked = legacy / "locked.yaml"
    first.write_text("a: 1", encoding="utf-8")
    locked.write_text("b: 2", encoding="utf-8")

    monkeypatch.setattr(Path, "iterdir", lambda self: iter([first, locked]))
    real_rename = os.rename

    def flaky_rename(src: object, dst: object) -> None:
        if str(src).endswith("locked.yaml"):
            raise PermissionError(f"locked: {src}")
        real_rename(src, dst)  # type: ignore[arg-type]

    monkeypatch.setattr(os, "rename", flaky_rename)

    resolved = state_path("orchestrator/approvals.yaml", base=tmp_path)

    assert resolved == "orchestrator/approvals.yaml"
    assert first.is_file()
    assert locked.is_file()
    assert not (target / "first.yaml").exists()
    assert not (target / "locked.yaml").exists()
