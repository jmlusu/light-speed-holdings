"""Pipeline for the Unified Career Automation system.

Contains:
- Canonical job models (pipeline.models.job)
- Extraction utilities (pipeline.extraction)
- Browser-assisted discovery (pipeline.discovery)
- Source import and orchestration interfaces
"""

from __future__ import annotations

from pipeline.models.job import (
    CapturedJob,
    CaptureMethod,
    ExtractionConfidence,
    ExtractionWarning,
    EmploymentType,
    build_from_evidence,
)

from pipeline.extraction import extract_job_data

from pipeline.discovery import (
    initiate_browser_session,
    complete_session,
    feed_to_pipeline,
    capture_from_saved_html,
    capture_from_pdf,
    capture_manual_description,
    capture_from_email_alert,
    BrowserSession,
    record_selected_posting,
)

# build_captured_job is re-exported from extraction module
build_captured_job = None  # defined in extraction.py

__all__ = [
    "CapturedJob",
    "CaptureMethod",
    "ExtractionConfidence",
    "ExtractionWarning",
    "EmploymentType",
    "build_from_evidence",
    "extract_job_data",
    "initiate_browser_session",
    "complete_session",
    "feed_to_pipeline",
    "capture_from_saved_html",
    "capture_from_pdf",
    "capture_manual_description",
    "capture_from_email_alert",
    "BrowserSession",
    "record_selected_posting",
]