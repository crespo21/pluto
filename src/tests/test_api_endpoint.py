# @"
# """Integration tests for user endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.infrastructure.database.models.user_model import Base
from src.infrastructure.database.config import get_session


@pytest.fixture(scope="function")
def test_db():
    """Create in-memory test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    def override_get_session():
        yield session
    
    app.dependency_overrides[get_session] = override_get_session
    yield session
    session.close()


@pytest.fixture
def client(test_db):
    """Create test client."""
    return TestClient(app)


class TestUserEndpoints:
    """Tests for user API endpoints."""

    def test_create_user(self, client):
        response = client.post(
            "/api/users",
            json={"username": "testuser", "email": "test@example.com", "status": "active"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_user(self, client):
        create_resp = client.post(
            "/api/users",
            json={"username": "alice", "email": "alice@example.com", "status": "active"}
        )
        user_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/users/{user_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["username"] == "alice"

    def test_get_user_by_username(self, client):
        client.post(
            "/api/users",
            json={"username": "bob", "email": "bob@example.com", "status": "active"}
        )

        response = client.get("/api/users/by-username/bob")
        assert response.status_code == 200
        assert response.json()["username"] == "bob"

    def test_update_user_status(self, client):
        create_resp = client.post(
            "/api/users",
            json={"username": "charlie", "email": "charlie@example.com", "status": "active"}
        )
        user_id = create_resp.json()["id"]

        update_resp = client.patch(f"/api/users/{user_id}/status", json={"status": "inactive"})
        assert update_resp.status_code == 200
        assert update_resp.json()["status"] == "inactive"

    def test_delete_user(self, client):
        create_resp = client.post(
            "/api/users",
            json={"username": "dave", "email": "dave@example.com", "status": "active"}
        )
        user_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/api/users/{user_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/users/{user_id}")
        assert get_resp.status_code == 404
# "@ | Out-File -Encoding UTF8 "src\tests\test_user_endpoints.py"
# Write-Host "✓ Created test_user_endpoints.py"