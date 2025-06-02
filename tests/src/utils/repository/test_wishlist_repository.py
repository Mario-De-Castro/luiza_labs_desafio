import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import NoResultFound
from src.utils.repository.wishlist_repository import WishlistRepository

@pytest.mark.asyncio
async def test_delete_by_client_id_and_product_id_success():
    db = AsyncMock()
    request = MagicMock()
    fake_product = MagicMock()
    fake_wishlist = MagicMock()
    # Mock get_by_client_id_and_product_id to return a product
    with patch.object(WishlistRepository, "get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by:
        mock_get_by.return_value = fake_product
        # Mock db.execute().scalars().first() to return a wishlist
        scalars_mock = MagicMock()
        scalars_mock.first.return_value = fake_wishlist
        result_mock = MagicMock()
        result_mock.scalars.return_value = scalars_mock
        db.execute.return_value = result_mock
        db.delete.return_value = None
        db.commit.return_value = None

        result = await WishlistRepository.delete_by_client_id_and_product_id(db, request)
        assert result == fake_wishlist
        db.delete.assert_awaited_once_with(fake_wishlist)
        db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_by_client_id_and_product_id_not_found():
    db = AsyncMock()
    request = MagicMock()
    # Mock get_by_client_id_and_product_id to return None
    with patch.object(WishlistRepository, "get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by:
        mock_get_by.return_value = None
        with pytest.raises(NoResultFound):
            await WishlistRepository.delete_by_client_id_and_product_id(db, request)

@pytest.mark.asyncio
async def test_delete_by_client_id_and_product_id_no_wishlist():
    db = AsyncMock()
    request = MagicMock()
    fake_product = MagicMock()
    # Mock get_by_client_id_and_product_id to return a product
    with patch.object(WishlistRepository, "get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by:
        mock_get_by.return_value = fake_product
        # Mock db.execute().scalars().first() to return None
        scalars_mock = MagicMock()
        scalars_mock.first.return_value = None
        result_mock = MagicMock()
        result_mock.scalars.return_value = scalars_mock
        db.execute.return_value = result_mock

        result = await WishlistRepository.delete_by_client_id_and_product_id(db, request)
        assert result is None

@pytest.mark.asyncio
async def test_delete_by_client_id_and_product_id_exception():
    db = AsyncMock()
    request = MagicMock()
    with patch.object(WishlistRepository, "get_by_client_id_and_product_id", new_callable=AsyncMock) as mock_get_by:
        mock_get_by.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            await WishlistRepository.delete_by_client_id_and_product_id(db, request)