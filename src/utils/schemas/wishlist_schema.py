from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import Query
from typing import Optional

from src.utils.helpers.helpers_functions import HelperFunctions

class WishlistBase(BaseModel):
    """
    Schema base para a wishlist de um cliente.

    Attributes:
        client_id (int): Identificador unico do cliente.
        product_id (int): Identificador do produto na wishlist.
        product_info (str): Informações sobre o produto.
        created_at (str):   Data e hora de criação da wishlist.

    """
    client_id: int
    product_id: int
    product_info: str
    created_at: datetime


class WishlistClear(BaseModel):
    """
    Schema para limpar a wishlist de um cliente.

    Attributes:
        client_id (int): Identificador unico do cliente cuja wishlist será limpa.
    """
    client_id: int


class GetWishlistByClientIdRequest(BaseModel):
    client_id: int = Field(example=[1])
    page: int = Field(Query(1, example=1))
    page_size: int = Field(Query(10, example=10))

class GetWishlistByClientIdResponse(BaseModel):
    items: list[WishlistBase]
    has_next: bool

class AddProductInWishlistRequest(BaseModel):
    client_id: int
    product_id: int

class AddProductInWishlistRequestPayload(BaseModel):
    product_id: int


class DeleteProductFromWishList(BaseModel):
    client_id: int = Field(example=1)
    product_id: int = Field(example=1)