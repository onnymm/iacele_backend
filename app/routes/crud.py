from fastapi import (
    APIRouter,
    status,
    Depends,
)
from typing import Literal
from app.core import iacele
from app.security import authenticate_user
from app.models import CRUD
from app.constants import TAG

router = APIRouter(
    prefix= '/crud',
    tags= [TAG.CRUD]
)

@router.post(
    '/create',
    name= 'Creación de uno o más registros',
    status_code= status.HTTP_201_CREATED,
)
async def _create(
    params: CRUD.Create,
    user_id: int = Depends(authenticate_user),
) -> list[int]:
    """
    ### Creación de registros
    Endpoint para creación de uno o muchos registros a partir del nombre de un
    modelo proporcionado y un diccionario (un único registro) o una lista de
    diccionarios (muchos registros).

    Ejemplo de esquema:
    ```js
    {
        "model_name": "base.users",
        "data": {
            'login': 'onnymm',
            'name': 'Onnymm Azzur',
        }
    }
    ```

    El retorno es un array de IDs de los registros creados.
    """

    # Creación de registros y obtención de sus IDs
    created_ids = iacele.core.create(
        user_id,
        **params.model_dump(),
    )

    return created_ids

@router.post(
    '/search',
    name= 'Búsqueda de registros',
    status_code= status.HTTP_200_OK,
)
async def _search(
    params: CRUD.Search,
    user_id: int = Depends(authenticate_user),
) -> list[int]:
    """
    ### Búsqueda de registros
    Endpoint para buscar y obtener un array de IDs de todos los registros de un
    modelo o específicamente los registros de éste que cumplan con una condición de
    búsqueda provista. También es posible segmentar desde un índice inicial de
    desfase y/o un límite de cantidad de IDs de registros retornada.
    
    ----

    #### Uso
    Puede usarse simplemente el nombre de un modelo para obtener las IDs de todos
    los registros de éste:
    ```
    {
        "model_name": "base.users"
    }
    ```
    Retorno:
    ```
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ```

    #### Filtro
    Puede utilizarse un filtro para obtener las IDs de registros que cumplan con
    criterios específicos:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]]
    }
    ```
    Retorno:
    ```
    [1, 2, 4, 6, 8, 9, 10]
    ```

    #### Límite de registros
    También puede especificarse una cantidad de IDs de registros a obtener, por
    ejemplo, los 3 primeros elementos:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]],
        "limit": 3
    }
    ```
    Retorno:
    ```
    [2, 3, 5]
    ```

    #### Desfase de resultados
    También puede usarse un parámetro de desfase de registros, ideal para
    paginación:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]],
        "limit": 3,
        "offset": 2,
    }
    ```
    Retorno:
    ```
    [5, 6, 8]
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
    - `"<"`: Menor que
    - `"<="`: Menor o igual que
    - `"><"`: Entre
    - `"in"`: Está en
    - `"not in"`: No está en
    - `"ilike"`: Contiene
    - `"not ilike"`: No contiene
    - `"~"`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
    - `"~*"`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)
    """

    # Búsqueda de registros
    data = iacele.core.search(
        user_id,
        **params.model_dump(),
    )

    return data

