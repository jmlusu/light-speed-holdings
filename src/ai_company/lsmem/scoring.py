"""Memory Scoring and Tier Routing.

Implements value score 0–5 and tier routing per architecture §1, §13, ADR-019.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, List, Optional


class Tier(IntEnum):
    """Memory quality tiers (architecture §1, ADR-019)."""

    DISCARDED = 0  # Score 0–1: not persisted
    TIER_1 = 1  # Score 2: basic persistence, default TTL
    TIER_2 = 2  # Score 3–4: extended TTL (+50%), higher injection priority
    TIER_3 = 3  # Score 5: infinite TTL, pinned, human-verified (verified_by required)
    TIER_4 = 4  # Score 6+: exceptional quality, permanent retention
    TIER_5 = 5  # Score 7+: exceptional quality, permanent retention


@dataclass(frozen=True)
class ScoreBreakdown:
    """Detailed score breakdown for transparency."""

    content_length_score: int  # 0–2 based on length
    confidence_score: int  # 0–2 based on confidence
    classification_bonus: int  # 0–1 for RESTRICTED/CONFIDENTIAL
    provenance_bonus: int  # 0–1 for human-verified source
    total: int  # 0–5 final score
    tier: Tier


class MemoryScorer:
    """
    Computes value score 0–5 for memory records.

    Scoring factors (architecture §1, ADR-019, handoff §17):
    - Content length (substantive vs trivial)
    - Confidence (agent-assessed reliability)
    - Classification (sensitive content = higher value)
    - Provenance (human-verified > agent > system)
    """

    # Minimum content length for each score tier
    LENGTH_THRESHOLDS = {
        0: 0,  # < 50 chars
        1: 50,  # 50–199 chars
        2: 200,  # 200–499 chars
        3: 500,  # 500–999 chars
        4: 1000,  # 1000+ chars
    }

    def score(
        self,
        content: str,
        confidence: float,
        classification: str,
        source: str,
        tags: Optional[List[str]] = None,
    ) -> ScoreBreakdown:
        """
        Compute value score for a memory record.

        Args:
            content: Memory content text
            confidence: Agent confidence 0.0–1.0
            classification: PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED
            source: agent_id, human, import, consolidation, system
            tags: Optional tags

        Returns:
            ScoreBreakdown with component scores and final tier
        """
        # Content length score (0–2)
        length = len(content.strip())
        if length < 20:
            length_score = 0
        elif length < 50:
            length_score = 1
        else:
            length_score = 2

        # Confidence score (0–2)
        if confidence < 0.3:
            confidence_score = 0
        elif confidence < 0.5:
            confidence_score = 1
        elif confidence < 0.8:
            confidence_score = 2
        else:
            confidence_score = 2

        # Classification bonus (0–1)
        class_bonus = 0
        if classification == "RESTRICTED" or classification == "CONFIDENTIAL":
            class_bonus = 1
        elif classification == "INTERNAL":
            class_bonus = 1  # Give some bonus for INTERNAL too

        # Provenance bonus (0–1)
        prov_bonus = 0
        if source == "human":
            prov_bonus = 1
        elif source == "consolidation":
            prov_bonus = 1  # Consolidated = higher value
        elif source == "agent":
            prov_bonus = 1  # Agent-generated content gets baseline value

        total = length_score + confidence_score + class_bonus + prov_bonus
        total = max(0, min(5, total))  # Clamp 0–5

        return ScoreBreakdown(
            content_length_score=length_score,
            confidence_score=confidence_score,
            classification_bonus=class_bonus,
            provenance_bonus=prov_bonus,
            total=total,
            tier=Tier(total),
        )

    def should_persist(self, breakdown: ScoreBreakdown) -> bool:
        """Check if score warrants persistence (score > 1)."""
        return breakdown.total > 1

    def get_ttl_multiplier(self, tier: Tier) -> float:
        """Get TTL multiplier for tier (ADR-019)."""
        multipliers = {
            Tier.TIER_1: 1.0,
            Tier.TIER_2: 1.5,  # +50%
            Tier.TIER_3: float("inf"),  # Infinite (pinned)
        }
        return multipliers.get(tier, 1.0)


def compute_injection_quota(
    breakdown: Optional[ScoreBreakdown] = None,
    max_memories: int = 15,
    max_tokens: int = 2000,
) -> dict[str, Any]:
    """
    Compute injection quota for session initialization (architecture §12, §13).

    Returns quota allocation per tier.
    """
    # Tier 3 gets priority, then Tier 2, then Tier 1
    tier_allocation = {
        Tier.TIER_3: max_memories // 2,
        Tier.TIER_2: max_memories // 3,
        Tier.TIER_1: max_memories // 6,
    }

    # Token allocation proportional
    token_allocation = {
        Tier.TIER_3: max_tokens // 2,
        Tier.TIER_2: max_tokens // 3,
        Tier.TIER_1: max_tokens // 6,
    }

    return {
        "max_memories": max_memories,
        "max_tokens": max_tokens,
        "tier_allocation": tier_allocation,
        "token_allocation": token_allocation,
    }
