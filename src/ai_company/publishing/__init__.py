"""Publishing rails for Pharos — queue, formats, and platform adapters.

Buy-side rails per ADR-020: LinkedIn/Substack are reached through a queue of
platform-ready artifacts rather than in-house API churn. Live POSTing fires only
when platform credentials are configured in the environment; otherwise the
``publish`` path returns a dry-run receipt.
"""

from ai_company.publishing.formats import format_linkedin, format_substack
from ai_company.publishing.publishers import LinkedInPublisher, SubstackPublisher
from ai_company.publishing.queue import PublishQueue, PublishRecord

__all__ = [
    "PublishQueue",
    "PublishRecord",
    "LinkedInPublisher",
    "SubstackPublisher",
    "format_linkedin",
    "format_substack",
]