@router.post(
    '/read',
    name= 'Lectura de registros',
    status_code= status.HTTP_200_OK,
)
async def _read(
    params: CRUD.Read,
    user_id: int = Depends(authenticate_user),
) -> list[dict]:
    """
    ### Lectura de registros
    Endpoint para obtener los datos de registros de un modelo, a partir de una ID o
    un array de IDs provistas. También es posible realizar un ordenamiento a partir
    de un campo del modelo y una dirección ascendente o descendente así como
    especificar los campos específicos a leer. De no especificarse los campos a
    leer, se obtienen los datos de todos los campos del modelo, por registro.

    ----

    #### Uso
    ```
    {
        "model_name": "base.users",
        "record_ids": [1, 2, 3]
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 1,
            "name": "iaCele",
            "login": "iacele",
            "active": false,
            ...
        },
        {...},
        ...
    ]
    ```

    #### Ordenamiento
    Los resultados pueden ordenarse en base al valor de uno o varios campos. En
    caso de ser un campo, puede especificarse el nombre de éste. En caso de ser un
    ordenamiento anidado, se provee un array de nombres de campo en el orden en el
    que se desea jerarquizar el ordenamiento:
    ```
    {
        "model_name": "base.users",
        "record_ids": [1, 2, 3],
        "sortby": "login"
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 3,
            "login": "lumii",
            ...
        },
        {
            "id": 1,
            "login": "iacele",
            ...
        },
        {
            "id": 2,
            "login": "onnymm",
            ...
        }
    ]
    ```

    #### Dirección de ordenamiento
    Puede especificarse una dirección de ordenamiento con un valor booleano que
    indica si el ordenamiento es ascendente o no. El valor prestablecido es `true`
    lo que indica que el ordenamiento es ascendente. El valor `false` indica que el
    ordenamiento no es ascendente, es decir, es desendente.
    ```
    {
        "model_name": "base.users",
        "record_ids": [1, 2, 3],
        "sortby": "login",
        "ascending": false,
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 2,
            "login": "onnymm",
            ...
        },
        {
            "id": 1,
            "login": "iacele",
            ...
        },
        {
            "id": 3,
            "login": "lumii",
            ...
        }
    ]
    ```

    #### Campos específicos
    Puede especificarse qué campos se desean consultar. Se usa un array de nombres
    de campo disponibles en el modelo. De no proporcionarse un valor se obtienen
    los datos de todos los campos existentes en el modelo. El campo de ID siempre
    estará disponible, se especifique o no:

    ```
    {
        "model_name": "base.users",
        "record_ids": [1, 2, 3]
        "fields": ["name", "active"]
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 1,
            "name": "iaCele",
            "active": false
        },
        {
            "id": 2,
            "name": "Onnymm Azzur",
            "active": true
        },
        {
            "id": 3,
            "name": "Lumii Mynx",
            "active": true
        }
    ]
    ```
    """

    # Lectura de datos
    data = iacele.core.read(
        user_id,
        **params.model_dump(),
    )

    return data

