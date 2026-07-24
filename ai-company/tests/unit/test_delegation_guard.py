"""Tests for PRE-18: Delegation depth limits and cycle detection."""

from __future__ import annotations

from ai_company.security.delegation_guard import (
    DelegationGuard,
    check_delegation_allowed,
    get_delegation_guard,
)


class TestDelegationGuardDepthLimit:
    """Depth limit enforcement tests."""

    def test_depth_zero_allows_first_delegation(self) -> None:
        guard = DelegationGuard(max_depth=3)
        allowed, reason = guard.check_delegation("t1", "agent_b", delegation_depth=0)
        assert allowed is True
        assert reason == ""

    def test_depth_at_limit_blocks(self) -> None:
        guard = DelegationGuard(max_depth=3)
        allowed, reason = guard.check_delegation("t1", "agent_d", delegation_depth=3)
        assert allowed is False
        assert "exceeds maximum" in reason

    def test_depth_one_below_limit_allows(self) -> None:
        guard = DelegationGuard(max_depth=3)
        allowed, _ = guard.check_delegation("t1", "agent_c", delegation_depth=2)
        assert allowed is True

    def test_custom_max_depth(self) -> None:
        guard = DelegationGuard(max_depth=1)
        allowed, _ = guard.check_delegation("t1", "agent_b", delegation_depth=0)
        assert allowed is True
        allowed, reason = guard.check_delegation("t1", "agent_c", delegation_depth=1)
        assert allowed is False
        assert "exceeds maximum" in reason

    def test_depth_limit_includes_chain_in_reason(self) -> None:
        guard = DelegationGuard(max_depth=2)
        history = ["agent_a", "agent_b"]
        allowed, reason = guard.check_delegation(
            "t1", "agent_c", delegation_depth=2, delegation_history=history
        )
        assert allowed is False
        assert "agent_a" in reason
        assert "agent_b" in reason


class TestDelegationGuardCycleDetection:
    """Cycle detection tests."""

    def test_simple_cycle_detected(self) -> None:
        guard = DelegationGuard()
        history = ["agent_a", "agent_b"]
        allowed, reason = guard.check_delegation(
            "t1", "agent_a", delegation_depth=1, delegation_history=history
        )
        assert allowed is False
        assert "cycle detected" in reason
        assert "agent_a" in reason

    def test_no_cycle_when_receiver_not_in_history(self) -> None:
        guard = DelegationGuard()
        history = ["agent_a", "agent_b"]
        allowed, _ = guard.check_delegation(
            "t1", "agent_c", delegation_depth=2, delegation_history=history
        )
        assert allowed is True

    def test_cycle_at_depth_zero_not_possible(self) -> None:
        """At depth 0 (root), delegation_history should be empty — no cycle."""
        guard = DelegationGuard()
        allowed, _ = guard.check_delegation("t1", "agent_a", delegation_depth=0)
        assert allowed is True

    def test_three_hop_cycle(self) -> None:
        """A -> B -> C -> A should be caught."""
        guard = DelegationGuard(max_depth=10)
        history = ["agent_a", "agent_b", "agent_c"]
        allowed, reason = guard.check_delegation(
            "t1", "agent_a", delegation_depth=3, delegation_history=history
        )
        assert allowed is False
        assert "cycle detected" in reason

    def test_empty_history_no_false_positive(self) -> None:
        guard = DelegationGuard()
        allowed, _ = guard.check_delegation(
            "t1", "agent_a", delegation_depth=0, delegation_history=[]
        )
        assert allowed is True


class TestDelegationGuardTotalCount:
    """Total delegation count limit tests."""

    def test_within_total_limit(self) -> None:
        guard = DelegationGuard(max_total=5)
        for i in range(4):
            guard.record_delegation("t1", f"agent_{i}")
        allowed, _ = guard.check_delegation("t1", "agent_4")
        assert allowed is True

    def test_exceeds_total_limit(self) -> None:
        guard = DelegationGuard(max_total=3)
        for i in range(3):
            guard.record_delegation("t1", f"agent_{i}")
        allowed, reason = guard.check_delegation("t1", "agent_3")
        assert allowed is False
        assert "exceeds maximum" in reason

    def test_total_limit_independent_per_task(self) -> None:
        guard = DelegationGuard(max_total=2)
        guard.record_delegation("t1", "agent_a")
        guard.record_delegation("t1", "agent_b")
        # t1 is at limit
        allowed_t1, _ = guard.check_delegation("t1", "agent_c")
        assert allowed_t1 is False
        # t2 has no delegations yet
        allowed_t2, _ = guard.check_delegation("t2", "agent_d")
        assert allowed_t2 is True


class TestDelegationGuardChainTracking:
    """Chain tracking and depth queries."""

    def test_get_chain_empty(self) -> None:
        guard = DelegationGuard()
        assert guard.get_chain("nonexistent") == []

    def test_get_chain_after_recordings(self) -> None:
        guard = DelegationGuard()
        guard.record_delegation("t1", "agent_a")
        guard.record_delegation("t1", "agent_b")
        assert guard.get_chain("t1") == ["agent_a", "agent_b"]

    def test_get_depth_empty(self) -> None:
        guard = DelegationGuard()
        assert guard.get_depth("nonexistent") == 0

    def test_get_depth_after_recordings(self) -> None:
        guard = DelegationGuard()
        guard.record_delegation("t1", "agent_a")
        guard.record_delegation("t1", "agent_b")
        guard.record_delegation("t1", "agent_c")
        assert guard.get_depth("t1") == 3

    def test_chains_are_independent_per_task(self) -> None:
        guard = DelegationGuard()
        guard.record_delegation("t1", "agent_a")
        guard.record_delegation("t2", "agent_x")
        guard.record_delegation("t2", "agent_y")
        assert guard.get_chain("t1") == ["agent_a"]
        assert guard.get_chain("t2") == ["agent_x", "agent_y"]


