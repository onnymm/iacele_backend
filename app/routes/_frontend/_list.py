from fastapi import (
    APIRouter,
    status,
    Depends,
)
from app import iacele
from app.models import Frontend
from app.security import authenticate_user

router = APIRouter(
    prefix= '/list',
    tags= ['Frontend']
)

@router.post(
    '/get',
    name= 'Obtención de lista de registros',
    status_code= status.HTTP_200_OK,
)
async def _get(
    params: Frontend.List.ListRequest,
    user_id: int = Depends(authenticate_user),
) -> Frontend.List.ListResponse:
    """
    ### Registros de lista
    Endpoint para obtener los datos de registros de un modelo, por paginación.

    ----

    #### Uso
    Puede usarse el nombre de un modelo para obtener los datos de todos los
    registros de éste, junto con un número de página y una cantidad máxima de
    registros a retornar:
    ```
    {
        "model_name": "base.users"
        "page": 0,
        "items_per_page": 80
    }
    ```
    Retorno:
    ```js
    {
        "record": [
            {
                "id": 5,
                "name": "Onnymm Azzur",
                "login": "onnymm",
                ...
            },
            ...
        ],
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

    #### Filtro
    Puede utilizarse un filtro para obtener los datos de registros que cumplan con
    criterios específicos:
    ```
    {
        "model_name": "base.users",
        "page": 0,
        "items_per_page": 80,
        "search_criteria": [["active", "=", true]]
    }
    ```

    #### Ordenamiento
    Los resultados pueden ordenarse en base al valor de uno o varios campos. En
    caso de ser un campo, puede especificarse el nombre de éste. En caso de ser un
    ordenamiento anidado, se provee un array de nombres de campo en el orden en el
    que se desea jerarquizar el ordenamiento:
    ```
    {
        "model_name": "base.users",
        "page": 0,
        "items_per_page": 80,
        "sortby": "login"
    }
    ```

    #### Dirección de ordenamiento
    Puede especificarse una dirección de ordenamiento con un valor booleano que
    indica si el ordenamiento es ascendente o no. El valor prestablecido es `true`
    lo que indica que el ordenamiento es ascendente. El valor `false` indica que el
    ordenamiento no es ascendente, es decir, es desendente.
    ```
    {
        "model_name": "base.users",
        "page": 0,
        "items_per_page": 80,
        "sortby": "login",
        "ascending": false
    }
    ```

    ----

    ### Criterio de búsqueda
    La estructura de criterio de búsqueda permite construir filtros tan complejos y
    específicos como sea necesario.

    Primeramente, cada filtro de búsqueda se forma de tres elementos dentro de un array:
    - Nombre del campo en el modelo
    - Operador de comparación
    - Valor

    ```
    ["active", "=", true]
    ```

    Sea uno o muchos filtros, se envuelven dentro de un array padre:
    ```
    [["active", "=", true]]
    ```

    Para usarse más de un filtro se unen por medio de operadores lógicos `&` (AND)
    y `|` (OR) seguidos de los filtros como segundo y tercer lugar:
    ```
    [
        "&",
            ["active", "=", true],
            ["create_date", ">", "2025-08-29"]
    ]
    ```

    Los operadores lógicos disponibles son:
    - `"="`: Igual a
    - `"!="`: Diferente de
    - `">"`: Mayor a
    - `">="`: Mayor o igual a
    - `"<`": Menor que
    - `"<="`: Menor o igual que
    - `"><"`: Entre
    - `"in"`: Está en
    - `"not in"`: No está en
    - `"ilike"`: Contiene
    - `"not ilike"`: No contiene
    - `"~"`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
    - `"~*"`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)
    """

    return iacele.orm.list_.get(
        user_id,
        **params.model_dump(),
    )