@router.post(
    '/search_read',
    name= 'Búsqueda y lectura de registros',
    status_code= status.HTTP_200_OK,
)
async def _search_read(
    params: CRUD.SearchRead,
    user_id: int = Depends(authenticate_user),
) -> list[dict]:
    """
    ### Búsqueda de registros
    Endpoint para buscar y obtener un array de datos de todos los registros de un
    modelo o específicamente los registros de éste que cumplan con una condición de
    búsqueda provista. También es posible realizar un ordenamiento a partir
    de un campo del modelo y una dirección ascendente o descendente así como
    especificar los campos específicos a leer así como segmentar desde un índice
    inicial de desfase y/o un límite de cantidad de datos de registros retornada.

    ----

    #### Uso
    Puede usarse simplemente el nombre de un modelo para obtener los datos de todos
    los registros de éste:
    ```
    {
        "model_name": "base.users"
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 1,
            "name": "iaCele",
            "login": "iacele",
            "active": false,
            ...
        },
        {...},
        ...
    ]
    ```

    #### Filtro
    Puede utilizarse un filtro para obtener los datos de registros que cumplan con
    criterios específicos:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]]
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 2,
            "name": "Onnymm Azzur",
            "active": true,
            ...
        },
        {
            "id": 3,
            "name": "Lumii Mynx",
            "active": true,
            ...
        },
        {
            "id": 4,
            "name": "Pygriio",
            "active": true,
            ...
        },
        ...
    ]
    ```

    #### Límite de registros
    También puede especificarse una cantidad de registros a obtener, por ejemplo,
    los 3 primeros elementos:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]],
        "limit": 2
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 2,
            "name": "Onnymm Azzur",
            "active": true,
            ...
        },
        {
            "id": 3,
            "name": "Lumii Mynx",
            "active": true,
            ...
        },
    ]
    ```

    #### Desfase de resultados
    También puede usarse un parámetro de desfase de registros, ideal para
    paginación:
    ```
    {
        "model_name": "base.users",
        "search_criteria": [["active", "=", true]],
        "limit": 2,
        "offset": 3,
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 6,
            "name": "Denkulu Marzink",
            "active": true,
            ...
        },
        {
            "id": 8,
            "name": "Zuynie Spyrx",
            "active": true,
            ...
        },
    ]
    ```

    #### Ordenamiento
    Los resultados pueden ordenarse en base al valor de uno o varios campos. En
    caso de ser un campo, puede especificarse el nombre de éste. En caso de ser un
    ordenamiento anidado, se provee un array de nombres de campo en el orden en el
    que se desea jerarquizar el ordenamiento:
    ```
    {
        "model_name": "base.users",
        "sortby": "login"
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 7,
            "login": "arcimx",
            ...
        },
        {
            "id": 6,
            "login": "denkulu",
            ...
        },
        {
            "id": 3,
            "login": "lumii",
            ...
        }
    ]
    ```

    #### Dirección de ordenamiento
    Puede especificarse una dirección de ordenamiento con un valor booleano que
    indica si el ordenamiento es ascendente o no. El valor prestablecido es `true`
    lo que indica que el ordenamiento es ascendente. El valor `false` indica que el
    ordenamiento no es ascendente, es decir, es desendente.
    ```
    {
        "model_name": "base.users",
        "sortby": "login",
        "ascending": false
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 8,
            "login": "zuynie",
            ...
        },
        {
            "id": 10,
            "login": "poryoku",
            ...
        },
        {
            "id": 2,
            "login": "onnymm",
            ...
        }
    ]
    ```

    #### Campos específicos
    Puede especificarse qué campos se desean consultar. Se usa un array de nombres
    de campo disponibles en el modelo. De no proporcionarse un valor se obtienen
    los datos de todos los campos existentes en el modelo. El campo de ID siempre
    estará disponible, se especifique o no:
    ```
    {
        "model_name": "base.users",
        "fields": ["name", "active"]
    }
    ```
    Retorno:
    ```
    [
        {
            "id": 1,
            "name": "iaCele",
            "active": false
        },
        {
            "id": 2,
            "name": "Onnymm Azzur",
            "active": true
        },
        {
            "id": 3,
            "name": "Lumii Mynx",
            "active": true
        }
    ]
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

    # Búsqueda y lectura de datos
    data = iacele.core.search_read(
        user_id,
        **params.model_dump()
    )

    return data

@router.patch(
    '/update',
    name= 'Actualización de registros',
    status_code= status.HTTP_200_OK,
)
async def _update(
    params: CRUD.Update,
    user_id: int = Depends(authenticate_user),
) -> Literal[True]:
    """
    ### Actualización de registros
    Endpoint para la actualización de uno o más registros a partir de su respectiva
    ID provista ya sea un valor de ID o un array de IDs, actualizando uno o más
    campos con el valor provisto. Solo se sobreescribe un mismo valor por cada
    campo a todos los registros provistos.

    ----

    #### Uso
    ```
    {
        "model_name": "base.users",
        "record_ids": 1,
        "data": {"active": true }
    }
    ```
    Retorno:
    ```
    true
    ```
    """

    # Actualización de registros
    iacele.core.update(
        user_id,
        **params.model_dump(),
    )

    return True

@router.delete(
    '/delete',
    name= 'Eliminación de registros',
    status_code= status.HTTP_200_OK,
)
async def _delete(
    params: CRUD.Delete,
    user_id: int = Depends(authenticate_user),
) -> Literal[True]:
    """
    ### Eliminación de registros
    Endpoint para la eliminación de uno o más registros de la base datos a partir
    de su respectiva ID provista.

    ----

    #### Uso
    ```
    {
        "model_name": "base.users",
        "record_ids": [8, 9, 10]
    }
    ```
    Retorno:
    ```
    true
    ```
    """

    # Eliminación de registros
    iacele.core.delete(
        user_id,
        **params.model_dump(),
    )

    return True
