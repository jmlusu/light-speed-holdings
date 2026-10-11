"""Top-priority page image plans for CEO dashboard and public website.

Implements a priority ranking system for images used on top-priority pages
(landing page, solution pages, insights page). Ensures critical pages have
pre-cached, optimized assets with appropriate fallback strategies.

The system follows the 5-tier HITL governance model and integrates with
the asset pipeline (T12) for caching and optimization.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ImagePriority(Enum):
    """Priority levels for page images, from highest to lowest."""

    CRITICAL = "critical"  # Landing page hero, primary CTAs
    HIGH = "high"  # Solution page heroes, key illustrations
    MEDIUM = "medium"  # Feature diagrams, supporting graphics
    LOW = "low"  # Decorative icons, secondary illustrations


class PageTarget(Enum):
    """Target pages for image prioritization."""

    LANDING = "landing"
    SOLUTIONS = "solutions"
    INSIGHTS = "insights"
    CASE_STUDIES = "case_studies"
    BLOG = "blog"


@dataclass
class ImagePlan:
    """A prioritized image plan for a specific page."""

    page: PageTarget
    priority: ImagePriority
    prompt: str  # Original generation prompt
    model_variant: str  # Which AI model to use (fp16, fp8, offload, etc.)
    expected_size_kb: int  # Target file size in KB
    alt_text: str  # Accessibility alt text
    caption: str | None = None  # Optional caption
    fallback_prompt: str | None = None  # Lower-priority fallback
    generated_at: float = field(default_factory=time.time)
    expires_at: float | None = field(
        default_factory=lambda: time.time() + 86400 * 30
    )  # 30-day expiry
    status: str = "pending"  # pending, generating, generated, failed, expired
    asset_hash: str | None = None  # Hash for caching (T12 integration)


@dataclass
class ImagePriorityPlan:
    """Complete priority plan for all top-priority pages."""

    landing: ImagePlan
    solutions: ImagePlan
    insights: ImagePlan
    case_studies: ImagePlan | None = None
    blog: ImagePlan | None = None

    # Generated assets (populated after generation)
    landing_asset_hash: str | None = None
    solutions_asset_hash: str | None = None
    insights_asset_hash: str | None = None
    case_studies_asset_hash: str | None = None
    blog_asset_hash: str | None = None

    # Priority ordering
    critical_order: list[PageTarget] = field(
        default_factory=lambda: [
            PageTarget.LANDING,
            PageTarget.SOLUTIONS,
            PageTarget.INSIGHTS,
        ]
    )

    # Cache integration (T12)
    asset_pipeline_integration: bool = True


class ImagePriorityEngine:
    """Engine that manages top-priority page image plans and generation.

    Responsibilities:
    - Define and track image priority for each top-page
    - Coordinate generation via ComfyUI (or fallback)
    - Manage cache invalidation and expiry
    - Ensure brand compliance (navy #070A40, red #DC3641, cyan #00BFFF)
    - Track generation metrics and costs
    """

    # Brand color constraints for image generation
    BRAND_CONSTRAINTS = {
        "primary_colors": ["#070A40", "#DC3641", "#00BFFF"],  # Navy, Red, Cyan
        "accent_colors": ["#FFFFFF", "#F5F5F5"],  # White, Light gray
        "forbidden": ["#FF0000", "#00FF00", "#0000FF"],  # Pure Reds/Greens/Blues
    }

    # Default model variants by priority (maps to ComfyUI model variants)
    DEFAULT_MODEL_VARIANTS = {
        ImagePriority.CRITICAL: "fp16",  # Highest quality, 16GB+ VRAM
        ImagePriority.HIGH: "fp8",  # Good quality, 8GB+ VRAM
        ImagePriority.MEDIUM: "offload",  # Acceptable quality, disk offload
        ImagePriority.LOW: "offload",  # Lowest priority, always offload
    }

    # Generation budgets (estimated cost in USD) by priority
    GENERATION_BUDGETS_USD = {
        ImagePriority.CRITICAL: 0.50,  # Higher quality, more tokens
        ImagePriority.HIGH: 0.25,
        ImagePriority.MEDIUM: 0.10,
        ImagePriority.LOW: 0.05,
    }

    # TTL in seconds for generated assets (before re-generation needed)
    GENERATION_TTL_SECONDS = {
        ImagePriority.CRITICAL: 86400 * 7,  # 1 week - critical pages
        ImagePriority.HIGH: 86400 * 14,  # 2 weeks - high priority
        ImagePriority.MEDIUM: 86400 * 30,  # 1 month - medium priority
        ImagePriority.LOW: 86400 * 60,  # 2 months - low priority
    }

    def __init__(self, asset_pipeline: Any | None = None) -> None:
        """Initialize the image priority engine.

        Args:
            asset_pipeline: Optional AssetPipeline instance (T12) for caching
        """
        self._asset_pipeline = asset_pipeline
        self._plans: ImagePriorityPlan = self._init_default_plans()
        self._metrics = {
            "total_generated": 0,
            "cache_hits": 0,
            "generation_failures": 0,
            "brand_compliance_checks": 0,
            "brand_compliance_passes": 0,
        }

    def _init_default_plans(self) -> ImagePriorityPlan:
        """Initialize default image plans for all top-priority pages."""
        return ImagePriorityPlan(
            landing=self._make_plan(
                PageTarget.LANDING,
                ImagePriority.CRITICAL,
                "LightSpeed Holdings CEO dashboard landing page hero image",
                "#070A40 #DC3641 #00BFFF abstract tech framework",
                500,
                "Transformative AI leadership for the future of work",
            ),
            solutions=self._make_plan(
                PageTarget.SOLUTIONS,
                ImagePriority.HIGH,
                "LightSpeed AI Company Builder solutions overview illustration",
                "#070A40 #DC3641 abstract cloud architecture diagram",
                300,
                "Comprehensive AI-native company building platform",
            ),
            insights=self._make_plan(
                PageTarget.INSIGHTS,
                ImagePriority.MEDIUM,
                "AI thought leadership insights dashboard background",
                "#070A40 subtle pattern",
                200,
                "Quarterly AI industry insights and market analysis",
            ),
            case_studies=self._make_plan(
                PageTarget.CASE_STUDIES,
                ImagePriority.LOW,
                "AI case study showcase hero image",
                "#070A40 #DC3641 tech illustrations",
                150,
                "Customer success stories with AI",
            )
            if False  # Disabled by default, enable when needed
            else None,
            blog=self._make_plan(
                PageTarget.BLOG,
                ImagePriority.LOW,
                "AI blog illustration feature image",
                "#070A40 #00BFFF tech abstract",
                150,
                "Monthly AI thought leadership blog posts",
            )
            if False  # Disabled by default, enable when needed
            else None,
        )

    def _make_plan(
        self,
        page: PageTarget,
        priority: ImagePriority,
        prompt: str,
        brand_constraints: str,
        expected_size_kb: int,
        alt_text: str,
    ) -> ImagePlan:
        """Create an ImagePlan with the given parameters."""
        return ImagePlan(
            page=page,
            priority=priority,
            prompt=prompt,
            model_variant=self.DEFAULT_MODEL_VARIANTS[priority],
            expected_size_kb=expected_size_kb,
            alt_text=alt_text,
            caption=self._generate_caption(page),
            fallback_prompt=self._make_fallback_prompt(page, priority),
        )

    @staticmethod
    def _generate_caption(page: PageTarget) -> str | None:
        """Generate a default caption for a page's image."""
        captions = {
            PageTarget.LANDING: "AI-native company building platform",
            PageTarget.SOLUTIONS: "AI-powered business solutions",
            PageTarget.INSIGHTS: "Quarterly AI industry insights",
            PageTarget.CASE_STUDIES: "Customer success stories",
            PageTarget.BLOG: "AI thought leadership article image",
        }
        return captions.get(page)

    @staticmethod
    def _make_fallback_prompt(page: PageTarget, priority: ImagePriority) -> str:
        """Make a fallback prompt for lower-priority generation."""
        fallbacks = {
            PageTarget.LANDING: "Abstract business technology background",
            PageTarget.SOLUTIONS: "Cloud infrastructure diagram",
            PageTarget.INSIGHTS: "Data analysis chart pattern",
            PageTarget.CASE_STUDIES: "Customer success icon set",
            PageTarget.BLOG: "Abstract technology waveform",
        }
        return fallbacks.get(page, "Abstract technology background")

    def get_plan(self, page: PageTarget) -> ImagePlan | None:
        """Get the image plan for a specific page.

        Args:
            page: The page target

        Returns:
            ImagePlan if found, None otherwise
        """
        plans_map = {
            PageTarget.LANDING: self._plans.landing,
            PageTarget.SOLUTIONS: self._plans.solutions,
            PageTarget.INSIGHTS: self._plans.insights,
            PageTarget.CASE_STUDIES: self._plans.case_studies,
            PageTarget.BLOG: self._plans.blog,
        }
        return plans_map.get(page)

    def is_expired(self, plan: ImagePlan) -> bool:
        """Check if an image plan has expired and needs regeneration.

        Args:
            plan: The image plan to check

        Returns:
            True if the plan has expired
        """
        if plan.expires_at is None:
            return False
        return time.time() > plan.expires_at

    def needs_regeneration(self, plan: ImagePlan) -> bool:
        """Check if an image plan needs regeneration (expired or failed).

        Args:
            plan: The image plan to check

        Returns:
            True if the plan needs regeneration
        """
        return self.is_expired(plan) or plan.status in ("failed", "expired")

    def get_cached_asset(self, plan: ImagePlan, asset_hash: str) -> Any | None:
        """Retrieve a cached asset from the asset pipeline (T12).

        Args:
            plan: The image plan
            asset_hash: The asset hash for lookup

        Returns:
            Cached asset data or None
        """
        if not self._asset_pipeline:
            return None
        entry = self._asset_pipeline.get_cached_asset(asset_hash)
        if entry is not None:
            self._metrics["cache_hits"] += 1
        return entry

    def mark_generated(self, plan: ImagePlan, asset_hash: str) -> None:
        """Mark an image plan as successfully generated.

        Args:
            plan: The image plan
            asset_hash: The asset hash for caching
        """
        plan.status = "generated"
        plan.asset_hash = asset_hash
        # Update expiry
        plan.expires_at = time.time() + self.GENERATION_TTL_SECONDS[plan.priority]
        # Update asset pipeline cache if available
        if self._asset_pipeline:
            # Asset was already cached during generation
            pass
        self._metrics["total_generated"] += 1

    def mark_failed(self, plan: ImagePlan) -> None:
        """Mark an image plan as failed.

        Args:
            plan: The image plan
        """
        plan.status = "failed"
        self._metrics["generation_failures"] += 1

    def get_priority_order(self) -> list[PageTarget]:
        """Get the prioritized list of pages for image generation.

        Returns:
            List of PageTarget in priority order
        """
        return self._plans.critical_order

    def get_metrics(self) -> dict[str, Any]:
        """Return current engine metrics."""
        return {
            **self._metrics,
            "total_plans": sum(
                1
                for p in [
                    self._plans.landing,
                    self._plans.solutions,
                    self._plans.insights,
                    self._plans.case_studies,
                    self._plans.blog,
                ]
                if p is not None
            ),
        }

    def validate_brand_compliance(self, plan: ImagePlan) -> bool:
        """Validate that an image plan complies with brand guidelines.

        Checks that generated images respect the LightSpeed brand colors
        (navy #070A40, red #DC3641, cyan #00BFFF) and don't use forbidden
        color patterns.

        Args:
            plan: The image plan to validate

        Returns:
            True if brand compliance passes
        """
        self._metrics["brand_compliance_checks"] += 1

        # Check that the prompt includes brand color constraints
        prompt_lower = plan.prompt.lower()
        brand_colors = self.BRAND_CONSTRAINTS["primary_colors"]
        has_brand_ref = any(
            color.lower().replace("#", "") in prompt_lower for color in brand_colors
        )

        # Check that forbidden colors are not explicitly requested
        forbidden = self.BRAND_CONSTRAINTS["forbidden"]
        has_forbidden = any(color.lower().replace("#", "") in prompt_lower for color in forbidden)

        passes = has_brand_ref and not has_forbidden

        if passes:
            self._metrics["brand_compliance_passes"] += 1

        logger.info(
            "Brand compliance %s for %s (%s): brand_ref=%s, forbidden=%s",
            "PASS" if passes else "FAIL",
            plan.page.value,
            plan.priority.value,
            has_brand_ref,
            has_forbidden,
        )

        return passes


# Convenience function for quick plan creation
def create_default_priority_plan(asset_pipeline: Any | None = None) -> ImagePriorityPlan:
    """Create a default ImagePriorityPlan with all top-page plans.

    Args:
        asset_pipeline: Optional AssetPipeline instance for caching

    Returns:
        Configured ImagePriorityPlan with default plans
    """
    engine = ImagePriorityEngine(asset_pipeline=asset_pipeline)
    return engine._plans


# Convenience function to check if a page image needs regeneration
def needs_regeneration(
    plan: ImagePlan,
    asset_pipeline: Any | None = None,
) -> bool:
    """Check if an image plan needs regeneration.

    Args:
        plan: The image plan
        asset_pipeline: Optional AssetPipeline instance

    Returns:
        True if the plan needs regeneration
    """
    engine = ImagePriorityEngine(asset_pipeline=asset_pipeline)
    return engine.is_expired(plan)


# Global default engine instance (lazy-initialized)
_default_engine: ImagePriorityEngine | None = None


def get_image_priority_engine() -> ImagePriorityEngine:
    """Get the global image priority engine instance.

    Returns:
        The singleton ImagePriorityEngine instance
    """
    global _default_engine
    if _default_engine is None:
        _default_engine = ImagePriorityEngine()
    return _default_engine
