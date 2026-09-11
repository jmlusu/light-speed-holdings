"""FX rate service with 24-hour in-memory cache.

Uses ExchangeRate-API.com Free tier (1500 req/mo).
Falls back to hardcoded rate on API failure.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

# Fallback rate: 1800 MWK = 1 USD
_FALLBACK_RATE = 1800.0

# Cache TTL: 24 hours in seconds
_CACHE_TTL = 24 * 60 * 60


class FxRateService:
    """Service for fetching and caching FX rates.

    Uses ExchangeRate-API.com Free tier with 24h in-memory cache.
    Thread-safe via GIL (single Python process).
    """

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = _CACHE_TTL):
        self._api_key = api_key or os.environ.get("EXCHANGERATE_API_KEY", "")
        self._cache_ttl = cache_ttl
        self._cache: dict[str, tuple[float, float]] = {}  # key -> (rate, timestamp)

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate from from_currency to to_currency.

        Returns cached rate if within TTL, otherwise fetches from API.
        Falls back to hardcoded rate on failure.
        """
        if from_currency == to_currency:
            return 1.0

        cache_key = f"{from_currency}:{to_currency}"
        now = time.time()

        # Check cache
        if cache_key in self._cache:
            rate, cached_at = self._cache[cache_key]
            if now - cached_at < self._cache_ttl:
                return rate

        # Fetch from API
        fetched_rate = self._fetch_rate(from_currency, to_currency)
        if fetched_rate is not None:
            self._cache[cache_key] = (fetched_rate, now)
            return fetched_rate

        # Fallback
        if from_currency == "MWK" and to_currency == "USD":
            return _FALLBACK_RATE
        if from_currency == "USD" and to_currency == "MWK":
            return 1.0 / _FALLBACK_RATE
        return 1.0

    def _fetch_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Fetch rate from ExchangeRate-API.com.

        Returns None on failure (triggers fallback).
        """
        if not self._api_key:
            logger.debug("No EXCHANGERATE_API_KEY set, using fallback rate")
            return None

        url = (
            f"https://v6.exchangerate-api.com/v6/{self._api_key}/pair/{from_currency}/{to_currency}"
        )

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ai-company/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                if data.get("result") == "success":
                    return float(data["conversion_rate"])
                logger.warning("FX API returned non-success: %s", data.get("result"))
                return None
        except (urllib.error.URLError, ValueError, KeyError) as e:
            logger.warning("FX rate fetch failed for %s/%s: %s", from_currency, to_currency, e)
            return None

    def clear_cache(self) -> None:
        """Clear the rate cache (useful for testing)."""
        self._cache.clear()


# Module-level singleton
_fx_service: Optional[FxRateService] = None


def get_fx_service() -> FxRateService:
    """Get or create the singleton FxRateService."""
    global _fx_service
    if _fx_service is None:
        _fx_service = FxRateService()
    return _fx_service
