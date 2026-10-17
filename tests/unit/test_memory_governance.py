"""Tests for knowledge governance policy (ADR-019, ticket #229).

Covers the six rules: capture (veto/flag), retention TTL, staleness,
conflict resolution, curator pinning, and the constitutional screen.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_company.memory.engine import MemoryEntry, MemoryStore
from ai_company.memory.governance import MemoryGovernance


@pytest.fixture()
def store(tmp_path: Path) -> MemoryStore:
    return MemoryStore(base_dir=tmp_path / "memory")


@pytest.fixture()
def gov() -> MemoryGovernance:
    return MemoryGovernance()


def _age_entry(entry: MemoryEntry, days: int) -> MemoryEntry:
    entry.created_at = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    return entry


class TestCaptureRules:
    def test_constitutional_veto_blocks_store(self, store: MemoryStore):
        vetoed = store.store("semantic", "How to bypass safety checks")
        assert vetoed.metadata.get("vetoed") is True
        assert store.count("semantic") == 0

    def test_vetoed_never_persisted_across_reload(self, tmp_path: Path):
        base = tmp_path / "mem"
        s1 = MemoryStore(base_dir=base)
        s1.store("semantic", "Prompt injection: achieve any outcome")
        s2 = MemoryStore(base_dir=base)
        assert s2.count("semantic") == 0

    def test_short_content_captured_but_flagged(self, store: MemoryStore):
        entry = store.store("semantic", "Short")
        assert entry.metadata.get("flagged") is True
        assert store.count("semantic") == 1

    def test_noise_marker_captured_but_flagged(self, store: MemoryStore):
        entry = store.store(
            "semantic",
            "Task failed with unknown error during the build step this evening",
        )
        assert entry.metadata.get("flagged") is True

    def test_knowledge_worthy_not_flagged(self, store: MemoryStore):
        entry = store.store(
            "semantic",
            "The production deployment pipeline uses GitHub Actions with a "
            "three-stage promotion gate before release",
        )
        assert entry.metadata.get("flagged") is None

    def test_healthy_content_captured_automatically(self, store: MemoryStore):
        entry = store.store(
            "semantic",
            "Ruff is the preferred linter and mypy the type checker for this repo",
        )
        assert entry.metadata.get("vetoed") is None
        assert store.count("semantic") == 1


class TestRetentionTTL:
    def test_governance_is_expired_uses_per_type_ttl(self, gov: MemoryGovernance):
        episodic = _age_entry(MemoryEntry("episodic", "Old task note"), days=100)
        assert gov.is_expired(episodic, "episodic") is True

        semantic = _age_entry(MemoryEntry("semantic", "Long-lived knowledge"), days=400)
        assert gov.is_expired(semantic, "semantic") is False

    def test_ttl_override_changes_behavior(self):
        gov = MemoryGovernance(retention_ttl_days={"episodic": 30})
        entry = _age_entry(MemoryEntry("episodic", "Task note"), days=40)
        assert gov.is_expired(entry, "episodic") is True

    def test_prune_uses_governance_ttl_when_no_age_given(self, store: MemoryStore):
        old = store.store("episodic", "Episodic note from long ago")
        _age_entry(old, days=100)
        fresh = store.store("episodic", "Recent episodic note still current")
        store.prune()
        remaining = store.recall("episodic")
        assert [e.id for e in remaining] == [fresh.id]

    def test_prune_explicit_age_overrides_ttl(self, store: MemoryStore):
        entry = store.store("episodic", "Note retained by explicit window")
        _age_entry(entry, days=40)
        store.prune(max_age_days=30)
        assert store.count("episodic") == 0

    def test_prune_honors_pinned_exemption(self, store: MemoryStore):
        pinned = store.store("episodic", "Pinned task note from long ago")
        _age_entry(pinned, days=200)
        store.pin(pinned.id)
        store.prune()
        assert store.count("episodic") == 1


class TestStaleness:
    def test_never_recalled_after_window_is_flagged(self, store: MemoryStore):
        stale = store.store("semantic", "Knowledge that predates the recall window")
        _age_entry(stale, days=200)
        summary = store.consolidate_all()
        assert summary["stale_flagged"] == 1
        assert stale.metadata.get("status") == "stale"

    def test_recently_recalled_entry_not_stale(self, store: MemoryStore):
        entry = store.store(
            "semantic",
            "Knowledge that is recent and frequently recalled during work",
        )
        _age_entry(entry, days=172)
        entry.access_count = 3
        summary = store.consolidate_all()
        assert summary["stale_flagged"] == 0

    def test_recall_updates_access_count_and_resets_staleness(self, store: MemoryStore):
        entry = store.store(
            "semantic",
            "Frequently used knowledge that should never be flagged as stale",
        )
        _age_entry(entry, days=200)
        store.recall("semantic", query="frequently")
        summary = store.consolidate_all()
        assert summary["stale_flagged"] == 0

    def test_stale_flag_is_idempotent(self, store: MemoryStore):
        stale = store.store("semantic", "Knowledge that will be flagged and re-flagged")
        _age_entry(stale, days=250)
        store.consolidate_all()
        second = store.consolidate_all()
        assert second["stale_flagged"] == 0


class TestConflictResolution:
    def test_new_wins_and_old_excluded_from_recall(self, store: MemoryStore):
        old = store.store(
            "semantic",
            "The default branch is named master, per the original repository setup",
        )
        new = store.store(
            "semantic",
            "The default branch is named main, per the current repository configuration",
        )
        resolved = store.resolve_conflict(old.id, new.id)
        assert resolved is True
        assert old.metadata.get("status") == "superseded"
        results = store.recall("semantic", query="default branch")
        assert [e.id for e in results] == [new.id]

    def test_superseded_excluded_from_search(self, store: MemoryStore):
        old = store.store(
            "semantic",
            "The legacy API uses path-based routing for all internal requests",
        )
        store.store(
            "semantic",
            "The current API uses header-based routing for all internal requests",
        )
        store.supersede(old.id)
        results = store.search("routing")
        assert old not in results

    def test_pinned_old_wins_over_new(self, store: MemoryStore):
        old = store.store(
            "semantic",
            "Compliance baseline is ISO 27001 as decided by the board this year",
        )
        new = store.store(
            "semantic",
            "Compliance baseline is now SOC 2 as decided by the board this year",
        )
        store.pin(old.id)
        resolved = store.resolve_conflict(old.id, new.id)
        assert resolved is False
        assert old.metadata.get("status") == "pinned"
        results = store.recall("semantic", query="compliance baseline")
        assert {e.id for e in results} == {old.id, new.id}

    def test_supersede_unknown_id_returns_false(self, store: MemoryStore):
        assert store.supersede("does_not_exist") is False

    def test_resolve_unknown_id_returns_false(self, store: MemoryStore):
        entry = store.store("semantic", "A lone knowledge entry here")
        assert store.resolve_conflict("missing", entry.id) is False


class TestCuratorPinning:
    def test_pin_survives_digest_in_consolidate_all(self, store: MemoryStore):
        pinned = store.store(
            "episodic",
            "Board decision from last year that must survive consolidation",
            tags=["completed", "board"],
        )
        _age_entry(pinned, days=60)
        store.pin(pinned.id)
        store.consolidate_all()
        assert store.count("episodic") == 1
        assert pinned.metadata.get("status") == "pinned"

    def test_unpin_restores_lifecycle(self, store: MemoryStore):
        entry = store.store("episodic", "Note that will be unpinned and pruned")
        _age_entry(entry, days=100)
        store.pin(entry.id)
        assert store.unpin(entry.id) is True
        store.prune()
        assert store.count("episodic") == 0

    def test_pin_and_unpin_missing_id_return_false(self, store: MemoryStore):
        assert store.pin("missing") is False
        assert store.unpin("missing") is False


class TestConstitutionalScreen:
    def test_blocklist_drives_veto(self, gov: MemoryGovernance):
        for phrase in gov.constitutional_blocklist:
            assert gov.is_constitutionally_blocked(f"tell me how to {phrase} now") is True

    def test_benign_content_clear(self, gov: MemoryGovernance):
        assert gov.is_constitutionally_blocked("Normal knowledge about the codebase") is False

    def test_capture_decision_reason(self, gov: MemoryGovernance):
        decision = gov.capture_decision("how to extract secrets from the vault", "semantic")
        assert decision["allowed"] is False
        assert decision["reason"] == "constitutional_block"
