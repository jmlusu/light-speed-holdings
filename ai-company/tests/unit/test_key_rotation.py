"""Tests for API key rotation (PRE-14)."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ai_company.security.key_rotation import (
    APIKey,
    KeyRotationManager,
    KeyRotationPolicy,
    _KEY_PREFIX,
)


@pytest.fixture()
def manager(tmp_path: Path) -> KeyRotationManager:
    return KeyRotationManager(keys_dir=tmp_path / "keys")


@pytest.fixture()
def manager_with_policy(tmp_path: Path) -> KeyRotationManager:
    mgr = KeyRotationManager(keys_dir=tmp_path / "keys")
    mgr.policy = KeyRotationPolicy(max_key_age_days=30, warning_days=7, max_active_keys=3)
    return mgr


# ── APIKey dataclass tests ───────────────────────────────────────────


class TestAPIKey:
    def test_key_is_valid_when_active(self) -> None:
        key = APIKey(
            key_id="k1",
            key_hash="abc",
            name="test",
            prefix="lsh_abc123",
            status="active",
            expires_at=time.time() + 86400,
        )
        assert key.is_valid() is True

    def test_key_is_invalid_when_revoked(self) -> None:
        key = APIKey(
            key_id="k1",
            key_hash="abc",
            name="test",
            prefix="lsh_abc123",
            status="revoked",
            expires_at=time.time() + 86400,
        )
        assert key.is_valid() is False

    def test_key_is_invalid_when_expired(self) -> None:
        key = APIKey(
            key_id="k1",
            key_hash="abc",
            name="test",
            prefix="lsh_abc123",
            status="active",
            expires_at=time.time() - 1,  # expired 1 second ago
        )
        assert key.is_valid() is False

    def test_key_is_valid_when_no_expiration(self) -> None:
        key = APIKey(
            key_id="k1",
            key_hash="abc",
            name="test",
            prefix="lsh_abc123",
            status="active",
            expires_at=0,  # no expiration
        )
        assert key.is_valid() is True

    def test_key_serialization_roundtrip(self) -> None:
        key = APIKey(
            key_id="k1",
            key_hash="abc123",
            name="openai",
            prefix="lsh_abc",
            scopes=["read", "write"],
            status="active",
        )
        data = key.to_dict()
        restored = APIKey.from_dict(data)
        assert restored.key_id == key.key_id
        assert restored.name == key.name
        assert restored.scopes == key.scopes
        assert restored.status == key.status


# ── Key creation tests ───────────────────────────────────────────────


class TestKeyCreation:
    def test_create_key_returns_raw_key(self, manager: KeyRotationManager) -> None:
        api_key, raw_key = manager.create_key(name="test-key")
        assert api_key.name == "test-key"
        assert raw_key.startswith(_KEY_PREFIX)
        assert api_key.status == "active"

    def test_create_key_has_unique_id(self, manager: KeyRotationManager) -> None:
        k1, _ = manager.create_key(name="key1")
        k2, _ = manager.create_key(name="key2")
        assert k1.key_id != k2.key_id

    def test_create_key_with_scopes(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="scoped", scopes=["read", "admin"])
        assert api_key.scopes == ["read", "admin"]

    def test_create_key_default_scopes_wildcard(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="default")
        assert api_key.scopes == ["*"]

    def test_create_key_has_expiration(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="expiring", expires_days=30)
        assert api_key.expires_at > time.time()
        assert api_key.expires_at <= time.time() + (30 * 86400) + 1

    def test_create_key_no_expiration(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="forever", expires_days=0)
        assert api_key.expires_at == 0

    def test_create_key_stores_hash(self, manager: KeyRotationManager) -> None:
        api_key, raw_key = manager.create_key(name="hashed")
        # Reconstruct the hash and verify it matches
        expected_hash = manager._hash_key(raw_key)
        assert api_key.key_hash == expected_hash

    def test_create_key_persists(self, tmp_path: Path) -> None:
        m1 = KeyRotationManager(keys_dir=tmp_path / "keys")
        api_key, _ = m1.create_key(name="persistent")

        m2 = KeyRotationManager(keys_dir=tmp_path / "keys")
        loaded = m2.get_key(api_key.key_id)
        assert loaded is not None
        assert loaded.name == "persistent"

    def test_create_key_exceeds_max_active_raises(
        self, manager_with_policy: KeyRotationManager
    ) -> None:
        # Create 3 keys (the max)
        for i in range(3):
            manager_with_policy.create_key(name="limited")

        with pytest.raises(ValueError, match="Maximum active keys"):
            manager_with_policy.create_key(name="limited")

    def test_create_key_different_names_not_limited(
        self, manager_with_policy: KeyRotationManager
    ) -> None:
        # Different names don't count against each other
        for i in range(5):
            manager_with_policy.create_key(name=f"name-{i}")
        # All 5 should succeed since they have different names
        assert len(manager_with_policy.list_keys()) == 5

    def test_create_key_prefix_is_subset_of_raw(
        self, manager: KeyRotationManager
    ) -> None:
        api_key, raw_key = manager.create_key(name="prefix-check")
        assert raw_key.startswith(api_key.prefix)


# ── Key validation tests ─────────────────────────────────────────────


class TestKeyValidation:
    def test_validate_valid_key(self, manager: KeyRotationManager) -> None:
        _, raw_key = manager.create_key(name="valid")
        result = manager.validate_key(raw_key)
        assert result is not None
        assert result.name == "valid"

    def test_validate_invalid_key(self, manager: KeyRotationManager) -> None:
        result = manager.validate_key("lsh_invalidkey123456")
        assert result is None

    def test_validate_expired_key(self, manager: KeyRotationManager) -> None:
        _, raw_key = manager.create_key(name="expiring", expires_days=0)
        # Force expiration by setting expires_at to the past
        api_key = manager.list_keys(name="expiring")[0]
        api_key.expires_at = time.time() - 1
        manager._save_keys()

        result = manager.validate_key(raw_key)
        assert result is None

    def test_validate_revoked_key(self, manager: KeyRotationManager) -> None:
        api_key, raw_key = manager.create_key(name="revoking")
        manager.revoke_key(api_key.key_id)

        result = manager.validate_key(raw_key)
        assert result is None

    def test_validate_updates_last_used(self, manager: KeyRotationManager) -> None:
        api_key, raw_key = manager.create_key(name="touching")
        assert api_key.last_used_at == 0

        manager.validate_key(raw_key)
        # Reload to check persistence
        reloaded = manager.get_key(api_key.key_id)
        assert reloaded is not None
        assert reloaded.last_used_at > 0


# ── Key rotation tests ───────────────────────────────────────────────


class TestKeyRotation:
    def test_rotate_creates_new_key(self, manager: KeyRotationManager) -> None:
        old_key, _ = manager.create_key(name="rotate-me")
        new_key, raw_key = manager.rotate_key(old_key.key_id)

        assert new_key.key_id != old_key.key_id
        assert new_key.name == old_key.name
        assert new_key.scopes == old_key.scopes
        assert new_key.rotated_from == old_key.key_id
        assert raw_key.startswith(_KEY_PREFIX)

    def test_rotate_revokes_old_key(self, manager: KeyRotationManager) -> None:
        old_key, _ = manager.create_key(name="revoking")
        manager.rotate_key(old_key.key_id)

        reloaded = manager.get_key(old_key.key_id)
        assert reloaded is not None
        assert reloaded.status == "revoked"

    def test_rotate_old_key_fails_validation(self, manager: KeyRotationManager) -> None:
        old_key, old_raw = manager.create_key(name="old-key")
        manager.rotate_key(old_key.key_id)

        result = manager.validate_key(old_raw)
        assert result is None

    def test_rotate_new_key_validates(self, manager: KeyRotationManager) -> None:
        old_key, _ = manager.create_key(name="new-key")
        new_key, new_raw = manager.rotate_key(old_key.key_id)

        result = manager.validate_key(new_raw)
        assert result is not None
        assert result.key_id == new_key.key_id

    def test_rotate_nonexistent_raises(self, manager: KeyRotationManager) -> None:
        with pytest.raises(KeyError, match="Key not found"):
            manager.rotate_key("nonexistent")

    def test_rotate_revoked_key_raises(self, manager: KeyRotationManager) -> None:
        old_key, _ = manager.create_key(name="already-revoked")
        manager.revoke_key(old_key.key_id)

        with pytest.raises(ValueError, match="already revoked"):
            manager.rotate_key(old_key.key_id)

    def test_double_rotation(self, manager: KeyRotationManager) -> None:
        key1, _ = manager.create_key(name="double")
        key2, raw2 = manager.rotate_key(key1.key_id)
        key3, raw3 = manager.rotate_key(key2.key_id)

        # key1 and key2 should be revoked
        assert manager.get_key(key1.key_id).status == "revoked"
        assert manager.get_key(key2.key_id).status == "revoked"
        assert manager.get_key(key3.key_id).status == "active"

        # Only key3 should validate
        assert manager.validate_key(raw2) is None
        assert manager.validate_key(raw3) is not None


# ── Key revocation tests ─────────────────────────────────────────────


class TestKeyRevocation:
    def test_revoke_key(self, manager: KeyRotationManager) -> None:
        api_key, raw_key = manager.create_key(name="revoke-me")
        revoked = manager.revoke_key(api_key.key_id)
        assert revoked.status == "revoked"

        # Should no longer validate
        assert manager.validate_key(raw_key) is None

    def test_revoke_nonexistent_raises(self, manager: KeyRotationManager) -> None:
        with pytest.raises(KeyError, match="Key not found"):
            manager.revoke_key("nonexistent")

    def test_revoke_persists(self, tmp_path: Path) -> None:
        m1 = KeyRotationManager(keys_dir=tmp_path / "keys")
        api_key, raw_key = m1.create_key(name="persistent-revoke")
        m1.revoke_key(api_key.key_id)

        m2 = KeyRotationManager(keys_dir=tmp_path / "keys")
        reloaded = m2.get_key(api_key.key_id)
        assert reloaded.status == "revoked"


# ── Key listing tests ────────────────────────────────────────────────


class TestKeyListing:
    def test_list_all_keys(self, manager: KeyRotationManager) -> None:
        manager.create_key(name="key1")
        manager.create_key(name="key2")
        keys = manager.list_keys()
        assert len(keys) == 2

    def test_list_filter_by_name(self, manager: KeyRotationManager) -> None:
        manager.create_key(name="prod")
        manager.create_key(name="prod")
        manager.create_key(name="staging")
        keys = manager.list_keys(name="prod")
        assert len(keys) == 2

    def test_list_filter_by_status(self, manager: KeyRotationManager) -> None:
        k1, _ = manager.create_key(name="active-key")
        k2, _ = manager.create_key(name="revoked-key")
        manager.revoke_key(k2.key_id)

        active = manager.list_keys(status="active")
        revoked = manager.list_keys(status="revoked")
        assert len(active) == 1
        assert len(revoked) == 1

    def test_list_returns_empty_for_no_match(self, manager: KeyRotationManager) -> None:
        manager.create_key(name="existing")
        keys = manager.list_keys(name="nonexistent")
        assert keys == []


# ── Expiration check tests ───────────────────────────────────────────


class TestExpirationChecks:
    def test_check_expirations_returns_expiring(
        self, manager_with_policy: KeyRotationManager
    ) -> None:
        # Create a key that expires in 5 days (within the 7-day warning window)
        api_key, _ = manager_with_policy.create_key(name="expiring-soon", expires_days=5)
        expiring = manager_with_policy.check_expirations()
        assert len(expiring) == 1
        assert expiring[0].key_id == api_key.key_id

    def test_check_expirations_skips_non_expiring(
        self, manager_with_policy: KeyRotationManager
    ) -> None:
        # Key expires in 25 days (beyond 7-day warning)
        manager_with_policy.create_key(name="not-yet", expires_days=25)
        expiring = manager_with_policy.check_expirations()
        assert len(expiring) == 0

    def test_check_expirations_auto_expires_overdue(
        self, manager_with_policy: KeyRotationManager
    ) -> None:
        api_key, _ = manager_with_policy.create_key(name="overdue", expires_days=0)
        # Force to past
        api_key.expires_at = time.time() - 1
        manager_with_policy._save_keys()

        manager_with_policy.check_expirations()
        reloaded = manager_with_policy.get_key(api_key.key_id)
        assert reloaded.status == "expired"

    def test_cleanup_expired_transitions_keys(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="cleanup-test", expires_days=0)
        api_key.expires_at = time.time() - 1
        manager._save_keys()

        count = manager.cleanup_expired()
        assert count == 1
        reloaded = manager.get_key(api_key.key_id)
        assert reloaded.status == "expired"

    def test_cleanup_expired_returns_zero_when_none(self, manager: KeyRotationManager) -> None:
        manager.create_key(name="fresh", expires_days=90)
        count = manager.cleanup_expired()
        assert count == 0

    def test_check_expirations_skips_revoked(self, manager: KeyRotationManager) -> None:
        api_key, _ = manager.create_key(name="revoked-expired", expires_days=0)
        api_key.expires_at = time.time() - 1
        manager._save_keys()
        manager.revoke_key(api_key.key_id)

        expiring = manager.check_expirations()
        # Revoked keys shouldn't appear (only active keys)
        assert all(k.key_id != api_key.key_id for k in expiring)


# ── Persistence tests ────────────────────────────────────────────────


class TestKeyPersistence:
    def test_full_lifecycle_persists(self, tmp_path: Path) -> None:
        """Create, rotate, revoke — all should survive reload."""
        keys_dir = tmp_path / "keys"

        m1 = KeyRotationManager(keys_dir=keys_dir)
        k1, raw1 = m1.create_key(name="lifecycle")
        k2, raw2 = m1.rotate_key(k1.key_id)
        m1.revoke_key(k2.key_id)

        m2 = KeyRotationManager(keys_dir=keys_dir)
        assert len(m2.list_keys()) == 2
        assert m2.get_key(k1.key_id).status == "revoked"
        assert m2.get_key(k2.key_id).status == "revoked"
        assert m2.validate_key(raw1) is None
        assert m2.validate_key(raw2) is None

    def test_yaml_format_valid(self, tmp_path: Path) -> None:
        """Keys file should be valid YAML."""
        import yaml

        manager = KeyRotationManager(keys_dir=tmp_path / "keys")
        manager.create_key(name="yaml-test")

        raw = (tmp_path / "keys" / "keys.yaml").read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        assert data["version"] == 1
        assert "keys" in data
        assert len(data["keys"]) == 1


# ── Policy tests ─────────────────────────────────────────────────────


class TestKeyRotationPolicy:
    def test_default_policy_values(self) -> None:
        policy = KeyRotationPolicy()
        assert policy.max_key_age_days == 90
        assert policy.warning_days == 14
        assert policy.max_active_keys == 5

    def test_custom_policy(self, manager: KeyRotationManager) -> None:
        manager.policy = KeyRotationPolicy(max_key_age_days=30, max_active_keys=2)
        assert manager.policy.max_key_age_days == 30
        assert manager.policy.max_active_keys == 2


# ── Security audit tests ─────────────────────────────────────────────


class TestSecurityAudit:
    def test_key_hash_is_sha256(self, manager: KeyRotationManager) -> None:
        """Keys are stored as SHA-256 hashes, not plaintext."""
        _, raw_key = manager.create_key(name="hash-audit")
        api_key = manager.list_keys(name="hash-audit")[0]

        # The stored hash should be a 64-char hex string (SHA-256)
        assert len(api_key.key_hash) == 64
        assert all(c in "0123456789abcdef" for c in api_key.key_hash)

    def test_raw_key_not_in_yaml(self, tmp_path: Path) -> None:
        """Raw key strings must never appear in the YAML file."""
        manager = KeyRotationManager(keys_dir=tmp_path / "keys")
        _, raw_key = manager.create_key(name="audit-raw")

        yaml_content = (tmp_path / "keys" / "keys.yaml").read_text(encoding="utf-8")
        assert raw_key not in yaml_content

    def test_revoked_key_cannot_be_used(self, manager: KeyRotationManager) -> None:
        """Once revoked, a key must fail validation."""
        _, raw_key = manager.create_key(name="revoke-test")
        api_key = manager.list_keys(name="revoke-test")[0]
        manager.revoke_key(api_key.key_id)
        assert manager.validate_key(raw_key) is None

    def test_all_keys_unique(self, manager: KeyRotationManager) -> None:
        """All generated keys must be unique."""
        manager.policy = KeyRotationPolicy(max_active_keys=100)
        keys = []
        for i in range(20):
            _, raw = manager.create_key(name=f"unique-{i}")
            keys.append(raw)
        assert len(set(keys)) == 20

    def test_key_prefix_format(self, manager: KeyRotationManager) -> None:
        """Keys should start with the lsh_ prefix."""
        _, raw_key = manager.create_key(name="prefix-test")
        assert raw_key.startswith("lsh_")
