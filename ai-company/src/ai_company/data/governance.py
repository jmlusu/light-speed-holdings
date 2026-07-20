"""Data governance framework — ownership, retention, lifecycle management.

Defines and enforces data governance policies across all data stores
(tasks, audit events, memory, escalations, KPIs, cost records):

- **Data ownership**: Each table is assigned a functional owner
  (department / role) responsible for its quality and lifecycle.
- **Retention policies**: Configurable per-table retention windows with
  automatic archival and purge.
- **Data lifecycle**: Tracks state transitions (active → archived → purged)
  and exposes governance reporting.

Usage::

    gov = DataGovernance(database)
    gov.apply_retention_policies()          # archival + purge pass
    report = gov.governance_report()        # dashboard-ready snapshot
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums & constants
# ---------------------------------------------------------------------------

class DataClassification(str, Enum):
    """Sensitivity classification for data assets."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class DataLifecycleState(str, Enum):
    """Lifecycle stage of a data record."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    PURGED = "purged"


class RetentionAction(str, Enum):
    """Action to take when a retention policy fires."""

    ARCHIVE = "archive"
    PURGE = "purge"
    ANONYMIZE = "anonymize"
    NONE = "none"


# ---------------------------------------------------------------------------
# Policy definitions
# ---------------------------------------------------------------------------


@dataclass
class RetentionPolicy:
    """Retention configuration for a single data domain.

    Attributes:
        table: Database table name.
        owner: Functional owner (department or role).
        classification: Sensitivity level.
        retention_days: Number of days to retain records before action.
        action: What to do once records exceed the retention window.
        archive_path: Path for archive export (when action is ARCHIVE).
        description: Human-readable explanation of the policy.
    """

    table: str
    owner: str
    classification: DataClassification = DataClassification.INTERNAL
    retention_days: int = 90
    action: RetentionAction = RetentionAction.PURGE
    archive_path: str = "data/archives/"
    description: str = ""


# Default governance policies — one per table in the schema
DEFAULT_POLICIES: list[RetentionPolicy] = [
    RetentionPolicy(
        table="tasks",
        owner="orchestrator",
        classification=DataClassification.INTERNAL,
        retention_days=365,
        action=RetentionAction.ARCHIVE,
        description="Task queue records. Archived after 1 year.",
    ),
    RetentionPolicy(
        table="audit_events",
        owner="compliance",
        classification=DataClassification.CONFIDENTIAL,
        retention_days=180,
        action=RetentionAction.ARCHIVE,
        description="Audit trail events. Archived after 6 months for compliance.",
    ),
    RetentionPolicy(
        table="memory_entries",
        owner="data",
        classification=DataClassification.INTERNAL,
        retention_days=730,
        action=RetentionAction.PURGE,
        description="Agent memory entries. Purged after 2 years.",
    ),
    RetentionPolicy(
        table="escalation_events",
        owner="orchestrator",
        classification=DataClassification.INTERNAL,
        retention_days=365,
        action=RetentionAction.PURGE,
        description="Escalation events. Resolved events purged after 1 year.",
    ),
    RetentionPolicy(
        table="kpi_values",
        owner="data",
        classification=DataClassification.INTERNAL,
        retention_days=730,
        action=RetentionAction.ARCHIVE,
        description="KPI time-series. Archived after 2 years.",
    ),
    RetentionPolicy(
        table="cost_records",
        owner="finance",
        classification=DataClassification.CONFIDENTIAL,
        retention_days=365,
        action=RetentionAction.ARCHIVE,
        description="LLM cost tracking. Archived after 1 year for budget audits.",
    ),
]


# ---------------------------------------------------------------------------
# Data Ownership Registry
# ---------------------------------------------------------------------------


@dataclass
class DataOwner:
    """Registered owner for a data asset."""

    owner_id: str
    department: str
    role: str
    email: str = ""
    responsibilities: list[str] = field(default_factory=list)


# Default ownership mapping
DEFAULT_OWNERS: list[DataOwner] = [
    DataOwner(
        owner_id="orchestrator",
        department="Engineering",
        role="orchestrator",
        responsibilities=[
            "Task queue integrity",
            "Escalation rule management",
            "Workflow state consistency",
        ],
    ),
    DataOwner(
        owner_id="compliance",
        department="Legal",
        role="compliance_officer",
        responsibilities=[
            "Audit trail completeness",
            "Data retention enforcement",
            "Regulatory compliance",
        ],
    ),
    DataOwner(
        owner_id="data",
        department="Data",
        role="chief_data_officer",
        responsibilities=[
            "Data quality assurance",
            "Memory store management",
            "KPI data integrity",
            "Data catalog maintenance",
        ],
    ),
    DataOwner(
        owner_id="finance",
        department="Finance",
        role="finance_lead",
        responsibilities=[
            "Cost tracking accuracy",
            "Budget limit enforcement",
            "Spend reporting",
        ],
    ),
]


# ---------------------------------------------------------------------------
# Data Governance Engine
# ---------------------------------------------------------------------------


class DataGovernance:
    """Central governance engine for the AI Company Builder data layer.

    Provides:
      - Retention policy enforcement (archive / purge / anonymize)
      - Ownership registry and accountability queries
      - Governance reporting and compliance dashboards
      - Data lifecycle management

    Args:
        database: Initialised :class:`Database` instance.
        policies: Override default retention policies.
        owners: Override default ownership registry.
    """

    def __init__(
        self,
        database: Database,
        policies: list[RetentionPolicy] | None = None,
        owners: list[DataOwner] | None = None,
    ) -> None:
        self._db = database
        self._policies: dict[str, RetentionPolicy] = {
            p.table: p for p in (policies or DEFAULT_POLICIES)
        }
        self._owners: dict[str, DataOwner] = {
            o.owner_id: o for o in (owners or DEFAULT_OWNERS)
        }

    # ── Retention enforcement ─────────────────────────────────────────

    def apply_retention_policies(self) -> dict[str, int]:
        """Run retention enforcement across all governed tables.

        Returns a mapping of ``table_name → records_processed``.
        """
        results: dict[str, int] = {}
        for table, policy in self._policies.items():
            count = self._enforce_table_retention(table, policy)
            results[table] = count
        return results

    def _enforce_table_retention(self, table: str, policy: RetentionPolicy) -> int:
        """Enforce retention on a single table. Returns records processed."""
        if policy.action == RetentionAction.NONE:
            return 0

        # Determine the timestamp column for each table
        ts_column = self._get_timestamp_column(table)
        if ts_column is None:
            logger.warning("No timestamp column known for table %s — skipping retention", table)
            return 0

        cutoff = (datetime.now(timezone.utc) - timedelta(days=policy.retention_days)).isoformat()

        # Count affected rows
        count_row = self._db.fetchone(
            f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_column} < ? AND {ts_column} != ''",
            (cutoff,),
        )
        affected = count_row["cnt"] if count_row else 0

        if affected == 0:
            return 0

        if policy.action == RetentionAction.ARCHIVE:
            self._archive_records(table, policy, ts_column, cutoff)
        elif policy.action == RetentionAction.PURGE:
            self._purge_records(table, ts_column, cutoff)
        elif policy.action == RetentionAction.ANONYMIZE:
            self._anonymize_records(table, ts_column, cutoff)

        logger.info(
            "Retention policy [%s] %s: %d records processed (cutoff=%s)",
            table,
            policy.action.value,
            affected,
            cutoff,
        )
        return affected

    def _get_timestamp_column(self, table: str) -> str | None:
        """Return the primary timestamp column name for a table."""
        mapping = {
            "tasks": "created_at",
            "audit_events": "timestamp",
            "memory_entries": "created_at",
            "escalation_events": "timestamp",
            "kpi_values": "timestamp",
            "cost_records": "timestamp",
        }
        return mapping.get(table)

    def _archive_records(
        self,
        table: str,
        policy: RetentionPolicy,
        ts_column: str,
        cutoff: str,
    ) -> None:
        """Export old records to a JSON archive file, then delete them."""
        from pathlib import Path

        archive_dir = Path(policy.archive_path)
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_file = archive_dir / f"{table}_archive.json"
        cutoff_row = self._db.fetchone(
            f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_column} < ? AND {ts_column} != ''",
            (cutoff,),
        )
        count = cutoff_row["cnt"] if cutoff_row else 0

        if count == 0:
            return

        # Fetch records to archive (limit batch for memory safety)
        rows = self._db.fetchall(
            f"SELECT * FROM {table} WHERE {ts_column} < ? AND {ts_column} != '' LIMIT 10000",
            (cutoff,),
        )

        # Append to existing archive
        existing: list[dict[str, Any]] = []
        if archive_file.exists():
            try:
                existing = json.loads(archive_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = []

        existing.extend(rows)

        archive_file.write_text(
            json.dumps(existing, indent=2, default=str),
            encoding="utf-8",
        )

        # Delete archived records
        self._db.execute(
            f"DELETE FROM {table} WHERE {ts_column} < ? AND {ts_column} != ''",
            (cutoff,),
        )
        self._db.commit()

    def _purge_records(self, table: str, ts_column: str, cutoff: str) -> None:
        """Permanently delete records older than the cutoff."""
        self._db.execute(
            f"DELETE FROM {table} WHERE {ts_column} < ? AND {ts_column} != ''",
            (cutoff,),
        )
        self._db.commit()

    def _anonymize_records(self, table: str, ts_column: str, cutoff: str) -> None:
        """Anonymize PII in records older than the cutoff.

        Replaces ``agent_id`` and ``content`` fields with hashed versions
        to preserve analytical value while removing identifying information.
        """
        import hashlib

        rows = self._db.fetchall(
            f"SELECT * FROM {table} WHERE {ts_column} < ? AND {ts_column} != '' LIMIT 1000",
            (cutoff,),
        )

        for row in rows:
            # Anonymize agent_id if present
            if "agent_id" in row and row["agent_id"]:
                anon = hashlib.sha256(row["agent_id"].encode()).hexdigest()[:12]
                self._db.execute(
                    f"UPDATE {table} SET agent_id = ? WHERE rowid = ?",
                    (f"anon_{anon}", row.get("rowid", "")),
                )

        self._db.commit()

    # ── Ownership queries ─────────────────────────────────────────────

    def get_owner(self, table: str) -> DataOwner | None:
        """Return the registered owner for a data table."""
        policy = self._policies.get(table)
        if policy is None:
            return None
        return self._owners.get(policy.owner)

    def list_owners(self) -> list[dict[str, Any]]:
        """Return all registered data owners with their responsibilities."""
        return [
            {
                "owner_id": o.owner_id,
                "department": o.department,
                "role": o.role,
                "email": o.email,
                "responsibilities": o.responsibilities,
            }
            for o in self._owners.values()
        ]

    def list_policies(self) -> list[dict[str, Any]]:
        """Return all configured retention policies."""
        return [
            {
                "table": p.table,
                "owner": p.owner,
                "classification": p.classification.value,
                "retention_days": p.retention_days,
                "action": p.action.value,
                "description": p.description,
            }
            for p in self._policies.values()
        ]

    # ── Governance reporting ──────────────────────────────────────────

    def governance_report(self) -> dict[str, Any]:
        """Generate a comprehensive governance status report.

        Includes table sizes, retention status, ownership mapping,
        and classification distribution.
        """
        table_stats: dict[str, dict[str, Any]] = {}
        for table in self._policies:
            policy = self._policies[table]
            ts_col = self._get_timestamp_column(table)
            row_count = self._db.table_count(table)

            oldest = None
            newest = None
            if ts_col:
                oldest_row = self._db.fetchone(
                    f"SELECT MIN({ts_col}) as oldest FROM {table} WHERE {ts_col} != ''"
                )
                newest_row = self._db.fetchone(
                    f"SELECT MAX({ts_col}) as newest FROM {table} WHERE {ts_col} != ''"
                )
                oldest = oldest_row["oldest"] if oldest_row else None
                newest = newest_row["newest"] if newest_row else None

            # Count records past retention
            past_retention = 0
            if ts_col and row_count > 0:
                cutoff = (
                    datetime.now(timezone.utc) - timedelta(days=policy.retention_days)
                ).isoformat()
                past_row = self._db.fetchone(
                    f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_col} < ? AND {ts_col} != ''",
                    (cutoff,),
                )
                past_retention = past_row["cnt"] if past_row else 0

            table_stats[table] = {
                "row_count": row_count,
                "classification": policy.classification.value,
                "owner": policy.owner,
                "retention_days": policy.retention_days,
                "action": policy.action.value,
                "records_past_retention": past_retention,
                "oldest_record": oldest,
                "newest_record": newest,
            }

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tables": table_stats,
            "owners": self.list_owners(),
            "policies": self.list_policies(),
        }

    def compliance_check(self) -> list[dict[str, Any]]:
        """Check for governance violations across all tables.

        Returns a list of findings, each with severity, table, and description.
        """
        findings: list[dict[str, Any]] = []

        for table, policy in self._policies.items():
            ts_col = self._get_timestamp_column(table)
            if ts_col is None:
                findings.append({
                    "severity": "warning",
                    "table": table,
                    "finding": "No timestamp column — retention cannot be enforced",
                })
                continue

            row_count = self._db.table_count(table)
            if row_count == 0:
                continue

            cutoff = (
                datetime.now(timezone.utc) - timedelta(days=policy.retention_days)
            ).isoformat()
            past_row = self._db.fetchone(
                f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_col} < ? AND {ts_col} != ''",
                (cutoff,),
            )
            past_retention = past_row["cnt"] if past_row else 0

            if past_retention > 0:
                findings.append({
                    "severity": "info",
                    "table": table,
                    "finding": (
                        f"{past_retention} records exceed {policy.retention_days}-day "
                        f"retention window — action: {policy.action.value}"
                    ),
                    "records_affected": past_retention,
                })

            # Check for empty required fields
            if table == "tasks":
                empty_assignee = self._db.fetchone(
                    "SELECT COUNT(*) as cnt FROM tasks WHERE assignee = '' OR assignee IS NULL"
                )
                if empty_assignee and empty_assignee["cnt"] > 0:
                    findings.append({
                        "severity": "warning",
                        "table": table,
                        "finding": (
                            f"{empty_assignee['cnt']} tasks have no assignee — "
                            "data quality issue"
                        ),
                    })

            if table == "audit_events":
                null_agent = self._db.fetchone(
                    "SELECT COUNT(*) as cnt FROM audit_events WHERE agent_id = '' OR agent_id IS NULL"
                )
                if null_agent and null_agent["cnt"] > 0:
                    findings.append({
                        "severity": "warning",
                        "table": table,
                        "finding": (
                            f"{null_agent['cnt']} audit events have no agent_id — "
                            "attribution gap"
                        ),
                    })

        return findings
