from uuid import uuid4

import pytest

from ai_company.athena.ats.scorer import ATSScorer
from ai_company.athena.models import Job, JobSource, JobStatus, JobType, Skill, UserProfile


@pytest.fixture
def sample_profile():
    return UserProfile(
        id=uuid4(),
        email="test@example.com",
        full_name="Test User",
        headline="Python Engineer",
        summary="Experienced Python developer",
        skills=[Skill(name="Python"), Skill(name="SQL")],
    )


@pytest.fixture
def sample_job():
    return Job(
        id=uuid4(),
        source=JobSource.REMOTE_OK,
        title="Python Developer",
        company="TechCo",
        location="Remote",
        job_type=JobType.FULL_TIME,
        description="Looking for Python and SQL skills.",
        requirements=["Python", "SQL"],
        keywords=["Python", "SQL"],
        application_url="https://example.com/apply",
        status=JobStatus.NEW,
    )


def test_ats_scorer(sample_profile, sample_job):
    scorer = ATSScorer()
    breakdown = scorer.score_resume_against_job(sample_profile, sample_job)
    assert breakdown.overall >= 0.0
    assert breakdown.overall <= 100.0
    assert 0.0 <= breakdown.keyword_match <= 100.0
    assert 0.0 <= breakdown.semantic_similarity <= 100.0

    tier = scorer.get_score_tier(breakdown.overall)
    assert tier in ["excellent", "good", "fair", "poor"]

    should_apply = scorer.should_auto_apply(breakdown.overall)
    assert isinstance(should_apply, bool)
