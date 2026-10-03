from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from ..ats import ats_scorer
from ..matching import matching_engine
from ..models import (
    Application,
    ApplicationStatus,
    Job,
    JobSource,
    JobStatus,
    JobType,
    UserProfile,
)
from ..scheduler import ScrapeConfig, athena_scheduler
from ..store import athena_db
from .schemas import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
    ATSScoreResponse,
    JobCreate,
    JobListResponse,
    JobResponse,
    MatchJobsRequest,
    MatchJobsResponse,
    PipelineStatsResponse,
    ScrapeJobRequest,
    ScrapeJobResponse,
    ScrapeStatsResponse,
    UserProfileCreate,
    UserProfileResponse,
)

router = APIRouter(prefix="/athena", tags=["athena"])


# Job endpoints
@router.post("/jobs", response_model=JobResponse)
async def create_job(job: JobCreate):
    """Create a new job entry."""
    job_obj = Job(**job.model_dump())
    return athena_db.add_job(job_obj)


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    status: Optional[JobStatus] = None,
    source: Optional[JobSource] = None,
    job_type: Optional[JobType] = None,
    location: Optional[str] = None,
    min_ats_score: Optional[float] = None,
    max_ats_score: Optional[float] = None,
    min_match_score: Optional[float] = None,
    max_match_score: Optional[float] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
):
    """List jobs with filters."""
    jobs = athena_db.jobs.get_all()

    if status:
        jobs = [j for j in jobs if j.status == status]
    if source:
        jobs = [j for j in jobs if j.source == source]
    if job_type:
        jobs = [j for j in jobs if j.job_type == job_type]
    if location:
        jobs = [j for j in jobs if location.lower() in j.location.lower()]
    if min_ats_score is not None:
        jobs = [j for j in jobs if j.ats_score and j.ats_score >= min_ats_score]
    if max_ats_score is not None:
        jobs = [j for j in jobs if j.ats_score and j.ats_score <= max_ats_score]
    if min_match_score is not None:
        jobs = [j for j in jobs if j.match_score and j.match_score >= min_match_score]
    if max_match_score is not None:
        jobs = [j for j in jobs if j.match_score and j.match_score <= max_match_score]
    if search:
        search_lower = search.lower()
        jobs = [
            j
            for j in jobs
            if search_lower in j.title.lower()
            or search_lower in j.company.lower()
            or search_lower in j.description.lower()
        ]

    total = len(jobs)
    jobs.sort(key=lambda j: j.scraped_at, reverse=True)
    jobs = jobs[offset : offset + limit]

    return JobListResponse(
        jobs=[JobResponse.model_validate(j) for j in jobs],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID):
    """Get a single job by ID."""
    job = athena_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(job)


