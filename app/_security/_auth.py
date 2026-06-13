from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidSignatureError
import jwt
from .._constants import AUTH
from .._constants import EMPTY_SESSION_UUID_VALUE
from .._constants import SESSION_UUID
from .._errors import invalid_token_error
from .._settings import CONFIG

# Esquema OAuth2
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def authenticate_user(
    token: Annotated[str, Depends(_oauth2_scheme)]
) -> str:

    # Si no hay valor de token...
    if token == EMPTY_SESSION_UUID_VALUE:
        # Se lanza error de token inválido
        raise invalid_token_error

    # Intento de verificación de firma
    try:
        # Obtención de la UUID de sesión del usuario
        session_uuid: str = (
            jwt.decode(
                token,
                CONFIG.CRYPT_KEY,
                [AUTH.ALGORYTHM]
            )
            # Obtención del valor de UUID de sessión
            [SESSION_UUID]
        )

    # Si la verificación de firma falla...
    except InvalidSignatureError:
        # Se lanza error de token inválido
        raise invalid_token_error

    return session_uuid
