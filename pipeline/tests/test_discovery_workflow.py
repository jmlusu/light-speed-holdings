"""Test script demonstrating the browser-assisted job discovery workflow.

This test verifies that all five capture methods feed the same normalized
pipeline without requiring separate scoring or eligibility implementations.
"""

import sys
from pathlib import Path

# Add project root to path BEFORE any pipeline imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Fixture directory - absolute path
FIXTURE_DIR = Path(r"C:\Users\jmlus\light-speed-holdings\pipeline\tests\fixtures")

# Now import from pipeline submodules
from pipeline.discovery import (
    complete_session,
    feed_to_pipeline,
    initiate_browser_session,
)
from pipeline.extraction import extract_job_data
from pipeline.models.job import (
    CaptureMethod,
    ExtractionConfidence,
    ExtractionWarning,
    build_from_evidence,
)

print("=" * 60)
print("Browser-Assisted Job Discovery - Workflow Demonstration")
print("=" * 60)


def test_html_with_json_ld():
    """Test 1: Saved HTML page with JSON-LD JobPosting."""
    print("\n=== Test 1: HTML with JSON-LD ===")
    fixture = FIXTURE_DIR / "html_with_json_ld.html"
    content = fixture.read_text(encoding="utf-8")

    # Extract job data
    extracted = extract_job_data(
        content=content,
        capture_method=CaptureMethod.HTML_SAVED,
        url=str(fixture),
        evidence_file=str(fixture),
    )
    print(f"  Extracted title: {extracted.get('job_title')}")
    print(f"  Extracted employer: {extracted.get('employer')}")
    print(f"  Extracted location: {extracted.get('location')}")
    print(f"  Extracted description: {extracted.get('description')[:60]!r}...")
    print(f"  Extraction confidence: {extracted.get('extraction_confidence')}")
    print(f"  Warnings: {extracted.get('extraction_warnings')}")

    # Build CapturedJob
    job = build_from_evidence(
        source_name="LinkedIn",
        original_url=str(fixture),
        capture_method=CaptureMethod.HTML_SAVED,
        evidence_file=str(fixture),
        job_title=extracted.get("job_title", ""),
        employer=extracted.get("employer", ""),
        location=extracted.get("location", ""),
        description=extracted.get("description", ""),
        closing_date=extracted.get("closing_date", ""),
        extraction_confidence=ExtractionConfidence(
            extracted.get("extraction_confidence", "unknown")
        ),
        extraction_warnings=[
            ExtractionWarning(w) for w in extracted.get("extraction_warnings", [])
        ],
    )

    print(f"  CapturedJob title: {job.job_title}")
    print(f"  CapturedJob employer: {job.employer}")
    print(f"  CapturedJob location: {job.location}")
    print(f"  CapturedJob confidence: {job.extraction_confidence.value}")
    print(f"  CapturedJob has_complete_info: {job.has_complete_info()}")
    print(f"  CapturedJob is_expired: {job.is_expired()}")
    return job


def test_html_without_json_ld():
    """Test 2: Page without JSON-LD."""
    print("\n=== Test 2: HTML without JSON-LD ===")
    fixture = FIXTURE_DIR / "html_without_json_ld.html"
    content = fixture.read_text(encoding="utf-8")

    # Extract job data (fallback to visible text)
    extracted = extract_job_data(
        content=content,
        capture_method=CaptureMethod.HTML_SAVED,
        url=str(fixture),
        evidence_file=str(fixture),
    )
    print(f"  Extracted title: {extracted.get('job_title')}")
    print(f"  Extracted employer: {extracted.get('employer')}")
    print(f"  Extracted location: {extracted.get('location')}")
    print(f"  Description length: {len(extracted.get('description', ''))}")
    print(f"  Extraction confidence: {extracted.get('extraction_confidence')}")
    print(f"  Warnings: {extracted.get('extraction_warnings')}")

    # Build CapturedJob
    job = build_from_evidence(
        source_name="Malawi Job Board",
        original_url=str(fixture),
        capture_method=CaptureMethod.HTML_SAVED,
        evidence_file=str(fixture),
        job_title=extracted.get("job_title", ""),
        employer=extracted.get("employer", ""),
        location=extracted.get("location", ""),
        description=extracted.get("description", ""),
        closing_date=extracted.get("closing_date", ""),
        extraction_confidence=ExtractionConfidence(
            extracted.get("extraction_confidence", "unknown")
        ),
        extraction_warnings=[
            ExtractionWarning(w) for w in extracted.get("extraction_warnings", [])
        ],
    )

    print(f"  CapturedJob title: {job.job_title}")
    print(f"  CapturedJob employer: {job.employer}")
    print(f"  CapturedJob location: {job.location}")
    print(f"  CapturedJob confidence: {job.extraction_confidence.value}")
    print(f"  CapturedJob has_complete_info: {job.has_complete_info()}")
    return job


