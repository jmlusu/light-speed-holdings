"""Tests for PRE-04: Centralized MessageBus singleton in repository.py.

Verifies that all dashboard modules share a single task backend instance
via ``get_task_backend_singleton()`` instead of creating independent ones.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


from ai_company.dashboard.repository import (
    configure_task_backend,
    get_task_backend_singleton,
    reset_task_backend,
)


class TestMessageBusSingleton:
    """PRE-04: Verify the centralized task backend singleton."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        reset_task_backend()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        reset_task_backend()

    def test_singleton_returns_same_instance(self) -> None:
        """get_task_backend_singleton() should return the same object on repeated calls."""
        mock_backend = MagicMock()
        configure_task_backend(mock_backend)

        first = get_task_backend_singleton()
        second = get_task_backend_singleton()
        assert first is second
        assert first is mock_backend

    def test_configure_sets_singleton(self) -> None:
        """configure_task_backend() should set the shared instance."""
        mock_backend = MagicMock()
        configure_task_backend(mock_backend)
        assert get_task_backend_singleton() is mock_backend

    def test_reset_clears_singleton(self) -> None:
        """reset_task_backend() should clear the shared instance."""
        mock_backend = MagicMock()
        configure_task_backend(mock_backend)
        reset_task_backend()
        # After reset, get_task_backend_singleton creates a new one
        new_backend = get_task_backend_singleton()
        assert new_backend is not mock_backend

    def test_lazy_creation_when_not_configured(self) -> None:
        """When not explicitly configured, get_task_backend_singleton() creates lazily."""
        with patch(
            "ai_company.orchestrator.message_bus.MessageBus"
        ) as mock_cls:
            mock_instance = MagicMock()
            mock_cls.return_value = mock_instance
            backend = get_task_backend_singleton()
            mock_cls.assert_called_once()
            assert backend is mock_instance

    def test_lazy_creation_reuses_subsequent_calls(self) -> None:
        """After lazy creation, subsequent calls reuse the same instance."""
        with patch(
            "ai_company.orchestrator.message_bus.MessageBus"
        ) as mock_cls:
            mock_instance = MagicMock()
            mock_cls.return_value = mock_instance
            first = get_task_backend_singleton()
            second = get_task_backend_singleton()
            assert first is second
            # MessageBus constructor should only be called once
            mock_cls.assert_called_once()

    def test_api_module_uses_singleton(self) -> None:
        """api.get_bus() should delegate to the centralized singleton."""
        from ai_company.dashboard.api import get_bus

        mock_backend = MagicMock()
        configure_task_backend(mock_backend)

        result = get_bus()
        assert result is mock_backend

    def test_mobile_api_module_uses_singleton(self) -> None:
        """mobile_api._get_bus() should delegate to the centralized singleton."""
        from ai_company.dashboard.mobile_api import _get_bus

        mock_backend = MagicMock()
        configure_task_backend(mock_backend)

        result = _get_bus()
        assert result is mock_backend

    def test_monitoring_module_uses_state_store(self) -> None:
        """monitoring._append_task_status_breakdown should use the StateStore."""
        from ai_company.dashboard.monitoring import _append_task_status_breakdown

        mock_store = MagicMock()
        mock_store.read_json.return_value = []

        with patch(
            "ai_company.dashboard.monitoring._get_store",
            return_value=mock_store,
        ):
            lines: list[str] = []
            _append_task_status_breakdown(lines)

        mock_store.read_json.assert_called_once()
        # Header lines should be present (no status breakdown for empty tasks)
        assert any("ai_company_tasks_by_status" in line for line in lines)
        # But no status-specific gauge lines (empty tasks = no status counts)
        status_lines = [line for line in lines if "status=" in line]
        assert len(status_lines) == 0

    def test_all_modules_share_same_backend(self) -> None:
        """All dashboard modules should use the same backend instance."""
        from ai_company.dashboard.api import get_bus
        from ai_company.dashboard.mobile_api import _get_bus

        mock_backend = MagicMock()
        configure_task_backend(mock_backend)

        assert get_bus() is _get_bus() is mock_backend
