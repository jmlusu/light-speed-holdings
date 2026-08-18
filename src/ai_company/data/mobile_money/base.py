"""Abstract base class for Mobile Money providers.

Defines the unified interface that all mobile money providers must implement.
"""

from __future__ import annotations

import hashlib
import hmac
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional


class ProviderError(Exception):
    """Base exception for mobile money provider errors."""

    def __init__(self, message: str, code: str = "PROVIDER_ERROR", details: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


class InvalidSignatureError(ProviderError):
    """Raised when webhook signature verification fails."""

    def __init__(self, message: str = "Invalid webhook signature", details: Optional[dict[str, Any]] = None):
        super().__init__(message, "INVALID_SIGNATURE", details)


class DuplicateTransactionError(ProviderError):
    """Raised when a duplicate transaction is detected."""

    def __init__(self, message: str = "Duplicate transaction", transaction_id: str = ""):
        super().__init__(message, "DUPLICATE_TRANSACTION", {"transaction_id": transaction_id})


class InsufficientFundsError(ProviderError):
    """Raised when the payer has insufficient funds."""

    def __init__(self, message: str = "Insufficient funds", details: Optional[dict[str, Any]] = None):
        super().__init__(message, "INSUFFICIENT_FUNDS", details)


class TimeoutError(ProviderError):
    """Raised when provider request times out."""

    def __init__(self, message: str = "Provider request timeout", details: Optional[dict[str, Any]] = None):
        super().__init__(message, "TIMEOUT", details)


@dataclass
class WebhookPayload:
    """Normalized webhook payload from any provider."""

    provider: str
    transaction_id: str
    amount: Decimal
    currency: str
    customer_reference: str
    payer_phone: str
    status: str  # completed, failed, pending
    timestamp: datetime
    metadata: dict[str, Any]
    raw_payload: dict[str, Any]

    @property
    def idempotency_key(self) -> str:
        """Generate idempotency key for this transaction."""
        # Format: provider:transaction_id
        return f"{self.provider}:{self.transaction_id}"


class AbstractProvider(ABC):
    """Abstract base class for mobile money providers.

    All providers must implement:
    - verify_signature: Validate webhook authenticity
    - parse_webhook: Normalize provider-specific payload
    - idempotency_key: Generate unique key for deduplication
    """

    PROVIDER_NAME: str = "base"
    SUPPORTED_CURRENCIES: tuple[str, ...] = ("MWK", "USD")

    def __init__(self, webhook_secret: str, **kwargs: Any):
        self.webhook_secret = webhook_secret
        self.config = kwargs

    @abstractmethod
    def verify_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify webhook signature using provider-specific method.

        Args:
            payload: Raw request body bytes
            signature_header: Signature from request headers

        Returns:
            True if signature is valid

        Raises:
            InvalidSignatureError: If signature is invalid
        """
        pass

    @abstractmethod
    def parse_webhook(self, payload: dict[str, Any], headers: dict[str, Any]) -> WebhookPayload:
        """Parse provider-specific webhook into normalized payload.

        Args:
            payload: Parsed JSON body
            headers: Request headers

        Returns:
            Normalized WebhookPayload

        Raises:
            ProviderError: If payload is malformed
        """
        pass

    def generate_idempotency_key(self, transaction_id: str) -> str:
        """Generate idempotency key for this transaction.

        Format: {provider}:{transaction_id}
        """
        return f"{self.PROVIDER_NAME}:{transaction_id}"

    def verify_hmac_sha256(self, payload: bytes, signature: str, secret: Optional[str] = None) -> bool:
        """Verify HMAC-SHA256 signature.

        Args:
            payload: Raw request body
            signature: Signature from header (hex encoded)
            secret: HMAC secret (defaults to self.webhook_secret)

        Returns:
            True if signature matches
        """
        secret = secret or self.webhook_secret
        expected = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def normalize_amount(self, amount: Any, currency: str) -> Decimal:
        """Normalize amount to Decimal with proper precision.

        Args:
            amount: Amount from provider (string, int, float)
            currency: Currency code (MWK, USD)

        Returns:
            Decimal amount with appropriate decimal places
        """
        decimal_amount = Decimal(str(amount))
        if currency == "MWK":
            # MWK typically has no decimal places - standard rounding
            return decimal_amount.quantize(Decimal("1"), rounding="ROUND_HALF_UP")
        # USD and others: 2 decimal places
        return decimal_amount.quantize(Decimal("0.01"))

    def validate_currency(self, currency: str) -> None:
        """Validate currency is supported."""
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ProviderError(
                f"Unsupported currency: {currency}",
                "UNSUPPORTED_CURRENCY",
                {"supported": list(self.SUPPORTED_CURRENCIES)}
            )