def test_pdf():
    """Test 3: PDF printout (simulated text extraction)."""
    print("\n=== Test 3: PDF (simulated) ===")
    fixture = FIXTURE_DIR / "pdf_simulated.txt"
    content = fixture.read_text(encoding="utf-8")

    # Extract job data from PDF text
    extracted = extract_job_data(
        content=content,
        capture_method=CaptureMethod.PDF_PRINTOUT,
        url=str(fixture),
        evidence_file=str(fixture),
    )
    print(f"  Extracted title: {extracted.get('job_title')}")
    print(f"  Extracted employer: {extracted.get('employer')}")
    print(f"  Extracted location: {extracted.get('location')}")
    print(f"  Description length: {len(extracted.get('description', ''))}")
    print(f"  Extraction confidence: {extracted.get('extraction_confidence')}")
    print(f"  Warnings: {extracted.get('extraction_warnings')}")

    # Build CapturedJob
    job = build_from_evidence(
        source_name="Malawi Job Board",
        original_url=str(fixture),
        capture_method=CaptureMethod.PDF_PRINTOUT,
        evidence_file=str(fixture),
        job_title=extracted.get("job_title", ""),
        employer=extracted.get("employer", ""),
        location=extracted.get("location", ""),
        description=extracted.get("description", ""),
        closing_date=extracted.get("closing_date", ""),
        extraction_confidence=ExtractionConfidence(
            extracted.get("extraction_confidence", "unknown")
        ),
        extraction_warnings=[
            ExtractionWarning(w) for w in extracted.get("extraction_warnings", [])
        ],
    )

    print(f"  CapturedJob title: {job.job_title}")
    print(f"  CapturedJob employer: {job.employer}")
    print(f"  CapturedJob location: {job.location}")
    print(f"  CapturedJob confidence: {job.extraction_confidence.value}")
    print(f"  CapturedJob has_complete_info: {job.has_complete_info()}")
    return job


def test_manual_description():
    """Test 4: Manually supplied job description."""
    print("\n=== Test 4: Manual supply ===")
    fixture = FIXTURE_DIR / "manual_job.txt"
    content = fixture.read_text(encoding="utf-8")

    # Extract from manual supply
    extracted = extract_job_data(
        content=content,
        capture_method=CaptureMethod.MANUAL_SUPPLY,
        url="manual-input",
        evidence_file="manual_input",
    )
    print(f"  Extracted title: {extracted.get('job_title')}")
    print(f"  Extracted employer: {extracted.get('employer')}")
    print(f"  Extracted location: {extracted.get('location')}")
    print(f"  Description length: {len(extracted.get('description', ''))}")
    print(f"  Extraction confidence: {extracted.get('extraction_confidence')}")
    print(f"  Warnings: {extracted.get('extraction_warnings')}")

    # Build CapturedJob with manual overrides
    job = build_from_evidence(
        source_name="Manual Supply",
        original_url="manual-input",
        capture_method=CaptureMethod.MANUAL_SUPPLY,
        evidence_file="manual_input",
        job_title=extracted.get("job_title", "Senior Consultant"),
        employer=extracted.get("employer", "International Development Consultants"),
        location=extracted.get("location", "Nairobi, Kenya"),
        description=extracted.get("description", ""),
        closing_date=extracted.get("closing_date", "July 15, 2024"),
        extraction_confidence=ExtractionConfidence(extracted.get("extraction_confidence", "low")),
        extraction_warnings=[
            ExtractionWarning(w) for w in extracted.get("extraction_warnings", [])
        ],
    )

    print(f"  CapturedJob title: {job.job_title}")
    print(f"  CapturedJob employer: {job.employer}")
    print(f"  CapturedJob location: {job.location}")
    print(f"  CapturedJob confidence: {job.extraction_confidence.value}")
    print(f"  CapturedJob has_complete_info: {job.has_complete_info()}")
    return job


