from sqlalchemy import Column, Index, Integer, String, DateTime
from src.utils.database.postgres import Base

class Wishlist(Base):
    """"
    Modelo de dados para a tabela de Wishlist.
   
    Atributos:
        wishlist_id (int): Identificador único da wishlist.
        client_id (int): Identificador do cliente associado à wishlist.
        product_id (int): Identificador do produto na wishlist.
        product_info (str): Informações sobre o produto.
        created_at (DateTime): Data e hora de criação da wishlist.

    Métodos:
        __repr__(): Retorna uma representação em string do objeto Wishlist.
        json(): Retorna um dicionário com os dados da wishlist.
        __str__(): Retorna uma string formatada com os detalhes da wishlist.
    """


    __tablename__ = "wishlist"

    wishlist_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, index=True)
    product_info = Column(String)
    created_at = Column(DateTime)

    __table_args__ = (
        Index('idx_wishlist_client_product', 'client_id', 'product_id'),
    )


    def __repr__(self):
        return f"<Wishlist(wishlist_id={self.wishlist_id}," \
               f"client_id={self.client_id},"\
               f"product_id={self.product_id},"\
               f"product_info={self.product_info},"\
               f"created_at={self.created_at})>"
    
    def json(self):
        return {
            "wishlist_id": self.wishlist_id,
            "client_id": self.client_id,
            "product_id": self.product_id,
            "product_info": self.product_info,
            "created_at": self.created_at
        }
    
    def __str__(self):
        return f"Wishlist(wishlist_id={self.wishlist_id}, client_id={self.client_id}, product_id={self.product_id})"
