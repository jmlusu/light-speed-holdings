"""Content safety filtering for LLM outputs.

Filters harmful, injected, or malicious content from agent outputs before
they are presented to users or stored in the system.

Security features:
- Prompt injection detection
- Harmful content filtering
- Code execution attempt blocking
- Cross-site scripting (XSS) prevention
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

# Security audit logger
_security_logger = logging.getLogger("ai_company.security.content_filter")


class ThreatLevel(Enum):
    """Severity level of detected content threats."""
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"


@dataclass
class FilterResult:
    """Result of content safety filtering."""
    original: str
    filtered: str
    threat_level: ThreatLevel
    threats_detected: list[str] = field(default_factory=list)
    was_modified: bool = False

    @property
    def is_safe(self) -> bool:
        return self.threat_level == ThreatLevel.SAFE


class ContentFilter:
    """Filters harmful content from LLM outputs.

    Usage:
        content_filter = ContentFilter()
        result = content_filter.scan(agent_output)
        if not result.is_safe:
            log_security_incident(result)
    """

    # Patterns that indicate prompt injection attempts
    INJECTION_PATTERNS: list[re.Pattern] = [
        # Direct instruction overrides
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+instructions?", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)", re.IGNORECASE),
        re.compile(r"forget\s+(everything|all|your\s+instructions?)", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(a|an|the)", re.IGNORECASE),

        # System prompt extraction attempts
        re.compile(r"(show|reveal|display|print|output)\s+(me\s+)?(your|the)\s+(system\s+)?(prompt|instructions?)", re.IGNORECASE),
        re.compile(r"what\s+(are|is)\s+your\s+(system\s+)?(prompt|instructions?)", re.IGNORECASE),
        re.compile(r"repeat\s+(everything|all|your)\s+(above|before|instructions?)", re.IGNORECASE),

        # Role manipulation
        re.compile(r"(act|behave|pretend)\s+(as\s+if|like)\s+you\s+(have|don.t|do\s+not)\s+(have|have\s+any)", re.IGNORECASE),
        re.compile(r"(switch|change)\s+to\s+(debug|admin|root|developer)\s+mode", re.IGNORECASE),

        # Data exfiltration attempts
        re.compile(r"(send|email|post|upload|exfiltrate)\s+(all\s+)?(data|files?|secrets?|keys?|tokens?)", re.IGNORECASE),
        re.compile(r"(curl|wget|fetch)\s+(https?://)", re.IGNORECASE),
    ]

    # Patterns indicating code execution attempts
    EXECUTION_PATTERNS: list[re.Pattern] = [
        re.compile(r"```(bash|sh|shell|powershell|cmd)", re.IGNORECASE),
        re.compile(r"eval\s*\(", re.IGNORECASE),
        re.compile(r"exec\s*\(", re.IGNORECASE),
        re.compile(r"__import__\s*\(", re.IGNORECASE),
        re.compile(r"subprocess\.(run|call|Popen)\s*\(", re.IGNORECASE),
        re.compile(r"os\.system\s*\(", re.IGNORECASE),
    ]

    # XSS/injection patterns
    XSS_PATTERNS: list[re.Pattern] = [
        re.compile(r"<script[^>]*>", re.IGNORECASE),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"on\w+\s*=", re.IGNORECASE),  # onclick=, onerror=, etc.
        re.compile(r"<iframe[^>]*>", re.IGNORECASE),
        re.compile(r"<object[^>]*>", re.IGNORECASE),
        re.compile(r"<embed[^>]*>", re.IGNORECASE),
    ]

    def __init__(
        self,
        block_on_dangerous: bool = True,
        log_threats: bool = True,
    ) -> None:
        self.block_on_dangerous = block_on_dangerous
        self.log_threats = log_threats

    def scan(self, content: str) -> FilterResult:
        """Scan content for safety threats.

        Args:
            content: The text content to scan.

        Returns:
            FilterResult with threat assessment and filtered content.
        """
        threats: list[str] = []
        max_threat = ThreatLevel.SAFE

        # Check for prompt injection
        injection_threats = self._check_injection(content)
        if injection_threats:
            threats.extend(injection_threats)
            max_threat = ThreatLevel.DANGEROUS

        # Check for code execution attempts
        execution_threats = self._check_execution(content)
        if execution_threats:
            threats.extend(execution_threats)
            if max_threat.value < ThreatLevel.DANGEROUS.value:
                max_threat = ThreatLevel.SUSPICIOUS

        # Check for XSS
        xss_threats = self._check_xss(content)
        if xss_threats:
            threats.extend(xss_threats)
            if max_threat.value < ThreatLevel.DANGEROUS.value:
                max_threat = ThreatLevel.SUSPICIOUS

        # Filter content if needed
        filtered = content
        was_modified = False

        if threats and self.block_on_dangerous:
            if max_threat == ThreatLevel.DANGEROUS:
                filtered = "[CONTENT BLOCKED - Security threat detected]"
                was_modified = True
                max_threat = ThreatLevel.BLOCKED

        # Log threats for security auditing
        if threats and self.log_threats:
            _security_logger.warning(
                "Content threats detected: %s | Level: %s | Preview: %s",
                threats,
                max_threat.value,
                content[:100],
            )

        return FilterResult(
            original=content,
            filtered=filtered,
            threat_level=max_threat,
            threats_detected=threats,
            was_modified=was_modified,
        )

    def _check_injection(self, content: str) -> list[str]:
        """Check for prompt injection attempts."""
        threats = []
        for pattern in self.INJECTION_PATTERNS:
            if pattern.search(content):
                threats.append(f"injection:{pattern.pattern[:50]}")
        return threats

    def _check_execution(self, content: str) -> list[str]:
        """Check for code execution attempts."""
        threats = []
        for pattern in self.EXECUTION_PATTERNS:
            if pattern.search(content):
                threats.append(f"execution:{pattern.pattern[:50]}")
        return threats

    def _check_xss(self, content: str) -> list[str]:
        """Check for XSS attempts."""
        threats = []
        for pattern in self.XSS_PATTERNS:
            if pattern.search(content):
                threats.append(f"xss:{pattern.pattern[:50]}")
        return threats

    def sanitize_for_display(self, content: str) -> str:
        """Sanitize content for safe display in HTML contexts.

        Escapes HTML entities and removes potentially dangerous tags.
        """
        # Basic HTML escaping
        content = content.replace("&", "&amp;")
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
        content = content.replace('"', "&quot;")
        content = content.replace("'", "&#x27;")

        return content


# Global instance for convenience
_default_filter: Optional[ContentFilter] = None


def get_content_filter() -> ContentFilter:
    """Get or create the default content filter instance."""
    global _default_filter
    if _default_filter is None:
        _default_filter = ContentFilter()
    return _default_filter


def filter_content(content: str) -> FilterResult:
    """Convenience function to scan content using the default filter."""
    return get_content_filter().scan(content)
