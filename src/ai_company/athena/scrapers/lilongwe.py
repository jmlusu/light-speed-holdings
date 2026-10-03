from typing import List, Optional
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup

from ..models import Job, JobSource, JobType
from .base import BaseScraper


class LilongweJobsScraper(BaseScraper):
    """Scraper for Lilongwe-specific job boards."""

    def __init__(self):
        super().__init__(
            source=JobSource.MALAWI_JOBS,
            base_url="https://www.malawijobs.com",
            rate_limit=2.0,
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
        location_param = quote_plus(location or "Lilongwe")
        url = f"{self.base_url}/jobs?q={search_query}&location={location_param}"

        try:
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-listing, .job-card, .job-item, [class*='job-']")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Malawi Jobs: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h2 a, h3 a, .job-title a, [class*='title'] a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            company_elem = element.select_one(".company, .employer, [class*='company']")
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"

            location_elem = element.select_one(".location, [class*='location']")
            location = location_elem.get_text(strip=True) if location_elem else "Lilongwe, Malawi"

            desc_elem = element.select_one(".description, .summary, [class*='description']")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            return self._create_job(
                title=title,
                company=company,
                location=location,
                job_type=JobType.FULL_TIME,
                description=description,
                application_url=job_url,
                source_job_id=job_url,
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse job listing: {e}")
            return None


class MalawiWorkScraper(BaseScraper):
    """Scraper for Malawi Work job board."""

    def __init__(self):
        super().__init__(
            source=JobSource.MALAWI_WORK,
            base_url="https://malawiwork.com",
            rate_limit=2.0,
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
        url = f"{self.base_url}/jobs/search?q={search_query}"

        try:
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-listing, .job-card, article.job")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Malawi Work: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h2 a, h3 a, .job-title a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            company_elem = element.select_one(".company-name, .employer")
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"

            location_elem = element.select_one(".job-location, .location")
            location = location_elem.get_text(strip=True) if location_elem else "Lilongwe, Malawi"

            desc_elem = element.select_one(".job-excerpt, .description")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            return self._create_job(
                title=title,
                company=company,
                location=location,
                job_type=JobType.FULL_TIME,
                description=description,
                application_url=job_url,
                source_job_id=job_url,
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Malawi Work listing: {e}")
            return None


class JobsMalawiScraper(BaseScraper):
    """Scraper for Jobs Malawi portal."""

    def __init__(self):
        super().__init__(
            source=JobSource.JOBS_MALAWI,
            base_url="https://jobs.malawi.net",
            rate_limit=2.0,
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
        url = f"{self.base_url}/search?q={search_query}"

        try:
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.select(".job-result, .listing-item, .job-post")

            for card in job_cards[:max_results]:
                job = await self.parse_job_listing(card)
                if job:
                    jobs.append(job)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to scrape Jobs Malawi: {e}")

        return jobs

    async def parse_job_listing(self, element) -> Optional[Job]:
        try:
            title_elem = element.select_one("h2 a, .job-title a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            job_url = urljoin(self.base_url, title_elem.get("href", ""))

            company_elem = element.select_one(".company, .employer-name")
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"

            location_elem = element.select_one(".location, .job-location")
            location = location_elem.get_text(strip=True) if location_elem else "Lilongwe, Malawi"

            desc_elem = element.select_one(".snippet, .description")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            return self._create_job(
                title=title,
                company=company,
                location=location,
                job_type=JobType.FULL_TIME,
                description=description,
                application_url=job_url,
                source_job_id=job_url,
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to parse Jobs Malawi listing: {e}")
            return None


def register_lilongwe_scrapers(registry):
    """Register all Lilongwe scrapers with the registry."""
    registry.register(LilongweJobsScraper())
    registry.register(MalawiWorkScraper())
    registry.register(JobsMalawiScraper())
