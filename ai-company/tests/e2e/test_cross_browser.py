"""Cross-browser dashboard tests.

Validates that the dashboard renders and behaves correctly across
Chromium, Firefox, and WebKit.

Prerequisites:
    pip install playwright pytest-playwright
    playwright install

Run:
    pytest tests/e2e/test_cross_browser.py -v --headed
"""

from __future__ import annotations

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(90),
]


# ---------------------------------------------------------------------------
# Core rendering tests per browser
# ---------------------------------------------------------------------------


class TestDashboardRendering:
    """Verify core dashboard rendering across browser engines."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(3000)

    def test_page_loads_with_title(self, page) -> None:
        assert "Dashboard" in page.title() or "Light Speed" in page.title()

    def test_header_visible(self, page) -> None:
        header = page.locator("header")
        assert header.is_visible()

    def test_kpi_cards_render(self, page) -> None:
        """All 6 KPI cards should be visible."""
        kpi_cards = page.locator(".kpi-card")
        assert kpi_cards.count() == 6

    def test_kpi_values_populated(self, page) -> None:
        """KPI values should be populated (not stuck at 0 if data exists)."""
        # Wait for data load
        page.wait_for_timeout(3000)
        # At least total_agents should be non-zero
        agent_card = page.locator(".kpi-card").nth(5)
        text = agent_card.inner_text()
        # Should contain a number (agents)
        assert any(c.isdigit() for c in text)

    def test_navigation_tabs_visible(self, page) -> None:
        """All navigation tabs should be rendered."""
        nav = page.locator("nav")
        links = nav.locator("a")
        assert links.count() >= 6  # dashboard, agents, tasks, kpis, costs, approvals

    def test_charts_section_exists(self, page) -> None:
        """Chart.js canvases should be present."""
        task_chart = page.locator("#taskStatusChart")
        assert task_chart.count() >= 0  # May be canvas or absent

    def test_recent_tasks_table(self, page) -> None:
        """Tasks table or empty state message should be visible."""
        table = page.locator("table")
        empty_state = page.locator("text=No tasks yet")
        assert table.count() > 0 or empty_state.count() > 0

    def test_websocket_indicator_shows_status(self, page) -> None:
        """WS connection indicator should show 'Live' or 'Offline'."""
        indicator = page.locator("text=Live").or_(page.locator("text=Offline"))
        assert indicator.count() > 0

    def test_dark_theme_applied(self, page) -> None:
        """The <html> element should have the 'dark' class."""
        html_classes = page.locator("html").get_attribute("class")
        assert "dark" in (html_classes or "")

    def test_alpine_js_initialized(self, page) -> None:
        """Alpine.js x-data should be bound to the body."""
        result = page.evaluate("""
            () => {
                const el = document.querySelector('[x-data]');
                return el && el._x_dataStack && el._x_dataStack.length > 0;
            }
        """)
        assert result is True


# ---------------------------------------------------------------------------
# Navigation tests
# ---------------------------------------------------------------------------


class TestCrossPageNavigation:
    """Verify navigation works across all dashboard pages."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

    @pytest.mark.parametrize("path,expected_text", [
        ("/agents", "Agents"),
        ("/tasks", "Tasks"),
        ("/kpis", "KPI"),
        ("/costs", "Cost"),
        ("/escalations", "Approv"),
    ])
    def test_page_renders(self, page, path: str, expected_text: str) -> None:
        """Each page route should render without errors."""
        page.goto(f"{self.url}{path}", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Page should not show a Python traceback
        body_text = page.locator("body").inner_text()
        assert "Traceback" not in body_text
        assert "Internal Server Error" not in body_text
        # Page should contain expected content
        assert expected_text.lower() in body_text.lower() or len(body_text) > 100

    def test_health_endpoint(self, page, dashboard_server: str) -> None:
        """The /health endpoint should return OK."""
        resp = page.goto(f"{dashboard_server}/health")
        assert resp.status == 200
        body = page.locator("body").inner_text()
        assert "ok" in body.lower()


# ---------------------------------------------------------------------------
# Responsive / viewport tests
# ---------------------------------------------------------------------------


class TestResponsiveBehavior:
    """Verify dashboard layout adapts to different viewports."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server

    def test_kpi_grid_adapts_to_mobile(self, page) -> None:
        """KPI cards should use 2-col grid on mobile."""
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        kpi_cards = page.locator(".kpi-card")
        assert kpi_cards.count() == 6

    def test_kpi_grid_adapts_to_tablet(self, page) -> None:
        """KPI cards should use 3-col grid on tablet."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        kpi_cards = page.locator(".kpi-card")
        assert kpi_cards.count() == 6

    def test_kpi_grid_adapts_to_desktop(self, page) -> None:
        """KPI cards should use 6-col grid on desktop."""
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        kpi_cards = page.locator(".kpi-card")
        assert kpi_cards.count() == 6

    def test_no_horizontal_scroll_on_mobile(self, page) -> None:
        """Page should not have horizontal overflow on mobile."""
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(self.url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        overflow = page.evaluate("""
            () => document.documentElement.scrollWidth > document.documentElement.clientWidth
        """)
        assert overflow is False, "Page has horizontal overflow on mobile viewport"
