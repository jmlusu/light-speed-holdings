"""Memory engine -- manages 6 types of company memory.

Memory types:
1. Episodic -- events and experiences (what happened)
2. Semantic -- facts and knowledge (what is known)
3. Procedural -- how-to knowledge (how to do things)
4. Relational -- entity relationships (who knows whom)
5. Temporal -- time-based records (when things happened)
6. Aggregate -- summaries and rollups (patterns and insights)

Uses FileStore for atomic persistence.  Supports optional vector-based
semantic search when a VectorStore is configured via
``enable_vector_search()``.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)


class MemoryEntry:
    """A single memory record."""

    def __init__(
        self,
        memory_type: str,
        content: str,
        metadata: dict[str, Any] | None = None,
        agent_id: str = "",
        tags: list[str] | None = None,
    ) -> None:
        self.id = f"{memory_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.memory_type = memory_type
        self.content = content
        self.metadata = metadata or {}
        self.agent_id = agent_id
        self.tags = tags or []
        self.created_at = datetime.now().isoformat()
        self.access_count = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "memory_type": self.memory_type,
            "content": self.content,
            "metadata": self.metadata,
            "agent_id": self.agent_id,
            "tags": self.tags,
            "created_at": self.created_at,
            "access_count": self.access_count,
        }


class MemoryStore:
    """Persistent memory storage backed by FileStore (JSON files).

    When a VectorStore is configured via ``enable_vector_search()``,
    the ``recall()`` method uses cosine-similarity-based semantic
    search instead of simple substring matching.
    """

    def __init__(self, base_dir: str | Path = "memory") -> None:
        self.base_dir = Path(base_dir)
        self._store = FileStore(self.base_dir, backup=False)
        self._stores: dict[str, list[MemoryEntry]] = {
            "episodic": [],
            "semantic": [],
            "procedural": [],
            "relational": [],
            "temporal": [],
            "aggregate": [],
        }
        self._vector_store: Any | None = None
        self._load_all()

    @property
    def has_vector_search(self) -> bool:
        """Return True if vector search is enabled and available."""
        return self._vector_store is not None and getattr(
            self._vector_store, "is_vector_capable", False
        )

    def enable_vector_search(
        self,
        embedding_engine: Any | None = None,
        index_dir: str | Path = "memory/vector_index",
    ) -> None:
        """Enable semantic vector search for memory recall.

        Args:
            embedding_engine: An EmbeddingEngine instance for computing embeddings.
            index_dir: Directory for persisting the vector index.
        """
        try:
            from ai_company.memory.vector_store import VectorStore

            self._vector_store = VectorStore(
                memory_store=self,
                embedding_engine=embedding_engine,
                index_dir=index_dir,
            )
            # Index existing entries
            self._vector_store.index_all()
        except ImportError:
            logger.warning("VectorStore unavailable — vector search disabled")

    def _file_name(self, memory_type: str) -> str:
        return f"{memory_type}.json"

    def _load_all(self) -> None:
        for mem_type in self._stores:
            data = self._store.read_json(self._file_name(mem_type))
            if data is None or not isinstance(data, list):
                continue
            for item in data:
                entry = MemoryEntry(
                    memory_type=mem_type,
                    content=item.get("content", ""),
                    metadata=item.get("metadata", {}),
                    agent_id=item.get("agent_id", ""),
                    tags=item.get("tags", []),
                )
                entry.id = item.get("id", entry.id)
                entry.created_at = item.get("created_at", entry.created_at)
                entry.access_count = item.get("access_count", 0)
                self._stores[mem_type].append(entry)

    def _save(self, memory_type: str) -> None:
        data = [e.to_dict() for e in self._stores[memory_type]]
        self._store.write_json(self._file_name(memory_type), data)

    def store(self, memory_type: str, content: str, **kwargs: Any) -> MemoryEntry:
        """Store a new memory entry.

        If vector search is enabled, the new entry is automatically indexed.
        """
        if memory_type not in self._stores:
            raise ValueError(f"Unknown memory type: {memory_type}")
        entry = MemoryEntry(memory_type=memory_type, content=content, **kwargs)
        self._stores[memory_type].append(entry)
        self._save(memory_type)

        # Auto-index in vector store if available
        if self._vector_store is not None:
            try:
                self._vector_store.index_entry(entry)
            except Exception:
                pass  # Non-fatal: indexing failure shouldn't break storage

        return entry

    def recall(
        self,
        memory_type: str,
        query: str = "",
        tags: list[str] | None = None,
        agent_id: str = "",
        limit: int = 10,
        use_semantic: bool = True,
    ) -> list[MemoryEntry]:
        """Recall memories with optional filtering.

        When vector search is enabled and ``use_semantic`` is True and
        a query is provided, uses cosine-similarity-based semantic search
        instead of substring matching.
        """
        if memory_type not in self._stores:
            return []

        # Use vector search if available and query provided
        if use_semantic and self._vector_store is not None and query:
            try:
                vector_results = self._vector_store.search(
                    query=query,
                    memory_type=memory_type,
                    tags=tags,
                    agent_id=agent_id,
                    top_k=limit,
                )
                return [entry for entry, _score in vector_results]
            except Exception:
                pass  # Fall through to substring search

        # Fallback to substring search
        results = self._stores[memory_type]

        if query:
            query_lower = query.lower()
            results = [e for e in results if query_lower in e.content.lower()]

        if tags:
            tag_set = set(tags)
            results = [e for e in results if tag_set.intersection(e.tags)]

        if agent_id:
            results = [e for e in results if e.agent_id == agent_id]

        # Sort by created_at descending (most recent first)
        results = sorted(results, key=lambda e: e.created_at, reverse=True)

        # Mark as accessed
        for e in results[:limit]:
            e.access_count += 1

        return results[:limit]

    def count(self, memory_type: str | None = None) -> int:
        """Count memories, optionally filtered by type."""
        if memory_type:
            return len(self._stores.get(memory_type, []))
        return sum(len(v) for v in self._stores.values())

    def stats(self) -> dict[str, int]:
        """Return counts per memory type."""
        return {k: len(v) for k, v in self._stores.items()}

    def consolidate(self, memory_type: str) -> dict[str, Any]:
        """Create an aggregate summary of a memory type."""
        entries = self._stores.get(memory_type, [])
        if not entries:
            return {"type": memory_type, "count": 0, "summary": "No entries"}

        # Build summary
        all_tags: dict[str, int] = {}
        all_agents: dict[str, int] = {}
        for e in entries:
            for tag in e.tags:
                all_tags[tag] = all_tags.get(tag, 0) + 1
            if e.agent_id:
                all_agents[e.agent_id] = all_agents.get(e.agent_id, 0) + 1

        summary = {
            "type": memory_type,
            "count": len(entries),
            "top_tags": sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_agents": sorted(all_agents.items(), key=lambda x: x[1], reverse=True)[:10],
            "latest": entries[-1].created_at if entries else None,
            "most_accessed": max(entries, key=lambda e: e.access_count).id if entries else None,
        }

        # Store as aggregate
        self.store(
            "aggregate",
            content=json.dumps(summary, indent=2),
            metadata={"source_type": memory_type, "entry_count": len(entries)},
            tags=["consolidation", memory_type],
        )

        return summary
