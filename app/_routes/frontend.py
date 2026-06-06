from typing import Annotated
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
from .._operations import tree_search_read

# Inicialización de router de transacciones CRUD
router = APIRouter(
    prefix= ROUTER_PREFIX.FRONTEND,
    tags= [TAG.FRONTEND],
)

@router.post(
    ENDPOINT_PATH.FRONTEND.TREE,
    name= ENDPOINT_NAME.FRONTEND.TREE,
    status_code= status.HTTP_200_OK,
)
def _tree(
    params: CRUD.SearchRead,
    session_uuid: Annotated[str, Depends(authenticate_user)],
):

    # Obtención de registros
    result = iacele.execute_transaction(
        session_uuid,
        lambda ctx: tree_search_read(ctx, params)
    )

    return result
