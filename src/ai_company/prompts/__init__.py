"""Prompt engineering subsystem — versioning, evaluation, templates, and analytics.

This package centralises all prompt management for the AI Company Builder:

- ``registry`` — version-controlled prompt storage with A/B test support
- ``templates`` — reusable prompt components (role, format, error, escalation)
- ``evals`` — automated evaluation framework with scoring and reporting
- ``analytics`` — performance tracking and improvement suggestions
"""

from ai_company.prompts.registry import PromptRegistry, PromptVersion

__all__ = ["PromptRegistry", "PromptVersion"]
