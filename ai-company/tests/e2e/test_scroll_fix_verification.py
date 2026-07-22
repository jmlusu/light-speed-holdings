"""E2E test to verify the auto-scroll bug fix.

This test specifically validates that the auto-scroll regression is resolved.
It should be run as a smoke test after any dashboard JS/CSS changes.

Prerequisites:
    pip install playwright pytest-playwright httpx
    playwright install

Run:
    pytest tests/e2e/test_scroll_fix_verification.py -v --headed
"""

from __future__ import annotations

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(120),
]


class TestAutoScrollBugFix:
    """Directly verify the auto-scroll bug is fixed."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server

    def test_no_scroll_jump_on_initial_load(self, page) -> None:
        """BUG: Page auto-scrolled on initial data load.
        FIX: Page should remain at scrollY=0 after full load.
        """
        page.goto(self.url, wait_until="networkidle")
        # Wait for Alpine.js init + first polling cycle
        page.wait_for_timeout(4000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, (
            f"AUTO-SCROLL BUG: Page scrolled to {scroll_y}px on initial load"
        )

    def test_no_scroll_jump_after_polling_cycle(self, page) -> None:
        """BUG: Page auto-scrolled every 10s when polling kicked in.
        FIX: Scroll position must remain stable through a polling cycle.
        """
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Position user partway down the page
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(500)
        initial = page.evaluate("window.scrollY")
        assert initial > 0, "Precondition: user should have scrolled down"

        # Wait for two polling cycles
        page.wait_for_timeout(22_000)

        final = page.evaluate("window.scrollY")
        assert abs(final - initial) <= 5, (
            f"AUTO-SCROLL BUG: Position drifted from {initial}px to {final}px "
            f"after polling cycles"
        )

    def test_no_scroll_jump_on_kpi_websocket_update(self, page) -> None:
        """BUG: WebSocket KPI updates caused page to scroll.
        FIX: WS updates update data without affecting scroll.
        """
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        page.evaluate("window.scrollTo(0, 700)")
        page.wait_for_timeout(500)
        initial = page.evaluate("window.scrollY")

        # Inject multiple WS messages rapidly
        for i in range(10):
            page.evaluate(f"""
                () => {{
                    const el = document.querySelector('[x-data]');
                    if (el && el._x_dataStack) {{
                        const data = el._x_dataStack[0];
                        if (data && data.handleWSMessage) {{
                            data.handleWSMessage({{
                                type: 'kpi_update',
                                payload: {{
                                    pending_tasks: {i},
                                    completed_tasks: {100 - i},
                                    total_agents: 5,
                                }}
                            }});
                        }}
                    }}
                }}
            """)
            page.wait_for_timeout(200)

        page.wait_for_timeout(1000)
        final = page.evaluate("window.scrollY")
        assert abs(final - initial) <= 5, (
            f"AUTO-SCROLL BUG: WS updates caused scroll from "
            f"{initial}px to {final}px"
        )

    def test_no_scroll_jump_on_chart_resize(self, page) -> None:
        """BUG: Chart.js resize/recreate caused layout shift + scroll.
        FIX: Chart operations should not affect scroll position.
        """
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(3000)

        page.evaluate("window.scrollTo(0, 400)")
        page.wait_for_timeout(500)
        initial = page.evaluate("window.scrollY")

        # Trigger chart resize (which destroys and recreates)
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        page.wait_for_timeout(2000)

        final = page.evaluate("window.scrollY")
        assert abs(final - initial) <= 5, (
            f"AUTO-SCROLL BUG: Chart resize caused scroll from "
            f"{initial}px to {final}px"
        )

    def test_smooth_scroll_behavior_not_causes_jump(self, page) -> None:
        """BUG: CSS scroll-behavior:smooth combined with DOM mutations
        caused unpredictable scrolling.
        FIX: scroll-behavior should not cause auto-jump on data updates.
        """
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Verify scroll-behavior: smooth is applied
        behavior = page.evaluate("""
            getComputedStyle(document.documentElement).scrollBehavior
        """)
        assert behavior == "smooth", (
            f"Expected scroll-behavior:smooth, got: {behavior}"
        )

        # Scroll down
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(1000)
        initial = page.evaluate("window.scrollY")

        # Trigger multiple data updates
        for _ in range(5):
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
            page.wait_for_timeout(1500)

        final = page.evaluate("window.scrollY")
        assert abs(final - initial) <= 10, (
            f"AUTO-SCROLL BUG: smooth scroll + data updates caused drift "
            f"from {initial}px to {final}px"
        )

    def test_scroll_stable_during_drag_and_drop(self, page) -> None:
        """Verify scroll doesn't jump during task drag operations."""
        page.goto(f"{self.url}/tasks", wait_until="networkidle")
        page.wait_for_timeout(3000)

        page.evaluate("window.scrollTo(0, 300)")
        page.wait_for_timeout(500)
        initial = page.evaluate("window.scrollY")

        # Simulate drag events (triggers classList changes)
        page.evaluate("""
            () => {
                document.querySelectorAll('tr').forEach(tr => {
                    tr.classList.add('dragging');
                    tr.classList.remove('dragging');
                });
            }
        """)
        page.wait_for_timeout(500)

        final = page.evaluate("window.scrollY")
        assert abs(final - initial) <= 2, (
            f"Drag operation caused scroll from {initial}px to {final}px"
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def dashboard_url(dashboard_server: str) -> str:
    return dashboard_server
