"""ETL Pipeline Framework — Base Classes.

Abstract base classes for Extract, Transform, Load components.
All pipelines compose these building blocks.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from ai_company.data.database import Database

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class ExtractionResult(Generic[T]):
    """Result of an extraction operation."""

    records: list[T]
    extracted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = ""
    record_count: int = 0
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.record_count = len(self.records)


@dataclass
class TransformResult(Generic[R]):
    """Result of a transformation operation."""

    records: list[R]
    transformed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    input_count: int = 0
    output_count: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.output_count = len(self.records)


@dataclass
class LoadResult:
    """Result of a load operation."""

    loaded_count: int = 0
    failed_count: int = 0
    loaded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target: str = ""
    errors: list[str] = field(default_factory=list)
    skipped_count: int = 0


@dataclass
class PipelineResult:
    """Complete pipeline execution result."""

    pipeline_name: str
    started_at: str
    completed_at: str | None = None
    extraction: ExtractionResult[Any] | None = None
    transformation: TransformResult[Any] | None = None
    load: LoadResult | None = None
    quality_check_passed: bool = True
    quality_violations: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def mark_completed(self) -> None:
        self.completed_at = datetime.now(timezone.utc).isoformat()

    @property
    def success(self) -> bool:
        return len(self.errors) == 0 and self.load is not None and self.load.failed_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline_name": self.pipeline_name,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "extraction": self.extraction.__dict__ if self.extraction else None,
            "transformation": self.transformation.__dict__ if self.transformation else None,
            "load": self.load.__dict__ if self.load else None,
            "quality_check_passed": self.quality_check_passed,
            "quality_violations": self.quality_violations,
            "errors": self.errors,
            "success": self.success,
        }


class Extractor(Generic[T], ABC):
    """Abstract base for data extractors."""

    def __init__(self, source_name: str, database: Database | None = None):
        self.source_name = source_name
        self.database = database

    @abstractmethod
    def extract(self, since: str | None = None, limit: int | None = None, **kwargs: Any) -> ExtractionResult[T]:
        """Extract records from source.

        Args:
            since: ISO timestamp to extract records after (incremental)
            limit: Maximum records to extract
            **kwargs: Source-specific parameters

        Returns:
            ExtractionResult with records and metadata
        """
        pass

    def validate_connection(self) -> bool:
        """Verify source is accessible."""
        return True


class Transformer(Generic[T, R], ABC):
    """Abstract base for data transformers."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def transform(self, records: list[T], **kwargs: Any) -> TransformResult[R]:
        """Transform input records to output format.

        Args:
            records: Input records from extractor
            **kwargs: Transformation parameters

        Returns:
            TransformResult with transformed records
        """
        pass


class Loader(Generic[R], ABC):
    """Abstract base for data loaders."""

    def __init__(self, target_name: str, database: Database | None = None):
        self.target_name = target_name
        self.database = database

    @abstractmethod
    def load(self, records: list[R], **kwargs: Any) -> LoadResult:
        """Load transformed records into target.

        Args:
            records: Transformed records
            **kwargs: Load parameters (e.g., upsert_mode, batch_size)

        Returns:
            LoadResult with counts and errors
        """
        pass

    def validate_target(self) -> bool:
        """Verify target is accessible and ready."""
        return True


