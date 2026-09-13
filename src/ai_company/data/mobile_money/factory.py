"""Factory for creating mobile money providers."""

from __future__ import annotations

from typing import Any, Literal

from .airtel import AirtelProvider
from .base import AbstractProvider
from .mock import MockProvider
from .paychangu import PayChanguProvider
from .tnm import TNMProvider


class ProviderRegistry:
    """Registry of available mobile money providers."""

    PROVIDERS = {
        "paychangu": PayChanguProvider,
        "airtel": AirtelProvider,
        "tnm": TNMProvider,
        "mock": MockProvider,
    }

    @classmethod
    def get_provider_class(cls, name: str) -> type[AbstractProvider]:
        """Get provider class by name."""
        if name not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {name}. Available: {list(cls.PROVIDERS.keys())}")
        return cls.PROVIDERS[name]

    @classmethod
    def list_providers(cls) -> list[str]:
        """List all available provider names."""
        return list(cls.PROVIDERS.keys())


def get_provider(
    name: Literal["paychangu", "airtel", "tnm", "mock"],
    webhook_secret: str,
    **kwargs: Any,
) -> AbstractProvider:
    """Create a provider instance by name.

    Args:
        name: Provider name (paychangu, airtel, tnm, mock)
        webhook_secret: Secret for HMAC signature verification
        **kwargs: Additional provider-specific configuration

    Returns:
        Provider instance

    Raises:
        ValueError: If provider name is unknown
    """
    provider_class = ProviderRegistry.get_provider_class(name)
    return provider_class(webhook_secret, **kwargs)


def list_providers() -> list[str]:
    """List all available provider names."""
    return ProviderRegistry.list_providers()
