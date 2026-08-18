"""Mock mobile money provider for testing.

Simulates all three providers (PayChangu, Airtel, TNM) with configurable
success/failure/timeout scenarios for contract testing.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Literal, Optional

from .base import AbstractProvider, WebhookPayload, InvalidSignatureError, ProviderError


class MockProvider(AbstractProvider):
    """Mock provider that simulates all three mobile money providers.

    Can be configured to simulate:
    - Success responses
    - Invalid signatures
    - Duplicate transactions
    - Timeouts
    - Insufficient funds
    - Various error conditions
    """

    PROVIDER_NAME = "mock"
    SUPPORTED_CURRENCIES = ("MWK", "USD", "EUR", "GBP")

    def __init__(
        self,
        webhook_secret: str = "test_secret",
        provider_to_simulate: Literal["paychangu", "airtel", "tnm"] = "paychangu",
        scenario: Literal["success", "invalid_signature", "duplicate", "timeout", "insufficient_funds", "invalid_payload"] = "success",
        delay_ms: int = 0,
        **kwargs,
    ):
        super().__init__(webhook_secret)
        self.provider_to_simulate = provider_to_simulate
        self.scenario = scenario
        self.delay_ms = delay_ms
        self._seen_transactions: set[str] = set()
        self._provider_configs = {
            "paychangu": {
                "provider_name": "paychangu",
                "signature_header": "X-Paychangu-Signature",
                "event_field": "event",
                "event_completed": "payment.completed",
                "transaction_field": "transaction",
                "id_field": "id",
            },
            "airtel": {
                "provider_name": "airtel",
                "signature_header": "X-Airtel-Signature",
                "status_field": "status",
                "status_success": "SUCCESS",
                "transaction_field": "transaction",
                "id_field": "transaction_id",
            },
            "tnm": {
                "provider_name": "tnm",
                "signature_header": "X-TNM-Signature",
                "status_field": "status",
                "status_completed": "COMPLETED",
                "transaction_field": "transaction",
                "id_field": "trans_id",
            },
        }
        self._config = self._provider_configs.get(provider_to_simulate, self._provider_configs["paychangu"])

    def verify_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify mock signature based on scenario."""
        # Simulate delay
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)

        if self.scenario == "invalid_signature":
            raise InvalidSignatureError(f"Mock {self.provider_to_simulate} invalid signature")

        # For valid signatures, always return True in success scenario
        if self.scenario == "success":
            return True

        # For other scenarios, still verify but may raise later
        config = self._config
        secret = self.webhook_secret.encode("utf-8")
        expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature_header)

    def parse_webhook(self, payload: dict, headers: dict) -> WebhookPayload:
        """Parse mock webhook based on configured scenario."""
        config = self._config
        provider_name = self.provider_to_simulate

        # Handle invalid_signature scenario by checking signature from headers
        if self.scenario == "invalid_signature":
            config = self._config
            signature_header = headers.get(config["signature_header"], "")
            payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
            self.verify_signature(payload_bytes, signature_header)

        # Simulate delay
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)

        # Handle scenarios
        if self.scenario == "timeout":
            time.sleep(5)  # Simulate 5 second timeout
            raise ProviderError("Mock timeout [TIMEOUT]", "TIMEOUT")

        if self.scenario == "insufficient_funds":
            raise ProviderError("Insufficient funds [INSUFFICIENT_FUNDS]", "INSUFFICIENT_FUNDS", {"balance": 100})

        if self.scenario == "duplicate":
            # Check if we've seen this transaction
            txn_field = config["id_field"]
            txn_data = payload.get(config["transaction_field"], {})
            txn_id = txn_data.get(txn_field, "")
            if not txn_id:
                raise ProviderError("Missing transaction ID for duplicate check [MALFORMED_PAYLOAD]", "MALFORMED_PAYLOAD")
            if txn_id in self._seen_transactions:
                raise ProviderError(
                    f"Duplicate transaction: {txn_id} [DUPLICATE_TRANSACTION]",
                    "DUPLICATE_TRANSACTION",
                    {"transaction_id": txn_id}
                )
            self._seen_transactions.add(txn_id)

        if self.scenario == "invalid_payload":
            raise ProviderError("Invalid payload structure [MALFORMED_PAYLOAD]", "MALFORMED_PAYLOAD")

        # Parse based on provider
        if provider_name == "paychangu":
            return self._parse_paychangu(payload, config)
        elif provider_name == "airtel":
            return self._parse_airtel(payload, config)
        elif provider_name == "tnm":
            return self._parse_tnm(payload, config)
        else:
            raise ProviderError(f"Unknown provider: {provider_name}", "UNKNOWN_PROVIDER")

    def _parse_paychangu(self, payload: dict, config: dict) -> WebhookPayload:
        """Parse PayChangu-style mock payload."""
        event = payload.get(config["event_field"], "")
        transaction = payload.get(config["transaction_field"], {})

        if event != config["event_completed"]:
            raise ProviderError(f"Unhandled event: {event}", "UNHANDLED_EVENT")

        transaction_id = transaction.get(config["id_field"], "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount = self.normalize_amount(transaction.get("amount", 1000), "MWK")
        self.validate_currency("MWK")

        customer = transaction.get("customer", {})
        customer_reference = transaction.get("reference", "")
        payer_phone = customer.get("phone", "")
        metadata = transaction.get("metadata", {})

        timestamp_str = transaction.get("completed_at") or transaction.get("created_at")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.now(timezone.utc)
        except (ValueError, TypeError):
            timestamp = datetime.now(timezone.utc)

        return WebhookPayload(
            provider="paychangu",
            transaction_id=transaction_id,
            amount=amount,
            currency="MWK",
            customer_reference=customer_reference,
            payer_phone=payer_phone,
            status="completed",
            timestamp=timestamp,
            metadata=metadata,
            raw_payload=payload,
        )

    def _parse_airtel(self, payload: dict, config: dict) -> WebhookPayload:
        """Parse Airtel-style mock payload."""
        transaction = payload.get(config["transaction_field"], {})

        if transaction.get(config["status_field"]) != config["status_success"]:
            raise ProviderError("Transaction not successful", "TRANSACTION_FAILED")

        transaction_id = transaction.get(config["id_field"], "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount = self.normalize_amount(transaction.get("amount", 1000), "MWK")
        self.validate_currency("MWK")

        customer_reference = transaction.get("reference", "")
        payer_phone = transaction.get("payer_msisdn", "")
        external_id = transaction.get("external_id", "")

        timestamp_str = transaction.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.now(timezone.utc)
        except (ValueError, TypeError):
            timestamp = datetime.now(timezone.utc)

        metadata = {"external_id": external_id}
        return WebhookPayload(
            provider="airtel",
            transaction_id=transaction_id,
            amount=amount,
            currency="MWK",
            customer_reference=customer_reference,
            payer_phone=payer_phone,
            status="completed",
            timestamp=timestamp,
            metadata=metadata,
            raw_payload=payload,
        )

    def _parse_tnm(self, payload: dict, config: dict) -> WebhookPayload:
        """Parse TNM-style mock payload."""
        transaction = payload.get(config["transaction_field"], {})

        if transaction.get(config["status_field"]) != config["status_completed"]:
            raise ProviderError("Transaction not completed", "TRANSACTION_FAILED")

        transaction_id = transaction.get(config["id_field"], "")
        if not transaction_id:
            raise ProviderError("Missing transaction ID", "MALFORMED_PAYLOAD")

        amount = self.normalize_amount(transaction.get("amount", 1000), "MWK")
        self.validate_currency("MWK")

        customer_reference = transaction.get("reference", "")
        payer_phone = transaction.get("msisdn", "")
        callback_data = transaction.get("callback_data", {})

        timestamp_str = transaction.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.now(timezone.utc)
        except (ValueError, TypeError):
            timestamp = datetime.now(timezone.utc)

        metadata = {"callback_data": callback_data}
        return WebhookPayload(
            provider="tnm",
            transaction_id=transaction_id,
            amount=amount,
            currency="MWK",
            customer_reference=customer_reference,
            payer_phone=payer_phone,
            status="completed",
            timestamp=timestamp,
            metadata=metadata,
            raw_payload=payload,
        )

    def reset_seen_transactions(self) -> None:
        """Reset the seen transactions set (for testing)."""
        self._seen_transactions.clear()

    def set_scenario(self, scenario: str) -> None:
        """Change the mock scenario."""
        self.scenario = scenario