from fastapi import Query
from app.core._types import CriteriaStructure
import json

def criteria_from_endpoint(search_criteria: str = Query("[]")):
    """
    ## Construcción de criterios de búsqueda
    Esta dependencia contiene un criterio de búsqueda desde el endpoint y
    retorna una función para construir un criterio de búsqueda a partir del
    criterio base provisto a la función retornada.

    Uso:
    >>> from fastapi import FastAPI, Depends
    >>> ...
    >>> @app.get(...)
    >>> def get_records(build_criteria = Depends(criteria_from_endpoint))
    >>>     search_criteria = build_criteria()
    >>>     # ['&', ('state', '=', 'done'), ('some_param', '=', ...)]

    ----

    ### Estructura de criterio de búsqueda
    La estructura del criterio de búsqueda consiste en una lista de tuplas de 3 valores, mejor
    conocidas como tripletas. Cada una de estas tripletas consiste en 3 diferentes parámetros:
    1. Nombre del campo de la tabla
    2. Operador de comparación
    3. Valor de comparación

    Algunos ejemplos de tripletas son:
    >>> ('id', '=', 5)
    >>> # ID es igual a 5
    >>> ('amount', '>', 500)
    >>> # "amount" es mayor a 500
    >>> ('name', 'ilike', 'as')
    >>> # "name" contiene "as"

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

    Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
    Unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
    primera posición:
    >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
    >>> # "amount" es mayor a 500 y "name" contiene "as"
    >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
    >>> # "id" es igual a 5 o "state" es igual a "posted"

    Los operadores lógicos disponibles son:
    - `'&'`: AND
    - `'|'`: OR
    """

    # Conversión del criterio de búsqueda de cadena de texto a lista de tuplas
    search_criteria: CriteriaStructure = json.loads(search_criteria)

    # Función de retorno
    def build_criteria(base_criteria: CriteriaStructure = []):

        # Si fue provisto un criterio de búsqueda base
        if len(base_criteria) > 0:

            # Si el criterio de búsqueda del endpoint contiene parámetros
            if len(search_criteria) > 0:

                # Se realiza la concatenación estructurada de ambos criterios de búsqueda
                base_criteria.insert(0, "&")
                return base_criteria + search_criteria

            # Se retorna el criterio base si no se obtuvo ningún parámetro del endpoint
            return base_criteria

        # Si no fue provisto un criterio de búsqueda base se retorna el criterio de búsqueda del endpoint
        return search_criteria

    # Retorno de la función para construcción de los parámetros
    return build_criteria
