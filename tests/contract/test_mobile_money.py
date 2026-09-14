"""Contract tests for mobile money providers.

Tests verify that all providers (PayChangu, Airtel, TNM, Mock) correctly
implement the AbstractProvider interface with proper signature verification,
idempotency, and payload parsing.
"""

from __future__ import annotations

import hashlib
import hmac
from decimal import Decimal

import pytest

from ai_company.data.mobile_money import (
    AirtelProvider,
    InvalidSignatureError,
    MockProvider,
    PayChanguProvider,
    ProviderError,
    TNMProvider,
    get_provider,
)


class TestProviderInterface:
    """Test that all providers implement the required interface."""

    @pytest.mark.parametrize("provider_name", ["paychangu", "airtel", "tnm", "mock"])
    def test_provider_creation(self, provider_name):
        """Test that all providers can be created via factory."""
        provider = get_provider(provider_name, webhook_secret="test_secret")
        assert provider is not None
        assert hasattr(provider, "verify_signature")
        assert hasattr(provider, "parse_webhook")
        assert hasattr(provider, "generate_idempotency_key")

    def test_mock_provider_creation(self):
        """Test mock provider with different configurations."""
        # Default (PayChangu)
        mock = get_provider("mock", "secret", provider_to_simulate="paychangu", scenario="success")
        assert mock.PROVIDER_NAME == "mock"

        # Airtel simulation
        mock = get_provider("mock", "secret", provider_to_simulate="airtel", scenario="success")
        assert mock.PROVIDER_NAME == "mock"

        # TNM simulation
        mock = get_provider("mock", "secret", provider_to_simulate="tnm", scenario="success")
        assert mock.PROVIDER_NAME == "mock"


class TestPayChanguProvider:
    """Tests for PayChangu provider."""

    def setup_method(self):
        self.secret = "test_webhook_secret"
        self.provider = PayChanguProvider(webhook_secret=self.secret)

    def _make_signature(self, payload: bytes) -> str:
        """Generate valid HMAC-SHA256 signature."""
        return hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()

    def test_verify_signature_valid(self):
        """Test valid signature verification."""
        payload = (
            b'{"event": "payment.completed", "transaction": {"id": "txn_123", "amount": 5000}}'
        )
        signature = self._make_signature(payload)
        assert self.provider.verify_signature(payload, signature) is True

    def test_verify_signature_invalid(self):
        """Test invalid signature raises error."""
        payload = b'{"event": "payment.completed"}'
        invalid_sig = "invalid_signature"
        with pytest.raises(InvalidSignatureError):
            self.provider.verify_signature(payload, invalid_sig)

    def test_verify_signature_missing(self):
        """Test missing signature header raises error."""
        payload = b'{"event": "payment.completed"}'
        with pytest.raises(InvalidSignatureError):
            self.provider.verify_signature(payload, "")

    def test_parse_webhook_completed(self):
        """Parse completed payment webhook."""
        payload = {
            "event": "payment.completed",
            "transaction": {
                "id": "txn_abc123",
                "amount": 5000,
                "currency": "MWK",
                "customer": {"phone": "+265991234567", "email": "test@example.com"},
                "reference": "ORDER-123",
                "metadata": {"task_id": "task_abc"},
                "completed_at": "2024-01-15T10:30:05Z",
            },
        }
        headers = {}
        result = self.provider.parse_webhook(payload, headers)

        assert result.provider == "paychangu"
        assert result.transaction_id == "txn_abc123"
        assert result.amount == Decimal("5000")
        assert result.currency == "MWK"
        assert result.customer_reference == "ORDER-123"
        assert result.payer_phone == "+265991234567"
        assert result.status == "completed"
        assert result.metadata["task_id"] == "task_abc"

    def test_parse_webhook_ignores_non_completed(self):
        """Non-completed events should raise error."""
        payload = {"event": "payment.failed", "transaction": {"id": "txn_123", "amount": 5000}}
        with pytest.raises(ProviderError, match="Unhandled event"):
            self.provider.parse_webhook(payload, {})

    def test_parse_webhook_missing_transaction(self):
        """Missing transaction data raises error."""
        payload = {"event": "payment.completed"}
        with pytest.raises(ProviderError, match="Missing transaction data"):
            self.provider.parse_webhook(payload, {})

    def test_idempotency_key_format(self):
        """Test idempotency key format."""
        key = self.provider.generate_idempotency_key("txn_123")
        assert key == "paychangu:txn_123"

    def test_amount_normalization(self):
        """Test amount normalization for MWK."""
        assert self.provider.normalize_amount(5000, "MWK") == Decimal("5000")
        assert self.provider.normalize_amount("5000.50", "MWK") == Decimal("5001")  # MWK rounds
        assert self.provider.normalize_amount(100.50, "USD") == Decimal("100.50")

    def test_currency_validation(self):
        """Test unsupported currency raises error."""
        with pytest.raises(ProviderError, match="Unsupported currency"):
            self.provider.validate_currency("EUR")


