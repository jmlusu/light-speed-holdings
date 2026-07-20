"""Tests for the database abstraction layer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.data.database import Database, init_database, get_database


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database for testing."""
    path = tmp_path / "test.db"
    database = Database(path)
    database.init_schema()
    yield database
    database.close()


class TestDatabase:
    """Tests for the Database class."""

    def test_init_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Database initialisation creates parent directories."""
        path = tmp_path / "nested" / "dir" / "test.db"
        db = Database(path)
        db.init_schema()
        assert path.parent.exists()
        db.close()

    def test_init_schema_version(self, db: Database) -> None:
        """Schema version is set after init."""
        version = db.get_schema_version()
        assert version == 1

    def test_init_schema_idempotent(self, db: Database) -> None:
        """Running init_schema twice doesn't error."""
        db.init_schema()
        db.init_schema()
        assert db.get_schema_version() == 1

    def test_execute_and_fetch(self, db: Database) -> None:
        """Basic execute and fetchall work."""
        db.execute(
            "INSERT INTO tasks (id, status) VALUES (?, ?)",
            ("test-1", "pending"),
        )
        db.commit()
        rows = db.fetchall("SELECT * FROM tasks WHERE id = ?", ("test-1",))
        assert len(rows) == 1
        assert rows[0]["id"] == "test-1"

    def test_fetchone_returns_none_for_missing(self, db: Database) -> None:
        """fetchone returns None when no row matches."""
        result = db.fetchone("SELECT * FROM tasks WHERE id = ?", ("nonexistent",))
        assert result is None

    def test_fetchone_returns_dict(self, db: Database) -> None:
        """fetchone returns a dict."""
        db.execute("INSERT INTO tasks (id, status) VALUES (?, ?)", ("t1", "completed"))
        db.commit()
        result = db.fetchone("SELECT * FROM tasks WHERE id = ?", ("t1",))
        assert result is not None
        assert result["id"] == "t1"
        assert result["status"] == "completed"

    def test_table_count(self, db: Database) -> None:
        """table_count returns correct number of rows."""
        assert db.table_count("tasks") == 0
        db.execute("INSERT INTO tasks (id) VALUES (?)", ("a",))
        db.execute("INSERT INTO tasks (id) VALUES (?)", ("b",))
        db.commit()
        assert db.table_count("tasks") == 2

    def test_export_json(self, db: Database) -> None:
        """export_json produces valid JSON."""
        db.execute(
            "INSERT INTO tasks (id, status, tags) VALUES (?,?,?)",
            ("x", "pending", json.dumps(["tag1"])),
        )
        db.commit()
        result = db.export_json("tasks")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["id"] == "x"
        assert data[0]["tags"] == ["tag1"]

    def test_context_manager(self, tmp_path: Path) -> None:
        """Database works as a context manager."""
        path = tmp_path / "ctx.db"
        with Database(path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS test (id TEXT)")
            conn.commit()
        # Verify the file exists
        assert path.exists()

    def test_transaction_rollback(self, db: Database) -> None:
        """Rollback undoes uncommitted changes."""
        db.execute("INSERT INTO tasks (id) VALUES (?)", ("rollback-test",))
        db.rollback()
        assert db.table_count("tasks") == 0

    def test_init_database_singleton(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """init_database creates a singleton."""
        import ai_company.data.database as mod

        monkeypatch.setattr(mod, "_default_db", None)
        db1 = init_database(tmp_path / "singleton.db")
        db2 = init_database(tmp_path / "singleton.db")
        assert db1 is db2
        assert get_database() is db1
        # Cleanup
        db1.close()
        monkeypatch.setattr(mod, "_default_db", None)
