"""PayChangu mobile money provider implementation.

Webhook format (from PayChangu documentation):
{
  "event": "payment.completed",
  "transaction": {
    "id": "txn_abc123",
    "amount": 5000,
    "currency": "MWK",
    "customer": {
      "phone": "+265991234567",
      "email": "customer@example.com",
      "name": "John Doe"
    },
    "reference": "ORDER-123",
    "metadata": {
      "task_id": "task_abc123"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T10:30:05Z"
  }
}

Signature header: X-Paychangu-Signature (HMAC-SHA256 of raw body)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import AbstractProvider, InvalidSignatureError, ProviderError, WebhookPayload


class PayChanguProvider(AbstractProvider):
    """PayChangu mobile money provider for Malawi."""

    PROVIDER_NAME = "paychangu"
    SUPPORTED_CURRENCIES = ("MWK", "USD")
    EVENT_COMPLETED = "payment.completed"
    EVENT_FAILED = "payment.failed"

    def verify_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify PayChangu HMAC-SHA256 signature.

        PayChangu sends signature in X-Paychangu-Signature header as hex string.
        """
        if not signature_header:
            raise InvalidSignatureError("Missing X-Paychangu-Signature header")

        # PayChangu sends hex-encoded HMAC-SHA256
        expected = self.verify_hmac_sha256(payload, signature_header)
        if not expected:
            raise InvalidSignatureError("Invalid PayChangu signature")
        return True

    def parse_webhook(self, payload: dict[str, Any], headers: dict[str, Any]) -> WebhookPayload:
        """Parse PayChangu webhook into normalized payload."""
        event = payload.get("event", "")
        transaction = payload.get("transaction", {})

        if not transaction:
            raise ProviderError("Missing transaction data in webhook", "MALFORMED_PAYLOAD")

        # Only process completed payments
        if event != self.EVENT_COMPLETED:
            raise ProviderError(
                f"Unhandled event type: {event}",
                "UNHANDLED_EVENT",
                {"event": event}
            )

        # Extract fields
        transaction_id = transaction.get("id", "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount_raw = transaction.get("amount")
        currency = transaction.get("currency", "MWK")
        amount = self.normalize_amount(amount_raw, currency)
        self.validate_currency(currency)

        customer = transaction.get("customer", {})
        customer_reference = transaction.get("reference", "")
        payer_phone = customer.get("phone", "")
        metadata = transaction.get("metadata", {})

        # Parse timestamps
        timestamp_str = transaction.get("completed_at") or transaction.get("created_at")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            timestamp = datetime.now()

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
