"""Tests for Ollama Optional Vector Search (architecture §4–§5)."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai_company.lsmem.vector import OllamaVectorStore


class TestOllamaVectorStore:
    """Test OllamaVectorStore optional vector search."""

    def test_init_defaults(self):
        """Test default initialization."""
        store = OllamaVectorStore()
        assert store.endpoint == "http://127.0.0.1:11434"
        assert store.model == "nomic-embed-text"
        assert store.timeout == 30.0
        assert store.enabled is True

    def test_init_custom(self):
        """Test custom initialization."""
        store = OllamaVectorStore(
            endpoint="http://localhost:11435",
            model="custom-model",
            timeout=10.0,
            enabled=False,
        )
        assert store.endpoint == "http://localhost:11435"
        assert store.model == "custom-model"
        assert store.timeout == 10.0
        assert store.enabled is False

    def test_disabled_returns_empty(self):
        """Test disabled store returns empty embeddings."""
        store = OllamaVectorStore(enabled=False)
        import asyncio

        result = asyncio.run(store.embed(["test", "text"]))
        assert result == [[], []]

    @pytest.mark.asyncio
    async def test_embed_without_client(self):
        """Test embed without initialized client returns empty."""
        store = OllamaVectorStore()
        result = await store.embed(["test"])
        assert result == [[]]

    @pytest.mark.asyncio
    async def test_embed_single(self):
        """Test embed_single without client."""
        store = OllamaVectorStore()
        result = await store.embed_single("test")
        assert result == []

    @pytest.mark.asyncio
    async def test_embed_success(self):
        """Test successful embedding with mocked client."""
        store = OllamaVectorStore()
        store._client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"embeddings": [[0.1, 0.2], [0.3, 0.4]]}
        mock_response.raise_for_status = MagicMock()
        store._client.post = AsyncMock(return_value=mock_response)

        result = await store.embed(["text1", "text2"])
        assert result == [[0.1, 0.2], [0.3, 0.4]]

    @pytest.mark.asyncio
    async def test_embed_timeout(self):
        """Test timeout handling."""
        import httpx

        store = OllamaVectorStore()
        store._client = MagicMock()
        store._client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))

        result = await store.embed(["test"])
        assert result == [[]]

    @pytest.mark.asyncio
    async def test_embed_http_error(self):
        """Test HTTP error handling."""
        import httpx

        store = OllamaVectorStore()
        store._client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error", request=MagicMock(), response=MagicMock(status_code=500)
        )
        store._client.post = AsyncMock(
            return_value=MagicMock(
                raise_for_status=MagicMock(
                    side_effect=httpx.HTTPStatusError(
                        "Server Error", request=MagicMock(), response=MagicMock(status_code=500)
                    )
                ),
                json=MagicMock(return_value={}),
            )
        )

        result = await store.embed(["test"])
        assert result == [[]]

    @pytest.mark.asyncio
    async def test_embed_single_success(self):
        """Test embed_single with mocked client."""
        store = OllamaVectorStore()
        store._client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"embeddings": [[0.1, 0.2, 0.3]]}
        mock_response.raise_for_status = MagicMock()
        store._client.post = AsyncMock(return_value=mock_response)

        result = await store.embed_single("test")
        assert result == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with OllamaVectorStore() as store:
            assert store._client is not None
        # Client should be closed after exit

    def test_from_config(self):
        """Test factory from config dict."""
        config = {
            "endpoint": "http://custom:11434",
            "model": "custom-model",
            "timeout_seconds": 15.0,
            "enabled": True,
        }
        store = OllamaVectorStore.from_config(config)
        assert store.endpoint == "http://custom:11434"
        assert store.model == "custom-model"
        assert store.timeout == 15.0
        assert store.enabled is True

    def test_is_healthy_check(self):
        """Test health check method."""
        store = OllamaVectorStore(enabled=False)
        assert store.is_healthy() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