class TestAirtelProvider:
    """Tests for Airtel provider."""

    def setup_method(self):
        self.secret = "test_webhook_secret"
        self.provider = AirtelProvider(webhook_secret=self.secret)

    def _make_signature(self, payload: bytes) -> str:
        return hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()

    def test_verify_signature_valid(self):
        payload = b'{"transaction": {"transaction_id": "airtel_123", "amount": 5000, "status": "SUCCESS"}}'
        signature = self._make_signature(payload)
        assert self.provider.verify_signature(payload, signature) is True

    def test_parse_webhook_success(self):
        payload = {
            "transaction": {
                "transaction_id": "AIRTEL_123456789",
                "amount": "5000.00",
                "currency": "MWK",
                "payer_msisdn": "265991234567",
                "payer_name": "John Doe",
                "reference": "ORDER-123",
                "status": "SUCCESS",
                "timestamp": "2024-01-15T10:30:00Z",
                "external_id": "task_abc",
            }
        }
        result = self.provider.parse_webhook(payload, {})

        assert result.provider == "airtel"
        assert result.transaction_id == "AIRTEL_123456789"
        assert result.amount == Decimal("5000")
        assert result.currency == "MWK"
        assert result.customer_reference == "ORDER-123"
        assert result.payer_phone == "265991234567"
        assert result.metadata["external_id"] == "task_abc"

    def test_parse_webhook_failed_status(self):
        """Failed status should raise error."""
        payload = {
            "transaction": {
                "transaction_id": "airtel_123",
                "amount": "5000",
                "currency": "MWK",
                "status": "FAILED",
            }
        }
        with pytest.raises(ProviderError, match="Transaction not successful"):
            self.provider.parse_webhook(payload, {})

    def test_idempotency_key(self):
        key = self.provider.generate_idempotency_key("airtel_123")
        assert key == "airtel:airtel_123"


class TestTNMProvider:
    """Tests for TNM provider."""

    def setup_method(self):
        self.secret = "test_webhook_secret"
        self.provider = TNMProvider(webhook_secret=self.secret)

    def _make_signature(self, payload: bytes) -> str:
        return hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()

    def test_verify_signature_valid(self):
        payload = b'{"transaction": {"trans_id": "tnm_123", "amount": 5000, "status": "COMPLETED"}}'
        signature = self._make_signature(payload)
        assert self.provider.verify_signature(payload, signature) is True

    def test_parse_webhook_completed(self):
        payload = {
            "transaction": {
                "trans_id": "TNM_987654321",
                "amount": "5000",
                "currency": "MWK",
                "msisdn": "265881234567",
                "customer_name": "Jane Smith",
                "reference": "INV-456",
                "status": "COMPLETED",
                "timestamp": "2024-01-15T10:30:00Z",
                "callback_data": {"task_id": "task_xyz"},
            }
        }
        result = self.provider.parse_webhook(payload, {})

        assert result.provider == "tnm"
        assert result.transaction_id == "TNM_987654321"
        assert result.amount == Decimal("5000")
        assert result.currency == "MWK"
        assert result.payer_phone == "265881234567"
        assert result.metadata["callback_data"]["task_id"] == "task_xyz"

    def test_idempotency_key(self):
        key = self.provider.generate_idempotency_key("tnm_123")
        assert key == "tnm:tnm_123"


