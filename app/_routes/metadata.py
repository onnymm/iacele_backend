from typing import Annotated
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from .._api.models import Metadata
from .._constants import ENDPOINT_NAME
from .._constants import ENDPOINT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._operations import operation_get_fields_metadata
from .._security import authenticate_user

# Inicialización de router de metadatos
router = APIRouter(
    prefix= ROUTER_PREFIX.METADATA,
    tags= [TAG.METADATA],
)

@router.post(
    ENDPOINT_PATH.METADATA.FIELDS,
    name= ENDPOINT_NAME.METADATA.FIELDS,
    status_code= status.HTTP_200_OK,
)
async def _get_fields_metadata(
    params: Metadata.Fields,
    session_uuid: Annotated[str, Depends(authenticate_user)],
):

    # Ejecución de transacción
    fields_metadata = iacele.execute_transaction(
        session_uuid,
        lambda ctx: operation_get_fields_metadata(ctx, params),
    )

    return fields_metadata
