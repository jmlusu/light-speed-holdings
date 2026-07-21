"""Tests for the encryption key lifecycle manager."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ai_company.security.encryption_key_manager import EncryptionKeyManager


@pytest.fixture(autouse=True)
def _set_master_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a deterministic master secret is available for tests."""
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", "test-master-secret-for-key-manager-tests")


class TestKeyManager:
    def test_key_derivation(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        key = km.get_current_key()
        assert len(key) == 32  # AES-256 = 32 bytes
        assert km.current_key_id != ""

    def test_key_rotation(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        old_id = km.current_key_id
        old_key = km.get_current_key()

        new_id = km.rotate()
        assert new_id != old_id
        assert km.current_key_id == new_id
        # New key should be different
        assert km.get_current_key() != old_key

    def test_previous_key_available_after_rotation(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        first_key = km.get_current_key()
        km.rotate()

        previous = km.get_previous_key()
        assert previous is not None
        assert previous == first_key

    def test_persistence_across_instances(self, tmp_path: Path) -> None:
        key_dir = tmp_path / "keys"
        km1 = EncryptionKeyManager(key_dir=key_dir)
        key_id_1 = km1.current_key_id
        key_1 = km1.get_current_key()

        # Create new instance from same directory
        km2 = EncryptionKeyManager(key_dir=key_dir)
        assert km2.current_key_id == key_id_1
        assert km2.get_current_key() == key_1

    def test_persistence_after_rotation(self, tmp_path: Path) -> None:
        key_dir = tmp_path / "keys"
        km1 = EncryptionKeyManager(key_dir=key_dir)
        km1.rotate()
        new_id = km1.current_key_id
        old_id = km1.previous_key_id

        km2 = EncryptionKeyManager(key_dir=key_dir)
        assert km2.current_key_id == new_id
        assert km2.previous_key_id == old_id
        assert km2.get_previous_key() is not None

    def test_genesis_key_created_on_first_use(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "new_keys")
        assert km.current_key_id != ""
        assert km.previous_key_id == ""
        assert km.get_previous_key() is None
        # Key file should exist
        assert (tmp_path / "new_keys" / "memory_keys.json").exists()

    def test_key_metadata_file_structure(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        meta_path = tmp_path / "keys" / "memory_keys.json"
        meta = json.loads(meta_path.read_text())

        assert "current_key_id" in meta
        assert "current_key_encrypted" in meta
        assert "created_at" in meta
        # Raw key should NOT be in the file
        assert "current_key_raw" not in meta

    def test_missing_master_secret_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("MEMORY_ENCRYPTION_KEY", raising=False)
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        with pytest.raises(RuntimeError, match="No master secret"):
            EncryptionKeyManager(key_dir=tmp_path / "keys")

    def test_fallback_to_jwt_secret_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("MEMORY_ENCRYPTION_KEY", raising=False)
        monkeypatch.setenv("JWT_SECRET_KEY", "jwt-fallback-secret")
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        assert len(km.get_current_key()) == 32

    def test_multiple_rotations_keep_only_previous(self, tmp_path: Path) -> None:
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        key_a = km.get_current_key()
        km.rotate()
        key_b = km.get_current_key()
        km.rotate()
        key_c = km.get_current_key()

        # Current should be key_c, previous should be key_b (not key_a)
        assert km.get_current_key() == key_c
        assert km.get_previous_key() == key_b

    def test_deterministic_key_id(self, tmp_path: Path) -> None:
        """Same key produces same key_id."""
        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        key_id = km.current_key_id
        # Reconstruct and verify same id
        km2 = EncryptionKeyManager(key_dir=tmp_path / "keys")
        assert km2.current_key_id == key_id
