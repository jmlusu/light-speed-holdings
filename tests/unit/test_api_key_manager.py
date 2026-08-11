"""Tests for the API key rotation manager (security/keys.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.security.keys import APIKeyManager, ProviderKeyState

_MASTER_SECRET = "test-master-secret-for-api-key-manager"


@pytest.fixture(autouse=True)
def _master_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_API_KEY_MASTER", _MASTER_SECRET)


@pytest.fixture()
def manager(tmp_path: Path) -> APIKeyManager:
    return APIKeyManager(key_dir=tmp_path / "security")


class TestSetAndGet:
    def test_set_key_then_get_returns_key(self, manager: APIKeyManager) -> None:
        key_id = manager.set_key("openai", "sk-test-123")
        assert manager.get_key("openai") == "sk-test-123"
        assert key_id == manager.get_status("openai")["current_key_id"]

    def test_get_key_fail_closed_without_key(self, manager: APIKeyManager) -> None:
        assert manager.get_key("anthropic") is None

    def test_set_key_for_unknown_provider_creates_state(self, manager: APIKeyManager) -> None:
        manager.set_key("anthropic", "sk-ant-test")
        assert "anthropic" in manager.list_providers()


class TestRotation:
    def test_rotate_moves_current_to_previous(self, manager: APIKeyManager) -> None:
        manager.set_key("openai", "sk-old-key")
        manager.rotate_key("openai", "sk-new-key")

        assert manager.get_key("openai") == "sk-new-key"
        # Previous key available during overlap period.
        assert manager.get_previous_key("openai") == "sk-old-key"

    def test_rotate_without_existing_key_fails(self, manager: APIKeyManager) -> None:
        assert manager.rotate_key("openai", "sk-new-key") is None

    def test_previous_key_not_available_after_overlap(self, tmp_path: Path) -> None:
        manager = APIKeyManager(key_dir=tmp_path / "security")
        manager.set_key("openai", "sk-old-key")
        manager.rotate_key("openai", "sk-new-key")
        # Force overlap window to already be closed.
        state = manager._providers["openai"]
        state.last_rotation -= state.overlap_period + 1
        assert manager.get_previous_key("openai") is None

    def test_key_rotation_due_when_no_state(self, manager: APIKeyManager) -> None:
        assert manager.is_rotation_due("openai") is True

    def test_key_rotation_not_due_immediately(self, manager: APIKeyManager) -> None:
        manager.set_key("openai", "sk-test-123")
        assert manager.is_rotation_due("openai") is False


class TestPersistenceAndSecurity:
    def test_state_persists_across_reload(self, tmp_path: Path) -> None:
        key_dir = tmp_path / "security"
        m1 = APIKeyManager(key_dir=key_dir)
        m1.set_key("openai", "sk-persist-me")

        m2 = APIKeyManager(key_dir=key_dir)
        assert m2.get_key("openai") == "sk-persist-me"

    def test_keys_encrypted_at_rest(self, tmp_path: Path) -> None:
        key_dir = tmp_path / "security"
        manager = APIKeyManager(key_dir=key_dir)
        manager.set_key("openai", "sk-super-secret-value")

        raw = (key_dir / "llm_api_keys.json").read_text(encoding="utf-8")
        assert "sk-super-secret-value" not in raw
        data = json.loads(raw)
        assert data["openai"]["current_key_encrypted"] != "sk-super-secret-value"

    def test_get_status_shape(self, manager: APIKeyManager) -> None:
        manager.set_key("openai", "sk-test-123")
        status = manager.get_status("openai")
        assert status is not None
        assert status["provider"] == "openai"
        assert set(status) == {
            "provider",
            "current_key_id",
            "previous_key_id",
            "last_rotation",
            "rotation_due",
            "in_overlap",
            "rotation_interval",
            "overlap_period",
        }

    def test_status_none_for_unknown_provider(self, manager: APIKeyManager) -> None:
        assert manager.get_status("unknown-provider") is None


class TestProviderKeyState:
    def test_is_in_overlap_false_without_previous(self) -> None:
        state = ProviderKeyState(provider="openai", current_key="k")
        assert state.is_in_overlap() is False

    def test_is_in_overlap_true_after_rotation(self) -> None:
        import time

        state = ProviderKeyState(
            provider="openai",
            current_key="new",
            previous_key="old",
            last_rotation=time.time(),
        )
        assert state.is_in_overlap() is True
