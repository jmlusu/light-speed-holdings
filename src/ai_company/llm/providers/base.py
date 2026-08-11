"""Abstract base class for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass, field
from enum import Enum


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
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{provider}] {message}")

    @property
    def category(self) -> ProviderErrorCategory:
        """Best-effort error classification for retry/breaker decisions."""
        return classify_provider_error(self.message, self.status_code)


class ProviderErrorCategory(str, Enum):
    """Coarse failure taxonomy shared by circuit breakers and retry logic."""

    RATE_LIMIT = "rate_limit"  # 429 — back off and retry later
    AUTH = "auth"  # 401/403 — config problem; retries won't self-heal
    SERVER = "server"  # 5xx — provider-side, worth retrying
    TIMEOUT = "timeout"  # request timed out (408 / transport)
    CONNECTION = "connection"  # transport-level connectivity failure
    CLIENT = "client"  # 4xx client error (other than 401/403/408/429)
    UNKNOWN = "unknown"  # no status code or recognisable signal


def classify_provider_error(message: str, status_code: int | None) -> ProviderErrorCategory:
    """Classify a provider failure for circuit-breaker/retry logic.

    Status codes take precedence when present (HTTP-backed providers raise
    with the underlying status). Timeout/connection detection falls back to
    message keywords for transport-level failures that carry no status code.
    """
    if status_code is not None:
        if status_code == 429:
            return ProviderErrorCategory.RATE_LIMIT
        if status_code in (401, 403):
            return ProviderErrorCategory.AUTH
        if status_code == 408:
            return ProviderErrorCategory.TIMEOUT
        if status_code >= 500:
            return ProviderErrorCategory.SERVER
        return ProviderErrorCategory.CLIENT

    lowered = message.lower()
    if "timed out" in lowered or "timeout" in lowered:
        return ProviderErrorCategory.TIMEOUT
    if "connect" in lowered or "connection" in lowered:
        return ProviderErrorCategory.CONNECTION
    return ProviderErrorCategory.UNKNOWN


class LLMResponseError(Exception):
    """Raised when the LLM response cannot be parsed after all retries."""

    def __init__(self, message: str, attempts: int = 0, last_raw: str = ""):
        self.attempts = attempts
        self.last_raw = last_raw
        super().__init__(message)
