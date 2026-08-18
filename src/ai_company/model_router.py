"""Model routing policy — resolves which LLM to use for a given agent and task.

Supports three routing layers:
  1. Per-agent override (agent-registry.json ``model`` field)
  2. Routing rules (context → tier, agent_type + priority → tier)
  3. Fallback to ``standard`` tier

Context-aware routing detects domain keywords in the task prompt and
selects the appropriate tier.  Quality-based fallback promotes to the
next higher tier when all providers in the current tier fail.

ML-enhanced routing integrates task complexity scoring to route simple
tasks to fast/cheap models and complex tasks to premium models.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import aiohttp
import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Free model metadata
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FreeModel:
    """Represents a free Opencode model with metadata for rotation."""

    id: str
    name: str
    context: int  # context window in tokens; larger = more capable
    provider: str = "opencode"
    model: str = ""
    priority: int = 0  # higher = preferred for rotation (context-weighted)


# In-memory cache for free model catalog
# Structure: {key: (timestamp, models_list)}
_FREE_MODEL_CACHE: dict[str, tuple[datetime, list[FreeModel]]] = {}
_CACHE_TTL_SECONDS = 3600  # 1 hour


# ---------------------------------------------------------------------------
# Domain → tier mapping for context-aware routing
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "finance": [
        "financial",
        "finance",
        "accounting",
        "budget",
        "revenue",
        "profit",
        "loss",
        "balance sheet",
        "cash flow",
        "invoice",
        "tax",
        "audit",
        "compliance",
        "ledger",
    ],
    "legal": [
        "legal",
        "contract",
        "agreement",
        "liability",
        "regulation",
        "statute",
        "litigation",
        "intellectual property",
        "patent",
        "trademark",
        "nda",
        "terms of service",
    ],
    "security": [
        "security",
        "vulnerability",
        "exploit",
        "breach",
        "auth",
        "encryption",
        "secret",
        "credential",
        "firewall",
        "pentest",
        "owasp",
        "cve",
    ],
    "code_review": [
        "review",
        "pull request",
        "pr",
        "code review",
        "diff",
        "merge",
        "refactor",
        "lint",
        "static analysis",
    ],
    "deployment": [
        "deploy",
        "release",
        "production",
        "rollback",
        "ci/cd",
        "pipeline",
        "kubernetes",
        "docker",
        "terraform",
    ],
    "data_science": [
        "model",
        "training",
        "inference",
        "dataset",
        "feature",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "epoch",
        "hyperparameter",
        "ml",
        "machine learning",
        "neural",
    ],
}

# Ordered tier progression for quality-based fallback
TIER_ORDER: list[str] = ["fast", "standard", "premium"]


# ---------------------------------------------------------------------------
# Task Complexity Scoring — routes simple tasks to fast/cheap models
# ---------------------------------------------------------------------------

# Keywords indicating simple, well-defined tasks
SIMPLE_TASK_KEYWORDS: dict[str, list[str]] = {
    "read_only": [
        "read",
        "view",
        "show",
        "display",
        "list",
        "cat",
        "head",
        "tail",
        "grep",
        "search",
        "find",
        "lookup",
        "get",
        "fetch",
    ],
    "single_file_edit": [
        "fix typo",
        "add comment",
        "update comment",
        "rename variable",
        "change string",
        "update constant",
        "modify config",
    ],
    "simple_command": [
        "run test",
        "run pytest",
        "run lint",
        "run build",
        "run script",
        "execute",
        "check",
        "verify",
        "validate",
    ],
    "boilerplate": [
        "create file",
        "add file",
        "new file",
        "scaffold",
        "template",
        "boilerplate",
        "stub",
        "placeholder",
    ],
}

# Keywords indicating complex tasks requiring reasoning
COMPLEX_TASK_KEYWORDS: dict[str, list[str]] = {
    "architecture": [
        "design",
        "architect",
        "structure",
        "refactor",
        "restructure",
        "reorganize",
        "pattern",
        "framework",
        "system design",
    ],
    "multi_file": [
        "multiple files",
        "across files",
        "several files",
        "many files",
        "codebase",
        "project-wide",
        "global",
        "cross-cutting",
    ],
    "debugging": [
        "debug",
        "trace",
        "root cause",
        "investigate",
        "diagnose",
        "troubleshoot",
        "why",
        "analyze failure",
    ],
    "integration": [
        "integrate",
        "connect",
        "wire up",
        "hook up",
        "link",
        "api",
        "endpoint",
        "service",
        "microservice",
    ],
    "security": [
        "security",
        "vulnerability",
        "audit",
        "compliance",
        "penetration",
        "threat model",
        "risk assessment",
        "hardening",
    ],
    "performance": [
        "optimize",
        "performance",
        "speed up",
        "latency",
        "throughput",
        "bottleneck",
        "profile",
        "benchmark",
    ],
    "planning": [
        "plan",
        "strategy",
        "roadmap",
        "design doc",
        "spec",
        "specification",
        "requirements",
        "break down",
        "decompose",
    ],
}

# Task type → base complexity score (0-100)
TASK_TYPE_COMPLEXITY: dict[str, int] = {
    "read": 10,
    "grep": 15,
    "list": 10,
    "edit": 30,
    "bash": 25,
    "webfetch": 20,
    "task": 40,  # delegation adds complexity
}

# Task-type detection keywords (maps prompt patterns to task_type keys
# used in the task_type_routing section of models.yaml).
TASK_TYPE_KEYWORDS: dict[str, list[str]] = {
    "read_only": [
        "read",
        "show",
        "display",
        "list",
        "cat",
        "print",
        "view",
        "display",
        "what is",
        "what are",
        "how does",
        "explain",
    ],
    "single_file_edit": [
        "edit",
        "modify",
        "update",
        "change",
        "fix typo",
        "rename",
        "adjust",
        "tweak",
    ],
    "simple_command": [
        "run",
        "execute",
        "build",
        "test",
        "install",
        "compile",
        "make",
        "npm",
        "yarn",
        "pip",
        "cargo",
    ],
    "boilerplate": [
        "scaffold",
        "template",
        "generate",
        "create file",
        "new file",
        "boilerplate",
        "init",
    ],
    "code_review": [
        "review",
        "audit",
        "check",
        "lint",
        "analyze",
        "code review",
        "pull request",
        "pr review",
    ],
    "debugging": [
        "fix",
        "bug",
        "error",
        "debug",
        "crash",
        "fail",
        "traceback",
        "exception",
        "broken",
        "issue",
    ],
    "refactor": [
        "refactor",
        "reorganize",
        "clean up",
        "restructure",
        "simplify",
        "optimize",
        "improve",
    ],
    "integration": [
        "integrate",
        "connect",
        "wire",
        "hook up",
        "link",
        "merge",
        "combine",
    ],
    "architecture": [
        "architecture",
        "design",
        "system design",
        "blueprint",
        "structure",
        "layout",
        "diagram",
    ],
    "planning": [
        "plan",
        "strategy",
        "roadmap",
        "design doc",
        "spec",
        "specification",
        "requirements",
        "break down",
        "decompose",
    ],
    "security": [
        "security",
        "vulnerability",
        "vulnerabilities",
        "auth",
        "permission",
        "encrypt",
        "sanitize",
        "injection",
        "xss",
    ],
    "performance": [
        "optimize",
        "performance",
        "speed up",
        "latency",
        "throughput",
        "bottleneck",
        "profile",
        "benchmark",
    ],
    "general": [],  # Catch-all, no specific keywords; always matches via fallback
}

# Complexity thresholds for tier selection
COMPLEXITY_THRESHOLDS: dict[str, int] = {
    "fast": 30,  # 0-30 → fast tier
    "standard": 60,  # 31-60 → standard tier
    "premium": 100,  # 61+ → premium tier
}

# Tiers that don't have static provider entries but are still valid routing targets.
# "free" uses a dynamic catalog; "override" comes from per-agent registry.
SPECIAL_TIER_IDS: frozenset[str] = frozenset({"free", "override"})


@dataclass(frozen=True)
class ComplexityScore:
    """Task complexity assessment."""

    score: int  # 0-100
    tier: str  # recommended tier
    factors: list[str]  # contributing factors
    task_type: str  # detected task type


@dataclass(frozen=True)
class Provider:
    """A single provider entry within a tier."""

    provider: str
    model: str


@dataclass(frozen=True)
class ProviderConfig:
    """Top-level provider configuration (backend, api_base, etc.).

    Attributes:
        id: Provider identifier (matches the ``providers`` YAML key).
        backend: Backend implementation name.
        default_model: Default model identifier.
        api_base: Base URL for the provider API.
        oauth2: Optional OAuth2 client-credentials config as a raw dict
            (keys: ``token_url``, ``client_id``/``client_id_env``,
            ``client_secret``/``client_secret_env``, ``scope``,
            ``audience``, ``cache_ttl_seconds``). Empty dict when unset.
        rate_limit: Optional token-bucket config as a raw dict with
            ``rate`` (tokens/sec) and ``capacity`` (burst) keys. Empty dict
            when unset (no client-side limiting applied).
    """

    id: str
    backend: str
    default_model: str
    api_base: str = ""
    oauth2: dict[str, Any] = field(default_factory=dict)
    rate_limit: dict[str, Any] = field(default_factory=dict)
    server: dict[str, Any] = field(default_factory=dict)
    hardware: dict[str, Any] = field(default_factory=dict)
    inference: dict[str, Any] = field(default_factory=dict)
    models: dict[str, Any] = field(default_factory=dict)
    model_dir: str = "./models"


@dataclass(frozen=True)
class Tier:
    """A cost/capability tier with ordered provider fallbacks."""

    id: str
    description: str
    providers: list[Provider] = field(default_factory=list)


@dataclass(frozen=True)
class Route:
    """The resolved result of a routing decision."""

    provider: str
    model: str
    tier: str
    reason: str


class ModelRouter:
    """Reads company/models.yaml and resolves model routing decisions.

    Routing priority:
      1. Per-agent override in agent-registry.json (``model`` field)
      2. Explicit context string (``context`` parameter)
      3. Domain-aware detection from ``task_prompt`` keywords
      4. Routing rules (agent_type + priority)
      5. Fallback to ``standard`` tier
    """

    def __init__(
        self,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
    ) -> None:
        self.config_path = Path(config_path)
        self.registry_path = Path(registry_path)
        self._config: dict[str, Any] = {}
        self._providers: dict[str, ProviderConfig] = {}
        self._tiers: dict[str, Tier] = {}
        self._routing: list[dict[str, Any]] = []
        self._registry: dict[str, dict[str, Any]] = {}
        self._model_cache: dict[str, list[FreeModel]] = {}
        self._cache_time: dict[str, datetime] = {}
        self._load()

    # ── Loading ──────────────────────────────────────────────────────

    def _load(self) -> None:
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        self._parse_providers()
        self._parse_tiers()
        self._routing = self._config.get("routing", [])
        self._load_registry()

    def _load_registry(self) -> None:
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                agents = json.load(f)
            self._registry = {a["name"]: a for a in agents}

    async def _fetch_free_model_catalog(self) -> list[FreeModel]:
        """Fetch free models from OpenCode Zen API, sorted by context window descending.

        Returns list of FreeModel sorted by context (largest first), ready for rotation.
        Caches result for 1 hour (models rarely change daily).
        Falls back to static list if API unavailable or on error.
        """
        # Check cache first
        cache_key = "free_model_catalog"
        if (
            cache_key in self._model_cache
            and self._cache_time.get(cache_key)
            and datetime.now(timezone.utc) - self._cache_time[cache_key]
            < timedelta(seconds=_CACHE_TTL_SECONDS)
        ):
            return self._model_cache[cache_key]

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    "https://opencode.ai/zen/v1/models",
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp,
            ):
                if resp.status == 200:
                    data = await resp.json()
                    models: list[FreeModel] = []
                    for m in data.get("data", []):
                        # Only include truly free models
                        is_free = m.get("free", False)
                        price_data = m.get("price", {})
                        usd_cost = price_data.get("usd", 0) if isinstance(price_data, dict) else 0
                        if is_free and usd_cost == 0:
                            ctx = m.get("max_tokens", 0) or m.get("context_length", 0) or 0
                            mid = m.get("id", "")
                            prov, model = mid.split("/", 1) if "/" in mid else ("opencode", mid)
                            # Higher priority = larger context window
                            priority = 1000 - ctx if ctx > 0 else 0
                            models.append(
                                FreeModel(
                                    id=mid,
                                    name=m.get("name", model),
                                    context=ctx,
                                    provider=prov,
                                    model=model,
                                    priority=priority,
                                )
                            )
                    # Sort by context descending, then priority descending
                    models.sort(key=lambda m: (-m.context, -m.priority))

                    # Cache the result
                    self._model_cache[cache_key] = models
                    self._cache_time[cache_key] = datetime.now(timezone.utc)
                    return models
        except (aiohttp.ClientError, TimeoutError, OSError) as exc:
            logger.debug("Failed to fetch free model catalog: %s", exc)
            pass  # Fall through to static fallback

        # Static fallback list (current known free models)
        static_models = [
            FreeModel(id="opencode/big-pickle", name="Big Pickle", context=200000, priority=800),
            FreeModel(id="opencode/gpt-5-nano", name="GPT-5 Nano", context=128000, priority=920),
            FreeModel(
                id="opencode/kimi-k2.5-free", name="Kimi K2.5 Free", context=262144, priority=738
            ),
            FreeModel(
                id="opencode/qwen3.6-plus-free",
                name="Qwen 3.6 Plus Free",
                context=262144,
                priority=738,
            ),
            FreeModel(
                id="opencode/minimax-m2.5-free",
                name="MiniMax M2.5 Free",
                context=204800,
                priority=795,
            ),
            FreeModel(
                id="opencode/glm-4.7-free", name="GLM-4.7 Free", context=200000, priority=800
            ),
        ]
        self._model_cache[cache_key] = static_models
        self._cache_time[cache_key] = datetime.now(timezone.utc)
        return static_models

    def _get_cached_free_models(self) -> list[FreeModel] | None:
        """Return cached free models if valid, else None."""
        cache_key = "free_model_catalog"
        if (
            cache_key in self._model_cache
            and self._cache_time.get(cache_key)
            and datetime.now(timezone.utc) - self._cache_time[cache_key]
            < timedelta(seconds=_CACHE_TTL_SECONDS)
        ):
            return self._model_cache[cache_key]
        return None

    def _set_cached_free_models(self, models: list[FreeModel]) -> None:
        """Set the cached free model catalog."""
        cache_key = "free_model_catalog"
        self._model_cache[cache_key] = models
        self._cache_time[cache_key] = datetime.now(timezone.utc)

    def _clear_cached_free_models(self) -> None:
        """Clear the free model catalog cache (e.g., on forced refresh)."""
        cache_key = "free_model_catalog"
        self._model_cache.pop(cache_key, None)
        self._cache_time.pop(cache_key, None)

    def _find_free_model(self, model_id: str) -> FreeModel | None:
        """Find a free model by its ID in the cached catalog.

        Returns None if the catalog is not yet cached (caller should
        ensure caching happens first, e.g., during ModelRouter init).
        """
        catalog = self._get_cached_free_models()
        if catalog is None:
            # Catalog not cached yet; return None rather than blocking
            return None
        for m in catalog:
            if m.id == model_id or m.model == model_id:
                return m
        return None

    TOKEN_LIMIT_PATTERNS: tuple[str, ...] = (
        "context length",
        "max_tokens",
        "token limit",
        "too many tokens",
        "exceeds maximum",
        "context window",
        "maximum context",
        "input too long",
        "prompt too long",
        "message too long",
    )

    async def rotate_on_token_limit(
        self,
        failed_model: str,
        task_prompt: str,
    ) -> Route | None:
        """Rotate to a free model with larger context window after token limit.

        Strategy:
        1. Find the current model in the free catalog
        2. Find the next free model with larger context window
        3. If found, return route with that model (same "free" tier)
        4. If no larger free model, rotate to next tier up (standard → premium)
        5. If at premium already, return None (caller should handle error)

        Returns a Route object or None if no rotation possible.
        """
        # Step 1: Find current model in catalog
        current = self._find_free_model(failed_model)
        if current is None:
            # Catalog not available; can't rotate
            return None

        # Step 2: Find next free model with larger context
        catalog = self._get_cached_free_models() or await self._fetch_free_model_catalog()
        if catalog is None:
            return None

        # Look for model with strictly larger context window
        next_model: FreeModel | None = None
        for m in catalog:
            if m.context > current.context and m.id != current.id:
                next_model = m
                break

        # Also check if any model in catalog has larger context than current
        if next_model is None:
            for m in catalog:
                if m.context > current.context:
                    next_model = m
                    break

        if next_model is None:
            # No larger free model available; try next tier up
            return self._rotate_to_next_tier("standard")

        # Step 3: Build and return route with larger-context model
        tier = self._get_tier_for_free_model(next_model)
        reason = f"token-limit rotation: {current.context}→{next_model.context} context window"

        return Route(
            provider=next_model.provider,
            model=next_model.model,
            tier=tier,
            reason=reason,
        )

    def _get_tier_for_free_model(self, model: FreeModel) -> str:
        """Determine which tier a free model should use.

        Free models are primarily used in the 'free' tier, but can also
        serve as fallbacks in 'standard' or 'premium' tiers depending on
        context window size.
        """
        # Map models to tiers based on context window size
        if model.context >= 1_000_000:
            return "premium"  # 1M+ context = premium capability
        elif model.context >= 200_000:
            return "standard"  # 200K+ context = standard capability
        else:
            return "fast"  # Smaller context = fast tier

    def rotate_on_token_limit_sync(
        self,
        failed_model: str,
        task_prompt: str,
    ) -> Route | None:
        """Synchronous version of rotate_on_token_limit for use in non-async contexts.

        Uses cached catalog only (no API fetch). If catalog not cached,
        returns None.
        """
        current = self._find_free_model(failed_model)
        if current is None:
            return None

        catalog = self._get_cached_free_models()
        if catalog is None:
            return None

        # Look for model with strictly larger context window
        next_model: FreeModel | None = None
        for m in catalog:
            if m.context > current.context and m.id != current.id:
                next_model = m
                break

        if next_model is None:
            for m in catalog:
                if m.context > current.context:
                    next_model = m
                    break

        if next_model is None:
            return self._rotate_to_next_tier("standard")

        tier = self._get_tier_for_free_model(next_model)
        reason = f"token-limit rotation: {current.context}→{next_model.context} context window"

        return Route(
            provider=next_model.provider,
            model=next_model.model,
            tier=tier,
            reason=reason,
        )

    def _rotate_to_next_tier(self, current_tier: str) -> Route:
        """Rotate to the next tier up in the sequential chain.

        fast → standard → premium. If already at premium, returns
        the current tier with a warning reason.
        """
        try:
            current_idx = TIER_ORDER.index(current_tier)
        except ValueError:
            current_idx = 1  # default to standard

        next_idx = current_idx + 1
        if next_idx >= len(TIER_ORDER):
            # Already at premium; return with warning
            return Route(
                provider="ollama",
                model="llama3.1:8b",
                tier=current_tier,
                reason="already at premium tier; no larger tier available",
            )

        next_tier = TIER_ORDER[next_idx]
        tier = self._tiers.get(next_tier)
        if tier is None or not tier.providers:
            return Route(
                provider="ollama",
                model="llama3.1:8b",
                tier=next_tier,
                reason=f"tier '{next_tier}' has no providers",
            )

        first = tier.providers[0]
        return Route(
            provider=first.provider,
            model=first.model,
            tier=next_tier,
            reason=f"rotation from '{current_tier}' to '{next_tier}' (sequential)",
        )

    # ── Budget degradation ─────────────────────────────────────────

    def get_budget_degradation_tier(
        self,
        original_tier: str,
        pressure: float,
        is_critical: bool = False,
    ) -> str:
        """Determine the degraded tier based on daily budget pressure.

        Thresholds (from models.yaml budget_degradation config):
          0.80 = warning → prefer cheaper tier (but don't force)
          0.90 = force fast tier for non-critical tasks
          0.95 = force free tier for all non-critical tasks
          1.00 = hard stop (handled by executor, not here)

        Parameters
        ----------
        original_tier:
            The tier that routing logic originally selected.
        pressure:
            Daily budget pressure ratio (0.0 to 1.0+).
        is_critical:
            Whether the task has critical priority (critical tasks
            bypass degradation thresholds).

        Returns
        -------
        str
            The potentially degraded tier ID.
        """
        # Load thresholds from config, with sensible defaults
        budget_cfg = self._config.get("budget_degradation", {})
        warning_threshold = budget_cfg.get("warning_threshold", 0.80)
        pressure_threshold = budget_cfg.get("pressure_threshold", 0.90)
        critical_threshold = budget_cfg.get("critical_threshold", 0.95)

        # Critical tasks bypass degradation
        if is_critical:
            return original_tier

        # No budget configured
        if pressure <= 0:
            return original_tier

        # Hard stop threshold (executor handles suspend)
        if pressure >= 1.0:
            logger.warning(
                "Budget hard stop: pressure=%.2f, tier forced to free",
                pressure,
            )
            return "free"

        # Critical threshold (95%): force free tier for non-critical
        if pressure >= critical_threshold:
            logger.warning(
                "Budget critical: pressure=%.2f, forcing free tier",
                pressure,
            )
            return "free"

        # Pressure threshold (90%): force fast tier for non-critical
        if pressure >= pressure_threshold:
            logger.info(
                "Budget pressure: pressure=%.2f, forcing fast tier",
                pressure,
            )
            return "fast"

        # Warning threshold (80%): prefer cheaper tier (but keep current
        # tier if it's already fast or free)
        if pressure >= warning_threshold and original_tier not in ("fast", "free"):
            logger.info(
                "Budget warning: pressure=%.2f, downgrading from %s to standard",
                pressure,
                original_tier,
            )
            return "standard"

        return original_tier

    # ── Routing logic ────────────
    def _parse_providers(self) -> None:
        for pid, pconf in self._config.get("providers", {}).items():
            self._providers[pid] = ProviderConfig(
                id=pid,
                backend=pconf.get("backend", pid),
                default_model=pconf.get("default_model", ""),
                api_base=pconf.get("api_base", ""),
                oauth2=pconf.get("oauth2") or {},
                rate_limit=pconf.get("rate_limit") or {},
                server=pconf.get("server") or {},
                hardware=pconf.get("hardware") or {},
                inference=pconf.get("inference") or {},
                models=pconf.get("models") or {},
                model_dir=pconf.get("model_dir", "./models"),
            )

    def _parse_tiers(self) -> None:
        for tid, tconf in self._config.get("tiers", {}).items():
            providers = [
                Provider(provider=p["provider"], model=p["model"])
                for p in tconf.get("providers", [])
            ]
            self._tiers[tid] = Tier(
                id=tid,
                description=tconf.get("description", ""),
                providers=providers,
            )

    # ── Domain detection ─────────────────────────────────────────────

    @staticmethod
    def detect_domain(task_prompt: str) -> str | None:
        """Detect the primary domain of a task from keyword heuristics.

        Scans the lowercased task prompt for domain-specific keywords and
        returns the domain with the most matches, or ``None`` if no domain
        has at least two keyword hits.

        Parameters
        ----------
        task_prompt:
            The user-facing task instruction or prompt text.

        Returns
        -------
        str | None
            The detected domain name (e.g. ``"finance"``, ``"security"``)
            or ``None`` if no strong match is found.
        """
        lower = task_prompt.lower()
        scores: dict[str, int] = {}
        for domain, keywords in DOMAIN_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in lower)
            if count >= 2:
                scores[domain] = count
        if not scores:
            return None
        return max(scores, key=scores.get)  # type: ignore[arg-type]

    @staticmethod
    def domain_to_context(domain: str) -> str | None:
        """Map a detected domain to a routing context string.

        Returns a context value that can be matched by routing rules in
        ``models.yaml``, or ``None`` if no mapping exists.
        """
        mapping: dict[str, str] = {
            "finance": "domain_finance",
            "legal": "domain_legal",
            "security": "domain_security",
            "code_review": "domain_code_review",
            "deployment": "domain_deployment",
            "data_science": "domain_data_science",
        }
        return mapping.get(domain)

    # ── Complexity Scoring ──────────────────────────────────────────────

    @staticmethod
    def detect_task_type(task_prompt: str) -> str:
        """Detect the primary task type from the prompt.

        Returns a task_type key (e.g. "read_only", "debugging", "architecture")
        that maps to the ``task_type_routing`` section of ``models.yaml``.
        Falls back to ``"general"`` if no strong match.
        """
        lower = task_prompt.lower()

        # Score each task type by keyword matches (skip "general" catch-all)
        scores: dict[str, int] = {}
        for task_type, keywords in TASK_TYPE_KEYWORDS.items():
            if task_type == "general" or not keywords:
                continue
            matches = sum(1 for kw in keywords if kw in lower)
            if matches > 0:
                scores[task_type] = matches

        if not scores:
            return "general"

        # Return the task type with the most keyword matches
        return max(scores, key=scores.get)  # type: ignore[arg-type]

    @staticmethod
    def score_complexity(task_prompt: str, agent_type: str | None = None) -> ComplexityScore:
        """Score task complexity and recommend a tier.

        Args:
            task_prompt: The task instruction/prompt.
            agent_type: Type of agent (executive, specialist, etc.).

        Returns:
            ComplexityScore with score, recommended tier, and factors.
        """
        lower = task_prompt.lower()
        factors: list[str] = []
        score = 20  # Base score

        # Factor 1: Task length (longer = more complex)
        word_count = len(task_prompt.split())
        if word_count > 100:
            score += 15
            factors.append(f"long_prompt({word_count}w)")
        elif word_count > 50:
            score += 8
            factors.append(f"medium_prompt({word_count}w)")

        # Factor 2: Simple task keywords (reduce score)
        simple_matches = 0
        for category, keywords in SIMPLE_TASK_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in lower)
            if matches:
                simple_matches += matches
                factors.append(f"simple:{category}({matches})")

        if simple_matches >= 3:
            score -= 15
        elif simple_matches >= 1:
            score -= 8

        # Factor 3: Complex task keywords (increase score)
        complex_matches = 0
        for category, keywords in COMPLEX_TASK_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in lower)
            if matches:
                complex_matches += matches
                factors.append(f"complex:{category}({matches})")

        if complex_matches >= 3:
            score += 25
        elif complex_matches >= 1:
            score += 12

        # Factor 4: Technical indicators
        tech_indicators = [
            (r"\b(async|await|promise|callback)\b", "async"),
            (r"\b(thread|process|concurrent|parallel)\b", "concurrency"),
            (r"\b(database|sql|query|migration|schema)\b", "database"),
            (r"\b(docker|kubernetes|deploy|ci/cd|pipeline)\b", "devops"),
            (r"\b(test|pytest|mock|fixture|coverage)\b", "testing"),
            (r"\b(auth|oauth|jwt|token|permission)\b", "auth"),
            (r"\b(api|rest|graphql|grpc|endpoint)\b", "api"),
            (r"\b(refactor|pattern|solid|clean code|architecture)\b", "architecture"),
        ]

        for pattern, label in tech_indicators:
            if re.search(pattern, lower):
                score += 5
                factors.append(f"tech:{label}")

        # Factor 5: Agent type modifier
        if agent_type:
            agent_modifiers = {
                "executive": 10,  # Executives do planning → more complex
                "board": 15,  # Board does governance → more complex
                "department": 5,  # Dept heads coordinate → moderate
                "specialist": 0,  # Specialists execute → base complexity
            }
            mod = agent_modifiers.get(agent_type.lower(), 0)
            if mod:
                score += mod
                factors.append(f"agent:{agent_type}(+{mod})")

        # Factor 6: Multiple steps indicated
        step_indicators = ["then", "after", "next", "followed by", "step", "phase"]
        step_count = sum(1 for ind in step_indicators if ind in lower)
        if step_count >= 2:
            score += 10
            factors.append(f"multi_step({step_count})")

        # Clamp score
        score = max(0, min(100, score))

        # Determine tier
        if score <= COMPLEXITY_THRESHOLDS["fast"]:
            tier = "fast"
        elif score <= COMPLEXITY_THRESHOLDS["standard"]:
            tier = "standard"
        else:
            tier = "premium"

        task_type = ModelRouter.detect_task_type(task_prompt)

        return ComplexityScore(
            score=score,
            tier=tier,
            factors=factors,
            task_type=task_type,
        )

    def resolve_with_complexity(
        self,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        priority: str = "medium",
        context: Optional[str] = None,
        task_prompt: Optional[str] = None,
        cost_tracker: Any = None,
    ) -> Route:
        """Resolve model with complexity-aware routing.

        This extends the standard resolve() by considering task complexity
        to potentially downgrade/upgrade the tier for cost efficiency.
        """
        # Get base route (passes cost_tracker for budget degradation)
        base_route = self.resolve(
            agent_name=agent_name,
            agent_type=agent_type,
            priority=priority,
            context=context,
            task_prompt=task_prompt,
            cost_tracker=cost_tracker,
        )

        # If per-agent override or explicit context, don't adjust
        if base_route.tier in ("override", "escalation", "approval"):
            return base_route

        # Score complexity if we have a task prompt
        if task_prompt:
            complexity = self.score_complexity(task_prompt, agent_type)

            # If complexity suggests a different tier, consider it
            # But only downgrade (never upgrade beyond base) for safety
            base_tier_idx = (
                TIER_ORDER.index(base_route.tier) if base_route.tier in TIER_ORDER else 1
            )
            complexity_tier_idx = (
                TIER_ORDER.index(complexity.tier) if complexity.tier in TIER_ORDER else 1
            )

            # Use the lower tier (cheaper) if complexity allows
            # But respect priority: high/critical tasks don't downgrade
            if priority in ("high", "critical"):
                final_tier_idx = base_tier_idx
                reason_suffix = f"; priority={priority} prevents downgrade"
            else:
                final_tier_idx = min(base_tier_idx, complexity_tier_idx)
                reason_suffix = f"; complexity={complexity.score}({complexity.tier})"

            final_tier = TIER_ORDER[final_tier_idx]

            if final_tier != base_route.tier:
                # Re-resolve with adjusted tier
                tier = self._tiers.get(final_tier)
                if tier and tier.providers:
                    first = tier.providers[0]
                    fallback_names = [p.provider for p in tier.providers[1:]]
                    return Route(
                        provider=first.provider,
                        model=first.model,
                        tier=final_tier,
                        reason=f"{base_route.reason}{reason_suffix} (downgraded from {base_route.tier})"
                        if fallback_names
                        else f"{base_route.reason}{reason_suffix}",
                    )

        return base_route

    # ── Routing logic ────────────────────────────────────────────────

    def _match_rule(
        self,
        agent_type: Optional[str] = None,
        priority: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Optional[str]:
        """Find the first routing rule that matches, return its tier.

        Context rules (escalation, approval, domain) always win over
        agent-type rules.
        """
        # Pass 1: context rules always take precedence
        if context:
            for rule in self._routing:
                if rule.get("context") == context:
                    return rule.get("tier")

        # Pass 2: agent type + priority rules
        if agent_type:
            for rule in self._routing:
                if rule.get("agent_type") == agent_type:
                    rule_priority = rule.get("priority")
                    if rule_priority is None or rule_priority == priority:
                        return rule.get("tier")

        return None

    def _resolve_tier_id(
        self,
        agent_name: Optional[str],
        agent_type: Optional[str],
        priority: str,
        context: Optional[str],
        task_prompt: Optional[str],
    ) -> tuple[str, str]:
        """Resolve the tier ID and the reason string.

        Returns a ``(tier_id, reason)`` tuple.
        """
        # Layer 0: Explicit context rules take precedence over per-agent override
        # for high-priority contexts (escalation, approval)
        if context:
            for rule in self._routing:
                if rule.get("context") == context:
                    tier_id = rule.get("tier")
                    if tier_id and (tier_id in self._tiers or tier_id in SPECIAL_TIER_IDS):
                        return tier_id, f"routing rule (context={context})"

        # Layer 1: per-agent override (returns "override" tier ID)
        if agent_name and agent_name in self._registry:
            agent = self._registry[agent_name]
            if agent.get("model"):
                return (
                    "override",
                    f"per-agent override in registry for '{agent_name}'",
                )
            if agent_type is None:
                agent_type = agent.get("type")

        # Layer 2: domain-aware detection from task prompt
        if task_prompt:
            domain = self.detect_domain(task_prompt)
            if domain:
                domain_ctx = self.domain_to_context(domain)
                if domain_ctx:
                    tier_id = self._match_rule(
                        agent_type=agent_type,
                        priority=priority,
                        context=domain_ctx,
                    )
                    if tier_id is not None and (
                        tier_id in self._tiers or tier_id in SPECIAL_TIER_IDS
                    ):
                        return (
                            tier_id,
                            f"domain-aware: '{domain}' detected → context '{domain_ctx}'",
                        )

        # Layer 3: task-type routing (detected from prompt keywords)
        if task_prompt:
            task_type = self.detect_task_type(task_prompt)
            task_type_routing = self._config.get("task_type_routing", {})
            if task_type in task_type_routing:
                task_tier = task_type_routing[task_type]
                if task_tier in self._tiers or task_tier in SPECIAL_TIER_IDS:
                    return (
                        task_tier,
                        f"task-type: '{task_type}' detected from prompt",
                    )

        # Layer 4: agent type + priority rules (no context)
        tier_id = self._match_rule(agent_type=agent_type, priority=priority, context=None)
        if tier_id is not None and (tier_id in self._tiers or tier_id in SPECIAL_TIER_IDS):
            return tier_id, f"routing rule (agent_type={agent_type}, priority={priority})"

        # Layer 5: fallback
        return "standard", "fallback to 'standard' tier"

    def resolve(
        self,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        priority: str = "medium",
        context: Optional[str] = None,
        task_prompt: Optional[str] = None,
        cost_tracker: Any = None,
    ) -> Route:
        """Resolve which model to use.

        Parameters
        ----------
        agent_name:
            Registry name of the agent (triggers per-agent override).
        agent_type:
            Agent type (``"executive"``, ``"specialist"``, etc.).
        priority:
            Task priority (``"low"``, ``"medium"``, ``"high"``, ``"critical"``).
        context:
            Explicit routing context (e.g. ``"escalation"``, ``"approval"``).
        task_prompt:
            Raw task text used for domain-aware detection.
        cost_tracker:
            Optional CostTracker instance for budget degradation.

        Returns
        -------
        Route
            The resolved provider, model, tier, and reason.
        """
        tier_id, reason = self._resolve_tier_id(
            agent_name, agent_type, priority, context, task_prompt
        )

        # Layer 1 special case: per-agent override
        if tier_id == "override" and agent_name and agent_name in self._registry:
            agent = self._registry[agent_name]
            override = agent["model"]
            if "/" in override:
                prov, model = override.split("/", 1)
            else:
                prov, model = "ollama", override
            return Route(
                provider=prov,
                model=model,
                tier="override",
                reason=reason,
            )

        # Apply budget degradation if cost_tracker is provided
        # Skip degradation for override, escalation, and approval contexts
        # (these are safety-critical and must not be degraded)
        _safety_contexts = {"escalation", "approval"}
        if cost_tracker is not None and tier_id != "override" and context not in _safety_contexts:
            pressure = cost_tracker.daily_pressure()
            is_critical = priority == "critical"
            degraded_tier = self.get_budget_degradation_tier(tier_id, pressure, is_critical)
            if degraded_tier != tier_id:
                reason = (
                    f"{reason} [budget degradation: {tier_id}→{degraded_tier} "
                    f"(pressure={pressure:.2f})]"
                )
                tier_id = degraded_tier

        # Free tier: use dynamic catalog (sync lookup from cache)
        if tier_id == "free":
            return self._resolve_free_tier(reason)

        tier = self._tiers.get(tier_id)
        if tier is None or not tier.providers:
            return Route(
                provider="ollama",
                model="llama3.1:8b",
                tier=tier_id,
                reason=f"{reason}; tier '{tier_id}' has no providers, using hardcoded fallback",
            )

        first = tier.providers[0]
        fallback_names = [p.provider for p in tier.providers[1:]]
        return Route(
            provider=first.provider,
            model=first.model,
            tier=tier_id,
            reason=f"{reason} (fallbacks: {', '.join(fallback_names)})"
            if fallback_names
            else reason,
        )

    def _resolve_free_tier(self, reason: str) -> Route:
        """Resolve a route for the free tier using the dynamic catalog.

        Returns the best available free model from the cached catalog.
        Falls back to static providers if catalog is not cached.
        """
        catalog = self._get_cached_free_models()
        if catalog:
            # Return the model with the largest context window (first in sorted list)
            best = catalog[0]
            return Route(
                provider=best.provider,
                model=best.model,
                tier="free",
                reason=f"{reason} (dynamic free catalog: {best.name}, {best.context} ctx)",
            )

        # Fallback: use static free_tier config from models.yaml
        free_tier_config = self._config.get("free_tier", {})
        static_fallback = free_tier_config.get("static_fallback", [])
        if static_fallback:
            first = static_fallback[0]
            return Route(
                provider=first["provider"],
                model=first["model"],
                tier="free",
                reason=f"{reason} (static fallback; catalog unavailable)",
            )

        # Last resort: hardcoded fallback
        return Route(
            provider="ollama",
            model="llama3.1:8b",
            tier="free",
            reason=f"{reason} (no free models available, using ollama fallback)",
        )

    # ── Quality-based fallback ───────────────────────────────────────

    def get_fallback_tier(self, failed_tier_id: str) -> Optional[Tier]:
        """Return the next higher tier for quality-based fallback.

        When all providers in the current tier fail, callers can use this
        method to promote to the next tier (fast → standard → premium).

        Parameters
        ----------
        failed_tier_id:
            The tier ID that just failed.

        Returns
        -------
        Tier | None
            The next tier, or ``None`` if no higher tier exists.
        """
        try:
            idx = TIER_ORDER.index(failed_tier_id)
        except ValueError:
            return None
        for next_id in TIER_ORDER[idx + 1 :]:
            tier = self._tiers.get(next_id)
            if tier and tier.providers:
                return tier
        return None

    def resolve_with_fallback(
        self,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        priority: str = "medium",
        context: Optional[str] = None,
        task_prompt: Optional[str] = None,
        cost_tracker: Any = None,
    ) -> list[Route]:
        """Resolve the primary route plus fallback chain for quality escalation.

        Returns an ordered list of ``Route`` objects starting with the
        primary choice and followed by fallback tiers.  Callers can iterate
        through the list when the primary tier's providers are all
        unavailable or return errors.

        Parameters
        ----------
        agent_name:
            Registry name of the agent.
        agent_type:
            Agent type.
        priority:
            Task priority.
        context:
            Explicit routing context.
        task_prompt:
            Raw task text for domain detection.
        cost_tracker:
            Optional CostTracker instance for budget degradation.

        Returns
        -------
        list[Route]
            Primary route first, then fallback routes in tier order.
        """
        primary = self.resolve(
            agent_name=agent_name,
            agent_type=agent_type,
            priority=priority,
            context=context,
            task_prompt=task_prompt,
            cost_tracker=cost_tracker,
        )
        routes: list[Route] = [primary]

        fallback_tier = self.get_fallback_tier(primary.tier)
        seen: set[str] = {primary.tier}
        while fallback_tier is not None:
            if fallback_tier.id not in seen:
                first = fallback_tier.providers[0]
                routes.append(
                    Route(
                        provider=first.provider,
                        model=first.model,
                        tier=fallback_tier.id,
                        reason=f"quality fallback from '{primary.tier}'",
                    )
                )
                seen.add(fallback_tier.id)
            fallback_tier = self.get_fallback_tier(fallback_tier.id)

        return routes

    # ── Introspection ────────────────────────────────────────────────

    def get_tier(self, tier_id: str) -> Optional[Tier]:
        return self._tiers.get(tier_id)

    def get_provider(self, provider_id: str) -> Optional[ProviderConfig]:
        return self._providers.get(provider_id)

    def list_tiers(self) -> list[Tier]:
        return list(self._tiers.values())

    def list_providers(self) -> list[ProviderConfig]:
        return list(self._providers.values())

    def resolve_all_agents(self) -> dict[str, Route]:
        """Resolve model routing for every agent in the registry."""
        results: dict[str, Route] = {}
        for name, _agent in self._registry.items():
            results[name] = self.resolve(agent_name=name)
        return results
