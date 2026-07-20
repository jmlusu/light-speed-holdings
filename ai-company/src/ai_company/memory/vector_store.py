"""Vector store — embedding-backed semantic memory search.

Extends MemoryStore with cosine-similarity-based retrieval using
sentence-transformers embeddings.  Falls back to substring search
when embeddings are unavailable.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

from ai_company.memory.engine import MemoryEntry, MemoryStore

logger = logging.getLogger(__name__)


class VectorStore:
    """Semantic vector store layered on top of MemoryStore.

    Maintains an embedding index alongside the JSON-backed memory store.
    When the embedding engine is available, recall uses cosine similarity;
    otherwise it falls back to the base MemoryStore substring search.

    Args:
        memory_store: The underlying MemoryStore instance.
        embedding_engine: Optional EmbeddingEngine for vector search.
        index_dir: Directory for persisting the vector index.
    """

    def __init__(
        self,
        memory_store: MemoryStore,
        embedding_engine: Any | None = None,
        index_dir: str | Path = "memory/vector_index",
    ) -> None:
        self.store = memory_store
        self.engine = embedding_engine
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)

        # In-memory index: entry_id -> embedding vector (np.ndarray or list)
        self._index: dict[str, Any] = {}
        self._entry_cache: dict[str, MemoryEntry] = {}

        if self.engine is not None:
            self._load_index()

    @property
    def is_vector_capable(self) -> bool:
        """Return True if vector search is available."""
        return self.engine is not None

    def index_entry(self, entry: MemoryEntry) -> None:
        """Add a memory entry to the vector index.

        Args:
            entry: The MemoryEntry to index.
        """
        if self.engine is None:
            return

        embedding = self.engine.encode(entry.content)
        self._index[entry.id] = embedding
        self._entry_cache[entry.id] = entry

    def index_all(self, memory_type: str | None = None) -> int:
        """Index all entries from the memory store.

        Args:
            memory_type: If provided, index only this type; else index all.

        Returns:
            Number of entries indexed.
        """
        if self.engine is None:
            return 0

        count = 0
        types_to_index = [memory_type] if memory_type else list(self.store._stores.keys())

        for mem_type in types_to_index:
            for entry in self.store._stores.get(mem_type, []):
                if entry.id not in self._index:
                    self.index_entry(entry)
                    count += 1

        self.save_index()
        return count

    def search(
        self,
        query: str,
        memory_type: str | None = None,
        tags: list[str] | None = None,
        agent_id: str = "",
        top_k: int = 10,
        min_score: float = 0.3,
    ) -> list[tuple[MemoryEntry, float]]:
        """Semantic search using cosine similarity.

        Args:
            query: The search query text.
            memory_type: Filter to this memory type.
            tags: Filter to entries matching these tags.
            agent_id: Filter to entries from this agent.
            top_k: Maximum results to return.
            min_score: Minimum similarity score threshold.

        Returns:
            List of (MemoryEntry, score) tuples sorted by descending score.
        """
        if self.engine is None or not self._index or not _HAS_NUMPY:
            # Fallback to substring search
            return self._fallback_search(query, memory_type, tags, agent_id, top_k)

        query_emb = self.engine.encode(query)

        # Filter candidate IDs
        candidates: list[str] = []
        for eid, entry in self._entry_cache.items():
            if memory_type and entry.memory_type != memory_type:
                continue
            if tags and not set(tags).intersection(entry.tags):
                continue
            if agent_id and entry.agent_id != agent_id:
                continue
            if eid in self._index:
                candidates.append(eid)

        if not candidates:
            return []

        # Compute similarities
        matrix = np.stack([self._index[eid] for eid in candidates])
        norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8
        normalized = matrix / norms
        scores = normalized @ query_emb

        # Sort and filter
        scored = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        results: list[tuple[MemoryEntry, float]] = []
        for eid, score in scored:
            if score < min_score:
                break
            if len(results) >= top_k:
                break
            found: MemoryEntry | None = self._entry_cache.get(eid)
            if found is None:
                found = self._find_entry(eid, memory_type)
            if found is not None:
                found.access_count += 1
                results.append((found, float(score)))

        return results

    def _fallback_search(
        self,
        query: str,
        memory_type: str | None,
        tags: list[str] | None,
        agent_id: str,
        top_k: int,
    ) -> list[tuple[MemoryEntry, float]]:
        """Fall back to substring-based search when embeddings unavailable."""
        results: list[tuple[MemoryEntry, float]] = []
        query_lower = query.lower()

        types_to_search = [memory_type] if memory_type else list(self.store._stores.keys())

        for mem_type in types_to_search:
            for entry in self.store._stores.get(mem_type, []):
                if tags and not set(tags).intersection(entry.tags):
                    continue
                if agent_id and entry.agent_id != agent_id:
                    continue
                if query_lower in entry.content.lower():
                    # Approximate score based on match density
                    matches = entry.content.lower().count(query_lower)
                    score = min(1.0, matches * 0.3)
                    results.append((entry, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _find_entry(self, entry_id: str, memory_type: str | None = None) -> MemoryEntry | None:
        """Look up an entry by ID from the memory store."""
        types_to_search = [memory_type] if memory_type else list(self.store._stores.keys())
        for mem_type in types_to_search:
            for entry in self.store._stores.get(mem_type, []):
                if entry.id == entry_id:
                    return entry
        return None

    def save_index(self) -> None:
        """Persist the vector index to disk."""
        index_file = self.index_dir / "vector_index.json"
        data: dict[str, Any] = {}
        for eid, vec in self._index.items():
            data[eid] = vec.tolist() if hasattr(vec, "tolist") else list(vec)

        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _load_index(self) -> None:
        """Load the vector index from disk."""
        index_file = self.index_dir / "vector_index.json"
        if not index_file.exists():
            return
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for eid, vec_list in data.items():
                if _HAS_NUMPY:
                    self._index[eid] = np.array(vec_list, dtype=np.float32)
                else:
                    self._index[eid] = vec_list
            logger.info("Loaded vector index with %d entries", len(self._index))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load vector index: %s", exc)
