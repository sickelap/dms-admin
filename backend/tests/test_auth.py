from fastapi.testclient import TestClient

from dms_admin_api.main import create_app


def test_login_sets_session_cookie() -> None:
    client = TestClient(create_app())

    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})

    assert response.status_code == 200
    assert response.json() == {"authenticated": True, "username": "admin"}
    assert "dms_admin_session" in response.cookies


def test_protected_endpoint_rejects_unauthenticated_requests() -> None:
    client = TestClient(create_app())

    response = client.get("/api/system/status")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_session_does_not_expose_configured_password() -> None:
    client = TestClient(create_app())
    client.post("/api/auth/login", json={"username": "admin", "password": "admin"})

    response = client.get("/api/auth/session")

    assert response.status_code == 200
    assert response.json() == {"authenticated": True, "username": "admin"}
    assert "password" not in response.text
