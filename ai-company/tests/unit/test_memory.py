"""Tests for the Memory engine."""

from __future__ import annotations

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


class TestMemorySearch:
    def test_search_keyword_across_types(self, store: MemoryStore):
        store.store("episodic", "Team meeting about roadmap", tags=["meeting"])
        store.store("semantic", "Python is a programming language", tags=["tech"])
        store.store("procedural", "How to deploy the service", tags=["ops"])
        results = store.search("meeting")
        assert len(results) == 1
        assert results[0].memory_type == "episodic"

    def test_search_case_insensitive(self, store: MemoryStore):
        store.store("semantic", "The QUICK brown fox", tags=["animal"])
        results = store.search("quick")
        assert len(results) == 1

    def test_search_filtered_by_type(self, store: MemoryStore):
        store.store("semantic", "deploy python service", tags=["tech"])
        store.store("procedural", "deploy via kubernetes", tags=["ops"])
        results = store.search("deploy", memory_type="procedural")
        assert len(results) == 1
        assert results[0].memory_type == "procedural"

    def test_search_unknown_type_returns_empty(self, store: MemoryStore):
        store.store("semantic", "fact")
        assert store.search("fact", memory_type="bogus") == []

    def test_search_relevance_ranking(self, store: MemoryStore):
        # Entry with more term occurrences should rank higher.
        store.store("semantic", "python python python", tags=["tech"])
        store.store("semantic", "python", tags=["tech"])
        results = store.search("python")
        assert len(results) == 2
        assert results[0].content.count("python") == 3

    def test_search_matches_tag_and_metadata(self, store: MemoryStore):
        store.store("semantic", "unrelated content", tags=["kubernetes"], metadata={"topic": "helm"})
        results = store.search("helm")
        assert len(results) == 1

    def test_search_limit(self, store: MemoryStore):
        for i in range(15):
            store.store("temporal", f"event {i}")
        results = store.search("event", limit=5)
        assert len(results) == 5

    def test_search_increments_access_count(self, store: MemoryStore):
        entry = store.store("semantic", "accessed memory", tags=["x"])
        assert entry.access_count == 0
        store.search("accessed")
        # The matched entry retains an incremented access count (persisted).
        assert entry.access_count == 1

    def test_search_no_query_returns_most_recent(self, store: MemoryStore):
        store.store("temporal", "first")
        store.store("temporal", "second")
        results = store.search("")
        assert len(results) == 2
        assert results[0].content == "second"

    def test_search_zero_limit(self, store: MemoryStore):
        store.store("semantic", "fact")
        assert store.search("fact", limit=0) == []


class TestMemoryPrune:
    def test_prune_max_age(self, store: MemoryStore):
        old = store.store("temporal", "old event")
        old.created_at = "2000-01-01T00:00:00"
        store._save("temporal")
        store.store("temporal", "new event")
        # Reset in-memory and reload to apply persisted timestamp.
        store._stores["temporal"] = []
        store._load_all()
        pruned = store.prune(max_age_days=1)
        assert pruned == 1
        assert store.count("temporal") == 1
        remaining = store.recall("temporal")
        assert remaining[0].content == "new event"

    def test_prune_max_entries_per_type(self, store: MemoryStore):
        for i in range(5):
            store.store("semantic", f"fact {i}")
        # Mark the earliest as most-accessed so it survives the cap.
        store._stores["semantic"][0].access_count = 100
        store._save("semantic")
        pruned = store.prune(max_entries_per_type=2)
        assert pruned == 3
        assert store.count("semantic") == 2

    def test_prune_returns_zero_when_no_args(self, store: MemoryStore):
        store.store("semantic", "fact")
        assert store.prune() == 0

    def test_prune_persists_changes(self, tmp_path: Path):
        base = tmp_path / "mem"
        s1 = MemoryStore(base_dir=base)
        s1.store("episodic", "keep me")
        old = s1.store("episodic", "drop me")
        old.created_at = "1999-01-01T00:00:00"
        s1._save("episodic")
        s1.prune(max_age_days=1)
        s2 = MemoryStore(base_dir=base)
        assert s2.count("episodic") == 1
        assert "keep me" in s2.recall("episodic")[0].content

    def test_prune_noop_when_within_limits(self, store: MemoryStore):
        store.store("semantic", "a")
        store.store("semantic", "b")
        assert store.prune(max_entries_per_type=10) == 0


