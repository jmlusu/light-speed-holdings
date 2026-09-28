"""Test scraper subsystem inventory.

All reads are anchored to the repository root; nothing is ever created,
skipped, or xfailed - a missing data file fails the test.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ATHENA_DIR = REPO_ROOT / "company" / "athena"

# Scraper script directories we expect (checked against the real filesystem)
SCRAPER_DIRS = [
    ".agents/skills/junta-leiloeiro/scripts/scraper/",
    "company/junta-leiloeiro/",
]


def _read_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file into a list of dicts (one per non-empty line).

    Raises FileNotFoundError when the file is missing - tests fail, never skip.
    """
    records: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            assert isinstance(record, dict), f"{path.name}: record is not a JSON object"
            records.append(record)
    return records


def inventory_scrapers() -> list[dict]:
    """Inventory all scraper subsystems and their data formats (read-only)."""
    sources: list[dict] = []

    # Read scrape_jobs.jsonl
    for record in _read_jsonl(ATHENA_DIR / "scrape_jobs.jsonl"):
        sources.append(
            {
                "source": record.get("source"),
                "query": record.get("query"),
                "location": record.get("location"),
                "job_type": record.get("job_type"),
                "max_results": record.get("max_results"),
                "status": record.get("status"),
                "jobs_found": record.get("jobs_found"),
                "jobs_new": record.get("jobs_new"),
                "jobs_updated": record.get("jobs_updated"),
            }
        )

    # Read jobs.jsonl
    for record in _read_jsonl(ATHENA_DIR / "jobs.jsonl"):
        sources.append(
            {
                "source": record.get("source"),
                "source_job_id": record.get("source_job_id"),
                "title": record.get("title"),
                "company": record.get("company"),
                "location": record.get("location"),
                "job_type": record.get("job_type"),
                "status": record.get("status"),
                "scraped_at": record.get("scraped_at"),
            }
        )

    # Read user_profiles.jsonl
    for record in _read_jsonl(ATHENA_DIR / "user_profiles.jsonl"):
        sources.append(
            {
                "source": "user_profiles",
                "email": record.get("email"),
                "full_name": record.get("full_name"),
                "location": record.get("location"),
                "headline": record.get("headline"),
                "skills": record.get("skills"),
                "experience": record.get("experience"),
            }
        )

    # List any scraper scripts (existing directories only - never created)
    scraper_dirs = []
    for rel in SCRAPER_DIRS:
        path = REPO_ROOT / rel
        if path.exists():
            scraper_dirs.append(rel)
            scripts = sorted(p.name for p in path.iterdir()) if path.is_dir() else []
            sources.append(
                {
                    "source": f"scraper_scripts:{rel}",
                    "scripts": scripts,
                }
            )

    if not scraper_dirs:
        sources.append(
            {
                "source": "scraper_scripts:not_found",
                "note": "No scraper script directories found at expected paths",
            }
        )

    return sources


def test_scrape_jobs_jsonl_is_valid() -> None:
    """scrape_jobs.jsonl parses and carries the scraper job-control fields."""
    records = _read_jsonl(ATHENA_DIR / "scrape_jobs.jsonl")
    assert records, "scrape_jobs.jsonl has no records"
    for record in records:
        for key in ("source", "query", "status"):
            assert key in record, f"scrape_jobs record missing '{key}'"


def test_jobs_jsonl_is_valid() -> None:
    """jobs.jsonl parses and carries the scraped-job fields."""
    records = _read_jsonl(ATHENA_DIR / "jobs.jsonl")
    assert records, "jobs.jsonl has no records"
    for record in records:
        for key in ("source", "source_job_id", "title", "status", "scraped_at"):
            assert key in record, f"jobs record missing '{key}'"


def test_user_profiles_jsonl_is_valid() -> None:
    """user_profiles.jsonl parses and carries identity fields."""
    records = _read_jsonl(ATHENA_DIR / "user_profiles.jsonl")
    assert records, "user_profiles.jsonl has no records"
    for record in records:
        for key in ("email", "full_name"):
            assert key in record, f"user_profiles record missing '{key}'"


def test_inventory_covers_all_jsonl_datasets() -> None:
    """inventory_scrapers() ingests all three JSONL datasets and labels every entry."""
    sources = inventory_scrapers()
    assert sources, "inventory returned no entries"
    assert any("query" in entry and "max_results" in entry for entry in sources), (
        "scrape_jobs dataset not inventoried"
    )
    assert any("source_job_id" in entry for entry in sources), "jobs dataset not inventoried"
    assert any(entry.get("source") == "user_profiles" for entry in sources), (
        "user_profiles dataset not inventoried"
    )
    for entry in sources:
        source = entry.get("source")
        assert isinstance(source, str) and source, "inventory entry missing 'source'"


def test_scraper_script_dirs_reporting_matches_filesystem() -> None:
    """Script-dir reporting mirrors the filesystem and never creates data."""
    before = {rel: (REPO_ROOT / rel).exists() for rel in SCRAPER_DIRS}
    sources = inventory_scrapers()
    after = {rel: (REPO_ROOT / rel).exists() for rel in SCRAPER_DIRS}
    assert before == after, "inventory_scrapers() must not create directories or files"

    prefix = "scraper_scripts:"
    reported = {
        entry["source"][len(prefix) :]
        for entry in sources
        if isinstance(entry.get("source"), str)
        and entry["source"].startswith(prefix)
        and entry["source"] != "scraper_scripts:not_found"
    }
    actual = {rel for rel, exists in after.items() if exists}
    assert reported == actual, f"reported {reported} vs actual {actual}"

    not_found = [e for e in sources if e.get("source") == "scraper_scripts:not_found"]
    if actual:
        assert not not_found, "not_found sentinel present despite existing scraper dirs"
    else:
        assert not_found, "expected not_found sentinel when no scraper dirs exist"
