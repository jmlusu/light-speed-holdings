"""E2E tests for dashboard scroll behavior.

Validates that:
- The auto-scroll bug is fixed (scroll position resets on data update)
- Scroll position remains stable after WebSocket/polling data updates
- The page does not auto-scroll on chart re-render
- Scroll works correctly across page navigation

These tests use Playwright for cross-browser automation.

Prerequisites:
    pip install playwright pytest-playwright
    playwright install

Run:
    pytest tests/e2e/test_dashboard_scroll.py -v --headed
"""

from __future__ import annotations

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(60),
]


# ---------------------------------------------------------------------------
# Scroll Position Stability Tests
# ---------------------------------------------------------------------------


class TestScrollPositionStability:
    """Verify scroll position is preserved after data updates."""

    @pytest.fixture(autouse=True)
    def _setup_page(self, page, dashboard_url: str) -> None:
        """Navigate to dashboard and wait for initial load."""
        page.goto(dashboard_url, wait_until="networkidle")
        # Wait for Alpine.js to initialize
        page.wait_for_timeout(2000)

    def test_scroll_position_unchanged_after_polling_cycle(
        self, page, dashboard_url: str
    ) -> None:
        """Scroll down, wait for polling cycle (10s), verify position preserved."""
        # Scroll to the tasks table area
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(500)

        initial_scroll_y = page.evaluate("window.scrollY")
        assert initial_scroll_y > 0, "Should have scrolled down"

        # Wait for the 10-second polling cycle + some buffer
        page.wait_for_timeout(12_000)

        final_scroll_y = page.evaluate("window.scrollY")
        # Allow 2px tolerance for sub-pixel rounding
        assert abs(final_scroll_y - initial_scroll_y) <= 2, (
            f"Scroll position drifted: was {initial_scroll_y}, now {final_scroll_y}"
        )

    def test_scroll_position_unchanged_after_websocket_kpi_update(
        self, page, dashboard_url: str
    ) -> None:
        """Scroll down, inject a KPI WebSocket message, verify position preserved."""
        page.evaluate("window.scrollTo(0, 800)")
        page.wait_for_timeout(500)

        initial_scroll_y = page.evaluate("window.scrollY")

        # Simulate a KPI update message via the WebSocket handler
        page.evaluate("""
            () => {
                const app = document.querySelector('[x-data]').__x;
                if (app && app.$data) {
                    app.$data.handleWSMessage({
                        type: 'kpi_update',
                        payload: {
                            pending_tasks: 99,
                            completed_tasks: 100,
                            total_agents: 10,
                        }
                    });
                }
            }
        """)
        page.wait_for_timeout(1000)

        final_scroll_y = page.evaluate("window.scrollY")
        assert abs(final_scroll_y - initial_scroll_y) <= 2, (
            f"Scroll position changed after WS KPI update: "
            f"was {initial_scroll_y}, now {final_scroll_y}"
        )

    def test_scroll_position_preserved_after_task_list_reassignment(
        self, page, dashboard_url: str
    ) -> None:
        """Scroll to tasks table, trigger task data reassignment, verify position."""
        # Scroll to the tasks table
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(500)

        initial_scroll_y = page.evaluate("window.scrollY")

        # Trigger a full data reload (simulates what the 10s poll does)
        page.evaluate("window.scrollTo(0, window.scrollY)")  # no-op, just read
        page.evaluate("""
            () => {
                const el = document.querySelector('[x-data]');
                if (el && el._x_dataStack) {
                    const data = el._x_dataStack[0];
                    if (data && data.loadDashboard) {
                        data.loadDashboard();
                    }
                }
            }
        """)
        page.wait_for_timeout(3000)

        final_scroll_y = page.evaluate("window.scrollY")
        assert abs(final_scroll_y - initial_scroll_y) <= 5, (
            f"Scroll position changed after task reload: "
            f"was {initial_scroll_y}, now {final_scroll_y}"
        )

    def test_no_auto_scroll_on_page_load(self, page, dashboard_url: str) -> None:
        """Verify page loads at scroll position 0 without unexpected auto-scroll."""
        page.goto(dashboard_url, wait_until="networkidle")
        page.wait_for_timeout(3000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, f"Page should start at top, but scrollY={scroll_y}"


# ---------------------------------------------------------------------------
# Chart Re-render Scroll Tests
# ---------------------------------------------------------------------------


class TestChartReRenderScroll:
    """Verify chart destroy/recreate cycles don't cause scroll jumps."""

    @pytest.fixture(autouse=True)
    def _setup_page(self, page, dashboard_url: str) -> None:
        page.goto(dashboard_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

    def test_scroll_stable_during_chart_destruction(
        self, page, dashboard_url: str
    ) -> None:
        """Scroll to chart area, trigger chart destroy+recreate, check position."""
        # Scroll to charts section
        page.evaluate("window.scrollTo(0, 400)")
        page.wait_for_timeout(500)

        initial_scroll_y = page.evaluate("window.scrollY")

        # Trigger chart re-render cycle (same as what updateChartsFromKPIs does)
        page.evaluate("""
            () => {
                if (typeof updateChartsFromKPIs === 'function') {
                    updateChartsFromKPIs(
                        { pending_tasks: 5, completed_tasks: 20, total_agents: 8 },
                        [{ name: 'Engineering', total_agents: 3 }]
                    );
                }
            }
        """)
        page.wait_for_timeout(1000)

        final_scroll_y = page.evaluate("window.scrollY")
        assert abs(final_scroll_y - initial_scroll_y) <= 2, (
            f"Chart re-render caused scroll jump: "
            f"was {initial_scroll_y}, now {final_scroll_y}"
        )

    def test_scroll_stable_through_multiple_update_cycles(
        self, page, dashboard_url: str
    ) -> None:
        """Run 5 consecutive KPI updates and verify scroll stays fixed."""
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(500)

        initial_scroll_y = page.evaluate("window.scrollY")

        for i in range(5):
            page.evaluate(f"""
                () => {{
                    if (typeof updateChartsFromKPIs === 'function') {{
                        updateChartsFromKPIs(
                            {{ pending_tasks: {i}, completed_tasks: {20 + i}, total_agents: 5 }},
                            [{{ name: 'Engineering', total_agents: 3 }}]
                        );
                    }}
                }}
            """)
            page.wait_for_timeout(500)

        final_scroll_y = page.evaluate("window.scrollY")
        assert abs(final_scroll_y - initial_scroll_y) <= 5, (
            f"Scroll drifted through 5 update cycles: "
            f"was {initial_scroll_y}, now {final_scroll_y}"
        )


# ---------------------------------------------------------------------------
# Cross-page Navigation Scroll Tests
# ---------------------------------------------------------------------------


class TestNavigationScroll:
    """Verify scroll position on page navigation."""

    def test_navigation_starts_at_top(self, page, dashboard_url: str) -> None:
        """After navigating to a page, scroll should start at 0."""
        # Scroll down on dashboard
        page.goto(dashboard_url, wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 1000)")
        page.wait_for_timeout(500)
        assert page.evaluate("window.scrollY") > 0

        # Navigate to agents page
        page.click('a[href="/agents"]')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, f"New page should start at top, scrollY={scroll_y}"

    def test_back_navigation_restores_no_autoscroll(
        self, page, dashboard_url: str
    ) -> None:
        """Navigate away and back; page should not auto-scroll on return."""
        page.goto(dashboard_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Navigate to tasks and back
        page.click('a[href="/tasks"]')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        page.click('a[href="/"]')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, f"Returned page should be at top, scrollY={scroll_y}"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def dashboard_url(dashboard_server: str) -> str:
    """Return the dashboard base URL."""
    return dashboard_server
