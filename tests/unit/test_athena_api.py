import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_athena_jobs_endpoint(client):
    response = client.get("/api/v1/athena/jobs", headers={"X-API-Key": "dev-admin-key"})
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert "total" in data


def test_athena_pipeline_stats(client):
    response = client.get("/api/v1/athena/stats/pipeline", headers={"X-API-Key": "dev-admin-key"})
    assert response.status_code == 200
    data = response.json()
    assert "total_jobs" in data
    assert "new" in data
