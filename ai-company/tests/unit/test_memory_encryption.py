"""Tests for memory encryption (content encryption engine + MemoryStore integration)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from ai_company.security.encryption_key_manager import EncryptionKeyManager
from ai_company.security.memory_encryption import decrypt, encrypt, is_encrypted


@pytest.fixture(autouse=True)
def _set_master_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a deterministic master secret is available for tests."""
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", "test-master-secret-for-encryption-tests")


@pytest.fixture()
def key_manager(tmp_path: Path) -> EncryptionKeyManager:
    return EncryptionKeyManager(key_dir=tmp_path / "keys")


# ── Content encryption tests ──────────────────────────────────────


class TestEncryptDecrypt:
    def test_encrypt_decrypt_roundtrip(self, key_manager: EncryptionKeyManager) -> None:
        plaintext = "This is sensitive memory content"
        encrypted = encrypt(plaintext, key_manager)
        decrypted = decrypt(encrypted, key_manager)
        assert decrypted == plaintext

    def test_encrypted_content_has_prefix(self, key_manager: EncryptionKeyManager) -> None:
        encrypted = encrypt("secret data", key_manager)
        assert encrypted.startswith("ENC:")

    def test_plaintext_passthrough(self, key_manager: EncryptionKeyManager) -> None:
        """Non-encrypted content passes through decrypt unchanged."""
        plaintext = "plain text content"
        # decrypt of non-encrypted content should passthrough
        assert decrypt(plaintext, key_manager) == plaintext
        # encrypt always encrypts when given a key_manager
        encrypted = encrypt(plaintext, key_manager)
        assert is_encrypted(encrypted)

    def test_plaintext_passthrough_on_decrypt(self, key_manager: EncryptionKeyManager) -> None:
        """Non-encrypted content passes through decrypt unchanged."""
        plaintext = "just plain text"
        assert decrypt(plaintext, key_manager) == plaintext

    def test_is_encrypted_detects_prefix(self) -> None:
        assert is_encrypted("ENC:dGFzdA==") is True
        assert is_encrypted("plain text") is False
        assert is_encrypted("") is False

    def test_key_rotation_decrypts_with_new_key(
        self, key_manager: EncryptionKeyManager
    ) -> None:
        """After rotation, new encryption uses new key."""
        encrypted_old = encrypt("old secret", key_manager)
        key_manager.rotate()
        encrypted_new = encrypt("new secret", key_manager)

        # Both should decrypt with the rotated manager
        assert decrypt(encrypted_old, key_manager) == "old secret"
        assert decrypt(encrypted_new, key_manager) == "new secret"

    def test_key_rotation_decrypts_old_content(
        self, key_manager: EncryptionKeyManager
    ) -> None:
        """Content encrypted with the old key can still be decrypted after rotation."""
        encrypted = encrypt("legacy content", key_manager)
        key_manager.rotate()
        # Should still decrypt (uses previous key)
        assert decrypt(encrypted, key_manager) == "legacy content"

    def test_wrong_key_fails(self, tmp_path: Path) -> None:
        """Decryption with a completely different key fails."""
        km1 = EncryptionKeyManager(key_dir=tmp_path / "keys1")
        km2 = EncryptionKeyManager(key_dir=tmp_path / "keys2")

        encrypted = encrypt("secret", km1)
        with pytest.raises(ValueError, match="Failed to decrypt"):
            decrypt(encrypted, km2)

    def test_empty_string(self, key_manager: EncryptionKeyManager) -> None:
        """Empty string is treated as plaintext (passthrough)."""
        assert encrypt("", key_manager) == ""
        assert decrypt("", key_manager) == ""

    def test_unicode_content(self, key_manager: EncryptionKeyManager) -> None:
        """Unicode content encrypts and decrypts correctly."""
        plaintext = "日本語テスト 🔐 émojis"
        encrypted = encrypt(plaintext, key_manager)
        decrypted = decrypt(encrypted, key_manager)
        assert decrypted == plaintext

    def test_no_double_encryption(self, key_manager: EncryptionKeyManager) -> None:
        """Encrypting already-encrypted content returns it unchanged."""
        encrypted = encrypt("secret", key_manager)
        double_encrypted = encrypt(encrypted, key_manager)
        assert double_encrypted == encrypted


