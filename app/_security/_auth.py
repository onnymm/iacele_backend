from typing import Annotated
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from .._constants import AUTH
from .._constants import EMPTY_SESSION_UUID_VALUE
from .._constants import SESSION_UUID
from .._settings import CONFIG

# Instancia de token de autenticación inválido
_invalid_token_error = HTTPException(
    status_code= status.HTTP_403_FORBIDDEN,
    detail= 'Token inválido'
)

# Esquema OAuth2
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def authenticate_user(
    token: Annotated[str, Depends(_oauth2_scheme)]
) -> str:

    # Si no hay valor de token...
    if token == EMPTY_SESSION_UUID_VALUE:
        # Se lanza error
        raise _invalid_token_error

    # Obtención de la UUID de sesión del usuario
    session_uuid = (
        jwt.decode(
            token,
            CONFIG.CRYPT_KEY,
            [AUTH.ALGORYTHM]
        )
        # Obtención del valor de UUID de sessión
        [SESSION_UUID]
    )

    return session_uuid
