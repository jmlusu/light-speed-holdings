"""Cost tracking and budget enforcement for LLM usage.

Logs every LLM call to a JSONL file and enforces configurable daily
and per-task budget caps.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Any


# Approximate costs per 1M tokens (USD) — input and output.
# Source: public pricing pages as of 2025.  Update as prices change.
MODEL_COSTS: dict[str, dict[str, float]] = {
    # OpenAI models
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "o1": {"input": 15.00, "output": 60.00},
    "o1-mini": {"input": 3.00, "output": 12.00},
    "o1-preview": {"input": 15.00, "output": 60.00},
    "o3-mini": {"input": 1.10, "output": 4.40},
    # Anthropic models
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    # DeepSeek models
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-coder": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
    # Ollama / local models — effectively free
    "llama3.1:8b": {"input": 0.0, "output": 0.0},
    "llama3.1:70b": {"input": 0.0, "output": 0.0},
    "codellama:13b": {"input": 0.0, "output": 0.0},
    "qwen2.5-coder:14b": {"input": 0.0, "output": 0.0},
    # Catch-all for unknown models
    "_default": {"input": 1.00, "output": 3.00},
}


def _cost_per_token(model: str, token_type: str) -> float:
    """Return the cost per single token for a model.

    Args:
        model: The model identifier string.
        token_type: Either "input" or "output".

    Returns:
        Cost in USD per single token.
    """
    costs = MODEL_COSTS.get(model, MODEL_COSTS["_default"])
    return costs.get(token_type, 1.00) / 1_000_000


@dataclass
class UsageRecord:
    """A single LLM usage event."""

    timestamp: str
    model: str
    provider: str
    agent_name: str
    task_id: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    iteration: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CostTracker:
    """Tracks LLM token usage and enforces budget constraints.

    Logs every call to ``results/cost_log.jsonl`` and can enforce
    daily and per-task budget limits.

    Args:
        results_dir: Directory where cost_log.jsonl is written.
        daily_budget_usd: Maximum daily spend in USD. ``None`` = unlimited.
        task_budget_usd: Maximum per-task spend in USD. ``None`` = unlimited.
    """

    def __init__(
        self,
        results_dir: str | Path = "results",
        daily_budget_usd: float | None = None,
        task_budget_usd: float | None = None,
    ) -> None:
        self.results_dir = Path(results_dir)
        self.daily_budget = daily_budget_usd
        self.task_budget = task_budget_usd

        # In-memory accumulators
        self._daily_cost: dict[str, float] = {}  # "YYYY-MM-DD" -> total
        self._task_costs: dict[str, float] = {}  # task_id -> total
        self._records: list[UsageRecord] = []

        # Rebuild accumulators from existing log
        self._rebuild_from_log()

    # ── Public API ─────────────────────────────────────────────────

    def record_usage(
        self,
        model: str,
        provider: str,
        agent_name: str,
        task_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        iteration: int = 1,
        metadata: dict[str, Any] | None = None,
    ) -> UsageRecord:
        """Record a single LLM usage event and persist to JSONL.

        Returns the created ``UsageRecord``.
        """
        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)

        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            model=model,
            provider=provider,
            agent_name=agent_name,
            task_id=task_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
            iteration=iteration,
            metadata=metadata or {},
        )

        # Update accumulators
        day_key = date.today().isoformat()
        self._daily_cost[day_key] = self._daily_cost.get(day_key, 0.0) + cost
        self._task_costs[task_id] = self._task_costs.get(task_id, 0.0) + cost
        self._records.append(record)

        # Persist to disk
        self._append_log(record)

        return record

    def check_budget(
        self,
        task_id: str,
        proposed_cost: float = 0.0,
    ) -> tuple[bool, str]:
        """Check if a new LLM call would exceed budget limits.

        Args:
            task_id: The task being budget-checked.
            proposed_cost: Estimated cost of the proposed call.

        Returns:
            ``(allowed, reason)`` tuple. ``allowed`` is True if the call
            can proceed.
        """
        day_key = date.today().isoformat()

        # Check daily budget
        if self.daily_budget is not None:
            current_daily = self._daily_cost.get(day_key, 0.0)
            if current_daily + proposed_cost > self.daily_budget:
                return (
                    False,
                    f"Daily budget exceeded: ${current_daily:.4f} + "
                    f"${proposed_cost:.4f} > ${self.daily_budget:.2f}",
                )

        # Check task budget
        if self.task_budget is not None:
            current_task = self._task_costs.get(task_id, 0.0)
            if current_task + proposed_cost > self.task_budget:
                return (
                    False,
                    f"Task budget exceeded: ${current_task:.4f} + "
                    f"${proposed_cost:.4f} > ${self.task_budget:.2f}",
                )

        return True, "within budget"

    def get_daily_summary(self, day: str | None = None) -> dict[str, Any]:
        """Get usage summary for a given day (or today if not specified).

        Args:
            day: ISO date string (``"YYYY-MM-DD"``). Defaults to today.

        Returns:
            Dict with total_cost_usd, total_prompt_tokens,
            total_completion_tokens, call_count, and per-model breakdown.
        """
        target_day = day or date.today().isoformat()

        total_cost = 0.0
        total_prompt = 0
        total_completion = 0
        call_count = 0
        by_model: dict[str, dict[str, Any]] = {}

        for rec in self._records:
            if rec.timestamp[:10] != target_day:
                continue

            total_cost += rec.cost_usd
            total_prompt += rec.prompt_tokens
            total_completion += rec.completion_tokens
            call_count += 1

            model_entry = by_model.setdefault(
                rec.model,
                {"cost_usd": 0.0, "prompt_tokens": 0, "completion_tokens": 0, "calls": 0},
            )
            model_entry["cost_usd"] += rec.cost_usd
            model_entry["prompt_tokens"] += rec.prompt_tokens
            model_entry["completion_tokens"] += rec.completion_tokens
            model_entry["calls"] += 1

        return {
            "date": target_day,
            "total_cost_usd": round(total_cost, 6),
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "call_count": call_count,
            "by_model": by_model,
        }

    def get_task_summary(self, task_id: str) -> dict[str, Any]:
        """Get usage summary for a specific task."""
        total_cost = 0.0
        total_prompt = 0
        total_completion = 0
        call_count = 0
        iterations = 0

        for rec in self._records:
            if rec.task_id != task_id:
                continue
            total_cost += rec.cost_usd
            total_prompt += rec.prompt_tokens
            total_completion += rec.completion_tokens
            call_count += 1
            iterations = max(iterations, rec.iteration)

        return {
            "task_id": task_id,
            "total_cost_usd": round(total_cost, 6),
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "call_count": call_count,
            "max_iteration": iterations,
        }

    def estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate the cost of a hypothetical LLM call without recording it."""
        return self._calculate_cost(model, prompt_tokens, completion_tokens)

    # ── Internal helpers ───────────────────────────────────────────

    def _calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """Calculate the cost in USD for a given token count."""
        input_cost = prompt_tokens * _cost_per_token(model, "input")
        output_cost = completion_tokens * _cost_per_token(model, "output")
        return round(input_cost + output_cost, 8)

    def _append_log(self, record: UsageRecord) -> None:
        """Append a usage record to the JSONL log file."""
        log_path = self.results_dir / "cost_log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict(), default=str) + "\n")
        except OSError:
            # Non-fatal: log append failure shouldn't crash the agent
            pass

    def _rebuild_from_log(self) -> None:
        """Load existing cost_log.jsonl to rebuild in-memory accumulators."""
        log_path = self.results_dir / "cost_log.jsonl"
        if not log_path.exists():
            return

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec_dict = json.loads(line)
                        day = rec_dict.get("timestamp", "")[:10]
                        cost = rec_dict.get("cost_usd", 0.0)
                        task_id = rec_dict.get("task_id", "")

                        self._daily_cost[day] = self._daily_cost.get(day, 0.0) + cost
                        self._task_costs[task_id] = self._task_costs.get(task_id, 0.0) + cost

                        record = UsageRecord(**rec_dict)
                        self._records.append(record)
                    except (json.JSONDecodeError, KeyError):
                        continue
        except OSError:
            pass
