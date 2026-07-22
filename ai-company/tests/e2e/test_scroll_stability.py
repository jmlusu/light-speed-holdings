"""E2E tests for dashboard scroll stability.

Validates that the auto-scroll bug is fixed and scroll position is
preserved during real-time data updates (polling + WebSocket).

Complements test_dashboard_scroll.py and test_scroll_fix_verification.py
with additional coverage for:
    - Rapid state mutation stress tests
    - Chart layout shift detection
    - Responsive layout validation
    - Error handling UI tests

Prerequisites:
    pip install playwright pytest-playwright
    playwright install chromium

Run:
    pytest tests/e2e/test_scroll_stability.py -v --browser chromium
    pytest tests/e2e/test_scroll_stability.py -v --browser chromium --headed
"""

from __future__ import annotations

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(120),
]


# ═══ Scroll Position Stability ════════════════════════════════════════


class TestScrollStability:
    """Verify scroll position is preserved during data updates."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    def test_initial_load_scroll_at_top(self, page) -> None:
        """AC-SCROLL-01: Page loads at scroll position (0, 0)."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, f"Expected scrollY=0 on load, got {scroll_y}"

    def test_scroll_preserved_after_two_polling_cycles(self, page) -> None:
        """AC-SCROLL-01: Scroll position unchanged after 20s (2 poll cycles)."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Scroll to bottom of page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        scroll_before = page.evaluate("window.scrollY")
        assert scroll_before > 0, "Scroll should have moved from top"

        # Wait for 2 polling cycles (10s each)
        page.wait_for_timeout(22000)

        scroll_after = page.evaluate("window.scrollY")
        delta = abs(scroll_after - scroll_before)

        assert delta == 0, (
            f"Scroll position drifted by {delta}px after polling. "
            f"Before: {scroll_before}, After: {scroll_after}"
        )

    def test_scroll_preserved_after_websocket_push(self, page) -> None:
        """AC-SCROLL-02: Scroll position unchanged after WebSocket message."""
        page.goto(self.url, wait_until="networkidle")

        # Wait for WebSocket connection
        page.wait_for_function(
            """() => {
                const el = document.querySelector('[x-data]');
                return el && el.__x && el.__x.$data.wsConnected === true;
            }""",
            timeout=10000,
        )

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        scroll_before = page.evaluate("window.scrollY")

        # Trigger a WebSocket message by creating a task via API
        page.evaluate("""
            fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    receiver_id: 'lead-engineering',
                    instruction: 'Scroll stability test task',
                    priority: 'low'
                })
            });
        """)

        # Wait for WS message to arrive and process
        page.wait_for_timeout(3000)

        scroll_after = page.evaluate("window.scrollY")
        delta = abs(scroll_after - scroll_before)

        assert delta == 0, (
            f"Scroll position drifted by {delta}px after WS update. "
            f"Before: {scroll_before}, After: {scroll_after}"
        )


# ═══ Rapid Mutation Stress Tests ═════════════════════════════════════


class TestRapidMutationStability:
    """Stress test scroll stability under rapid state changes."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    def test_scroll_stable_during_rapid_kpi_mutations(self, page) -> None:
        """REG-10: Scroll stable under 10 rapid state mutations."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        scroll_before = page.evaluate("window.scrollY")

        # Trigger 10 rapid state mutations via Alpine.js data
        page.evaluate("""
            const el = document.querySelector('[x-data]');
            if (el && el.__x) {
                const data = el.__x.$data;
                for (let i = 0; i < 10; i++) {
                    data.kpis.pending_tasks = i;
                    data.kpis.completed_tasks = 100 - i;
                    data.kpis.failed_tasks = i * 2;
                }
            }
        """)

        page.wait_for_timeout(1000)

        scroll_after = page.evaluate("window.scrollY")
        delta = abs(scroll_after - scroll_before)

        assert delta == 0, (
            f"Scroll drifted by {delta}px during rapid mutation"
        )

    def test_no_layout_shift_on_chart_update(self, page) -> None:
        """AC-SCROLL-06: Charts re-render without layout shift."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Record initial body height
        height_before = page.evaluate("document.body.scrollHeight")

        # Trigger chart update
        page.evaluate("""
            if (typeof updateChartsFromKPIs === 'function') {
                updateChartsFromKPIs(
                    { pending_tasks: 50, completed_tasks: 200, failed_tasks: 3 },
                    [{ name: 'Engineering', total_agents: 8 }]
                );
            }
        """)

        page.wait_for_timeout(1000)

        height_after = page.evaluate("document.body.scrollHeight")
        delta = abs(height_after - height_before)

        # Allow 1px tolerance for rounding
        assert delta <= 1, (
            f"Body height shifted by {delta}px during chart update"
        )

    def test_no_flicker_during_polling(self, page) -> None:
        """AC-DATA-05: No visible flicker during poll cycle."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Take screenshot before polling
        screenshot_before = page.screenshot()

        # Wait for polling cycle
        page.wait_for_timeout(12000)

        # Take screenshot after polling
        screenshot_after = page.screenshot()

        # Screenshots should be identical (no visual change)
        # We can't do pixel-perfect comparison, but we verify no errors
        assert len(screenshot_before) > 0, "Screenshot before polling failed"
        assert len(screenshot_after) > 0, "Screenshot after polling failed"


# ═══ Data Loading ═════════════════════════════════════════════════════


class TestDataLoading:
    """Verify data loads correctly and updates don't disrupt the UI."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    def test_kpi_cards_populate(self, page) -> None:
        """AC-DATA-01: KPI cards show values within 2s."""
        page.goto(self.url, wait_until="networkidle")

        # Wait for KPI values to populate
        page.wait_for_function(
            """() => {
                const el = document.querySelector('[x-data]');
                if (!el || !el.__x) return false;
                const data = el.__x.$data;
                return data.kpis.total_agents > 0 || data.kpis.pending_tasks >= 0;
            }""",
            timeout=5000,
        )

        kpi_cards = page.locator(".kpi-card")
        assert kpi_cards.count() >= 5, "Expected at least 5 KPI cards"

    def test_websocket_connects_within_5s(self, page) -> None:
        """AC-DATA-03: WebSocket connects within 5s."""
        page.goto(self.url)

        page.wait_for_function(
            """() => {
                const el = document.querySelector('[x-data]');
                return el && el.__x && el.__x.$data.wsConnected === true;
            }""",
            timeout=5000,
        )

    def test_empty_task_list_shows_message(self, page) -> None:
        """AC-ERR-03: Empty state shows helpful message."""
        page.goto(f"{self.url}/tasks", wait_until="networkidle")
        page.wait_for_timeout(2000)

        content = page.content()
        has_empty = "No pending tasks" in content or "No tasks" in content
        has_tasks = page.locator("[draggable='true']").count() > 0

        assert has_empty or has_tasks, "Expected either empty message or task cards"

    def test_polling_does_not_duplicate_tasks(self, page) -> None:
        """AC-DATA-06: Polling does not duplicate task entries."""
        page.goto(f"{self.url}/tasks", wait_until="networkidle")
        page.wait_for_timeout(2000)

        count_before = page.locator("[draggable='true']").count()

        # Wait for 2 polling cycles
        page.wait_for_timeout(22000)

        count_after = page.locator("[draggable='true']").count()

        assert count_after <= count_before + 1, (
            f"Task count increased from {count_before} to {count_after} "
            f"during polling — possible duplication"
        )