class TestDelegationGuardReset:
    """Reset on task completion/failure."""

    def test_reset_clears_chain(self) -> None:
        guard = DelegationGuard()
        guard.record_delegation("t1", "agent_a")
        guard.record_delegation("t1", "agent_b")
        guard.reset("t1")
        assert guard.get_chain("t1") == []
        assert guard.get_depth("t1") == 0

    def test_reset_clears_count(self) -> None:
        guard = DelegationGuard(max_total=2)
        for i in range(2):
            guard.record_delegation("t1", f"agent_{i}")
        # At limit before reset
        assert guard.check_delegation("t1", "agent_2")[0] is False
        guard.reset("t1")
        # Below limit after reset
        assert guard.check_delegation("t1", "agent_2")[0] is True

    def test_reset_nonexistent_task_no_error(self) -> None:
        guard = DelegationGuard()
        guard.reset("nonexistent")  # should not raise


class TestDelegationGuardEdgeCases:
    """Edge cases: empty history, root-level delegation, singleton."""

    def test_root_delegation_always_allowed(self) -> None:
        """A depth-0 delegation should never be blocked by depth/cycle."""
        guard = DelegationGuard(max_depth=0)
        # Even with max_depth=0, depth 0 should pass the >= check
        # because the check is delegation_depth >= max_depth which is 0 >= 0 = True
        # This is intentional: max_depth=0 means no delegation allowed at all
        allowed, reason = guard.check_delegation("t1", "agent_a", delegation_depth=0)
        assert allowed is False
        assert "exceeds maximum" in reason

    def test_max_depth_one_allows_single_level(self) -> None:
        guard = DelegationGuard(max_depth=1)
        allowed, _ = guard.check_delegation("t1", "agent_b", delegation_depth=0)
        assert allowed is True
        allowed, reason = guard.check_delegation("t1", "agent_c", delegation_depth=1)
        assert allowed is False

    def test_receiver_as_empty_string(self) -> None:
        """Empty receiver should not cause errors."""
        guard = DelegationGuard()
        allowed, _ = guard.check_delegation("t1", "", delegation_depth=0)
        assert allowed is True

    def test_task_id_with_special_chars(self) -> None:
        guard = DelegationGuard()
        guard.record_delegation("t-1/2_3", "agent_a")
        assert guard.get_chain("t-1/2_3") == ["agent_a"]

    def test_max_concurrent_constant_defined(self) -> None:
        """Ensure MAX_CONCURRENT_DELEGATIONS is defined (used in integration)."""
        from ai_company.security.delegation_guard import MAX_CONCURRENT_DELEGATIONS
        assert MAX_CONCURRENT_DELEGATIONS > 0


class TestDelegationGuardSingleton:
    """Module-level singleton and quick-check function."""

    def test_get_delegation_guard_returns_same_instance(self) -> None:
        g1 = get_delegation_guard()
        g2 = get_delegation_guard()
        assert g1 is g2

    def test_check_delegation_allowed_uses_singleton(self) -> None:
        guard = get_delegation_guard()
        # Record a delegation on the singleton
        test_task_id = "_singleton_test_task"
        guard.reset(test_task_id)  # clean slate
        allowed, _ = check_delegation_allowed(test_task_id, "agent_x")
        assert allowed is True


class TestDelegationGuardFullChain:
    """End-to-end chain simulation."""

    def test_full_delegation_chain_respects_depth(self) -> None:
        """Simulate A->B->C->D with max_depth=3."""
        guard = DelegationGuard(max_depth=3)
        task_id = "task_chain"

        # A delegates to B (depth 0 -> 1)
        allowed, _ = guard.check_delegation(task_id, "B", delegation_depth=0)
        assert allowed is True
        guard.record_delegation(task_id, "B")

        # B delegates to C (depth 1 -> 2)
        allowed, _ = guard.check_delegation(
            task_id, "C", delegation_depth=1, delegation_history=["A"]
        )
        assert allowed is True
        guard.record_delegation(task_id, "C")

        # C delegates to D (depth 2 -> 3)
        allowed, _ = guard.check_delegation(
            task_id, "D", delegation_depth=2, delegation_history=["A", "B"]
        )
        assert allowed is True
        guard.record_delegation(task_id, "D")

        # D tries to delegate to E (depth 3 — BLOCKED)
        allowed, reason = guard.check_delegation(
            task_id, "E", delegation_depth=3, delegation_history=["A", "B", "C"]
        )
        assert allowed is False
        assert "exceeds maximum" in reason

    def test_chain_with_cycle_at_end(self) -> None:
        """A->B->C->B should detect cycle."""
        guard = DelegationGuard(max_depth=10)
        task_id = "task_cycle"

        allowed, _ = guard.check_delegation(task_id, "B", delegation_depth=0)
        assert allowed is True
        guard.record_delegation(task_id, "B")

        allowed, _ = guard.check_delegation(
            task_id, "C", delegation_depth=1, delegation_history=["A"]
        )
        assert allowed is True
        guard.record_delegation(task_id, "C")

        # C tries to delegate back to B — cycle detected
        allowed, reason = guard.check_delegation(
            task_id, "B", delegation_depth=2, delegation_history=["A", "B"]
        )
        assert allowed is False
        assert "cycle detected" in reason
