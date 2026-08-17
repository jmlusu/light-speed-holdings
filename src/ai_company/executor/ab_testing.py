"""A/B Testing Framework for gradual rollout of optimizations.

Provides feature flags, experiment tracking, and metrics collection
for validating token reduction optimizations.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    """Configuration for an A/B experiment."""
    name: str
    description: str
    enabled: bool = False
    traffic_split: float = 0.5  # Percentage of traffic to treatment (0.0-1.0)
    start_date: str | None = None
    end_date: str | None = None
    target_agents: list[str] = field(default_factory=list)  # Empty = all agents
    excluded_agents: list[str] = field(default_factory=list)


@dataclass
class ExperimentMetrics:
    """Metrics collected during an experiment."""
    experiment_name: str
    variant: str  # "control" or "treatment"
    task_id: str
    agent_name: str
    timestamp: str

    # Token metrics
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    # Cost metrics
    cost_usd: float = 0.0

    # Performance metrics
    iterations: int = 0
    duration_seconds: float = 0.0
    success: bool = True
    error: str = ""

    # Optimization-specific metrics
    system_prompt_tokens: int = 0
    history_tokens: int = 0
    tool_feedback_tokens: int = 0

    # Quality metrics
    task_completed: bool = False
    required_retries: int = 0


class ABTestingFramework:
    """Manages A/B experiments for optimization rollout.

    Usage:
        framework = ABTestingFramework()

        # Check if agent should use treatment
        if framework.should_use_treatment("optimized_prompts", agent_name):
            # Use optimized code path
            pass

        # Record metrics
        framework.record_metrics(ExperimentMetrics(...))
    """

    def __init__(self, config_path: str = "config/experiments.yaml"):
        self.config_path = Path(config_path)
        self._experiments: dict[str, ExperimentConfig] = {}
        self._metrics_buffer: list[ExperimentMetrics] = []
        self._lock = threading.Lock()
        self._assignment_cache: dict[str, str] = {}  # task_id -> variant
        self._load_config()

    def _load_config(self) -> None:
        """Load experiment configuration from YAML."""
        import yaml

        if not self.config_path.exists():
            logger.info("No experiment config found at %s, using defaults", self.config_path)
            self._create_default_config()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            for exp_data in data.get("experiments", []):
                config = ExperimentConfig(**exp_data)
                self._experiments[config.name] = config

            logger.info("Loaded %d experiments from %s", len(self._experiments), self.config_path)
        except (OSError, yaml.YAMLError) as e:
            logger.warning("Failed to load experiment config: %s", e)
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default experiment configuration."""
        # Default: optimized prompts experiment at 50% traffic
        self._experiments["optimized_prompts"] = ExperimentConfig(
            name="optimized_prompts",
            description="Token-efficient system prompts with conditional sections",
            enabled=True,
            traffic_split=0.5,
            target_agents=[],  # All agents
        )

        self._experiments["history_summarization"] = ExperimentConfig(
            name="history_summarization",
            description="Conversation history summarization to reduce context",
            enabled=True,
            traffic_split=0.5,
            target_agents=[],
        )

        self._experiments["tool_summarization"] = ExperimentConfig(
            name="tool_summarization",
            description="Tool result summarization for token efficiency",
            enabled=True,
            traffic_split=0.5,
            target_agents=[],
        )

        self._experiments["complexity_routing"] = ExperimentConfig(
            name="complexity_routing",
            description="Task complexity scoring for smart tier routing",
            enabled=True,
            traffic_split=0.5,
            target_agents=[],
        )

        self._save_config()

    def _save_config(self) -> None:
        """Save experiment configuration to YAML."""
        import yaml

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "experiments": [asdict(exp) for exp in self._experiments.values()]
        }

        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False)
        except (OSError, yaml.YAMLError) as e:
            logger.warning("Failed to save experiment config: %s", e)

    def should_use_treatment(
        self,
        experiment_name: str,
        agent_name: str,
        task_id: str = "",
    ) -> bool:
        """Determine if an agent/task should use the treatment variant.

        Uses consistent hashing for stable assignment across restarts.
        """
        experiment = self._experiments.get(experiment_name)
        if not experiment or not experiment.enabled:
            return False

        # Check agent targeting
        if experiment.target_agents and agent_name not in experiment.target_agents:
            return False
        if agent_name in experiment.excluded_agents:
            return False

        # Check date range
        now = datetime.now(timezone.utc).date().isoformat()
        if experiment.start_date and now < experiment.start_date:
            return False
        if experiment.end_date and now > experiment.end_date:
            return False

        # Consistent assignment based on task_id + experiment_name
        if task_id:
            cache_key = f"{experiment_name}:{task_id}"
            with self._lock:
                if cache_key in self._assignment_cache:
                    return self._assignment_cache[cache_key] == "treatment"

                # Hash-based assignment
                import hashlib
                hash_input = f"{experiment_name}:{task_id}".encode()
                hash_val = int(hashlib.md5(hash_input, usedforsecurity=False).hexdigest(), 16)
                assignment = "treatment" if (hash_val / (2**128)) < experiment.traffic_split else "control"
                self._assignment_cache[cache_key] = assignment
                return assignment == "treatment"

        # No task_id - use random assignment
        import random
        return random.random() < experiment.traffic_split

    def get_variant(self, experiment_name: str, agent_name: str, task_id: str = "") -> str:
        """Get the variant name for logging."""
        return "treatment" if self.should_use_treatment(experiment_name, agent_name, task_id) else "control"

    def record_metrics(self, metrics: ExperimentMetrics) -> None:
        """Record experiment metrics."""
        with self._lock:
            self._metrics_buffer.append(metrics)

            # Flush periodically
            if len(self._metrics_buffer) >= 100:
                self._flush_metrics()

    def _flush_metrics(self) -> None:
        """Flush metrics buffer to disk."""
        if not self._metrics_buffer:
            return

        metrics_dir = Path("results/experiments")
        metrics_dir.mkdir(parents=True, exist_ok=True)

        # Group by experiment
        by_experiment: dict[str, list[ExperimentMetrics]] = {}
        for m in self._metrics_buffer:
            by_experiment.setdefault(m.experiment_name, []).append(m)

        for exp_name, metrics_list in by_experiment.items():
            date_str = datetime.now(timezone.utc).date().isoformat()
            file_path = metrics_dir / f"{exp_name}_{date_str}.jsonl"

            try:
                with open(file_path, "a", encoding="utf-8") as f:
                    for m in metrics_list:
                        f.write(json.dumps(asdict(m)) + "\n")
            except (OSError, json.JSONDecodeError) as e:
                logger.warning("Failed to write experiment metrics: %s", e)

        self._metrics_buffer.clear()

    def get_experiment_summary(self, experiment_name: str) -> dict[str, Any]:
        """Get summary statistics for an experiment."""
        metrics_dir = Path("results/experiments")
        if not metrics_dir.exists():
            return {"error": "No metrics directory"}

        import glob
        files = glob.glob(str(metrics_dir / f"{experiment_name}_*.jsonl"))

        all_metrics: list[ExperimentMetrics] = []
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            all_metrics.append(ExperimentMetrics(**data))
            except (OSError, json.JSONDecodeError) as e:
                logger.warning("Failed to read metrics file %s: %s", file_path, e)

        if not all_metrics:
            return {"error": "No metrics found"}

        # Split by variant
        control = [m for m in all_metrics if m.variant == "control"]
        treatment = [m for m in all_metrics if m.variant == "treatment"]

        def summarize(metrics_list: list[ExperimentMetrics]) -> dict[str, Any]:
            if not metrics_list:
                return {}
            return {
                "count": len(metrics_list),
                "avg_tokens": sum(m.total_tokens for m in metrics_list) / len(metrics_list),
                "avg_cost": sum(m.cost_usd for m in metrics_list) / len(metrics_list),
                "avg_iterations": sum(m.iterations for m in metrics_list) / len(metrics_list),
                "avg_duration": sum(m.duration_seconds for m in metrics_list) / len(metrics_list),
                "success_rate": sum(1 for m in metrics_list if m.success) / len(metrics_list),
                "completion_rate": sum(1 for m in metrics_list if m.task_completed) / len(metrics_list),
            }

        return {
            "experiment": experiment_name,
            "control": summarize(control),
            "treatment": summarize(treatment),
            "total_samples": len(all_metrics),
        }

    def enable_experiment(self, name: str, traffic_split: float | None = None) -> bool:
        """Enable an experiment."""
        if name in self._experiments:
            self._experiments[name].enabled = True
            if traffic_split is not None:
                self._experiments[name].traffic_split = traffic_split
            self._save_config()
            return True
        return False

    def disable_experiment(self, name: str) -> bool:
        """Disable an experiment."""
        if name in self._experiments:
            self._experiments[name].enabled = False
            self._save_config()
            return True
        return False

    def set_traffic_split(self, name: str, split: float) -> bool:
        """Update traffic split for an experiment."""
        if name in self._experiments:
            self._experiments[name].traffic_split = max(0.0, min(1.0, split))
            self._save_config()
            return True
        return False


