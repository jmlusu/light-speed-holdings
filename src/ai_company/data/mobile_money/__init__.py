"""Mobile Money provider package.

Provides unified interface for multiple mobile money providers
with unified signature verification, parsing, and idempotency.
"""

from __future__ import annotations

from .airtel import AirtelProvider
from .base import (
    AbstractProvider,
    DuplicateTransactionError,
    InvalidSignatureError,
    ProviderError,
    WebhookPayload,
)
from .factory import ProviderRegistry, get_provider
from .mock import MockProvider
from .paychangu import PayChanguProvider
from .tnm import TNMProvider

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
