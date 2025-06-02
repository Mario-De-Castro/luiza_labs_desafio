from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.utils.schemas.wishlist_schema import (
    WishlistBase,
    GetWishlistByClientIdRequest,
    GetWishlistByClientIdResponse,
    AddProductInWishlistRequest,
    DeleteProductFromWishList
)
from src.utils.repository import (
    WishlistRepository
)
from src.utils.helpers.helpers_functions import HelperFunctions
from src.utils.exceptions.exceptions import GenericExceptions, DataAlreadyExistsException
from logging import Logger
import requests


class WishlistService:

    async def get_wishlist_by_client_id(db: AsyncSession, request: GetWishlistByClientIdRequest, logger: Logger):
        """
            Obtem todos os produtos da lista de favoritos de maneira paginada

            Args:
                db (AsyncSession): Sessão assincrona do banco de dados.
                request (GetWishlistByClientIdRequest): Schema GetWishlistByClientIdRequest contendo os parâmetros de paginação.
            
            Returns:
                GetWishlistByClientIdResponse: Resposta contendo a lista de produtos do clientes e se ha mais paginas.
        
        """
        try:
            wishlist, has_next = await WishlistRepository.get_by_client_id(db, request)
            return GetWishlistByClientIdResponse(
                items=[WishlistBase(**products.json()) for products in wishlist],
                has_next=has_next
            )
        except Exception as e:
            raise GenericExceptions(f"Erro ao retornar a lista de clientes: {str(e)}")
        
    async def add_product_in_wishlist(db: AsyncSession, wishlist_data: AddProductInWishlistRequest):
        """
            Cria um novo produto na wishlist do cliente.

            Args:
                db (AsyncSession): Sessão assincrona do banco de dados.
                wishlist_data (AddProductInWishlistRequest): Schema contendo os dados do produto a ser adicionado na wishlist.

            Raises:
                HTTPException: Se o produto ja estiver na wishlist do cliente ou se o produto não for encontrado.
                GenericExceptions: Se ocorrer um erro ao adicionar o produto na wishlist.
            
            Returns:
                WishlistBase: Retorna um objeto WishlistBase com os dados do produto adicionado na wishlist.
        """
        try:
            product_exist_on_the_client_wishlist = await WishlistRepository.get_by_client_id_and_product_id(db, wishlist_data)
            if product_exist_on_the_client_wishlist:
                raise DataAlreadyExistsException("Product already exists in the wishlist for this client.")
            
            product_url = f"http://challenge-api.luizalabs.com/api/product/{wishlist_data.product_id}/"
            try:
                response = requests.get(product_url, timeout=3)
                if response.status_code == 200:
                    product_info = response.json()
                else:
                    raise HTTPException(status_code=404, detail="Product not found or no exist")
            except requests.exceptions.RequestException:
                product = await WishlistRepository.get_by_product_id(db, wishlist_data.product_id)
                if product:
                    product_info = product.product_info
                else:
                    product_info = {
                        "price": 0.0,
                        "image": "https://image_mockado.com.br",
                        "brand": "MockBrand",
                        "id": wishlist_data.product_id,
                        "title": "Produto Mockado",
                        "reviewScore": 3,
                        "mocked": True
                    }
            wishlist_data = await WishlistRepository.create(db, wishlist_data, str(product_info))
            return WishlistBase(**wishlist_data.json())
        except DataAlreadyExistsException as e:
            raise
        except Exception as e:
            raise GenericExceptions(f"Erro ao adicionar produto na lista de favoritos -> {e}")


    async def delete_product_from_wishlist(db: AsyncSession, request: DeleteProductFromWishList):
        """
        Deleta um produto da lista de desejo do cliente com base no product_id e client_id informado.

        Args:
            db (AsyncSession): Sessão assincrona do banco de dados.
            client_id (int): ID do cliente a ser deletado.
            product_id (int): ID do produto a ser deletado da lista de desejo.
            
        Raises:
            NoResultFound: Se não for encontrado nenhum produto na wishlist do cliente com o product_id informado.
            GenericExceptions: Se ocorrer um erro ao deletar o produto da wishlist.
        Returns:
            dict: Dicionário indicando se a operação foi bem-sucedida.
        """
        try:
            await WishlistRepository.delete_by_client_id_and_product_id(db, request)
            return {"ok": True}
        except NoResultFound:
            raise
        except Exception as e:
            raise GenericExceptions(f"Erro ao deletar o client -> {e}")
