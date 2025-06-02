import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.api.services.clients_services import ClientsService
from src.utils.exceptions.exceptions import GenericExceptions
from src.utils.schemas.clients_schema import ClientsCreate, ClientsUpdate, ListAllClientsRequest, ClientsOut

@pytest.mark.asyncio
async def test_get_all_clients_success():
    db = MagicMock(spec=AsyncSession)
    request = MagicMock(spec=ListAllClientsRequest)
    logger = MagicMock()
    fake_clients = [MagicMock(json=lambda: {"id": 1, "nome": "Test", "email": "test@test.com", "wishlist_id": 1, "created_at": "2024-01-01T00:00:00"})]
    with patch("src.utils.repository.ClientsRepository.get_all", new_callable=AsyncMock) as mock_get_all:
        mock_get_all.return_value = (fake_clients, False)
        result = await ClientsService.get_all_clients(db, request, logger)
        assert hasattr(result, "items")
        assert hasattr(result, "has_next")
        assert result.items[0].id == 1

@pytest.mark.asyncio
async def test_get_all_clients_exception():
    db = MagicMock(spec=AsyncSession)
    request = MagicMock(spec=ListAllClientsRequest)
    logger = MagicMock()
    with patch("src.utils.repository.ClientsRepository.get_all", new_callable=AsyncMock) as mock_get_all:
        mock_get_all.side_effect = Exception("DB error")
        with pytest.raises(GenericExceptions):
            await ClientsService.get_all_clients(db, request, logger)

@pytest.mark.asyncio
async def test_get_client_success():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    fake_client = MagicMock()
    with patch("src.utils.repository.ClientsRepository.get_by_id", new_callable=AsyncMock) as mock_get_by_id:
        mock_get_by_id.return_value = fake_client
        result = await ClientsService.get_client(db, client_id)
        assert result == fake_client

@pytest.mark.asyncio
async def test_get_client_exception():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    with patch("src.utils.repository.ClientsRepository.get_by_id", new_callable=AsyncMock) as mock_get_by_id:
        mock_get_by_id.side_effect = Exception("DB error")
        with pytest.raises(GenericExceptions):
            await ClientsService.get_client(db, client_id)

@pytest.mark.asyncio
async def test_create_client_success():
    db = MagicMock(spec=AsyncSession)
    client_data = MagicMock(spec=ClientsCreate)
    client_data.email = "test@test.com"
    fake_client = MagicMock()
    with patch("src.utils.repository.ClientsRepository.get_by_email", new_callable=AsyncMock) as mock_get_by_email, \
         patch("src.utils.repository.ClientsRepository.create", new_callable=AsyncMock) as mock_create:
        mock_get_by_email.return_value = None
        mock_create.return_value = fake_client
        result = await ClientsService.create_client(db, client_data)
        assert result == fake_client

@pytest.mark.asyncio
async def test_create_client_exception():
    db = MagicMock(spec=AsyncSession)
    client_data = MagicMock(spec=ClientsCreate)
    client_data.email = "test@test.com"
    with patch("src.utils.repository.ClientsRepository.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
        mock_get_by_email.side_effect = Exception("Erro na base de dados")
        with pytest.raises(GenericExceptions):
            await ClientsService.create_client(db, client_data)

@pytest.mark.asyncio
async def test_update_client_success():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    client_data = MagicMock(spec=ClientsUpdate)
    fake_client = MagicMock()
    with patch("src.utils.repository.ClientsRepository.update", new_callable=AsyncMock) as mock_update:
        mock_update.return_value = fake_client
        result = await ClientsService.update_client(db, client_id, client_data)
        assert result == fake_client

@pytest.mark.asyncio
async def test_update_client_exception():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    client_data = MagicMock(spec=ClientsUpdate)
    with patch("src.utils.repository.ClientsRepository.update", new_callable=AsyncMock) as mock_update:
        mock_update.side_effect = Exception("Erro na base de dados")
        with pytest.raises(GenericExceptions):
            await ClientsService.update_client(db, client_id, client_data)

@pytest.mark.asyncio
async def test_delete_cliente_success():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    with patch("src.utils.repository.ClientsRepository.delete", new_callable=AsyncMock) as mock_delete:
        result = await ClientsService.delete_cliente(db, client_id)
        assert result == {"ok": True}

@pytest.mark.asyncio
async def test_delete_cliente_exception():
    db = MagicMock(spec=AsyncSession)
    client_id = 1
    with patch("src.utils.repository.ClientsRepository.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.side_effect = Exception("Erro na Base de Dados")
        with pytest.raises(GenericExceptions):
            await ClientsService.delete_cliente(db, client_id)