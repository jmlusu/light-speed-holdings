"""LLM response quality tracking — monitors response health over time.

Stores metrics in JSONL format for analysis. Tracks:
- Validation pass/fail rates
- Suspicious content detection rates
- Response length distributions
- Parse success rates
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ResponseQualityMetric:
    """Single response quality measurement."""

    timestamp: float = field(default_factory=time.time)
    agent_id: str = ""
    model: str = ""
    validation_passed: bool = True
    validation_reason: str = ""
    response_length: int = 0
    plan_steps: int = 0
    has_tool_calls: bool = False
    suspicious_content_detected: bool = False
    parse_success: bool = True


class ResponseQualityTracker:
    """Track LLM response quality over time for monitoring and alerting.

    Stores metrics in JSONL format for analysis.  Keeps a rolling window
    of the most recent metrics for rate calculations and alerting.
    """

    def __init__(self, log_dir: str = ".opencode/response_quality") -> None:
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_file = self._log_dir / "quality.jsonl"
        self._metrics: list[ResponseQualityMetric] = []
        self._window_size = 100  # Rolling window for rate calculations

    def record(self, metric: ResponseQualityMetric) -> None:
        """Record a response quality metric."""
        self._metrics.append(metric)

        # Append to JSONL log
        try:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {
                            "timestamp": metric.timestamp,
                            "agent_id": metric.agent_id,
                            "model": metric.model,
                            "validation_passed": metric.validation_passed,
                            "validation_reason": metric.validation_reason,
                            "response_length": metric.response_length,
                            "plan_steps": metric.plan_steps,
                            "has_tool_calls": metric.has_tool_calls,
                            "suspicious_content_detected": metric.suspicious_content_detected,
                            "parse_success": metric.parse_success,
                        }
                    )
                    + "\n"
                )
        except Exception as exc:
            logger.warning("Failed to write quality metric: %s", exc)

        # Prune old metrics
        if len(self._metrics) > self._window_size * 2:
            self._metrics = self._metrics[-self._window_size :]

    def get_validation_rate(self, agent_id: str | None = None) -> float:
        """Get the validation pass rate over the rolling window."""
        recent = self._get_recent(agent_id)
        if not recent:
            return 1.0
        passed = sum(1 for m in recent if m.validation_passed)
        return passed / len(recent)

    def get_suspicious_rate(self, agent_id: str | None = None) -> float:
        """Get the rate of suspicious content detection."""
        recent = self._get_recent(agent_id)
        if not recent:
            return 0.0
        suspicious = sum(1 for m in recent if m.suspicious_content_detected)
        return suspicious / len(recent)

    def get_parse_success_rate(self, agent_id: str | None = None) -> float:
        """Get the JSON parse success rate."""
        recent = self._get_recent(agent_id)
        if not recent:
            return 1.0
        success = sum(1 for m in recent if m.parse_success)
        return success / len(recent)

    def get_avg_response_length(self, agent_id: str | None = None) -> float:
        """Get average response length."""
        recent = self._get_recent(agent_id)
        if not recent:
            return 0.0
        return sum(m.response_length for m in recent) / len(recent)

    def get_summary(self, agent_id: str | None = None) -> dict[str, Any]:
        """Get a summary of response quality metrics."""
        recent = self._get_recent(agent_id)
        if not recent:
            return {"total": 0}

        return {
            "total": len(recent),
            "validation_rate": round(self.get_validation_rate(agent_id), 4),
            "suspicious_rate": round(self.get_suspicious_rate(agent_id), 4),
            "parse_success_rate": round(self.get_parse_success_rate(agent_id), 4),
            "avg_response_length": round(self.get_avg_response_length(agent_id), 1),
            "models_used": list({m.model for m in recent if m.model}),
        }

    def _get_recent(self, agent_id: str | None = None) -> list[ResponseQualityMetric]:
        """Get recent metrics, optionally filtered by agent."""
        metrics = self._metrics[-self._window_size :]
        if agent_id:
            metrics = [m for m in metrics if m.agent_id == agent_id]
        return metrics

    def check_alerts(self, agent_id: str | None = None) -> list[dict[str, Any]]:
        """Check for quality issues that should trigger alerts."""
        alerts: list[dict[str, Any]] = []

        validation_rate = self.get_validation_rate(agent_id)
        if validation_rate < 0.9:
            alerts.append(
                {
                    "type": "validation_degradation",
                    "severity": "warning" if validation_rate > 0.7 else "critical",
                    "message": f"Validation rate dropped to {validation_rate:.1%}",
                    "agent_id": agent_id,
                }
            )

        suspicious_rate = self.get_suspicious_rate(agent_id)
        if suspicious_rate > 0.05:
            alerts.append(
                {
                    "type": "suspicious_content_spike",
                    "severity": "critical",
                    "message": f"Suspicious content rate: {suspicious_rate:.1%}",
                    "agent_id": agent_id,
                }
            )

        parse_rate = self.get_parse_success_rate(agent_id)
        if parse_rate < 0.95:
            alerts.append(
                {
                    "type": "parse_failure_spike",
                    "severity": "warning",
                    "message": f"Parse success rate dropped to {parse_rate:.1%}",
                    "agent_id": agent_id,
                }
            )

        return alerts


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_tracker: ResponseQualityTracker | None = None


def get_response_quality_tracker() -> ResponseQualityTracker:
    """Return the module-level singleton."""
    global _default_tracker  # noqa: PLW0603
    if _default_tracker is None:
        _default_tracker = ResponseQualityTracker()
    return _default_tracker


def reset_response_quality_tracker() -> None:
    """Reset the module-level singleton (for testing)."""
    global _default_tracker  # noqa: PLW0603
    _default_tracker = None