class Pipeline(ABC):
    """Abstract base for composed ETL pipelines."""

    def __init__(
        self,
        name: str,
        database: Database,
        extractor: Extractor[Any] | None = None,
        transformer: Transformer[Any, Any] | None = None,
        loader: Loader[Any] | None = None,
    ):
        self.name = name
        self.database = database
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self._result: PipelineResult | None = None

    @abstractmethod
    def run(
        self,
        since: str | None = None,
        batch_size: int = 1000,
        quality_check: bool = True,
        **kwargs: Any,
    ) -> PipelineResult:
        """Execute the full pipeline.

        Args:
            since: Incremental extraction timestamp
            batch_size: Records per batch
            quality_check: Run data quality validation
            **kwargs: Pipeline-specific parameters

        Returns:
            PipelineResult with execution details
        """
        pass

    def _create_result(self) -> PipelineResult:
        return PipelineResult(
            pipeline_name=self.name,
            started_at=datetime.now(timezone.utc).isoformat(),
        )

    def _audit_pipeline_start(self, result: PipelineResult) -> None:
        """Emit audit event for pipeline start."""
        try:
            from ai_company.audit.events import AuditEvent, AuditEventType
            from ai_company.audit.integration import get_writer

            writer = get_writer()
            if writer:
                writer.write(
                    AuditEvent(
                        event_type=AuditEventType.ETL_PIPELINE_START,
                        agent_id="etl_orchestrator",
                        tool="pipeline.run",
                        metadata={
                            "pipeline": self.name,
                            "started_at": result.started_at,
                            "extraction_source": self.extractor.source_name if self.extractor else "none",
                            "load_target": self.loader.target_name if self.loader else "none",
                        },
                    )
                )
        except Exception:  # noqa: BLE001 - audit is best-effort
            logger.debug("Audit hook skipped for pipeline start", exc_info=True)

    def _audit_pipeline_complete(self, result: PipelineResult) -> None:
        """Emit audit event for pipeline completion."""
        try:
            from ai_company.audit.events import AuditEvent, AuditEventType
            from ai_company.audit.integration import get_writer

            writer = get_writer()
            if writer:
                writer.write(
                    AuditEvent(
                        event_type=AuditEventType.ETL_PIPELINE_COMPLETE,
                        agent_id="etl_orchestrator",
                        tool="pipeline.run",
                        metadata={
                            "pipeline": self.name,
                            "started_at": result.started_at,
                            "completed_at": result.completed_at,
                            "success": result.success,
                            "extracted": result.extraction.record_count if result.extraction else 0,
                            "transformed": result.transformation.output_count if result.transformation else 0,
                            "loaded": result.load.loaded_count if result.load else 0,
                            "failed": result.load.failed_count if result.load else 0,
                            "quality_passed": result.quality_check_passed,
                            "errors": result.errors,
                        },
                    )
                )
        except Exception:  # noqa: BLE001 - audit is best-effort
            logger.debug("Audit hook skipped for pipeline complete", exc_info=True)


# Convenience function for simple extract-transform-load
def run_etl(
    extractor: Extractor[T],
    transformer: Transformer[T, R],
    loader: Loader[R],
    since: str | None = None,
    batch_size: int = 1000,
    quality_check: bool = True,
) -> PipelineResult:
    """Run a simple ETL flow with given components.

    This is a convenience function for one-off pipelines that don't
    need a full Pipeline subclass.
    """
    result = PipelineResult(
        pipeline_name=f"{extractor.source_name}->{loader.target_name}",
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    # Extract
    extraction = extractor.extract(since=since, limit=batch_size)
    result.extraction = extraction
    if extraction.errors:
        result.errors.extend([f"extract: {e}" for e in extraction.errors])

    # Transform
    if extraction.records:
        transformation = transformer.transform(extraction.records)
        result.transformation = transformation
        if transformation.errors:
            result.errors.extend([f"transform: {e}" for e in transformation.errors])

        # Quality check
        if quality_check and transformation.records:
            from ai_company.data.etl.quality.validator import validate_records

            violations = validate_records(transformation.records, loader.target_name)  # type: ignore[arg-type]
            result.quality_violations = violations
            if any(v["severity"] == "critical" for v in violations):
                result.quality_check_passed = False
                result.errors.append("Quality check failed: critical violations")

        # Load
        if result.quality_check_passed or not any(v["severity"] == "critical" for v in violations):
            load = loader.load(transformation.records)
            result.load = load
            if load.errors:
                result.errors.extend([f"load: {e}" for e in load.errors])

    result.mark_completed()
    return result


__all__ = [
    "ExtractionResult",
    "TransformResult",
    "LoadResult",
    "PipelineResult",
    "Extractor",
    "Transformer",
    "Loader",
    "Pipeline",
    "run_etl",
]
