"""Tests for the onboarding integration module (Issue #29)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_company.hr.onboarding import (
    OnboardingManager,
    OnboardingRequest,
    OnboardingStatus,
    _request_to_registry_entry,
)


@pytest.fixture()
def sample_registry(tmp_path: Path) -> Path:
    """Create a minimal company-registry.yaml for testing."""
    data = {
        "company": {
            "name": "Test Corp",
            "agents": [
                {
                    "id": "cto",
                    "name": "CTO",
                    "title": "Chief Technology Officer",
                    "type": "executive",
                    "department": "Technology",
                    "reports_to": "chief_of_staff",
                    "responsibilities": ["Lead engineering"],
                    "tools": ["read", "write", "execute"],
                },
                {
                    "id": "lead_backend",
                    "name": "Lead Backend Engineer",
                    "title": "Lead Backend",
                    "type": "specialist",
                    "department": "Technology",
                    "reports_to": "cto",
                    "responsibilities": ["Build APIs"],
                    "tools": ["read", "write", "execute", "grep"],
                },
            ],
        }
    }
    registry_path = tmp_path / "company-registry.yaml"
    registry_path.write_text(yaml.dump(data), encoding="utf-8")
    return registry_path


@pytest.fixture()
def manager(sample_registry: Path, tmp_path: Path) -> OnboardingManager:
    return OnboardingManager(
        registry_path=str(sample_registry),
        templates_dir=str(Path(__file__).resolve().parents[2] / "templates"),
        output_dir=str(tmp_path / "agents"),
        approval_config_path=str(tmp_path / "approvals.yaml"),
    )


def _make_manager(tmp_path: Path | None = None) -> OnboardingManager:
    """Create an OnboardingManager isolated from the production approvals.yaml."""
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    return OnboardingManager(
        registry_path="/dev/null",
        approval_config_path=str(tmp_path / "approvals.yaml"),
    )


def _make_request(**overrides: object) -> OnboardingRequest:
    defaults = {
        "request_id": "req-001",
        "agent_id": "data_engineer",
        "name": "Data Engineer",
        "role": "Data Engineer",
        "department": "Data",
        "agent_type": "specialist",
        "reports_to": "cto",
        "responsibilities": ["Build pipelines"],
        "tools": ["read", "write", "execute"],
    }
    defaults.update(overrides)
    return OnboardingRequest(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# OnboardingRequest tests
# ---------------------------------------------------------------------------


def test_request_defaults() -> None:
    req = _make_request()
    assert req.status == OnboardingStatus.REQUESTED
    assert req.created_at != ""
    assert req.updated_at != ""


def test_request_to_registry_entry() -> None:
    req = _make_request()
    entry = _request_to_registry_entry(req)
    assert entry["id"] == "data_engineer"
    assert entry["name"] == "Data Engineer"
    assert entry["type"] == "specialist"
    assert entry["department"] == "Data"
    assert entry["reports_to"] == "cto"
    assert entry["tools"] == ["read", "write", "execute"]


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------


def test_validate_valid_entry(manager: OnboardingManager) -> None:
    req = _make_request()
    errors = manager.validate_draft(req)
    assert errors == []


def test_validate_duplicate_id(manager: OnboardingManager) -> None:
    req = _make_request(agent_id="cto")
    errors = manager.validate_draft(req)
    assert any("already exists" in e for e in errors)


def test_validate_missing_agent_id(manager: OnboardingManager) -> None:
    req = _make_request(agent_id="")
    errors = manager.validate_draft(req)
    assert any("agent_id" in e for e in errors)


def test_validate_missing_name(manager: OnboardingManager) -> None:
    req = _make_request(name="")
    errors = manager.validate_draft(req)
    assert any("name" in e for e in errors)


def test_validate_missing_department(manager: OnboardingManager) -> None:
    req = _make_request(department="")
    errors = manager.validate_draft(req)
    assert any("department" in e for e in errors)


def test_validate_invalid_reports_to(manager: OnboardingManager) -> None:
    req = _make_request(reports_to="nonexistent_agent")
    errors = manager.validate_draft(req)
    assert any("reports_to" in e for e in errors)


def test_validate_invalid_agent_type(manager: OnboardingManager) -> None:
    req = _make_request(agent_type="invalid")
    errors = manager.validate_draft(req)
    assert any("agent_type" in e for e in errors)


def test_validate_reports_to_by_name(manager: OnboardingManager) -> None:
    req = _make_request(reports_to="CTO")
    errors = manager.validate_draft(req)
    assert errors == []


# ---------------------------------------------------------------------------
# Registry integration tests
# ---------------------------------------------------------------------------


def test_add_to_registry(manager: OnboardingManager, sample_registry: Path) -> None:
    req = _make_request()
    result = manager.add_to_registry(req)
    assert result is True

    data = yaml.safe_load(sample_registry.read_text(encoding="utf-8"))
    agents = data["company"]["agents"]
    new_agent = next(a for a in agents if a["id"] == "data_engineer")
    assert new_agent["name"] == "Data Engineer"
    assert new_agent["department"] == "Data"


def test_add_to_registry_validation_failure(
    manager: OnboardingManager, sample_registry: Path
) -> None:
    req = _make_request(agent_id="cto")
    result = manager.add_to_registry(req)
    assert result is False

    data = yaml.safe_load(sample_registry.read_text(encoding="utf-8"))
    agents = data["company"]["agents"]
    assert sum(1 for a in agents if a["id"] == "cto") == 1


def test_backup_created_on_generate(manager: OnboardingManager, sample_registry: Path) -> None:
    req = _make_request()
    manager.generate(req)

    backups = list(sample_registry.parent.glob("company-registry.yaml.bak.*"))
    assert len(backups) >= 1


def test_generate_produces_agent_file(manager: OnboardingManager, sample_registry: Path) -> None:
    req = _make_request()
    generated = manager.generate(req)

    assert len(generated) >= 1
    agent_files = [f for f in generated if "data-engineer" in f.name]
    assert len(agent_files) == 1

    content = agent_files[0].read_text(encoding="utf-8")
    assert "Data Engineer" in content
    assert "permission:" in content


def test_generate_rolls_back_on_failure(
    manager: OnboardingManager, sample_registry: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_content = sample_registry.read_text(encoding="utf-8")
    req = _make_request()

    def broken_generate_all(self_gen: object) -> list[Path]:
        raise RuntimeError("Simulated generation failure")

    from ai_company.generator import AgentGenerator

    monkeypatch.setattr(AgentGenerator, "generate_all", broken_generate_all)

    with pytest.raises(RuntimeError, match="Simulated generation failure"):
        manager.generate(req)

    restored = sample_registry.read_text(encoding="utf-8")
    assert restored == original_content


# ---------------------------------------------------------------------------
# Status transition tests
# ---------------------------------------------------------------------------


def test_activate_request() -> None:
    req = _make_request()
    req.status = OnboardingStatus.APPROVAL
    activated = _make_manager().activate(req)
    assert activated.status == OnboardingStatus.ACTIVE


def test_archive_request() -> None:
    req = _make_request()
    req.status = OnboardingStatus.ACTIVE
    archived = _make_manager().archive(req)
    assert archived.status == OnboardingStatus.ARCHIVED


# ---------------------------------------------------------------------------
# OnboardingStatus enum tests
# ---------------------------------------------------------------------------


def test_status_values() -> None:
    assert OnboardingStatus.REQUESTED.value == "requested"
    assert OnboardingStatus.ACTIVE.value == "active"
    assert OnboardingStatus.FAILED.value == "failed"
    assert OnboardingStatus.ARCHIVED.value == "archived"


# ---------------------------------------------------------------------------
# State machine tests (Issue #28)
# ---------------------------------------------------------------------------

from ai_company.hr.onboarding import (  # noqa: E402
    _TRANSITIONS,
    STATE_LABELS,
    _RequestStore,
    can_transition,
    is_terminal,
)


def _make_store() -> _RequestStore:
    """Create a temporary _RequestStore for testing."""
    import tempfile

    return _RequestStore(data_dir=Path(tempfile.mkdtemp()))


def test_all_states_have_labels() -> None:
    for state in OnboardingStatus:
        assert state in STATE_LABELS, f"Missing label for {state}"


def test_all_states_have_transition_entry() -> None:
    for state in OnboardingStatus:
        assert state in _TRANSITIONS, f"Missing transition entry for {state}"


def test_terminal_states_have_no_outgoing() -> None:
    for state in (OnboardingStatus.REJECTED, OnboardingStatus.FAILED, OnboardingStatus.ARCHIVED):
        assert len(_TRANSITIONS[state]) == 0, f"{state} should be terminal"


def test_happy_path_transitions() -> None:
    happy = [
        OnboardingStatus.REQUESTED,
        OnboardingStatus.CONFIG_REVIEW,
        OnboardingStatus.SECURITY_REVIEW,
        OnboardingStatus.GENERATING,
        OnboardingStatus.TESTING,
        OnboardingStatus.APPROVAL,
        OnboardingStatus.ACTIVE,
    ]
    for i in range(len(happy) - 1):
        assert happy[i + 1] in _TRANSITIONS[happy[i]], (
            f"{happy[i].value} → {happy[i + 1].value} should be valid"
        )


def test_rejection_from_each_non_terminal() -> None:
    non_terminal = [
        OnboardingStatus.REQUESTED,
        OnboardingStatus.CONFIG_REVIEW,
        OnboardingStatus.SECURITY_REVIEW,
        OnboardingStatus.GENERATING,
        OnboardingStatus.TESTING,
        OnboardingStatus.APPROVAL,
    ]
    for state in non_terminal:
        assert OnboardingStatus.REJECTED in _TRANSITIONS[state], (
            f"{state.value} should be rejectable"
        )


def test_can_transition_function() -> None:
    assert can_transition(OnboardingStatus.REQUESTED, OnboardingStatus.CONFIG_REVIEW)
    assert not can_transition(OnboardingStatus.REQUESTED, OnboardingStatus.ACTIVE)
    assert not can_transition(OnboardingStatus.ACTIVE, OnboardingStatus.REQUESTED)


def test_is_terminal_function() -> None:
    assert is_terminal(OnboardingStatus.REJECTED)
    assert is_terminal(OnboardingStatus.FAILED)
    assert is_terminal(OnboardingStatus.ARCHIVED)
    assert not is_terminal(OnboardingStatus.ACTIVE)
    assert not is_terminal(OnboardingStatus.REQUESTED)
    assert not is_terminal(OnboardingStatus.APPROVAL)


def test_request_transition_to_valid() -> None:
    req = _make_request()
    req.transition_to(OnboardingStatus.CONFIG_REVIEW)
    assert req.status == OnboardingStatus.CONFIG_REVIEW


def test_request_transition_to_invalid() -> None:
    req = _make_request()
    with pytest.raises(ValueError, match="Invalid transition"):
        req.transition_to(OnboardingStatus.ACTIVE)


def test_request_to_dict_roundtrip() -> None:
    req = _make_request()
    req.status = OnboardingStatus.SECURITY_REVIEW
    d = req.to_dict()
    restored = OnboardingRequest.from_dict(d)
    restored.request_id = req.request_id
    assert restored.status == OnboardingStatus.SECURITY_REVIEW
    assert restored.agent_id == req.agent_id


# ---------------------------------------------------------------------------
# Service lifecycle tests (Issue #28)
# ---------------------------------------------------------------------------


def test_create_request_persists() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(
        agent_id="new_bot",
        name="New Bot",
        role="Bot",
        department="Engineering",
    )
    assert req.status == OnboardingStatus.REQUESTED
    assert req.agent_id == "new_bot"
    loaded = mgr.get_request(req.request_id)
    assert loaded is not None
    assert loaded.agent_id == "new_bot"


def test_advance_happy_path() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    for expected in [
        OnboardingStatus.CONFIG_REVIEW,
        OnboardingStatus.SECURITY_REVIEW,
        OnboardingStatus.GENERATING,
        OnboardingStatus.TESTING,
        OnboardingStatus.APPROVAL,
        OnboardingStatus.ACTIVE,
    ]:
        req = mgr.advance(req)
        assert req.status == expected


def test_advance_from_active_raises() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.ACTIVE
    with pytest.raises(ValueError, match="Cannot advance"):
        mgr.advance(req)


def test_security_review_approve() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.SECURITY_REVIEW
    req = mgr.security_review(req, reviewer="cto", approved=True)
    assert req.status == OnboardingStatus.GENERATING
    assert req.security_reviewer == "cto"


def test_security_review_reject() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.SECURITY_REVIEW
    req = mgr.security_review(req, reviewer="cto", approved=False)
    assert req.status == OnboardingStatus.REJECTED
    assert "rejected" in req.error.lower()


def test_reject_from_midpoint() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.TESTING
    req = mgr.reject(req, reason="Tests failed")
    assert req.status == OnboardingStatus.REJECTED
    assert req.error == "Tests failed"


def test_archive_from_active() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.ACTIVE
    req = mgr.archive(req)
    assert req.status == OnboardingStatus.ARCHIVED
    assert is_terminal(req.status)


def test_record_failure() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    req = mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    req.status = OnboardingStatus.GENERATING
    req = mgr.record_failure(req, "Generator crashed")
    assert req.status == OnboardingStatus.FAILED
    assert req.error == "Generator crashed"


def test_list_requests_filter() -> None:
    mgr = _make_manager()
    mgr._store = _make_store()
    mgr.create_request(agent_id="a1", name="A1", role="R", department="D")
    mgr.create_request(agent_id="a2", name="A2", role="R", department="D")
    all_reqs = mgr.list_requests()
    assert len(all_reqs) == 2
    requested = mgr.list_requests(status=OnboardingStatus.REQUESTED)
    assert len(requested) == 2
    active = mgr.list_requests(status=OnboardingStatus.ACTIVE)
    assert len(active) == 0
