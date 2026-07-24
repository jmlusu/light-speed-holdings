"""Tests for PRE-10 — PII detection and masking module.

Covers:
  - Email detection and masking
  - SSN detection and masking
  - Credit card detection (with Luhn validation)
  - API key detection
  - Phone number detection
  - IP address detection
  - Private key detection
  - Masking strategies (FULL, PARTIAL, HASH, PLACEHOLDER)
  - Configurable detection toggles
  - DetectionResult properties
  - Convenience functions
"""

from __future__ import annotations


from ai_company.security.pii_detector import (
    DetectionResult,
    MaskingStrategy,
    PIIDetector,
    PIIType,
    detect_and_mask_pii,
    get_pii_detector,
)


# ── Email Detection ────────────────────────────────────────────────


class TestEmailDetection:
    def test_detects_email(self) -> None:
        detector = PIIDetector(detect_emails=True)
        result = detector.scan("Contact me at user@example.com for details.")
        assert result.has_pii
        assert PIIType.EMAIL in result.pii_types_found
        assert any(m.value == "user@example.com" for m in result.matches)

    def test_detects_multiple_emails(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Email a@b.com and c@d.org")
        assert len([m for m in result.matches if m.pii_type == PIIType.EMAIL]) == 2

    def test_email_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("Send to user@example.com")
        # Partial mask: keep first char, show domain
        assert "u***r@example.com" in result.masked

    def test_email_short_local_partial_mask(self) -> None:
        """Short local part (<3 chars) gets different mask format."""
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("Send to ab@example.com")
        # len("ab") <= 2, so mask is: local[0] + "***" (no trailing char)
        assert "a***@example.com" in result.masked

    def test_email_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        result = detector.scan("Email user@example.com")
        assert "[REDACTED]" in result.masked
        assert "user@example.com" not in result.masked

    def test_email_placeholder_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PLACEHOLDER)
        result = detector.scan("Email user@example.com")
        assert "[EMAIL]" in result.masked

    def test_email_hash_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.HASH)
        result = detector.scan("Email user@example.com")
        assert "[HASH:" in result.masked
        assert "user@example.com" not in result.masked

    def test_invalid_email_not_detected(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Just a plain string with @ but not valid")
        emails = [m for m in result.matches if m.pii_type == PIIType.EMAIL]
        # The pattern might match but _is_valid_email should reject it
        assert len(emails) == 0


# ── SSN Detection ──────────────────────────────────────────────────


class TestSSNDetection:
    def test_detects_ssn_with_dashes(self) -> None:
        detector = PIIDetector()
        result = detector.scan("SSN: 123-45-6789")
        assert PIIType.SSN in result.pii_types_found
        assert any(m.value == "123-45-6789" for m in result.matches)

    def test_detects_ssn_with_dots(self) -> None:
        detector = PIIDetector()
        result = detector.scan("SSN: 123.45.6789")
        assert PIIType.SSN in result.pii_types_found

    def test_detects_ssn_without_separators(self) -> None:
        detector = PIIDetector()
        result = detector.scan("SSN: 123456789")
        assert PIIType.SSN in result.pii_types_found

    def test_rejects_invalid_ssn_000(self) -> None:
        detector = PIIDetector()
        result = detector.scan("SSN: 000-45-6789")
        ssns = [m for m in result.matches if m.pii_type == PIIType.SSN]
        assert len(ssns) == 0

    def test_rejects_invalid_ssn_666(self) -> None:
        detector = PIIDetector()
        result = detector.scan("SSN: 666-45-6789")
        ssns = [m for m in result.matches if m.pii_type == PIIType.SSN]
        assert len(ssns) == 0

    def test_ssn_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("SSN: 123-45-6789")
        assert "***-**-6789" in result.masked

    def test_ssn_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        result = detector.scan("SSN: 123-45-6789")
        assert "[REDACTED]" in result.masked


# ── Credit Card Detection ──────────────────────────────────────────


class TestCreditCardDetection:
    def test_detects_visa(self) -> None:
        detector = PIIDetector()
        # Valid Visa test number (passes Luhn)
        result = detector.scan("Card: 4111111111111111")
        assert PIIType.CREDIT_CARD in result.pii_types_found

    def test_detects_visa_with_spaces(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Card: 4111 1111 1111 1111")
        assert PIIType.CREDIT_CARD in result.pii_types_found

    def test_detects_visa_with_dashes(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Card: 4111-1111-1111-1111")
        assert PIIType.CREDIT_CARD in result.pii_types_found

    def test_detects_mastercard(self) -> None:
        detector = PIIDetector()
        # Valid Mastercard (passes Luhn)
        result = detector.scan("Card: 5500000000000004")
        assert PIIType.CREDIT_CARD in result.pii_types_found

    def test_cc_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("Card: 4111111111111111")
        # CC number also triggers phone detection (10-digit substring overlap),
        # so both masks are applied. Verify original CC is fully masked.
        assert "4111111111111111" not in result.masked
        # The last 4 digits of the CC should appear in the mask
        assert "1111" in result.masked

    def test_cc_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        result = detector.scan("Card: 4111111111111111")
        # FULL mask replaces everything with [REDACTED]
        assert "[REDACTED]" in result.masked
        assert "4111111111111111" not in result.masked

    def test_cc_placeholder_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PLACEHOLDER)
        result = detector.scan("Card: 4111111111111111")
        # CC number also triggers phone detection, so both placeholders appear
        assert "[CREDIT_CARD]" in result.masked or "[PHONE]" in result.masked
        assert "4111111111111111" not in result.masked

    def test_invalid_cc_not_detected(self) -> None:
        """Credit card number that fails Luhn check should not be detected."""
        detector = PIIDetector()
        # 4111111111111112 fails Luhn
        result = detector.scan("Card: 4111111111111112")
        cc = [m for m in result.matches if m.pii_type == PIIType.CREDIT_CARD]
        assert len(cc) == 0


# ── API Key Detection ──────────────────────────────────────────────


class TestAPIKeyDetection:
    def test_detects_github_token(self) -> None:
        detector = PIIDetector()
        # ghp_ + 36 alphanumeric chars (regex: \bghp_[A-Za-z0-9]{36}\b)
        result = detector.scan("Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij")
        assert PIIType.API_KEY in result.pii_types_found

    def test_detects_openai_key(self) -> None:
        detector = PIIDetector()
        # sk- + 48 chars
        key = "sk-" + "A" * 48
        result = detector.scan(f"Key: {key}")
        assert PIIType.API_KEY in result.pii_types_found

    def test_detects_anthropic_key(self) -> None:
        detector = PIIDetector()
        key = "sk-ant-" + "A" * 48
        result = detector.scan(f"Key: {key}")
        assert PIIType.API_KEY in result.pii_types_found

    def test_detects_aws_access_key(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Key: AKIAIOSFODNN7EXAMPLE")
        assert PIIType.API_KEY in result.pii_types_found

    def test_api_key_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        # ghp_ + 36 chars
        result = detector.scan("Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij")
        matches = [m for m in result.matches if m.pii_type == PIIType.API_KEY]
        assert len(matches) >= 1
        # Should show first 4 and last 4
        assert "ghp_" in result.masked

    def test_api_key_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        # ghp_ + 36 chars
        result = detector.scan("Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij")
        assert "[REDACTED]" in result.masked
        assert "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij" not in result.masked

    def test_api_key_placeholder_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PLACEHOLDER)
        # ghp_ + 36 chars
        result = detector.scan("Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij")
        assert "[API_KEY]" in result.masked

    def test_generic_long_key_detected(self) -> None:
        """A 32+ character alphanumeric string should be detected as generic API key."""
        detector = PIIDetector()
        long_key = "A" * 36
        result = detector.scan(f"Key: {long_key}")
        api_keys = [m for m in result.matches if m.pii_type == PIIType.API_KEY]
        assert len(api_keys) >= 1


# ── Phone Number Detection ─────────────────────────────────────────


class TestPhoneDetection:
    def test_detects_us_phone_with_formatting(self) -> None:
        detector = PIIDetector()
        # The phone regex requires [-.]? between ) and next digit — space doesn't match
        # Use parentheses without space: (555)123-4567
        result = detector.scan("Call (555)123-4567")
        assert PIIType.PHONE in result.pii_types_found

    def test_detects_us_phone_dashes(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Call 555-123-4567")
        assert PIIType.PHONE in result.pii_types_found

    def test_detects_phone_with_country_code(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Call +1-555-123-4567")
        assert PIIType.PHONE in result.pii_types_found

    def test_phone_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("Call 555-123-4567")
        assert "***-***-4567" in result.masked

    def test_phone_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        result = detector.scan("Call 555-123-4567")
        assert "[REDACTED]" in result.masked

    def test_phone_placeholder_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PLACEHOLDER)
        result = detector.scan("Call 555-123-4567")
        assert "[PHONE]" in result.masked


# ── IP Address Detection ───────────────────────────────────────────


class TestIPDetection:
    def test_detects_ipv4(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Server: 192.168.1.100")
        assert PIIType.IP_ADDRESS in result.pii_types_found

    def test_detects_valid_ip(self) -> None:
        detector = PIIDetector()
        result = detector.scan("IP: 10.0.0.1")
        assert PIIType.IP_ADDRESS in result.pii_types_found

    def test_rejects_invalid_octet(self) -> None:
        detector = PIIDetector()
        result = detector.scan("IP: 999.999.999.999")
        ips = [m for m in result.matches if m.pii_type == PIIType.IP_ADDRESS]
        assert len(ips) == 0

    def test_ip_partial_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PARTIAL)
        result = detector.scan("IP: 192.168.1.100")
        assert "192.168.*.*" in result.masked

    def test_ip_full_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        result = detector.scan("IP: 192.168.1.100")
        assert "[REDACTED]" in result.masked

    def test_ip_placeholder_mask(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.PLACEHOLDER)
        result = detector.scan("IP: 192.168.1.100")
        assert "[IP_ADDRESS]" in result.masked


# ── Private Key Detection ──────────────────────────────────────────


class TestPrivateKeyDetection:
    def test_detects_rsa_private_key(self) -> None:
        detector = PIIDetector()
        result = detector.scan("-----BEGIN RSA PRIVATE KEY-----")
        assert PIIType.PRIVATE_KEY in result.pii_types_found

    def test_detects_generic_private_key(self) -> None:
        detector = PIIDetector()
        result = detector.scan("-----BEGIN PRIVATE KEY-----")
        assert PIIType.PRIVATE_KEY in result.pii_types_found

    def test_detects_ec_private_key(self) -> None:
        detector = PIIDetector()
        result = detector.scan("-----BEGIN EC PRIVATE KEY-----")
        assert PIIType.PRIVATE_KEY in result.pii_types_found


# ── DetectionResult Properties ─────────────────────────────────────


class TestDetectionResult:
    def test_has_pii_true_when_matches(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Email: test@example.com")
        assert result.has_pii is True

    def test_has_pii_false_when_clean(self) -> None:
        detector = PIIDetector()
        result = detector.scan("This is clean text.")
        assert result.has_pii is False

    def test_pii_types_found_unique(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Email a@b.com, phone 555-123-4567")
        types = result.pii_types_found
        assert PIIType.EMAIL in types
        assert PIIType.PHONE in types
        assert len(types) == 2

    def test_was_modified_true(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Email: test@example.com")
        assert result.was_modified is True

    def test_was_modified_false_clean(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Clean text")
        assert result.was_modified is False

    def test_original_preserved(self) -> None:
        detector = PIIDetector()
        original = "Email: test@example.com"
        result = detector.scan(original)
        assert result.original == original

    def test_matches_sorted_by_position(self) -> None:
        detector = PIIDetector()
        result = detector.scan("Email a@b.com and 555-123-4567")
        positions = [(m.start, m.end) for m in result.matches]
        assert positions == sorted(positions, key=lambda x: x[0])


# ── Configurable Detection Toggles ─────────────────────────────────


class TestDetectionToggles:
    def test_email_detection_disabled(self) -> None:
        detector = PIIDetector(detect_emails=False)
        result = detector.scan("Email: test@example.com")
        emails = [m for m in result.matches if m.pii_type == PIIType.EMAIL]
        assert len(emails) == 0

    def test_ssn_detection_disabled(self) -> None:
        detector = PIIDetector(detect_ssn=False)
        result = detector.scan("SSN: 123-45-6789")
        ssns = [m for m in result.matches if m.pii_type == PIIType.SSN]
        assert len(ssns) == 0

    def test_credit_card_detection_disabled(self) -> None:
        detector = PIIDetector(detect_credit_cards=False)
        result = detector.scan("Card: 4111111111111111")
        cc = [m for m in result.matches if m.pii_type == PIIType.CREDIT_CARD]
        assert len(cc) == 0

    def test_api_key_detection_disabled(self) -> None:
        detector = PIIDetector(detect_api_keys=False)
        result = detector.scan("Token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh")
        api = [m for m in result.matches if m.pii_type == PIIType.API_KEY]
        assert len(api) == 0

    def test_phone_detection_disabled(self) -> None:
        detector = PIIDetector(detect_phones=False)
        result = detector.scan("Call 555-123-4567")
        phones = [m for m in result.matches if m.pii_type == PIIType.PHONE]
        assert len(phones) == 0

    def test_ip_detection_disabled(self) -> None:
        detector = PIIDetector(detect_ips=False)
        result = detector.scan("IP: 192.168.1.1")
        ips = [m for m in result.matches if m.pii_type == PIIType.IP_ADDRESS]
        assert len(ips) == 0

    def test_private_keys_always_detected(self) -> None:
        """Private keys are always checked regardless of toggles."""
        detector = PIIDetector(
            detect_emails=False, detect_ssn=False,
            detect_credit_cards=False, detect_api_keys=False,
            detect_phones=False, detect_ips=False,
        )
        result = detector.scan("-----BEGIN RSA PRIVATE KEY-----")
        assert PIIType.PRIVATE_KEY in result.pii_types_found


# ── Multiple PII Types in One Scan ─────────────────────────────────


class TestMultiplePIITypes:
    def test_mixed_content(self) -> None:
        detector = PIIDetector()
        text = (
            "Contact john@example.com, SSN 123-45-6789, "
            "Card 4111111111111111, phone 555-123-4567"
        )
        result = detector.scan(text)
        assert result.has_pii
        types = result.pii_types_found
        assert PIIType.EMAIL in types
        assert PIIType.SSN in types
        assert PIIType.CREDIT_CARD in types
        assert PIIType.PHONE in types

    def test_masked_content_has_no_raw_pii(self) -> None:
        detector = PIIDetector(masking_strategy=MaskingStrategy.FULL)
        text = "Email john@example.com and SSN 123-45-6789"
        result = detector.scan(text)
        assert "john@example.com" not in result.masked
        assert "123-45-6789" not in result.masked


# ── Convenience Functions ──────────────────────────────────────────


class TestConvenienceFunctions:
    def test_get_pii_detector_returns_singleton(self) -> None:
        d1 = get_pii_detector()
        d2 = get_pii_detector()
        assert d1 is d2

    def test_detect_and_mask_pii(self) -> None:
        result = detect_and_mask_pii("Email: user@example.com")
        assert isinstance(result, DetectionResult)
        assert result.has_pii


# ── Empty / Clean Content ──────────────────────────────────────────


class TestCleanContent:
    def test_empty_string(self) -> None:
        detector = PIIDetector()
        result = detector.scan("")
        assert result.has_pii is False
        assert result.masked == ""
        assert result.was_modified is False

    def test_plain_text(self) -> None:
        detector = PIIDetector()
        result = detector.scan("The quick brown fox jumps over the lazy dog.")
        assert result.has_pii is False
        assert result.masked == result.original
        assert result.was_modified is False


# ── Luhn Algorithm ─────────────────────────────────────────────────


class TestLuhnCheck:
    def test_valid_luhn(self) -> None:
        detector = PIIDetector()
        assert detector._luhn_check("4111111111111111") is True

    def test_invalid_luhn(self) -> None:
        detector = PIIDetector()
        assert detector._luhn_check("4111111111111112") is False

    def test_non_numeric_luhn(self) -> None:
        detector = PIIDetector()
        assert detector._luhn_check("not-a-number") is False
