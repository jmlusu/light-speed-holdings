"""LS-MEM SQLite Engine — Core CRUD and Lifecycle.

Implements architecture §1, §2, §3, §6–§10, §12–§16:
- SQLite + FTS5 storage
- CRUD operations with secret scan + classification + gateway + audit
- Lifecycle management (TTL, staleness, supersede, pin, veto)
- Value scoring 0–5 with tier routing (via scoring.py)
- Integrity checks + FTS5 rebuild
- Export/import
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

from .audit import AuditLogger
from .classification import Classification, ClassificationLayer
from .gateway import GatewayConfig, PermissionGateway
from .redaction import SecretScanner
from .scoring import MemoryScorer


@dataclass
class MemoryRecord:
    """A memory record matching LS-MEM-DATA-MODEL.md schema."""

    id: str
    type: str
    title: str
    content: str
    source: str
    project: str
    created_by: str
    created_at: str
    updated_at: str
    classification: str
    confidence: float
    tags: List[str]
    ttl_days: Optional[int]
    stale_at: Optional[str]
    superseded_by: Optional[str]
    pinned: bool
    constitutional_block: bool
    verified_by: Optional[str]
    tier: int
    approved_for_external_use: bool
    external_approval_token: Optional[str]
    status: str
    deleted_at: Optional[str]
    delete_actor: Optional[str]
    fts_rowid: Optional[int] = None
    vector_id: Optional[str] = None
    correlation_id: str = ""


@dataclass
class EngineConfig:
    """Engine configuration from config.yaml."""

    schema_version: int = 1
    storage: Dict[str, Any] = field(
        default_factory=lambda: {
            "workspace_path": ".lightspeed/memory",
            "global_path": "~/.lightspeed/memory",
        }
    )
    fts: Dict[str, Any] = field(
        default_factory=lambda: {
            "tokenizer": "unicode61",
            "remove_diacritics": True,
            "tokenchars": "_",
            "stopwords": [
                "the",
                "a",
                "an",
                "and",
                "or",
                "but",
                "in",
                "on",
                "at",
                "to",
                "for",
                "of",
                "with",
                "by",
            ],
        }
    )
    injection: Dict[str, Any] = field(
        default_factory=lambda: {
            "max_memories": 15,
            "max_tokens": 2000,
            "min_value_score": 2,
            "exclude_superseded": True,
            "exclude_vetoed": True,
        }
    )
    audit: Dict[str, Any] = field(
        default_factory=lambda: {"retention_days_crud": 90, "retention_days_gateway": 365}
    )
    gateway: Dict[str, Any] = field(
        default_factory=lambda: {
            "external_access": {
                "enabled": False,
                "approved_providers": [],
                "approved_domains": [],
                "approved_operations": [],
                "data_classes_allowed": {
                    "public": False,
                    "internal": False,
                    "confidential": False,
                    "restricted": False,
                },
            }
        }
    )
    ollama: Dict[str, Any] = field(
        default_factory=lambda: {
            "endpoint": "http://127.0.0.1:11434",
            "model": "nomic-embed-text",
            "timeout_seconds": 30,
            "enabled": False,
        }
    )
    bridge: Dict[str, Any] = field(
        default_factory=lambda: {"json_store_path": "memory", "dry_run": True}
    )

    def __post_init__(self) -> None:
        # Tolerate explicit None from untyped callers; defaults come from default_factory.
        if self.storage is None:
            self.storage = {
                "workspace_path": ".lightspeed/memory",
                "global_path": "~/.lightspeed/memory",
            }
        if self.fts is None:
            self.fts = {
                "tokenizer": "unicode61",
                "remove_diacritics": True,
                "tokenchars": "_",
                "stopwords": [
                    "the",
                    "a",
                    "an",
                    "and",
                    "or",
                    "but",
                    "in",
                    "on",
                    "at",
                    "to",
                    "for",
                    "of",
                    "with",
                    "by",
                ],
            }
        if self.injection is None:
            self.injection = {
                "max_memories": 15,
                "max_tokens": 2000,
                "min_value_score": 2,
                "exclude_superseded": True,
                "exclude_vetoed": True,
            }
        if self.audit is None:
            self.audit = {"retention_days_crud": 90, "retention_days_gateway": 365}
        if self.gateway is None:
            self.gateway = {
                "external_access": {
                    "enabled": False,
                    "approved_providers": [],
                    "approved_domains": [],
                    "approved_operations": [],
                    "data_classes_allowed": {
                        "public": False,
                        "internal": False,
                        "confidential": False,
                        "restricted": False,
                    },
                }
            }
        if self.ollama is None:
            self.ollama = {
                "endpoint": "http://127.0.0.1:11434",
                "model": "nomic-embed-text",
                "timeout_seconds": 30,
                "enabled": False,
            }
        if self.bridge is None:
            self.bridge = {"json_store_path": "memory", "dry_run": True}


class LSMEMEngine:
    """
    LS-MEM SQLite Engine.

    Implements the core memory engine per architecture §1:
    - SQLite + FTS5 storage
    - CRUD operations with security pipeline
    - Lifecycle management (TTL, staleness, supersede, pin, veto)
    - Value scoring 0–5 with tier routing (via MemoryScorer)
    - Integrity checks + FTS5 rebuild
    """

    VALID_TYPES = frozenset(
        [
            "observation",
            "decision",
            "architecture",
            "requirement",
            "preference",
            "task",
            "milestone",
            "bug",
            "solution",
            "lesson",
            "entity",
            "document",
            "session",
        ]
    )

    VALID_CLASSIFICATIONS = frozenset(["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"])
    VALID_STATUSES = frozenset(["ACTIVE", "SUPERSEDED", "ARCHIVED", "EXPIRED", "PURGED"])

    def __init__(
        self,
        db_path: Path,
        config: Optional[EngineConfig] = None,
        scanner: Optional[SecretScanner] = None,
        classifier: Optional[ClassificationLayer] = None,
        gateway: Optional[PermissionGateway] = None,
        auditor: Optional[AuditLogger] = None,
        scorer: Optional[MemoryScorer] = None,
    ):
        """
        Initialize the engine.

        Args:
            db_path: Path to SQLite database
            config: EngineConfig from config.yaml
            scanner: SecretScanner for pre-persist secret detection
            classifier: ClassificationLayer for auto-classification
            gateway: PermissionGateway for external access control
            auditor: AuditLogger for tamper-evident audit trail
            scorer: MemoryScorer for value scoring 0-5
        """
        self.db_path = Path(db_path)
        self.config = config or EngineConfig()
        self.scanner = scanner
        self.classifier = classifier or ClassificationLayer()
        self.gateway = gateway or PermissionGateway(GatewayConfig.from_dict(self.config.gateway))
        self.auditor = auditor
        self.scorer = scorer or MemoryScorer()
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize database schema and verify integrity."""
        if self._initialized:
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.row_factory = sqlite3.Row

        # Verify integrity
        integrity = self._conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"Database integrity check failed: {integrity}")

        self._create_schema()

        # Initialize auditor if not provided
        if self.auditor is None:
            audit_db = self.db_path.parent / "audit" / "audit.db"
            self.auditor = AuditLogger(
                audit_db,
                retention_days_crud=self.config.audit.get("retention_days_crud", 90),
                retention_days_gateway=self.config.audit.get("retention_days_gateway", 365),
            )
        self.auditor.initialize()

        # Initialize gateway with config
        self.gateway = PermissionGateway(GatewayConfig.from_dict(self.config.gateway))

        self._initialized = True

    def _create_schema(self) -> None:
        """Create tables and indexes."""
        assert self._conn is not None

        self._conn.executescript("""
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
            CREATE INDEX IF NOT EXISTS idx_mem_superseded ON memories(superseded_by);
            CREATE INDEX IF NOT EXISTS idx_mem_tier ON memories(tier DESC);
            CREATE INDEX IF NOT EXISTS idx_mem_value_score ON memories(confidence DESC);

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                title, content,
                content='memories',
                content_rowid='rowid',
                tokenize='unicode61 remove_diacritics 1'
            );

            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content);
                INSERT INTO memories_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
            END;
        """)
        self._conn.commit()

    # ===== SECURITY PIPELINE =====

    def _run_security_pipeline(
        self,
        content: str,
        classification: str,
        source: str,
    ) -> tuple[str, str, bool]:
        """
        Run the pre-persist security pipeline (architecture §6–§8).

        Returns: (final_content, final_classification, blocked)
        """
        final_content = content
        final_classification = classification
        blocked = False

        # 1. Secret scan + redaction (architecture §8)
        if self.scanner:
            scan_result = self.scanner.scan(content)
            final_content = scan_result.redacted
            if scan_result.classification_upgrade == "RESTRICTED":
                final_classification = "RESTRICTED"
                blocked = True  # Restricted content requires special handling

        # 2. Auto-classification (architecture §7)
        auto_class = self.classifier.classify(
            final_content, Classification.from_string(final_classification)
        )
        if auto_class.level() > Classification.from_string(final_classification).level():
            final_classification = auto_class.value

        # 3. Constitutional veto (ADR-019)
        if self._check_constitutional_veto(final_content):
            raise ValueError("Content blocked by constitutional veto (ADR-019)")

        return final_content, final_classification, blocked

    def _check_constitutional_veto(self, content: str) -> bool:
        """Check ADR-019 constitutional veto patterns."""
        veto_patterns = [
            "constitutional veto",
            "constitutional block",
            "do not capture",
            "prohibited content",
        ]
        content_lower = content.lower()
        return any(p in content_lower for p in veto_patterns)

    def _compute_value_score(
        self, content: str, classification: str, confidence: float, source: str
    ) -> int:
        """Compute value score 0–5 using MemoryScorer."""
        breakdown = self.scorer.score(
            content=content,
            confidence=confidence,
            classification=classification,
            source=source,
        )
        return breakdown.total

    def _score_to_tier(self, score: int) -> int:
        """Map score 0–5 to tier."""
        if score <= 1:
            return 0  # Discarded
        elif score == 2:
            return 1
        elif score <= 4:
            return 2
        else:
            return 3

    def _compute_stale_at(self, created_at: str, ttl_days: Optional[int]) -> Optional[str]:
        """Compute staleness timestamp (180 days default per ADR-019)."""
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            stale = created.replace(day=created.day + 180)
            return stale.isoformat()
        except (ValueError, AttributeError):
            return None

    def _insert_record(self, record: MemoryRecord) -> None:
        """Insert record into database."""
        assert self._conn is not None

        tags_json = json.dumps(record.tags)

        self._conn.execute(
            """
            INSERT INTO memories (
                id, type, title, content, source, project, created_by,
                created_at, updated_at, classification, confidence, tags,
                ttl_days, stale_at, superseded_by, pinned,
                constitutional_block, verified_by, tier,
                approved_for_external_use, external_approval_token,
                status, deleted_at, delete_actor, fts_rowid, vector_id, correlation_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                record.id,
                record.type,
                record.title,
                record.content,
                record.source,
                record.project,
                record.created_by,
                record.created_at,
                record.updated_at,
                record.classification,
                record.confidence,
                tags_json,
                record.ttl_days,
                record.stale_at,
                record.superseded_by,
                int(record.pinned),
                int(record.constitutional_block),
                record.verified_by,
                record.tier,
                int(record.approved_for_external_use),
                record.external_approval_token,
                record.status,
                record.deleted_at,
                record.delete_actor,
                record.fts_rowid,
                record.vector_id,
                record.correlation_id,
            ),
        )

        self._conn.commit()

    def _audit(
        self,
        event_type: str,
        actor: str,
        correlation_id: str,
        details: Dict[str, Any],
        payload: Optional[Any] = None,
    ) -> None:
        """Log audit event."""
        if self.auditor:
            self.auditor.log(event_type, actor, correlation_id, details, payload)

    # ===== CRUD OPERATIONS =====

    def remember(
        self,
        content: str,
        type: str,
        title: str,
        project: str,
        created_by: str,
        source: str = "agent",
        classification: str = "INTERNAL",
        confidence: float = 0.5,
        tags: Optional[List[str]] = None,
        ttl_days: Optional[int] = None,
        correlation_id: Optional[str] = None,
    ) -> MemoryRecord:
        """
        Store a new memory (architecture §1, §12).

        Runs secret scan + classification + constitutional veto + value scoring.
        """
        if not self._initialized:
            self.initialize()

        if type not in self.VALID_TYPES:
            raise ValueError(f"Invalid type: {type}. Must be one of {sorted(self.VALID_TYPES)}")

        if classification not in self.VALID_CLASSIFICATIONS:
            raise ValueError(f"Invalid classification: {classification}")

        # Security pipeline
        final_content, final_classification, _ = self._run_security_pipeline(
            content, classification, source
        )

        # Value scoring
        value_score = self._compute_value_score(
            final_content, final_classification, confidence, source
        )
        if value_score <= 1:
            raise ValueError(
                f"Value score {value_score} too low (0–1 discarded per architecture §1)"
            )

        tier = self._score_to_tier(value_score)

        record_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        corr_id = correlation_id or str(uuid.uuid4())

        # Default TTL per type
        if ttl_days is None:
            ttl_days = self._get_default_ttl(type)

        record = MemoryRecord(
            id=record_id,
            type=type,
            title=title[:500],
            content=final_content,
            source=source,
            project=project,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            classification=final_classification,
            confidence=confidence,
            tags=tags or [],
            ttl_days=ttl_days,
            stale_at=self._compute_stale_at(now, ttl_days),
            superseded_by=None,
            pinned=False,
            constitutional_block=False,
            verified_by=None,
            tier=tier,
            approved_for_external_use=False,
            external_approval_token=None,
            status="ACTIVE",
            deleted_at=None,
            delete_actor=None,
            correlation_id=corr_id,
        )

        self._insert_record(record)

        # Audit
        self._audit(
            "memory_create",
            created_by,
            corr_id,
            {
                "memory_id": record_id,
                "type": type,
                "title": title,
                "classification": final_classification,
                "tier": tier,
                "project": project,
            },
            payload={"content_preview": final_content[:200]},
        )

        return record

    def get(self, record_id: str) -> Optional[MemoryRecord]:
        """Get a memory by ID."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        row = self._conn.execute("SELECT * FROM memories WHERE id = ?", (record_id,)).fetchone()
        if row:
            return self._row_to_record(row)
        return None

    def update(
        self,
        record_id: str,
        actor: str,
        content: Optional[str] = None,
        title: Optional[str] = None,
        classification: Optional[str] = None,
        tags: Optional[List[str]] = None,
        confidence: Optional[float] = None,
    ) -> Optional[MemoryRecord]:
        """Update a memory record."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        # Get existing record
        existing = self.get(record_id)
        if not existing:
            return None

        # Check if superseded
        if existing.status == "SUPERSEDED":
            raise ValueError("Cannot update superseded memory; create new version instead")

        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        # Prepare updates
        updates: Dict[str, Any] = {"updated_at": now, "correlation_id": corr_id}
        if content is not None:
            final_content, final_classification, _ = self._run_security_pipeline(
                content, existing.classification, existing.source
            )
            updates["content"] = final_content
            updates["classification"] = final_classification
        if title is not None:
            updates["title"] = title[:500]
        if classification is not None:
            if classification not in self.VALID_CLASSIFICATIONS:
                raise ValueError(f"Invalid classification: {classification}")
            updates["classification"] = classification
        if tags is not None:
            updates["tags"] = json.dumps(tags)
        if confidence is not None:
            updates["confidence"] = confidence

        # Build dynamic update query
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [record_id]

        self._conn.execute(f"UPDATE memories SET {set_clause} WHERE id = ?", values)
        self._conn.commit()

        # Audit
        self._audit(
            "memory_update",
            actor,
            corr_id,
            {
                "memory_id": record_id,
                "updated_fields": list(updates.keys()),
            },
        )

        return self.get(record_id)

    def supersede(self, record_id: str, actor: str, new_record_id: str) -> bool:
        """Mark a memory as superseded by a newer version (ADR-019 newest-wins)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'SUPERSEDED', superseded_by = ?, updated_at = ?, correlation_id = ?
            WHERE id = ? AND status = 'ACTIVE'
        """,
            (new_record_id, now, corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_update",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "superseded",
                    "superseded_by": new_record_id,
                },
            )
            return True
        return False

    def pin(self, record_id: str, actor: str, pinned: bool = True) -> bool:
        """Pin/unpin a memory (curator pin — exempt from age pruning)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET pinned = ?, updated_at = ?, correlation_id = ?
            WHERE id = ?
        """,
            (int(pinned), now, corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_update",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "pin" if pinned else "unpin",
                    "pinned": pinned,
                },
            )
            return True
        return False

    def verify(self, record_id: str, actor: str, verified: bool = True) -> bool:
        """Mark memory as human-verified (Tier 3 promotion)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        verified_by = f"{actor}@{now}" if verified else None
        tier = 3 if verified else 1

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET verified_by = ?, tier = ?, updated_at = ?, correlation_id = ?
            WHERE id = ?
        """,
            (verified_by, tier, now, corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_update",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "verify" if verified else "unverify",
                    "verified_by": verified_by,
                    "tier": tier,
                },
            )
            return True
        return False

    # ===== SEARCH =====

    def search(
        self,
        query: str,
        project: Optional[str] = None,
        type_filter: Optional[str] = None,
        classification_filter: Optional[str] = None,
        limit: int = 15,
        min_tier: int = 1,
    ) -> List[MemoryRecord]:
        """
        Search memories via FTS5 (architecture §3).

        Returns up to `limit` results ranked by bm25 + value score + recency.
        """
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        # Build query
        conditions = [
            "m.status = 'ACTIVE'",
            "m.constitutional_block = 0",
            f"m.tier >= {min_tier}",
            "m.classification != 'RESTRICTED'",
        ]
        params: List[Any] = []

        if project:
            conditions.append("m.project = ?")
            params.append(project)
        if type_filter:
            conditions.append("m.type = ?")
            params.append(type_filter)
        if classification_filter:
            conditions.append("m.classification != ?")
            params.append("RESTRICTED")  # Explicit filter also excludes RESTRICTED

        where_clause = " AND ".join(conditions)

        if query.strip() in ("", "*"):
            # Match-all: FTS5 MATCH rejects '*' as a parse error, so the
            # session injector's project-wide sweep bypasses the FTS index.
            sql = f"""
                SELECT m.*, 0.0 as rank
                FROM memories m
                WHERE {where_clause}
                ORDER BY rank + (m.tier * 10) + (julianday('now') - julianday(m.updated_at)) * -0.1
                LIMIT ?
            """
            params = params + [limit]
        else:
            # FTS5 search with bm25 ranking
            sql = f"""
                SELECT m.*, bm25(memories_fts) as rank
                FROM memories_fts
                JOIN memories m ON m.rowid = memories_fts.rowid
                WHERE memories_fts MATCH ? AND {where_clause}
                ORDER BY rank + (m.tier * 10) + (julianday('now') - julianday(m.updated_at)) * -0.1
                LIMIT ?
            """
            params = [query] + params + [limit]

        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_record(row) for row in rows]

    def search_by_correlation(self, correlation_id: str) -> List[MemoryRecord]:
        """Get all memories sharing a correlation ID."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT * FROM memories WHERE correlation_id = ? ORDER BY created_at", (correlation_id,)
        ).fetchall()
        return [self._row_to_record(row) for row in rows]

    # ===== DELETION (architecture §14) =====

    def forget(self, record_id: str, actor: str) -> bool:
        """Soft-delete a memory (architecture §14)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'ARCHIVED', deleted_at = ?, delete_actor = ?, correlation_id = ?
            WHERE id = ? AND status = 'ACTIVE'
        """,
            (now, actor, corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_delete",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "forget",
                },
            )
            return True
        return False

    def purge(self, record_id: str, actor: str, confirm: bool = False) -> bool:
        """Hard-delete a memory (architecture §14). Requires explicit confirmation."""
        if not confirm:
            raise ValueError("Purge requires explicit confirmation (--confirm-purge)")

        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'PURGED', deleted_at = ?, delete_actor = ?, correlation_id = ?
            WHERE id = ?
        """,
            (now, actor, corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_delete",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "purge",
                },
            )
            return True
        return False

    def restore(self, record_id: str, actor: str) -> bool:
        """Restore a soft-deleted (forgotten) memory within retention window."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        corr_id = str(uuid.uuid4())

        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'ACTIVE', deleted_at = NULL, delete_actor = NULL, correlation_id = ?
            WHERE id = ? AND status = 'ARCHIVED'
        """,
            (corr_id, record_id),
        )

        self._conn.commit()

        if cursor.rowcount > 0:
            self._audit(
                "memory_update",
                actor,
                corr_id,
                {
                    "memory_id": record_id,
                    "action": "restore",
                },
            )
            return True
        return False

    # ===== LIFECYCLE MAINTENANCE =====

    def apply_lifecycle(self) -> Dict[str, int]:
        """
        Apply lifecycle rules (architecture §1, ADR-019):
        - Mark stale memories as ARCHIVED
        - Mark expired memories as EXPIRED
        - Respect pinned entries

        Returns counts of affected records.
        """
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        now = datetime.now(timezone.utc).isoformat()
        corr_id = str(uuid.uuid4())

        counts = {"stale_archived": 0, "expired": 0}

        # Mark stale (180 days, not pinned)
        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'ARCHIVED', updated_at = ?, correlation_id = ?
            WHERE status = 'ACTIVE'
            AND stale_at IS NOT NULL
            AND stale_at < ?
            AND pinned = 0
        """,
            (now, corr_id, now),
        )
        counts["stale_archived"] = cursor.rowcount

        # Mark expired (TTL elapsed, not pinned)
        cursor = self._conn.execute(
            """
            UPDATE memories
            SET status = 'EXPIRED', updated_at = ?, correlation_id = ?
            WHERE status = 'ACTIVE'
            AND ttl_days IS NOT NULL
            AND date(created_at, '+' || ttl_days || ' days') < date('now')
            AND pinned = 0
        """,
            (now, corr_id),
        )
        counts["expired"] = cursor.rowcount

        self._conn.commit()

        if counts["stale_archived"] > 0 or counts["expired"] > 0:
            self._audit(
                "memory_update",
                "system",
                corr_id,
                {
                    "action": "lifecycle",
                    **counts,
                },
            )

        return counts

    # ===== FTS5 MAINTENANCE =====

    def rebuild_fts(self) -> int:
        """Rebuild FTS5 index (architecture §16, threat T27)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        self._conn.execute("DELETE FROM memories_fts")
        self._conn.execute("""
            INSERT INTO memories_fts(rowid, title, content)
            SELECT rowid, title, content FROM memories WHERE status = 'ACTIVE'
        """)
        self._conn.commit()

        count = self._conn.execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]
        return int(count)

    def integrity_check(self) -> bool:
        """Run SQLite integrity check (architecture §2, threat T27)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None
        result = self._conn.execute("PRAGMA integrity_check").fetchone()[0]
        return bool(result == "ok")

    # ===== EXPORT / IMPORT =====

    def export(
        self,
        project: Optional[str] = None,
        include_restricted: bool = False,
        actor: str = "system",
    ) -> List[MemoryRecord]:
        """Export memories (architecture §15)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        conditions = ["status = 'ACTIVE'"]
        params = []

        if project:
            conditions.append("project = ?")
            params.append(project)
        if not include_restricted:
            conditions.append("classification != 'RESTRICTED'")

        where = " AND ".join(conditions)
        sql = f"SELECT * FROM memories WHERE {where} ORDER BY created_at"

        rows = self._conn.execute(sql, params).fetchall()
        records = [self._row_to_record(row) for row in rows]

        # Re-run secret scanner on export (architecture §15, threat T26)
        if self.scanner:
            for record in records:
                scan_result = self.scanner.scan(record.content)
                record.content = scan_result.redacted
                if scan_result.classification_upgrade == "RESTRICTED":
                    record.classification = "RESTRICTED"

        # Audit
        corr_id = str(uuid.uuid4())
        self._audit(
            "export",
            actor,
            corr_id,
            {
                "scope": {"project": project, "include_restricted": include_restricted},
                "record_count": len(records),
            },
            payload={"records": [r.id for r in records]},
        )

        return records

    def status(self) -> Dict[str, Any]:
        """Get engine status (architecture §12 memory-status tool)."""
        if not self._initialized:
            self.initialize()

        assert self._conn is not None

        stats = {}
        stats["total"] = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        stats["active"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE status = 'ACTIVE'"
        ).fetchone()[0]
        stats["archived"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE status = 'ARCHIVED'"
        ).fetchone()[0]
        stats["superseded"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE status = 'SUPERSEDED'"
        ).fetchone()[0]
        stats["expired"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE status = 'EXPIRED'"
        ).fetchone()[0]
        stats["purged"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE status = 'PURGED'"
        ).fetchone()[0]
        stats["pinned"] = self._conn.execute(
            "SELECT COUNT(*) FROM memories WHERE pinned = 1"
        ).fetchone()[0]

        # By type
        type_rows = self._conn.execute(
            "SELECT type, COUNT(*) FROM memories WHERE status = 'ACTIVE' GROUP BY type"
        ).fetchall()
        stats["by_type"] = {row[0]: row[1] for row in type_rows}

        # By classification
        class_rows = self._conn.execute(
            "SELECT classification, COUNT(*) FROM memories WHERE status = 'ACTIVE' GROUP BY classification"
        ).fetchall()
        stats["by_classification"] = {row[0]: row[1] for row in class_rows}

        # By tier
        tier_rows = self._conn.execute(
            "SELECT tier, COUNT(*) FROM memories WHERE status = 'ACTIVE' GROUP BY tier"
        ).fetchall()
        stats["by_tier"] = {str(row[0]): row[1] for row in tier_rows}

        # FTS stats
        stats["fts_count"] = self._conn.execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]

        # DB size
        stats["db_size_bytes"] = self.db_path.stat().st_size if self.db_path.exists() else 0

        # Integrity
        stats["integrity_ok"] = self.integrity_check()

        return stats

    # ===== INTERNAL HELPERS =====

    def _get_default_ttl(self, type: str) -> int:
        """Get default TTL per type (from LS-MEM-DATA-MODEL.md §3)."""
        ttl_map = {
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
        return ttl_map.get(type, 365)

    def _row_to_record(self, row: sqlite3.Row) -> MemoryRecord:
        """Convert sqlite3.Row to MemoryRecord."""
        return MemoryRecord(
            id=row["id"],
            type=row["type"],
            title=row["title"],
            content=row["content"],
            source=row["source"],
            project=row["project"],
            created_by=row["created_by"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            classification=row["classification"],
            confidence=row["confidence"],
            tags=json.loads(row["tags"]),
            ttl_days=row["ttl_days"],
            stale_at=row["stale_at"],
            superseded_by=row["superseded_by"],
            pinned=bool(row["pinned"]),
            constitutional_block=bool(row["constitutional_block"]),
            verified_by=row["verified_by"],
            tier=row["tier"],
            approved_for_external_use=bool(row["approved_for_external_use"]),
            external_approval_token=row["external_approval_token"],
            status=row["status"],
            deleted_at=row["deleted_at"],
            delete_actor=row["delete_actor"],
            correlation_id=row["correlation_id"],
        )

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
            self._initialized = False

    def __enter__(self) -> "LSMEMEngine":
        self.initialize()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
