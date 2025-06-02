from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClientsCreate(BaseModel):
    nome: str
    email: EmailStr

class ClientsUpdate(BaseModel):
    nome: Optional[str] | None = None
    email: Optional[EmailStr] | None = None

class ClientsOut(BaseModel):
    id: int
    nome: Optional[str]
    email: Optional[EmailStr] = None
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ListAllClientsRequest(BaseModel):
    page: int = 1
    page_size: int = 10

class ListAllClientsResponse(BaseModel):
    items: list[ClientsOut]
    has_next: bool

