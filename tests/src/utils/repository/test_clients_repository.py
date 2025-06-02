import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import NoResultFound
from src.utils.repository.clients_repository import ClientsRepository

@pytest.mark.asyncio
async def test_get_all_success():
    db = AsyncMock()
    request = MagicMock(page=1, page_size=2)
    fake_clients = [MagicMock(), MagicMock(), MagicMock()]
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = fake_clients
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    db.execute.return_value = result_mock

    rows, has_next = await ClientsRepository.get_all(db, request)
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert has_next is True

@pytest.mark.asyncio
async def test_get_by_id_success():
    db = AsyncMock()
    client = MagicMock()
    db.get.return_value = client
    result = await ClientsRepository.get_by_id(db, 1)
    assert result == client

@pytest.mark.asyncio
async def test_get_by_id_not_found():
    db = AsyncMock()
    db.get.return_value = None
    with pytest.raises(NoResultFound):
        await ClientsRepository.get_by_id(db, 1)

@pytest.mark.asyncio
async def test_get_by_email_success():
    db = AsyncMock()
    fake_client = MagicMock()
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = fake_client
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    db.execute.return_value = result_mock

    result = await ClientsRepository.get_by_email(db, "test@email.com")
    assert result == fake_client

@pytest.mark.asyncio
async def test_get_by_email_none():
    db = AsyncMock()
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = None
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    db.execute.return_value = result_mock

    result = await ClientsRepository.get_by_email(db, "notfound@email.com")
    assert result is None


@pytest.mark.asyncio
async def test_create_success():
    db = AsyncMock()
    client_data = MagicMock()
    client_data.dict.return_value = {"nome": "Test", "email": "test@email.com"}
    fake_client = MagicMock()
    with patch("src.utils.repository.clients_repository.Clients", return_value=fake_client):
        with patch("src.utils.repository.clients_repository.HelperFunctions.get_time") as mock_time:
            mock_time.return_value.replace.return_value = "2024-01-01T00:00:00"
            db.add.return_value = None
            db.commit.return_value = None
            db.refresh.return_value = None
            result = await ClientsRepository.create(db, client_data)
            assert result == fake_client
            assert fake_client.created_at == "2024-01-01T00:00:00"

@pytest.mark.asyncio
async def test_update_success():
    db = AsyncMock()
    client = MagicMock()
    db.get.return_value = client
    clients_data = MagicMock()
    clients_data.dict.return_value = {"nome": "Novo Mario"}

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result.scalars.return_value = mock_scalars
    db.execute.return_value = mock_result

    db.commit.return_value = None
    db.refresh.return_value = None

    result = await ClientsRepository.update(db, 1, clients_data)
    assert result == client
    assert client.nome == "Novo Mario"

@pytest.mark.asyncio
async def test_update_not_found():
    db = AsyncMock()
    db.get.return_value = None
    clients_data = MagicMock()
    import pytest
    with pytest.raises(NoResultFound):
        await ClientsRepository.update(db, 1, clients_data)


@pytest.mark.asyncio
async def test_delete_success():
    db = AsyncMock()
    client = MagicMock()
    db.get.return_value = client
    db.delete.return_value = None
    db.commit.return_value = None
    result = await ClientsRepository.delete(db, 1)
    assert result == client

@pytest.mark.asyncio
async def test_delete_not_found():
    db = AsyncMock()
    db.get.return_value = None
    with pytest.raises(NoResultFound):
        await ClientsRepository.delete(db, 1)
