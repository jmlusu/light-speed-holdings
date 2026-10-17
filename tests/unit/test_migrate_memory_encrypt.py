"""Unit tests for migrate_memory_encrypt module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.data.database import Database
from ai_company.security.encryption_key_manager import EncryptionKeyManager
from ai_company.security.memory_encryption import decrypt, is_encrypted
from ai_company.security.migrate_memory_encrypt import (
    encrypt_legacy_entries,
    migrate_file_based_entries,
)


@pytest.fixture(autouse=True)
def _set_master_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", "test-master-secret-migrate")


@pytest.fixture()
def key_manager(tmp_path: Path) -> EncryptionKeyManager:
    return EncryptionKeyManager(key_dir=tmp_path / "keys")


@pytest.fixture()
def db(tmp_path: Path) -> Database:
    db_file = tmp_path / "test_migration.db"
    database = Database(str(db_file))
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS memory_entries (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            content_search TEXT,
            agent_id TEXT,
            tags TEXT,
            created_at TEXT
        )
        """
    )
    database.commit()
    return database


class TestMigrateDatabaseEntries:
    def test_encrypt_legacy_entries_migrates_plaintext(
        self, db: Database, key_manager: EncryptionKeyManager
    ) -> None:
        db.execute(
            "INSERT INTO memory_entries (id, content, content_search) VALUES (?, ?, ?)",
            ("entry-1", "Plaintext note 1", "Plaintext note 1"),
        )
        db.execute(
            "INSERT INTO memory_entries (id, content, content_search) VALUES (?, ?, ?)",
            ("entry-2", "Plaintext note 2", "Plaintext note 2"),
        )
        db.commit()

        count = encrypt_legacy_entries(database=db, key_manager=key_manager)
        assert count == 2

        rows = db.fetchall("SELECT id, content FROM memory_entries")
        for row in rows:
            assert is_encrypted(row["content"])
            assert decrypt(row["content"], key_manager) in ("Plaintext note 1", "Plaintext note 2")

        # Second run should be idempotent and encrypt 0 entries
        second_count = encrypt_legacy_entries(database=db, key_manager=key_manager)
        assert second_count == 0

    def test_encrypt_legacy_entries_empty_database(
        self, db: Database, key_manager: EncryptionKeyManager
    ) -> None:
        count = encrypt_legacy_entries(database=db, key_manager=key_manager)
        assert count == 0


class TestMigrateFileBasedEntries:
    def test_migrate_file_based_entries_success(
        self, tmp_path: Path, key_manager: EncryptionKeyManager
    ) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir(parents=True)

        file1 = memory_dir / "agent1.json"
        data1 = [
            {"id": "m1", "content": "secret entry one"},
            {"id": "m2", "content": ""},
        ]
        file1.write_text(json.dumps(data1), encoding="utf-8")

        # Key file that should be skipped
        key_file = memory_dir / "memory_keys.json"
        key_file.write_text("{}", encoding="utf-8")

        # Invalid json file that should be skipped safely
        corrupt_file = memory_dir / "corrupted.json"
        corrupt_file.write_text("{invalid json", encoding="utf-8")

        # Non-list json file
        dict_file = memory_dir / "dict.json"
        dict_file.write_text(json.dumps({"key": "val"}), encoding="utf-8")

        count = migrate_file_based_entries(base_dir=str(memory_dir), key_manager=key_manager)
        assert count == 1

        updated_data = json.loads(file1.read_text(encoding="utf-8"))
        assert is_encrypted(updated_data[0]["content"])
        assert decrypt(updated_data[0]["content"], key_manager) == "secret entry one"
        assert updated_data[1]["content"] == ""

        # Second run should be idempotent
        second_count = migrate_file_based_entries(base_dir=str(memory_dir), key_manager=key_manager)
        assert second_count == 0

    def test_migrate_nonexistent_directory(
        self, tmp_path: Path, key_manager: EncryptionKeyManager
    ) -> None:
        non_existent = tmp_path / "does_not_exist"
        count = migrate_file_based_entries(base_dir=str(non_existent), key_manager=key_manager)
        assert count == 0
