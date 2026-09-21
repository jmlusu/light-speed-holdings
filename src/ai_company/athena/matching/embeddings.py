import contextlib
import hashlib
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from ai_company.paths import get_project_root


class EmbeddingCache:
    """Cache for embeddings to avoid recomputation."""

    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            project_root = get_project_root()
            cache_dir = project_root / "company" / "athena" / "embeddings_cache"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, np.ndarray] = {}

    def _get_cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:32]

    def _get_cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.npy"

    def get(self, text: str) -> Optional[np.ndarray]:
        key = self._get_cache_key(text)
        if key in self._memory_cache:
            return self._memory_cache[key]

        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                embedding: np.ndarray = np.load(cache_path)
                self._memory_cache[key] = embedding
                return embedding
            except (OSError, ValueError):
                pass
        return None

    def set(self, text: str, embedding: np.ndarray) -> None:
        key = self._get_cache_key(text)
        self._memory_cache[key] = embedding
        cache_path = self._get_cache_path(key)
        with contextlib.suppress(OSError, ValueError):
            np.save(cache_path, embedding)


# Global cache instance
embedding_cache = EmbeddingCache()


class EmbeddingModel:
    """Wrapper for sentence-transformers embedding model."""

    _instance: Optional["EmbeddingModel"] = None
    _model = None

    def __new__(cls) -> "EmbeddingModel":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._model is None:
            self._load_model()

    def _load_model(self) -> None:
        """Load the sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer

            # Use a lightweight but effective model
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            self._model = None

    def is_available(self) -> bool:
        return self._model is not None

    def encode(self, texts: List[str], use_cache: bool = True) -> np.ndarray:
        """Encode texts to embeddings."""
        if not self.is_available():
            raise RuntimeError("sentence-transformers not available")

        if isinstance(texts, str):
            texts = [texts]

        embeddings: List[Optional[np.ndarray]] = []
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            if use_cache:
                cached = embedding_cache.get(text)
                if cached is not None:
                    embeddings.append(cached)
                    continue
            uncached_texts.append(text)
            uncached_indices.append(i)
            embeddings.append(None)

        if uncached_texts:
            assert self._model is not None
            new_embeddings = self._model.encode(uncached_texts, convert_to_numpy=True)
            for idx, emb in zip(uncached_indices, new_embeddings, strict=False):
                embeddings[idx] = emb
                if use_cache:
                    embedding_cache.set(uncached_texts[uncached_indices.index(idx)], emb)

        return np.array(embeddings)

    def encode_single(self, text: str, use_cache: bool = True) -> np.ndarray:
        """Encode a single text to embedding."""
        embedding: np.ndarray = self.encode([text], use_cache)[0]
        return embedding


# Global model instance
embedding_model = EmbeddingModel()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)

    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b, axis=1, keepdims=True)

    if a_norm == 0 or b_norm == 0:
        return 0.0

    return float(np.dot(a, b.T)[0, 0] / (a_norm[0, 0] * b_norm[0, 0]))


def batch_cosine_similarity(query: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between query and multiple candidates."""
    if query.ndim == 1:
        query = query.reshape(1, -1)

    query_norm = np.linalg.norm(query, axis=1, keepdims=True)
    candidates_norm = np.linalg.norm(candidates, axis=1, keepdims=True)

    if query_norm == 0:
        return np.zeros(candidates.shape[0])

    # Avoid division by zero
    candidates_norm = np.where(candidates_norm == 0, 1, candidates_norm)

    similarities: np.ndarray = np.dot(candidates, query.T).flatten() / (
        candidates_norm.flatten() * query_norm.flatten()
    )
    return similarities
