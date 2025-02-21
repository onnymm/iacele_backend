import json
from app.core.types import CriteriaStructure
from app.models.base import BaseDataRequest
from app.database import db_connection
from app.database.types import types
from app.extensions.dml_manager import DMLManager
from app.constants.key_values import op
from app.extensions.regex_generator import re_engine
from app.types import (
    SearchMethod,
    SearchStructure,
    DataResponse,
    FieldData,
)

def get_data_for_table(
    table_name: str,
    params: BaseDataRequest,
    search: SearchStructure,
    search_criteria: CriteriaStructure = [],
    fields: list[str]= [],
) -> DataResponse:
    """
    ## Obtención de datos para tabla
    Este método realiza una consula a la base de datos y retorna un diccionario
    con tres atributos:
    - `'data'`: La lista con una página de diccionarios que contienen registros
    con sus atributos.
    - `'count'`: Un conteo total de los registros existentes en esta consulta.
    - `'fields'`: Información de los tipos de campos.
    """

    # Creación del criterio de búsqueda completo
    full_search_criteria = DMLManager.and_(
        search_criteria,
        create_text_search_criteria(search),
    )

    # Búsqueda y lectura en la base de datos
    data = db_connection.search_read(
        table_name,
        full_search_criteria,
        offset= params.page * params.items_per_page,
        limit= params.items_per_page,
        sortby= params.sortby,
        ascending= params.ascending,
        output_format= "dict",
    )

    # Obtención del conteo
    count = db_connection.search_count(
        table_name,
        full_search_criteria,
    )

    # Obtención de la información de los campos
    field_types = _get_field_types(table_name, fields)

    # Retorno de la información
    return {
        'data': data,
        'count': count,
        'fields': field_types
    }

def _get_field_types(table_name: str, fields: list[str] = []) -> list[FieldData]:
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

def create_text_search_criteria(search: str) -> CriteriaStructure:
    """
    Creación de criterio de búsqueda a partir de dominio de texto de búsqueda proporcionado.
    """

    # Obtención del objeto de estructura de búsqueda de texto
    search: SearchStructure = json.loads(search)

    # Inicialización del objecto para la creación del criterio de búsqueda
    base_criteria: CriteriaStructure = []

    # Creación de los criterios de búsqueda individuales
    for m in search['method']:
        base_criteria = DMLManager.or_(build_search_text_criteria(m, search['text']), base_criteria)

    # Retorno de los parámetros
    return base_criteria

def build_search_text_criteria(search_method: SearchMethod, search_text: str) -> CriteriaStructure:

    if search_method['type'] == 're':
        value = re_engine.create_search(search_text)
    else:
        value = search_text

    return [(search_method['field'], op[search_method['type']], value)]
