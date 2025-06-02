from sqlalchemy import Column, Integer, String, DateTime
from src.utils.database.postgres import Base

class Clients(Base):
    """
    Modelo de dados para a tabela de Clientes.

    Atributos:
        id (int): Identificador único do cliente.
        nome (str): Nome do cliente.
        email (str): Email do cliente, deve ser único.
        wishlist_id (str): Identificador da wishlist associada ao cliente.
        
    Métodos:
        __repr__(): Retorna uma representação em string do objeto Cliente.
        json(): Retorna um dicionário com os dados do cliente.
        __str__(): Retorna uma string formatada com os detalhes do cliente.
    """
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


    def __repr__(self):
        return f"<Clients(id={self.id}, nome={self.nome}, email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"
    
    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def __str__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})"
