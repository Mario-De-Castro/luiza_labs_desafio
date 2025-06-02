import pytest
from src.utils.models.clients import Clients
from datetime import datetime

def test_clients_repr():
    client = Clients(
        id=1,
        nome="Zezinho",
        email="zezinho@email.com",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0)
    )
    expected = "<Clients(id=1, nome=Zezinho, email=zezinho@email.com, created_at=2024-01-01 12:00:00, updated_at=2024-01-02 12:00:00)>"
    assert repr(client) == expected

def test_clients_json():
    dt_created = datetime(2024, 1, 1, 12, 0, 0)
    dt_updated = datetime(2024, 1, 2, 12, 0, 0)
    client = Clients(
        id=2,
        nome="Mario",
        email="Mario@email.com",
        created_at=dt_created,
        updated_at=dt_updated
    )
    expected = {
        "id": 2,
        "nome": "Mario",
        "email": "Mario@email.com",
        "created_at": dt_created,
        "updated_at": dt_updated
    }
    assert client.json() == expected

def test_clients_str():
    client = Clients(
        id=3,
        nome="Luiza",
        email="Luiza@email.com",
        created_at=datetime(2024, 1, 3, 10, 0, 0),
        updated_at=datetime(2024, 1, 4, 10, 0, 0)
    )
    expected = "Cliente(id=3, nome=Luiza, email=Luiza@email.com, created_at=2024-01-03 10:00:00, updated_at=2024-01-04 10:00:00)"
    assert str(client) == expected