"""Tests for memory access controls (PRE-17)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ai_company.security.memory_access_control import (
    DEFAULT_ACCESS_MATRIX,
    MemoryAccessControl,
    check_memory_access,
    filter_memories_by_access,
    get_memory_access_control,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_memory(content: str, tags: list[str] | None = None) -> dict:
    """Build a minimal memory dict as returned by recall_context."""
    return {"content": content, "tags": tags or [], "agent_id": "anyone", "type": "semantic"}


# ---------------------------------------------------------------------------
# can_access — core permission logic
# ---------------------------------------------------------------------------

class TestCanAccess:
    """Direct permission checks on MemoryAccessControl.can_access."""

    def test_allowed_agent_can_access_restricted_tag(self) -> None:
        mac = MemoryAccessControl()
        assert mac.can_access("cfo", ["financial"]) is True

    def test_disallowed_agent_cannot_access_restricted_tag(self) -> None:
        mac = MemoryAccessControl()
        assert mac.can_access("devops", ["financial"]) is False

    def test_unrestricted_tag_always_allowed(self) -> None:
        """Tags absent from the matrix should be accessible by anyone."""
        mac = MemoryAccessControl()
        assert mac.can_access("devops", ["meeting_notes"]) is True

    def test_multiple_restricted_tags_all_must_pass(self) -> None:
        """Agent must be allowed for every restricted tag in the list."""
        mac = MemoryAccessControl()
        # cfo is in both financial and budget lists
        assert mac.can_access("cfo", ["financial", "budget"]) is True
        # devops is in neither
        assert mac.can_access("devops", ["financial", "budget"]) is False

    def test_mixed_restricted_and_unrestricted_tags(self) -> None:
        """An unrestricted tag alongside a restricted one doesn't bypass the check."""
        mac = MemoryAccessControl()
        # meeting_notes is unrestricted, but financial blocks devops
        assert mac.can_access("devops", ["meeting_notes", "financial"]) is False

    def test_empty_tags_always_allowed(self) -> None:
        mac = MemoryAccessControl()
        assert mac.can_access("any_agent", []) is True

    def test_unknown_agent_denied_for_restricted_tag(self) -> None:
        mac = MemoryAccessControl()
        assert mac.can_access("nonexistent_agent_999", ["security"]) is False

    def test_ceo_has_broad_access(self) -> None:
        """human_ceo should appear in most restricted categories."""
        mac = MemoryAccessControl()
        assert mac.can_access("human_ceo", ["financial"]) is True
        assert mac.can_access("human_ceo", ["hr"]) is True
        assert mac.can_access("human_ceo", ["security"]) is True
        assert mac.can_access("human_ceo", ["strategy"]) is True

    def test_custom_matrix(self) -> None:
        matrix = {"secret": ["alpha", "beta"]}
        mac = MemoryAccessControl(access_matrix=matrix)
        assert mac.can_access("alpha", ["secret"]) is True
        assert mac.can_access("gamma", ["secret"]) is False
        # "other" is unrestricted in this custom matrix
        assert mac.can_access("gamma", ["other"]) is True


# ---------------------------------------------------------------------------
# filter_memories
# ---------------------------------------------------------------------------

class TestFilterMemories:
    """Filtering lists of memory dicts by access permissions."""

    def test_filters_out_restricted_memories(self) -> None:
        mac = MemoryAccessControl()
        memories = [
            _make_memory("Team standup", tags=["meeting"]),
            _make_memory("Q4 revenue", tags=["financial"]),
            _make_memory("Deploy runbook", tags=["ops"]),
        ]
        result = mac.filter_memories("devops", memories)
        assert len(result) == 2
        assert all(m["tags"] != ["financial"] for m in result)

    def test_keeps_all_when_agent_has_access(self) -> None:
        mac = MemoryAccessControl()
        memories = [
            _make_memory("Q4 revenue", tags=["financial"]),
            _make_memory("Budget forecast", tags=["budget"]),
        ]
        result = mac.filter_memories("cfo", memories)
        assert len(result) == 2

    def test_empty_list_returns_empty(self) -> None:
        mac = MemoryAccessControl()
        assert mac.filter_memories("cfo", []) == []

    def test_no_tags_memory_always_passes(self) -> None:
        mac = MemoryAccessControl()
        memories = [_make_memory("General note", tags=[])]
        result = mac.filter_memories("devops", memories)
        assert len(result) == 1

    def test_mixed_tags_per_entry(self) -> None:
        mac = MemoryAccessControl()
        memories = [
            _make_memory("A", tags=["financial", "meeting"]),  # restricted
            _make_memory("B", tags=["meeting"]),               # unrestricted
            _make_memory("C", tags=["hr"]),                     # restricted
        ]
        result = mac.filter_memories("devops", memories)
        assert len(result) == 1
        assert result[0]["content"] == "B"

    def test_preserves_memory_dict_structure(self) -> None:
        mac = MemoryAccessControl()
        original = _make_memory("test content", tags=["financial"])
        result = mac.filter_memories("cfo", [original])
        assert result[0] is original  # same dict object, no copy overhead


# ---------------------------------------------------------------------------
# get_allowed_tags / get_restricted_tags
# ---------------------------------------------------------------------------

