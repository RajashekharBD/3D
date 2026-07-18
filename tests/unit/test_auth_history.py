import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.auth import get_current_user
from backend.app.core.database import db

client = TestClient(app)

# Mock user for auth dependency bypass
MOCK_USER = {
    "id": "d0000000-0000-0000-0000-000000000000",
    "email": "test_user@example.com"
}

@pytest.fixture(autouse=True)
def override_auth_dependency():
    """Overrides current user dependency to inject mock credentials."""
    app.dependency_overrides[get_current_user] = lambda: MOCK_USER
    yield
    app.dependency_overrides.clear()

def test_api_profile_endpoint():
    """Verifies profile endpoint returns profile structure and mock stats."""
    response = client.get("/api/v1/profile")
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert "statistics" in data
    assert data["profile"]["email"] == "test_user@example.com"

def test_api_history_list_endpoint():
    """Verifies history endpoint returns list of jobs structure."""
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert "total" in data
    assert isinstance(data["jobs"], list)

def test_api_history_job_not_found():
    """Verifies detail of non-existent job returns 404."""
    response = client.get("/api/v1/history/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