class TestMockProvider:
    """Tests for MockProvider with all scenarios."""

    def test_mock_paychangu_success(self):
        """Mock PayChangu success scenario."""
        mock = MockProvider(
            webhook_secret="secret", provider_to_simulate="paychangu", scenario="success"
        )

        payload = {
            "event": "payment.completed",
            "transaction": {
                "id": "mock_txn_123",
                "amount": 5000,
                "currency": "MWK",
                "customer": {"phone": "+265991234567"},
                "reference": "TEST-123",
                "completed_at": "2024-01-15T10:30:00Z",
            },
        }
        result = mock.parse_webhook(payload, {})
        assert result.provider == "paychangu"
        assert result.transaction_id == "mock_txn_123"

    def test_mock_airtel_success(self):
        """Mock Airtel success scenario."""
        mock = MockProvider(
            webhook_secret="secret", provider_to_simulate="airtel", scenario="success"
        )

        payload = {
            "transaction": {
                "transaction_id": "airtel_mock_123",
                "amount": "5000.00",
                "currency": "MWK",
                "payer_msisdn": "265991234567",
                "status": "SUCCESS",
                "timestamp": "2024-01-15T10:30:00Z",
            }
        }
        result = mock.parse_webhook(payload, {})
        assert result.provider == "airtel"
        assert result.transaction_id == "airtel_mock_123"

    def test_mock_tnm_success(self):
        """Mock TNM success scenario."""
        mock = MockProvider(webhook_secret="secret", provider_to_simulate="tnm", scenario="success")

        payload = {
            "transaction": {
                "trans_id": "tnm_mock_123",
                "amount": "5000",
                "currency": "MWK",
                "msisdn": "265881234567",
                "status": "COMPLETED",
                "timestamp": "2024-01-15T10:30:00Z",
            }
        }
        result = mock.parse_webhook(payload, {})
        assert result.provider == "tnm"
        assert result.transaction_id == "tnm_mock_123"

    def test_mock_invalid_signature(self):
        """Mock invalid signature scenario."""
        mock = MockProvider("secret", "paychangu", scenario="invalid_signature")
        with pytest.raises(InvalidSignatureError):
            mock.parse_webhook({}, {"X-Paychangu-Signature": "bad"})

    def test_mock_duplicate_transaction(self):
        """Mock duplicate transaction scenario."""
        mock = MockProvider("secret", "paychangu", scenario="duplicate")

        payload = {
            "event": "payment.completed",
            "transaction": {"id": "dup_txn_123", "amount": 1000, "currency": "MWK"},
        }

        # First call succeeds
        result1 = mock.parse_webhook(payload, {})
        assert result1.transaction_id == "dup_txn_123"

        # Second call raises duplicate error
        with pytest.raises(ProviderError, match="Duplicate transaction"):
            mock.parse_webhook(payload, {})

    def test_mock_timeout(self):
        """Mock timeout scenario."""
        mock = MockProvider("secret", "paychangu", scenario="timeout", delay_ms=100)

        payload = {"event": "payment.completed", "transaction": {"id": "txn", "amount": 1000}}
        with pytest.raises(ProviderError, match="TIMEOUT"):
            mock.parse_webhook(payload, {})

    def test_mock_insufficient_funds(self):
        """Mock insufficient funds scenario."""
        mock = MockProvider("secret", "paychangu", scenario="insufficient_funds")

        payload = {"event": "payment.completed", "transaction": {"id": "txn", "amount": 1000}}
        with pytest.raises(ProviderError, match="INSUFFICIENT_FUNDS"):
            mock.parse_webhook(payload, {})

    def test_mock_invalid_payload(self):
        """Mock invalid payload scenario."""
        mock = MockProvider("secret", "paychangu", scenario="invalid_payload")

        with pytest.raises(ProviderError, match="MALFORMED_PAYLOAD"):
            mock.parse_webhook({}, {})

    def test_mock_signature_verification(self):
        """Mock signature verification works for all providers."""
        for provider_name in ["paychangu", "airtel", "tnm"]:
            mock = MockProvider("secret", provider_name, scenario="success")
            payload = b"test payload"
            sig = hmac.new(b"secret", payload, hashlib.sha256).hexdigest()
            assert mock.verify_signature(payload, sig) is True

    def test_mock_reset_seen_transactions(self):
        """Mock reset clears duplicate tracking."""
        mock = MockProvider("secret", "paychangu", scenario="duplicate")

        payload = {"event": "payment.completed", "transaction": {"id": "dup_123", "amount": 1000}}
        mock.parse_webhook(payload, {})  # First succeeds

        with pytest.raises(ProviderError, match="Duplicate"):
            mock.parse_webhook(payload, {})  # Second fails

        mock.reset_seen_transactions()
        # After reset, should succeed again
        result = mock.parse_webhook(payload, {})
        assert result.transaction_id == "dup_123"


class TestProviderIdempotency:
    """Test idempotency key generation across all providers."""

    @pytest.mark.parametrize(
        "provider_class,expected_prefix",
        [
            (PayChanguProvider, "paychangu:"),
            (AirtelProvider, "airtel:"),
            (TNMProvider, "tnm:"),
        ],
    )
    def test_idempotency_key_format(self, provider_class, expected_prefix):
        provider = provider_class("secret")
        key = provider.generate_idempotency_key("txn_123")
        assert key.startswith(expected_prefix)
        assert key == f"{expected_prefix}txn_123"


class TestProviderCurrencyValidation:
    """Test currency validation across providers."""

    @pytest.mark.parametrize("provider_class", [PayChanguProvider, AirtelProvider, TNMProvider])
    def test_supported_currencies(self, provider_class):
        provider = provider_class("secret")
        assert "MWK" in provider.SUPPORTED_CURRENCIES
        assert "USD" in provider.SUPPORTED_CURRENCIES

    @pytest.mark.parametrize("provider_class", [PayChanguProvider, AirtelProvider, TNMProvider])
    def test_unsupported_currency(self, provider_class):
        provider = provider_class("secret")
        with pytest.raises(ProviderError, match="Unsupported currency"):
            provider.validate_currency("EUR")
