"""Abstract base class for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChatMessage:
    """A single message in a conversation."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass(frozen=True)
class ChatResponse:
    """Structured response from an LLM provider."""

    content: str
    model: str
    provider: str
    usage: dict[str, int] = field(default_factory=dict)  # prompt_tokens, completion_tokens


class LLMProvider(ABC):
    """Abstract interface that all LLM providers must implement."""

    name: str

    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        """Send a chat request and return the response.

        Args:
            system_prompt: System-level instructions for the model.
            user_prompt: The user's message / task instruction.
            model: Optional model override. If None, uses provider default.

        Returns:
            ChatResponse with the model's text output.

        Raises:
            LLMProviderError: On API errors, timeouts, or rate limits.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is reachable and configured.

        Returns True if the provider can accept requests (API key set, endpoint reachable).
        """


class LLMProviderError(Exception):
    """Raised when an LLM provider call fails."""

    def __init__(self, provider: str, message: str, status_code: int | None = None):
        self.provider = provider
        self.status_code = status_code
        super().__init__(f"[{provider}] {message}")


class LLMResponseError(Exception):
    """Raised when the LLM response cannot be parsed after all retries."""

    def __init__(self, message: str, attempts: int = 0, last_raw: str = ""):
        self.attempts = attempts
        self.last_raw = last_raw
        super().__init__(message)
