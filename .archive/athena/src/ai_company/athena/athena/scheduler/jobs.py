import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ai_company.models.task import Task, TaskPriority, TaskStatus
from ai_company.orchestrator.message_bus import MessageBus

from ..ats import ATSScoreBreakdown, ats_scorer
from ..matching import matching_engine
from ..models import Job, JobSource, JobStatus, JobType, ScrapeJob, UserProfile
from ..scrapers import scraper_registry
from ..store import athena_db

logger = logging.getLogger(__name__)


@dataclass
class ScrapeConfig:
    """Configuration for a scrape job."""

    query: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    max_results: int = 100
    sources: Optional[List[JobSource]] = None
    user_profile_id: Optional[UUID] = None  # For matching/scoring


class AthenaScheduler:
    """Scheduler for Athena scraping and processing jobs."""

    def __init__(self, message_bus: Optional[MessageBus] = None):
        self.scheduler = AsyncIOScheduler()
        self.message_bus = message_bus
        self._running = False
        self.default_configs: List[ScrapeConfig] = []

    def add_default_config(self, config: ScrapeConfig) -> None:
        """Add a default scrape configuration."""
        self.default_configs.append(config)

    def start(self) -> None:
        """Start the scheduler."""
        if self._running:
            return

        # Schedule scrape jobs every 4 hours
        self.scheduler.add_job(
            self.run_all_scrapes,
            trigger=IntervalTrigger(hours=4),
            id="athena_scrape_jobs",
            name="Athena: Scrape all job sources",
            replace_existing=True,
        )

        # Schedule matching/scoring every 30 minutes
        self.scheduler.add_job(
            self.process_new_jobs,
            trigger=IntervalTrigger(minutes=30),
            id="athena_process_jobs",
            name="Athena: Process and score new jobs",
            replace_existing=True,
        )

        # Schedule cleanup daily
        self.scheduler.add_job(
            self.cleanup_old_jobs,
            trigger=IntervalTrigger(days=1),
            id="athena_cleanup",
            name="Athena: Cleanup old jobs",
            replace_existing=True,
        )

        self.scheduler.start()
        self._running = True
        logger.info("Athena scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        if not self._running:
            return
        self.scheduler.shutdown()
        self._running = False
        logger.info("Athena scheduler stopped")

    async def run_all_scrapes(self) -> None:
        """Run scrape jobs for all default configurations."""
        logger.info("Starting scheduled scrape run")
        for config in self.default_configs:
            try:
                await self.run_scrape_config(config)
            except Exception as e:  # noqa: BLE001
                logger.error(f"Scrape config failed: {config.query} - {e}")

    async def run_scrape_config(self, config: ScrapeConfig) -> ScrapeJob:
        """Run a single scrape configuration."""
        scrape_job = ScrapeJob(
            source=config.sources[0] if config.sources else JobSource.LINKEDIN,
            query=config.query,
            location=config.location,
            job_type=config.job_type,
            max_results=config.max_results,
            status="running",
            started_at=datetime.utcnow(),
        )
        athena_db.add_scrape_job(scrape_job)

        try:
            sources = config.sources or None
            jobs = await scraper_registry.search_all(
                query=config.query,
                location=config.location,
                job_type=config.job_type,
                max_results=config.max_results,
                sources=sources,
            )

            # Save jobs and count new/updated
            new_count = 0
            updated_count = 0
            for job in jobs:
                existing = None
                for j in athena_db.jobs.get_all():
                    if j.source_job_id and j.source_job_id == job.source_job_id:
                        existing = j
                        break

                if existing:
                    job.id = existing.id
                    job.scraped_at = existing.scraped_at
                    athena_db.update_job(job)
                    updated_count += 1
                else:
                    athena_db.add_job(job)
                    new_count += 1

            scrape_job.jobs_found = len(jobs)
            scrape_job.jobs_new = new_count
            scrape_job.jobs_updated = updated_count
            scrape_job.status = "completed"
            scrape_job.completed_at = datetime.utcnow()

            logger.info(
                f"Scrape completed: {config.query} - {len(jobs)} jobs ({new_count} new, {updated_count} updated)"
            )

        except Exception as e:  # noqa: BLE001
            scrape_job.status = "failed"
            scrape_job.error = str(e)
            scrape_job.completed_at = datetime.utcnow()
            logger.error(f"Scrape failed: {config.query} - {e}")

        athena_db.update_scrape_job(scrape_job)

        # Trigger processing of new jobs
        if scrape_job.jobs_new > 0:
            await self.process_new_jobs()

        return scrape_job

    async def process_new_jobs(self) -> None:
        """Process new jobs: match, score, and queue for applications."""
        logger.info("Processing new jobs for matching and scoring")

        # Get unscored jobs
        new_jobs = athena_db.jobs.filter(status=JobStatus.NEW)
        fetched_jobs = athena_db.jobs.filter(status=JobStatus.FETCHED)
        all_new = new_jobs + fetched_jobs

        if not all_new:
            logger.info("No new jobs to process")
            return

        # Get active user profiles
        profiles = athena_db.user_profiles.get_all()
        if not profiles:
            logger.warning("No user profiles found for matching")
            # Just mark as fetched
            for job in all_new:
                job.status = JobStatus.FETCHED
                athena_db.update_job(job)
            return

        for job in all_new:
            try:
                # For each profile, compute match and ATS score
                best_match = None
                best_score = 0.0

                for profile in profiles:
                    match_score = matching_engine.compute_match_score(profile, job)
                    if match_score > best_score:
                        best_score = match_score
                        best_match = profile

                if best_match:
                    job.match_score = best_score
                    job.match_tier = matching_engine._get_match_tier(best_score)

                    # Compute ATS score
                    ats_breakdown = ats_scorer.score_resume_against_job(best_match, job)
                    job.ats_score = ats_breakdown.overall

                    # Update job status
                    if ats_breakdown.overall >= 90:
                        job.status = JobStatus.SCORED
                        # Queue for auto-application if enabled
                        if self.message_bus and ats_scorer.should_auto_apply(ats_breakdown.overall):
                            await self._queue_application(job, best_match, ats_breakdown)
                    elif ats_breakdown.overall >= 80:
                        job.status = JobStatus.SCORED
                        # Flag for review
                        if self.message_bus:
                            await self._queue_review(job, best_match, ats_breakdown)
                    else:
                        job.status = JobStatus.FETCHED

                    athena_db.update_job(job)
                    logger.info(
                        f"Job {job.title} scored: ATS={ats_breakdown.overall}, Match={best_score}"
                    )

            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to process job {job.id}: {e}")
                job.status = JobStatus.FETCHED
                athena_db.update_job(job)

    async def _queue_application(
        self,
        job: Job,
        profile: UserProfile,
        ats_breakdown: ATSScoreBreakdown,
    ) -> None:
        """Queue an application task via MessageBus."""
        bus = self.message_bus
        if bus is None:
            logger.warning("No message bus available; skipping auto-apply queue for job %s", job.id)
            return

        task = Task(
            id=f"athena-apply-{job.id}",
            name="athena.apply",
            sender_id="athena-scheduler",
            receiver_id="dashboard",
            instruction=(
                f"Auto-apply for job {job.id} on behalf of profile {profile.id} — "
                f"ATS score {ats_breakdown.overall} meets the auto-apply threshold."
            ),
            description=json.dumps(
                {
                    "job_id": str(job.id),
                    "profile_id": str(profile.id),
                    "ats_score": ats_breakdown.overall,
                    "auto_apply": True,
                }
            ),
            tags=["athena", "apply"],
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
        )
        bus.send_task(task)
        logger.info("Queued auto-application for job %s", job.id)

    async def _queue_review(
        self,
        job: Job,
        profile: UserProfile,
        ats_breakdown: ATSScoreBreakdown,
    ) -> None:
        """Queue a review task via MessageBus."""
        bus = self.message_bus
        if bus is None:
            logger.warning("No message bus available; skipping review queue for job %s", job.id)
            return

        task = Task(
            id=f"athena-review-{job.id}",
            name="athena.review",
            sender_id="athena-scheduler",
            receiver_id="dashboard",
            instruction=(
                f"Review job {job.id} for profile {profile.id} — "
                f"ATS score {ats_breakdown.overall} is in the 80-89 human-review band."
            ),
            description=json.dumps(
                {
                    "job_id": str(job.id),
                    "profile_id": str(profile.id),
                    "ats_score": ats_breakdown.overall,
                    "flag_reason": "ATS score 80-89 requires human review",
                }
            ),
            tags=["athena", "review"],
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
        )
        bus.send_task(task)
        logger.info("Queued review for job %s", job.id)

    async def cleanup_old_jobs(self, days: int = 90) -> None:
        """Clean up old jobs beyond retention period."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        all_jobs = athena_db.jobs.get_all()
        deleted = 0
        for job in all_jobs:
            if job.scraped_at < cutoff and job.status in [JobStatus.ARCHIVED, JobStatus.REJECTED]:
                athena_db.jobs.delete(job.id)
                deleted += 1

        logger.info(f"Cleaned up {deleted} old jobs")


# Global scheduler instance
athena_scheduler = AthenaScheduler()


def init_scheduler(message_bus: MessageBus) -> AthenaScheduler:
    """Initialize the scheduler with message bus."""
    global athena_scheduler
    athena_scheduler = AthenaScheduler(message_bus)

    # Add default scrape configurations
    athena_scheduler.add_default_config(
        ScrapeConfig(
            query="software engineer",
            location="Lilongwe, Malawi",
            max_results=50,
        )
    )
    athena_scheduler.add_default_config(
        ScrapeConfig(
            query="data scientist",
            location="Lilongwe, Malawi",
            max_results=50,
        )
    )
    athena_scheduler.add_default_config(
        ScrapeConfig(
            query="remote software engineer",
            location="Remote",
            max_results=100,
        )
    )
    athena_scheduler.add_default_config(
        ScrapeConfig(
            query="freelance developer",
            location="Remote",
            max_results=50,
            sources=[JobSource.UPWORK, JobSource.TOPTAL],
        )
    )

    athena_scheduler.start()
    return athena_scheduler
