"""Memory integration — stores task outcomes, learns from execution, and provides
semantic search via vector embeddings.

This module bridges the executor to the memory subsystem:
- ``recall_context`` injects relevant memories before task execution
- ``record_task_outcome`` stores results after completion
- ``semantic_search`` provides embedding-based similarity search
"""

from __future__ import annotations

import os
from typing import Any

from ai_company.memory.engine import MemoryStore

_store: MemoryStore | None = None
_vector_store: Any = None  # Lazy-loaded VectorStore

# Explicit disable values for the AI_COMPANY_LEARNING_ENABLED feature flag.
# Anything else (absent, "1", "true", "yes", ...) enables learning.
_LEARNING_DISABLE_VALUES = {"0", "false", "no", "off"}


def learning_enabled() -> bool:
    """Return whether the continuous-learning pipeline is enabled (ticket #232).

    Reads the ``AI_COMPANY_LEARNING_ENABLED`` feature-flag: absent means
    enabled (default-on), and explicit disable values (``0``, ``false``,
    ``no``, ``off`` — case-insensitive, whitespace-trimmed) disable the
    pipeline.  This is the rollback switch for learning instrumentation.
    """
    value = os.environ.get("AI_COMPANY_LEARNING_ENABLED")
    if value is None:
        return True
    return value.strip().lower() not in _LEARNING_DISABLE_VALUES


def init_memory(base_dir: str = "memory") -> MemoryStore:
    """Initialize the memory store and optional vector store."""
    global _store, _vector_store
    _store = MemoryStore(base_dir=base_dir)
    # Initialize vector store with EmbeddingEngine for real semantic search
    try:
        from ai_company.memory.vector_store import VectorStore
        from ai_company.ml.embeddings import EmbeddingEngine

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
    except Exception:  # noqa: BLE001 - vector store is best-effort
        _vector_store = None
    return _store


def get_store() -> MemoryStore | None:
    return _store


def pin_memory(entry_id: str) -> bool:
    """Curator override: pin a memory so it survives prune/digest."""
    if _store is None:
        return False
    return _store.pin(entry_id)


def unpin_memory(entry_id: str) -> bool:
    """Remove a pin from a memory entry."""
    if _store is None:
        return False
    return _store.unpin(entry_id)


def governance_summary() -> dict[str, Any]:
    """Return the active governance policy (TTLs, staleness window, blocklist)."""
    if _store is None:
        return {}
    gov = getattr(_store, "governance", None)
    if gov is None:
        return {}
    return {
        "retention_ttl_days": dict(gov.retention_ttl_days),
        "staleness_days": gov.staleness_days,
        "constitutional_blocklist": list(gov.constitutional_blocklist),
        "min_knowledge_length": gov.min_knowledge_length,
    }


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
    content = (
        f"Task {task_id}: {instruction[:200]}\nStatus: {status}\nResult: {result_summary[:300]}"
    )
    _store.store(
        "episodic",
        content=content,
        agent_id=agent_id,
        tags=tags,
        metadata={"task_id": task_id, "status": status},
    )


def record_knowledge(
    agent_id: str, topic: str, content: str, tags: list[str] | None = None
) -> None:
    """Record semantic knowledge discovered during execution."""
    if _store is None:
        return
    _store.store("semantic", content=content, agent_id=agent_id, tags=tags or [topic])


