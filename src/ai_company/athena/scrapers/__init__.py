from .base import BaseScraper, ScraperRegistry, scraper_registry
from .consultancy import register_consultancy_scrapers
from .lilongwe import register_lilongwe_scrapers
from .remote import register_remote_scrapers


def register_all_scrapers():
    """Register all scrapers with the global registry."""
    register_lilongwe_scrapers(scraper_registry)
    register_remote_scrapers(scraper_registry)
    register_consultancy_scrapers(scraper_registry)


# Auto-register on import
register_all_scrapers()

__all__ = [
    "BaseScraper",
    "ScraperRegistry",
    "scraper_registry",
    "register_all_scrapers",
]
