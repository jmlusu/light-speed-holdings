from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from .enums import ApplicationStatus, JobSource, JobStatus, JobType, MatchTier


class SalaryRange(BaseModel):
    min: Optional[Decimal] = None
    max: Optional[Decimal] = None
    currency: str = "USD"
    period: str = "yearly"  # yearly, monthly, hourly


class Skill(BaseModel):
    name: str
    level: Optional[str] = None  # beginner, intermediate, advanced, expert
    years_experience: Optional[float] = None
    category: Optional[str] = None  # technical, soft, language, etc.


class Experience(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    company: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    current: bool = False
    description: str
    achievements: List[str] = []
    skills_used: List[str] = []


class Education(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    institution: str
    degree: str
    field_of_study: str
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None
    honors: List[str] = []


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    type: str  # resume, cover_letter, certification, portfolio, other
    file_path: str
    mime_type: str
    size_bytes: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    parsed_content: Optional[Dict[str, Any]] = None


class JobPreferences(BaseModel):
    keywords: List[str] = []
    excluded_keywords: List[str] = []
    locations: List[str] = []  # e.g., ["Lilongwe, Malawi", "Remote"]
    job_types: List[JobType] = []
    min_salary: Optional[Decimal] = None
    preferred_sources: List[JobSource] = []
    remote_only: bool = False
    visa_sponsorship_required: bool = False


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source: JobSource
    source_job_id: Optional[str] = None  # Original ID from source
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
    ats_score: Optional[float] = None
    match_score: Optional[float] = None
    match_tier: Optional[MatchTier] = None
    status: JobStatus = JobStatus.NEW
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}  # Source-specific extra data


class Application(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job_id: UUID
    user_profile_id: UUID
    resume_id: UUID
    cover_letter_id: Optional[UUID] = None
    tailored_resume_path: Optional[str] = None
    tailored_cover_letter_path: Optional[str] = None
    ats_score: float
    match_score: float
    status: ApplicationStatus = ApplicationStatus.PENDING
    submitted_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    receipt_data: Dict[str, Any] = {}  # Confirmation number, reference ID, etc.
    follow_up_dates: List[datetime] = []
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
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
    documents: List[Document] = []
    resume_base: Optional[Dict[str, Any]] = None  # Parsed structured resume
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ScrapeJob(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source: JobSource
    query: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    max_results: int = 100
    status: str = "pending"  # pending, running, completed, failed
    jobs_found: int = 0
    jobs_new: int = 0
    jobs_updated: int = 0
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
