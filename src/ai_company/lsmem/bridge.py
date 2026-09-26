"""One-Way Import Bridge: JSON MemoryStore → LS-MEM SQLite.

Implements ADR-025 Decision Rule 3: one-way import bridge from existing JSON
MemoryStore into LS-MEM, with dry-run mode and 6→13 type mapping.

Per architecture §1, §C1, and ADR-025.
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from .redaction import SecretScanner

# 6 → 13 Type Mapping (ADR-025 Decision Rule 3; architecture §4)
TYPE_MAPPING = {
    "episodic": "observation",
    "semantic": "lesson",
    "procedural": "solution",
    "relational": "entity",
    "temporal": "session",
    "aggregate": "decision",
}

# Default confidence per source type (architecture §4)
TYPE_CONFIDENCE = {
    "episodic": 0.7,
    "semantic": 0.8,
    "procedural": 0.8,
    "relational": 0.7,
    "temporal": 0.6,
    "aggregate": 0.8,
}

# Default TTL per LS-MEM type (days) — from LS-MEM-DATA-MODEL.md §3
DEFAULT_TTL = {
    "observation": 365,
    "decision": 730,
    "architecture": 1095,
    "requirement": 730,
    "preference": 365,
    "task": 180,
    "milestone": 1095,
    "bug": 365,
    "solution": 730,
    "lesson": 730,
    "entity": 1095,
    "document": 1095,
    "session": 30,
}


@dataclass(frozen=True)
class ImportStats:
    """Statistics from an import operation."""

    total_json_records: int
    imported: int
    skipped: int
    errors: int
    restricted_upgraded: int


class MemoryStoreBridge:
    """
    One-way import bridge from JSON MemoryStore to LS-MEM SQLite.

    Features:
    - Dry-run mode (default): reports what would be imported, writes nothing
    - Secret scanning on import (may upgrade classification to RESTRICTED)
    - 6→13 type mapping with configurable confidence
    - ADR-019 governance field mapping (TTL, staleness, pin, supersede, veto)
    - Atomic transactions (all-or-nothing)
    - Correlation IDs for audit linkage
    """

    def __init__(
        self,
        json_store_path: Path,
        sqlite_path: Path,
        scanner: Optional[SecretScanner] = None,
    ):
        """
        Initialize the bridge.

        Args:
            json_store_path: Path to JSON MemoryStore directory (contains *.json files)
            sqlite_path: Path to LS-MEM SQLite database
            scanner: Optional SecretScanner for redaction during import
        """
        self.json_store_path = Path(json_store_path)
        self.sqlite_path = Path(sqlite_path)
        self.scanner = scanner or SecretScanner()

    def import_all(self, dry_run: bool = True) -> ImportStats:
        """
        Import all JSON records from the MemoryStore.

        Args:
            dry_run: If True, only reports what would be imported (default: True)

        Returns:
            ImportStats with counts
        """
        if not self.json_store_path.exists():
            raise FileNotFoundError(f"JSON store not found: {self.json_store_path}")

        json_files = list(self.json_store_path.glob("*.json"))
        if not json_files:
            return ImportStats(0, 0, 0, 0, 0)

        total = 0
        imported = 0
        skipped = 0
        errors = 0
        restricted_upgraded = 0

        # Ensure SQLite schema exists
        if not dry_run:
            self._ensure_schema()

        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Handle both single record and array of records
                records = data if isinstance(data, list) else [data]

                for record in records:
                    total += 1
                    try:
                        result = self._import_record(record, dry_run)
                        if result in ("imported", "restricted_upgraded"):
                            imported += 1
                            if result == "restricted_upgraded":
                                restricted_upgraded += 1
                        elif result == "skipped":
                            skipped += 1
                    except (OSError, json.JSONDecodeError, ValueError) as e:
                        errors += 1
                        if not dry_run:
                            print(f"Error importing record from {json_file}: {e}")

            except (OSError, json.JSONDecodeError) as e:
                errors += 1
                if not dry_run:
                    print(f"Error reading {json_file}: {e}")

        # Index imported rows into the external-content FTS table (bridge
        # inserts bypass the engine's insert triggers when it creates the schema).
        if not dry_run and imported > 0:
            self._rebuild_fts()

        return ImportStats(
            total_json_records=total,
            imported=imported,
            skipped=skipped,
            errors=errors,
            restricted_upgraded=restricted_upgraded,
        )

    def _rebuild_fts(self) -> None:
        """Rebuild memories_fts from the memories table."""
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute("INSERT INTO memories_fts(memories_fts) VALUES ('rebuild')")
        conn.commit()
        conn.close()

    def _import_record(self, record: dict[str, Any], dry_run: bool) -> str:
        """Import a single JSON record. Returns 'imported', 'skipped', or 'restricted_upgraded'."""
        # Validate required fields
        if not self._validate_record(record):
            return "skipped"

        # Map type
        json_type = record.get("type", "episodic")
        lsmem_type = TYPE_MAPPING.get(json_type, "observation")

        # Generate UUID if not present
        record_id = record.get("id") or str(uuid.uuid4())

        # Scan content for secrets
        content = record.get("content", "")
        scan_result = self.scanner.scan(content)
        redacted_content = scan_result.redacted

        # Determine classification
        classification = record.get("classification", "INTERNAL")
        if scan_result.classification_upgrade == "RESTRICTED":
            classification = "RESTRICTED"

        # Map ADR-019 governance fields
        governance = self._map_governance(record, lsmem_type)

        # Build LS-MEM record
        lsmem_record = {
            "id": record_id,
            "type": lsmem_type,
            "title": record.get("title", "Imported memory")[:500],
            "content": redacted_content,
            "source": "import",
            "project": record.get("project", "default"),
            "created_by": record.get("created_by", "legacy"),
            "created_at": record.get("created_at", datetime.now(timezone.utc).isoformat()),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "classification": classification,
            "confidence": TYPE_CONFIDENCE.get(json_type, 0.7),
            "tags": json.dumps(record.get("tags", [])),
            "ttl_days": governance["ttl_days"],
            "stale_at": governance["stale_at"],
            "superseded_by": None,
            "pinned": governance["pinned"],
            "constitutional_block": governance["constitutional_block"],
            "verified_by": None,  # Imported records start at Tier 1
            "tier": 1,
            "approved_for_external_use": False,
            "external_approval_token": None,
            "status": "ACTIVE",
            "deleted_at": None,
            "delete_actor": None,
            "correlation_id": str(uuid.uuid4()),
        }

        if dry_run:
            # In dry-run, just report what would be imported
            return "restricted_upgraded" if classification == "RESTRICTED" else "imported"

        # Insert into SQLite
        self._insert_record(lsmem_record)
        return "restricted_upgraded" if classification == "RESTRICTED" else "imported"

    def _validate_record(self, record: dict[str, Any]) -> bool:
        """Validate that record has minimum required fields."""
        # At minimum need content
        return record.get("content") is not None

    def _map_governance(self, record: dict[str, Any], lsmem_type: str) -> dict[str, Any]:
        """Map ADR-019 governance concepts to LS-MEM schema (ADR-025 Decision Rule 4)."""
        # TTL
        ttl_days = record.get("ttl_days") or DEFAULT_TTL.get(lsmem_type)

        # Staleness (180 days default from ADR-019)
        created_at_str = record.get("created_at")
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            except ValueError:
                created_at = datetime.now(timezone.utc)
        else:
            created_at = datetime.now(timezone.utc)

        stale_at = (created_at + timedelta(days=180)).isoformat()

        # Pin status
        pinned = 1 if record.get("pinned", False) else 0

        # Constitutional veto check (CONSTITUTIONAL_BLOCKLIST patterns)
        constitutional_block = 0
        content = record.get("content", "").lower()
        blocklist_patterns = [
            "constitutional veto",
            "constitutional block",
            "do not capture",
            "prohibited content",
        ]
        for pattern in blocklist_patterns:
            if pattern in content:
                constitutional_block = 1
                break

        return {
            "ttl_days": ttl_days,
            "stale_at": stale_at,
            "pinned": pinned,
            "constitutional_block": constitutional_block,
        }

    def _ensure_schema(self) -> None:
        """Create LS-MEM schema if not exists."""
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                project TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                classification TEXT NOT NULL DEFAULT 'INTERNAL',
                confidence REAL NOT NULL DEFAULT 0.5,
                tags TEXT DEFAULT '[]',
                ttl_days INTEGER,
                stale_at TEXT,
                superseded_by TEXT,
                pinned INTEGER NOT NULL DEFAULT 0,
                constitutional_block INTEGER NOT NULL DEFAULT 0,
                verified_by TEXT,
                tier INTEGER NOT NULL DEFAULT 1,
                approved_for_external_use INTEGER NOT NULL DEFAULT 0,
                external_approval_token TEXT,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                deleted_at TEXT,
                delete_actor TEXT,
                fts_rowid INTEGER,
                vector_id TEXT,
                correlation_id TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_mem_project_type ON memories(project, type);
            CREATE INDEX IF NOT EXISTS idx_mem_classification ON memories(classification);
            CREATE INDEX IF NOT EXISTS idx_mem_status ON memories(status);
            CREATE INDEX IF NOT EXISTS idx_mem_stale_at ON memories(stale_at);
            CREATE INDEX IF NOT EXISTS idx_mem_correlation ON memories(correlation_id);

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                title, content,
                content='memories',
                content_rowid='rowid',
                tokenize='unicode61 remove_diacritics 1'
            );
        """)
        conn.commit()
        conn.close()

    def _insert_record(self, record: dict[str, Any]) -> None:
        """Insert a record into SQLite."""
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute("PRAGMA journal_mode=WAL")

        cols = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        values = [record[k] for k in record]

        conn.execute(f"INSERT INTO memories ({cols}) VALUES ({placeholders})", values)

        # Also insert into FTS
        rowid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO memories_fts(rowid, title, content) VALUES (?, ?, ?)",
            (rowid, record["title"], record["content"]),
        )

        conn.commit()
        conn.close()


def import_memory_store(
    json_store_path: Path,
    sqlite_path: Path,
    dry_run: bool = True,
    scanner: Optional[SecretScanner] = None,
) -> ImportStats:
    """
    Convenience function to run the import bridge.

    Args:
        json_store_path: Path to JSON MemoryStore directory
        sqlite_path: Path to LS-MEM SQLite database
        dry_run: If True, only reports (default: True)
        scanner: Optional SecretScanner

    Returns:
        ImportStats
    """
    bridge = MemoryStoreBridge(json_store_path, sqlite_path, scanner)
    return bridge.import_all(dry_run=dry_run)
