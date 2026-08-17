"""Tests for the unified onboarding service module."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_company.services.onboarding import (
    OnboardingService,
    OnboardingState,
    OnboardingRequest,
    _request_to_registry_entry,
    can_transition,
    is_terminal,
    valid_transitions,
    STATE_LABELS,
    _TRANSITIONS,
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
                    "tools": ["read", "edit", "bash"],
                },
                {
                    "id": "lead_backend",
                    "name": "Lead Backend Engineer",
                    "title": "Lead Backend",
                    "type": "specialist",
                    "department": "Technology",
                    "reports_to": "cto",
                    "responsibilities": ["Build APIs"],
                    "tools": ["read", "edit", "bash", "grep"],
                },
            ],
        }
    }
    registry_path = tmp_path / "company-registry.yaml"
    registry_path.write_text(yaml.dump(data), encoding="utf-8")
    return registry_path


@pytest.fixture()
def service(sample_registry: Path, tmp_path: Path) -> OnboardingService:
    """Create an OnboardingService for testing."""
    # Create hr directory for persistence
    hr_dir = tmp_path / "hr"
    hr_dir.mkdir(exist_ok=True)

    return OnboardingService(
        registry_path=str(sample_registry),
        templates_dir=str(Path(__file__).resolve().parents[2] / "templates"),
        output_dir=str(tmp_path / "agents"),
        data_dir=str(tmp_path),
    )


def _make_request(**overrides: object) -> OnboardingRequest:
    """Create an OnboardingRequest with defaults."""
    defaults = {
        "agent_id": "data_engineer",
        "name": "Data Engineer",
        "role": "Data Engineer",
        "department": "Data",
        "agent_type": "specialist",
        "reports_to": "cto",
        "responsibilities": ["Build pipelines"],
        "tools": ["read", "edit", "bash"],
    }
    defaults.update(overrides)
    return OnboardingRequest(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# State machine tests
# ---------------------------------------------------------------------------


def test_all_states_have_labels() -> None:
    for state in OnboardingState:
        assert state in STATE_LABELS, f"Missing label for {state}"


def test_all_states_have_transition_entry() -> None:
    for state in OnboardingState:
        assert state in _TRANSITIONS, f"Missing transition entry for {state}"


def test_terminal_states_have_no_outgoing() -> None:
    for state in (OnboardingState.REJECTED, OnboardingState.ARCHIVED):
        assert len(_TRANSITIONS[state]) == 0, f"{state} should be terminal"


def test_happy_path_transitions() -> None:
    happy = [
        OnboardingState.REQUESTED,
        OnboardingState.CONFIG_REVIEW,
        OnboardingState.SECURITY_REVIEW,
        OnboardingState.GENERATING,
        OnboardingState.TESTING,
        OnboardingState.APPROVAL,
        OnboardingState.ACTIVE,
    ]
    for i in range(len(happy) - 1):
        assert happy[i + 1] in _TRANSITIONS[happy[i]], (
            f"{happy[i].value} → {happy[i + 1].value} should be valid"
        )


def test_rejection_from_each_non_terminal() -> None:
    non_terminal = [
        OnboardingState.REQUESTED,
        OnboardingState.CONFIG_REVIEW,
        OnboardingState.SECURITY_REVIEW,
        OnboardingState.GENERATING,
        OnboardingState.TESTING,
        OnboardingState.APPROVAL,
    ]
    for state in non_terminal:
        assert OnboardingState.REJECTED in _TRANSITIONS[state], (
            f"{state.value} should be rejectable"
        )


def test_can_transition_function() -> None:
    assert can_transition(OnboardingState.REQUESTED, OnboardingState.CONFIG_REVIEW)
    assert not can_transition(OnboardingState.REQUESTED, OnboardingState.ACTIVE)
    assert not can_transition(OnboardingState.ACTIVE, OnboardingState.REQUESTED)


def test_is_terminal_function() -> None:
    assert is_terminal(OnboardingState.REJECTED)
    assert not is_terminal(OnboardingState.FAILED)
    assert is_terminal(OnboardingState.ARCHIVED)
    assert not is_terminal(OnboardingState.ACTIVE)
    assert not is_terminal(OnboardingState.REQUESTED)
    assert not is_terminal(OnboardingState.APPROVAL)


def test_request_transition_to_valid() -> None:
    req = _make_request()
    req.transition_to(OnboardingState.CONFIG_REVIEW)
    assert req.state == OnboardingState.CONFIG_REVIEW


def test_request_transition_to_invalid() -> None:
    req = _make_request()
    with pytest.raises(ValueError, match="Invalid transition"):
        req.transition_to(OnboardingState.ACTIVE)


# ---------------------------------------------------------------------------
# OnboardingRequest tests
# ---------------------------------------------------------------------------


def test_request_defaults() -> None:
    req = _make_request()
    assert req.state == OnboardingState.REQUESTED
    assert req.created_at is not None
    assert req.updated_at is not None


def test_request_to_registry_entry() -> None:
    req = _make_request()
    entry = _request_to_registry_entry(req)
    assert entry["id"] == "data_engineer"
    assert entry["name"] == "Data Engineer"
    assert entry["type"] == "specialist"
    assert entry["department"] == "Data"
    assert entry["reports_to"] == "cto"
    assert entry["tools"] == ["read", "edit", "bash"]


def test_request_to_dict_roundtrip() -> None:
    req = _make_request()
    req.state = OnboardingState.SECURITY_REVIEW
    d = req.to_dict()
    restored = OnboardingRequest.from_dict(d)
    restored.id = req.id
    assert restored.state == OnboardingState.SECURITY_REVIEW
    assert restored.agent_id == req.agent_id


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------


def test_validate_valid_entry(service: OnboardingService) -> None:
    req = _make_request()
    errors = service.validate_draft(req)
    assert errors == []


def test_validate_duplicate_id(service: OnboardingService) -> None:
    req = _make_request(agent_id="cto")
    errors = service.validate_draft(req)
    assert any("already exists" in e for e in errors)


def test_validate_missing_agent_id(service: OnboardingService) -> None:
    req = _make_request(agent_id="")
    errors = service.validate_draft(req)
    assert any("agent_id" in e for e in errors)


def test_validate_missing_name(service: OnboardingService) -> None:
    req = _make_request(name="")
    errors = service.validate_draft(req)
    assert any("name" in e for e in errors)


def test_validate_missing_department(service: OnboardingService) -> None:
    req = _make_request(department="")
    errors = service.validate_draft(req)
    assert any("department" in e for e in errors)


def test_validate_invalid_reports_to(service: OnboardingService) -> None:
    req = _make_request(reports_to="nonexistent_agent")
    errors = service.validate_draft(req)
    assert any("reports_to" in e for e in errors)


def test_validate_invalid_agent_type(service: OnboardingService) -> None:
    req = _make_request(agent_type="invalid")
    errors = service.validate_draft(req)
    assert any("agent_type" in e for e in errors)


def test_validate_reports_to_by_name(service: OnboardingService) -> None:
    req = _make_request(reports_to="CTO")
    errors = service.validate_draft(req)
    assert errors == []


# ---------------------------------------------------------------------------
# Service API tests
# ---------------------------------------------------------------------------


def test_request_onboarding(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="new_bot",
        role="Bot",
        department="Engineering",
        tools=["read", "edit"],
    )
    assert result.success
    assert result.data is not None
    assert result.data["agent_id"] == "new_bot"
    assert result.data["tier"] == 3  # edit is sensitive


def test_request_onboarding_duplicate(service: OnboardingService) -> None:
    service.request_onboarding(
        agent_id="new_bot",
        role="Bot",
        department="Engineering",
    )
    result = service.request_onboarding(
        agent_id="new_bot",
        role="Bot2",
        department="Engineering",
    )
    assert not result.success
    assert "already has an active onboarding request" in result.errors[0]


def test_list_requests(service: OnboardingService) -> None:
    service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    service.request_onboarding(
        agent_id="bot2",
        role="Bot",
        department="Engineering",
    )
    result = service.list_requests()
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2


def test_list_requests_filter(service: OnboardingService) -> None:
    service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    result = service.list_requests(state="requested")
    assert result.success
    assert result.data is not None
    assert len(result.data) == 1


def test_get_status(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    assert result.success
    request_id = result.data["request_id"]

    status_result = service.get_status(request_id)
    assert status_result.success
    assert status_result.data is not None
    assert status_result.data["agent_id"] == "bot1"


def test_get_status_not_found(service: OnboardingService) -> None:
    result = service.get_status("nonexistent")
    assert not result.success
    assert "not found" in result.errors[0]


# ---------------------------------------------------------------------------
# State transition tests via service methods
# ---------------------------------------------------------------------------


def test_advance_to_next(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to config_review
    result = service.advance_to_next(request_id)
    assert result.success
    assert result.data["state"] == "config_review"

    # Advance to security_review
    result = service.advance_to_next(request_id)
    assert result.success
    assert result.data["state"] == "security_review"


def test_security_review_approve(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to security_review
    service.advance_to_next(request_id)
    service.advance_to_next(request_id)

    # Security review
    result = service.security_review(request_id, reviewer="cto", approved=True)
    assert result.success
    assert result.data["state"] == "generating"


def test_security_review_reject(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to security_review
    service.advance_to_next(request_id)
    service.advance_to_next(request_id)

    # Security review
    result = service.security_review(request_id, reviewer="cto", approved=False, reason="Too risky")
    assert result.success
    assert result.data["state"] == "rejected"


def test_reject_from_requested(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    result = service.reject_onboarding(request_id, rejected_by="ceo", reason="Not needed")
    assert result.success
    assert result.data["state"] == "rejected"


def test_archive(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to active
    for _ in range(5):  # requested -> config_review -> security_review -> generating -> testing -> approval
        service.advance_to_next(request_id)
    service.approve_onboarding(request_id, approved_by="ceo")

    # Archive
    result = service.archive(request_id)
    assert result.success
    assert result.data["state"] == "archived"


def test_retry_from_failure(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to generating
    service.advance_to_next(request_id)
    service.advance_to_next(request_id)
    service.advance_to_next(request_id)

    # Simulate failure
    req = service._get_request(request_id)
    req.error = "Generator crashed"
    req.state = OnboardingState.FAILED
    service._save_request(req)

    # Retry
    result = service.retry_from_failure(request_id)
    assert result.success
    assert result.data["state"] == "generating"


# ---------------------------------------------------------------------------
# Registry integration tests
# ---------------------------------------------------------------------------


def test_add_to_registry(service: OnboardingService, sample_registry: Path) -> None:
    req = _make_request()
    result = service.add_to_registry(req)
    assert result.success

    data = yaml.safe_load(sample_registry.read_text(encoding="utf-8"))
    agents = data["company"]["agents"]
    new_agent = next(a for a in agents if a["id"] == "data_engineer")
    assert new_agent["name"] == "Data Engineer"
    assert new_agent["department"] == "Data"


def test_add_to_registry_validation_failure(service: OnboardingService, sample_registry: Path) -> None:
    req = _make_request(agent_id="cto")
    result = service.add_to_registry(req)
    assert not result.success

    data = yaml.safe_load(sample_registry.read_text(encoding="utf-8"))
    agents = data["company"]["agents"]
    assert sum(1 for a in agents if a["id"] == "cto") == 1


# ---------------------------------------------------------------------------
# Tier calculation tests
# ---------------------------------------------------------------------------


def test_compute_tier_standard(service: OnboardingService) -> None:
    tier = service._compute_tier(["read", "grep", "list"])
    assert tier == 2


def test_compute_tier_sensitive(service: OnboardingService) -> None:
    tier = service._compute_tier(["read", "edit", "bash"])
    assert tier == 3


def test_compute_tier_empty(service: OnboardingService) -> None:
    tier = service._compute_tier([])
    assert tier == 2


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


def test_advance_from_active_fails(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Advance to active
    for _ in range(5):
        service.advance_to_next(request_id)
    service.approve_onboarding(request_id, approved_by="ceo")

    # Try to advance from active
    result = service.advance_to_next(request_id)
    assert not result.success
    assert "Cannot advance" in result.errors[0]


def test_security_review_wrong_state(service: OnboardingService) -> None:
    result = service.request_onboarding(
        agent_id="bot1",
        role="Bot",
        department="Engineering",
    )
    request_id = result.data["request_id"]

    # Try security review when not in security_review state
    result = service.security_review(request_id, reviewer="cto", approved=True)
    assert not result.success
    assert "SECURITY_REVIEW" in result.errors[0]