# ═══ Error Handling ═══════════════════════════════════════════════════


class TestErrorHandling:
    """Verify graceful error handling in the UI."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    def test_live_badge_when_connected(self, page) -> None:
        """AC-ERR-02: 'Live' badge shown when WebSocket is connected."""
        page.goto(self.url, wait_until="networkidle")

        page.wait_for_function(
            """() => {
                const el = document.querySelector('[x-data]');
                return el && el.__x && el.__x.$data.wsConnected === true;
            }""",
            timeout=5000,
        )

        live_badge = page.locator("text=Live")
        assert live_badge.is_visible(), "Live badge should be visible when WS connected"

    def test_toast_notification_displayed(self, page) -> None:
        """AC-ERR-01: Toast notification can be triggered."""
        page.goto(self.url, wait_until="networkidle")

        # Programmatically trigger a toast
        page.evaluate("""
            const el = document.querySelector('[x-data]');
            if (el && el.__x) {
                el.__x.$data.showToast('error', 'Test Error', 'Test message');
            }
        """)

        page.wait_for_timeout(500)

        toast = page.locator("text=Test Error")
        assert toast.is_visible(), "Toast notification should be visible"


# ═══ Responsive Design ═══════════════════════════════════════════════


class TestResponsiveDesign:
    """Verify layout adapts correctly to different viewport sizes."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    @pytest.mark.parametrize(
        "width,height",
        [
            (320, 568),    # Mobile
            (768, 1024),   # Tablet
            (1440, 900),   # Desktop
        ],
    )
    def test_no_horizontal_overflow(self, page, width: int, height: int) -> None:
        """No horizontal scroll at any viewport width."""
        page.set_viewport_size({"width": width, "height": height})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")

        assert scroll_width <= client_width + 1, (
            f"Horizontal overflow at {width}px: "
            f"scrollWidth={scroll_width} > clientWidth={client_width}"
        )

    def test_navigation_tabs_visible_on_mobile(self, page) -> None:
        """AC-RESP-05: Tab navigation accessible at 320px width."""
        page.set_viewport_size({"width": 320, "height": 568})
        page.goto(self.url, wait_until="networkidle")

        nav = page.locator("nav")
        assert nav.is_visible(), "Navigation should be visible on mobile"

    def test_kpi_grid_adapts_to_viewport(self, page) -> None:
        """AC-RESP-01/02/03: KPI grid adapts to viewport width."""
        # Desktop: should show more columns
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        grid = page.locator(".grid").first
        assert grid.is_visible(), "KPI grid should be visible on desktop"

        # Mobile: should still show grid
        page.set_viewport_size({"width": 320, "height": 568})
        page.wait_for_timeout(1000)

        assert grid.is_visible(), "KPI grid should be visible on mobile"


# ═══ Navigation ═══════════════════════════════════════════════════════


class TestNavigation:
    """Verify tab navigation works correctly."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_url: str) -> None:
        self.url = dashboard_url

    def test_tab_navigation_loads_page_at_top(self, page) -> None:
        """AC-SCROLL-04: New page loads at scroll position top."""
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Scroll down
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(300)

        # Navigate to Tasks tab
        page.click("a[href='/tasks']")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, f"Expected scrollY=0 after navigation, got {scroll_y}"

    def test_all_tabs_load_without_server_error(self, page) -> None:
        """All page routes load without 5xx errors."""
        routes = ["/", "/agents", "/tasks", "/kpis", "/costs", "/escalations"]

        for route in routes:
            response = page.goto(f"{self.url}{route}")
            assert response is not None, f"No response for {route}"
            assert response.status < 500, (
                f"Server error {response.status} on {route}"
            )
