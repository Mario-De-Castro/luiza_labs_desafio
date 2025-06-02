from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.utils.database.postgres import init_db
from src.api.routes.client_route import router as cliente_router
from src.api.routes.wishlist_route import router as wishlist_router
from src.api.routes.auth_route import router as auth_router


from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError


from src.utils.exceptions.exceptions import (
    SchemaValidationError,
    GenericExceptions,
    UnauthorizedException,
    DataAlreadyExistsException
)
from src.utils.exceptions.api_exceptions import (
    no_result_found_handler,
    integrity_error_handler,
    generic_exception_handler,
    schema_validate_handler,
    unauthorized_exception_handler,
    data_already_exists_handler
)

origins = [
    "http://localhost",
    "http://localhost:3000"
]

def configure_routers(_app: FastAPI):
    """
    Configura as rotas principais da API e inclui os roteadores de endpoints.

    Args:
        _app (FastAPI): Instância do aplicativo FastAPI onde os roteadores serão registrados.
    """
    _app.include_router(auth_router, prefix='/api/v1')
    _app.include_router(cliente_router, prefix='/api/v1')
    _app.include_router(wishlist_router, prefix='/api/v1')

def configure_middlewares(_app: FastAPI):
    """
    Configura middlewares para a aplicação, incluindo o middleware de CORS.

    Args:
        _app (FastAPI): Instância do aplicativo FastAPI onde o middleware será registrado.
    """
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_exception_handlers(_app: FastAPI):
    """
    Configura os manipuladores de exceções personalizados para a API.
    
    Além disso, configura um manipulador para a exceção RequestValidationError, que personaliza
    a resposta de erro de validação de requisições (erro no payload enviado).

    Args:
        _app (FastAPI): Instância do aplicativo FastAPI onde os manipuladores de exceção serão registrados.
    """
    _app.add_exception_handler(NoResultFound, no_result_found_handler)
    _app.add_exception_handler(IntegrityError, integrity_error_handler)
    _app.add_exception_handler(GenericExceptions, generic_exception_handler)
    _app.add_exception_handler(SchemaValidationError, schema_validate_handler)
    _app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    _app.add_exception_handler(DataAlreadyExistsException, data_already_exists_handler)


    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Manipulador personalizado para erros de validação de requisição.

        Este manipulador captura erros de validação de payload e formata as mensagens de erro 
        de uma maneira mais amigável, informando quais campos estão ausentes ou malformados 
        no corpo da requisição.

        Args:
            request (Request): A requisição que causou o erro.
            exc (RequestValidationError): A exceção gerada pela falha de validação.

        Returns:
            JSONResponse: Resposta JSON contendo as mensagens de erro de validação.
        """
        errors = exc.errors()
        custom_errors = []

        for err in errors:
            loc = " -> ".join([str(location) for location in err['loc'][1:]])
            msg = "Error in the sent payload. Check your JSON" if type(err['loc'][1]) == int else f"Field not provided or invalid: {loc}"
            custom_errors.append(msg)

        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({"message": custom_errors})
        )

def configure_database(_app: FastAPI):
    """
    Configura a conexão com o banco de dados e inicializa a base de dados.

    Args:
        _app (FastAPI): Instância do aplicativo FastAPI onde a conexão com o banco de dados será configurada.
    """
    @_app.on_event("startup")
    async def on_startup():
        await init_db()


def configure_health_check_endpoint(_app: FastAPI):

    @_app.get('/health', status_code=200)
    async def health_check():
        """
        Endpoint para verificar se a API está funcionando corretamente.

        Returns:
            dict: Dicionário com status ok.
        """
        return {"status": "ok"}

def create_app():
    """
    Cria e configura a instância principal do aplicativo FastAPI.

    Returns:
        FastAPI: A instância configurada do aplicativo FastAPI.
    """
    _app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
    configure_exception_handlers(_app)
    configure_middlewares(_app)
    configure_routers(_app)
    configure_database(_app)
    configure_health_check_endpoint(_app)

    return _app

app = create_app()
