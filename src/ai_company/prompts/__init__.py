"""Prompt engineering subsystem — versioning and templates.

This package centralises all prompt management for the AI Company Builder:

- ``registry`` — version-controlled prompt storage with A/B test support
- ``templates`` — reusable prompt components (role, format, error, escalation)
"""

from ai_company.prompts.registry import PromptRegistry, PromptVersion

__all__ = ["PromptRegistry", "PromptVersion"]
