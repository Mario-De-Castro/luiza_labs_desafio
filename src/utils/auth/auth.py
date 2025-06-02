from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.utils.exceptions.exceptions import UnauthorizedException
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica o token JWT fornecido e extrai o ID do usuario.

    Args:
        token (str): O token JWT a ser verificado.
    Returns:
        str: O ID do usuario extraído do token.
    Raises:
        UnauthorizedException: Se o token for invalido ou não contiver um ID de usuario.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException
        return user_id
    except JWTError:
        raise UnauthorizedException