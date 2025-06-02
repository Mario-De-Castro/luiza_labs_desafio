from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime
from src.utils.exceptions.exceptions import UnauthorizedException

from src.utils.auth.auth import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Endpoint para autenticação de usuario e geração de token JWT.
        
        **Parâmetros:**
        - `form_data`: Dados do formulario de autenticação, incluindo `username` e `password`.

        **Retorna:**
        - Um dicionário contendo o token de acesso e o tipo de token.
        - `access_token`: Token JWT gerado para o usuário autenticado.
        - `token_type`: Tipo do token (geralmente "bearer").

        **Exceções:**
        - `UnauthorizedException`: Se as credenciais fornecidas não forem validas.
    """
    if form_data.username != "admin" or form_data.password != "admin":
        raise UnauthorizedException
    to_encode = {"sub": form_data.username, "exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}