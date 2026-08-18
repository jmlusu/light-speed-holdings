"""KPI Snapshot Pipeline.

Periodic pipeline that collects all department KPIs and stores them in SQLite.
Matches the KPISnapshotScheduler but as a composable ETL pipeline.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.dashboard.kpis import collect_all_kpis
from ai_company.data.database import Database
from ai_company.data.etl.base import ExtractionResult, LoadResult, Pipeline, PipelineResult
from ai_company.data.etl.extractors.sqlite_extractor import (
    AuditEventExtractor,
    CostRecordExtractor,
    TaskExtractor,
)
from ai_company.data.etl.loaders.sqlite_loader import KPIValueLoader
from ai_company.data.etl.transformers.kpi_transformer import KPITimeseriesTransformer
from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)


class KPISnapshotPipeline(Pipeline):
    """Pipeline for periodic KPI snapshot collection and storage.

    This is the ETL equivalent of KPISnapshotScheduler.run_snapshot(),
    but structured as a composable pipeline with quality checks.
    """

    def __init__(
        self,
        database: Database,
        project_root: Path | None = None,
    ):
        self.project_root = project_root or get_project_root()
        self._collector_db = database

        # Components
        extractor = None  # We use collect_all_kpis directly
        transformer = KPITimeseriesTransformer()
        loader = KPIValueLoader(database)

        super().__init__(
            name="kpi_snapshot",
            database=database,
            extractor=extractor,
            transformer=transformer,
            loader=loader,
        )

    def run(
        self,
        since: str | None = None,
        batch_size: int = 1000,
        quality_check: bool = True,
        **kwargs: Any,
    ) -> PipelineResult:
        """Collect all department KPIs and ingest into SQLite.

        Args:
            since: Not used (KPI snapshot is always current state)
            batch_size: Not used (single snapshot)
            quality_check: Validate KPI values before storage
            **kwargs: Additional options

        Returns:
            PipelineResult with execution details
        """
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            # Extract: Collect live KPIs from all department collectors
            logger.info("Collecting KPI snapshot from all departments...")
            snapshot = collect_all_kpis(project_root=self.project_root, database=self._collector_db)
            extraction_records = [snapshot]  # Wrap as single record for transformer
            result.extraction = self._make_extraction_result(extraction_records)

            # Transform: Convert snapshot to kpi_values records
            logger.info("Transforming KPI snapshot to time-series records...")
            assert self.transformer is not None, "transformer must be set for KPISnapshotPipeline"
            transformation = self.transformer.transform(extraction_records)
            result.transformation = transformation

            if transformation.errors:
                result.errors.extend([f"transform: {e}" for e in transformation.errors])

            # Quality check
            if quality_check and transformation.records:
                from ai_company.data.etl.quality.validator import validate_records

                violations = validate_records(transformation.records, "kpi_values")
                result.quality_violations = violations
                if any(v["severity"] == "critical" for v in violations):
                    result.quality_check_passed = False
                    result.errors.append("Quality check failed: critical violations")
                    logger.warning("KPI snapshot quality check failed: %d critical violations", sum(1 for v in violations if v["severity"] == "critical"))

            # Load: Store in SQLite
            if result.quality_check_passed or not any(v["severity"] == "critical" for v in result.quality_violations):
                logger.info("Loading %d KPI records into SQLite...", len(transformation.records))
                assert self.loader is not None, "loader must be set for KPISnapshotPipeline"
                load_result = self.loader.load(transformation.records)
                result.load = load_result
                logger.info("KPI snapshot loaded: %d records, %d failed", load_result.loaded_count, load_result.failed_count)

                if load_result.errors:
                    result.errors.extend([f"load: {e}" for e in load_result.errors])

        except Exception as exc:  # noqa: BLE001
            logger.exception("KPI snapshot pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result

    def _make_extraction_result(self, records: list[dict[str, Any]]) -> ExtractionResult[dict[str, Any]]:
        """Create extraction result for the snapshot."""
        from ai_company.data.etl.base import ExtractionResult
        return ExtractionResult(
            records=records,
            source="kpi_collectors",
            extracted_at=datetime.now(timezone.utc).isoformat(),
        )


class CompanyKPIPipeline(Pipeline):
    """Pipeline for computing company-level KPIs (KPI-001 to KPI-005)."""

    def __init__(
        self,
        database: Database,
        project_root: Path | None = None,
    ):
        self.project_root = project_root or get_project_root()

        from ai_company.data.etl.transformers.kpi_transformer import CompanyKPITransformer

        extractor = TaskExtractor(database)
        transformer = CompanyKPITransformer()
        loader = None  # Company KPIs are written to config/company/kpis.yaml, not SQLite

        super().__init__(
            name="company_kpi",
            database=database,
            extractor=extractor,
            transformer=transformer,
            loader=loader,
        )

    def run(
        self,
        since: str | None = None,
        batch_size: int = 1000,
        quality_check: bool = True,
        write_to_yaml: bool = False,
        **kwargs: Any,
    ) -> PipelineResult:
        """Compute company-level KPIs from task telemetry.

        Args:
            since: Timestamp for incremental task extraction (30-day window default)
            batch_size: Max tasks to extract
            quality_check: Validate computed KPIs
            write_to_yaml: If True, update config/company/kpis.yaml
            **kwargs: Additional options

        Returns:
            PipelineResult with computed KPIs
        """
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            # Determine window
            if since is None:
                from datetime import timedelta
                since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()

            # Extract: Get tasks from SQLite (or fallback to file)
            logger.info("Extracting tasks for company KPI computation...")
            assert self.extractor is not None, "extractor must be set for CompanyKPIPipeline"
            extraction = self.extractor.extract(since=since, limit=batch_size)
            result.extraction = extraction

            if extraction.errors:
                result.errors.extend([f"extract: {e}" for e in extraction.errors])

            # Transform: Compute company KPIs
            logger.info("Computing company KPIs from %d tasks...", len(extraction.records))
            assert self.transformer is not None, "transformer must be set for CompanyKPIPipeline"
            transformation = self.transformer.transform(extraction.records)
            result.transformation = transformation

            if transformation.errors:
                result.errors.extend([f"transform: {e}" for e in transformation.errors])

            # Quality check
            if quality_check and transformation.records:
                from ai_company.data.etl.quality.validator import validate_records

                violations = validate_records(transformation.records, "company_kpis")
                result.quality_violations = violations
                if any(v["severity"] == "critical" for v in violations):
                    result.quality_check_passed = False
                    result.errors.append("Quality check failed: critical violations")

            # Load: Optionally write to YAML
            if write_to_yaml and transformation.records:
                logger.info("Writing company KPIs to config/company/kpis.yaml...")
                self._write_company_kpis_to_yaml(transformation.records)
                result.load = LoadResult(
                    loaded_count=len(transformation.records),
                    target="yaml:config/company/kpis.yaml",
                )
            else:
                # Computations are available in result.transformation.records
                # even when not writing to YAML - set a LoadResult to indicate
                # results are in-memory and available
                result.load = LoadResult(
                    loaded_count=len(transformation.records) if transformation.records else 0,
                    target="in-memory:company_kpi_computation",
                )

        except Exception as exc:  # noqa: BLE001
            logger.exception("Company KPI pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result

    def _write_company_kpis_to_yaml(self, kpi_records: list[dict[str, Any]]) -> None:
        """Update config/company/kpis.yaml with computed KPI values."""

        kpi_path = self.project_root / "config" / "company" / "kpis.yaml"
        if not kpi_path.exists():
            raise FileNotFoundError(f"KPI config not found: {kpi_path}")

        # Read current YAML preserving comments
        lines = kpi_path.read_text(encoding="utf-8").splitlines(keepends=True)

        # Build updates dict
        updates = {}
        for record in kpi_records:
            kpi_id = record["kpi_id"]
            updates[kpi_id] = {
                "current": record["current"],
                "computed_at": f'"{record["computed_at"]}"',
            }

        # Apply updates (similar to compute_company_kpis.py)
        current_id = None
        out = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("- id:"):
                current_id = stripped.split(":", 1)[1].strip().strip("\"'")

            if current_id in updates and stripped.startswith(("current:", "computed_at:")):
                field = stripped.split(":", 1)[0]
                new_value = updates[current_id][field]
                indent = line[: len(line) - len(line.lstrip())]
                comment = line.split("#", 1)[1].strip() if "#" in line else ""
                suffix = f"  # {comment}" if comment else ""
                line = f"{indent}{field}: {new_value}{suffix}\n"

            out.append(line)

        kpi_path.write_text("".join(out), encoding="utf-8")
        logger.info("Updated company KPIs in %s", kpi_path)


class CostAggregationPipeline(Pipeline):
    """Pipeline for daily/weekly/monthly cost aggregation."""

    def __init__(
        self,
        database: Database,
        period: str = "daily",
    ):
        from ai_company.data.etl.loaders.sqlite_loader import CostAggregationLoader
        from ai_company.data.etl.transformers.kpi_transformer import CostAggregationTransformer

        extractor = CostRecordExtractor(database)
        transformer = CostAggregationTransformer(period=period)
        loader = CostAggregationLoader(database)

        super().__init__(
            name=f"cost_{period}_aggregation",
            database=database,
            extractor=extractor,
            transformer=transformer,
            loader=loader,
        )
        self.period = period

    def run(
        self,
        since: str | None = None,
        batch_size: int = 10000,
        quality_check: bool = True,
        **kwargs: Any,
    ) -> PipelineResult:
        """Aggregate cost records for the specified period."""
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            # Default to last 30 days if no since provided
            if since is None:
                from datetime import timedelta
                since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()

            # Extract
            logger.info("Extracting cost records for %s aggregation...", self.period)
            assert self.extractor is not None, "extractor must be set"
            extraction = self.extractor.extract(since=since, limit=batch_size)
            result.extraction = extraction

            if extraction.errors:
                result.errors.extend([f"extract: {e}" for e in extraction.errors])

            # Transform
            logger.info("Aggregating %d cost records...", len(extraction.records))
            assert self.transformer is not None, "transformer must be set"
            transformation = self.transformer.transform(extraction.records)
            result.transformation = transformation

            if transformation.errors:
                result.errors.extend([f"transform: {e}" for e in transformation.errors])

            # Quality check
            if quality_check and transformation.records:
                from ai_company.data.etl.quality.validator import validate_records

                violations = validate_records(transformation.records, f"cost_{self.period}_aggregation")
                result.quality_violations = violations
                if any(v["severity"] == "critical" for v in violations):
                    result.quality_check_passed = False
                    result.errors.append("Quality check failed: critical violations")

            # Load: Store aggregated results in SQLite
            if result.quality_check_passed or not any(v["severity"] == "critical" for v in result.quality_violations):
                logger.info("Loading %d cost aggregation records into SQLite...", len(transformation.records))
                assert self.loader is not None, "loader must be set"
                load_result = self.loader.load(transformation.records)
                result.load = load_result
                logger.info("Cost aggregation loaded: %d records, %d failed", load_result.loaded_count, load_result.failed_count)

                if load_result.errors:
                    result.errors.extend([f"load: {e}" for e in load_result.errors])

        except Exception as exc:  # noqa: BLE001
            logger.exception("Cost aggregation pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result


class AgentPerformancePipeline(Pipeline):
    """Pipeline for agent performance analytics."""

    def __init__(
        self,
        database: Database,
        days: int = 30,
    ):
        from ai_company.data.etl.loaders.sqlite_loader import AgentPerformanceMetricsLoader
        from ai_company.data.etl.transformers.kpi_transformer import AgentPerformanceTransformer

        # We need both tasks and audit events - use a composite extractor
        self.task_extractor = TaskExtractor(database)
        self.audit_extractor = AuditEventExtractor(database)

        transformer = AgentPerformanceTransformer(days=days)
        loader = AgentPerformanceMetricsLoader(database)

        super().__init__(
            name="agent_performance",
            database=database,
            extractor=None,  # Custom extraction
            transformer=transformer,
            loader=loader,
        )
        self.days = days

    def run(
        self,
        since: str | None = None,
        batch_size: int = 10000,
        quality_check: bool = True,
        **kwargs: Any,
    ) -> PipelineResult:
        """Compute agent performance metrics."""
        result = self._create_result()
        self._audit_pipeline_start(result)

        try:
            if since is None:
                from datetime import timedelta
                since = (datetime.now(timezone.utc) - timedelta(days=self.days)).isoformat()

            # Extract tasks
            logger.info("Extracting tasks for agent performance...")
            task_extraction = self.task_extractor.extract(since=since, limit=batch_size)
            if task_extraction.errors:
                result.errors.extend([f"task_extract: {e}" for e in task_extraction.errors])

            # Extract audit events
            logger.info("Extracting audit events for agent performance...")
            audit_extraction = self.audit_extractor.extract(since=since, limit=batch_size)
            if audit_extraction.errors:
                result.errors.extend([f"audit_extract: {e}" for e in audit_extraction.errors])

            # Combine for transform
            combined_records = task_extraction.records + audit_extraction.records
            result.extraction = ExtractionResult(
                records=combined_records,
                source="tasks+audit",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

            # Transform
            logger.info("Computing agent performance for %d agents...", self.days)
            assert self.transformer is not None, "transformer must be set"
            transformation = self.transformer.transform(
                combined_records,
                tasks=task_extraction.records,
                audit_events=audit_extraction.records,
            )
            result.transformation = transformation

            if transformation.errors:
                result.errors.extend([f"transform: {e}" for e in transformation.errors])

            # Quality check
            if quality_check and transformation.records:
                from ai_company.data.etl.quality.validator import validate_records

                violations = validate_records(transformation.records, "agent_performance")
                result.quality_violations = violations
                if any(v["severity"] == "critical" for v in violations):
                    result.quality_check_passed = False
                    result.errors.append("Quality check failed: critical violations")

            # Load: Store agent performance metrics in SQLite
            if result.quality_check_passed or not any(v["severity"] == "critical" for v in result.quality_violations):
                logger.info("Loading %d agent performance records into SQLite...", len(transformation.records))
                assert self.loader is not None, "loader must be set"
                load_result = self.loader.load(transformation.records)
                result.load = load_result
                logger.info("Agent performance loaded: %d records, %d failed", load_result.loaded_count, load_result.failed_count)

                if load_result.errors:
                    result.errors.extend([f"load: {e}" for e in load_result.errors])

        except Exception as exc:  # noqa: BLE001
            logger.exception("Agent performance pipeline failed")
            result.errors.append(f"pipeline: {exc}")

        result.mark_completed()
        self._audit_pipeline_complete(result)
        return result


__all__ = [
    "KPISnapshotPipeline",
    "CompanyKPIPipeline",
    "CostAggregationPipeline",
    "AgentPerformancePipeline",
]