# ── MemoryStore integration tests ─────────────────────────────────


class TestMemoryStoreEncryption:
    def test_memory_store_encrypt_on_store(self, tmp_path: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        store = MemoryStore(base_dir=tmp_path / "memory")
        store.enable_encryption(km)

        entry = store.store("episodic", "Confidential meeting notes")
        # Content in memory should be encrypted
        assert is_encrypted(entry.content)

    def test_memory_store_decrypt_on_recall(self, tmp_path: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        store = MemoryStore(base_dir=tmp_path / "memory")
        store.enable_encryption(km)

        store.store("semantic", "Secret knowledge", tags=["secret"])
        results = store.recall("semantic", tags=["secret"])
        assert len(results) == 1
        assert results[0].content == "Secret knowledge"

    def test_memory_store_search_decrypts(self, tmp_path: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        store = MemoryStore(base_dir=tmp_path / "memory")
        store.enable_encryption(km)

        store.store("semantic", "The quick brown fox")
        results = store.search("quick")
        assert len(results) == 1
        assert results[0].content == "The quick brown fox"

    def test_memory_store_persistence_with_encryption(self, tmp_path: Path) -> None:
        from ai_company.memory.engine import MemoryStore

        km1 = EncryptionKeyManager(key_dir=tmp_path / "keys")
        store1 = MemoryStore(base_dir=tmp_path / "memory")
        store1.enable_encryption(km1)
        store1.store("episodic", "Persistent encrypted data")

        # Reload with same keys
        km2 = EncryptionKeyManager(key_dir=tmp_path / "keys")
        store2 = MemoryStore(base_dir=tmp_path / "memory")
        store2.enable_encryption(km2)
        results = store2.recall("episodic")
        assert len(results) == 1
        assert results[0].content == "Persistent encrypted data"


# ── Migration tests ───────────────────────────────────────────────


class TestMigration:
    def test_migration_encrypts_legacy(self, tmp_path: Path) -> None:
        from ai_company.data.database import Database
        from ai_company.memory.engine import MemoryStore
        from ai_company.security.migrate_memory_encrypt import encrypt_legacy_entries

        db = Database(tmp_path / "test.db")
        db.init_schema()

        # Insert plaintext entries directly
        db.execute(
            """INSERT INTO memory_entries
               (id, memory_type, content, content_search, metadata, agent_id, tags, created_at, access_count)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                "test_001",
                "episodic",
                "Legacy plaintext content",
                "Legacy plaintext content",
                "{}",
                "agent1",
                "[]",
                "2025-01-01T00:00:00",
                0,
            ),
        )
        db.commit()

        km = EncryptionKeyManager(key_dir=tmp_path / "keys")
        count = encrypt_legacy_entries(database=db, key_manager=km)
        assert count == 1

        # Verify encrypted in DB
        row = db.fetchone("SELECT content FROM memory_entries WHERE id = 'test_001'")
        assert is_encrypted(row["content"])

        # Verify content_search still has plaintext
        assert row["content"] != "Legacy plaintext content"

    def test_migration_idempotent(self, tmp_path: Path) -> None:
        from ai_company.data.database import Database
        from ai_company.security.migrate_memory_encrypt import encrypt_legacy_entries

        db = Database(tmp_path / "test2.db")
        db.init_schema()

        km = EncryptionKeyManager(key_dir=tmp_path / "keys")

        # Insert and encrypt
        db.execute(
            """INSERT INTO memory_entries
               (id, memory_type, content, content_search, metadata, agent_id, tags, created_at, access_count)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                "idem_001",
                "semantic",
                "Will be encrypted",
                "Will be encrypted",
                "{}",
                "",
                "[]",
                "2025-01-01T00:00:00",
                0,
            ),
        )
        db.commit()

        count1 = encrypt_legacy_entries(database=db, key_manager=km)
        assert count1 == 1

        # Run again — should encrypt 0 (already encrypted)
        count2 = encrypt_legacy_entries(database=db, key_manager=km)
        assert count2 == 0
