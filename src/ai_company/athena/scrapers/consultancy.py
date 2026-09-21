import re
from typing import List, Optional
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup

from ..models import Job, JobSource, JobType
from .base import BaseScraper


class UpworkScraper(BaseScraper):
    """Scraper for Upwork freelance jobs."""

    def __init__(self):
        super().__init__(
            source=JobSource.UPWORK,
            base_url="https://www.upwork.com",
            rate_limit=3.0,
            use_browser=True,
        )

    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        jobs = []
        search_query = quote_plus(query)
        url = f"{self.base_url}/nx/search/jobs/?q={search_query}&sort=recency"

        try:
            html = await self.fetch_with_browser(url, wait_for=".job-tile")
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-tile, [data-test='job-tile']")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Upwork: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h2 a, .job-title a, [data-test='job-title']")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = title_elem.get("href", "")
            if job_url and not job_url.startswith("http"):
                job_url = urljoin(self.base_url, job_url)

            company_elem = element.select_one(".client-name, .client-info")
            company = company_elem.get_text(strip=True) if company_elem else "Upwork Client"

            budget_elem = element.select_one(".budget, [data-test='budget']")
            budget = budget_elem.get_text(strip=True) if budget_elem else ""

            job_type_elem = element.select_one(".job-type, [data-test='job-type']")
            job_type_text = job_type_elem.get_text(strip=True).lower() if job_type_elem else ""

            job_type_enum = JobType.CONSULTANCY
            if "fixed" in job_type_text:
                job_type_enum = JobType.CONTRACT
            elif "hourly" in job_type_text:
                job_type_enum = JobType.FREELANCE

            skills_elem = element.select(".skill-tag, .air3-tag")
            keywords = [skill.get_text(strip=True) for skill in skills_elem]

            description = budget

            return self._create_job(
                title=title,
                company=company,
                location="Remote (Upwork)",
                job_type=job_type_enum,
                description=description,
                application_url=job_url,
                source_job_id=job_url,
                keywords=keywords,
                metadata={"budget": budget, "platform": "upwork"},
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Upwork listing: {e}")
            return None

    async def get_job_details(self, job: Job) -> Job:
        if not job.application_url:
            return job
        try:
            html = await self.fetch_with_browser(
                str(job.application_url), wait_for=".job-description"
            )
            soup = BeautifulSoup(html, "html.parser")
            desc_elem = soup.select_one(".job-description, [data-test='job-description']")
            if desc_elem:
                job.description = desc_elem.get_text(strip=True)
                job.requirements = self._extract_requirements(job.description)

            # Get client info
            client_elem = soup.select_one(".client-info, .about-client")
            if client_elem:
                job.metadata["client_info"] = client_elem.get_text(strip=True)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to get Upwork job details: {e}")
        return job

    def _extract_requirements(self, description: str) -> List[str]:
        req_patterns = [
            r"(?:requirements?|qualifications?|skills?):\s*(.*?)(?:\n\n|\n[A-Z]|$)",
            r"(?:must have|required|experience with):\s*(.*?)(?:\n|$)",
        ]
        requirements = []
        for pattern in req_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE | re.DOTALL)
            for match in matches:
                items = re.split(r"[;\nâ€¢\-]", match)
                requirements.extend([item.strip() for item in items if item.strip()])
        return requirements[:20]


