import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.api.services.clients_services import ClientsService
from src.api.services.wishlist_services import WishlistService
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
def mock_wishlist_get_wishlist_by_client_id():
    with patch.object(WishlistService, 'get_wishlist_by_client_id', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_wishlist_add_product_in_wishlist():
    with patch.object(WishlistService, 'add_product_in_wishlist', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_wishlist_delete_product_from_wishlist():
    with patch.object(WishlistService, 'delete_product_from_wishlist', new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
async def test_get_wishlist_by_client_id(mock_wishlist_get_wishlist_by_client_id, token, client):
    mock_wishlist_get_wishlist_by_client_id.return_value = {
        "items": [],
        "has_next": False
    }
    response = client.get(
        "/api/v1/clients/1/favorite/",
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "items" in response.json()
    assert "has_next" in response.json()

@pytest.mark.asyncio
async def test_add_product_in_wishlist(mock_wishlist_add_product_in_wishlist, token, client):
    mock_wishlist_add_product_in_wishlist.return_value = {
        "wishlist_id": 1,
        "client_id": 1,
        "product_id": 1,
        "product_info": '{"price": 100.0,"image": "http://example.com/image.jpg","brand": "Brand","title": "Product Title","reviewScore": 4.5}',
        "created_at": datetime.now().isoformat(),
    }
    response = client.post(
        "/api/v1/clients/1/favorite/",
        json={"product_id": 1},
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["client_id"] == 1
    assert response.json()["product_id"] == 1

@pytest.mark.asyncio
async def test_delete_product_from_wishlist(mock_wishlist_delete_product_from_wishlist, token, client):
    mock_wishlist_delete_product_from_wishlist.return_value = {
        "id": 1,
        "client_id": 1,
        "product_id": 1
    }
    response = client.delete(
        "/api/v1/clients/1/favorite/1",
        headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
