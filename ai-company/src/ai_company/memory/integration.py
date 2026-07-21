"""Memory integration — stores task outcomes, learns from execution, and provides
semantic search via vector embeddings.

This module bridges the executor to the memory subsystem:
- ``recall_context`` injects relevant memories before task execution
- ``record_task_outcome`` stores results after completion
- ``semantic_search`` provides embedding-based similarity search
"""

from __future__ import annotations

from typing import Any

from ai_company.memory.engine import MemoryStore

_store: MemoryStore | None = None
_vector_store: Any = None  # Lazy-loaded VectorStore


def init_memory(base_dir: str = "memory") -> MemoryStore:
    """Initialize the memory store and optional vector store."""
    global _store, _vector_store
    _store = MemoryStore(base_dir=base_dir)
    # Initialize vector store with EmbeddingEngine for real semantic search
    try:
        from ai_company.ml.embeddings import EmbeddingEngine
        from ai_company.memory.vector_store import VectorStore

        engine = EmbeddingEngine(
            model_name="all-MiniLM-L6-v2",
            cache_dir=f"{base_dir}/embeddings",
        )
        _vector_store = VectorStore(
            memory_store=_store,
            embedding_engine=engine,
            index_dir=f"{base_dir}/vector_index",
        )
        # Index existing entries
        _vector_store.index_all()
    except Exception:
        _vector_store = None
    return _store


def get_store() -> MemoryStore | None:
    return _store


def record_task_outcome(
    task_id: str,
    agent_id: str,
    instruction: str,
    status: str,
    result_summary: str,
    tools_used: list[str] | None = None,
) -> None:
    """Record a completed task as episodic memory."""
    if _store is None:
        return
    tags = [status, agent_id]
    if tools_used:
        tags.extend(tools_used)
    content = f"Task {task_id}: {instruction[:200]}\nStatus: {status}\nResult: {result_summary[:300]}"
    _store.store(
        "episodic",
        content=content,
        agent_id=agent_id,
        tags=tags,
        metadata={"task_id": task_id, "status": status},
    )


def record_knowledge(agent_id: str, topic: str, content: str, tags: list[str] | None = None) -> None:
    """Record semantic knowledge discovered during execution."""
    if _store is None:
        return
    _store.store("semantic", content=content, agent_id=agent_id, tags=tags or [topic])


def record_procedure(agent_id: str, procedure: str, context: str, tags: list[str] | None = None) -> None:
    """Record procedural how-to knowledge."""
    if _store is None:
        return
    _store.store("procedural", content=procedure, agent_id=agent_id, tags=tags or ["procedure"])


def recall_context(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Recall relevant memories for context loading.

    Tries semantic (vector) search first for high-quality results.
    Falls back to keyword-based search if vector store is unavailable
    or returns no results.
    """
    if _store is None:
        return []

    # Try semantic search first
    if _vector_store is not None:
        try:
            raw = _vector_store.search(query, top_k=limit)
            if raw:
                return [
                    {
                        "type": entry.memory_type,
                        "content": entry.content,
                        "agent_id": entry.agent_id,
                        "tags": entry.tags,
                        "similarity": round(score, 4),
                    }
                    for entry, score in raw
                ]
        except Exception:
            pass  # Fall through to keyword search

    # Fallback: keyword-based search
    results: list[dict[str, Any]] = []
    for mem_type in ["episodic", "semantic", "procedural"]:
        entries = _store.recall(mem_type, query=query, limit=limit)
        for e in entries:
            results.append(
                {"type": mem_type, "content": e.content, "agent_id": e.agent_id, "tags": e.tags}
            )
    return results[:limit]


def semantic_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search memories using embedding-based semantic similarity.

    Returns results from all memory types, ranked by cosine similarity.
    Each result includes a 'similarity' score (0.0 to 1.0).
    """
    if _vector_store is None:
        return []

    try:
        raw = _vector_store.search(query, top_k=top_k)
        return [
            {
                "type": entry.memory_type,
                "content": entry.content,
                "agent_id": entry.agent_id,
                "tags": entry.tags,
                "similarity": round(score, 4),
            }
            for entry, score in raw
        ]
    except Exception:
        return []


def store_semantic(
    doc_id: str,
    content: str,
    agent_id: str = "",
    tags: list[str] | None = None,
    memory_type: str = "semantic",
) -> None:
    """Store a document in the vector store for semantic search.

    Creates a MemoryEntry in the underlying store, then indexes it
    in the vector store for embedding-based retrieval.
    """
    if _store is None or _vector_store is None:
        return
    try:
        entry = _store.store(
            memory_type,
            content=content,
            agent_id=agent_id,
            tags=tags or [],
        )
        _vector_store.index_entry(entry)
        _vector_store.save_index()
    except Exception:
        pass  # Non-fatal: semantic storage is best-effort
