from fastapi import (
    Body,
    Depends,
    Query,
    APIRouter,
    status,
)
from app.models import UserInDB
from app.security import get_current_user
from app.types import DBTable
from app import db_connection

# Creación del ruteador
router = APIRouter(
    prefix= '/crud',
    tags= ['CRUD']
)

@router.get(
    '/read',
    name= 'Lectura de registros',
    status_code= status.HTTP_200_OK,
)
def _read(
    user: UserInDB = Depends(get_current_user),
    table_name: DBTable = Query(),
    record_ids: int | list[int] = Query(),
    fields: list[str] = Query([])
):
    """
    ## Lectura de registros
    Este endpoint retorna la información de uno o más registros de una tabla
    en la base de datos.

    ### Los parámetros de entrada son:
    - `table_name`: Nombre de la tabla de donde se tomarán los registros.
    - `record_ids`: IDs de los respectivos registros a leer.
    - `fields`: Campos a mostrar. En caso de no ser especificado, se toman todos los
    campos de la tabla de la base de datos.
    - `offset`: Desfase de inicio de primer registro a mostrar.
    - `limit`: Límite de registros retornados por la base de datos.
    """

    return db_connection.read(
        table_name,
        record_ids,
        fields,
        output_format= 'dict'
    )

@router.patch(
    '/update',
    name= "Modificación de un registro",
    status_code= status.HTTP_200_OK,
)
def _update(
    user: UserInDB = Depends(get_current_user),
    record_id: int = Body(),
    table_name: DBTable = Body(),
    data_to_write: dict = Body()
) -> bool:
    """
    ## Actualización de registros
    Este endpoint realiza la actualización de uno o más registros a partir de
    su respectiva ID provista, actualizando uno o más campos con el valor
    provisto. Este método solo sobreescribe un mismo valor por cada campo a
    todos los registros provistos.

    ### Los parámetros de entrada son:
    - `table_name`: Nombre de la tabla en donde se harán los cambios
    - `record_ids`: ID o lista de IDs a actualizar
    - `data`: Diccionario de valores a modificar masivamente
    """

    # Actualización en la base de datos
    db_connection.update(
        table_name,
        record_id,
        data_to_write,
    )

    return True
