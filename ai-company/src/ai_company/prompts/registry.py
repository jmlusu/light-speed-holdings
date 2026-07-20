"""Version-controlled prompt registry with A/B test support and rollback.

Prompts are stored as JSON files under ``.opencode/prompt-versions/``.
Each prompt has a unique ``prompt_id`` and multiple versioned entries.

Features:
- Immutable version history (each edit creates a new version)
- A/B test traffic splitting
- Rollback to any previous version
- Metadata tags for filtering (agent_type, domain, etc.)
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PromptVersion:
    """A single immutable version of a prompt."""

    prompt_id: str
    version: int
    content: str
    created_at: float = field(default_factory=time.time)
    author: str = "system"
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    hash: str = ""
    active: bool = True

    def __post_init__(self) -> None:
        if not self.hash:
            self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """SHA-256 of prompt_id + content for deduplication."""
        payload = f"{self.prompt_id}:{self.content}".encode()
        return hashlib.sha256(payload).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PromptVersion:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ABTestConfig:
    """Configuration for A/B testing between prompt versions."""

    prompt_id: str
    variant_a_version: int
    variant_b_version: int
    traffic_split: float = 0.5  # fraction going to variant A
    enabled: bool = True
    started_at: float = field(default_factory=time.time)

    def pick_variant(self) -> int:
        """Deterministically pick a variant based on current time hash."""
        import random

        seed = int(time.time() * 1000) % 10000
        rng = random.Random(seed)
        return (
            self.variant_a_version
            if rng.random() < self.traffic_split
            else self.variant_b_version
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PromptRegistry:
    """Central registry for versioned prompts with A/B test support.

    Storage layout::

        .opencode/prompt-versions/
            <prompt_id>/
                versions.json      — list of all versions
                ab_test.json       — active A/B test config (if any)

    Usage::

        registry = PromptRegistry()
        # Register a new prompt
        version = registry.register("exec.system", "You are an executive...")
        # Update (creates new version)
        v2 = registry.register("exec.system", "You are a senior executive...")
        # Rollback
        registry.rollback("exec.system", target_version=1)
        # A/B test
        registry.start_ab_test("exec.system", variant_a=1, variant_b=2)
    """

    def __init__(self, storage_dir: str = ".opencode/prompt-versions") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    def register(
        self,
        prompt_id: str,
        content: str,
        *,
        author: str = "system",
        tags: list[str] | None = None,
        notes: str = "",
    ) -> PromptVersion:
        """Register a new version of a prompt.

        If the content is identical to the latest version, returns the
        existing version without creating a duplicate.
        """
        versions = self._load_versions(prompt_id)

        # Dedup: skip if content unchanged
        if versions:
            latest = versions[-1]
            if latest.content == content:
                return latest

        new_version = PromptVersion(
            prompt_id=prompt_id,
            version=len(versions) + 1,
            content=content,
            author=author,
            tags=tags or [],
            notes=notes,
        )
        versions.append(new_version)
        self._save_versions(prompt_id, versions)
        return new_version

    def get(
        self, prompt_id: str, version: int | None = None
    ) -> PromptVersion | None:
        """Get a specific version, or the latest if version is None.

        Respects active A/B test configuration if present — returns the
        randomly selected variant.
        """
        versions = self._load_versions(prompt_id)
        if not versions:
            return None

        # Check for active A/B test
        ab_test = self._load_ab_test(prompt_id)
        if ab_test and ab_test.enabled and version is None:
            variant = ab_test.pick_variant()
            for v in versions:
                if v.version == variant:
                    return v

        if version is None:
            # Return the latest active version
            for v in reversed(versions):
                if v.active:
                    return v
            return versions[-1]

        for v in versions:
            if v.version == version:
                return v
        return None

    def rollback(self, prompt_id: str, target_version: int) -> PromptVersion | None:
        """Deactivate all versions after ``target_version``.

        Returns the rolled-back-to version, or None if not found.
        """
        versions = self._load_versions(prompt_id)
        if not versions:
            return None

        target = None
        for v in versions:
            if v.version == target_version:
                target = v
                v.active = True
            elif v.version > target_version:
                v.active = False

        if target:
            self._save_versions(prompt_id, versions)
        return target

    def list_prompts(self) -> list[str]:
        """List all registered prompt IDs."""
        prompts: list[str] = []
        for entry in sorted(self.storage_dir.iterdir()):
            if entry.is_dir() and (entry / "versions.json").exists():
                prompts.append(entry.name)
        return prompts

    def list_versions(self, prompt_id: str) -> list[PromptVersion]:
        """List all versions for a prompt."""
        return self._load_versions(prompt_id)

    def get_active_version(self, prompt_id: str) -> PromptVersion | None:
        """Get the currently active version (no A/B test override)."""
        versions = self._load_versions(prompt_id)
        for v in reversed(versions):
            if v.active:
                return v
        return versions[-1] if versions else None

    # ------------------------------------------------------------------
    # A/B Testing
    # ------------------------------------------------------------------

    def start_ab_test(
        self,
        prompt_id: str,
        variant_a: int,
        variant_b: int,
        traffic_split: float = 0.5,
    ) -> ABTestConfig:
        """Start an A/B test between two versions."""
        config = ABTestConfig(
            prompt_id=prompt_id,
            variant_a_version=variant_a,
            variant_b_version=variant_b,
            traffic_split=traffic_split,
        )
        ab_path = self.storage_dir / prompt_id / "ab_test.json"
        ab_path.parent.mkdir(parents=True, exist_ok=True)
        ab_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
        return config

    def stop_ab_test(self, prompt_id: str) -> None:
        """Stop the active A/B test for a prompt."""
        ab_path = self.storage_dir / prompt_id / "ab_test.json"
        if ab_path.exists():
            ab_path.unlink()

    def _load_ab_test(self, prompt_id: str) -> ABTestConfig | None:
        ab_path = self.storage_dir / prompt_id / "ab_test.json"
        if not ab_path.exists():
            return None
        try:
            data = json.loads(ab_path.read_text(encoding="utf-8"))
            return ABTestConfig(**data)
        except (json.JSONDecodeError, TypeError):
            return None

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def export_all(self) -> dict[str, list[dict[str, Any]]]:
        """Export all prompts and versions as a serialisable dict."""
        result: dict[str, list[dict[str, Any]]] = {}
        for prompt_id in self.list_prompts():
            result[prompt_id] = [
                v.to_dict() for v in self._load_versions(prompt_id)
            ]
        return result

    def import_from_dict(self, data: dict[str, list[dict[str, Any]]]) -> int:
        """Import prompts from an exported dict. Returns count imported."""
        count = 0
        for prompt_id, version_dicts in data.items():
            for vd in version_dicts:
                pv = PromptVersion.from_dict(vd)
                self.register(
                    prompt_id,
                    pv.content,
                    author=pv.author,
                    tags=pv.tags,
                    notes=pv.notes,
                )
                count += 1
        return count

    # ------------------------------------------------------------------
    # Internal storage
    # ------------------------------------------------------------------

    def _load_versions(self, prompt_id: str) -> list[PromptVersion]:
        path = self.storage_dir / prompt_id / "versions.json"
        if not path.exists():
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return [PromptVersion.from_dict(v) for v in raw]
        except (json.JSONDecodeError, TypeError):
            return []

    def _save_versions(
        self, prompt_id: str, versions: list[PromptVersion]
    ) -> None:
        path = self.storage_dir / prompt_id / "versions.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [v.to_dict() for v in versions]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
