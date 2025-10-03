from typing import Annotated
from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from app.constants import TAG
from app.models import Token
from ..core import iacele

router = APIRouter(
    prefix= '/token',
    tags= [TAG.AUTH],
)

@router.post(
    '/',
    name= 'Obtención de token',
    status_code= status.HTTP_200_OK,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    ### Obtención de token de autenticación de usuario
    Inicio de sesión y obtención de token.
    """

    # Obtención del token de usuario
    user_token = iacele.core.login(form_data.username, form_data.password)

    # Retorno del token
    return Token(access_token= user_token, token_type= "bearer")
