"""Prompt analytics — track performance over time and suggest improvements.

Stores evaluation history as JSONL and provides:
- Trend analysis (is prompt quality improving?)
- Failure pattern detection
- Automatic improvement suggestions
- Prompt performance comparison (A/B test results)
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PromptMetric:
    """A single metric data point for a prompt version."""

    prompt_id: str
    version: int
    timestamp: float = field(default_factory=time.time)
    avg_score: float = 0.0
    format_score: float = 0.0
    tool_score: float = 0.0
    reasoning_score: float = 0.0
    result_score: float = 0.0
    error_count: int = 0
    warning_count: int = 0
    judge_scores: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PromptMetric:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PromptInsight:
    """An actionable insight derived from analytics."""

    prompt_id: str
    insight_type: str  # "degradation", "improvement", "pattern", "suggestion"
    severity: str  # "info", "warning", "critical"
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class PromptAnalytics:
    """Track prompt performance and generate insights.

    Storage: ``.opencode/prompt-analytics/metrics.jsonl``

    Usage::

        analytics = PromptAnalytics()

        # Record a metric
        analytics.record(PromptMetric(
            prompt_id="exec.system",
            version=2,
            avg_score=0.85,
            format_score=0.9,
            tool_score=0.8,
        ))

        # Get trends
        trends = analytics.get_trends("exec.system")

        # Get insights
        insights = analytics.get_insights("exec.system")
    """

    def __init__(
        self,
        storage_dir: str = ".opencode/prompt-analytics",
    ) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_path = self.storage_dir / "metrics.jsonl"
        self._cache: list[PromptMetric] | None = None

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(self, metric: PromptMetric) -> None:
        """Append a metric data point."""
        with open(self.metrics_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(metric.to_dict()) + "\n")
        self._cache = None  # invalidate cache

    def record_from_eval_result(
        self,
        prompt_id: str,
        version: int,
        eval_result: Any,  # EvalResult from eval_scorer
        judge_scores: dict[str, float] | None = None,
    ) -> None:
        """Record metrics from an EvalResult object."""
        metric = PromptMetric(
            prompt_id=prompt_id,
            version=version,
            avg_score=eval_result.score.total,
            format_score=eval_result.score.format_compliance,
            tool_score=eval_result.score.tool_usage,
            reasoning_score=eval_result.score.reasoning_quality,
            result_score=eval_result.score.result_quality,
            error_count=len(eval_result.score.errors),
            warning_count=len(eval_result.score.warnings),
            judge_scores=judge_scores or {},
        )
        self.record(metric)

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def get_metrics(
        self,
        prompt_id: str | None = None,
        version: int | None = None,
        since: float | None = None,
    ) -> list[PromptMetric]:
        """Query metrics with optional filters."""
        all_metrics = self._load_all()

        result = all_metrics
        if prompt_id is not None:
            result = [m for m in result if m.prompt_id == prompt_id]
        if version is not None:
            result = [m for m in result if m.version == version]
        if since is not None:
            result = [m for m in result if m.timestamp >= since]

        return result

    def get_trends(self, prompt_id: str) -> dict[str, Any]:
        """Analyze trends for a prompt over time."""
        metrics = self.get_metrics(prompt_id=prompt_id)
        if not metrics:
            return {"prompt_id": prompt_id, "data_points": 0}

        # Group by version
        by_version: dict[int, list[PromptMetric]] = defaultdict(list)
        for m in metrics:
            by_version[m.version].append(m)

        # Compute per-version averages
        version_avgs: dict[int, float] = {}
        for ver, ver_metrics in by_version.items():
            version_avgs[ver] = sum(m.avg_score for m in ver_metrics) / len(ver_metrics)

        # Trend: compare latest version to previous
        sorted_versions = sorted(version_avgs.keys())
        trend_direction = "stable"
        trend_delta = 0.0

        if len(sorted_versions) >= 2:
            prev_ver = sorted_versions[-2]
            curr_ver = sorted_versions[-1]
            trend_delta = version_avgs[curr_ver] - version_avgs[prev_ver]
            if trend_delta > 0.05:
                trend_direction = "improving"
            elif trend_delta < -0.05:
                trend_direction = "degrading"

        # Recent performance (last 24h)
        day_ago = time.time() - 86400
        recent = [m for m in metrics if m.timestamp >= day_ago]
        recent_avg = (
            sum(m.avg_score for m in recent) / len(recent) if recent else 0.0
        )

        return {
            "prompt_id": prompt_id,
            "data_points": len(metrics),
            "versions": sorted_versions,
            "version_averages": version_avgs,
            "latest_version": sorted_versions[-1] if sorted_versions else None,
            "latest_avg": version_avgs.get(sorted_versions[-1], 0) if sorted_versions else 0,
            "trend_direction": trend_direction,
            "trend_delta": round(trend_delta, 4),
            "recent_24h_avg": round(recent_avg, 4),
            "recent_24h_count": len(recent),
        }

    def get_insights(self, prompt_id: str) -> list[PromptInsight]:
        """Generate actionable insights for a prompt."""
        trends = self.get_trends(prompt_id)
        metrics = self.get_metrics(prompt_id=prompt_id)
        insights: list[PromptInsight] = []

        # Insight 1: Performance degradation
        if trends.get("trend_direction") == "degrading":
            delta = trends.get("trend_delta", 0)
            insights.append(
                PromptInsight(
                    prompt_id=prompt_id,
                    insight_type="degradation",
                    severity="warning",
                    message=(
                        f"Prompt performance is degrading (delta: {delta:+.2%}). "
                        "Consider reviewing the latest version changes."
                    ),
                    details=trends,
                )
            )

        # Insight 2: High error rate
        if metrics:
            total_errors = sum(m.error_count for m in metrics)
            error_rate = total_errors / len(metrics)
            if error_rate > 0.2:
                insights.append(
                    PromptInsight(
                        prompt_id=prompt_id,
                        insight_type="pattern",
                        severity="warning",
                        message=(
                            f"High error rate: {error_rate:.0%} of evaluations "
                            f"had errors ({total_errors} total). "
                            "Review common error patterns."
                        ),
                        details={"error_rate": error_rate, "total_errors": total_errors},
                    )
                )

        # Insight 3: Format compliance issues
        if metrics:
            avg_format = sum(m.format_score for m in metrics) / len(metrics)
            if avg_format < 0.7:
                insights.append(
                    PromptInsight(
                        prompt_id=prompt_id,
                        insight_type="suggestion",
                        severity="info",
                        message=(
                            f"Format compliance is low ({avg_format:.0%}). "
                            "Add clearer JSON structure instructions and examples."
                        ),
                        details={"avg_format_score": avg_format},
                    )
                )

        # Insight 4: Version comparison
        by_version: dict[int, list[PromptMetric]] = defaultdict(list)
        for m in metrics:
            by_version[m.version].append(m)

        sorted_versions = sorted(by_version.keys())
        if len(sorted_versions) >= 2:
            prev = by_version[sorted_versions[-2]]
            curr = by_version[sorted_versions[-1]]
            prev_avg = sum(m.avg_score for m in prev) / len(prev)
            curr_avg = sum(m.avg_score for m in curr) / len(curr)

            if curr_avg > prev_avg:
                insights.append(
                    PromptInsight(
                        prompt_id=prompt_id,
                        insight_type="improvement",
                        severity="info",
                        message=(
                            f"Version {sorted_versions[-1]} ({curr_avg:.2f}) "
                            f"outperforms version {sorted_versions[-2]} ({prev_avg:.2f})."
                        ),
                    )
                )

        # Insight 5: Stale prompt (not updated recently)
        if metrics:
            latest_ts = max(m.timestamp for m in metrics)
            days_stale = (time.time() - latest_ts) / 86400
            if days_stale > 30:
                insights.append(
                    PromptInsight(
                        prompt_id=prompt_id,
                        insight_type="suggestion",
                        severity="info",
                        message=(
                            f"Prompt hasn't been evaluated in {days_stale:.0f} days. "
                            "Consider running fresh evaluations."
                        ),
                    )
                )

        return insights

    def get_failure_patterns(
        self, prompt_id: str | None = None, top_n: int = 10
    ) -> list[dict[str, Any]]:
        """Identify common failure patterns across evaluations."""
        metrics = self.get_metrics(prompt_id=prompt_id)
        if not metrics:
            return []

        # Collect all issues from metadata
        issue_counts: dict[str, int] = defaultdict(int)
        for m in metrics:
            for issue in m.metadata.get("issues", []):
                issue_counts[issue] += 1

        sorted_issues = sorted(issue_counts.items(), key=lambda x: -x[1])
        return [
            {"pattern": issue, "count": count}
            for issue, count in sorted_issues[:top_n]
        ]

    def compare_versions(
        self, prompt_id: str, version_a: int, version_b: int
    ) -> dict[str, Any]:
        """Compare two versions of a prompt."""
        metrics_a = self.get_metrics(prompt_id=prompt_id, version=version_a)
        metrics_b = self.get_metrics(prompt_id=prompt_id, version=version_b)

        def _avg(ms: list[PromptMetric], attr: str) -> float:
            vals = [getattr(m, attr) for m in ms]
            return sum(vals) / len(vals) if vals else 0.0

        return {
            "prompt_id": prompt_id,
            "version_a": version_a,
            "version_b": version_b,
            "version_a_avg": _avg(metrics_a, "avg_score"),
            "version_b_avg": _avg(metrics_b, "avg_score"),
            "version_a_samples": len(metrics_a),
            "version_b_samples": len(metrics_b),
            "winner": (
                version_b
                if _avg(metrics_b, "avg_score") > _avg(metrics_a, "avg_score")
                else version_a
            ),
        }

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------

    def _load_all(self) -> list[PromptMetric]:
        if self._cache is not None:
            return self._cache

        if not self.metrics_path.exists():
            return []

        metrics: list[PromptMetric] = []
        with open(self.metrics_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        metrics.append(PromptMetric.from_dict(data))
                    except (json.JSONDecodeError, TypeError):
                        continue

        self._cache = metrics
        return metrics
