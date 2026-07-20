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

import itertools
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# Monotonic insertion counter so recency ordering is deterministic even when
# two entries share an identical ``created_at`` timestamp (e.g. stored within
# the same tick). Persisted alongside each entry so reloads preserve order.
_entry_sequence = itertools.count()


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
        self.seq = next(_entry_sequence)

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
            "seq": self.seq,
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
                entry.seq = item.get("seq", next(_entry_sequence))
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

        # Sort by insertion sequence descending (most recent first); created_at
        # is a secondary tie-breaker for entries reloaded from disk.
        results = sorted(results, key=lambda e: (e.seq, e.created_at), reverse=True)

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

    def _relevance_score(self, entry: MemoryEntry, terms: list[str]) -> int:
        """Compute a simple term-frequency relevance score for an entry.

        Counts how many times any query term appears (as a substring) in the
        entry's content, tags, and metadata values.  Higher is more relevant.
        """
        haystack_parts = [entry.content]
        haystack_parts.extend(entry.tags)
        haystack_parts.extend(str(v) for v in entry.metadata.values())
        haystack = " ".join(haystack_parts).lower()
        score = 0
        for term in terms:
            score += haystack.count(term)
        return score

    def search(
        self,
        query: str,
        memory_type: str | None = None,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """Search memories across all (or one) type by keyword/substring match.

        Performs case-insensitive keyword matching across stored memory
        content, tags, and metadata.  If vector (semantic) search is enabled
        and available, it is used preferentially for ranking; otherwise a
        simple term-frequency relevance score is used to rank keyword hits.

        Args:
            query: The search query (matched as substrings, space-split into terms).
            memory_type: Optional single memory type to restrict the search to.
            limit: Maximum number of results to return.

        Returns:
            A list of matching :class:`MemoryEntry` objects ranked by relevance
            (most relevant first), truncated to ``limit``.
        """
        if limit <= 0:
            return []

        types = [memory_type] if memory_type else list(self._stores.keys())
        # Validate explicit type
        if memory_type and memory_type not in self._stores:
            return []

        query_lower = query.lower()
        terms = [t for t in query_lower.split() if t]

        # Gather candidate entries across the requested types.
        candidates: list[MemoryEntry] = []
        for mem_type in types:
            candidates.extend(self._stores.get(mem_type, []))

        if not candidates:
            return []

        # Prefer semantic/vector search when available, a query is given, and a
        # single memory type is requested (the VectorStore filters by one type).
        if query and self.has_vector_search and self._vector_store is not None and memory_type:
            try:
                raw = self._vector_store.search(
                    query=query,
                    memory_type=memory_type,
                    top_k=limit,
                )
                if raw:
                    results = [entry for entry, _score in raw]
                    for entry in results:
                        entry.access_count += 1
                    return results[:limit]
            except Exception:
                pass  # Fall through to keyword ranking

        # Keyword path: keep entries that match any term in content/tags/metadata.
        if not terms:
            # Empty/whitespace query: return most recent across types.
            matched = sorted(
                candidates, key=lambda e: (e.seq, e.created_at), reverse=True
            )
        else:
            scored: list[tuple[int, MemoryEntry]] = []
            for entry in candidates:
                score = self._relevance_score(entry, terms)
                if score > 0:
                    scored.append((score, entry))
            # Sort by relevance desc, then most-recent as tie-breaker.
            matched = [
                e
                for _score, e in sorted(
                    scored,
                    key=lambda t: (t[0], t[1].seq, t[1].created_at),
                    reverse=True,
                )
            ]

        # Mark matched entries as accessed.
        for entry in matched[:limit]:
            entry.access_count += 1

        return matched[:limit]

    def prune(
        self,
        max_age_days: int | None = None,
        max_entries_per_type: int | None = None,
    ) -> int:
        """Remove memories based on age and/or per-type entry caps.

        - Memories older than ``max_age_days`` (by ``created_at``) are removed.
        - Each memory type is trimmed to the most-recently-accessed/created
          ``max_entries_per_type`` entries (ties broken by ``created_at``).

        Args:
            max_age_days: If set, drop entries older than this many days.
            max_entries_per_type: If set, cap each type to this many entries,
                keeping the most-accessed (then most-recently-created).

        Returns:
            The total number of entries pruned.  Changes are persisted.
        """
        if max_age_days is None and max_entries_per_type is None:
            return 0

        pruned = 0
        now = datetime.now()

        for mem_type, entries in self._stores.items():
            if not entries:
                continue

            survivors = list(entries)

            # Age-based filtering.
            if max_age_days is not None:
                kept_by_age: list[MemoryEntry] = []
                for entry in survivors:
                    try:
                        created = datetime.fromisoformat(entry.created_at)
                    except ValueError:
                        created = now
                    age_days = (now - created).total_seconds() / 86400.0
                    if age_days > max_age_days:
                        pruned += 1
                    else:
                        kept_by_age.append(entry)
                survivors = kept_by_age

            # Per-type cap (most-accessed first, then most-recently-created).
            if max_entries_per_type is not None and len(survivors) > max_entries_per_type:
                survivors.sort(
                    key=lambda e: (e.access_count, e.created_at),
                    reverse=True,
                )
                dropped = survivors[max_entries_per_type:]
                pruned += len(dropped)
                survivors = survivors[:max_entries_per_type]

            # Only persist if the list actually changed.
            if len(survivors) != len(entries):
                self._stores[mem_type] = survivors
                self._save(mem_type)

        return pruned

    def consolidate_all(self) -> dict[str, int]:
        """Periodic maintenance pass across all memory types.

        Performs a safe, idempotent maintenance routine:
        1. Deduplicates near-identical semantic memories (same normalized
           content within the ``semantic`` type), keeping the earliest entry.
        2. Rolls up aggregate statistics by re-running ``consolidate`` on each
           non-aggregate type whose entry count exceeds the number of existing
           aggregate rollups for that type.

        This method is intended to be called periodically (e.g. by a scheduler)
        and is safe to invoke repeatedly — duplicates are removed once and
        aggregate summaries are rebuilt deterministically.

        Returns:
            A summary dict with keys:
              - ``semantic_duplicates_removed``
              - ``aggregates_created``
              - ``types_processed``
        """
        summary = {
            "semantic_duplicates_removed": 0,
            "aggregates_created": 0,
            "types_processed": 0,
        }

        # 1. Deduplicate near-identical semantic memories.
        semantic_entries = self._stores.get("semantic", [])
        if semantic_entries:
            seen: dict[str, MemoryEntry] = {}
            deduped: list[MemoryEntry] = []
            for entry in semantic_entries:
                key = " ".join(entry.content.lower().split())
                if key in seen:
                    # Drop the later duplicate (keep earliest by created_at).
                    existing = seen[key]
                    if entry.created_at < existing.created_at:
                        # Replace: keep the earlier one, drop the existing.
                        deduped = [e for e in deduped if e is not existing]
                        seen[key] = entry
                        deduped.append(entry)
                    summary["semantic_duplicates_removed"] += 1
                    continue
                seen[key] = entry
                deduped.append(entry)
            if len(deduped) != len(semantic_entries):
                self._stores["semantic"] = deduped
                self._save("semantic")

        # 2. Roll up aggregate stats per non-aggregate type.
        for mem_type in ("episodic", "semantic", "procedural", "relational", "temporal"):
            entries = self._stores.get(mem_type, [])
            if not entries:
                continue
            summary["types_processed"] += 1
            # Count existing aggregate rollups sourced from this type.
            existing_rollups = sum(
                1
                for e in self._stores.get("aggregate", [])
                if e.metadata.get("source_type") == mem_type
            )
            # Rebuild rollup when counts diverge from current entry count.
            if existing_rollups != len(entries) or existing_rollups == 0:
                self.consolidate(mem_type)
                summary["aggregates_created"] += 1

        return summary

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
