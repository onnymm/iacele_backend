from typing import Annotated
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from .._api.models import TokenData
from .._constants import AUTH
from .._constants import ENDPOINT_NAME
from .._constants import ROOT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._settings import CONFIG
from .._constants import SESSION_UUID

# Inicialización de router de obtención de token
router = APIRouter(
    prefix= ROUTER_PREFIX.TOKEN,
    tags= [TAG.AUTH],
)

@router.post(
    ROOT_PATH,
    name= ENDPOINT_NAME.AUTH.TOKEN,
    status_code= status.HTTP_200_OK,
)
async def _login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenData:

    # Obtención de valores
    user_login = form_data.username
    password = form_data.password

    # Obtención de UUID de sesión
    session_uuid = iacele.login(user_login, password)
    # Construcción de datos a codificar
    data_to_encode = {SESSION_UUID: session_uuid}
    # Creación de token de acceso
    access_token = jwt.encode(data_to_encode, CONFIG.CRYPT_KEY, AUTH.ALGORYTHM)

    # Inicialización de modelo a retornar
    token_data = TokenData(access_token= access_token, token_type= AUTH.TOKEN_TYPE)

    return token_data
