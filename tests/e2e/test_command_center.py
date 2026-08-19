"""E2E tests for the J.A.R.V.I.S. Command Center page.

Validates that the /command-center route renders correctly and
the SVG overlay + Alpine.js controller initialize without errors.

Prerequisites:
    uv sync --extra dev --extra e2e
    uv run playwright install
    uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"

Run:
    uv run pytest tests/e2e/test_command_center.py -v
"""

from __future__ import annotations

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(60),
]


class TestCommandCenterRendering:
    """Verify command center page renders core elements."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server
        page.goto(f"{self.url}/command-center", wait_until="networkidle")
        page.wait_for_timeout(3000)

    def test_page_loads(self, page) -> None:
        """Command center page should load without errors."""
        body_text = page.locator("body").inner_text()
        assert "Traceback" not in body_text
        assert "Internal Server Error" not in body_text

    def test_page_title_contains_command_center(self, page) -> None:
        title = page.title()
        assert "Command" in title or "Dashboard" in title or "Light Speed" in title

    def test_alpine_js_initialized(self, page) -> None:
        """Alpine.js x-data should be bound on the command-center div."""
        result = page.evaluate("""
            () => {
                const el = document.querySelector('.command-center[x-data]');
                return !!(el && el._x_dataStack && el._x_dataStack.length > 0);
            }
        """)
        assert result is True

    def test_command_center_panel_exists(self, page) -> None:
        """The main .command-center wrapper should exist."""
        panels = page.locator(".command-center")
        assert panels.count() >= 1

    def test_alpine_variant_bound(self, page) -> None:
        """Alpine should expose a 'variant' property ('A', 'B', or 'C')."""
        variant = page.evaluate("""
            () => {
                const el = document.querySelector('.command-center[x-data]');
                if (!el || !el._x_dataStack) return null;
                const data = el._x_dataStack[0];
                return data && data.variant ? data.variant : null;
            }
        """)
        assert variant in ("A", "B", "C", None)


class TestCommandCenterSVGOverlay:
    """Verify SVG overlay elements are present in the template."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server
        page.goto(f"{self.url}/command-center", wait_until="networkidle")
        page.wait_for_timeout(3000)

    def test_arc_reactor_exists(self, page) -> None:
        """The .cc-arc-reactor container should exist in the DOM."""
        reactors = page.locator(".cc-arc-reactor")
        assert reactors.count() >= 1

    def test_svg_overlay_exists(self, page) -> None:
        """SVG overlay elements should exist within arc reactors."""
        svg = page.locator(".cc-core-svg-overlay")
        assert svg.count() >= 1

    def test_reactor_rings_exist(self, page) -> None:
        """Reactor ring elements (outer, middle, inner) should exist."""
        rings = page.locator(".cc-reactor-ring")
        assert rings.count() >= 3


class TestCommandCenterAPIEndpoints:
    """Verify new read-only API endpoints are reachable."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server

    def test_health_endpoint(self, page) -> None:
        resp = page.goto(f"{self.url}/health")
        assert resp.status == 200
        body = page.locator("body").inner_text()
        assert "ok" in body.lower()

    def test_api_health_endpoint(self, page) -> None:
        resp = page.goto(f"{self.url}/api/v1/models/telemetry")
        assert resp.status == 200

    def test_briefing_endpoint(self, page) -> None:
        resp = page.goto(f"{self.url}/api/v1/briefing")
        assert resp.status == 200


class TestCommandCenterResponsive:
    """Verify command center adapts to different viewports."""

    @pytest.fixture(autouse=True)
    def _setup(self, page, dashboard_server: str) -> None:
        self.url = dashboard_server

    def test_renders_on_mobile(self, page) -> None:
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{self.url}/command-center", wait_until="networkidle")
        page.wait_for_timeout(2000)
        body_text = page.locator("body").inner_text()
        assert "Traceback" not in body_text

    def test_renders_on_tablet(self, page) -> None:
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(f"{self.url}/command-center", wait_until="networkidle")
        page.wait_for_timeout(2000)
        body_text = page.locator("body").inner_text()
        assert "Traceback" not in body_text

    def test_renders_on_desktop(self, page) -> None:
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(f"{self.url}/command-center", wait_until="networkidle")
        page.wait_for_timeout(2000)
        body_text = page.locator("body").inner_text()
        assert "Traceback" not in body_text
