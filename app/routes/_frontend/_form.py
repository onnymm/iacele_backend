from fastapi import (
    APIRouter,
    status,
    Depends,
)
from pydantic import BaseModel
from app import iacele
from app.models import Frontend
from app.security import authenticate_user
from app.constants import TAG
from app.types import (
    FieldMetadata,
    SelectionValue,
)

class FormRecord(BaseModel):
    record: dict
    fields: list[FieldMetadata[SelectionValue]]

router = APIRouter(
    prefix= '/form',
    tags= [TAG.FRONTEND],
)

@router.post(
    '/get',
    name= 'Obtención de registro para formulario',
    status_code= status.HTTP_200_OK,
)
async def _get(
    params: Frontend.Form.FormRequest,
    user_id: int = Depends(authenticate_user),
) -> Frontend.Form.FormResponse:
    """
    ### Registro de formulario
    Endpoint para obtener los datos de un registro de un modelo a partir de una ID.

    ----

    #### Uso
    ```
    {
        "model_name": "base.users",
        "record_id": 5
    }
    ```
    Retorno:
    ```js
    {
        "record": {
            "id": 5,
            "name": "Onnymm Azzur",
            "login": "onnymm",
            ...
        },
        "fields": {
            [
                {
                    id: 7,
                    name: "create_uid",
                    label: "Creado por",
                    ttype: "many2one",
                    help_info: null,
                    ...
                },
                ...
            ]
        }
    }
    ```
    """

    return iacele.orm.form.get(
        user_id,
        **params.model_dump(),
    )
