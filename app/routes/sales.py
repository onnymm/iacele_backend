from fastapi import APIRouter, Depends, status, Body
from app import db_connection
from app.security import get_current_user
from app.constants import (
    tags,
)
from app.models import (
    BaseDataRequest,
    UserInDB,
)
from dml_manager import DMLManager, CriteriaStructure

router = APIRouter(
    prefix= '/sales',
    tags= [tags.sales],
    dependencies= [
        Depends(get_current_user),
    ],
)

@router.post(
    '/commissions',
    name= 'Visualización de comisiones',
    status_code= status.HTTP_200_OK,
)
async def _commissions(
    user: UserInDB = Depends(get_current_user),
    view_params: BaseDataRequest = Body(),
):
    """
    ## Visualización de comisiones

    En este endpoint se pueden visualizar las comisiones.

    ### Estructura de criterio de búsqueda
    La estructura del criterio de búsqueda consiste en una lista de tuplas de 3 valores, mejor
    conocidas como tripletas. Cada una de estas tripletas consiste en 3 diferentes parámetros:
    1. Nombre del campo de la tabla
    2. Operador de comparación
    3. Valor de comparación

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

    return data_for_table(
        'commissions.line',
        view_params,
        [('salesperson_id', '=', user.odoo_id)]
    )

def data_for_table(
    table_name: str,
    view_params: BaseDataRequest,
    base_criteria: CriteriaStructure = [],
) -> list[dict]:

    # Creación del criterio de búsqueda completo
    search_criteria = DMLManager.and_(
        view_params.search_criteria,
        base_criteria
    )

    data = db_connection.search_read(
        table_name,
        search_criteria,
        # fields= ['id'],
        offset= view_params.items_per_page * view_params.page,
        limit= view_params.items_per_page,
        sortby= view_params.sortby,
        ascending= view_params.ascending,
        output_format= 'dict',
    )

    count = db_connection.search_count(
        table_name,
        search_criteria,
    )

    return {
        'data': data,
        'count': count,
    }
