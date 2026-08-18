"""Legacy File Extractors.

Extractors for reading from legacy JSON/YAML file stores.
Used for backward compatibility and migration.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ai_company.data.etl.base import ExtractionResult, Extractor
from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)


class FileExtractor(Extractor[dict[str, Any]]):
    """Base class for file-based extractors."""

    def __init__(self, source_name: str, file_path: str, project_root: Path | None = None):
        super().__init__(source_name=source_name, database=None)
        self.file_path = file_path
        self.project_root = project_root or get_project_root()
        self.full_path = self.project_root / file_path


class JSONFileExtractor(FileExtractor):
    """Extractor for JSON files (arrays or objects)."""

    def extract(
        self,
        since: str | None = None,
        limit: int | None = None,
        timestamp_field: str = "created_at",
        **kwargs: Any,
    ) -> ExtractionResult[dict[str, Any]]:
        if not self.full_path.exists():
            logger.warning("File not found: %s", self.full_path)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[f"File not found: {self.full_path}"],
            )

        try:
            with open(self.full_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            records: list[dict[str, Any]] = []
            if isinstance(data, list):
                records = [item for item in data if isinstance(item, dict)]
            elif isinstance(data, dict):
                # Try common keys that contain arrays
                for key in ("tasks", "events", "records", "entries", "items"):
                    if key in data and isinstance(data[key], list):
                        records = [item for item in data[key] if isinstance(item, dict)]
                        break
                if not records:
                    records = [data]

            # Filter by timestamp if provided
            if since and timestamp_field:
                filtered: list[dict[str, Any]] = []
                for record in records:
                    ts = record.get(timestamp_field, "")
                    if ts and ts >= since:
                        filtered.append(record)
                records = filtered

            if limit:
                records = records[:limit]

            return ExtractionResult(
                records=records,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        except json.JSONDecodeError as exc:
            logger.error("JSON decode error in %s: %s", self.full_path, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[f"JSON decode error: {exc}"],
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("File extraction failed for %s: %s", self.full_path, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )


class YAMLFileExtractor(FileExtractor):
    """Extractor for YAML files."""

    def extract(
        self,
        since: str | None = None,
        limit: int | None = None,
        list_key: str | None = None,
        **kwargs: Any,
    ) -> ExtractionResult[dict[str, Any]]:
        if not self.full_path.exists():
            logger.warning("File not found: %s", self.full_path)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[f"File not found: {self.full_path}"],
            )

        try:
            with open(self.full_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            records: list[dict[str, Any]] = []
            if list_key and list_key in data and isinstance(data[list_key], list):
                records = [item for item in data[list_key] if isinstance(item, dict)]
            elif isinstance(data, list):
                records = [item for item in data if isinstance(item, dict)]
            elif isinstance(data, dict):
                # Wrap single object
                records = [data]

            if limit:
                records = records[:limit]

            return ExtractionResult(
                records=records,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        except yaml.YAMLError as exc:
            logger.error("YAML parse error in %s: %s", self.full_path, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[f"YAML parse error: {exc}"],
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("File extraction failed for %s: %s", self.full_path, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )


class NDJSONFileExtractor(FileExtractor):
    """Extractor for NDJSON (newline-delimited JSON) files."""

    def extract(
        self,
        since: str | None = None,
        limit: int | None = None,
        timestamp_field: str = "timestamp",
        **kwargs: Any,
    ) -> ExtractionResult[dict[str, Any]]:
        if not self.full_path.exists():
            logger.warning("File not found: %s", self.full_path)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[f"File not found: {self.full_path}"],
            )

        records: list[dict[str, Any]] = []
        try:
            with open(self.full_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        if isinstance(record, dict):
                            records.append(record)
                    except json.JSONDecodeError as exc:
                        logger.warning("Skipping malformed line %d in %s: %s", line_num, self.full_path, exc)

            # Filter by timestamp
            if since and timestamp_field:
                filtered: list[dict[str, Any]] = []
                for record in records:
                    ts = record.get(timestamp_field, "")
                    if ts and ts >= since:
                        filtered.append(record)
                records = filtered

            if limit:
                records = records[:limit]

            return ExtractionResult(
                records=records,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        except Exception as exc:  # noqa: BLE001
            logger.error("NDJSON extraction failed for %s: %s", self.full_path, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )


# Pre-configured extractors for known legacy files
class InboxExtractor(JSONFileExtractor):
    """Extractor for .opencode/inbox.json (legacy task queue)."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:inbox_json", ".opencode/inbox.json", project_root)


class DeadLetterExtractor(JSONFileExtractor):
    """Extractor for .opencode/dead_letter.json (failed tasks)."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:dead_letter_json", ".opencode/dead_letter.json", project_root)

    def extract(self, since: str | None = None, limit: int | None = None, timestamp_field: str = "created_at", **kwargs: Any) -> ExtractionResult[dict[str, Any]]:
        # DLQ entries may not have timestamps, so skip time filtering
        return super().extract(since=None, limit=limit, timestamp_field="", **kwargs)


class CostTrackerExtractor(JSONFileExtractor):
    """Extractor for orchestrator/cost_tracker.json (legacy cost tracking)."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:cost_tracker_json", "orchestrator/cost_tracker.json", project_root)

    def extract(self, since: str | None = None, limit: int | None = None, timestamp_field: str = "created_at", **kwargs: Any) -> ExtractionResult[dict[str, Any]]:
        # cost_tracker.json is a single object, not an array
        result = super().extract(since=None, limit=None, **kwargs)
        if result.records and isinstance(result.records[0], dict):
            # Wrap the single object as a record
            return ExtractionResult(
                records=[result.records[0]],
                source=self.source_name,
                extracted_at=result.extracted_at,
                errors=result.errors,
            )
        return result


class ApprovalsExtractor(YAMLFileExtractor):
    """Extractor for orchestrator/approvals.yaml."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:approvals_yaml", "orchestrator/approvals.yaml", project_root)

    def extract(self, since: str | None = None, limit: int | None = None, list_key: str | None = None, **kwargs: Any) -> ExtractionResult[dict[str, Any]]:
        return super().extract(since=since, limit=limit, list_key="requests", **kwargs)


class SchedulerExtractor(YAMLFileExtractor):
    """Extractor for orchestrator/scheduler.yaml."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:scheduler_yaml", "orchestrator/scheduler.yaml", project_root)

    def extract(self, since: str | None = None, limit: int | None = None, list_key: str | None = None, **kwargs: Any) -> ExtractionResult[dict[str, Any]]:
        return super().extract(since=since, limit=limit, list_key="tasks", **kwargs)


class EscalationYAMLExtractor(YAMLFileExtractor):
    """Extractor for orchestrator/escalation.yaml."""

    def __init__(self, project_root: Path | None = None):
        super().__init__("file:escalation_yaml", "orchestrator/escalation.yaml", project_root)

    def extract(self, since: str | None = None, limit: int | None = None, list_key: str | None = None, **kwargs: Any) -> ExtractionResult[dict[str, Any]]:
        return super().extract(since=since, limit=limit, list_key="events", **kwargs)


__all__ = [
    "FileExtractor",
    "JSONFileExtractor",
    "YAMLFileExtractor",
    "NDJSONFileExtractor",
    "InboxExtractor",
    "DeadLetterExtractor",
    "CostTrackerExtractor",
    "ApprovalsExtractor",
    "SchedulerExtractor",
    "EscalationYAMLExtractor",
]