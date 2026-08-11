"""Sprint 4 T012 — ``ai-company llm usage`` CLI command tests (ticket #9).

Verifies the command aggregates the executor's ``cost_log.jsonl`` with
filters for time period, model, and agent, plus JSON output.
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ai_company.cli.main import app
from ai_company.llm.cost_tracker import CostTracker

runner = CliRunner()


def _seed_log(tmp_path: Path, days_ago: int = 0) -> Path:
    """Write a cost_log.jsonl with two records and return its results dir."""
    import datetime

    results = tmp_path / "results"
    tracker = CostTracker(results_dir=results)
    stamp = (datetime.date.today() - datetime.timedelta(days=days_ago)).isoformat()
    tracker.record_usage(
        model="gpt-4o-mini",
        provider="openai",
        agent_name="agent_a",
        task_id="task-1",
        prompt_tokens=1_000,
        completion_tokens=500,
    )
    # Rewrite the timestamp to control the day (CostTracker uses now()).
    log_path = results / "cost_log.jsonl"
    lines = log_path.read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[0])
    rec["timestamp"] = f"{stamp}T12:00:00"
    rec["agent_name"] = "agent_a"
    log_path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    return results


class TestLlmUsageCommand:
    def test_reports_usage_with_default_window(self, tmp_path: Path) -> None:
        results = _seed_log(tmp_path)
        result = runner.invoke(app, ["llm", "usage", "--results-dir", str(results), "--days", "7"])
        assert result.exit_code == 0
        assert "LLM Usage" in result.output
        assert "Calls:" in result.output
        assert "gpt-4o-mini" in result.output
        assert "agent_a" in result.output

    def test_empty_log_reports_no_usage(self, tmp_path: Path) -> None:
        results = tmp_path / "results"
        results.mkdir(parents=True, exist_ok=True)
        result = runner.invoke(app, ["llm", "usage", "--results-dir", str(results), "--days", "7"])
        assert result.exit_code == 0
        assert "No LLM usage recorded" in result.output

    def test_agent_filter_limits_output(self, tmp_path: Path) -> None:
        results = _seed_log(tmp_path)
        result = runner.invoke(
            app,
            [
                "llm",
                "usage",
                "--results-dir",
                str(results),
                "--days",
                "7",
                "--agent",
                "agent_b",
            ],
        )
        assert result.exit_code == 0
        assert "No LLM usage recorded" in result.output

    def test_json_output_shape(self, tmp_path: Path) -> None:
        results = _seed_log(tmp_path)
        result = runner.invoke(
            app,
            ["llm", "usage", "--results-dir", str(results), "--days", "7", "--json"],
        )
        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["call_count"] == 1
        assert payload["total_prompt_tokens"] == 1_000
        assert payload["total_completion_tokens"] == 500
        assert "gpt-4o-mini" in payload["by_model"]
        assert "agent_a" in payload["by_agent"]

    def test_model_filter_within_window(self, tmp_path: Path) -> None:
        results = _seed_log(tmp_path)
        result = runner.invoke(
            app,
            [
                "llm",
                "usage",
                "--results-dir",
                str(results),
                "--days",
                "7",
                "--model",
                "gpt-4o-mini",
            ],
        )
        assert result.exit_code == 0
        assert "gpt-4o-mini" in result.output

    def test_days_outside_window_filters_out(self, tmp_path: Path) -> None:
        results = _seed_log(tmp_path, days_ago=30)
        result = runner.invoke(
            app,
            ["llm", "usage", "--results-dir", str(results), "--days", "7"],
        )
        assert result.exit_code == 0
        assert "No LLM usage recorded" in result.output
