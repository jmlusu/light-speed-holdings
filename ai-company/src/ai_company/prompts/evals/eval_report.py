"""Evaluation report generator.

Produces human-readable and machine-readable reports from evaluation results.

Output formats:
- Markdown (for docs/reports/)
- JSON (for analytics pipeline)
- Console summary (for CI)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.prompts.evals.eval_runner import EvalRunResult


class EvalReport:
    """Generate evaluation reports in multiple formats.

    Usage::

        report = EvalReport(run_result)
        report.to_markdown("reports/prompt-eval.md")
        report.to_json("reports/prompt-eval.json")
        print(report.to_console())
    """

    def __init__(self, run_result: EvalRunResult) -> None:
        self.result = run_result
        self.timestamp = datetime.now().isoformat()

    def to_markdown(self, output_path: str | None = None) -> str:
        """Generate a Markdown evaluation report."""
        lines: list[str] = []
        agg = self.result.aggregates

        lines.append("# Prompt Evaluation Report")
        lines.append(f"\n**Generated:** {self.timestamp}")
        lines.append(f"**Duration:** {self.result.duration_seconds}s")
        lines.append(f"**Test Cases:** {agg.get('count', 0)}")

        # Overall scores
        lines.append("\n## Overall Scores\n")
        lines.append("| Metric | Score |")
        lines.append("|--------|-------|")
        lines.append(f"| **Total** | {agg.get('avg_total', 0):.1%} |")
        lines.append(f"| Format Compliance | {agg.get('avg_format', 0):.1%} |")
        lines.append(f"| Tool Usage | {agg.get('avg_tools', 0):.1%} |")
        lines.append(f"| Reasoning Quality | {agg.get('avg_reasoning', 0):.1%} |")
        lines.append(f"| Result Quality | {agg.get('avg_result', 0):.1%} |")
        lines.append(
            f"| Constraint Adherence | {agg.get('avg_constraints', 0):.1%} |"
        )
        lines.append(f"| Score Range | {agg.get('min_total', 0):.1%} — {agg.get('max_total', 0):.1%} |")

        # Per-test breakdown
        lines.append("\n## Per-Test Results\n")
        lines.append("| Test | Name | Agent | Difficulty | Score |")
        lines.append("|------|------|-------|------------|-------|")

        for tr in self.result.test_results:
            # Find test case info from the result
            score_bar = self._score_bar(tr.score.total)
            lines.append(
                f"| {tr.test_case_id} | {tr.test_case_id} | — | — | "
                f"{score_bar} {tr.score.total:.1%} |"
            )

        # Errors and warnings
        all_errors = []
        all_warnings = []
        for tr in self.result.test_results:
            all_errors.extend(tr.score.errors)
            all_warnings.extend(tr.score.warnings)
        all_errors.extend(self.result.errors)

        if all_errors:
            lines.append(f"\n## Errors ({len(all_errors)})\n")
            for e in all_errors[:20]:
                lines.append(f"- {e}")

        if all_warnings:
            lines.append(f"\n## Warnings ({len(all_warnings)})\n")
            for w in all_warnings[:20]:
                lines.append(f"- {w}")

        # Recommendations
        lines.append("\n## Recommendations\n")
        lines.extend(self._generate_recommendations())

        content = "\n".join(lines)

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        return content

    def to_json(self, output_path: str | None = None) -> str:
        """Generate a JSON evaluation report."""
        report_data: dict[str, Any] = {
            "timestamp": self.timestamp,
            "duration_seconds": self.result.duration_seconds,
            "aggregates": self.result.aggregates,
            "config": {
                "max_test_cases": self.result.config.max_test_cases,
                "model_override": self.result.config.model_override,
            },
            "test_results": [
                {
                    "id": tr.test_case_id,
                    "score": {
                        "total": tr.score.total,
                        "format_compliance": tr.score.format_compliance,
                        "tool_usage": tr.score.tool_usage,
                        "reasoning_quality": tr.score.reasoning_quality,
                        "result_quality": tr.score.result_quality,
                        "constraint_adherence": tr.score.constraint_adherence,
                    },
                    "errors": tr.score.errors,
                    "warnings": tr.score.warnings,
                    "tokens_used": tr.tokens_used,
                    "latency_ms": tr.latency_ms,
                }
                for tr in self.result.test_results
            ],
            "errors": self.result.errors,
        }

        content = json.dumps(report_data, indent=2)

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        return content

    def to_console(self) -> str:
        """Generate a compact console summary for CI output."""
        agg = self.result.aggregates
        lines: list[str] = []

        lines.append("=" * 60)
        lines.append("  PROMPT EVALUATION SUMMARY")
        lines.append("=" * 60)
        lines.append(f"  Tests: {agg.get('count', 0)}  |  Duration: {self.result.duration_seconds}s")
        lines.append(f"  Total Score:  {agg.get('avg_total', 0):.1%}  "
                     f"(min={agg.get('min_total', 0):.1%} max={agg.get('max_total', 0):.1%})")
        lines.append("-" * 60)
        lines.append(f"  Format:       {agg.get('avg_format', 0):.1%}")
        lines.append(f"  Tools:        {agg.get('avg_tools', 0):.1%}")
        lines.append(f"  Reasoning:    {agg.get('avg_reasoning', 0):.1%}")
        lines.append(f"  Result:       {agg.get('avg_result', 0):.1%}")
        lines.append(f"  Constraints:  {agg.get('avg_constraints', 0):.1%}")
        lines.append("-" * 60)
        lines.append(f"  Errors: {agg.get('total_errors', 0)}  |  "
                     f"Warnings: {agg.get('total_warnings', 0)}")
        lines.append("=" * 60)

        # Failed tests
        failed = [tr for tr in self.result.test_results if tr.score.total < 0.5]
        if failed:
            lines.append(f"\n  FAILED TESTS ({len(failed)}):")
            for tr in failed:
                lines.append(f"    {tr.test_case_id}: {tr.score.total:.1%}")
                for e in tr.score.errors:
                    lines.append(f"      ERROR: {e}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _score_bar(score: float, width: int = 10) -> str:
        """Render a visual score bar."""
        filled = round(score * width)
        return "█" * filled + "░" * (width - filled)

    def _generate_recommendations(self) -> list[str]:
        """Generate actionable recommendations based on scores."""
        agg = self.result.aggregates
        recs: list[str] = []

        avg_total = agg.get("avg_total", 0)
        avg_format = agg.get("avg_format", 0)
        avg_tools = agg.get("avg_tools", 0)
        avg_reasoning = agg.get("avg_reasoning", 0)

        if avg_total >= 0.8:
            recs.append("- **Good overall quality.** Continue monitoring and fine-tune.")
        elif avg_total >= 0.6:
            recs.append("- **Moderate quality.** Focus on the weakest dimension below.")
        else:
            recs.append("- **Low quality.** Major prompt revision recommended.")

        if avg_format < 0.7:
            recs.append(
                "- **Improve format compliance:** Add clearer JSON structure "
                "instructions and examples to the system prompt."
            )

        if avg_tools < 0.7:
            recs.append(
                "- **Improve tool usage:** Add tool-specific instructions with "
                "examples of correct tool selection for common scenarios."
            )

        if avg_reasoning < 0.6:
            recs.append(
                "- **Improve reasoning quality:** Add chain-of-thought prompting "
                "and explicit instructions to explain the 'why' before the 'what'."
            )

        if agg.get("total_errors", 0) > 0:
            recs.append(
                "- **Address errors:** Review individual test failures and "
                "add error-handling instructions to the prompt."
            )

        if not recs:
            recs.append("- All metrics are within acceptable ranges.")

        return recs
