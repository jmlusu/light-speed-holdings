"""AI-generated vs human-created content sourcing decision model.

Implements a tiered decision framework that determines whether a given
content creation task should be handled by AI generation, human authors,
or a hybrid approach. The decision is based on task complexity, budget
constraints, brand compliance requirements, urgency, and governance tiers.

The model follows the 5-tier HITL (Human-in-the-Loop) approval matrix
consistent with the organization's governance structure:
  Tier 0: Fully autonomous - AI generates without human review
  Tier 1: AI generates, light human review
  Tier 2: AI generates, structured human gate
  Tier 3: Human draft, AI polish
  Tier 4: Human-created, AI review only
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class SourcingDecision(Enum):
    """Possible sourcing decisions for content creation."""

    AI_GENERATE = "ai_generate"  # AI generates, may have light review
    AI_WITH_REVIEW = "ai_with_review"  # AI generates, human review required
    HYBRID = "hybrid"  # AI draft + human polish
    HUMAN_CREATE = "human_create"  # Human creates, AI reviews
    HUMAN_ONLY = "human_only"  # Human-only, no AI involvement


class DecisionTier(Enum):
    """HITL decision tier (0-4), consistent with the approval gate matrix."""

    TIER_0 = 0  # Fully autonomous, AI generates without human review
    TIER_1 = 1  # AI generates, light human review (summary check)
    TIER_2 = 2  # AI generates, structured human gate (approval required)
    TIER_3 = 3  # Human draft, AI polish and enhancement
    TIER_4 = 4  # Human-created, AI review only for optimization


@dataclass
class ContentSpec:
    """Specifications for a content creation task."""

    content_type: str  # e.g., "blog_post", "whitepaper", "social_post", "email", "report"
    topic: str  # The subject/topic of the content
    audience: str  # Target audience
    objective: str  # What the content aims to achieve
    word_count: int | None = None  # Target or estimated length
    urgency: str | None = None  # "low", "medium", "high", "critical"
    budget_tier: str | None = None  # "fast", "standard", "premium", "enterprise"
    brand_compliance: bool = True  # Whether strict brand compliance is required
    technical_complexity: str | None = None  # "low", "medium", "high"
    has_deadline: bool = False  # Whether there's a hard deadline


@dataclass
class SourcingDecisionResult:
    """Result of the sourcing decision model."""

    decision: SourcingDecision
    tier: DecisionTier
    rationale: str  # Why this decision was made
    estimated_cost_usd: float | None = None  # Estimated AI cost
    estimated_hours: float | None = None  # Estimated human hours
    recommended_model: str | None = None  # Which AI model to use
    required_review: bool = False  # Whether human review is required
    review_tier: DecisionTier | None = None  # Required review tier if applicable


class AIGenSourcingEngine:
    """Engine that determines AI vs human content sourcing decisions.

    The decision framework considers:
    1. Content type and complexity
    2. Budget constraints and model tier mapping
    3. Brand compliance requirements
    4. Urgency and deadline pressure
    5. Governance tier requirements
    6. Evidence/claims backing needed
    """

    # Decision rules mapped by content type (initialized in __init__)
    _decision_rules: dict[str, dict[str, Any]] | None = None

    # Brand compliance thresholds (initialized in __init__)
    _brand_compliance_rules: dict[str, Any] | None = None

    def __init__(self) -> None:
        """Initialize decision rules if not already set."""
        if AIGenSourcingEngine._decision_rules is None:
            AIGenSourcingEngine._decision_rules = self._build_decision_rules()
        if AIGenSourcingEngine._brand_compliance_rules is None:
            AIGenSourcingEngine._brand_compliance_rules = self._build_brand_compliance_rules()

        # Promote class variables to instance variables for this engine
        self._decision_rules = AIGenSourcingEngine._decision_rules
        self._brand_compliance_rules = AIGenSourcingEngine._brand_compliance_rules

    @staticmethod
    def _build_decision_rules() -> dict[str, dict[str, Any]]:
        """Build the content-type-to-decision mapping rules.

        Rules follow the 5-tier HITL matrix:
        - Tier 0: Simple, low-stakes, budget-allowing AI generation
        - Tier 1: Moderate complexity, requires light review
        - Tier 2: High compliance or public-facing, requires approval
        - Tier 3: Human-authored with AI enhancement
        - Tier 4: Critical, brand-critical, or compliance-mandated human-only
        """
        return {
            "blog_post": {
                "default_tier": DecisionTier.TIER_1,
                "min_budget": "fast",
                "brand_override": True,
                "urgency_boost": {"high": 1, "critical": 2},  # bump tier
            },
            "whitepaper": {
                "default_tier": DecisionTier.TIER_3,
                "min_budget": "premium",
                "brand_override": True,
                "urgency_boost": {},
            },
            "social_post": {
                "default_tier": DecisionTier.TIER_0,
                "min_budget": "fast",
                "brand_override": False,
                "urgency_boost": {"critical": 1},
            },
            "email": {
                "default_tier": DecisionTier.TIER_1,
                "min_budget": "fast",
                "brand_override": True,
                "urgency_boost": {"high": 1},
            },
            "report": {
                "default_tier": DecisionTier.TIER_3,
                "min_budget": "premium",
                "brand_override": True,
                "urgency_boost": {},
            },
            "case_study": {
                "default_tier": DecisionTier.TIER_4,
                "min_budget": "enterprise",
                "brand_override": True,
                "urgency_boost": {},
            },
            "press_release": {
                "default_tier": DecisionTier.TIER_4,
                "min_budget": "enterprise",
                "brand_override": True,
                "urgency_boost": {},
            },
        }

    @staticmethod
    def _build_brand_compliance_rules() -> dict[str, Any]:
        """Build brand compliance decision rules.

        Strict brand compliance pushes decisions toward higher tiers
        (more human involvement).
        """
        return {
            "strict_brand": {
                "ai_tier_ceiling": DecisionTier.TIER_2,  # AI cannot exceed Tier 2
                "requires_approval": True,
                "evidence_backing": True,
            },
            "moderate_brand": {
                "ai_tier_ceiling": DecisionTier.TIER_3,
                "requires_approval": False,
                "evidence_backing": False,
            },
            "relaxed_brand": {
                "ai_tier_ceiling": DecisionTier.TIER_4,
                "requires_approval": False,
                "evidence_backing": False,
            },
        }

    def decide(
        self,
        spec: ContentSpec,
        brand_compliance_level: str = "moderate_brand",
        budget_provider: str | None = None,
        current_date: datetime | None = None,
    ) -> SourcingDecisionResult:
        """Determine the sourcing decision for a content creation task.

        Args:
            spec: Content specifications
            brand_compliance_level: "strict_brand", "moderate_brand", or "relaxed_brand"
            budget_provider: Which budget provider to consult (for tier mapping)
            current_date: Override current date for testing

        Returns:
            SourcingDecisionResult with the determined decision and tier
        """
        rules = (self._decision_rules or {}).get(
            spec.content_type, (self._decision_rules or {}).get("blog_post", {"default_tier": 0})
        )
        brand_rules = (self._brand_compliance_rules or {}).get(brand_compliance_level, {})

        # Start with default tier for this content type
        tier = rules["default_tier"]

        # Apply urgency boost if needed
        if spec.urgency and spec.urgency in rules.get("urgency_boost", {}):
            boost = rules["urgency_boost"][spec.urgency]
            tier = self._bump_tier(tier, boost)

        # Apply brand compliance ceiling
        ai_tier_ceiling = brand_rules.get("ai_tier_ceiling", DecisionTier.TIER_4)
        tier = DecisionTier(min(tier.value, ai_tier_ceiling.value))  # Cap at the brand ceiling

        # Apply brand override (strict brand forces higher tier)
        if brand_rules.get("requires_approval", False) and spec.brand_compliance:
            tier = self._bump_tier(tier, 1)

        # Determine the sourcing decision based on tier
        decision, rationale, estimated_cost, estimated_hours, recommended_model = (
            self._tier_to_decision(tier, spec)
        )

        # Determine if review is required
        required_review = tier in (DecisionTier.TIER_2, DecisionTier.TIER_3)
        review_tier = DecisionTier.TIER_2 if tier == DecisionTier.TIER_3 else None

        result = SourcingDecisionResult(
            decision=decision,
            tier=tier,
            rationale=rationale,
            estimated_cost_usd=estimated_cost,
            estimated_hours=estimated_hours,
            recommended_model=recommended_model,
            required_review=required_review,
            review_tier=review_tier,
        )

        logger.info(
            "Sourcing decision for %s: tier=%s, decision=%s",
            spec.content_type,
            tier.value,
            decision.value,
        )

        return result

    @staticmethod
    def _bump_tier(tier: DecisionTier, steps: int) -> DecisionTier:
        """Move tier up by *steps* (toward more human involvement)."""
        current = tier.value
        new_value = min(current + steps, 4)  # Cap at Tier 4
        return DecisionTier(new_value)

    def _tier_to_decision(
        self,
        tier: DecisionTier,
        spec: ContentSpec,
    ) -> tuple[SourcingDecision, str, float | None, float | None, str | None]:
        """Convert a decision tier to a sourcing decision and rationale."""

        if tier == DecisionTier.TIER_0:
            return (
                SourcingDecision.AI_GENERATE,
                f"Tier 0: Fully autonomous AI generation for {spec.content_type}",
                self._estimate_ai_cost(spec, "fast"),
                None,
                self._recommend_model("fast"),
            )

        if tier == DecisionTier.TIER_1:
            return (
                SourcingDecision.AI_WITH_REVIEW,
                f"Tier 1: AI generation with light human review for {spec.content_type}",
                self._estimate_ai_cost(spec, "standard"),
                None,
                self._recommend_model("standard"),
            )

        if tier == DecisionTier.TIER_2:
            return (
                SourcingDecision.HYBRID,
                f"Tier 2: AI generation with structured human gate for {spec.content_type} "
                f"(brand compliance: {spec.brand_compliance})",
                self._estimate_ai_cost(spec, "premium"),
                None,
                self._recommend_model("premium"),
            )

        if tier == DecisionTier.TIER_3:
            return (
                SourcingDecision.HYBRID,
                f"Tier 3: Human draft with AI polish for {spec.content_type} "
                f"(brand compliance: {spec.brand_compliance})",
                None,
                self._estimate_hours(spec, "human_draft"),
                None,
            )

        # tier == DecisionTier.TIER_4
        return (
            SourcingDecision.HUMAN_CREATE,
            f"Tier 4: Human-created content for {spec.content_type} "
            f"(brand compliance: {spec.brand_compliance}, "
            f"strict requirements)",
            None,
            self._estimate_hours(spec, "human_only"),
            None,
        )

    @staticmethod
    def _estimate_ai_cost(spec: ContentSpec, budget_tier: str) -> float | None:
        """Estimate AI generation cost based on content spec and budget tier.

        Pricing is approximate and model-dependent.
        """
        # Rough per-token estimates by tier (2026 pricing)
        rates = {
            "fast": 0.0001,  # per 1K tokens
            "standard": 0.0002,
            "premium": 0.0005,
            "enterprise": 0.001,
        }
        rate = rates.get(budget_tier, 0.0002)

        # Estimate token count from word count or default
        if spec.word_count:
            # Rough: 1 token ≈ 0.75 words for English
            tokens = spec.word_count / 0.75
        else:
            # Default estimates by content type
            defaults = {
                "blog_post": 800,
                "whitepaper": 2500,
                "social_post": 200,
                "email": 300,
                "report": 1500,
                "case_study": 3000,
                "press_release": 500,
            }
            tokens = defaults.get(spec.content_type, 500)

        cost = (tokens / 1000) * rate
        return round(cost, 4)

    @staticmethod
    def _estimate_hours(spec: ContentSpec, mode: str) -> float | None:
        """Estimate human hours required for content creation.

        Mode: "human_draft" (human writes from scratch, AI polishes)
              "human_only" (human creates entirely)
        """
        # Base hours by content type (rough estimates)
        defaults = {
            "blog_post": 2.0,
            "whitepaper": 8.0,
            "social_post": 0.5,
            "email": 1.0,
            "report": 4.0,
            "case_study": 12.0,
            "press_release": 2.0,
        }
        base_hours = defaults.get(spec.content_type, 2.0)

        # Adjust for word count if provided
        if spec.word_count and spec.word_count > 1000:
            # Rough: 0.2 hours per additional 100 words over 1000
            extra_hours = (spec.word_count - 1000) * 0.2 / 100
            base_hours += extra_hours

        # Adjust for complexity
        if spec.technical_complexity == "high":
            base_hours *= 1.5
        elif spec.technical_complexity == "low":
            base_hours *= 0.8

        # Adjust for urgency
        if spec.urgency == "critical":
            base_hours *= 1.3  # Faster but more stressful
        elif spec.urgency == "high":
            base_hours *= 1.1

        return round(base_hours, 2)

    @staticmethod
    def _recommend_model(tier_level: str) -> str | None:
        """Recommend an AI model based on the budget tier level.

        tier_level: "fast", "standard", "premium", "enterprise"
        """
        model_map = {
            "fast": "gemini-1.5-flash",
            "standard": "gemini-1.5-pro",
            "premium": "gemini-1.5-pro-long",
            "enterprise": "gemini-1.5-pro-32k",
        }
        return model_map.get(tier_level)


# Convenience function for quick decisions
def decide_sourcing(
    content_type: str,
    topic: str,
    audience: str,
    objective: str,
    word_count: int | None = None,
    urgency: str | None = None,
    budget_tier: str | None = None,
    brand_compliance: bool = True,
    **kwargs: Any,
) -> SourcingDecisionResult:
    """Quick sourcing decision without building a full ContentSpec.

    Args:
        content_type: Type of content (blog_post, whitepaper, etc.)
        topic: Content topic
        audience: Target audience
        objective: Content objective
        word_count: Estimated length
        urgency: "low"|"medium"|"high"|"critical"
        budget_tier: "fast"|"standard"|"premium"|"enterprise"
        brand_compliance: Whether strict brand compliance is required

    Returns:
        SourcingDecisionResult with the determined decision
    """
    spec = ContentSpec(
        content_type=content_type,
        topic=topic,
        audience=audience,
        objective=objective,
        word_count=word_count,
        urgency=urgency,
        budget_tier=budget_tier,
        brand_compliance=brand_compliance,
    )
    engine = AIGenSourcingEngine()
    return engine.decide(spec, **kwargs)
