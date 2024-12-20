from typing import Literal, Union
from typing import TypedDict, Callable
import pandas as pd

# Operadores de comparación para queries SQL
_ComparisonOperator = Literal['=', '!=', '>', '>=', '<', '<=', '><', 'in', 'not in', 'ilike', 'not ilike']
# Operadores lógicos para queries SQL
_LogicOperator = Literal['&', '|']
# Tipo de dato de valor para queries SQL
_TripletValue = Union[
    int,
    float,
    str,
    list[int, str]
]
# Estructura de tripletas para queries SQL
_TripletStructure = tuple[str, _ComparisonOperator, _TripletValue]
# Estructura de criterios de búsqueda para queries SQL
CriteriaStructure = list[
    Union[
    _LogicOperator,
        _TripletStructure
    ]
]
"""
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

# Valor de criterio de búsqueda
_CommonType = Union[str, int, float, list[int]]

# Función de transformación de datos de pandas.DataFrame
class DataTransformationCallback(TypedDict):
    search_criteria: CriteriaStructure
    callback: Callable[[pd.DataFrame], list[dict]]

# Mapa de funciones de transformación de datos de pandas.DataFrame
TransformCallbacksCollection = dict[str, DataTransformationCallback]