class TestMemoryConsolidateAll:
    def test_consolidate_all_creates_aggregates(self, store: MemoryStore):
        store.store("episodic", "Meeting 1", tags=["m"], agent_id="ceo")
        store.store("semantic", "Fact 1", tags=["t"], agent_id="cto")
        summary = store.consolidate_all()
        assert summary["types_processed"] == 2
        assert summary["aggregates_created"] == 2
        assert store.count("aggregate") >= 2

    def test_consolidate_all_dedup_semantic(self, store: MemoryStore):
        store.store("semantic", "Python is great")
        store.store("semantic", "python  is   great")  # near-identical, normalized equal
        store.store("semantic", "Unique fact")
        summary = store.consolidate_all()
        # Write-time dedup catches the duplicate at store(), so only 2
        # entries exist by the time consolidate_all runs.
        assert summary["semantic_duplicates_removed"] == 0
        assert store.count("semantic") == 2

    def test_consolidate_all_idempotent(self, store: MemoryStore):
        store.store("episodic", "Event A", tags=["x"])
        store.consolidate_all()
        agg_after_first = store.count("aggregate")
        second = store.consolidate_all()
        # Calling again should not keep growing aggregates unbounded:
        # only rebuild when counts diverge, so re-run is safe.
        assert second["semantic_duplicates_removed"] == 0
        assert store.count("aggregate") == agg_after_first


class TestContentHash:
    def test_content_hash_deterministic(self):
        """Content hash should be deterministic for same input."""
        hash1 = MemoryEntry.content_hash("Hello World")
        hash2 = MemoryEntry.content_hash("Hello World")
        assert hash1 == hash2

    def test_content_hash_normalizes_whitespace(self):
        """Content hash should normalize whitespace."""
        hash1 = MemoryEntry.content_hash("Hello   World")
        hash2 = MemoryEntry.content_hash("Hello World")
        assert hash1 == hash2

    def test_content_hash_normalizes_case(self):
        """Content hash should be case-insensitive."""
        hash1 = MemoryEntry.content_hash("Hello World")
        hash2 = MemoryEntry.content_hash("hello world")
        assert hash1 == hash2

    def test_content_hash_differs_for_different_content(self):
        """Different content should produce different hashes."""
        hash1 = MemoryEntry.content_hash("alpha")
        hash2 = MemoryEntry.content_hash("beta")
        assert hash1 != hash2


class TestStoreDedup:
    def test_store_deduplicates_identical_content(self, store: MemoryStore):
        """Storing identical content twice should create only one entry."""
        content = "This is a test memory entry"
        entry1 = store.store("episodic", content)
        entry2 = store.store("episodic", content)
        assert entry1.id == entry2.id  # Same entry returned

    def test_store_allows_different_content_same_type(self, store: MemoryStore):
        """Different content in same type should create separate entries."""
        entry1 = store.store("episodic", "First memory")
        entry2 = store.store("episodic", "Second memory")
        assert entry1.id != entry2.id

    def test_store_allows_same_content_different_type(self, store: MemoryStore):
        """Same content in different types should create separate entries."""
        entry1 = store.store("episodic", "Shared memory")
        entry2 = store.store("semantic", "Shared memory")
        assert entry1.id != entry2.id

    def test_dedup_count_unchanged(self, store: MemoryStore):
        """Duplicate store should not increase the count."""
        store.store("episodic", "unique fact")
        store.store("episodic", "unique fact")
        store.store("episodic", "unique fact")
        assert store.count("episodic") == 1

    def test_dedup_persists_across_reloads(self, tmp_path: Path):
        """Dedup should prevent duplicates even after store reload."""
        s1 = MemoryStore(base_dir=tmp_path / "mem")
        s1.store("semantic", "persistent fact")
        s1.store("semantic", "persistent fact")

        s2 = MemoryStore(base_dir=tmp_path / "mem")
        assert s2.count("semantic") == 1
        # Storing again should still dedup
        s2.store("semantic", "persistent fact")
        assert s2.count("semantic") == 1

    def test_dedup_returns_existing_entry(self, store: MemoryStore):
        """When dedup fires, the returned entry should be the original."""
        entry = store.store("semantic", "remember this", tags=["important"])
        dup = store.store("semantic", "remember this")
        assert dup.id == entry.id
        assert dup.tags == ["important"]
        assert dup.created_at == entry.created_at
