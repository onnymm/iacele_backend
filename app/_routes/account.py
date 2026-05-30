from typing import Annotated
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from .._constants import ENDPOINT_NAME
from .._constants import ENDPOINT_PATH
from .._constants import PRESET_PROFILE_FIELDS
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
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

    # Obtención de los datos del usuario
    my_user_data = iacele.me(
        session_uuid,
        PRESET_PROFILE_FIELDS,
    )

    return my_user_data