# Global instance for easy access
_global_framework: ABTestingFramework | None = None


def get_ab_framework() -> ABTestingFramework:
    """Get or create the global A/B testing framework."""
    global _global_framework
    if _global_framework is None:
        _global_framework = ABTestingFramework()
    return _global_framework


def should_use_optimized_prompts(agent_name: str, task_id: str = "") -> bool:
    """Convenience function for optimized prompts experiment."""
    return get_ab_framework().should_use_treatment("optimized_prompts", agent_name, task_id)


def should_use_history_summarization(agent_name: str, task_id: str = "") -> bool:
    """Convenience function for history summarization experiment."""
    return get_ab_framework().should_use_treatment("history_summarization", agent_name, task_id)


def should_use_tool_summarization(agent_name: str, task_id: str = "") -> bool:
    """Convenience function for tool summarization experiment."""
    return get_ab_framework().should_use_treatment("tool_summarization", agent_name, task_id)


def should_use_complexity_routing(agent_name: str, task_id: str = "") -> bool:
    """Convenience function for complexity routing experiment."""
    return get_ab_framework().should_use_treatment("complexity_routing", agent_name, task_id)


def record_experiment_metrics(metrics: ExperimentMetrics) -> None:
    """Convenience function to record metrics."""
    get_ab_framework().record_metrics(metrics)
