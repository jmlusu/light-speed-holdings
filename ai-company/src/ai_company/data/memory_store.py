"""SQLite-backed memory store — drop-in replacement for memory.engine.MemoryStore.

Provides the same public interface as the file-based MemoryStore with
added query capabilities and efficient indexing.  Supports the 6 memory
types: episodic, semantic, procedural, relational, temporal, aggregate.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ai_company.data.database import Database

if TYPE_CHECKING:
    from ai_company.security.encryption_key_manager import EncryptionKeyManager

logger = logging.getLogger(__name__)

MEMORY_TYPES = frozenset({
    "episodic",
    "semantic",
    "procedural",
    "relational",
    "temporal",
    "aggregate",
})


class MemoryEntryDB:
    """A single memory record backed by the database."""

    __slots__ = (
        "id", "memory_type", "content", "metadata",
        "agent_id", "tags", "created_at", "access_count",
    )

    def __init__(
        self,
        id: str,
        memory_type: str,
        content: str,
        metadata: dict[str, Any],
        agent_id: str,
        tags: list[str],
        created_at: str,
        access_count: int,
    ) -> None:
        self.id = id
        self.memory_type = memory_type
        self.content = content
        self.metadata = metadata
        self.agent_id = agent_id
        self.tags = tags
        self.created_at = created_at
        self.access_count = access_count

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "memory_type": self.memory_type,
            "content": self.content,
            "metadata": self.metadata,
            "agent_id": self.agent_id,
            "tags": self.tags,
            "created_at": self.created_at,
            "access_count": self.access_count,
        }


class MemoryStoreDB:
    """SQLite-backed memory storage.

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database
        self._key_manager: EncryptionKeyManager | None = None
        self._ensure_content_search_column()

    def _ensure_content_search_column(self) -> None:
        """Add content_search column if it doesn't exist (migration)."""
        try:
            cols = self._db.fetchall("PRAGMA table_info(memory_entries)")
            col_names = {c["name"] for c in cols}
            if "content_search" not in col_names:
                self._db.execute(
                    "ALTER TABLE memory_entries ADD COLUMN content_search TEXT NOT NULL DEFAULT ''"
                )
                self._db.commit()
                logger.info("Added content_search column to memory_entries")
        except Exception:
            pass  # Column already exists or table doesn't exist yet

    def enable_encryption(self, key_manager: EncryptionKeyManager) -> None:
        """Enable at-rest encryption for memory content.

        When enabled, ``store()`` encrypts content before saving and stores
        a plaintext copy in ``content_search`` for substring queries.
        ``recall()`` decrypts content after loading.
        """
        self._key_manager = key_manager
        logger.info("MemoryStoreDB encryption enabled with key %s", key_manager.current_key_id)

    # ── Core API (compatible with MemoryStore) ────────────────────────

    def store(
        self,
        memory_type: str,
        content: str,
        **kwargs: Any,
    ) -> MemoryEntryDB:
        """Store a new memory entry.

        If encryption is enabled, content is encrypted before saving and a
        plaintext copy is stored in the ``content_search`` column for
        substring queries.
        """
        if memory_type not in MEMORY_TYPES:
            raise ValueError(f"Unknown memory type: {memory_type}")

        metadata = kwargs.get("metadata", {})
        agent_id = kwargs.get("agent_id", "")
        tags = kwargs.get("tags", []) or []
        now = datetime.now().isoformat()
        entry_id = f"{memory_type}_{uuid.uuid4().hex[:12]}"

        # Encrypt content for storage, keep plaintext for search
        stored_content = content
        content_search = content
        if self._key_manager is not None:
            from ai_company.security.memory_encryption import encrypt
            stored_content = encrypt(content, self._key_manager)

        self._db.execute(
            """INSERT INTO memory_entries
               (id, memory_type, content, content_search, metadata, agent_id, tags, created_at, access_count)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                entry_id,
                memory_type,
                stored_content,
                content_search,
                json.dumps(metadata, default=str),
                agent_id,
                json.dumps(tags),
                now,
                0,
            ),
        )
        self._db.commit()

        return MemoryEntryDB(
            id=entry_id,
            memory_type=memory_type,
            content=content,  # Return plaintext to caller
            metadata=metadata,
            agent_id=agent_id,
            tags=tags,
            created_at=now,
            access_count=0,
        )

    def recall(
        self,
        memory_type: str,
        query: str = "",
        tags: list[str] | None = None,
        agent_id: str = "",
        limit: int = 10,
    ) -> list[MemoryEntryDB]:
        """Recall memories with optional filtering.

        If encryption is enabled, uses the ``content_search`` column for
        substring matching and decrypts content after loading.
        """
        if memory_type not in MEMORY_TYPES:
            return []

        # Build SQL dynamically for optional filters
        conditions = ["memory_type = ?"]
        params: list[Any] = [memory_type]

        # Use content_search column for substring queries (plaintext copy)
        if query:
            conditions.append("content_search LIKE ?")
            params.append(f"%{query}%")

        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)

        where_clause = " AND ".join(conditions)
        rows = self._db.fetchall(
            f"SELECT * FROM memory_entries WHERE {where_clause} ORDER BY created_at DESC",
            tuple(params),
        )

        entries = [self._row_to_entry(r) for r in rows]

        # Post-query filter: tag intersection (not easily done in SQL with JSON)
        if tags:
            tag_set = set(tags)
            entries = [e for e in entries if tag_set.intersection(e.tags)]

        # Apply limit and decrypt
        result = entries[:limit]
        self._decrypt_entries(result)

        # Increment access counts
        if result:
            ids = [e.id for e in result]
            placeholders = ",".join(["?"] * len(ids))
            self._db.execute(
                f"UPDATE memory_entries SET access_count = access_count + 1 WHERE id IN ({placeholders})",
                tuple(ids),
            )
            self._db.commit()

        return result

    def count(self, memory_type: str | None = None) -> int:
        """Count memories, optionally filtered by type."""
        if memory_type:
            row = self._db.fetchone(
                "SELECT COUNT(*) as cnt FROM memory_entries WHERE memory_type = ?",
                (memory_type,),
            )
            return row["cnt"] if row else 0
        return self._db.table_count("memory_entries")

    def stats(self) -> dict[str, int]:
        """Return counts per memory type."""
        rows = self._db.fetchall(
            "SELECT memory_type, COUNT(*) as cnt FROM memory_entries GROUP BY memory_type"
        )
        result = {mt: 0 for mt in MEMORY_TYPES}
        for r in rows:
            result[r["memory_type"]] = r["cnt"]
        return result

    def get_all(self, memory_type: str) -> list[MemoryEntryDB]:
        """Return all entries of a given type (decrypted if encryption enabled)."""
        rows = self._db.fetchall(
            "SELECT * FROM memory_entries WHERE memory_type = ? ORDER BY created_at ASC",
            (memory_type,),
        )
        entries = [self._row_to_entry(r) for r in rows]
        self._decrypt_entries(entries)
        return entries

    # ── Extended queries ──────────────────────────────────────────────

    def search_content(self, query: str, limit: int = 20) -> list[MemoryEntryDB]:
        """Full-text content search across all memory types.

        Uses the ``content_search`` column (plaintext) for substring matching.
        """
        rows = self._db.fetchall(
            """SELECT * FROM memory_entries
               WHERE content_search LIKE ?
               ORDER BY access_count DESC, created_at DESC
               LIMIT ?""",
            (f"%{query}%", limit),
        )
        return [self._row_to_entry(r) for r in rows]

    def recent(self, memory_type: str, limit: int = 10) -> list[MemoryEntryDB]:
        """Return the most recent entries of a type (decrypted)."""
        rows = self._db.fetchall(
            "SELECT * FROM memory_entries WHERE memory_type = ? ORDER BY created_at DESC LIMIT ?",
            (memory_type, limit),
        )
        entries = [self._row_to_entry(r) for r in rows]
        self._decrypt_entries(entries)
        return entries

    def most_accessed(self, memory_type: str, limit: int = 10) -> list[MemoryEntryDB]:
        """Return the most-accessed entries of a type (decrypted)."""
        rows = self._db.fetchall(
            "SELECT * FROM memory_entries WHERE memory_type = ? ORDER BY access_count DESC LIMIT ?",
            (memory_type, limit),
        )
        entries = [self._row_to_entry(r) for r in rows]
        self._decrypt_entries(entries)
        return entries

    # ── Migration helpers ─────────────────────────────────────────────

    def import_from_json_dir(self, base_dir: str | Path) -> int:
        """Import memory entries from the legacy ``memory/*.json`` files.

        Returns the number of entries imported.
        """
        base = Path(base_dir)
        if not base.exists():
            logger.warning("Legacy memory directory not found: %s", base)
            return 0

        total = 0
        for mem_type in MEMORY_TYPES:
            path = base / f"{mem_type}.json"
            if not path.exists():
                continue

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                self.store(
                    mem_type,
                    content=item.get("content", ""),
                    metadata=item.get("metadata", {}),
                    agent_id=item.get("agent_id", ""),
                    tags=item.get("tags", []),
                )
                total += 1

            logger.info("Imported %d %s entries from %s", len(data), mem_type, path)

        return total

    def export_to_json_dir(self, base_dir: str | Path) -> int:
        """Export all memory entries to the legacy ``memory/*.json`` format.

        Writes one JSON file per memory type.  Returns the total number
        of entries exported.
        """
        base = Path(base_dir)
        base.mkdir(parents=True, exist_ok=True)

        total = 0
        for mem_type in MEMORY_TYPES:
            entries = self.get_all(mem_type)
            if not entries:
                continue

            data = [e.to_dict() for e in entries]
            path = base / f"{mem_type}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

            total += len(data)
            logger.info("Exported %d %s entries to %s", len(data), mem_type, path)

        return total

    # ── Internal helpers ──────────────────────────────────────────────

    def _decrypt_entries(self, entries: list[MemoryEntryDB]) -> None:
        """Decrypt content in-place for entries returned to callers."""
        if self._key_manager is None:
            return
        from ai_company.security.memory_encryption import decrypt
        for entry in entries:
            entry.content = decrypt(entry.content, self._key_manager)

    @staticmethod
    def _row_to_entry(row: dict[str, Any]) -> MemoryEntryDB:
        """Convert a database row to a MemoryEntryDB.

        Note: Content is NOT decrypted here — callers that need plaintext
        should decrypt explicitly. This keeps the static method simple and
        avoids coupling it to the key manager.
        """
        return MemoryEntryDB(
            id=row["id"],
            memory_type=row["memory_type"],
            content=row["content"],
            metadata=json.loads(row.get("metadata", "{}")),
            agent_id=row.get("agent_id", ""),
            tags=json.loads(row.get("tags", "[]")),
            created_at=row["created_at"],
            access_count=row.get("access_count", 0),
        )
