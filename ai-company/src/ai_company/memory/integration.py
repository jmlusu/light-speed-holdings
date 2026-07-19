"""Memory integration — stores task outcomes and learns from execution."""

from __future__ import annotations

from typing import Any

from ai_company.memory.engine import MemoryStore

_store: MemoryStore | None = None


def init_memory(base_dir: str = "memory") -> MemoryStore:
    global _store
    _store = MemoryStore(base_dir=base_dir)
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
    """Recall relevant memories for context loading."""
    if _store is None:
        return []
    results: list[dict[str, Any]] = []
    for mem_type in ["episodic", "semantic", "procedural"]:
        entries = _store.recall(mem_type, query=query, limit=limit)
        for e in entries:
            results.append(
                {"type": mem_type, "content": e.content, "agent_id": e.agent_id, "tags": e.tags}
            )
    return results[:limit]
