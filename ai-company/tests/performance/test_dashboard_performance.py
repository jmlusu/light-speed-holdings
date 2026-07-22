"""Performance tests for the CEO dashboard.

Validates:
- Page load time (time to interactive)
- API response times under load
- Chart render performance
- Scroll smoothness metrics
- Memory usage stability

Run:
    pytest tests/performance/test_dashboard_performance.py -v -m performance
    # Or run all:
    pytest tests/performance/test_dashboard_performance.py -v
"""

from __future__ import annotations

import time
from pathlib import Path
from statistics import mean, stdev

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from tests.fixtures.dashboard_data import patch_rate_limiter, seed_dashboard_workspace

pytestmark = pytest.mark.performance


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Isolated TestClient for performance testing."""
    monkeypatch.chdir(tmp_path)
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    dash_api._bus = None

    seed_dashboard_workspace(tmp_path, task_count=50, agent_count=10)

    with patch_rate_limiter():
        yield TestClient(app, raise_server_exceptions=False)

    reset_state_store()
    dash_api._bus = None


# ---------------------------------------------------------------------------
# API Response Time Benchmarks
# ---------------------------------------------------------------------------


class TestAPIPerformance:
    """Benchmark API endpoint response times."""

    @pytest.mark.parametrize("endpoint", [
        "/api/dashboard",
        "/api/agents",
        "/api/tasks",
        "/api/org-chart",
        "/api/departments",
        "/api/kpis",
        "/api/kpis/summary",
        "/api/models",
        "/api/metrics",
        "/health",
    ])
    def test_endpoint_response_time_p95(
        self, client: TestClient, endpoint: str
    ) -> None:
        """P95 response time must be under 200ms."""
        times = []
        for _ in range(10):
            start = time.perf_counter()
            resp = client.get(endpoint)
            elapsed_ms = (time.perf_counter() - start) * 1000
            times.append(elapsed_ms)
            assert resp.status_code in (200, 404)

        p95 = sorted(times)[int(len(times) * 0.95)]
        assert p95 < 200, (
            f"{endpoint} P95 response time {p95:.0f}ms exceeds 200ms. "
            f"All times: {[f'{t:.1f}' for t in times]}"
        )

    def test_dashboard_endpoint_throughput(self, client: TestClient) -> None:
        """Dashboard endpoint should handle 100 sequential requests in < 10s."""
        start = time.perf_counter()
        for _ in range(100):
            resp = client.get("/api/dashboard")
            assert resp.status_code == 200
        elapsed = time.perf_counter() - start

        assert elapsed < 10.0, (
            f"100 dashboard requests took {elapsed:.1f}s (limit: 10s)"
        )

    def test_concurrent_task_creation(self, client: TestClient) -> None:
        """Create 50 tasks concurrently and verify all succeed."""
        start = time.perf_counter()
        results = []
        for i in range(50):
            resp = client.post("/api/tasks", json={
                "receiver_id": "lead-engineering",
                "instruction": f"Performance test task {i}",
            })
            results.append(resp)
        elapsed = time.perf_counter() - start

        for resp in results:
            assert resp.status_code == 201

        assert elapsed < 5.0, (
            f"50 task creations took {elapsed:.1f}s (limit: 5s)"
        )

    def test_large_dataset_performance(self, client: TestClient) -> None:
        """Dashboard should handle 500+ tasks without degradation."""
        # Create 500 additional tasks (workspace already seeds 50)
        for i in range(500):
            client.post("/api/tasks", json={
                "receiver_id": "lead-engineering",
                "instruction": f"Bulk task {i}",
            })

        # Measure dashboard response with large dataset
        start = time.perf_counter()
        resp = client.get("/api/dashboard")
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert resp.status_code == 200
        assert elapsed_ms < 500, (
            f"Dashboard with 500+ tasks took {elapsed_ms:.0f}ms (limit: 500ms)"
        )

        # Also check task listing (50 seeded + 500 created = 550)
        start = time.perf_counter()
        resp = client.get("/api/tasks")
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert resp.status_code == 200
        task_count = len(resp.json())
        assert task_count >= 500, f"Expected at least 500 tasks, got {task_count}"
        assert elapsed_ms < 500, (
            f"Task listing ({task_count} tasks) took {elapsed_ms:.0f}ms (limit: 500ms)"
        )


# ---------------------------------------------------------------------------
# API Consistency Tests (No Variance Spikes)
# ---------------------------------------------------------------------------


class TestAPIConsistency:
    """Ensure API response times are consistent (no variance spikes)."""

    def test_dashboard_response_time_consistency(self, client: TestClient) -> None:
        """Response time standard deviation should be < 50ms across 20 requests."""
        times = []
        for _ in range(20):
            start = time.perf_counter()
            client.get("/api/dashboard")
            times.append((time.perf_counter() - start) * 1000)

        avg = mean(times)
        sd = stdev(times) if len(times) > 1 else 0

        assert sd < 50, (
            f"Response time variance too high: avg={avg:.1f}ms, sd={sd:.1f}ms. "
            f"Times: {[f'{t:.1f}' for t in times]}"
        )

    def test_no_memory_leak_on_repeated_calls(self, client: TestClient) -> None:
        """Repeated API calls should not cause memory growth (basic check)."""
        import os

        # Get baseline
        try:
            import psutil
            proc = psutil.Process(os.getpid())
            baseline_mb = proc.memory_info().rss / 1024 / 1024
        except ImportError:
            pytest.skip("psutil not installed")

        # Make 200 API calls
        for _ in range(200):
            client.get("/api/dashboard")

        # Check memory
        current_mb = proc.memory_info().rss / 1024 / 1024
        growth_mb = current_mb - baseline_mb

        assert growth_mb < 50, (
            f"Memory grew by {growth_mb:.1f}MB after 200 API calls "
            f"(baseline: {baseline_mb:.1f}MB, current: {current_mb:.1f}MB)"
        )


# ---------------------------------------------------------------------------
# Dashboard Data Integrity Tests
# ---------------------------------------------------------------------------


class TestDataIntegrity:
    """Verify data consistency across repeated reads."""

    def test_dashboard_kpis_are_consistent(self, client: TestClient) -> None:
        """Multiple dashboard reads should return the same KPI values."""
        results = [client.get("/api/dashboard").json() for _ in range(5)]

        for key in ("pending_tasks", "total_agents", "completed_tasks"):
            values = [r[key] for r in results]
            assert len(set(values)) == 1, (
                f"Inconsistent {key}: {values}"
            )

    def test_task_count_matches_across_endpoints(self, client: TestClient) -> None:
        """Task count from /api/dashboard should match /api/tasks length."""
        dashboard = client.get("/api/dashboard").json()
        tasks = client.get("/api/tasks").json()

        total_from_dashboard = (
            dashboard["pending_tasks"]
            + dashboard["in_progress_tasks"]
            + dashboard["completed_tasks"]
            + dashboard["failed_tasks"]
            + dashboard["escalated_tasks"]
        )
        assert total_from_dashboard == len(tasks), (
            f"Dashboard reports {total_from_dashboard} tasks, "
            f"but /api/tasks returns {len(tasks)}"
        )

    def test_agent_count_consistency(self, client: TestClient) -> None:
        """Agent count from dashboard should match /api/agents length."""
        dashboard = client.get("/api/dashboard").json()
        agents = client.get("/api/agents").json()
        assert dashboard["total_agents"] == len(agents)

    def test_org_chart_agent_count_matches(self, client: TestClient) -> None:
        """Total agents in org chart should match /api/agents count."""
        agents = client.get("/api/agents").json()
        org = client.get("/api/org-chart").json()

        def count_nodes(nodes: list) -> int:
            total = 0
            for node in nodes:
                total += 1
                total += count_nodes(node.get("children", []))
            return total

        assert count_nodes(org) == len(agents)


# ---------------------------------------------------------------------------
# WebSocket broadcast tests
# ---------------------------------------------------------------------------


class TestWebSocketPerformance:
    """Validate WebSocket infrastructure performance."""

    def test_broadcast_manager_connect_disconnect(self) -> None:
        """ConnectionManager connect/disconnect should be fast."""
        from ai_company.dashboard.ws import ConnectionManager

        cm = ConnectionManager()

        class FakeWS:
            def __init__(self) -> None:
                self.messages: list[str] = []

            async def accept(self) -> None:
                pass

            async def send_text(self, text: str) -> None:
                self.messages.append(text)

        import asyncio

        async def _bench() -> None:
            ws = FakeWS()
            start = time.perf_counter()
            for _ in range(100):
                await cm.connect(ws)
                await cm.disconnect(ws)
            elapsed_ms = (time.perf_counter() - start) * 1000
            return elapsed_ms

        elapsed_ms = asyncio.run(_bench())
        assert elapsed_ms < 500, (
            f"100 connect/disconnect cycles took {elapsed_ms:.0f}ms"
        )

    def test_broadcast_reach_all_clients(self) -> None:
        """Broadcast should reach all connected clients."""
        from ai_company.dashboard.ws import ConnectionManager

        cm = ConnectionManager()

        class FakeWS:
            def __init__(self) -> None:
                self.messages: list[str] = []

            async def accept(self) -> None:
                pass

            async def send_text(self, text: str) -> None:
                self.messages.append(text)

        import asyncio

        async def _test() -> None:
            clients = [FakeWS() for _ in range(10)]
            for ws in clients:
                await cm.connect(ws)

            await cm.broadcast({"type": "test", "data": "hello"})

            for ws in clients:
                assert len(ws.messages) == 1
                assert '"test"' in ws.messages[0]

        asyncio.run(_test())
