from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.database.postgres import get_db

from src.utils.schemas.wishlist_schema import (
    GetWishlistByClientIdRequest,
    GetWishlistByClientIdResponse,
    AddProductInWishlistRequest,
    DeleteProductFromWishList,
    WishlistBase,
    AddProductInWishlistRequestPayload
)
from src.api.services.wishlist_services import WishlistService
from src.utils.auth.auth import verify_token


from src.utils.helpers.helpers_functions import HelperFunctions

router = APIRouter(prefix="/clients", tags=["Lista de favoritos"])

logger = HelperFunctions.get_logger()

@router.get("/{client_id}/favorite", response_model=GetWishlistByClientIdResponse)
async def get_wishlist_by_client_id(
    request: GetWishlistByClientIdRequest = Depends(),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
        Lista os produtos favorito do cliente

        **Parâmetros:**
        - `client_id` (int): Identificador unico do cliente.
        - `page` (int): Numero da página a ser consultada (Padrão e 1).
        - `page_size` (int): Tamanho da página (Padrão e 10).

        **Retorna:**
        - Uma dicionario com 2 campos sendo eles items e has_next:
            - `items`: Lista de produtos favorito do cliente paginada.
            - `has_next`: Booleano indicando se ha mais paginas disponiveis.
    """
    return await WishlistService.get_wishlist_by_client_id(db, request, logger)

@router.post("/{client_id}/favorite", response_model=WishlistBase)
async def add_product_in_wishlist(
    client_id: int,
    payload: AddProductInWishlistRequestPayload,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
    Adiciona um produto na lista de desejo do cliente.

    **Payload:**
    As informações necessarias para adicionar um produto na lista de desejo são;

    - `client_id` (str): Identificador do cliente.
    - `product_id` (int): Identificador do produto

    **Retorna:**
    - Um dicionario com os dados do produto criado, incluindo o ID gerado.
    
    """
    request = AddProductInWishlistRequest(client_id=client_id, product_id=payload.product_id)
    return await WishlistService.add_product_in_wishlist(db, request)

@router.delete("/{client_id}/favorite/{product_id}")
async def delete_client(
    client_id: int,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
    ):
    """
    Deleta um produto da lista de desejo do cliente.

    **Parâmetros:**
    - `client_id` (int): ID do cliente a ser deletado.
    - `product_id` (int): ID do produto a ser deletado da lista de desejo.

    **Retorna:**
    - Um dicionario com a mensagem de sucesso da exclusão do produto da lista.
    """
    request = DeleteProductFromWishList(client_id=client_id, product_id=product_id)
    return await WishlistService.delete_product_from_wishlist(db, request)