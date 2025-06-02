from fastapi.testclient import TestClient
from src.main import app, create_app

def test_create_app_returns_fastapi_instance():
    test_app = create_app()
    assert hasattr(test_app, "openapi")
    assert hasattr(test_app, "router")
    assert callable(test_app.openapi)

def test_health_check_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_docs_and_redoc_endpoints():
    client = TestClient(app)
    docs_response = client.get("/api/docs")
    redoc_response = client.get("/api/redoc")
    assert docs_response.status_code == 200
    assert redoc_response.status_code == 200

def test_cors_headers_on_health_check():
    client = TestClient(app)
    response = client.options("/health", headers={
        "Origin": "http://localhost",
        "Access-Control-Request-Method": "GET"
    })
    assert response.headers.get("access-control-allow-origin") == "http://localhost"