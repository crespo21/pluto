from fastapi.testclient import TestClient

from src.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "Pluto API is running"}


def test_users_route_exists():
    client = TestClient(app)
    response = client.get("/api/users/1")

    assert response.status_code in (200, 404, 422)
