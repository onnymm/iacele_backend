from typing import Literal
from pydantic import BaseModel
from fastapi import (
    APIRouter,
    status,
    Depends,
)
from app.constants import TAG
from app.core import iacele
from app.models import Server
from app.security import authenticate_user

class Action(BaseModel):
    model_name: str
    record_id: int
    action: str

router = APIRouter(
    prefix= '/server',
    tags= [TAG.SERVER],
)

@router.post(
    '/action',
    name= 'Ejecutar acción de servidor',
    status_code= status.HTTP_200_OK,
)
def _action(
    params: Server.Action,
    user_id: int = Depends(authenticate_user),
) -> Literal[True]:
    """
    ### Acción de servidor
    Endpoint para ejecutar una acción de servidor sobre un registro de un modelo de
    la base de datos.

    Uso:
    ```js
    {
        "model_name": "base.users",
        "record_id": 1,
        "action": "reset_password"
    }
    ```
    """

    # Se ejecuta la acción en el servidor
    iacele.core.action(
        user_id,
        params.model_name,
        params.action,
        params.record_id,
    )

    return True
