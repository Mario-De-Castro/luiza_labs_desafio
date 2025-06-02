from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from src.utils.exceptions.exceptions import DataAlreadyExistsException
from src.utils.models.clients import Clients
from src.utils.schemas.clients_schema import ClientsCreate, ClientsUpdate, ListAllClientsRequest
from src.utils.helpers.helpers_functions import HelperFunctions


class ClientsRepository:

    async def get_all(db: AsyncSession, request: ListAllClientsRequest) -> tuple[list[Clients], bool]:
        """
            Obter todos os clientes de maneira paginada.

            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                request (ListAllClientsRequest): Schema contendo os parâmetros de paginação.
            Returns:
                Tuple(List[Clients], bool): Lista de clientes e um booleano (has_next) indicando se ha mais paginas
        """
        try:
            result = await db.execute(
                select(
                    Clients
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
    
    async def get_by_id(db: AsyncSession, Clients_id: int) -> Clients | None:
        """
            Obter um cliente pelo ID.

            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                Clients_id (int): ID do cliente a ser buscado.
            Returns:
                Clients: Cliente encontrado ou None se não encontrado.
        """
        try: 
            client = await db.get(Clients, Clients_id)

            if not client:
                raise NoResultFound
            
            return client

        except Exception as e:
            raise
    
    async def get_by_email(db: AsyncSession, email: str) -> Clients | None:
        """
            Obter um cliente pelo email.

            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                email (str): Email do cliente a ser buscado.

            Returns:
                Clients: Cliente encontrado ou None se não encontrado.
        """
        try:
            result = await db.execute(select(Clients).where(Clients.email == email))
            return result.scalars().first()
        except Exception as e:
            raise
    
    async def create(db: AsyncSession, Clients_data: ClientsCreate) -> Clients:
        """
        Cria um novo cliente no banco de dados.

        Args:
            db (AsyncSession): Sessão assíncrona do banco de dados.
            Clients_data (ClientsCreate): Dados do cliente a ser criado.

        Returns:
            Clients: Cliente criado com os dados do mesmo.
        """
        try:
            client = Clients(**Clients_data.dict())
            client.created_at = HelperFunctions.get_time().replace(tzinfo=None)
            db.add(client)
            await db.commit()
            await db.refresh(client)
            return client
        except Exception as e:
            raise

    async def update(db: AsyncSession, clients_id: int, clients_data: ClientsUpdate) -> Clients:
        """
        Atualiza os dados de um cliente existente.

        Args:
            db (AsyncSession): Sessão assíncrona do banco de dados.
            clients_id (int): ID do cliente a ser atualizado.
            clients_data (ClientsUpdate): Dados atualizados do cliente.
        
        Returns:
            Clients: Cliente atualizado com os novos dados.
        """
        try:
            client = await db.get(Clients, clients_id)
            if not client:
                raise NoResultFound
            
            if clients_data.email:
                existing_client_by_email = await ClientsRepository.get_by_email(db, clients_data.email)
                if existing_client_by_email:
                    raise DataAlreadyExistsException("Client with this parameter already exists in the base")
            
            data = clients_data.dict(exclude_unset=True)
            for key, value in data.items():
                if value is not None:
                    setattr(client, key, value)
            client.updated_at = HelperFunctions.get_time().replace(tzinfo=None)
            await db.commit()
            await db.refresh(client)
            return client
        except Exception as e:
            raise

    async def delete(db: AsyncSession, Clients_id: int) -> Clients:
        """
        Deleta um cliente pelo ID.

        Args:
            db (AsyncSession): Sessão assíncrona do banco de dados.
            Clients_id (int): ID do cliente a ser deletado.
        
        returns:
            Clients: Cliente deletado com os dados do mesmo.
        """
        try:
            client = await db.get(Clients, Clients_id)
            if not client:
                raise NoResultFound
            await db.delete(client)
            await db.commit()
            return client
        except Exception as e:
            raise
