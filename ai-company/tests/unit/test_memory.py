"""Tests for the Memory engine."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.memory.engine import MemoryEntry, MemoryStore


@pytest.fixture()
def store(tmp_path: Path) -> MemoryStore:
    return MemoryStore(base_dir=tmp_path / "memory")


class TestMemoryEntry:
    def test_create_entry(self):
        entry = MemoryEntry("episodic", "Did something", agent_id="ceo", tags=["important"])
        assert entry.memory_type == "episodic"
        assert entry.content == "Did something"
        assert entry.agent_id == "ceo"
        assert "important" in entry.tags
        assert entry.access_count == 0

    def test_to_dict(self):
        entry = MemoryEntry("semantic", "Fact: sky is blue")
        d = entry.to_dict()
        assert d["memory_type"] == "semantic"
        assert d["content"] == "Fact: sky is blue"
        assert "id" in d
        assert "created_at" in d


class TestMemoryStore:
    def test_store_and_recall(self, store: MemoryStore):
        store.store("episodic", "Team meeting happened", agent_id="ceo", tags=["meeting"])
        results = store.recall("episodic", query="meeting")
        assert len(results) == 1
        assert "meeting" in results[0].content

    def test_recall_by_tag(self, store: MemoryStore):
        store.store("semantic", "Python is a language", tags=["tech", "python"])
        store.store("semantic", "Company policy on PTO", tags=["policy"])
        results = store.recall("semantic", tags=["tech"])
        assert len(results) == 1
        assert "Python" in results[0].content

    def test_recall_by_agent(self, store: MemoryStore):
        store.store("procedural", "How to deploy", agent_id="devops")
        store.store("procedural", "How to hire", agent_id="hr")
        results = store.recall("procedural", agent_id="hr")
        assert len(results) == 1
        assert "hire" in results[0].content

    def test_count(self, store: MemoryStore):
        store.store("episodic", "Event 1")
        store.store("episodic", "Event 2")
        store.store("semantic", "Fact 1")
        assert store.count("episodic") == 2
        assert store.count("semantic") == 1
        assert store.count() == 3

    def test_stats(self, store: MemoryStore):
        store.store("episodic", "A")
        store.store("semantic", "B")
        store.store("semantic", "C")
        stats = store.stats()
        assert stats["episodic"] == 1
        assert stats["semantic"] == 2
        assert stats["procedural"] == 0

    def test_unknown_type_raises(self, store: MemoryStore):
        with pytest.raises(ValueError, match="Unknown memory type"):
            store.store("nonexistent", "data")

    def test_persistence(self, tmp_path: Path):
        """Data persists across store instances."""
        store1 = MemoryStore(base_dir=tmp_path / "mem")
        store1.store("temporal", "Timestamped event")

        store2 = MemoryStore(base_dir=tmp_path / "mem")
        results = store2.recall("temporal")
        assert len(results) == 1

    def test_consolidate(self, store: MemoryStore):
        store.store("episodic", "Meeting 1", tags=["meeting"], agent_id="ceo")
        store.store("episodic", "Meeting 2", tags=["meeting", "review"], agent_id="cto")
        summary = store.consolidate("episodic")
        assert summary["count"] == 2
        assert summary["type"] == "episodic"
        # Should have created an aggregate entry
        assert store.count("aggregate") >= 1

    def test_recall_limit(self, store: MemoryStore):
        for i in range(20):
            store.store("temporal", f"Event {i}")
        results = store.recall("temporal", limit=5)
        assert len(results) == 5
