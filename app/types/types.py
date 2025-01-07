from typing import TypedDict, Literal, Union
from datetime import datetime, date

# Estructuras de búsqueda de texto desde el frontend
class SearchMethod(TypedDict):
    field: str
    type: Literal['re', 'contains', 'match']
class SearchStructure(TypedDict):
    text: str
    method: list[SearchMethod]
class SearchOP(TypedDict):
    re: str
    contains: str
    match: str

FieldType = Literal['char', 'integer', 'float', 'monetary', 'date']

# Estructuras de respuesta de datos
class FieldData(TypedDict):
    name: str
    ttype: FieldType

DataValue = Union[int | str | float | list[int] | datetime | date | None]

DataRecords = list[dict[str, DataValue]]

class DataResponse(TypedDict):
    data: DataRecords
    count: int
    fields: list[FieldData]
