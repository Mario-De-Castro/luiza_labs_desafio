from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

#DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    """
    Cria uma sessão de banco de dados assíncrona para ser usada nas rotas.
    Esta função é um gerador que fornece uma sessão de banco de dados para cada requisição,
    garantindo que a sessão seja fechada após o uso.
    
    Yields:
        AsyncSession: Uma sessão de banco de dados assíncrona.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos modelos.
    Esta função deve ser chamada uma vez durante a inicialização da aplicação para garantir
    que todas as tabelas necessárias estejam criadas no banco de dados.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
