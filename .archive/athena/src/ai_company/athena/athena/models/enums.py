from enum import Enum


class JobSource(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    COMPANY_CAREER = "company_career"
    MALAWI_JOBS = "malawi_jobs"
    MALAWI_WORK = "malawi_work"
    JOBS_MALAWI = "jobs_malawi"
    UPWORK = "upwork"
    TOPTAL = "toptal"
    FREELANCER = "freelancer"
    GURU = "guru"
    PEOPLE_PER_HOUR = "people_per_hour"
    REMOTE_OK = "remote_ok"
    WE_WORK_REMOTELY = "we_work_remotely"
    REMOTE_CO = "remote_co"
    OTHER = "other"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    CONSULTANCY = "consultancy"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class JobStatus(str, Enum):
    NEW = "new"
    FETCHED = "fetched"
    MATCHED = "matched"
    SCORED = "scored"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    WITHDRAWN = "withdrawn"


class MatchTier(str, Enum):
    EXCELLENT = "excellent"  # >= 90
    GOOD = "good"  # 80-89
    FAIR = "fair"  # 70-79
    POOR = "poor"  # < 70
