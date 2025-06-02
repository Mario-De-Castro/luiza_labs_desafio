import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.api.services.clients_services import ClientsService
import os
from jose import jwt
from datetime import datetime


@pytest.fixture
def client():
    from src.main import app
    return TestClient(app)

@pytest.fixture
def token():
    SECRET_KEY = os.getenv("SECRET_KEY", "test_secret_key")
    ALGORITHM = "HS256"
    payload = {"sub": "testuser"}
    return "Bearer " + jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def mock_clients_get_all_clients():
    with patch.object(ClientsService, 'get_all_clients', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_clients_get_client():
    with patch.object(ClientsService, 'get_client', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_clients_test_create_client():
    with patch.object(ClientsService, 'create_client', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_clients_test_update_client():
    with patch.object(ClientsService, 'update_client', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_clients_test_delete_client():
    with patch.object(ClientsService, 'delete_cliente', new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
async def test_list_all_clients(mock_clients_get_all_clients, token, client):
    mock_clients_get_all_clients.return_value = {
        "items": [],
        "has_next": False
    }
    response = client.get(
        "/api/v1/clients/",
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "items" in response.json()
    assert "has_next" in response.json()

@pytest.mark.asyncio
async def test_get_client(mock_clients_get_client, token, client):
    mock_clients_get_client.return_value = {
        "id": 1,
        "nome": "Cliente Teste",
        "email": "teste@teste.com",
        "wishlist_id": 1,
        "created_at": datetime.utcnow().isoformat()
    }
    response = client.get(
        "/api/v1/clients/1",
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_create_client(mock_clients_test_create_client, token, client):
    mock_clients_test_create_client.return_value = {
        "id": 1,
        "nome": "Cliente Teste",
        "email": "teste@teste.com",
        "wishlist_id": 1,
        "created_at": datetime.utcnow().isoformat()
    }
    payload = {
        "nome": "Cliente Teste",
        "email": "teste@teste.com"
    }
    response = client.post(
        "/api/v1/clients/",
        json=payload,
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == "Cliente Teste"

@pytest.mark.asyncio
async def test_update_client(mock_clients_test_update_client, token, client):
    mock_clients_test_update_client.return_value = {
        "id": 1,
        "nome": "Cliente Atualizado",
        "email": "atualizado@teste.com",
        "wishlist_id": 1,
        "created_at": datetime.utcnow().isoformat()
    }
    payload = {
        "nome": "Cliente Atualizado",
        "email": "atualizado@teste.com"
    }
    response = client.put(
        "/api/v1/clients/1",
        json=payload,
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == "Cliente Atualizado"

@pytest.mark.asyncio
async def test_delete_client(mock_clients_test_delete_client, token, client):
    mock_clients_test_delete_client.return_value = None
    response = client.delete(
        "/api/v1/clients/1",
        headers={"Authorization": token}
    )
    assert response.status_code in (200, 204)