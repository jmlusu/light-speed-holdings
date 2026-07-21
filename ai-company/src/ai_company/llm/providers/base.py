"""Abstract base class for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChatMessage:
    """A single message in a conversation."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass(frozen=True)
class ChatResponse:
    """Structured response from an LLM provider.

    Attributes:
        content: The model's text output.
        model: Model identifier used for this call.
        provider: Provider name (e.g. "ollama", "openai").
        prompt_tokens: Number of tokens in the prompt.
        completion_tokens: Number of tokens in the completion.
        total_tokens: Total tokens (prompt + completion).
        usage: Legacy dict for backward compatibility.
    """

    content: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    usage: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Derive total_tokens and populate usage dict for backward compatibility."""
        if self.total_tokens == 0 and (self.prompt_tokens or self.completion_tokens):
            object.__setattr__(self, "total_tokens", self.prompt_tokens + self.completion_tokens)
        if not self.usage:
            object.__setattr__(
                self,
                "usage",
                {
                    "prompt_tokens": self.prompt_tokens,
                    "completion_tokens": self.completion_tokens,
                },
            )


@dataclass(frozen=True)
class StreamChunk:
    """A single chunk from a streaming response."""

    delta: str  # The text delta for this chunk
    finish_reason: str | None = None
    usage: dict[str, int] | None = None  # Only on final chunk


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

    def chat_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> Generator[StreamChunk, None, None]:
        """Stream a chat response chunk by chunk.

        Default implementation falls back to non-streaming chat.
        Override in subclasses for true streaming.
        """
        response = self.chat(system_prompt, user_prompt, model)
        yield StreamChunk(
            delta=response.content,
            finish_reason="stop",
            usage=response.usage if response.usage else None,
        )

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
