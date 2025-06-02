import pytest
from src.utils.models.wishlist import Wishlist
from datetime import datetime

def test_wishlist_repr():
    wishlist = Wishlist(
        wishlist_id=1,
        client_id=10,
        product_id=100,
        product_info="{'name': 'Produto Teste'}",
        created_at=datetime(2024, 1, 1, 12, 0, 0)
    )
    expected = "<Wishlist(wishlist_id=1,client_id=10,product_id=100,product_info={'name': 'Produto Teste'},created_at=2024-01-01 12:00:00)>"
    assert repr(wishlist) == expected

def test_wishlist_json():
    dt = datetime(2024, 2, 2, 15, 30, 0)
    wishlist = Wishlist(
        wishlist_id=2,
        client_id=20,
        product_id=200,
        product_info="{'name': 'PRoduto Topdemais'}",
        created_at=dt
    )
    expected = {
        "wishlist_id": 2,
        "client_id": 20,
        "product_id": 200,
        "product_info": "{'name': 'PRoduto Topdemais'}",
        "created_at": dt
    }
    assert wishlist.json() == expected

def test_wishlist_str():
    wishlist = Wishlist(
        wishlist_id=3,
        client_id=30,
        product_id=300,
        product_info="{'name': 'Produto X'}",
        created_at=datetime(2024, 3, 3, 10, 0, 0)
    )
    expected = "Wishlist(wishlist_id=3, client_id=30, product_id=300)"
    assert str(wishlist) == expected