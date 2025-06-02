from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.utils.exceptions.exceptions import GenericExceptions
from src.utils.models.wishlist import Wishlist
from src.utils.schemas.wishlist_schema import (
    AddProductInWishlistRequest,
    GetWishlistByClientIdRequest,
    DeleteProductFromWishList
)
from src.utils.helpers.helpers_functions import HelperFunctions
from sqlalchemy.exc import NoResultFound


class WishlistRepository:
    
    async def get_by_client_id(db: AsyncSession, request: GetWishlistByClientIdRequest):
        try:
            result = await db.execute(
                select(
                    Wishlist
                ).where(
                    Wishlist.client_id == request.client_id
                ).offset(
                    (request.page - 1) * request.page_size
                ).limit(request.page_size + 1)
                )
        
            rows = result.scalars().all()
            has_next = len(rows) > request.page_size
            rows = rows[:request.page_size]

            return rows, has_next
        except Exception as e:
            raise
    
    async def get_by_product_id(db: AsyncSession, product_id: int) -> Wishlist:
        try:
            result = await db.execute(select(Wishlist).where(Wishlist.product_id == product_id))
            return result.scalars().first()
        except Exception as e:
            raise
    
    async def get_by_client_id_and_product_id(db: AsyncSession, wishlist_data: AddProductInWishlistRequest):
        try:
            result = await db.execute(
                select(
                    Wishlist
                ).filter(
                    Wishlist.client_id == wishlist_data.client_id,
                    Wishlist.product_id == wishlist_data.product_id
                )
            )
            return result.scalars().first()
        except Exception as e:
            raise
 
    async def create(db: AsyncSession, wishlist_data: AddProductInWishlistRequest, product_info: str) -> Wishlist:
        """
        Cria um novo produto na wishlist do cliente.

        Args:
            db (AsyncSession): Sessão assincrona do banco de dados.
            wishlist_data (AddProductInWishlistRequest): Schema contendo os dados do produto a ser adicionado na wishlist.
            product_info (str): Informações adicionais sobre o produto.
        Raises:
            HTTPException: Se o produto ja estiver na wishlist do cliente ou se o produto não for encontrado.
            GenericExceptions: Se ocorrer um erro ao adicionar o produto na wishlist.
        Returns:
            Wishlist: Retorna um objeto Wishlist com os dados do produto adicionado na wishlist.
        """
        try:
            wishlist = Wishlist(
                client_id=wishlist_data.client_id,
                product_id=wishlist_data.product_id,
                product_info=product_info,
                created_at=HelperFunctions.get_time().replace(tzinfo=None)
            )
            db.add(wishlist)
            await db.commit()
            await db.refresh(wishlist)
            return wishlist
        except Exception as e:
            raise
    
    async def delete_by_client_id_and_product_id(db: AsyncSession, request: DeleteProductFromWishList):
        """
        Deleta um produto da wishlist do cliente.

        Args:
            db (AsyncSession): Sessão assincrona do banco de dados.
            request (DeleteProductFromWishList): Schema contendo os dados do cliente e do produto a ser deletado.
        Raises:
            NoResultFound: Se o produto não for encontrado na wishlist do cliente.
            GenericExceptions: Se ocorrer um erro ao deletar o produto da wishlist.
        Returns:
            Wishlist: Retorna o objeto Wishlist deletado, ou None se não houver produto na wishlist.
        """
        try:
            product = await WishlistRepository.get_by_client_id_and_product_id(db, request)
            if not product:
                raise NoResultFound
            result = await db.execute(
                select(Wishlist).where(
                    Wishlist.client_id == request.client_id,
                    Wishlist.product_id == request.product_id
                )
            )
            wishlist = result.scalars().first()
            if wishlist:
                await db.delete(wishlist)
                await db.commit()
                return wishlist
            return None
        
        except Exception as e:
            raise