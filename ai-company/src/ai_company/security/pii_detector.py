"""PII (Personally Identifiable Information) detection and masking.

Detects and masks sensitive information in agent outputs including:
- Email addresses
- Social Security Numbers (SSN)
- Credit card numbers
- API keys and tokens
- Phone numbers
- IP addresses

Security features:
- Pattern-based detection with checksum validation
- Configurable masking strategies
- Audit logging for compliance
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

# Security audit logger
_security_logger = logging.getLogger("ai_company.security.pii_detector")


class PIIType(Enum):
    """Types of PII that can be detected."""
    EMAIL = "email"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    API_KEY = "api_key"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    AWS_KEY = "aws_key"
    PRIVATE_KEY = "private_key"


class MaskingStrategy(Enum):
    """Strategy for masking detected PII."""
    FULL = "full"           # Replace entirely with [REDACTED]
    PARTIAL = "partial"     # Show first/last characters
    HASH = "hash"           # Replace with hash
    PLACEHOLDER = "placeholder"  # Replace with type-specific placeholder


@dataclass
class PIIMatch:
    """A detected PII instance."""
    pii_type: PIIType
    value: str
    start: int
    end: int
    confidence: float = 1.0


@dataclass
class DetectionResult:
    """Result of PII detection scan."""
    original: str
    masked: str
    matches: list[PIIMatch] = field(default_factory=list)
    was_modified: bool = False

    @property
    def has_pii(self) -> bool:
        return len(self.matches) > 0

    @property
    def pii_types_found(self) -> set[PIIType]:
        return {m.pii_type for m in self.matches}


class PIIDetector:
    """Detects and masks PII in text content.

    Usage:
        detector = PIIDetector()
        result = detector.scan(text_with_pii)
        safe_output = result.masked
    """

    # Email pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    # SSN pattern (XXX-XX-XXXX or XXXXXXXXX)
    SSN_PATTERN = re.compile(
        r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b"
    )

    # Credit card patterns (major card types)
    CC_PATTERNS = {
        "visa": re.compile(r"\b4\d{3}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
        "mastercard": re.compile(r"\b5[1-5]\d{2}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
        "amex": re.compile(r"\b3[47]\d{2}[- ]?\d{6}[- ]?\d{5}\b"),
        "discover": re.compile(r"\b6(?:011|5\d{2})[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
    }

    # API key patterns
    API_KEY_PATTERNS = {
        "generic": re.compile(r"\b[A-Za-z0-9]{32,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "aws_secret_key": re.compile(r"(?:aws_secret_access_key|secret_key)[=:]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?", re.IGNORECASE),
        "github_token": re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
        "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{48}\b"),
        "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9]{48}\b"),
    }

    # Phone number pattern (US format)
    PHONE_PATTERN = re.compile(
        r"(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}"
    )

    # IP address pattern (IPv4)
    IP_PATTERN = re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    )

    # Private key pattern
    PRIVATE_KEY_PATTERN = re.compile(
        r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"
    )

    def __init__(
        self,
        masking_strategy: MaskingStrategy = MaskingStrategy.PARTIAL,
        detect_emails: bool = True,
        detect_ssn: bool = True,
        detect_credit_cards: bool = True,
        detect_api_keys: bool = True,
        detect_phones: bool = True,
        detect_ips: bool = True,
        log_detections: bool = True,
    ) -> None:
        self.masking_strategy = masking_strategy
        self.detect_emails = detect_emails
        self.detect_ssn = detect_ssn
        self.detect_credit_cards = detect_credit_cards
        self.detect_api_keys = detect_api_keys
        self.detect_phones = detect_phones
        self.detect_ips = detect_ips
        self.log_detections = log_detections

    def scan(self, content: str) -> DetectionResult:
        """Scan content for PII and return masked version.

        Args:
            content: Text content to scan.

        Returns:
            DetectionResult with matches and masked content.
        """
        matches: list[PIIMatch] = []

        # Detect all PII types
        if self.detect_emails:
            matches.extend(self._detect_emails(content))
        if self.detect_ssn:
            matches.extend(self._detect_ssn(content))
        if self.detect_credit_cards:
            matches.extend(self._detect_credit_cards(content))
        if self.detect_api_keys:
            matches.extend(self._detect_api_keys(content))
        if self.detect_phones:
            matches.extend(self._detect_phones(content))
        if self.detect_ips:
            matches.extend(self._detect_ips(content))

        # Always check for private keys
        matches.extend(self._detect_private_keys(content))

        # Sort matches by position (reverse for replacement)
        matches.sort(key=lambda m: m.start, reverse=True)

        # Apply masking
        masked = content
        was_modified = False
        for match in matches:
            replacement = self._mask_value(match)
            masked = masked[:match.start] + replacement + masked[match.end:]
            was_modified = True

        # Log detections for audit
        if matches and self.log_detections:
            pii_types = {m.pii_type.value for m in matches}
            _security_logger.warning(
                "PII detected: %s | Count: %d | Preview: %s",
                pii_types,
                len(matches),
                content[:100],
            )

        # Reverse matches to original positions since we reversed for replacement
        matches.sort(key=lambda m: m.start)

        return DetectionResult(
            original=content,
            masked=masked,
            matches=matches,
            was_modified=was_modified,
        )

    def _detect_emails(self, content: str) -> list[PIIMatch]:
        """Detect email addresses."""
        matches = []
        for match in self.EMAIL_PATTERN.finditer(content):
            # Basic validation - must have @ and valid domain
            email = match.group()
            if self._is_valid_email(email):
                matches.append(PIIMatch(
                    pii_type=PIIType.EMAIL,
                    value=email,
                    start=match.start(),
                    end=match.end(),
                ))
        return matches

    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation."""
        parts = email.split("@")
        if len(parts) != 2:
            return False
        local, domain = parts
        if not local or not domain:
            return False
        if "." not in domain:
            return False
        return True

    def _detect_ssn(self, content: str) -> list[PIIMatch]:
        """Detect Social Security Numbers."""
        matches = []
        for match in self.SSN_PATTERN.finditer(content):
            ssn = match.group()
            # Remove separators for validation
            digits = re.sub(r"[-.]", "", ssn)
            # Basic SSN validation
            if len(digits) == 9 and not digits.startswith("000") and not digits.startswith("666"):
                matches.append(PIIMatch(
                    pii_type=PIIType.SSN,
                    value=ssn,
                    start=match.start(),
                    end=match.end(),
                ))
        return matches

    def _detect_credit_cards(self, content: str) -> list[PIIMatch]:
        """Detect credit card numbers with Luhn validation."""
        matches = []
        for card_type, pattern in self.CC_PATTERNS.items():
            for match in pattern.finditer(content):
                cc = match.group()
                # Remove spaces and dashes for validation
                digits = re.sub(r"[- ]", "", cc)
                # Luhn algorithm check
                if self._luhn_check(digits):
                    matches.append(PIIMatch(
                        pii_type=PIIType.CREDIT_CARD,
                        value=cc,
                        start=match.start(),
                        end=match.end(),
                    ))
        return matches

    def _luhn_check(self, card_number: str) -> bool:
        """Validate credit card number using Luhn algorithm."""
        try:
            digits = [int(d) for d in card_number]
        except ValueError:
            return False

        checksum = 0
        reverse_digits = digits[::-1]
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    def _detect_api_keys(self, content: str) -> list[PIIMatch]:
        """Detect API keys and tokens."""
        matches = []
        for key_type, pattern in self.API_KEY_PATTERNS.items():
            for match in pattern.finditer(content):
                matches.append(PIIMatch(
                    pii_type=PIIType.API_KEY,
                    value=match.group(),
                    start=match.start(),
                    end=match.end(),
                ))
        return matches

    def _detect_phones(self, content: str) -> list[PIIMatch]:
        """Detect phone numbers."""
        matches = []
        for match in self.PHONE_PATTERN.finditer(content):
            phone = match.group()
            # Basic validation - should have 10 digits
            digits = re.sub(r"[^0-9]", "", phone)
            if len(digits) == 10 or (len(digits) == 11 and digits[0] == "1"):
                matches.append(PIIMatch(
                    pii_type=PIIType.PHONE,
                    value=phone,
                    start=match.start(),
                    end=match.end(),
                ))
        return matches

    def _detect_ips(self, content: str) -> list[PIIMatch]:
        """Detect IP addresses."""
        matches = []
        for match in self.IP_PATTERN.finditer(content):
            ip = match.group()
            # Basic validation - each octet 0-255
            parts = ip.split(".")
            if all(0 <= int(p) <= 255 for p in parts):
                matches.append(PIIMatch(
                    pii_type=PIIType.IP_ADDRESS,
                    value=ip,
                    start=match.start(),
                    end=match.end(),
                ))
        return matches

    def _detect_private_keys(self, content: str) -> list[PIIMatch]:
        """Detect private key headers."""
        matches = []
        for match in self.PRIVATE_KEY_PATTERN.finditer(content):
            matches.append(PIIMatch(
                pii_type=PIIType.PRIVATE_KEY,
                value=match.group(),
                start=match.start(),
                end=match.end(),
                confidence=1.0,
            ))
        return matches

    def _mask_value(self, match: PIIMatch) -> str:
        """Apply masking strategy to a detected PII value."""
        if self.masking_strategy == MaskingStrategy.FULL:
            return "[REDACTED]"

        elif self.masking_strategy == MaskingStrategy.PARTIAL:
            return self._partial_mask(match)

        elif self.masking_strategy == MaskingStrategy.HASH:
            return f"[HASH:{hash(match.value) & 0xFFFFFFFF:08X}]"

        elif self.masking_strategy == MaskingStrategy.PLACEHOLDER:
            return self._get_placeholder(match.pii_type)

        return "[REDACTED]"

    def _partial_mask(self, match: PIIMatch) -> str:
        """Show first and last characters with masking in between."""
        value = match.value
        if len(value) <= 4:
            return "****"

        if match.pii_type == PIIType.EMAIL:
            # Mask local part, keep domain
            local, domain = value.split("@", 1)
            if len(local) <= 2:
                masked_local = local[0] + "***"
            else:
                masked_local = local[0] + "***" + local[-1]
            return f"{masked_local}@{domain}"

        elif match.pii_type == PIIType.SSN:
            # Keep last 4
            return f"***-**-{value[-4:]}"

        elif match.pii_type == PIIType.CREDIT_CARD:
            # Keep last 4
            digits = re.sub(r"[- ]", "", value)
            return f"****-****-****-{digits[-4:]}"

        elif match.pii_type == PIIType.API_KEY:
            # Keep first 4 and last 4
            return f"{value[:4]}...{value[-4:]}"

        elif match.pii_type == PIIType.PHONE:
            # Keep last 4
            digits = re.sub(r"[^0-9]", "", value)
            return f"***-***-{digits[-4:]}"

        elif match.pii_type == PIIType.IP_ADDRESS:
            # Mask last two octets
            parts = value.split(".")
            return f"{parts[0]}.{parts[1]}.*.*"

        # Default: keep first and last char
        return value[0] + "*" * (len(value) - 2) + value[-1]

    def _get_placeholder(self, pii_type: PIIType) -> str:
        """Get type-specific placeholder."""
        placeholders = {
            PIIType.EMAIL: "[EMAIL]",
            PIIType.SSN: "[SSN]",
            PIIType.CREDIT_CARD: "[CREDIT_CARD]",
            PIIType.API_KEY: "[API_KEY]",
            PIIType.PHONE: "[PHONE]",
            PIIType.IP_ADDRESS: "[IP_ADDRESS]",
            PIIType.AWS_KEY: "[AWS_KEY]",
            PIIType.PRIVATE_KEY: "[PRIVATE_KEY]",
        }
        return placeholders.get(pii_type, "[REDACTED]")


# Global instance for convenience
_default_detector: Optional[PIIDetector] = None


def get_pii_detector() -> PIIDetector:
    """Get or create the default PII detector instance."""
    global _default_detector
    if _default_detector is None:
        _default_detector = PIIDetector()
    return _default_detector


def detect_and_mask_pii(content: str) -> DetectionResult:
    """Convenience function to detect and mask PII using the default detector."""
    return get_pii_detector().scan(content)
