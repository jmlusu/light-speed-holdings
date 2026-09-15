"""Publisher adapters for the Pharos publish rails.

Env-gated by design (ADR-020, buy-side): a live HTTP POST fires ONLY when the
corresponding platform credentials are present in the environment.  Without
creds the adapter returns a **dry-run receipt** so the queue/CLI stay fully
exercisable and testable offline.  No secrets are ever stored or committed.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

from ai_company.publishing.formats import format_linkedin, format_substack
from ai_company.publishing.queue import PublishRecord

logger = logging.getLogger(__name__)

# Env keys (DASHBOARD-key naming style, ADR-012/RBAC convention):
#   PHAROS_LINKEDIN_API_URL / PHAROS_LINKEDIN_TOKEN
#   PHAROS_SUBSTACK_API_URL  / PHAROS_SUBSTACK_TOKEN
LINKEDIN_URL_ENV = "PHAROS_LINKEDIN_API_URL"
LINKEDIN_TOKEN_ENV = "PHAROS_LINKEDIN_TOKEN"
SUBSTACK_URL_ENV = "PHAROS_SUBSTACK_API_URL"
SUBSTACK_TOKEN_ENV = "PHAROS_SUBSTACK_TOKEN"


@dataclass
class PublishResult:
    """Outcome of a publish attempt.

    ``status`` is one of ``dry_run`` (no creds configured), ``posted`` (HTTP
    success) or ``failed`` (transport/HTTP error).  ``url`` is set only on
    success, ``error`` only on failure.
    """

    status: str
    platform: str
    record_id: str
    title: str
    url: str = ""
    error: str = ""
    detail: dict[str, Any] = field(default_factory=dict)


class _BasePublisher:
    """Shared envelope: decide dry-run vs live, then hand off to ``_post``."""

    platform = ""

    def _creds(self) -> tuple[str, str]:
        """Return ``(url, token)`` for this platform (empty when unconfigured)."""
        raise NotImplementedError

    def publish(
        self,
        record: PublishRecord,
        *,
        force_live: bool = False,
    ) -> PublishResult:
        """Publish *record* to this platform.

        Returns a dry-run receipt when creds are absent (unless ``force_live``,
        which is used only by explicit opt-in operators/tests).  Never raises on
        transport errors — they become a ``failed`` result.
        """
        url, token = self._creds()
        if not (url and token) and not force_live:
            logger.info("No creds for %s — returning dry-run receipt", self.platform)
            return PublishResult(
                status="dry_run",
                platform=self.platform,
                record_id=record.id,
                title=record.title,
                detail={"note": "credentials not configured; live POST skipped"},
            )

        formatted = self._format(record)
        try:
            body = self._post(url, token, formatted)
        except Exception as exc:  # noqa: BLE001 - surface transport failure as a result
            logger.exception("Publish to %s failed for %s", self.platform, record.id)
            return PublishResult(
                status="failed",
                platform=self.platform,
                record_id=record.id,
                title=record.title,
                error=str(exc),
                detail={"formatted": formatted},
            )
        return PublishResult(
            status="posted",
            platform=self.platform,
            record_id=record.id,
            title=record.title,
            url=body.get("url", ""),
            detail={"formatted": formatted},
        )

    def _format(self, record: PublishRecord) -> dict[str, Any]:
        raise NotImplementedError

    def _post(self, url: str, token: str, formatted: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class LinkedInPublisher(_BasePublisher):
    """Posts a LinkedIn-ready artifact to ``PHAROS_LINKEDIN_API_URL``."""

    platform = "linkedin"

    def _creds(self) -> tuple[str, str]:
        return os.environ.get(LINKEDIN_URL_ENV, ""), os.environ.get(LINKEDIN_TOKEN_ENV, "")

    def _format(self, record: PublishRecord) -> dict[str, Any]:
        return format_linkedin(record.title, record.body)

    def _post(self, url: str, token: str, formatted: dict[str, Any]) -> dict[str, Any]:
        import httpx

        resp = httpx.post(
            url,
            json={
                "author": "urn:li:person:light_speed_holdings",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": formatted["text"]},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            },
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=15.0,
        )
        resp.raise_for_status()
        return {"url": resp.headers.get("Location", "")}


class SubstackPublisher(_BasePublisher):
    """Posts a Substack-ready markdown artifact to ``PHAROS_SUBSTACK_API_URL``."""

    platform = "substack"

    def _creds(self) -> tuple[str, str]:
        return os.environ.get(SUBSTACK_URL_ENV, ""), os.environ.get(SUBSTACK_TOKEN_ENV, "")

    def _format(self, record: PublishRecord) -> dict[str, Any]:
        return format_substack(record.title, record.body)

    def _post(self, url: str, token: str, formatted: dict[str, Any]) -> dict[str, Any]:
        import httpx

        resp = httpx.post(
            url,
            json={
                "title": formatted["markdown"].splitlines()[0].lstrip("# ").strip(),
                "markdown": formatted["markdown"],
            },
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=15.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return {"url": data.get("url", "")}


__all__ = [
    "LINKEDIN_URL_ENV",
    "LINKEDIN_TOKEN_ENV",
    "SUBSTACK_URL_ENV",
    "SUBSTACK_TOKEN_ENV",
    "LinkedInPublisher",
    "PublishResult",
    "SubstackPublisher",
]