class ToptalScraper(BaseScraper):
    """Scraper for Toptal freelance jobs."""

    def __init__(self):
        super().__init__(
            source=JobSource.TOPTAL,
            base_url="https://www.toptal.com",
            rate_limit=3.0,
            use_browser=True,
        )

    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        jobs = []
        search_query = quote_plus(query)
        url = f"{self.base_url}/freelance-jobs?skill={search_query}"

        try:
            html = await self.fetch_with_browser(url, wait_for=".job-card")
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-card, .project-card")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Toptal: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h3 a, .job-title a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            company_elem = element.select_one(".client-name, .company")
            company = company_elem.get_text(strip=True) if company_elem else "Toptal Client"

            duration_elem = element.select_one(".duration, .project-length")
            duration = duration_elem.get_text(strip=True) if duration_elem else ""

            skills_elem = element.select(".skill, .tag")
            keywords = [skill.get_text(strip=True) for skill in skills_elem]

            return self._create_job(
                title=title,
                company=company,
                location="Remote (Toptal)",
                job_type=JobType.CONSULTANCY,
                description=duration,
                application_url=job_url,
                source_job_id=job_url,
                keywords=keywords,
                metadata={"duration": duration, "platform": "toptal"},
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Toptal listing: {e}")
            return None


class FreelancerScraper(BaseScraper):
    """Scraper for Freelancer.com."""

    def __init__(self):
        super().__init__(
            source=JobSource.FREELANCER,
            base_url="https://www.freelancer.com",
            rate_limit=3.0,
            use_browser=True,
        )

    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        jobs = []
        search_query = quote_plus(query)
        url = f"{self.base_url}/jobs/{search_query}/"

        try:
            html = await self.fetch_with_browser(url, wait_for=".JobSearchCard-item")
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".JobSearchCard-item, .project-card")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Freelancer: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one(".JobSearchCard-primary-heading a, h3 a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            budget_elem = element.select_one(".JobSearchCard-secondary-price, .budget")
            budget = budget_elem.get_text(strip=True) if budget_elem else ""

            skills_elem = element.select(".JobSearchCard-primary-tags a, .tag")
            keywords = [skill.get_text(strip=True) for skill in skills_elem]

            return self._create_job(
                title=title,
                company="Freelancer Client",
                location="Remote (Freelancer)",
                job_type=JobType.FREELANCE,
                description=budget,
                application_url=job_url,
                source_job_id=job_url,
                keywords=keywords,
                metadata={"budget": budget, "platform": "freelancer"},
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Freelancer listing: {e}")
            return None


class GuruScraper(BaseScraper):
    """Scraper for Guru.com."""

    def __init__(self):
        super().__init__(
            source=JobSource.GURU,
            base_url="https://www.guru.com",
            rate_limit=3.0,
            use_browser=True,
        )

    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        jobs = []
        search_query = quote_plus(query)
        url = f"{self.base_url}/d/jobs/{search_query}/"

        try:
            html = await self.fetch_with_browser(url, wait_for=".jobRecord")
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".jobRecord, .job-item")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Guru: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one(".jobTitle a, h3 a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            company_elem = element.select_one(".employerName, .company")
            company = company_elem.get_text(strip=True) if company_elem else "Guru Client"

            budget_elem = element.select_one(".jobBudget, .budget")
            budget = budget_elem.get_text(strip=True) if budget_elem else ""

            return self._create_job(
                title=title,
                company=company,
                location="Remote (Guru)",
                job_type=JobType.FREELANCE,
                description=budget,
                application_url=job_url,
                source_job_id=job_url,
                metadata={"budget": budget, "platform": "guru"},
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Guru listing: {e}")
            return None


class PeoplePerHourScraper(BaseScraper):
    """Scraper for PeoplePerHour."""

    def __init__(self):
        super().__init__(
            source=JobSource.PEOPLE_PER_HOUR,
            base_url="https://www.peopleperhour.com",
            rate_limit=3.0,
            use_browser=True,
        )

    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        jobs = []
        search_query = quote_plus(query)
        url = f"{self.base_url}/freelance-jobs/{search_query}"

        try:
            html = await self.fetch_with_browser(url, wait_for=".job-card")
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-card, .project-card")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape PeoplePerHour: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h3 a, .job-title a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            budget_elem = element.select_one(".budget, .price")
            budget = budget_elem.get_text(strip=True) if budget_elem else ""

            skills_elem = element.select(".skill, .tag")
            keywords = [skill.get_text(strip=True) for skill in skills_elem]

            return self._create_job(
                title=title,
                company="PPH Client",
                location="Remote (PeoplePerHour)",
                job_type=JobType.FREELANCE,
                description=budget,
                application_url=job_url,
                source_job_id=job_url,
                keywords=keywords,
                metadata={"budget": budget, "platform": "peopleperhour"},
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse PeoplePerHour listing: {e}")
            return None


def register_consultancy_scrapers(registry):
    """Register all consultancy scrapers with the registry."""
    registry.register(UpworkScraper())
    registry.register(ToptalScraper())
    registry.register(FreelancerScraper())
    registry.register(GuruScraper())
    registry.register(PeoplePerHourScraper())
