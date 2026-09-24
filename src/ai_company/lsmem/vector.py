"""Optional Vector Search with Ollama Embeddings.

Implements architecture §4–§5: Optional vector search layer using Ollama embeddings.
Only activated after deterministic FTS5 works; never cloud fallback.
"""

import logging
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

import httpx

logger = logging.getLogger(__name__)


class OllamaVectorStore:
    """
    Optional semantic search layer using Ollama embeddings.

    Architecture §4–§5:
    - Only used after deterministic FTS5 works (locked decision 5)
    - Local-only, loopback-only (127.0.0.1:11434)
    - Model: nomic-embed-text (274 MB, installed locally)
    - If Ollama unavailable: degrade to FTS5-only, NEVER cloud fallback
    """

    def __init__(
        self,
        endpoint: str = "http://127.0.0.1:11434",
        model: str = "nomic-embed-text",
        timeout: float = 30.0,
        enabled: bool = True,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.enabled = enabled
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "OllamaVectorStore":
        if not self.enabled:
            return self
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._client:
            await self._client.aclose()

    def _check_available(self) -> bool:
        """Check if Ollama is available (sync version for health checks)."""
        if not self.enabled:
            return False
        try:
            import urllib.error
            import urllib.request

            with urllib.request.urlopen(f"{self.endpoint}/api/tags", timeout=2) as resp:
                return bool(resp.status == 200)
        except (OSError, ValueError, urllib.error.URLError):
            return False

    async def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Returns empty list if Ollama is unavailable or disabled.
        """
        if not self.enabled or not self._client:
            logger.debug("Ollama disabled or not initialized, returning empty embeddings")
            return [[] for _ in texts]

        try:
            response = await self._client.post(
                f"{self.endpoint}/api/embeddings",
                json={"model": self.model, "prompt": texts},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            embeddings: List[List[float]] = data.get("embeddings", [[] for _ in texts])
            return embeddings
        except httpx.TimeoutException:
            logger.warning("Ollama embedding request timed out")
            return [[] for _ in texts]
        except httpx.HTTPStatusError as e:
            logger.warning(f"Ollama embedding HTTP error: {e.response.status_code}")
            return [[] for _ in texts]
        except (OSError, ValueError, httpx.HTTPError) as e:
            logger.warning(f"Ollama embedding error: {e}")
            return [[] for _ in texts]

    async def embed_single(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        embeddings = await self.embed([text])
        return embeddings[0] if embeddings else []

    def is_healthy(self) -> bool:
        """Check if Ollama service is healthy."""
        return self._check_available()

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "OllamaVectorStore":
        """Create from config dict."""
        return cls(
            endpoint=config.get("endpoint", "http://127.0.0.1:11434"),
            model=config.get("model", "nomic-embed-text"),
            timeout=config.get("timeout_seconds", 30.0),
            enabled=config.get("enabled", False),
        )
