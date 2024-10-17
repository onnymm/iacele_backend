import pandas as pd
from app.utils.data_transformation import list_fields
from app.extensions.iacele_pandas import BaseIACelePandas
from app.data.dataframes import data as dataframe_data

# Registro de la extensión de iaCele en Pandas
@pd.api.extensions.register_dataframe_accessor("iacele")
class IACelePandas(BaseIACelePandas):
    pass

def get_commisions(
    page: int,
    items_per_page: int,
    search_criteria: str = None,
    sortby: str = None,
    ascending: bool = True,
    search: list[dict] = None
):
    
    # Obtención del índice de inicio del DataFrame
    start_index = page * items_per_page
    # Obtención del índice de fin del DataFrame
    end_index = start_index + items_per_page

    # Obtención del conjunto de datos local
    data: pd.DataFrame = dataframe_data["commisions"]['data']

    # Obteción de los campos
    fields = dataframe_data["commisions"]['fields']

    # Si hay criterio de búsqueda se realiza el filtro
    if search_criteria != "":
        data = data.query(search_criteria)

    if search:
        data = data.iacele.search(search, list_fields(fields))

    # Si hay ordenamiento se realiza
    if sortby:
        data = data.sort_values(sortby, ascending= ascending)

    # Conteo de datos
    count = len(data)

    # Transformación del DataFrame a lista de diccionarios
    data =  (
        data
        .iloc
        [start_index:end_index]
        .iacele.to_backend_response()
    )

    # Retorno del diccionario con los datos, la información de los campos y el conteo total de datos
    return {
        'data': data,
        'fields': fields,
        'count': count
    }