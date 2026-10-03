from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from ..models import (
    ApplicationStatus,
    Document,
    Education,
    Experience,
    JobPreferences,
    JobSource,
    JobStatus,
    JobType,
    MatchTier,
    SalaryRange,
    Skill,
)


# Request/Response schemas
class JobCreate(BaseModel):
    source: JobSource
    source_job_id: Optional[str] = None
    title: str
    company: str
    location: str
    job_type: JobType
    description: str
    requirements: List[str] = []
    responsibilities: List[str] = []
    keywords: List[str] = []
    salary_range: Optional[SalaryRange] = None
    posted_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    application_url: HttpUrl
    apply_email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    company_website: Optional[HttpUrl] = None
    company_size: Optional[str] = None
    company_industry: Optional[str] = None
    benefits: List[str] = []


class JobResponse(BaseModel):
    id: UUID
    source: JobSource
    source_job_id: Optional[str]
    title: str
    company: str
    location: str
    job_type: JobType
    description: str
    requirements: List[str]
    responsibilities: List[str]
    keywords: List[str]
    salary_range: Optional[SalaryRange]
    posted_date: Optional[datetime]
    expiry_date: Optional[datetime]
    application_url: HttpUrl
    apply_email: Optional[EmailStr]
    contact_person: Optional[str]
    company_website: Optional[HttpUrl]
    company_size: Optional[str]
    company_industry: Optional[str]
    benefits: List[str]
    ats_score: Optional[float]
    match_score: Optional[float]
    match_tier: Optional[MatchTier]
    status: JobStatus
    scraped_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    limit: int
    offset: int


class JobFilter(BaseModel):
    status: Optional[JobStatus] = None
    source: Optional[JobSource] = None
    job_type: Optional[JobType] = None
    location: Optional[str] = None
    min_ats_score: Optional[float] = None
    max_ats_score: Optional[float] = None
    min_match_score: Optional[float] = None
    max_match_score: Optional[float] = None
    search: Optional[str] = None
    limit: int = 50
    offset: int = 0


class UserProfileCreate(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    headline: str = ""
    summary: str = ""
    skills: List[Skill] = []
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[str] = []
    languages: List[str] = []
    preferences: JobPreferences = Field(default_factory=JobPreferences)


class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[HttpUrl]
    portfolio_url: Optional[HttpUrl]
    github_url: Optional[HttpUrl]
    headline: str
    summary: str
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    certifications: List[str]
    languages: List[str]
    preferences: JobPreferences
    documents: List[Document]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    job_id: UUID
    user_profile_id: UUID
    resume_id: UUID
    cover_letter_id: Optional[UUID] = None


class ApplicationResponse(BaseModel):
    id: UUID
    job_id: UUID
    user_profile_id: UUID
    resume_id: UUID
    cover_letter_id: Optional[UUID]
    tailored_resume_path: Optional[str]
    tailored_cover_letter_path: Optional[str]
    ats_score: float
    match_score: float
    status: ApplicationStatus
    submitted_at: Optional[datetime]
    confirmed_at: Optional[datetime]
    receipt_data: Dict[str, Any]
    follow_up_dates: List[datetime]
    notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    applications: List[ApplicationResponse]
    total: int


class ScrapeJobRequest(BaseModel):
    query: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    max_results: int = 100
    sources: Optional[List[JobSource]] = None
    user_profile_id: Optional[UUID] = None


class ScrapeJobResponse(BaseModel):
    id: UUID
    source: JobSource
    query: str
    location: Optional[str]
    job_type: Optional[JobType]
    max_results: int
    status: str
    jobs_found: int
    jobs_new: int
    jobs_updated: int
    error: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ATSScoreResponse(BaseModel):
    job_id: UUID
    profile_id: UUID
    keyword_match: float
    semantic_similarity: float
    experience_relevance: float
    education_match: float
    overall: float
    details: Dict[str, Any]
    tier: str
    should_auto_apply: bool
    should_flag_for_review: bool


class MatchJobsRequest(BaseModel):
    profile_id: UUID
    job_ids: Optional[List[UUID]] = None
    top_k: Optional[int] = None
    min_score: float = 0


class MatchJobsResponse(BaseModel):
    matches: List[Dict[str, Any]]
    total: int


class PipelineStatsResponse(BaseModel):
    total_jobs: int
    new: int
    fetched: int
    matched: int
    scored: int
    applied: int
    interview: int
    offer: int
    rejected: int
    by_source: Dict[str, int]
    by_type: Dict[str, int]
    avg_ats_score: float
    avg_match_score: float


class ScrapeStatsResponse(BaseModel):
    recent_scrapes: List[ScrapeJobResponse]
    total_jobs_scraped: int
    total_new_jobs: int
    last_scrape_at: Optional[datetime]
