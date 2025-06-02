from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.database.postgres import get_db
from src.utils.schemas.clients_schema import (
    ClientsOut,
    ClientsCreate,
    ClientsUpdate,
    ListAllClientsRequest,
    ListAllClientsResponse
)
from src.api.services.clients_services import ClientsService

from src.utils.helpers.helpers_functions import HelperFunctions
from src.utils.auth.auth import verify_token

router = APIRouter(prefix="/clients", tags=["Clientes"])

logger = HelperFunctions.get_logger()

@router.get("/", response_model=ListAllClientsResponse)
async def list_all_clients(
    request: ListAllClientsRequest = Depends(),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
        Lista todos os clientes de maneira paginada.

        **Parâmetros:**
        - `page` (int): Numero da página a ser consultada (Padrão e 1)
        - `page_size` (int): Tamanho da página (Padrão e 10)

        **Retorna:**
        - Uma dicionario com 2 campos sendo eles items e has_next:
            - `items`: Lista de clientes paginada.
            - `has_next`: Booleano indicando se ha mais paginas disponiveis.
    """
    return await ClientsService.get_all_clients(db, request, logger)

@router.get("/{client_id}", response_model=ClientsOut)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
    Obtém um cliente pelo ID.

    **Parâmetros:**
    - `client_id` (int): ID do cliente a ser buscado.
    **Retorna:**
    - Um objeto `ClientsOut` com os dados do cliente encontrado.
    """
    return await ClientsService.get_client(db, client_id)

@router.post("/", response_model=ClientsOut)
async def create_client(
    cliente: ClientsCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
    Cria um novo cliente no banco de dados.

    **Payload:**
    dE parametros para criar o cliente é esperado um JSON contendo os seguintes campos:
        - `nome` (str): Nome do cliente.
        - `email` (str): Email do cliente.

    **Retorna:**
    - Um dicionario com os dados do cliente criado, incluindo o ID gerado.
    
    """
    return await ClientsService.create_client(db, cliente)

@router.put("/{client_id}", response_model=ClientsOut)
async def update_client(
    client_id: int,
    cliente: ClientsUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
    Atualiza os dados de um cliente existente.

    **Parâmetros:**
        - `client_id` (int): ID do cliente a ser atualizado.

    **Payload:**
        NEsse endpoint ee esperado um JSON contendo os seguintes campos:
        - `nome` (str): Nome do cliente (opcional).
        - `email` (str): Email do cliente (opcional).
    
    **Retorna:**
    - Um dicionario com os dados do cliente atualizado.
    """
    return await ClientsService.update_client(db, client_id, cliente)

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """
    Deleta um cliente pelo ID.

    **Parâmetros:**
    - `client_id` (int): ID do cliente a ser deletado.

    **Retorna:**
    - Um dicionario com a mensagem de sucesso da exclusão do cliente.
    """
    return await ClientsService.delete_cliente(db, client_id)
