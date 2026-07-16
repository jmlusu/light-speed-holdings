"""Memory engine — manages 6 types of company memory.

Memory types:
1. Episodic — events and experiences (what happened)
2. Semantic — facts and knowledge (what is known)
3. Procedural — how-to knowledge (how to do things)
4. Relational — entity relationships (who knows whom)
5. Temporal — time-based records (when things happened)
6. Aggregate — summaries and rollups (patterns and insights)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


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
    """Persistent memory storage backed by JSON files."""

    def __init__(self, base_dir: str | Path = "memory") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._stores: dict[str, list[MemoryEntry]] = {
            "episodic": [],
            "semantic": [],
            "procedural": [],
            "relational": [],
            "temporal": [],
            "aggregate": [],
        }
        self._load_all()

    def _file_path(self, memory_type: str) -> Path:
        return self.base_dir / f"{memory_type}.json"

    def _load_all(self) -> None:
        for mem_type in self._stores:
            path = self._file_path(mem_type)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
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
        path = self._file_path(memory_type)
        data = [e.to_dict() for e in self._stores[memory_type]]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def store(self, memory_type: str, content: str, **kwargs: Any) -> MemoryEntry:
        """Store a new memory entry."""
        if memory_type not in self._stores:
            raise ValueError(f"Unknown memory type: {memory_type}")
        entry = MemoryEntry(memory_type=memory_type, content=content, **kwargs)
        self._stores[memory_type].append(entry)
        self._save(memory_type)
        return entry

    def recall(
        self,
        memory_type: str,
        query: str = "",
        tags: list[str] | None = None,
        agent_id: str = "",
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """Recall memories with optional filtering."""
        if memory_type not in self._stores:
            return []

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
