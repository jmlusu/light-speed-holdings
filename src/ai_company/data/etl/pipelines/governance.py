"""Governance Pipeline.

Pipeline for data retention, archival, and compliance enforcement.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from ai_company.data.database import Database
from ai_company.data.etl.base import LoadResult, Pipeline, PipelineResult
from ai_company.data.governance import DataGovernance

logger = logging.getLogger(__name__)


class GovernancePipeline(Pipeline):
    """Pipeline for data governance: retention enforcement, archival, compliance checks."""

    def __init__(self, database: Database):
        self.governance = DataGovernance(database)

        super().__init__(
            name="governance",
            database=database,
            extractor=None,
            transformer=None,
            loader=None,
        )

    def run(
        self,
        since: str | None = None,
        batch_size: int = 10000,
        quality_check: bool = True,
        dry_run: bool = False,
        **kwargs: Any,
    ) -> PipelineResult:
        """Run governance enforcement: retention policies, compliance checks.

        Args:
            since: Not used (governance runs on full tables)
            batch_size: Not used
            quality_check: Run compliance checks after enforcement
            dry_run: If True, only report what would be done
            **kwargs: Additional options

        Returns:
            PipelineResult with governance actions taken
        """
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            # Run retention enforcement
            logger.info("Running retention policy enforcement (dry_run=%s)...", dry_run)
            if not dry_run:
                retention_results = self.governance.apply_retention_policies()
            else:
                # Dry run: just check what would be affected
                retention_results = {}
                for table, policy in self.governance._policies.items():
                    ts_col = self.governance._get_timestamp_column(table)
                    if ts_col:
                        cutoff = self.governance._retention_cutoff(table, policy.retention_days)
                        count_row = self.governance._db.fetchone(
                            f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_col} < ? AND {ts_col} != ''",
                            (cutoff,),
                        )
                        retention_results[table] = count_row["cnt"] if count_row else 0

            # Run compliance checks
            logger.info("Running compliance checks...")
            compliance_findings = self.governance.compliance_check()

            # Generate governance report
            report = self.governance.governance_report()

            from ai_company.data.etl.base import ExtractionResult

            result.extraction = ExtractionResult(
                records=[
                    {
                        "retention": retention_results,
                        "compliance": compliance_findings,
                        "report": report,
                    }
                ],
                source="governance",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

            # Quality check: compliance findings as violations
            if quality_check:
                critical_findings = [
                    f for f in compliance_findings if f.get("severity") == "critical"
                ]
                high_findings = [f for f in compliance_findings if f.get("severity") == "high"]
                if critical_findings:
                    result.quality_check_passed = False
                    result.errors.append(
                        f"Governance: {len(critical_findings)} critical compliance findings"
                    )
                if high_findings:
                    result.warnings = [
                        f"Governance: {len(high_findings)} high-severity compliance findings"
                    ]

        except Exception as exc:  # noqa: BLE001
            logger.exception("Governance pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.load = LoadResult(
            loaded_count=len(retention_results) + len(compliance_findings),
            target="governance_actions",
        )

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result


class DeadLetterProcessingPipeline(Pipeline):
    """Pipeline for processing dead letter queue entries."""

    def __init__(self, database: Database):
        super().__init__(
            name="dead_letter_processing",
            database=database,
            extractor=None,
            transformer=None,
            loader=None,
        )

    def run(
        self,
        since: str | None = None,
        batch_size: int = 100,
        quality_check: bool = True,
        auto_retry: bool = False,
        max_retries: int = 3,
        **kwargs: Any,
    ) -> PipelineResult:
        """Process dead letter queue entries.

        Args:
            since: Not used
            batch_size: Max DLQ entries to process per run
            quality_check: Validate retried tasks
            auto_retry: Automatically retry eligible entries
            max_retries: Maximum retry attempts before giving up
            **kwargs: Additional options

        Returns:
            PipelineResult with processing results
        """
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            import json

            from ai_company.paths import get_project_root

            dlq_path = get_project_root() / ".opencode" / "dead_letter.json"
            if not dlq_path.exists():
                # No DLQ file - pipeline completes with no entries to process
                # result.load remains None since there's no loader
                result.mark_completed()
                return result

            with open(dlq_path, "r", encoding="utf-8") as f:
                dlq_entries = json.load(f)

            if not isinstance(dlq_entries, list):
                dlq_entries = []

            processed = 0
            retried = 0
            failed = 0

            # Process each entry
            remaining_entries = []
            for entry in dlq_entries:
                retry_count = entry.get("retry_count", 0)
                processed += 1

                if auto_retry and retry_count < max_retries:
                    # Attempt retry via MessageBus
                    try:
                        from ai_company.models.task import Task
                        from ai_company.orchestrator.message_bus import MessageBus

                        task = Task(**entry)
                        task.retry_count = retry_count + 1
                        bus = MessageBus(str(get_project_root() / ".opencode" / "inbox.json"))
                        bus.send_task(task)
                        retried += 1
                        logger.info("Retried DLQ task %s (attempt %d)", task.id, task.retry_count)
                    except Exception as exc:  # noqa: BLE001
                        logger.error("DLQ retry failed for %s: %s", entry.get("id", "?"), exc)
                        entry["retry_count"] = retry_count + 1
                        entry["last_error"] = str(exc)
                        remaining_entries.append(entry)
                        failed += 1
                else:
                    # Keep in DLQ
                    remaining_entries.append(entry)

            # Write back remaining entries
            with open(dlq_path, "w", encoding="utf-8") as f:
                json.dump(remaining_entries, f, indent=2)

            from ai_company.data.etl.base import ExtractionResult

            result.extraction = ExtractionResult(
                records=[
                    {
                        "processed": processed,
                        "retried": retried,
                        "failed": failed,
                        "remaining": len(remaining_entries),
                    }
                ],
                source="dead_letter",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        except Exception as exc:  # noqa: BLE001
            logger.exception("DLQ processing pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.load = LoadResult(
            loaded_count=processed,
            target="dead_letter",
        )

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result


class InboxPurgePipeline(Pipeline):
    """Pipeline for purging stale/completed tasks from inbox."""

    def __init__(self, database: Database):
        super().__init__(
            name="inbox_purge",
            database=database,
            extractor=None,
            transformer=None,
            loader=None,
        )

    def run(
        self,
        since: str | None = None,
        batch_size: int = 1000,
        quality_check: bool = True,
        max_age_days: int = 30,
        statuses_to_purge: list[str] | None = None,
        **kwargs: Any,
    ) -> PipelineResult:
        """Purge old tasks from the inbox/MessageBus.

        Args:
            since: Cutoff timestamp (overrides max_age_days)
            batch_size: Max tasks to purge per run
            quality_check: Verify no active tasks are purged
            max_age_days: Purge tasks older than this (default 30 days)
            statuses_to_purge: Which statuses to purge (default: completed, failed)
            **kwargs: Additional options

        Returns:
            PipelineResult with purge results
        """
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            from ai_company.orchestrator.message_bus import MessageBus
            from ai_company.paths import get_project_root

            if statuses_to_purge is None:
                statuses_to_purge = ["completed", "failed"]

            # Determine cutoff
            if since is None:
                from datetime import timedelta

                since = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).isoformat()

            bus = MessageBus(
                str(get_project_root() / ".opencode" / "inbox.json"), database=self.database
            )
            all_tasks = bus.get_all_tasks()

            purged = 0
            kept = 0
            errors: list[str] = []

            for task in all_tasks:
                if task.status.value in statuses_to_purge:
                    created = task.created_at or ""
                    if created and created < since:
                        # Quality check: ensure not in_progress or pending
                        if quality_check and task.status.value in (
                            "in_progress",
                            "pending",
                            "escalated",
                        ):
                            errors.append(
                                f"Skipping active task {task.id} with status {task.status.value}"
                            )
                            kept += 1
                            continue

                        try:
                            bus.delete_task(task.id)
                            purged += 1
                        except Exception as exc:  # noqa: BLE001
                            errors.append(f"Failed to purge {task.id}: {exc}")
                    else:
                        kept += 1
                else:
                    kept += 1

            from ai_company.data.etl.base import ExtractionResult

            result.extraction = ExtractionResult(
                records=[
                    {
                        "purged": purged,
                        "kept": kept,
                        "cutoff": since,
                        "statuses": statuses_to_purge,
                    }
                ],
                source="inbox",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

            if errors:
                result.errors.extend(errors)

        except Exception as exc:  # noqa: BLE001
            logger.exception("Inbox purge pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.load = LoadResult(
            loaded_count=purged,
            target="inbox_purged",
        )

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result


__all__ = [
    "GovernancePipeline",
    "DeadLetterProcessingPipeline",
    "InboxPurgePipeline",
]