def record_procedure(
    agent_id: str, procedure: str, context: str, tags: list[str] | None = None
) -> None:
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
    if not learning_enabled():
        return []
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
        except Exception:  # noqa: BLE001 - vector search is best-effort
            pass  # Fall through to keyword search

    # Fallback: keyword-based search
    results: list[dict[str, Any]] = []
    for mem_type in ["episodic", "semantic", "procedural"]:
        entries = _store.recall(mem_type, query=query, limit=limit)
        for e in entries:
            results.append(
                {"type": mem_type, "content": e.content, "agent_id": e.agent_id, "tags": e.tags}
            )

    # Token-overlap expansion: substring search is too strict for natural
    # queries that do not appear verbatim in memory content. Score entries by
    # how many query tokens appear in their content + tags when substring
    # search found nothing, so realistic queries still surface memories.
    if not results and query:
        tokens = [t.lower() for t in query.split() if len(t) >= 2]
        if tokens:
            scored: list[tuple[float, dict[str, Any]]] = []
            for mem_type in ["episodic", "semantic", "procedural"]:
                for e in _store.recall(mem_type, limit=limit * 20):
                    haystack = f"{e.content} {' '.join(e.tags)}".lower()
                    overlap = sum(1 for t in tokens if t in haystack)
                    if overlap:
                        score = overlap / len(tokens)
                        scored.append(
                            (
                                score,
                                {
                                    "type": mem_type,
                                    "content": e.content,
                                    "agent_id": e.agent_id,
                                    "tags": e.tags,
                                    "similarity": round(score, 4),
                                },
                            )
                        )
            scored.sort(key=lambda item: item[0], reverse=True)
            results = [item[1] for item in scored[:limit]]

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
    except Exception:  # noqa: BLE001 - vector search is best-effort
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
    except Exception:  # noqa: BLE001 - semantic storage is best-effort
        pass  # Non-fatal: semantic storage is best-effort


# ---------------------------------------------------------------------------
# Post-task knowledge extraction — heuristic-based (no LLM cost)
# ---------------------------------------------------------------------------


def extract_post_task_knowledge(
    task_id: str,
    agent_id: str,
    instruction: str,
    status: str,
    result_summary: str,
    tool_results: list[Any] | None = None,
) -> None:
    """Extract semantic and procedural knowledge from a completed task.

    Uses heuristic pattern-matching on tool traces and the final response
    to distill what was learned (semantic) and how to do it again (procedural).
    No LLM call — purely pattern-based, zero additional cost.

    Args:
        task_id: The task identifier.
        agent_id: The agent that executed the task.
        instruction: The original task instruction.
        status: Task outcome (completed, failed, timeout).
        result_summary: The final response text.
        tool_results: List of ToolResult records from the loop.
    """
    if _store is None:
        return

    # --- Semantic extraction: what was learned ---
    if status == "completed" and result_summary:
        tool_names = [r.tool for r in (tool_results or []) if r.tool]
        if tool_names:
            unique_tools = list(dict.fromkeys(tool_names))
            topic = f"task-pattern:{agent_id}"
            content = (
                f"Agent {agent_id} solved: {instruction[:150]}\n"
                f"Tools used (in order): {', '.join(unique_tools)}\n"
                f"Outcome: {result_summary[:200]}"
            )
            record_knowledge(
                agent_id=agent_id,
                topic=topic,
                content=content,
                tags=["auto-extracted", "task-pattern", status, agent_id],
            )

    # --- Procedural extraction: error → fix patterns ---
    if status == "failed" and tool_results:
        failed_tools = [r for r in tool_results if r.status != "ok"]
        if failed_tools:
            for record in failed_tools:
                tool_name = record.tool or "unknown"
                error_msg = (
                    record.error or record.output[:200] if record.output else "unknown error"
                )
                procedure = (
                    f"When {tool_name} fails during task like '{instruction[:100]}':\n"
                    f"Error was: {error_msg[:150]}\n"
                    f"The task ultimately {'succeeded' if status == 'completed' else 'failed'}."
                )
                record_procedure(
                    agent_id=agent_id,
                    procedure=procedure,
                    context=f"error-recovery:{tool_name}",
                    tags=["auto-extracted", "error-recovery", tool_name, agent_id],
                )

    # --- Procedural extraction: timeout patterns ---
    if status == "timeout" and tool_results:
        tool_names = [r.tool for r in tool_results if r.tool]
        if tool_names:
            unique_tools = list(dict.fromkeys(tool_names))
            procedure = (
                f"Task timed out after using: {', '.join(unique_tools)}\n"
                f"Instruction was: {instruction[:150]}\n"
                f"Consider breaking this into smaller subtasks or increasing iteration limit."
            )
            record_procedure(
                agent_id=agent_id,
                procedure=procedure,
                context="timeout-prevention",
                tags=["auto-extracted", "timeout", agent_id],
            )
