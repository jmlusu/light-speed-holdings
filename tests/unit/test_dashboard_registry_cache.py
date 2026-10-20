"""Tests for the dashboard's cached registry reads.

The registry used to be re-read and re-parsed on every request, which
dominated the latency of the agent and org-chart endpoints. The cache is
keyed on the file's revision, so these tests pin the two properties that
matter: the file is not re-read while it is unchanged, and a change is picked
up immediately.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.dashboard import api as dash_api
from ai_company.dashboard.repository import get_state_store, reset_state_store

REGISTRY = [
    {
        "name": "chief-of-staff",
        "role": "Chief of Staff",
        "type": "executive",
        "department": "Executive",
        "reportsTo": "human-ceo",
        "directReports": ["lead-engineering"],
    },
    {
        "name": "lead-engineering",
        "role": "Lead Engineer",
        "type": "specialist",
        "department": "Engineering",
        "reportsTo": "chief-of-staff",
        "directReports": [],
    },
]


@pytest.fixture()
def registry_workspace(tmp_path: Path) -> Path:
    """Anchor the state store at an isolated workspace holding a registry."""
    reset_state_store()
    get_state_store(tmp_path)
    (tmp_path / "company").mkdir()
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(REGISTRY), encoding="utf-8"
    )
    dash_api._REGISTRY_CACHE["key"] = None
    dash_api._REGISTRY_CACHE["raw"] = None
    yield tmp_path
    reset_state_store()
    dash_api._REGISTRY_CACHE["key"] = None
    dash_api._REGISTRY_CACHE["raw"] = None


def test_registry_file_is_read_once_while_unchanged(
    registry_workspace: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Repeated reads must not re-read and re-parse the file."""
    original = dash_api._load_json
    calls: list[str] = []

    def counting_load_json(path):  # type: ignore[no-untyped-def]
        calls.append(str(path))
        return original(path)

    monkeypatch.setattr(dash_api, "_load_json", counting_load_json)

    dash_api._load_registry()
    dash_api._load_registry()
    dash_api._load_registry()

    assert calls == ["company/agent-registry.json"]


def test_registry_change_is_picked_up_immediately(registry_workspace: Path) -> None:
    """A rewritten registry must be visible on the very next read."""
    assert [a["name"] for a in dash_api._load_registry()] == [
        "chief-of-staff",
        "lead-engineering",
    ]

    changed = [
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": ["lead-engineering", "lead-marketing"],
        },
        *REGISTRY[1:],
        {
            "name": "lead-marketing",
            "role": "Marketing Lead",
            "type": "specialist",
            "department": "Marketing",
            "reportsTo": "chief-of-staff",
            "directReports": [],
        },
    ]
    (registry_workspace / "company" / "agent-registry.json").write_text(
        json.dumps(changed), encoding="utf-8"
    )

    assert "lead-marketing" in [a["name"] for a in dash_api._load_registry()]


def test_registry_camel_case_keys_are_normalized(registry_workspace: Path) -> None:
    """The cache must not skip the legacy camelCase normalization."""
    loaded = dash_api._load_registry()
    assert loaded[0]["reports_to"] == "human-ceo"
    assert "reportsTo" not in loaded[0]


def test_callers_do_not_share_mutable_state(registry_workspace: Path) -> None:
    """Each call returns its own copies, so one caller cannot poison the next."""
    first = dash_api._load_registry()
    second = dash_api._load_registry()

    assert first[0] is not second[0]
    first[0]["role"] = "mutated"
    assert dash_api._load_registry()[0]["role"] == "Chief of Staff"
