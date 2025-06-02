from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.utils.schemas.clients_schema import (
    ClientsCreate,
    ClientsUpdate,
    ListAllClientsRequest,
    ListAllClientsResponse,
    ClientsOut
)
from src.utils.repository import (
    ClientsRepository
)
from src.utils.exceptions.exceptions import GenericExceptions, DataAlreadyExistsException
from logging import Logger


class ClientsService:

    async def get_all_clients(db: AsyncSession, request: ListAllClientsRequest, logger: Logger):
        """
            Obtem todos os clientes de maneira paginada

            Args:
                db (AsyncSession): Sessão assincrona do banco de dados.
                request (ListAllClientsRequest): Schema ListAllClientsRequest contendo os parâmetros de paginação.
            
            Returns:
                ListAllClientsResponse: Resposta contendo a lista de clientes e se ha mais paginas.
        
        """
        try:
            clients, has_next = await ClientsRepository.get_all(db, request)
            return ListAllClientsResponse(
                items=[ClientsOut(**client.json()) for client in clients],
                has_next=has_next
            )
        except Exception as e:
            raise GenericExceptions(f"Erro ao buscar clientes: {str(e)}")

    async def get_client(db: AsyncSession, client_id: int):
        """
            Obtem um cliente pelo ID do mesmo na tabela clients

            Args:
                db (AsyncSession): Sessão assincrona do banco de dados.
                client_id (int): ID do cliente a ser buscado.
            Returns:
                ClientsOut: Cliente encontrado com os dados do mesmo.
        """
        try:
            return await ClientsRepository.get_by_id(db, client_id)
        except NoResultFound:
            raise
        except Exception as e:
            raise GenericExceptions(f"Erro ao buscar cliente pelo id -> {e}")

    async def create_client(db: AsyncSession, client_data: ClientsCreate):
        """
            Cria um novo cliente no banco de dados e tambem cria uma wishlist para o mesmo.

            Args:
                db (AsyncSession): Sessão assincrona do banco de dados.
                client_data (ClientsCreate): Dados do cliente a ser criado.
            
            Returns:
                ClientsOut: Cliente criado com os dados do mesmo, incluindo a wishlist.
        """
        try:
            existing_cliente = await ClientsRepository.get_by_email(db, client_data.email)
            if existing_cliente:
                raise DataAlreadyExistsException("Client with this email already exists.")
            client_data = await ClientsRepository.create(db, client_data)
            return client_data
        except DataAlreadyExistsException:
            raise
        except Exception as e:
            raise GenericExceptions(f"Erro ao criar o client -> {e}")

    async def update_client(db: AsyncSession, client_id: int, client_data: ClientsUpdate):
        """
        Atualiza os dados de um cliente existente no banco de dados.

        Args:
            db (AsyncSession): Sessão assincrona do banco de dados.
            client_id (int): ID do cliente a ser atualizado.
            client_data (ClientsUpdate): Dados para atualizar do cliente.
        Returns:
            ClientsOut: Cliente atualizado com os novos dados.
        """
        try:
            return await ClientsRepository.update(db, client_id, client_data)
        except NoResultFound:
            raise
        except DataAlreadyExistsException:
            raise

        except Exception as e:
            raise GenericExceptions(f"Erro ao atualizar o client -> {e}")

    async def delete_cliente(db: AsyncSession, client_id: int):
        """
        Deleta um cliente do banco de dados pelo ID do mesmo.

        Args:
            db (AsyncSession): Sessão assincrona do banco de dados.
            client_id (int): ID do cliente a ser deletado.
        Returns:
            dict: Dicionário indicando se a operação foi bem-sucedida.
        """
        try:
            await ClientsRepository.delete(db, client_id)
            return {"ok": True}
        except NoResultFound:
            raise
        except Exception as e:
            raise GenericExceptions(f"Erro ao deletar o client -> {e}")
