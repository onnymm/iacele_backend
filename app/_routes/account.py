from typing import Annotated
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from lylac.errors import InvalidSessionUUIDError
from .._constants import ENDPOINT_NAME
from .._constants import ENDPOINT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._errors import invalid_token_error
from .._operations import me
from .._security import authenticate_user

# Inicialización de router de transacciones de cuenta
router = APIRouter(
    prefix= ROUTER_PREFIX.ACCOUNT,
    tags= [TAG.ACCOUNT],
)

@router.get(
    ENDPOINT_PATH.ACCOUNT.ME,
    name= ENDPOINT_NAME.ACCOUNT.ME,
    status_code= status.HTTP_200_OK,
)
async def _me(
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> dict:

    # Intento de obtención de los datos de usuario
    try:
        # Obtención de los datos del usuario de la sesión
        my_user_data = iacele.execute_transaction(session_uuid, me)
    # Si la UUID de sesión es inválida...
    except InvalidSessionUUIDError:
        # Se arroja error
        raise invalid_token_error

    return my_user_data
