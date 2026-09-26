"""Classification Layer — Four-Tier Classification System.

Implements architecture §7: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
with inheritance rules, auto-classification, and human override.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class Classification(str, Enum):
    """Four-tier classification (architecture §7, locked decision 3)."""

    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"

    @classmethod
    def from_string(cls, value: str) -> "Classification":
        """Parse classification from string (case-insensitive)."""
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.INTERNAL  # Default

    def level(self) -> int:
        """Return numeric level for comparison (higher = more sensitive)."""
        levels = {
            Classification.PUBLIC: 0,
            Classification.INTERNAL: 1,
            Classification.CONFIDENTIAL: 2,
            Classification.RESTRICTED: 3,
        }
        return levels[self]

    def egress_default(self) -> bool:
        """Default egress permission (all blocked by default per architecture §7)."""
        return False


@dataclass(frozen=True)
class ClassificationRule:
    """Rule for automatic classification."""

    pattern: str
    classification: Classification
    confidence: float
    description: str


# Default classification rules (architecture §7)
DEFAULT_RULES: List[ClassificationRule] = [
    ClassificationRule(
        pattern=r"(?i)\b(password|secret|api[_-]?key|token|credential)\b",
        classification=Classification.RESTRICTED,
        confidence=0.9,
        description="Explicit secret keywords",
    ),
    ClassificationRule(
        pattern=r"(?i)\b(confidential|proprietary|internal only|not for distribution)\b",
        classification=Classification.CONFIDENTIAL,
        confidence=0.8,
        description="Confidential markings",
    ),
    ClassificationRule(
        pattern=r"(?i)\b(public|published|open source|mit license|apache license)\b",
        classification=Classification.PUBLIC,
        confidence=0.7,
        description="Public release indicators",
    ),
]


class ClassificationLayer:
    """
    Classification layer per architecture §7.

    - Four tiers: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    - Restricted never plaintext (locked decision 3)
    - Auto-classification with human override (upgrade only past scanner hit)
    - Inheritance: child chunks inherit parent classification (upgrade only)
    """

    def __init__(self, rules: Optional[List[ClassificationRule]] = None):
        self.rules = rules or DEFAULT_RULES

    def classify(self, content: str, current: Optional[Classification] = None) -> Classification:
        """
        Auto-classify content based on rules.

        Args:
            content: Text to classify
            current: Current classification (for override logic)

        Returns:
            Determined classification
        """
        # Start with current or default
        result = current or Classification.INTERNAL

        # Apply rules — take maximum classification
        for rule in self.rules:
            import re

            if re.search(rule.pattern, content) and rule.classification.level() > result.level():
                result = rule.classification

        return result

    def can_downgrade(
        self, current: Classification, proposed: Classification, scanner_hit_restricted: bool
    ) -> bool:
        """
        Check if downgrade is allowed (architecture §7, threat T06 residual).

        Never downgrade past a scanner hit on RESTRICTED content.
        """
        if scanner_hit_restricted and proposed.level() < Classification.RESTRICTED.level():
            return False
        return proposed.level() <= current.level()

    def inherit_classification(
        self, parent: Classification, child: Classification
    ) -> Classification:
        """
        Inherit classification from parent to child (architecture §13.2).

        Child inherits parent's classification at minimum (upgrade only).
        """
        if child.level() < parent.level():
            return parent
        return child

    def egress_permitted(
        self, classification: Classification, gateway_config: dict[str, Any]
    ) -> bool:
        """
        Check if egress is permitted for classification (architecture §9).

        Checks gateway config data_classes_allowed.
        """
        allowed = gateway_config.get("data_classes_allowed", {})
        return bool(allowed.get(classification.value.lower(), False))


def propagate_classification(parent: Classification, child: Classification) -> Classification:
    """Module-level convenience function for classification inheritance."""
    return ClassificationLayer().inherit_classification(parent, child)
