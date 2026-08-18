"""Airtel Money mobile money provider implementation.

Webhook format (from Airtel Money API documentation):
{
  "transaction": {
    "transaction_id": "AIRTEL_123456789",
    "amount": "5000.00",
    "currency": "MWK",
    "payer_msisdn": "265991234567",
    "payer_name": "John Doe",
    "reference": "ORDER-123",
    "status": "SUCCESS",
    "timestamp": "2024-01-15T10:30:00Z",
    "external_id": "task_abc123"
  }
}

Signature: X-Airtel-Signature header (HMAC-SHA256 of raw body with secret)
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from .base import AbstractProvider, WebhookPayload, InvalidSignatureError, ProviderError


class AirtelProvider(AbstractProvider):
    """Airtel Money mobile money provider for Malawi."""

    PROVIDER_NAME = "airtel"
    SUPPORTED_CURRENCIES = ("MWK", "USD")
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILED = "FAILED"
    STATUS_PENDING = "PENDING"

    def verify_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify Airtel HMAC-SHA256 signature.

        Airtel sends signature in X-Airtel-Signature header as hex string.
        """
        if not signature_header:
            raise InvalidSignatureError("Missing X-Airtel-Signature header")

        # Airtel sends hex-encoded HMAC-SHA256
        expected = self.verify_hmac_sha256(payload, signature_header)
        if not expected:
            raise InvalidSignatureError("Invalid Airtel signature")
        return True

    def parse_webhook(self, payload: dict, headers: dict) -> WebhookPayload:
        """Parse Airtel webhook into normalized payload."""
        transaction = payload.get("transaction", {})

        if not transaction:
            raise ProviderError("Missing transaction data in webhook", "MALFORMED_PAYLOAD")

        status = transaction.get("status", "")
        if status != self.STATUS_SUCCESS:
            raise ProviderError(
                f"Transaction not successful: {status}",
                "TRANSACTION_FAILED",
                {"status": status}
            )

        transaction_id = transaction.get("transaction_id", "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount_raw = transaction.get("amount")
        currency = transaction.get("currency", "MWK")
        amount = self.normalize_amount(amount_raw, currency)
        self.validate_currency(currency)

        customer_reference = transaction.get("reference", "")
        payer_phone = transaction.get("payer_msisdn", "")
        payer_name = transaction.get("payer_name", "")
        external_id = transaction.get("external_id", "")

        # Parse timestamp
        timestamp_str = transaction.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            timestamp = datetime.now()

        metadata = {
            "external_id": external_id,
            "payer_name": payer_name,
            "provider_transaction_id": transaction_id,
        }

        return WebhookPayload(
            provider=self.PROVIDER_NAME,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            customer_reference=customer_reference,
            payer_phone=payer_phone,
            status="completed",
            timestamp=timestamp,
            metadata=metadata,
            raw_payload=payload,
        )