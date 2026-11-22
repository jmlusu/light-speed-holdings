"""Extraction utilities for job postings from various capture formats.

Supports:
- JSON-LD JobPosting extraction (primary)
- Fallback visible-text extraction
- HTML saved pages
- PDF printouts
- Manually supplied descriptions
- Job-alert email imports
"""

from __future__ import annotations

import re
from typing import Any

from pipeline.models.job import (
    CapturedJob,
    CaptureMethod,
    ExtractionConfidence,
    ExtractionWarning,
)

# ---------------------------------------------------------------------------
# JSON-LD extraction
# ---------------------------------------------------------------------------


def _extract_json_ld(text: str) -> dict[str, Any] | None:
    """Try to extract a JSON-LD @context block containing JobPosting.

    Returns the parsed JSON dict if a valid JobPosting is found, or None.
    """
    if not text:
        return None

    # Match <script type="application/ld+json">...</script>
    matches = re.findall(
        r'<script\s+type="application/ld\+json"\s*>(.*?)</script>',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    for raw in matches:
        raw_clean = re.sub(r"\s+", " ", raw).strip()
        try:
            data = __import__("json").loads(raw_clean)
        except (ValueError, Exception):
            continue

        # Validate it looks like a JobPosting
        if isinstance(data, dict):
            # Check for typical JobPosting fields
            title = data.get("title")
            if title:
                return data
            # Also accept if it has "jobTitle"
            if data.get("jobTitle"):
                return data
            # Accept any LD+JSON block as potential job data
            if any(k in data for k in ("title", "jobTitle", "description")):
                return data

    return None


def extract_json_ld(job_text: str) -> dict[str, Any] | None:
    """Public entry point for JSON-LD extraction.

    Args:
        job_text: Raw text/HTML of a job posting.

    Returns:
        Parsed JSON dict or None if no valid JobPosting found.
    """
    return _extract_json_ld(job_text)


# ---------------------------------------------------------------------------
# Fallback visible-text extraction
# ---------------------------------------------------------------------------


def _strip_html(html: str) -> str:
    """Remove HTML tags, preserving visible text content."""
    if not html:
        return ""
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_key_value_pairs(text: str) -> dict[str, str]:
    """Try to pull key:value pairs from free-form text.

    Looks for common patterns like "Location:", "Closing:", etc.
    """
    kv: dict[str, str] = {}
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Pattern: "Label: value" or "Label - value"
        m = re.match(r"^(Location|location|Location:)\s*(.+)$", line, re.IGNORECASE)
        if m and "location" not in kv:
            kv["location"] = m.group(2).strip()
        m = re.match(r"^(Closing|Closing date|closing|closes)\s*(.+)$", line, re.IGNORECASE)
        if m and "closing_date" not in kv:
            kv["closing_date"] = m.group(2).strip()
        m = re.match(r"^(Employer|Employer:|Company|company)\s*(.+)$", line, re.IGNORECASE)
        if m and "employer" not in kv:
            kv["employer"] = m.group(2).strip()
        m = re.match(r"^(Title|Job Title|Position|position)\s*(.+)$", line, re.IGNORECASE)
        if m and "job_title" not in kv:
            kv["job_title"] = m.group(2).strip()
    return kv


def extract_visible_text(job_text: str) -> dict[str, str]:
    """Extract job fields from visible text (fallback when no JSON-LD).

    Returns a dict with whatever fields can be identified.
    """
    if not job_text:
        return {}

    text = _strip_html(job_text)
    if not text.strip():
        return {}

    kv = _extract_key_value_pairs(text)

    # If we have enough body-like content, use the full text as description
    description = text
    # Trim to reasonable length if very long
    if len(description) > 2000:
        description = description[:2000] + "..."

    return {
        "job_title": kv.get("job_title") or "",
        "employer": kv.get("employer") or "",
        "location": kv.get("location") or "",
        "closing_date": kv.get("closing_date") or "",
        "description": description,
    }


# ---------------------------------------------------------------------------
# Capture-method-specific extractors
# ---------------------------------------------------------------------------


def extract_from_html(html: str, url: str | None = None) -> dict[str, Any]:
    """Extract job data from a saved HTML page.

    Tries JSON-LD first, then falls back to visible-text extraction.
    """
    result: dict[str, Any] = {}

    # Try JSON-LD first
    ld = extract_json_ld(html)
    if ld:
        result["job_title"] = ld.get("title") or ld.get("jobTitle") or ""
        result["employer"] = ld.get("hiringOrganization", {}).get("name") or ""
        result["location"] = (
            ld.get("jobLocation", {}).get("address", {}).get("addressLocality")
            or ld.get("jobLocation", {}).get("address", {}).get("addressRegion")
            or ""
        )
        result["description"] = ld.get("description") or ""
        result["closing_date"] = ld.get("validThrough") or ld.get("datePosted") or ""
        if result["closing_date"]:
            # Normalize to ISO-ish string
            result["closing_date"] = str(result["closing_date"])
        # Set confidence high if JSON-LD found
        result["extraction_confidence"] = "high"
        result["warnings"] = []
    else:
        # Fallback to visible text
        visible = extract_visible_text(html)
        result.update(visible)
        result["extraction_confidence"] = "medium"
        result["warnings"] = [ExtractionWarning.NO_JSON_LD]

    # Add source/URL context
    if url:
        result["original_url"] = url

    return result


def extract_from_pdf(pdf_text: str, url: str | None = None) -> dict[str, Any]:
    """Extract job data from a PDF printout's text content.

    Tries visible-text extraction since PDFs rarely have embedded JSON-LD.
    """
    result = extract_visible_text(pdf_text)

    if result.get("job_title") or result.get("employer") or result.get("location"):
        result["extraction_confidence"] = "medium"
        result["warnings"] = [ExtractionWarning.INCOMPLETE_META]
    else:
        result["extraction_confidence"] = "low"
        result["warnings"] = [ExtractionWarning.POOR_FORMAT, ExtractionWarning.MISSING_FIELDS]

    if url:
        result["original_url"] = url

    return result


def extract_from_manual(description: str, **overrides: object) -> dict[str, Any]:
    """Extract from a manually supplied job description.

    The *description* is treated as the full job text; other fields must
    be supplied via overrides or will be marked with warnings.
    """
    result: dict[str, Any] = {
        "description": description or "",
        "extraction_confidence": "low",
        "warnings": [
            ExtractionWarning.MISSING_FIELDS
        ],  # will be refined if overrides provide fields
    }

    # Apply any provided overrides
    for key, value in overrides.items():
        if key in ("job_title", "employer", "location", "closing_date"):
            result[key] = value

    # If we have at least a title, downgrade warnings
    if result.get("job_title"):
        # Remove MISSING_FIELDS if we have title, employer, location
        if result.get("employer") and result.get("location"):
            result["warnings"] = [
                w for w in result["warnings"] if w != ExtractionWarning.MISSING_FIELDS
            ]
        else:
            result["warnings"].append(ExtractionWarning.MISSING_FIELDS)

    if url := overrides.get("original_url"):
        result["original_url"] = url

    return result


def extract_from_email_alert(email_body: str, url: str | None = None) -> dict[str, Any]:
    """Extract from a job-alert email import.

    Emails are authorized separately; this extracts whatever job data
    appears in the body.
    """
    result = extract_visible_text(email_body)

    if not result.get("job_title") and not result.get("employer"):
        result["extraction_confidence"] = "low"
        result["warnings"] = [
            ExtractionWarning.POOR_FORMAT,
            ExtractionWarning.MISSING_FIELDS,
        ]
    else:
        result["extraction_confidence"] = "medium"
        result["warnings"] = [ExtractionWarning.NO_JSON_LD]

    if url:
        result["original_url"] = url

    return result


# -------------------------------------------------------------------------
# High-level: try all methods, produce a unified extraction result
# -------------------------------------------------------------------------


def extract_job_data(
    content: str,
    *,
    capture_method: CaptureMethod,
    url: str | None = None,
    evidence_file: str | None = None,
) -> dict[str, Any]:
    """Extract job data from content using the specified capture method.

    This is the main entry point. It dispatches to the method-appropriate
    extractor and then normalizes the output into a common dict format.

    Returns a dict with these keys (at minimum):
        job_title, employer, location, description, closing_date,
        original_url, extraction_confidence, extraction_warnings
    """
    # Normalize capture method name
    method = capture_method

    # Dispatch
    if method == CaptureMethod.HTML_SAVED:
        raw = extract_from_html(content, url=url)
    elif method == CaptureMethod.PDF_PRINTOUT:
        raw = extract_from_pdf(content, url=url)
    elif method == CaptureMethod.MANUAL_SUPPLY:
        raw = extract_from_manual(content)
    elif method == CaptureMethod.EMAIL_ALERT:
        raw = extract_from_email_alert(content, url=url)
    else:  # VISIBLE_TEXT or fallback
        raw = extract_visible_text(content)

    # Ensure required keys exist
    normalized: dict[str, Any] = {
        "job_title": raw.get("job_title", ""),
        "employer": raw.get("employer", ""),
        "location": raw.get("location", ""),
        "description": raw.get("description", ""),
        "closing_date": raw.get("closing_date", ""),
        "original_url": raw.get("original_url", url or ""),
        "extraction_confidence": raw.get("extraction_confidence", ExtractionConfidence.UNKNOWN),
        "extraction_warnings": raw.get("warnings", []),
    }

    # If we have no confidence set, default to low
    if not normalized["extraction_confidence"]:
        normalized["extraction_confidence"] = ExtractionConfidence.LOW

    # Ensure warnings is a list
    warnings = normalized["extraction_warnings"]
    if not isinstance(warnings, list):
        normalized["extraction_warnings"] = [warnings] if warnings else []

    return normalized


# -------------------------------------------------------------------------
# Build CapturedJob from extracted data + evidence reference
# -------------------------------------------------------------------------


def build_captured_job(
    *,
    source_name: str,
    original_url: str,
    capture_method: CaptureMethod,
    evidence_file: str,
    extraction_warnings: list[ExtractionWarning] | None = None,
    **kwargs: object,
) -> CapturedJob:
    """Construct a CapturedJob from extracted data and an evidence reference.

    This is the bridge between raw extraction and the canonical model.
    """
    kwargs.setdefault("source_name", source_name)
    kwargs.setdefault("original_url", original_url)
    kwargs.setdefault("capture_method", capture_method)
    kwargs.setdefault("evidence_file", evidence_file or "")
    kwargs.setdefault(
        "extraction_warnings",
        list(extraction_warnings) if extraction_warnings else [],
    )

    # Build the job; extra fields will be ignored or stored via model config
    job = CapturedJob(**kwargs)

    # Ensure warnings is never None
    if job.extraction_warnings is None:
        job.extraction_warnings = []

    return job
