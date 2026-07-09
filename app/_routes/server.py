from typing import Annotated
from typing import Literal
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from .._constants import ENDPOINT_NAME
from .._constants import ENDPOINT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._security import authenticate_user
from .._api.models import Server

# Inicialización de router de procesos de servidor
router = APIRouter(
    prefix= ROUTER_PREFIX.SERVER,
    tags= [TAG.SERVER],
)

@router.post(
    ENDPOINT_PATH.SERVER.ACTION,
    name= ENDPOINT_NAME.SERVER.ACTION,
    status_code= status.HTTP_200_OK,
)
async def _action(
    params: Server.Action,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> Literal[True]:

    # Ejecución de la acción
    iacele.action(session_uuid, **params.model_dump())

    return True

@router.post(
    ENDPOINT_PATH.SERVER.TASK,
    name= ENDPOINT_NAME.SERVER.TASK,
    status_code= status.HTTP_200_OK,
)
async def _task(
    params: Server.Tast,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> Literal[True]:

    # Ejecución de tarea de servidor
    iacele.task(session_uuid, **params.model_dump())

    return True
