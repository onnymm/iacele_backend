from app.core._types import CriteriaStructure
from app.models.base import BaseDataRequest
from app.database import db_connection
from app.database.types import types

def get_data_for_table(
    table_name: str,
    params: BaseDataRequest,
    search_criteria: CriteriaStructure = [],
    fields: list[str]= []
):
    """
    ## Obtención de datos para tabla
    Este método realiza una consula a la base de datos y retorna un diccionario
    con tres atributos:
    - `'data'`: La lista con una página de diccionarios que contienen registros
    con sus atributos.
    - `'count'`: Un conteo total de los registros existentes en esta consulta.
    - `'fields'`: Información de los tipos de campos.
    """

    data = db_connection.search_read(
        table_name,
        search_criteria,
        offset= params.page * params.items_per_page,
        limit= params.items_per_page,
        sortby= params.sortby,
        ascending= params.ascending,
        output_format= "dict",
    )

    count = db_connection.search_count(
        table_name,
        search_criteria,
    )

    fields = _get_field_types(table_name, fields)

    return {
        'data': data,
        'count': count,
        'fields': fields
    }

def _get_field_types(table_name: str, fields: list[str] = []):
    """
    ## Obtención de tipos de campo
    Esta función interna retorna una lista de diccionarios que contiene los
    tipos de campo a partir del nombre de una tabla y de una lista de nombres
    de campo provistos. Si la lista de nombres de campo no fue provista se
    retornan todos los campos con sus tipos.
    """

    # Si una lista con nombres fue provista
    if len(fields):
        # Se retorna la selección de tipos de campo
        return [
            {
                'name': field,
                'ttype': types[table_name][field]
            }
            for field in fields
        ]
    # Si una lista con nombres no fue provista
    else:
        # Se retornan todos los campos
        return [
            {
                'name': field,
                'ttype': types[table_name][field]
            }
            for field in types[table_name].keys()
        ]
