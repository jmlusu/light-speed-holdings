"""Prompt evaluation framework — test cases, scoring, and reporting.

This package provides automated evaluation of agent prompts:

- ``eval_dataset`` — test cases for each agent type
- ``eval_scorer`` — scoring logic (correctness, format, quality)
- ``eval_runner`` — executes prompts against test scenarios
- ``eval_report`` — generates evaluation reports
"""

from ai_company.prompts.evals.eval_runner import EvalRunner
from ai_company.prompts.evals.eval_scorer import EvalScorer

__all__ = ["EvalRunner", "EvalScorer"]
