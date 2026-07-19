"""Model routing policy — resolves which LLM to use for a given agent and task.

Supports three routing layers:
  1. Per-agent override (agent-registry.json ``model`` field)
  2. Routing rules (context → tier, agent_type + priority → tier)
  3. Fallback to ``standard`` tier

Context-aware routing detects domain keywords in the task prompt and
selects the appropriate tier.  Quality-based fallback promotes to the
next higher tier when all providers in the current tier fail.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


# ---------------------------------------------------------------------------
# Domain → tier mapping for context-aware routing
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "finance": ["financial", "finance", "accounting", "budget", "revenue",
                "profit", "loss", "balance sheet", "cash flow", "invoice",
                "tax", "audit", "compliance", "ledger"],
    "legal": ["legal", "contract", "agreement", "liability", "regulation",
              "statute", "litigation", "intellectual property", "patent",
              "trademark", "nda", "terms of service"],
    "security": ["security", "vulnerability", "exploit", "breach", "auth",
                 "encryption", "secret", "credential", "firewall", "pentest",
                 "owasp", "cve"],
    "code_review": ["review", "pull request", "pr", "code review", "diff",
                    "merge", "refactor", "lint", "static analysis"],
    "deployment": ["deploy", "release", "production", "rollback", "ci/cd",
                   "pipeline", "kubernetes", "docker", "terraform"],
    "data_science": ["model", "training", "inference", "dataset", "feature",
                     "accuracy", "precision", "recall", "f1", "epoch",
                     "hyperparameter", "ml", "machine learning", "neural"],
}

# Ordered tier progression for quality-based fallback
TIER_ORDER: list[str] = ["fast", "standard", "premium"]


@dataclass(frozen=True)
class Provider:
    """A single provider entry within a tier."""

    provider: str
    model: str


@dataclass(frozen=True)
class ProviderConfig:
    """Top-level provider configuration (backend, api_base, etc.)."""

    id: str
    backend: str
    default_model: str
    api_base: str = ""


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
        self._registry: dict[str, dict] = {}
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

    def _parse_providers(self) -> None:
        for pid, pconf in self._config.get("providers", {}).items():
            self._providers[pid] = ProviderConfig(
                id=pid,
                backend=pconf.get("backend", pid),
                default_model=pconf.get("default_model", ""),
                api_base=pconf.get("api_base", ""),
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

        # Layer 2: explicit context rules
        tier_id = self._match_rule(
            agent_type=agent_type, priority=priority, context=context
        )
        if tier_id is not None and tier_id in self._tiers:
            return tier_id, f"routing rule (context={context})"

        # Layer 3: domain-aware detection from task prompt
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
                    if tier_id is not None and tier_id in self._tiers:
                        return (
                            tier_id,
                            f"domain-aware: '{domain}' detected → context '{domain_ctx}'",
                        )

        # Layer 4: agent type + priority rules (no context)
        tier_id = self._match_rule(
            agent_type=agent_type, priority=priority, context=None
        )
        if tier_id is not None and tier_id in self._tiers:
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
            reason=f"{reason} (fallbacks: {', '.join(fallback_names)})" if fallback_names else reason,
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
        for next_id in TIER_ORDER[idx + 1:]:
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
        for name, agent in self._registry.items():
            results[name] = self.resolve(agent_name=name)
        return results
