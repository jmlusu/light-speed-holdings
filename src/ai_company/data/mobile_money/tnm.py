"""TNM Mpamba mobile money provider implementation.

Webhook format (from TNM Mpamba API documentation):
{
  "transaction": {
    "trans_id": "TNM_987654321",
    "amount": "5000",
    "currency": "MWK",
    "msisdn": "265881234567",
    "customer_name": "Jane Smith",
    "reference": "INV-456",
    "status": "COMPLETED",
    "timestamp": "2024-01-15T10:30:00Z",
    "callback_data": {
      "task_id": "task_xyz789"
    }
  }
}

Signature: X-TNM-Signature header (HMAC-SHA256)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import AbstractProvider, InvalidSignatureError, ProviderError, WebhookPayload


class TNMProvider(AbstractProvider):
    """TNM Mpamba mobile money provider for Malawi."""

    PROVIDER_NAME = "tnm"
    SUPPORTED_CURRENCIES = ("MWK", "USD")
    STATUS_COMPLETED = "COMPLETED"
    STATUS_FAILED = "FAILED"
    STATUS_PENDING = "PENDING"

    def verify_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify TNM HMAC-SHA256 signature.

        TNM sends signature in X-TNM-Signature header as hex string.
        """
        if not signature_header:
            raise InvalidSignatureError("Missing X-TNM-Signature header")

        expected = self.verify_hmac_sha256(payload, signature_header)
        if not expected:
            raise InvalidSignatureError("Invalid TNM signature")
        return True

    def parse_webhook(self, payload: dict[str, Any], headers: dict[str, Any]) -> WebhookPayload:
        """Parse TNM webhook into normalized payload."""
        transaction = payload.get("transaction", {})

        if not transaction:
            raise ProviderError("Missing transaction data in webhook", "MALFORMED_PAYLOAD")

        status = transaction.get("status", "")
        if status != self.STATUS_COMPLETED:
            raise ProviderError(
                f"Transaction not completed: {status}",
                "TRANSACTION_FAILED",
                {"status": status}
            )

        transaction_id = transaction.get("trans_id", "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount_raw = transaction.get("amount")
        currency = transaction.get("currency", "MWK")
        amount = self.normalize_amount(amount_raw, currency)
        self.validate_currency(currency)

        customer_reference = transaction.get("reference", "")
        payer_phone = transaction.get("msisdn", "")
        customer_name = transaction.get("customer_name", "")
        callback_data = transaction.get("callback_data", {})

        # Parse timestamp
        timestamp_str = transaction.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            timestamp = datetime.now()

        metadata = {
            "callback_data": callback_data,
            "customer_name": customer_name,
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
