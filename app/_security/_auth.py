from typing import Annotated
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .._constants import AUTH
from .._constants import SESSION_UUID
from .._settings import CONFIG

# Esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def authenticate_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> str:

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