@router.patch("/jobs/{job_id}", response_model=JobResponse)
async def update_job(job_id: UUID, updates: Dict[str, Any]):
    """Update a job."""
    job = athena_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in updates.items():
        if hasattr(job, key):
            setattr(job, key, value)

    return athena_db.update_job(job)


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: UUID):
    """Delete a job."""
    if not athena_db.jobs.delete(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return {"success": True}


# User Profile endpoints
@router.post("/profiles", response_model=UserProfileResponse)
async def create_profile(profile: UserProfileCreate):
    """Create a new user profile."""
    profile_obj = UserProfile(**profile.model_dump())
    return athena_db.add_user_profile(profile_obj)


@router.get("/profiles", response_model=List[UserProfileResponse])
async def list_profiles():
    """List all user profiles."""
    profiles = athena_db.user_profiles.get_all()
    return [UserProfileResponse.model_validate(p) for p in profiles]


@router.get("/profiles/{profile_id}", response_model=UserProfileResponse)
async def get_profile(profile_id: UUID):
    """Get a user profile by ID."""
    profile = athena_db.get_user_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfileResponse.model_validate(profile)


@router.get("/profiles/email/{email}", response_model=UserProfileResponse)
async def get_profile_by_email(email: str):
    """Get a user profile by email."""
    profile = athena_db.get_user_profile_by_email(email)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfileResponse.model_validate(profile)


@router.patch("/profiles/{profile_id}", response_model=UserProfileResponse)
async def update_profile(profile_id: UUID, updates: Dict[str, Any]):
    """Update a user profile."""
    profile = athena_db.get_user_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in updates.items():
        if hasattr(profile, key):
            setattr(profile, key, value)

    return athena_db.update_user_profile(profile)


# Application endpoints
@router.post("/applications", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate):
    """Create a new application."""
    app = Application(**application.model_dump())
    return athena_db.add_application(app)


@router.get("/applications", response_model=ApplicationListResponse)
async def list_applications(
    user_profile_id: Optional[UUID] = None,
    job_id: Optional[UUID] = None,
    status: Optional[ApplicationStatus] = None,
):
    """List applications with filters."""
    apps = athena_db.get_applications(user_profile_id, job_id, status)
    return ApplicationListResponse(
        applications=[ApplicationResponse.model_validate(a) for a in apps],
        total=len(apps),
    )


@router.get("/applications/{app_id}", response_model=ApplicationResponse)
async def get_application(app_id: UUID):
    """Get an application by ID."""
    app = athena_db.get_application(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return ApplicationResponse.model_validate(app)


@router.patch("/applications/{app_id}", response_model=ApplicationResponse)
async def update_application(app_id: UUID, updates: Dict[str, Any]):
    """Update an application."""
    app = athena_db.get_application(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    for key, value in updates.items():
        if hasattr(app, key):
            setattr(app, key, value)

    return athena_db.update_application(app)


# Scraping endpoints
@router.post("/scrape", response_model=ScrapeJobResponse)
async def trigger_scrape(request: ScrapeJobRequest, background_tasks: BackgroundTasks):
    """Trigger a scrape job."""
    config = ScrapeConfig(
        query=request.query,
        location=request.location,
        job_type=request.job_type,
        max_results=request.max_results,
        sources=request.sources,
        user_profile_id=request.user_profile_id,
    )
    scrape_job = await athena_scheduler.run_scrape_config(config)
    return ScrapeJobResponse.model_validate(scrape_job)


@router.get("/scrape/history", response_model=List[ScrapeJobResponse])
async def get_scrape_history(limit: int = 50):
    """Get recent scrape job history."""
    jobs = athena_db.get_recent_scrape_jobs(limit)
    return [ScrapeJobResponse.model_validate(j) for j in jobs]


# Matching & Scoring endpoints
@router.post("/match", response_model=MatchJobsResponse)
async def match_jobs(request: MatchJobsRequest):
    """Match jobs against a user profile."""
    profile = athena_db.get_user_profile(request.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    jobs: List[Job] = []
    if request.job_ids:
        jobs = [j for j in (athena_db.get_job(jid) for jid in request.job_ids) if j is not None]
    else:
        jobs = athena_db.jobs.get_all()

    scored = matching_engine.rank_jobs(profile, jobs, request.top_k)

    if request.min_score > 0:
        scored = [(j, s) for j, s in scored if s >= request.min_score]

    matches = [
        {
            "job": JobResponse.model_validate(job),
            "match_score": score,
            "match_tier": job.match_tier.value if job.match_tier else None,
        }
        for job, score in scored
    ]

    return MatchJobsResponse(matches=matches, total=len(matches))


@router.get("/score/{job_id}/{profile_id}", response_model=ATSScoreResponse)
async def get_ats_score(job_id: UUID, profile_id: UUID):
    """Get ATS score for a job-profile pair."""
    job = athena_db.get_job(job_id)
    profile = athena_db.get_user_profile(profile_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    breakdown = ats_scorer.score_resume_against_job(profile, job)

    return ATSScoreResponse(
        job_id=job_id,
        profile_id=profile_id,
        keyword_match=breakdown.keyword_match,
        semantic_similarity=breakdown.semantic_similarity,
        experience_relevance=breakdown.experience_relevance,
        education_match=breakdown.education_match,
        overall=breakdown.overall,
        details=breakdown.details,
        tier=ats_scorer.get_score_tier(breakdown.overall),
        should_auto_apply=ats_scorer.should_auto_apply(breakdown.overall),
        should_flag_for_review=ats_scorer.should_flag_for_review(breakdown.overall),
    )


# Statistics endpoints
@router.get("/stats/pipeline", response_model=PipelineStatsResponse)
async def get_pipeline_stats():
    """Get job pipeline statistics."""
    jobs = athena_db.jobs.get_all()

    by_status = {}
    for status in JobStatus:
        by_status[status.value] = len([j for j in jobs if j.status == status])

    by_source = {}
    for source in JobSource:
        count = len([j for j in jobs if j.source == source])
        if count > 0:
            by_source[source.value] = count

    by_type = {}
    for jtype in JobType:
        count = len([j for j in jobs if j.job_type == jtype])
        if count > 0:
            by_type[jtype.value] = count

    ats_scores = [j.ats_score for j in jobs if j.ats_score is not None]
    match_scores = [j.match_score for j in jobs if j.match_score is not None]

    return PipelineStatsResponse(
        total_jobs=len(jobs),
        new=by_status.get(JobStatus.NEW.value, 0),
        fetched=by_status.get(JobStatus.FETCHED.value, 0),
        matched=by_status.get(JobStatus.MATCHED.value, 0),
        scored=by_status.get(JobStatus.SCORED.value, 0),
        applied=by_status.get(JobStatus.APPLIED.value, 0),
        interview=by_status.get(JobStatus.INTERVIEW.value, 0),
        offer=by_status.get(JobStatus.OFFER.value, 0),
        rejected=by_status.get(JobStatus.REJECTED.value, 0),
        by_source=by_source,
        by_type=by_type,
        avg_ats_score=sum(ats_scores) / len(ats_scores) if ats_scores else 0,
        avg_match_score=sum(match_scores) / len(match_scores) if match_scores else 0,
    )


@router.get("/stats/scraping", response_model=ScrapeStatsResponse)
async def get_scraping_stats():
    """Get scraping statistics."""
    scrape_jobs = athena_db.get_recent_scrape_jobs(20)
    total_scraped = sum(j.jobs_found for j in scrape_jobs)
    total_new = sum(j.jobs_new for j in scrape_jobs)
    last_scrape = scrape_jobs[0].completed_at if scrape_jobs else None

    return ScrapeStatsResponse(
        recent_scrapes=[ScrapeJobResponse.model_validate(j) for j in scrape_jobs],
        total_jobs_scraped=total_scraped,
        total_new_jobs=total_new,
        last_scrape_at=last_scrape,
    )


# Scheduler control
@router.post("/scheduler/start")
async def start_scheduler():
    """Start the Athena scheduler."""
    if not athena_scheduler._running:
        athena_scheduler.start()
    return {"status": "started", "running": athena_scheduler._running}


@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the Athena scheduler."""
    if athena_scheduler._running:
        athena_scheduler.stop()
    return {"status": "stopped", "running": athena_scheduler._running}


@router.get("/scheduler/status")
async def get_scheduler_status():
    """Get scheduler status."""
    jobs = []
    for job in athena_scheduler.scheduler.get_jobs():
        jobs.append(
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            }
        )
    return {"running": athena_scheduler._running, "jobs": jobs}
