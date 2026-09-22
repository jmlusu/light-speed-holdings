"""Athena - Job & Consultancy Application Platform"""

__version__ = "0.1.0"

from .models import (
    Application,
    ApplicationStatus,
    Document,
    Education,
    Experience,
    Job,
    JobPreferences,
    JobSource,
    JobStatus,
    JobType,
    MatchTier,
    SalaryRange,
    ScrapeJob,
    Skill,
    UserProfile,
)

__all__ = [
    "JobSource",
    "JobType",
    "JobStatus",
    "ApplicationStatus",
    "MatchTier",
    "SalaryRange",
    "Skill",
    "Experience",
    "Education",
    "Document",
    "JobPreferences",
    "Job",
    "Application",
    "UserProfile",
    "ScrapeJob",
]
