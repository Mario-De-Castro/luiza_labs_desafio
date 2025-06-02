import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/v1/token",
        data={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/token",
        data={"username": "wrong", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401