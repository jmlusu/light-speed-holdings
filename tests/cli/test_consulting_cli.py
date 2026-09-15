"""Foaster-style AI consulting CLI command tests (side-effect free).

The consulting commands persist engagements to module-level
``ENGAGEMENTS_DIR``/``MEMORY_DIR`` constants.  This project's Typer version
runs ``CliRunner`` commands in the real working directory, so every test
redirects those constants to a ``tmp_path`` via monkeypatch to guarantee no
real ``consulting/`` or ``memory/`` repository state is ever written.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from ai_company.cli.consulting import app
from ai_company.memory.engine import MemoryStore

runner = CliRunner()


def _start_engagement(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *args: str,
) -> str:
    """Start an engagement in an isolated tmp dir and return its ID."""
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    result = runner.invoke(app, ["start", *args])
    assert result.exit_code == 0
    match = re.search(r"with ID '([^']+)'\.", result.stdout)
    assert match is not None
    return match.group(1)


def _load_engagements(tmp_path: Path) -> list[dict[str, Any]]:
    """Read engagements from the isolated tmp dir."""
    import yaml

    file = tmp_path / "engagements.yaml"
    data = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
    return list(data.get("engagements", []))


def _completed_engagement_data(client_id: str = "acme") -> dict[str, Any]:
    """Return a minimally completed engagement dict for pre-seeding."""
    return {
        "id": "eng_seeded",
        "client_id": client_id,
        "name": "Seed Co",
        "scope": "ai_transformation",
        "departments": ["eng"],
        "status": "completed",
        "current_step": "client_presentation",
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00",
        "steps_completed": ["onboarding"],
        "interview_results": [],
        "workflow_maps": [],
        "opportunities": [],
        "roadmap": None,
        "client_feedback": "Great work",
        "roadmap_approved": True,
        "expert_feedback": "Looks good",
    }


def test_start_creates_engagement(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    engagement_id = _start_engagement(
        monkeypatch, tmp_path, "--client", "acme", "--name", "Test Co"
    )
    engagements = _load_engagements(tmp_path)
    assert len(engagements) == 1
    eng = engagements[0]
    assert eng["id"] == engagement_id
    assert eng["client_id"] == "acme"
    assert eng["name"] == "Test Co"
    assert eng["status"] == "onboarding"
    assert eng["current_step"] == "onboarding"
    assert eng["departments"] == ["all"]
    assert "eng_" in engagement_id


def test_start_with_departments_splits_list(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _start_engagement(
        monkeypatch,
        tmp_path,
        "--client",
        "acme",
        "--name",
        "Multi Depts",
        "--departments",
        "eng,ops,sales",
    )
    eng = _load_engagements(tmp_path)[0]
    assert eng["departments"] == ["eng", "ops", "sales"]


def test_list_engagements_empty(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    result = runner.invoke(app, ["list-engagements"])
    assert result.exit_code == 0
    assert "No consulting engagements found." in result.stdout


def test_status_nonexistent_engagement_exits_1(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    result = runner.invoke(app, ["status", "--engagement", "eng_missing"])
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()


def test_full_lifecycle_happy_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    monkeypatch.setattr("ai_company.cli.consulting.MEMORY_DIR", tmp_path / "memory")

    eng_id = _start_engagement(monkeypatch, tmp_path, "--client", "acme", "--name", "Lifecycle")

    steps: list[tuple[str, list[str]]] = [
        ("deploy-interviews", ["--engagement", eng_id]),
        ("synthesize", ["--engagement", eng_id]),
        ("identify", ["--engagement", eng_id]),
        ("draft", ["--engagement", eng_id]),
        ("review", ["--engagement", eng_id, "--approve"]),
        ("present", ["--engagement", eng_id]),
        ("feed-knowledge", ["--engagement", eng_id]),
    ]
    for command, args in steps:
        result = runner.invoke(app, [command, *args])
        assert result.exit_code == 0, f"{command} failed: {result.stdout}"

    eng = _load_engagements(tmp_path)[0]
    assert eng["status"] == "completed"
    assert eng["current_step"] == "client_presentation"
    assert eng["knowledge_fed"] is True


def test_feed_knowledge_uses_supported_memory_types(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Regression: feed-knowledge must not crash on 'Unknown memory type: feedback'."""
    from ai_company.cli.consulting import _save_engagements_file

    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    monkeypatch.setattr("ai_company.cli.consulting.MEMORY_DIR", tmp_path / "memory")
    _save_engagements_file({"engagements": [_completed_engagement_data()]})

    result = runner.invoke(app, ["feed-knowledge", "--engagement", "eng_seeded"])
    assert result.exit_code == 0, result.stdout
    assert "Learnings fed to knowledge base" in result.stdout

    store = MemoryStore(base_dir=str(tmp_path / "memory"))
    assert store.count() >= 1
    entries = store.search("")
    assert any("consulting" in e.tags for e in entries)


def test_review_without_approve_or_reject_exits_1(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from ai_company.cli.consulting import _save_engagements_file

    eng = _completed_engagement_data()
    eng["status"] = "reviewed"
    eng["current_step"] = "draft_roadmap"
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    _save_engagements_file({"engagements": [eng]})

    result = runner.invoke(app, ["review", "--engagement", "eng_seeded"])
    assert result.exit_code == 1
    assert "Must specify --approve or --reject" in result.stdout


def test_synthesize_wrong_state_exits_1(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from ai_company.cli.consulting import _save_engagements_file

    eng = _completed_engagement_data()
    eng["status"] = "onboarding"
    eng["current_step"] = "onboarding"
    monkeypatch.setattr("ai_company.cli.consulting.ENGAGEMENTS_DIR", tmp_path)
    _save_engagements_file({"engagements": [eng]})

    result = runner.invoke(app, ["synthesize", "--engagement", "eng_seeded"])
    assert result.exit_code == 1
    assert "must be in 'deploy_interviews' state" in result.stdout
