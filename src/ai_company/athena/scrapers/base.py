import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, cast

import httpx
from pydantic import HttpUrl

try:
    from playwright.async_api import (
        Browser as PlaywrightBrowser,
    )
    from playwright.async_api import (
        async_playwright,
    )

    PLAYWRIGHT_AVAILABLE = True
except ImportError:  # pragma: no cover - playwright is an optional e2e dependency
    PLAYWRIGHT_AVAILABLE = False
    # Only referenced behind the PLAYWRIGHT_AVAILABLE guard, so Any placeholders
    # keep the module importable and mypy happy when the e2e extra is not installed.
    PlaywrightBrowser = Any  # noqa: F811
    async_playwright = Any  # noqa: F811

from ..models import Job, JobSource, JobType

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for job scrapers."""

    def __init__(
        self,
        source: JobSource,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        rate_limit: float = 1.0,  # seconds between requests
        use_browser: bool = False,
    ) -> None:
        self.source = source
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.rate_limit = rate_limit
        self.use_browser = use_browser
        self._client: Optional[httpx.AsyncClient] = None
        self._browser: Optional[PlaywrightBrowser] = None
        self._last_request_time = 0.0
        self.logger = logger

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers=self.headers,
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def _get_browser(self) -> PlaywrightBrowser:
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Athena browser fetching requires the optional 'playwright' package")
        if self._browser is None or not self._browser.is_connected():
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(headless=True)
        return self._browser

    async def _rate_limit_wait(self) -> None:
        import time

        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self._last_request_time = time.time()

    async def fetch_html(self, url: str) -> str:
        """Fetch HTML content from URL."""
        await self._rate_limit_wait()
        client = await self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        return response.text

    async def fetch_json(self, url: str) -> Dict[str, Any]:
        """Fetch JSON content from URL."""
        await self._rate_limit_wait()
        client = await self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    async def fetch_with_browser(self, url: str, wait_for: Optional[str] = None) -> str:
        """Fetch page using Playwright browser."""
        browser = await self._get_browser()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle")
            if wait_for:
                await page.wait_for_selector(wait_for, timeout=10000)
            content = await page.content()
            return cast(str, content)
        finally:
            await page.close()

    @abstractmethod
    async def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
    ) -> List[Job]:
        """Search for jobs matching criteria."""
        pass

    @abstractmethod
    async def parse_job_listing(self, element_or_html: Any) -> Optional[Job]:
        """Parse a single job listing from HTML element or page."""
        pass

    async def get_job_details(self, job: Job) -> Job:
        """Fetch detailed job information from job URL."""
        return job

    async def close(self) -> None:
        """Clean up resources."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        if self._browser and self._browser.is_connected():
            await self._browser.close()

    def _create_job(
        self,
        title: str,
        company: str,
        location: str,
        job_type: JobType,
        description: str,
        application_url: str,
        **kwargs: Any,
    ) -> Job:
        """Helper to create a Job with common fields."""
        return Job(
            source=self.source,
            title=title,
            company=company,
            location=location,
            job_type=job_type,
            description=description,
            application_url=HttpUrl(application_url),
            **kwargs,
        )


class ScraperRegistry:
    """Registry for managing all scrapers."""

    def __init__(self) -> None:
        self._scrapers: Dict[JobSource, BaseScraper] = {}

    def register(self, scraper: BaseScraper) -> None:
        self._scrapers[scraper.source] = scraper

    def get(self, source: JobSource) -> Optional[BaseScraper]:
        return self._scrapers.get(source)

    def get_all(self) -> List[BaseScraper]:
        return list(self._scrapers.values())

    async def search_all(
        self,
        query: str,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        max_results: int = 100,
        sources: Optional[List[JobSource]] = None,
    ) -> List[Job]:
        """Search across all registered scrapers."""
        scrapers: List[BaseScraper] = list(self._scrapers.values())
        if sources:
            scrapers = [s for s in scrapers if s.source in sources]

        all_jobs: List[Job] = []
        for scraper in scrapers:
            try:
                jobs = await scraper.search_jobs(query, location, job_type, max_results)
                all_jobs.extend(jobs)
                logger.info(f"Scraper {scraper.source} found {len(jobs)} jobs")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Scraper {scraper.source} failed: {e}")

        return all_jobs

    async def close_all(self) -> None:
        for scraper in self._scrapers.values():
            await scraper.close()


# Global registry instance
scraper_registry = ScraperRegistry()
