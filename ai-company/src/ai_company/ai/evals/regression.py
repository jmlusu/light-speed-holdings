"""Prompt regression testing — track prompt quality over time.

Provides snapshot-based regression detection: save prompt output
snapshots and compare new outputs against historical baselines.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PromptSnapshot:
    """A captured snapshot of a prompt's behavior at a point in time."""

    prompt_id: str
    variant: str
    system_prompt: str
    user_input: str
    output: str
    score: float
    model_used: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


class RegressionDetector:
    """Detects prompt quality regressions by comparing snapshots.

    Maintains a history of prompt snapshots and can compare new outputs
    against historical baselines to flag quality drops.

    Args:
        storage_dir: Directory for storing snapshot history.
    """

    def __init__(self, storage_dir: str | Path = "results/evals/snapshots") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._snapshots: dict[str, list[PromptSnapshot]] = {}
        self._load_all()

    def record(
        self,
        prompt_id: str,
        variant: str,
        system_prompt: str,
        user_input: str,
        output: str,
        score: float,
        model_used: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> PromptSnapshot:
        """Record a new prompt snapshot."""
        snap = PromptSnapshot(
            prompt_id=prompt_id,
            variant=variant,
            system_prompt=system_prompt,
            user_input=user_input,
            output=output,
            score=score,
            model_used=model_used,
            metadata=metadata or {},
        )

        key = f"{prompt_id}::{variant}"
        if key not in self._snapshots:
            self._snapshots[key] = []
        self._snapshots[key].append(snap)
        self._save(key)
        return snap

    def detect_regression(
        self,
        prompt_id: str,
        variant: str,
        current_score: float,
        threshold: float = 0.1,
        window: int = 10,
    ) -> dict[str, Any] | None:
        """Check if the current score represents a regression.

        Args:
            prompt_id: The prompt identifier.
            variant: The prompt variant.
            current_score: The score of the latest output.
            threshold: Maximum allowed score drop (0.0-1.0).
            window: Number of recent snapshots to consider for baseline.

        Returns:
            Regression info dict if regression detected, else None.
        """
        key = f"{prompt_id}::{variant}"
        snaps = self._snapshots.get(key, [])
        if not snaps:
            return None

        # Use the last N snapshots (excluding the current one) as baseline
        recent = snaps[-(window + 1):-1] if len(snaps) > window else snaps[:-1]
        if not recent:
            return None

        baseline_scores = [s.score for s in recent]
        baseline_mean = sum(baseline_scores) / len(baseline_scores)
        baseline_min = min(baseline_scores)

        drop_from_mean = baseline_mean - current_score
        drop_from_min = baseline_min - current_score

        if drop_from_mean > threshold or drop_from_min > threshold * 0.5:
            return {
                "prompt_id": prompt_id,
                "variant": variant,
                "current_score": current_score,
                "baseline_mean": round(baseline_mean, 4),
                "baseline_min": round(baseline_min, 4),
                "drop_from_mean": round(drop_from_mean, 4),
                "drop_from_min": round(drop_from_min, 4),
                "window_size": len(recent),
                "severity": "critical" if drop_from_mean > threshold * 2 else "warning",
            }
        return None

    def get_history(
        self,
        prompt_id: str,
        variant: str = "",
        limit: int = 50,
    ) -> list[PromptSnapshot]:
        """Get snapshot history for a prompt, optionally filtered by variant."""
        results: list[PromptSnapshot] = []
        for key, snaps in self._snapshots.items():
            pid, var = key.split("::", 1) if "::" in key else (key, "")
            if pid == prompt_id and (not variant or var == variant):
                results.extend(snaps)
        results.sort(key=lambda s: s.timestamp, reverse=True)
        return results[:limit]

    def get_stats(self, prompt_id: str, variant: str = "") -> dict[str, Any]:
        """Get aggregated stats for a prompt's snapshot history."""
        snaps = self.get_history(prompt_id, variant, limit=1000)
        if not snaps:
            return {"prompt_id": prompt_id, "variant": variant, "count": 0}

        scores = [s.score for s in snaps]
        return {
            "prompt_id": prompt_id,
            "variant": variant,
            "count": len(snaps),
            "mean_score": round(sum(scores) / len(scores), 4),
            "min_score": round(min(scores), 4),
            "max_score": round(max(scores), 4),
            "latest_score": round(snaps[0].score, 4),
            "first_seen": snaps[-1].timestamp,
            "last_seen": snaps[0].timestamp,
        }

    # ── Persistence ────────────────────────────────────────────────

    def _file_path(self, key: str) -> Path:
        safe_name = key.replace("::", "__").replace("/", "__")
        return self.storage_dir / f"{safe_name}.json"

    def _save(self, key: str) -> None:
        snaps = self._snapshots.get(key, [])
        data = [
            {
                "prompt_id": s.prompt_id,
                "variant": s.variant,
                "system_prompt": s.system_prompt,
                "user_input": s.user_input,
                "output": s.output,
                "score": s.score,
                "model_used": s.model_used,
                "timestamp": s.timestamp,
                "metadata": s.metadata,
            }
            for s in snaps
        ]
        self._file_path(key).write_text(
            json.dumps(data, indent=2, default=str),
            encoding="utf-8",
        )

    def _load_all(self) -> None:
        for path in self.storage_dir.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                for item in data:
                    snap = PromptSnapshot(
                        prompt_id=item["prompt_id"],
                        variant=item["variant"],
                        system_prompt=item["system_prompt"],
                        user_input=item["user_input"],
                        output=item["output"],
                        score=item["score"],
                        model_used=item.get("model_used", ""),
                        timestamp=item.get("timestamp", ""),
                        metadata=item.get("metadata", {}),
                    )
                    key = f"{snap.prompt_id}::{snap.variant}"
                    if key not in self._snapshots:
                        self._snapshots[key] = []
                    self._snapshots[key].append(snap)
            except (json.JSONDecodeError, KeyError, OSError) as exc:
                logger.warning("Failed to load snapshot %s: %s", path.name, exc)
