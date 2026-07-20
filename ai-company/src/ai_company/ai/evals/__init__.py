"""Prompt evaluation pipeline — regression testing, LLM-as-judge, and A/B support.

Provides a framework for systematically evaluating prompt quality:
- Regression testing: detect quality drops when prompts change
- LLM-as-judge: use a powerful model to score prompt outputs
- A/B testing: compare prompt variants side-by-side
"""

from ai_company.ai.evals.evaluator import (
    EvalCase,
    EvalResult,
    EvalRunner,
    PromptVariant,
)

__all__ = ["EvalCase", "EvalResult", "EvalRunner", "PromptVariant"]
