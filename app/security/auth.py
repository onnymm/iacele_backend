from typing import Annotated
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from lylac.errors import ExpiredSessionToken
from app.constants import ERRORS
from app.core import iacele

# Esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def authenticate_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> int:

    try:
        # Obtención de la ID del usuario
        user_id = iacele.core.authenticate(token)

        return user_id
    except ExpiredSessionToken:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= ERRORS.EXPIRED_SESSION,
            headers= {"WWW-Authenticate": "Bearer"}
        )
