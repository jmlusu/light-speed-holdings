"""LLM abstraction layer for the AI Company Builder."""

from ai_company.llm.client import LLMClient
from ai_company.llm.providers.base import LLMProvider

__all__ = ["LLMClient", "LLMProvider"]
