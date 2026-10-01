from uuid import uuid4

import pytest

from ai_company.athena.matching.engine import MatchingEngine
from ai_company.athena.models import Job, JobSource, JobStatus, JobType, Skill, UserProfile


@pytest.fixture
def sample_profile():
    return UserProfile(
        id=uuid4(),
        email="test@example.com",
        full_name="Test User",
        headline="Senior Python Engineer",
        summary="Experienced Python and FastAPI developer",
        skills=[Skill(name="Python"), Skill(name="FastAPI"), Skill(name="Docker")],
    )


@pytest.fixture
def sample_job():
    return Job(
        id=uuid4(),
        source=JobSource.REMOTE_OK,
        title="Backend Python Developer",
        company="TechCo",
        location="Remote",
        job_type=JobType.FULL_TIME,
        description="Looking for Python and FastAPI expert with Docker experience.",
        requirements=["Python", "FastAPI"],
        keywords=["Python", "FastAPI", "Docker"],
        application_url="https://example.com/apply",
        status=JobStatus.NEW,
    )


def test_matching_engine_fallback(sample_profile, sample_job):
    engine = MatchingEngine()
    # Force fallback by marking model unavailable or testing keyword match directly
    score = engine._keyword_match_score(sample_profile, sample_job)
    assert score > 0.0
    assert score <= 100.0


def test_compute_match_score(sample_profile, sample_job):
    engine = MatchingEngine()
    score = engine.compute_match_score(sample_profile, sample_job)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0
