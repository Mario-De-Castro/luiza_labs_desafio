import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.utils.schemas.wishlist_schema import GetWishlistByClientIdRequest
from src.api.services.wishlist_services import WishlistService

@pytest.mark.asyncio
async def test_get_client_by_client_id_success():

    db = MagicMock(spec=AsyncSession)
    request = GetWishlistByClientIdRequest(client_id=1, page=1, page_size=10)
    logger = MagicMock()
    fake_wishlist = [MagicMock(json=lambda: {"wishlist_id": 1, "client_id": 1, "product_id": 1, "product_info": '{"price": 100.0, "image": "http://example.com/image.jpg", "brand": "Brand", "title": "Product Title", "reviewScore": 4.5}', "created_at": "2024-01-01T00:00:00"})]
    
    with patch("src.utils.repository.WishlistRepository.get_by_client_id", new_callable=AsyncMock) as mock_get_by_client_id:
        mock_get_by_client_id.return_value = (fake_wishlist, False)
        result = await WishlistService.get_wishlist_by_client_id(db, request, logger)
        assert hasattr(result, "items")
        assert hasattr(result, "has_next")
        assert len(result.items) == 1
        assert result.items[0].client_id == 1

@pytest.mark.asyncio
async def test_get_client_by_client_id_exception():
    db = MagicMock(spec=AsyncSession)
    request = GetWishlistByClientIdRequest(client_id=1, page=1, page_size=10)
    logger = MagicMock()
    
    with patch("src.utils.repository.WishlistRepository.get_by_client_id", new_callable=AsyncMock) as mock_get_by_client_id:
        mock_get_by_client_id.side_effect = Exception("DB error")
        with pytest.raises(HTTPException):
            await WishlistService.get_wishlist_by_client_id(db, request, logger)

@pytest.mark.asyncio
async def test_add_product_in_wishlist_success():
    db = MagicMock(spec=AsyncSession)
    wishlist_data = MagicMock()
    wishlist_data.client_id = 1
    wishlist_data.product_id = 1

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result.scalars.return_value = mock_scalars
    db.execute.return_value = mock_result

    mock_wishlist_obj = MagicMock()
    mock_wishlist_obj.json.return_value = {
        "client_id": 1,
        "product_id": 1,
        "product_info": '{"price": 100.0, "image": "http://example.com/image.jpg", "brand": "Brand", "title": "Product Title", "reviewScore": 4.5}',
        "created_at": "2024-01-01T00:00:00"
    }

    with patch("src.utils.repository.WishlistRepository.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_wishlist_obj

        result = await WishlistService.add_product_in_wishlist(db, wishlist_data)
        assert result.client_id == 1
        assert result.product_id == 1

@pytest.mark.asyncio
async def test_add_product_in_wishlist_product_exists():
    db = MagicMock(spec=AsyncSession)
    wishlist_data = MagicMock()
    wishlist_data.client_id = 1
    wishlist_data.product_id = 1
    
    with patch("src.utils.repository.WishlistRepository.get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by_client_id_and_product_id:
        mock_get_by_client_id_and_product_id.return_value = True
        
        with pytest.raises(HTTPException):
            await WishlistService.add_product_in_wishlist(db, wishlist_data)

@pytest.mark.asyncio
async def test_add_product_in_wishlist_product_not_found():
    db = MagicMock(spec=AsyncSession)
    wishlist_data = MagicMock()
    wishlist_data.client_id = 1
    wishlist_data.product_id = 1
    
    with patch("src.utils.repository.WishlistRepository.get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by_client_id_and_product_id, \
         patch("requests.get", side_effect=Exception("Product not found")):
        mock_get_by_client_id_and_product_id.return_value = None
        
        with pytest.raises(HTTPException):
            await WishlistService.add_product_in_wishlist(db, wishlist_data)

@pytest.mark.asyncio
async def test_delete_product_from_wishlist_success():
    db = MagicMock(spec=AsyncSession)
    request = MagicMock()
    request.client_id = 1
    request.product_id = 1
    
    with patch("src.utils.repository.WishlistRepository.delete_by_client_id_and_product_id", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = MagicMock(id=1, client_id=1, product_id=1)
        
        result = await WishlistService.delete_product_from_wishlist(db, request)
        assert result.get('ok') == True


@pytest.mark.asyncio
async def test_delete_product_from_wishlist_not_found():
    db = MagicMock(spec=AsyncSession)
    request = MagicMock()
    request.client_id = 1
    request.product_id = 1
    
    with patch("src.utils.repository.WishlistRepository.delete_by_client_id_and_product_id", new_callable=AsyncMock) as mock_delete:
        mock_delete.side_effect = Exception("Product not found")
        
        with pytest.raises(HTTPException):
            await WishlistService.delete_product_from_wishlist(db, request)
