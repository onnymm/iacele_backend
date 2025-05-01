from fastapi import (
    Depends,
    Query,
    APIRouter,
    status,
)
from app.models import (
    UserInDB,
    request,
    response,
)
from app.security import get_current_user
from app import db_connection

# Creación del ruteador
router = APIRouter(
    prefix= '/crud',
    tags= ['CRUD']
)

@router.post(
    '/create',
    name= 'Creación de registros',
    status_code= status.HTTP_201_CREATED,
)
async def _create(
    params: request.create,
    _: UserInDB = Depends(get_current_user),
) -> bool:
    """
    ## Creación de registros
    Este endpoint permite la creación de uno o más registros en una tabla de la
    base de datos.

    ### Los parámetros de entrada son:
    - `tableName`: Nombre de la tabla de donde se crearán los registros.
    - `data`: Diccionario o lista de diccionarios de atributos de los registros
    a crear.
    """

    return db_connection.create(
        params.table,
        params.data,
    )

@router.get(
    '/read',
    name= 'Lectura de registros',
    status_code= status.HTTP_200_OK,
)
async def _read(
    params: request.read = Query(),
    _: UserInDB = Depends(get_current_user),
) -> response.records:
    """
    ## Lectura de registros
    Este endpoint permite la lectura de uno o más registros de una tabla en la
    base de datos.

    ### Los parámetros de entrada son:
    - `tableName`: Nombre de la tabla de donde se tomarán los registros.
    - `recordIds`: IDs de los respectivos registros a leer.
    - `fields`: Campos a mostrar. En caso de no ser especificado, se toman todos los
    campos de la tabla de la base de datos (opcional).
    - `offset`: Desfase de inicio de primer registro a mostrar (opcional).
    - `limit`: Límite de registros retornados por la base de datos (opcional).
    """

    # Lectura de registros
    data = db_connection.read(
        params.table,
        params.record_ids,
        params.fields,
        params.sortby,
        params.ascending,
        output_format= 'dict'
    )

    # Retorno de información
    return data

@router.post(
    '/search_read',
    name= 'Búsqueda de registros',
    status_code= status.HTTP_200_OK,
)
async def _search_read(
    params: request.search_read,
    _: UserInDB = Depends(get_current_user),
) -> response.search_read:
    """
    ## Búsqueda y visualización de registros
    Este endpoint permite la búsqueda y visualización de registros en una tabla
    de la base de datos.

    ### Parámetros de entrada
    - `tableName`: Nombre de la tabla en la base de datos.
    - `searchCriteria`: Criterio de búsqueda (opcional).
    - `fields`: Campos específicos a visualizar en los resultados arrojados
    (opcional).
    - `offset`: Desfase de índice de registros a visualizar (opcional).
    - `limit`: Cantidad máxima de registros a visualizar (opcional).
    - `sortby`: Campo o campos como criterio de ordenamiento de registros
    (opcional).
    - `ascending`: Dirección de ordenamiento ascendente (opcional).

    ### Estructura de criterio de búsqueda
    La estructura del criterio de búsqueda consiste en una lista de tuplas de 3 valores, mejor
    conocidas como tripletas. Cada una de estas tripletas consiste en 3 diferentes parámetros:
    1. Nombre del campo de la tabla.
    2. Operador de comparación.
    3. Valor de comparación.

    Algunos ejemplos de tripletas son:
    ```py
    ('id', '=', 5)
    # ID es igual a 5
    ('amount', '>', 500)
    # "amount" es mayor a 500
    ('name', 'ilike', 'as')
    # "name" contiene "as"
    ```

    Los operadores de comparación disponibles son:
    - `'='`: Igual a
    - `'!='`: Diferente de
    - `'>'`: Mayor a
    - `'>='`: Mayor o igual a
    - `'<`': Menor que
    - `'<='`: Menor o igual que
    - `'><'`: Entre
    - `'in'`: Está en
    - `'not in'`: No está en
    - `'ilike'`: Contiene
    - `'not ilike'`: No contiene
    - `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
    - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)

    Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
    Unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
    primera posición:
    ```py
    ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
    # "amount" es mayor a 500 y "name" contiene "as"
    ['|', ('id', '=', 5), ('state', '=', 'posted')]
    # "id" es igual a 5 o "state" es igual a "posted"
    ```

    Los operadores lógicos disponibles son:
    - `'&'`: AND
    - `'|'`: OR
    """

    # Búsqueda y lectura de los registros
    data = db_connection.search_read(
        params.table,
        params.search_criteria,
        params.fields,
        params.offset,
        params.limit,
        params.sortby,
        params.ascending,
    )

    # Conteo de resultados
    count = db_connection.search_count(
        params.table,
        params.search_criteria,
    )

    # Retorno de la información
    return {
        'data': data,
        'count': count,
    }

@router.patch(
    '/update',
    name= "Modificación de un registro",
    status_code= status.HTTP_200_OK,
)
async def _update(
    params: request.update,
    _: UserInDB = Depends(get_current_user),
) -> bool:
    """
    ## Actualización de registros
    Este endpoint realiza la actualización de uno o más registros a partir de
    su respectiva ID provista, actualizando uno o más campos con el valor
    provisto. Este método solo sobreescribe un mismo valor por cada campo a
    todos los registros provistos.

    ### Los parámetros de entrada son:
    - `tableName`: Nombre de la tabla en donde se harán los cambios.
    - `recordIds`: ID o lista de IDs a actualizar.
    - `data`: Diccionario de valores a modificar masivamente.
    """

    # Actualización en la base de datos
    db_connection.update(
        params.table,
        params.record_id,
        params.data_to_write,
    )

    return True

@router.delete(
    '/delete',
    name= 'Eliminación de registros',
    status_code= status.HTTP_200_OK,
)
async def _delete(
    params: request.delete,
    _: UserInDB = Depends(get_current_user)
):
    """
    ## Eliminación de registros
    Este endpoint permite la eliminación de uno o más registros en una tabla de
    la base de datos.

    ### Parámetros de entrada
    - `tableName`: Nombre de la tabla de donde se eliminarán los registros.
    - `recordIds`: ID o lista de IDs de los registros a eliminar.
    """

    # Eliminación de los registros en la base de datos
    db_connection.delete(params.table, params.record_ids)

    return True
