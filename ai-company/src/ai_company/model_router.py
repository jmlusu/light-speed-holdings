"""Model routing policy — resolves which LLM to use for a given agent and task."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


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
    """Reads company/models.yaml and resolves model routing decisions."""

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

    # ── Routing logic ────────────────────────────────────────────────

    def _match_rule(
        self,
        agent_type: Optional[str] = None,
        priority: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Optional[str]:
        """Find the first routing rule that matches, return its tier.

        Context rules (escalation, approval) always win over agent-type rules.
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

    def resolve(
        self,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        priority: str = "medium",
        context: Optional[str] = None,
    ) -> Route:
        """Resolve which model to use.

        Priority order:
          1. Per-agent override in agent-registry.json ("model" field)
          2. Context rules (escalation, approval) — always win
          3. Routing rule match -> tier -> first reachable provider
          4. Fallback to "standard" tier
        """
        # Layer 1: per-agent override
        if agent_name and agent_name in self._registry:
            agent = self._registry[agent_name]
            override = agent.get("model")
            if override:
                # Parse "provider/model" or just "model"
                if "/" in override:
                    prov, model = override.split("/", 1)
                else:
                    prov, model = "ollama", override
                return Route(
                    provider=prov,
                    model=model,
                    tier="override",
                    reason=f"per-agent override in registry for '{agent_name}'",
                )
            # Infer type from registry if not provided
            if agent_type is None:
                agent_type = agent.get("type")

        # Layer 2: routing rules (context wins over agent-type)
        tier_id = self._match_rule(
            agent_type=agent_type, priority=priority, context=context
        )

        # Layer 3: fallback
        if tier_id is None or tier_id not in self._tiers:
            tier_id = "standard"

        tier = self._tiers[tier_id]
        if not tier.providers:
            return Route(
                provider="ollama",
                model="llama3.1:8b",
                tier=tier_id,
                reason=f"tier '{tier_id}' has no providers, using hardcoded fallback",
            )

        # Return the first provider in the tier (fallback chain is for runtime)
        first = tier.providers[0]
        return Route(
            provider=first.provider,
            model=first.model,
            tier=tier_id,
            reason=f"tier '{tier_id}' default (fallbacks: {', '.join(p.provider for p in tier.providers[1:])})",
        )

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
