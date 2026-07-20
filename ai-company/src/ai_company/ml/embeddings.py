"""Embedding engine — local sentence-transformer based text embeddings.

Provides a lightweight interface for computing and comparing text
embeddings without external API dependencies.  Falls back gracefully
when sentence-transformers is unavailable.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, cast

import numpy as np

logger = logging.getLogger(__name__)

# Lazy import sentinel
_model = None
_model_name: str = ""


def _get_model(model_name: str = "all-MiniLM-L6-v2") -> Any:
    """Lazily load the sentence-transformer model.

    Args:
        model_name: HuggingFace model identifier.

    Returns:
        The SentenceTransformer model instance.

    Raises:
        ImportError: If sentence-transformers is not installed.
    """
    global _model, _model_name

    if _model is not None and _model_name == model_name:
        return _model

    try:
        from sentence_transformers import SentenceTransformer  # type: ignore[import-not-found]

        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
        _model_name = model_name
        logger.info("Embedding model loaded successfully (dim=%d)", _model.get_sentence_embedding_dimension())
        return _model
    except ImportError:
        raise ImportError(
            "sentence-transformers is required for embedding features. "
            "Install with: pip install sentence-transformers"
        )


class EmbeddingEngine:
    """Compute and compare text embeddings using sentence-transformers.

    Provides methods for encoding text, computing cosine similarity,
    and managing a persistent embedding cache.

    Args:
        model_name: HuggingFace model identifier.
        cache_dir: Directory for persistent embedding cache.
        dimension: Expected embedding dimension (auto-detected from model).
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        cache_dir: str | Path = "memory/embeddings",
        dimension: int | None = None,
    ) -> None:
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._dimension = dimension
        self._cache: dict[str, np.ndarray] = {}
        self._load_cache()

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        if self._dimension is None:
            model = _get_model(self.model_name)
            self._dimension = model.get_sentence_embedding_dimension()
        return self._dimension

    def encode(self, texts: str | list[str], normalize: bool = True) -> np.ndarray:
        """Encode one or more text strings into embedding vectors.

        Args:
            texts: Single string or list of strings to encode.
            normalize: Whether to L2-normalize the vectors.

        Returns:
            numpy array of shape (n, dimension) or (dimension,) for single input.
        """
        model = _get_model(self.model_name)

        single = isinstance(texts, str)
        if single:
            text_list = [cast(str, texts)]
        else:
            text_list = list(texts)

        # Check cache for each text
        uncached: list[tuple[int, str]] = []
        results: list[np.ndarray | None] = [None] * len(text_list)

        for i, text in enumerate(text_list):
            cache_key = self._cache_key(text)
            if cache_key in self._cache:
                results[i] = self._cache[cache_key]
            else:
                uncached.append((i, text))

        # Encode uncached texts
        if uncached:
            uncached_texts = [t for _, t in uncached]
            new_embeddings = model.encode(
                uncached_texts,
                normalize_embeddings=normalize,
                show_progress_bar=False,
            )
            for (i, text), embedding in zip(uncached, new_embeddings):
                arr = np.array(embedding, dtype=np.float32)
                self._cache[self._cache_key(text)] = arr
                results[i] = arr

        final_results = [r for r in results if r is not None]
        if not final_results:
            return np.array([], dtype=np.float32)
        stacked = np.stack(final_results)
        return stacked[0] if single else stacked

    def similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity between two text strings.

        Args:
            text_a: First text.
            text_b: Second text.

        Returns:
            Cosine similarity score in [-1, 1].
        """
        emb_a = self.encode(text_a)
        emb_b = self.encode(text_b)
        return float(np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b) + 1e-8))

    def rank_by_relevance(
        self,
        query: str,
        candidates: list[str],
        top_k: int = 5,
    ) -> list[tuple[int, float, str]]:
        """Rank candidate texts by relevance to a query.

        Args:
            query: The query text.
            candidates: List of candidate texts.
            top_k: Number of top results to return.

        Returns:
            List of (index, score, text) tuples sorted by descending score.
        """
        if not candidates:
            return []

        query_emb = self.encode(query)
        candidate_embs = self.encode(candidates)

        # Compute cosine similarities
        norms = np.linalg.norm(candidate_embs, axis=1, keepdims=True) + 1e-8
        normalized = candidate_embs / norms
        scores = normalized @ query_emb

        # Get top-k indices
        k = min(top_k, len(candidates))
        top_indices = np.argsort(scores)[::-1][:k]

        return [(int(idx), float(scores[idx]), candidates[idx]) for idx in top_indices]

    def save_cache(self) -> None:
        """Persist the embedding cache to disk."""
        cache_file = self.cache_dir / "embeddings_cache.json"
        data = {
            key: vec.tolist()
            for key, vec in self._cache.items()
        }
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _load_cache(self) -> None:
        """Load embedding cache from disk."""
        cache_file = self.cache_dir / "embeddings_cache.json"
        if not cache_file.exists():
            return
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._cache = {k: np.array(v, dtype=np.float32) for k, v in data.items()}
            logger.info("Loaded %d cached embeddings", len(self._cache))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load embedding cache: %s", exc)

    @staticmethod
    def _cache_key(text: str) -> str:
        """Generate a deterministic cache key from text content."""
        import hashlib
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:32]