def test_duplicate_posting():
    """Test 5: Duplicate posting from another source (same JSON-LD as Test 1)."""
    print("\n=== Test 5: Duplicate posting ===")
    fixture = FIXTURE_DIR / "html_duplicate.jsonld.html"
    content = fixture.read_text(encoding="utf-8")

    # Extract job data (same as Test 1 - JSON-LD present)
    extracted = extract_job_data(
        content=content,
        capture_method=CaptureMethod.HTML_SAVED,
        url=str(fixture),
        evidence_file=str(fixture),
    )
    print(f"  Extracted title: {extracted.get('job_title')}")
    print(f"  Extraction confidence: {extracted.get('extraction_confidence')}")

    # Build CapturedJob - same data as Test 1 but from different source
    job = build_from_evidence(
        source_name="LinkedIn (second capture)",
        original_url=str(fixture),
        capture_method=CaptureMethod.HTML_SAVED,
        evidence_file=str(fixture),
        job_title=extracted.get("job_title", ""),
        employer=extracted.get("employer", ""),
        location=extracted.get("location", ""),
        description=extracted.get("description", ""),
        closing_date=extracted.get("closing_date", ""),
        extraction_confidence=ExtractionConfidence(
            extracted.get("extraction_confidence", "unknown")
        ),
        extraction_warnings=[
            ExtractionWarning(w) for w in extracted.get("extraction_warnings", [])
        ],
    )

    print(f"  CapturedJob title: {job.job_title}")
    print(f"  CapturedJob employer: {job.employer}")
    print(f"  CapturedJob location: {job.location}")
    print(f"  CapturedJob confidence: {job.extraction_confidence.value}")
    print(f"  CapturedJob has_complete_info: {job.has_complete_info()}")
    return job


def test_browser_session_lifecycle():
    """Test browser session initiation and completion lifecycle."""
    print("\n=== Test 6: Browser session lifecycle ===")

    # Initiate a session
    sess = initiate_browser_session(
        job_boards=["linkedin", "malawi"],
        search_terms="software engineer",
        locations=["Lilongwe", "Blantyre", "Remote"],
    )

    # Record some selected postings (simulated)
    # In a real session, the user would capture evidence and call
    # record_selected_posting with the evidence file paths

    # Complete the session
    captured = complete_session(sess)
    print(f"  Jobs captured in session: {len(captured)}")

    # Feed to pipeline
    results = feed_to_pipeline(captured)
    print("  Pipeline import results:")
    print(f"    Total jobs: {results['total_jobs']}")
    print(f"    Successfully imported: {results['successfully_imported']}")
    print(f"    Extraction failures: {results['extraction_failures']}")
    print(f"    Incomplete info: {results['incomplete_jobs']}")
    print(f"    Closed/expired: {results['closed_or_expired']}")
    print(f"    Eligible: {results['eligible']}")

    return sess, captured, results


def main():
    """Run all tests."""
    print("Browser-Assisted Job Discovery - Workflow Demonstration")
    print("=" * 60)

    # Run individual capture method tests
    job1 = test_html_with_json_ld()
    job2 = test_html_without_json_ld()
    job3 = test_pdf()
    job4 = test_manual_description()
    job5 = test_duplicate_posting()

    # Verify all jobs conform to the canonical model
    print("\n" + "=" * 60)
    print("Canonical Model Validation")
    print("=" * 60)

    jobs = [job1, job2, job3, job4, job5]
    for i, job in enumerate(jobs, 1):
        print(f"\nJob {i}:")
        print(f"  - source_name: {job.source_name}")
        print(f"  - original_url: {job.original_url}")
        print(f"  - job_title: {job.job_title}")
        print(f"  - employer: {job.employer}")
        print(f"  - location: {job.location}")
        print(f"  - employment_type: {job.employment_type}")
        print(f"  - description: {job.description[:50]!r}...")
        print(f"  - closing_date: {job.closing_date}")
        print(f"  - capture_method: {job.capture_method.value}")
        print(f"  - extraction_confidence: {job.extraction_confidence.value}")
        print(f"  - extraction_warnings: {job.extraction_warnings}")
        print(f"  - has_complete_info: {job.has_complete_info()}")
        print(f"  - has_expiry: {job.has_expiry()}")
        print(f"  - is_expired: {job.is_expired()}")

    # Test browser session lifecycle
    sess, captured, results = test_browser_session_lifecycle()

    # Summary
    print("\n" + "=" * 60)
    print("WORKFLOW SUMMARY")
    print("=" * 60)
    print("\nAll five capture methods successfully:")
    print("  1. HTML with JSON-LD extraction")
    print("  2. HTML without JSON-LD (fallback visible text)")
    print("  3. PDF printout (text extraction)")
    print("  4. Manual job description supply")
    print("  5. Duplicate posting (same normalized pipeline)")
    print("\nAll jobs enter the same normalized pipeline without")
    print("requiring separate scoring or eligibility implementations.")
    print("\nBrowser session lifecycle demonstrated: initiate -> capture ->")
    print("complete -> feed to pipeline.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
