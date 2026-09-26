"""Secret Scanner with Canonical Redaction Token.

Implements the LS-MEM secret scanner per architecture §8 and threat model T01–T04, T26.
Wraps the existing PIIDetector to emit [REDACTED_SECRET] as the canonical token.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Pattern

from ..security.pii_detector import PIIDetector

# Canonical redaction tokens (locked decision 4; threat model §4.2)
REDACTION_TOKEN = "[REDACTED_SECRET]"
LEGACY_REDACTION_TOKEN = "[REDACTED]"


class SecretType(Enum):
    """Types of secrets detected."""

    API_KEY = "api_key"
    ACCESS_TOKEN = "access_token"
    PASSWORD = "password"
    JWT = "jwt"
    PRIVATE_KEY = "private_key"
    CLOUD_CREDENTIAL = "cloud_credential"
    OAUTH_TOKEN = "oauth_token"
    DATABASE_URL = "database_url"
    ENV_SECRET = "env_secret"
    GITHUB_TOKEN = "github_token"
    SSH_KEY = "ssh_key"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SecretMatch:
    """A detected secret match."""

    secret_type: SecretType
    pattern_name: str
    start: int
    end: int
    matched_text: str
    confidence: float  # 0.0–1.0


@dataclass(frozen=True)
class ScanResult:
    """Result of scanning content for secrets."""

    original: str
    redacted: str
    matches: List[SecretMatch]
    has_restricted: bool
    classification_upgrade: Optional[str] = None  # "RESTRICTED" if any high-confidence hit


class SecretScanner:
    """
    Secret scanner that wraps PIIDetector and adds LS-MEM specific patterns.

    Emits [REDACTED_SECRET] as the canonical redaction token (locked decision 4).
    Accepts [REDACTED] as legacy alias on read (threat model §4.2).
    """

    # Extended patterns beyond PIIDetector (architecture §8)
    EXTENDED_PATTERNS: List[tuple[SecretType, str, Pattern[str]]] = [
        # API keys (various providers)
        (SecretType.API_KEY, "sk_live", re.compile(r"\bsk_live_[a-zA-Z0-9]{24,}\b")),
        (SecretType.API_KEY, "sk_test", re.compile(r"\bsk_test_[a-zA-Z0-9]{24,}\b")),
        (SecretType.API_KEY, "generic_bearer", re.compile(r"\bBearer\s+[a-zA-Z0-9._-]{20,}\b")),
        (
            SecretType.API_KEY,
            "generic_api_key",
            re.compile(r"\bapi[_-]?key[_-]?['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9._-]{20,}['\"]?"),
        ),
        # AWS
        (SecretType.CLOUD_CREDENTIAL, "aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        (SecretType.CLOUD_CREDENTIAL, "aws_secret_key", re.compile(r"\b[0-9a-zA-Z/+=]{40}\b")),
        # GCP
        (
            SecretType.CLOUD_CREDENTIAL,
            "gcp_service_account",
            re.compile(r"\"type\":\s*\"service_account\""),
        ),
        # Azure
        (
            SecretType.CLOUD_CREDENTIAL,
            "azure_client_secret",
            re.compile(
                r"\bazure[_-]?client[_-]?secret['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9._-]{20,}['\"]?"
            ),
        ),
        # GitHub
        (SecretType.GITHUB_TOKEN, "github_pat", re.compile(r"\bghp_[a-zA-Z0-9]{36}\b")),
        (SecretType.GITHUB_TOKEN, "github_oauth", re.compile(r"\bgho_[a-zA-Z0-9]{36}\b")),
        (SecretType.GITHUB_TOKEN, "github_app", re.compile(r"\bghs_[a-zA-Z0-9]{36}\b")),
        # Database URLs
        (
            SecretType.DATABASE_URL,
            "postgres_url",
            re.compile(r"postgres(?:ql)?://[^:\s]+:[^@\s]+@[^/\s]+/\w+"),
        ),
        (SecretType.DATABASE_URL, "mysql_url", re.compile(r"mysql://[^:\s]+:[^@\s]+@[^/\s]+/\w+")),
        (
            SecretType.DATABASE_URL,
            "mongodb_url",
            re.compile(r"mongodb://[^:\s]+:[^@\s]+@[^/\s]+/\w+"),
        ),
        # .env secrets
        (
            SecretType.ENV_SECRET,
            "env_assignment",
            re.compile(r"^[A-Z_]+_?(?:KEY|SECRET|TOKEN|PASSWORD|PASS)\s*=\s*[^\s#]+", re.MULTILINE),
        ),
        # JWT
        (
            SecretType.JWT,
            "jwt_token",
            re.compile(r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"),
        ),
        # Private keys (PEM)
        (
            SecretType.PRIVATE_KEY,
            "rsa_private_key",
            re.compile(
                r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
            ),
        ),
        (
            SecretType.PRIVATE_KEY,
            "ssh_private_key",
            re.compile(
                r"-----BEGIN OPENSSH PRIVATE KEY-----[\s\S]*?-----END OPENSSH PRIVATE KEY-----"
            ),
        ),
        # SSH
        (
            SecretType.SSH_KEY,
            "ssh_rsa_pub",
            re.compile(r"\bssh-rsa\s+[A-Za-z0-9+/]+[=]{0,3}\s+\S+@\S+"),
        ),
        (
            SecretType.SSH_KEY,
            "ssh_ed25519_pub",
            re.compile(r"\bssh-ed25519\s+[A-Za-z0-9+/]+[=]{0,3}\s+\S+@\S+"),
        ),
        # OAuth tokens
        (SecretType.OAUTH_TOKEN, "google_oauth", re.compile(r"\bya29\.[a-zA-Z0-9_-]+\b")),
        (SecretType.OAUTH_TOKEN, "slack_bot", re.compile(r"\bxoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+\b")),
        (SecretType.OAUTH_TOKEN, "slack_user", re.compile(r"\bxoxp-[0-9]+-[0-9]+-[a-zA-Z0-9]+\b")),
        # Generic password in code
        (
            SecretType.PASSWORD,
            "password_assignment",
            re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE),
        ),
    ]

    # High-confidence patterns that force RESTRICTED classification
    HIGH_CONFIDENCE_TYPES = {
        SecretType.PRIVATE_KEY,
        SecretType.SSH_KEY,
    }

    def __init__(self, pii_detector: Optional[PIIDetector] = None):
        """
        Initialize the secret scanner.

        Args:
            pii_detector: Optional existing PIIDetector instance. If None, creates a new one.
        """
        self.pii_detector = pii_detector or PIIDetector()
        self._compiled_patterns = self.EXTENDED_PATTERNS

    def scan(self, content: str) -> ScanResult:
        """
        Scan content for secrets.

        Args:
            content: Text to scan.

        Returns:
            ScanResult with redacted content and match details.
        """
        if not content:
            return ScanResult(
                original=content,
                redacted=content,
                matches=[],
                has_restricted=False,
            )

        matches: List[SecretMatch] = []
        redacted = content

        # 1. Run PIIDetector (existing patterns) - uses scan() method returning DetectionResult
        pii_result = self.pii_detector.scan(content)
        for pii_match in pii_result.matches:
            # pii_match is a PIIMatch with: pii_type, value, start, end, confidence
            secret_type = self._map_pii_to_secret_type(pii_match.pii_type.value)
            matches.append(
                SecretMatch(
                    secret_type=secret_type,
                    pattern_name=pii_match.pii_type.value,
                    start=pii_match.start,
                    end=pii_match.end,
                    matched_text=pii_match.value,
                    confidence=pii_match.confidence,
                )
            )

        # 2. Run extended patterns
        for secret_type, pattern_name, pattern in self._compiled_patterns:
            for m in pattern.finditer(content):
                matched = m.group(0)
                confidence = self._compute_confidence(secret_type, matched)
                matches.append(
                    SecretMatch(
                        secret_type=secret_type,
                        pattern_name=pattern_name,
                        start=m.start(),
                        end=m.end(),
                        matched_text=matched,
                        confidence=confidence,
                    )
                )

        # 3. Sort matches by position (descending) for non-overlapping redaction
        # Deduplicate overlapping matches first - keep highest confidence
        # For equal confidence, prefer longer match (full PEM blocks over headers)
        matches.sort(key=lambda m: (m.start, -m.end, -m.confidence))
        deduped: List[SecretMatch] = []
        for match in matches:
            if not deduped:
                deduped.append(match)
            else:
                last = deduped[-1]
                # Check for overlap
                if match.start < last.end:
                    # Overlapping - keep the one with higher confidence
                    # For equal confidence, prefer longer match (full PEM blocks over headers)
                    if match.confidence > last.confidence or (
                        match.confidence == last.confidence
                        and (match.end - match.start) > (last.end - last.start)
                    ):
                        deduped[-1] = match
                else:
                    deduped.append(match)
        matches = deduped

        # 4. Apply redaction using descending start positions for correct indexing
        matches.sort(key=lambda m: m.start, reverse=True)
        redacted = content
        has_restricted = False
        for match in matches:
            if match.confidence >= 0.8:
                replacement = REDACTION_TOKEN
                has_restricted = True
            else:
                replacement = REDACTION_TOKEN
            # Use original content indices since we're building from end
            redacted = redacted[: match.start] + replacement + redacted[match.end :]

        # 5. Determine classification upgrade
        classification_upgrade = "RESTRICTED" if has_restricted else None

        return ScanResult(
            original=content,
            redacted=redacted,
            matches=matches,
            has_restricted=has_restricted,
            classification_upgrade=classification_upgrade,
        )

    def scan_and_classify(
        self, content: str, current_classification: str = "INTERNAL"
    ) -> tuple[str, str]:
        """
        Scan content and return (redacted_content, upgraded_classification).

        Args:
            content: Text to scan.
            current_classification: Current classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED).

        Returns:
            Tuple of (redacted_content, final_classification).
        """
        result = self.scan(content)
        if result.classification_upgrade == "RESTRICTED":
            return result.redacted, "RESTRICTED"
        return result.redacted, current_classification

    def _map_pii_to_secret_type(self, pii_pattern: str) -> SecretType:
        """Map PIIDetector pattern name to SecretType."""
        mapping = {
            "api_key": SecretType.API_KEY,
            "private_key": SecretType.PRIVATE_KEY,
            "aws_access_key": SecretType.CLOUD_CREDENTIAL,
            "github_token": SecretType.GITHUB_TOKEN,
            "jwt": SecretType.JWT,
            "password": SecretType.PASSWORD,
        }
        return mapping.get(pii_pattern, SecretType.UNKNOWN)

    def _compute_confidence(self, secret_type: SecretType, matched: str) -> float:
        """Compute confidence score for a match."""
        # High confidence for structured secrets
        # Full PEM blocks get 1.0 to beat PIIDetector's header-only matches
        if secret_type in (SecretType.PRIVATE_KEY, SecretType.SSH_KEY):
            if matched.strip().startswith("-----BEGIN") and "-----END" in matched:
                return 1.0  # Full PEM block - highest confidence
            return 0.95
        if secret_type == SecretType.JWT:
            return 0.95
        if secret_type in (
            SecretType.API_KEY,
            SecretType.GITHUB_TOKEN,
            SecretType.CLOUD_CREDENTIAL,
        ):
            return 0.9
        if secret_type in (SecretType.DATABASE_URL, SecretType.OAUTH_TOKEN):
            return 0.85
        if secret_type == SecretType.ENV_SECRET:
            return 0.75
        if secret_type == SecretType.PASSWORD:
            return 0.7
        return 0.6

    @staticmethod
    def normalize_redaction(text: str) -> str:
        """
        Normalize legacy redaction tokens to canonical form.

        Args:
            text: Text that may contain [REDACTED] legacy tokens.

        Returns:
            Text with [REDACTED] replaced by [REDACTED_SECRET].
        """
        return text.replace(LEGACY_REDACTION_TOKEN, REDACTION_TOKEN)

    @staticmethod
    def is_redacted(text: str) -> bool:
        """Check if text contains a redaction token (canonical or legacy)."""
        return REDACTION_TOKEN in text or LEGACY_REDACTION_TOKEN in text


def scan_content(content: str) -> ScanResult:
    """Convenience function to scan content with default scanner."""
    scanner = SecretScanner()
    return scanner.scan(content)


def redact_content(content: str) -> str:
    """Convenience function to redact content with default scanner."""
    return scan_content(content).redacted