class TestTagListing:
    def test_get_allowed_tags_for_agent(self) -> None:
        mac = MemoryAccessControl()
        tags = mac.get_allowed_tags("cfo")
        assert "financial" in tags
        assert "budget" in tags
        assert "expense" in tags
        assert "strategy" in tags

    def test_get_allowed_tags_returns_sorted(self) -> None:
        mac = MemoryAccessControl()
        tags = mac.get_allowed_tags("cfo")
        assert tags == sorted(tags)

    def test_get_allowed_tags_empty_for_unknown_agent(self) -> None:
        mac = MemoryAccessControl()
        assert mac.get_allowed_tags("nonexistent_agent_999") == []

    def test_get_restricted_tags(self) -> None:
        mac = MemoryAccessControl()
        restricted = mac.get_restricted_tags()
        assert "financial" in restricted
        assert "hr" in restricted
        assert "security" in restricted
        assert len(restricted) == len(DEFAULT_ACCESS_MATRIX)

    def test_restricted_tags_after_removal(self) -> None:
        mac = MemoryAccessControl()
        mac.remove_access("financial")
        restricted = mac.get_restricted_tags()
        assert "financial" not in restricted


# ---------------------------------------------------------------------------
# set_access / remove_access — matrix mutation
# ---------------------------------------------------------------------------

class TestMatrixMutation:
    def test_set_access_adds_new_tag(self) -> None:
        mac = MemoryAccessControl()
        mac.set_access("top_secret", ["alpha"])
        assert mac.can_access("alpha", ["top_secret"]) is True
        assert mac.can_access("beta", ["top_secret"]) is False

    def test_set_access_overwrites_existing_tag(self) -> None:
        mac = MemoryAccessControl()
        mac.set_access("financial", ["new_agent"])
        assert mac.can_access("new_agent", ["financial"]) is True
        assert mac.can_access("cfo", ["financial"]) is False

    def test_remove_access_makes_tag_unrestricted(self) -> None:
        mac = MemoryAccessControl()
        mac.remove_access("financial")
        assert mac.can_access("anyone", ["financial"]) is True

    def test_remove_nonexistent_tag_is_noop(self) -> None:
        mac = MemoryAccessControl()
        mac.remove_access("does_not_exist")  # should not raise

    def test_access_matrix_property(self) -> None:
        mac = MemoryAccessControl()
        matrix = mac.access_matrix
        assert "financial" in matrix
        assert "security" in matrix


# ---------------------------------------------------------------------------
# Singleton helpers
# ---------------------------------------------------------------------------

class TestSingletonHelpers:
    def test_get_memory_access_control_returns_singleton(self) -> None:
        mac1 = get_memory_access_control()
        mac2 = get_memory_access_control()
        assert mac1 is mac2

    def test_check_memory_access_quick_function(self) -> None:
        assert check_memory_access("cfo", ["financial"]) is True
        assert check_memory_access("devops", ["financial"]) is False

    def test_filter_memories_by_access_quick_function(self) -> None:
        memories = [_make_memory("Q4 numbers", tags=["financial"])]
        result = filter_memories_by_access("devops", memories)
        assert len(result) == 0
        result = filter_memories_by_access("cfo", memories)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# Integration: recall_context with agent_id filtering
# ---------------------------------------------------------------------------

class TestRecallContextAccessControl:
    """Verify that recall_context applies access filtering when agent_id is given."""

    def _build_fake_store(self, entries: list[tuple[str, list[str]]]) -> MagicMock:
        """Create a mock MemoryStore with a fake recall that returns entries."""
        store = MagicMock()

        class _FakeEntry:
            def __init__(self, content: str, tags: list[str]) -> None:
                self.memory_type = "semantic"
                self.content = content
                self.agent_id = "anyone"
                self.tags = tags

        def _fake_recall(mem_type: str, query: str = "", limit: int = 5, **kw: object) -> list:
            return [_FakeEntry(c, t) for c, t in entries]

        store.recall.side_effect = _fake_recall
        return store

    def test_recall_context_no_agent_id_no_filtering(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Without agent_id, no filtering is applied (backward compat)."""
        from ai_company.memory import integration as mem_int

        store = self._build_fake_store([
            ("financial data", ["financial"]),
            ("ops runbook", ["ops"]),
        ])
        monkeypatch.setattr(mem_int, "_store", store)
        monkeypatch.setattr(mem_int, "_vector_store", None)

        # recall_context with no agent_id should return unfiltered results
        results = mem_int.recall_context("financial", limit=20)
        # recall_context iterates 3 memory types, mock returns 2 each → 6 total.
        # All should be present (no filtering), truncated to limit.
        assert len(results) == 6
        assert any(r["tags"] == ["financial"] for r in results)
        assert any(r["tags"] == ["ops"] for r in results)

    def test_recall_context_with_agent_id_filters(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With agent_id, restricted memories are filtered out."""
        from ai_company.memory import integration as mem_int

        store = self._build_fake_store([
            ("financial data", ["financial"]),
            ("ops runbook", ["ops"]),
        ])
        monkeypatch.setattr(mem_int, "_store", store)
        monkeypatch.setattr(mem_int, "_vector_store", None)

        # devops should NOT see financial memories
        results = mem_int.recall_context("financial", agent_id="devops", limit=20)
        assert all(r["tags"] != ["financial"] for r in results)
        assert len(results) == 3  # 3 types × 1 ops entry each

        # CFO SHOULD see financial memories
        results = mem_int.recall_context("financial", agent_id="cfo", limit=20)
        assert any(r["tags"] == ["financial"] for r in results)
