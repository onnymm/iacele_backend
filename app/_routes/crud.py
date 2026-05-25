from typing import Annotated
from typing import Literal
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from .._api.models import CRUD
from .._constants import ENDPOINT_NAME
from .._constants import ENDPOINT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._security import authenticate_user

# Inicialización de router de transacciones CRUD
router = APIRouter(
    prefix= ROUTER_PREFIX.CRUD,
    tags= [TAG.CRUD],
)

@router.post(
    ENDPOINT_PATH.CRUD.CREATE,
    name= ENDPOINT_NAME.CRUD.CREATE,
    status_code= status.HTTP_201_CREATED,
)
async def _create(
    params: CRUD.Create,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> list[int]:

    # Creación de registros
    created_records = iacele.create(session_uuid, **params.model_dump())

    return created_records

@router.post(
    ENDPOINT_PATH.CRUD.SEARCH,
    name= ENDPOINT_NAME.CRUD.SEARCH,
    status_code= status.HTTP_200_OK,
)
async def _search(
    params: CRUD.Search,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> list[int]:

    # Búsqueda de registros
    records = iacele.search(session_uuid, **params.model_dump())

    return records

@router.post(
    ENDPOINT_PATH.CRUD.READ,
    name= ENDPOINT_NAME.CRUD.READ,
    status_code= status.HTTP_200_OK,
)
async def _read(
    params: CRUD.Read,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> list[dict]:

    # Búsqueda de registros
    records_data = iacele.read(session_uuid, **params.model_dump())

    return records_data

@router.post(
    ENDPOINT_PATH.CRUD.SEARCH_READ,
    name= ENDPOINT_NAME.CRUD.SEARCH_READ,
    status_code= status.HTTP_200_OK,
)
async def _search_read(
    params: CRUD.SearchRead,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> list[dict]:

    # Búsqueda y lectura de registros
    records_data = iacele.search_read(session_uuid, **params.model_dump())

    return records_data

@router.patch(
    ENDPOINT_PATH.CRUD.UPDATE,
    name= ENDPOINT_NAME.CRUD.UPDATE,
    status_code= status.HTTP_200_OK,
)
async def _update(
    params: CRUD.Update,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> Literal[True]:

    # Actualización de registros
    result = iacele.update(session_uuid, **params.model_dump())

    return result

@router.delete(
    ENDPOINT_PATH.CRUD.DELETE,
    name= ENDPOINT_NAME.CRUD.DELETE,
    status_code= status.HTTP_200_OK,
)
async def _delete(
    params: CRUD.Delete,
    session_uuid: Annotated[str, Depends(authenticate_user)],
) -> Literal[True]:

    # Eliminación de registros
    result = iacele.delete(session_uuid, **params.model_dump())

    return result
