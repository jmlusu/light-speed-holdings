"""Canonical Job model for the Unified Career Automation system.

Every captured job must conform to this model.  Original evidence files
(e.g. saved HTML, PDFs, screenshots) are kept separate from these
normalized records.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CaptureMethod(str, Enum):
    """How the job was captured."""

    HTML_SAVED = "html_saved"
    PDF_PRINTOUT = "pdf_printout"
    VISIBLE_TEXT = "visible_text"
    MANUAL_SUPPLY = "manual_supply"
    EMAIL_ALERT = "email_alert"


class ExtractionConfidence(str, Enum):
    """Confidence level for extracted fields."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ExtractionWarning(str, Enum):
    """Warning flags for extraction issues."""

    NO_JSON_LD = "no_json_ld"
    INCOMPLETE_META = "incomplete_meta"
    POOR_FORMAT = "poor_format"
    MISSING_FIELDS = "missing_fields"
    PARSE_ERROR = "parse_error"


class EmploymentType(str, Enum):
    """Available employment types."""

    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    CONTRACT_TO_HIRE = "contract_to_hire"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class CapturedJob(BaseModel):
    """Normalized job record conforming to the canonical capture contract.

    Attributes:
        source_name: Name of the job board/origin.
        original_url: The original job posting URL.
        capture_timestamp: When the job was captured (ISO 8601).
        job_title: The job title as stated in the posting.
        employer: The hiring employer.
        location: Job location (city, region, or "Remote").
        employment_type: Employment type if available.
        description: Full available job description.
        closing_date: Application closing date if available.
        capture_method: How the job was captured (CaptureMethod enum).
        evidence_file: Reference to the original evidence file.
        extraction_confidence: Confidence level for extracted fields.
        extraction_warnings: List of extraction warning flags.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    source_name: str
    original_url: str
    capture_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    job_title: str
    employer: str
    location: str
    employment_type: Optional[EmploymentType] = None
    description: str
    closing_date: Optional[str] = None
    capture_method: CaptureMethod
    evidence_file: str  # path or reference to original evidence
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNKNOWN
    extraction_warnings: list[ExtractionWarning] = Field(default_factory=list)

    def has_complete_info(self) -> bool:
        """Return True if all required fields have non-empty values."""
        return bool(self.job_title and self.employer and self.location and self.description)

    def has_expiry(self) -> bool:
        """Return True if a closing date is set and appears valid."""
        if not self.closing_date:
            return False
        return bool(self.closing_date.strip())

    def is_expired(self) -> bool:
        """Return True if the closing date has passed.

        Note: This is a simple comparison; full expiry logic may use
        the eligibility gate.
        """
        if not self.closing_date:
            return False
        try:
            from datetime import datetime as _dt

            closing = _dt.fromisoformat(self.closing_date.replace("Z", "+00:00"))
            now = _dt.now(timezone.utc)
            return now > closing
        except Exception:
            return False


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def build_from_evidence(
    *,
    source_name: str,
    original_url: str,
    capture_method: CaptureMethod,
    evidence_file: str,
    extraction_warnings: list[ExtractionWarning] | None = None,
    **kwargs: object,
) -> CapturedJob:
    """Factory to build a CapturedJob from evidence reference.

    Ensures evidence_file is always set and extraction_warnings defaults
    are applied consistently across all capture methods.
    """
    warnings = list(extraction_warnings) if extraction_warnings else []
    return CapturedJob(
        source_name=source_name,
        original_url=original_url,
        capture_method=capture_method,
        evidence_file=evidence_file,
        extraction_warnings=warnings,
        **kwargs,
    )
