"""Mobile Money provider package.

Provides unified interface for multiple mobile money providers
with unified signature verification, parsing, and idempotency.
"""

from __future__ import annotations

from .base import AbstractProvider, WebhookPayload, ProviderError, InvalidSignatureError, DuplicateTransactionError
from .paychangu import PayChanguProvider
from .airtel import AirtelProvider
from .tnm import TNMProvider
from .mock import MockProvider
from .factory import get_provider, ProviderRegistry

__all__ = [
    "AbstractProvider",
    "WebhookPayload",
    "ProviderError",
    "InvalidSignatureError",
    "DuplicateTransactionError",
    "PayChanguProvider",
    "AirtelProvider",
    "TNMProvider",
    "MockProvider",
    "get_provider",
    "ProviderRegistry",
]