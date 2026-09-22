from uuid import uuid4

import pytest

from ai_company.athena.models import Job, JobSource, JobStatus, JobType
from ai_company.athena.store import AthenaDB


@pytest.fixture
def temp_db(tmp_path):
    return AthenaDB(base_dir=tmp_path / "athena")


def test_job_store_crud(temp_db):
    job_id = uuid4()
    job = Job(
        id=job_id,
        source=JobSource.REMOTE_OK,
        title="Python Engineer",
        company="Acme Corp",
        location="Remote",
        job_type=JobType.FULL_TIME,
        description="Write Python code",
        application_url="https://example.com/apply",
        status=JobStatus.NEW,
    )

    # Add
    temp_db.add_job(job)

    # Get
    fetched = temp_db.get_job(job_id)
    assert fetched is not None
    assert fetched.title == "Python Engineer"
    assert fetched.company == "Acme Corp"

    # Update
    fetched.status = JobStatus.FETCHED
    temp_db.update_job(fetched)
    updated = temp_db.get_job(job_id)
    assert updated.status == JobStatus.FETCHED

    # List
    jobs = temp_db.get_jobs()
    assert len(jobs) == 1

    # Delete
    assert temp_db.jobs.delete(job_id)
    assert temp_db.get_job(job_id) is None
