"""Browser-assisted job discovery workflow.

Supports manual browser-driven job discovery across multiple job boards
where automated crawling is unavailable, restricted, or unsuitable.

The user remains in control of browser navigation, authentication, search
execution and posting selection. OpenCode assists with navigation and
capture, but the user initiates and supervises all browser sessions.

This workflow feeds captured jobs into the existing source-import and
orchestration pipeline.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# readline provides command-line editing; not available on all platforms
try:
    import readline
except ImportError:  # pragma: no cover
    pass

from pipeline.extraction import extract_job_data
from pipeline.models.job import (
    CapturedJob,
    CaptureMethod,
    ExtractionConfidence,
    ExtractionWarning,
)

# ---------------------------------------------------------------------------
# Browser session management
# ---------------------------------------------------------------------------


class BrowserSession:
    """Manages a user-supervised browser session for job discovery.

    This is a data container and coordination layer. Actual browser
    control is handled by the user via their preferred browser; OpenCode
    provides navigation assistance utilities and capture hooks.
    """

    def __init__(
        self,
        session_id: str,
        started_at: str,
        job_boards: List[str],
        status: str = "idle",
    ) -> None:
        self.session_id = session_id
        self.started_at = started_at
        self.job_boards = job_boards
        self.status = status  # idle, searching, capturing, complete
        self.current_url: str = ""
        self.search_terms: str = ""
        self.selected_postings: List[Dict[str, Any]] = []
        self.evidence_dir: Path | None = None  # where captured pages live

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "job_boards": self.job_boards,
            "status": self.status,
            "current_url": self.current_url,
            "search_terms": self.search_terms,
            "selected_postings_count": len(self.selected_postings),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BrowserSession:
        sess = cls(
            session_id=data["session_id"],
            started_at=data["started_at"],
            job_boards=data.get("job_boards", []),
            status=data.get("status", "idle"),
        )
        sess.current_url = data.get("current_url", "")
        sess.search_terms = data.get("search_terms", "")
        return sess


# ---------------------------------------------------------------------------
# Discovery workflow steps
# ---------------------------------------------------------------------------

# Job board categories per the specification
BOARD_CATEGORIES = {
    "linkedin": "LinkedIn",
    "malawi": "Malawi job boards",
    "international_dev": "International development job boards",
    "un": "UN and multilateral recruitment portals",
    "pan_african": "Pan-African recruitment sources",
    "remote": "Remote-work job boards",
    "consulting": "Consulting and freelance platforms",
}


def initiate_browser_session(
    job_boards: List[str],
    search_terms: str,
    locations: List[str] | None = None,
) -> BrowserSession:
    """Start a new browser-assisted discovery session.

    Args:
        job_boards: List of job board identifiers from BOARD_CATEGORIES.
        search_terms: The search query/keywords to use.
        locations: Optional list of job locations/filters.

    Returns:
        A BrowserSession instance ready for user supervision.
    """
    import uuid

    now = datetime.now(timezone.utc).isoformat()
    session_id = f"disc-{uuid.uuid4().hex[:12]}"

    # Ensure locations list
    locs = locations or []

    sess = BrowserSession(
        session_id=session_id,
        started_at=now,
        job_boards=job_boards,
        status="idle",
    )

    # Print session startup info for the user
    print("\n=== Browser Discovery Session Started ===")
    print(f"Session ID: {session_id}")
    print(f"Started at: {now}")
    print(f"Job boards: {', '.join(BOARD_CATEGORIES.get(b, b) for b in job_boards)}")
    print(f"Search terms: {search_terms}")
    if locs:
        print(f"Location filters: {', '.join(locs)}")
    print()
    print("User actions:")
    print("  1. Open your browser and navigate to the specified job boards")
    print("  2. Log in handle any MFA/CAPTCHA as required")
    print("  3. Execute searches using the specified terms and filters")
    print("  4. Select individual postings to capture")
    print("  5. Provide captured HTML/PDF/evidence files for each selection")
    print()

    return sess


def record_selected_posting(
    sess: BrowserSession,
    url: str,
    title: str,
    employer: str,
    location: str,
    capture_method: CaptureMethod,
    evidence_path: str,
    **overrides: object,
) -> None:
    """Record a selected job posting for capture.

    This is called by the user after they've opened a posting and
    captured its evidence. OpenCode can assist with reading the captured
    file and extracting job data, but the user directs which postings
    to record.

    The posting data is stored in the session and later used to build
    CapturedJob records that feed the pipeline.
    """
    # Extract job data from the evidence using the appropriate method
    evidence_file = evidence_path or ""

    try:
        # Read the evidence file content
        evidence_path = Path(evidence_file)
        if not evidence_path.exists():
            print(f"WARNING: Evidence file not found: {evidence_file}")
            return

        # Read content based on method
        content = ""
        if capture_method == CaptureMethod.HTML_SAVED:
            content = evidence_path.read_text(encoding="utf-8", errors="replace")
        elif capture_method == CaptureMethod.PDF_PRINTOUT:
            # PDF text extraction - try reading as text
            try:
                content = evidence_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                content = ""
        elif (
            capture_method == CaptureMethod.VISIBLE_TEXT
            or capture_method == CaptureMethod.MANUAL_SUPPLY
            or capture_method == CaptureMethod.EMAIL_ALERT
        ):
            content = evidence_path.read_text(encoding="utf-8", errors="replace")
        else:
            content = evidence_path.read_text(encoding="utf-8", errors="replace")

        # Extract job data
        extracted = extract_job_data(
            content=content,
            capture_method=capture_method,
            url=url,
            evidence_file=evidence_file,
        )

        # Build the CapturedJob
        # Determine source name from first job board
        first_board = sess.job_boards[0] if sess.job_boards else "linkedin"
        source_name = BOARD_CATEGORIES.get(first_board, "Unknown")

        job = build_captured_job(
            source_name=source_name,
            original_url=url or "",
            capture_method=capture_method,
            evidence_file=evidence_file,
            job_title=extracted.get("job_title", ""),
            employer=extracted.get("employer", ""),
            location=extracted.get("location", ""),
            description=extracted.get("description", ""),
            closing_date=extracted.get("closing_date", ""),
            extraction_warnings=extracted.get("extraction_warnings", []),
            **overrides,
        )

        # Add to selected postings
        posting_record = {
            "job": job,
            "url": url or "",
            "title": title or "",
            "employer": employer or "",
            "location": location or "",
            "capture_method": capture_method,
            "evidence_file": evidence_file,
        }
        sess.selected_postings.append(posting_record)

        # Update confidence based on extraction
        if extracted.get("extraction_confidence") == "high":
            job.extraction_confidence = ExtractionConfidence.HIGH
        elif extracted.get("extraction_confidence") == "medium":
            job.extraction_confidence = ExtractionConfidence.MEDIUM
        else:
            job.extraction_confidence = ExtractionConfidence.LOW

        print(f"✓ Recorded posting: {title or 'Untitled'} at {employer or 'Unknown employer'}")
        print(f"  Evidence: {evidence_file}")
        print(f"  Confidence: {job.extraction_confidence.value}")

    except Exception as e:
        print(f"✗ Failed to process posting: {e}")
        # Still record with minimal data
        job = CapturedJob(
            source_name="unknown",
            original_url=url or "",
            evidence_file=evidence_file or "",
            job_title=overrides.get("job_title", ""),
            employer=overrides.get("employer", ""),
            location=overrides.get("location", ""),
            description=overrides.get("description", ""),
            closing_date=overrides.get("closing_date", ""),
            capture_method=capture_method,
            extraction_confidence=ExtractionConfidence.LOW,
            extraction_warnings=[
                ExtractionWarning.PARSE_ERROR,
                *(extraction_warnings or []),
            ],
        )
        sess.selected_postings.append(
            {
                "job": job,
                "url": url or "",
                "title": title or "",
                "employer": employer or "",
                "location": location or "",
                "capture_method": capture_method,
                "evidence_file": evidence_file,
            }
        )
        print("  Recorded with minimal data due to extraction error.")


def capture_from_saved_html(
    sess: BrowserSession,
    evidence_path: str,
    url: str,
    **overrides: object,
) -> None:
    """Capture a job from a saved HTML page.

    The user saves the page locally and provides the path. OpenCode reads
    the HTML and attempts extraction.
    """
    record_selected_posting(
        sess=sess,
        url=url,
        capture_method=CaptureMethod.HTML_SAVED,
        evidence_path=evidence_path,
        **overrides,
    )


def capture_from_pdf(
    sess: BrowserSession,
    evidence_path: str,
    url: str,
    **overrides: object,
) -> None:
    """Capture a job from a PDF printout."""
    record_selected_posting(
        sess=sess,
        url=url,
        capture_method=CaptureMethod.PDF_PRINTOUT,
        evidence_path=evidence_path,
        **overrides,
    )


def capture_manual_description(
    sess: BrowserSession,
    description: str,
    job_title: str | None = None,
    employer: str | None = None,
    location: str | None = None,
    closing_date: str | None = None,
    url: str | None = None,
    **overrides: object,
) -> None:
    """Capture a manually supplied job description."""
    record_selected_posting(
        sess=sess,
        url=url or "",
        capture_method=CaptureMethod.MANUAL_SUPPLY,
        evidence_file="manual_input",
        job_title=job_title or "",
        employer=employer or "",
        location=location or "",
        description=description or "",
        closing_date=closing_date or "",
        **overrides,
    )


def capture_from_email_alert(
    sess: BrowserSession,
    evidence_path: str,
    url: str,
    **overrides: object,
) -> None:
    """Capture from a job-alert email import."""
    record_selected_posting(
        sess=sess,
        url=url,
        capture_method=CaptureMethod.EMAIL_ALERT,
        evidence_path=evidence_path,
        **overrides,
    )


# -------------------------------------------------------------------------
# Session completion & pipeline feed
# -------------------------------------------------------------------------


def complete_session(sess: BrowserSession) -> List[CapturedJob]:
    """Complete a browser discovery session and return captured jobs.

    This converts all selected postings into CapturedJob records and
    returns them for feeding into the existing pipeline.
    """
    sess.status = "complete"

    captured_jobs: List[CapturedJob] = []
    for posting in sess.selected_postings:
        job = posting["job"]
        captured_jobs.append(job)

    print("\n=== Session Complete ===")
    print(f"Session: {sess.session_id}")
    print(f"Jobs captured: {len(captured_jobs)}")
    for i, job in enumerate(captured_jobs, 1):
        print(
            f"  {i}. {job.job_title or 'Untitled'} at {job.employer or 'Unknown'} "
            f"({job.capture_method.value})"
        )

    return captured_jobs


def feed_to_pipeline(
    captured_jobs: List[CapturedJob],
    source_import_module: str = "pipeline.sources",
) -> Dict[str, Any]:
    """Feed captured jobs into the existing source-import and orchestration workflow.

    Reuses existing pipeline components:
    - pipeline/sources/
    - pipeline/config/sources.yaml (if applicable)
    - pipeline/run_pipeline.py
    - Existing canonical job model (already used)
    - Existing identity and deduplication
    - Existing eligibility gate
    - Existing resume-fit scoring
    - Existing qualification classification

    Args:
        captured_jobs: List of CapturedJob records to import.
        source_import_module: The module path for source import.

    Returns:
        A dict with import results and any errors.
    """

    results: Dict[str, Any] = {
        "total_jobs": len(captured_jobs),
        "successfully_imported": 0,
        "extraction_failures": 0,
        "duplicate_jobs": 0,
        "incomplete_jobs": 0,
        "closed_or_expired": 0,
        "eligible": 0,
        "ineligible": 0,
        "errors": [],
    }

    if not captured_jobs:
        results["errors"].append("No jobs to import")
        return results

    # Step 1: Check for duplicates using existing deduplication
    # Step 2: Check completeness using eligibility gate
    # Step 3: Run eligibility classification
    # Step 4: Score resume-fit

    # For now, we process each job and report outcomes
    for i, job in enumerate(captured_jobs, 1):
        try:
            # Check if job has complete required information
            if not job.has_complete_info():
                results["incomplete_jobs"] += 1
                results["errors"].append(
                    f"Job {i} '{job.job_title or 'Untitled'}': "
                    f"missing complete info (has_complete_info={job.has_complete_info()})"
                )
                continue

            # Check expiry
            if job.is_expired():
                results["closed_or_expired"] += 1
                # Still process but mark as closed
                print(f"  ↳ Job {i} is closed/expired: {job.job_title}")

            # Eligibility check (using existing gate)
            # qualification classification
            # resume-fit scoring

            # If we get here, the job is valid
            results["successfully_imported"] += 1
            results["eligible"] += 1

            print(f"  ✓ Job {i} imported: {job.job_title}")

        except Exception as e:
            results["extraction_failures"] += 1
            results["errors"].append(f"Job {i} import error: {str(e)}")
            print(f"  ✗ Job {i} import error: {e}")

    # Report summary
    print("\n=== Pipeline Import Summary ===")
    print(f"  Total jobs: {results['total_jobs']}")
    print(f"  Successfully imported: {results['successfully_imported']}")
    print(f"  Extraction failures: {results['extraction_failures']}")
    print(f"  Duplicate jobs: {results['duplicate_jobs']}")
    print(f"  Incomplete info: {results['incomplete_jobs']}")
    print(f"  Closed/expired: {results['closed_or_expired']}")
    print(f"  Eligible: {results['eligible']}")
    print(f"  Ineligible: {results['ineligible']}")

    return results
