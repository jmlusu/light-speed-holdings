"""Tests for the opt-in ``storage import-opencode`` mirror command (ADR-011)."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()


def _seed_opencode(data_root: Path) -> None:
    """Write a small legacy `.opencode/` payload (tasks + audit events)."""
    opencode = data_root / ".opencode"
    opencode.mkdir(parents=True, exist_ok=True)
    (opencode / "inbox.json").write_text(
        json.dumps(
            [
                {
                    "id": "t-1",
                    "name": "task one",
                    "sender_id": "orchestrator",
                    "receiver_id": "ceo",
                    "instruction": "do it",
                    "status": "pending",
                },
                {
                    "id": "t-2",
                    "name": "task two",
                    "sender_id": "orchestrator",
                    "receiver_id": "cfo",
                    "instruction": "budget",
                    "status": "pending",
                },
            ]
        ),
        encoding="utf-8",
    )
    lines = [
        {
            "event_id": "e-1",
            "timestamp": "2026-08-12T00:00:00+00:00",
            "event_type": "task_created",
            "agent_id": "orchestrator",
            "task_id": "t-1",
        },
        {
            "event_id": "e-2",
            "timestamp": "2026-08-12T00:00:01+00:00",
            "event_type": "task_completed",
            "agent_id": "ceo",
            "task_id": "t-1",
        },
    ]
    (opencode / "audit.jsonl").write_text(
        "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
    )


def _run_import(tmp_path: Path) -> tuple[object, Path]:
    db = tmp_path / "data" / "ai_company.db"
    result = runner.invoke(
        app,
        [
            "storage",
            "import-opencode",
            "--data-root",
            str(tmp_path),
            "--database",
            str(db),
        ],
    )
    return result, db


def test_import_opencode_mirrors_tasks_and_audit(tmp_path: Path) -> None:
    _seed_opencode(tmp_path)
    result, db = _run_import(tmp_path)

    assert result.exit_code == 0, result.output
    assert "Imported 2 task(s) and 2 audit event(s)" in result.output
    assert "left unchanged" in result.output
    assert db.exists()


def test_import_opencode_is_idempotent(tmp_path: Path) -> None:
    _seed_opencode(tmp_path)
    result1, db = _run_import(tmp_path)
    assert result1.exit_code == 0, result1.output

    result2, _ = _run_import(tmp_path)
    assert result2.exit_code == 0, result2.output
    assert "Imported 2 task(s) and 2 audit event(s)" in result2.output


def test_import_opencode_missing_files_is_graceful(tmp_path: Path) -> None:
    result, db = _run_import(tmp_path)
    assert result.exit_code == 0, result.output
    assert "Imported 0 task(s) and 0 audit event(s)" in result.output
    assert db.exists()
