import pandas as pd
from ._re import SearchEngine
from ._transformation import Transformation
from ._data import Data
from odoo_api_manager import OdooAPIManager
from typing import Annotated

class BaseIACelePandas():
    """
    ## Módulo de extensión de Pandas
    Este módulo extiende la funcionalidad de Pandas para uso de IACele.

    Uso:
    >>> import pandas as pd
    >>> @pd.api.extensions.register_dataframe_accessor("iacele")
    >>> class IACelePandas(BaseIACelePandas):
    >>>     # Asignación de herramientras adicionales
    >>>     api_manager = ...
    """

    # Motor de búsquedas con expresiones regulares
    re = SearchEngine()
    # Extensión de transformación de datos
    transformation = Transformation()
    # Extensión para uso de variables de datos
    data = Data()

    # Tipado sin assignación
    api_manager: OdooAPIManager = ...

    def __init__(self, df_obj: pd.DataFrame) -> None:
        self.df = df_obj



    def to_backend_response(self) -> list[dict]:
        """
        ## DataFrame a JSON
        Este método convierte el DataFrame a una lista de diccionarios
        acondicionada para ser enviada por el framework de Backend FastAPI para
        ser fácilmente usada por el servidor Frontend.

        Uso:
        >>> df.iacele.to_backend_response()
        """
        return (
            list(
                self.df
                .T
                .to_dict()
                .values()
            )
        )



    def re_search(self, search: str, column: str) -> pd.Series:
        """
        ## Búsqueda con expresiones regulares
        Este método realiza una búsqueda en una columna del DataFrame creando
        una expresión regular para mayor precisión en las coincidencias y
        retorna un pandas.Series de booleanos para usarse como indexador en
        el DataFrame.

        Recibe como primer argumento el texto a buscar y como segundo argumento
        la columna en dónde realizar la búsqueda:

        Uso:
        >>> matches = df.iacele.re_search("Hola", "user_name")
        >>> df[matches]
        >>> #    id ... user_name
        >>> # 0  14 ...      Hola
        >>> # 1  23 ...    hooola
        >>> # 2  24 ...  HOOOLAAA
        >>> # 3  36 ...      Hólä
        """

        # Expresión regular formada para la búsqueda de coincidencias
        regex_exp = self.re.create_search(search)

        # Filtro de la búsqueda
        matches = self.df[column].astype(str).str.contains(regex_exp, case= False)

        # Retorno de las coincidencias
        return matches



    def search(self, search: list[dict[str]], fields_info: dict[str]) -> pd.DataFrame:
        """
        Búsqueda de resultados
        Este método realiza una búsqueda a través de una lista de diccionarios
        provista que contengan cada uno las siguientes llaves:
        >>> # Muestra de un dicciorio
        >>> {
        >>>     'search': 'Algún texto',
        >>>     'field': 'product_name',
        >>>     'type': 're',
        >>> }

        Estos atributos indican los siguientes parámetros:
        - `'search'`: El texto a encontrar en la búsqueda.
        - `'field'`: El nombre de la columna a realizar esta búsqueda.
        - `'type'`: Tipo de búsqueda a realizar. Las opciones disponibles son
        las siguientes:
            - `'re'`: Búsqueda con expresiones regulares (Busca coincidencias
            similares, no sólo las exactas).
            - `'contains'`: Búsqueda por contenido del texto buscado.
            - `'exact'`: Búsqueda por coincidencia exacta de todo el contenido
            buscado.
        """

        # Almacenamiento de las columnas iniciales para retorno del DataFrame sin alterar
        initial_columns = self.df.columns

        # Columna inicial para operaciones lógicas
        matches = self.df["init_condition"] = False

        # Iteración por cada parámetro de búsqueda de los criterios de búsqueda
        for param in search:

            # Obtención de columna a filtrar
            self.df[f"{param["field"]}__search"] = self.transformation.get_values_from_series(self.df[param["field"]], fields_info[param["field"]])

            # Obtención de coincidencias en base al tipo de búsqueda
            matches |= self._search_callback(param["type"], param["search"], param["field"])

        # Creación del DataFrame filtrado
        results = self.df[matches]

        # Retorno del DataFrame con las columnas originales
        return results[initial_columns]



    def _search_callback(self, search_type: str, search_text: str, column_name: str) -> Annotated[pd.Series, bool]:
        match search_type:
            case "re":
                return self.df.iacele.re_search(search_text, column_name)
            case "contains":
                return self.df[column_name].astype(str).contains(search_text, regex= False, case= False)
            case "exact":
                return self.df[column_name].astype(str) == search_text


    def get_additional_fields(self, view: str) -> pd.DataFrame:

        # Iteración por cada uno de los módulos de donde se obtendrá la información
        for module in self.data.table_data_views[view]:

            # Campos para usar en el DataFrame
            fields = self.data.table_data_views[view][module]['fields']

            # Criterio de búsqueda dinámico
            search_criteria = self._build_search_criteria(view, module)

            # Obtención del conjunto de datos directamente en DataFrame
            data = self.api_manager.data.get_dataset(module, search_criteria, fields)

            # Obtención de la función de transformación y obtención de los datos
            data_callback = self.data.table_data_views[view][module]['callback']

            # Ejecución de la función
            self.df = self.df.pipe(
                lambda df: data_callback(
                    df,
                    data
                )
            )

        # Retorno del nuevo DataFrame
        return self.df

    def _build_search_criteria(self, view: str, module: str):

        # Se obtiene la estructura para generar
        return self._evaluate_search_criteria(self.data.table_data_views[view]['stock.quant']['criteria'])

    def _evaluate_search_criteria(self, search_criteria: list[tuple, str, int, bool] | tuple[str, int, bool, list[int]]):
        
        if isinstance(search_criteria, list) or isinstance(search_criteria, tuple):
            
            structure = type(search_criteria)(
                [
                    self._evaluate_search_criteria(value)
                        if isinstance(value, tuple) or isinstance(value, list)
                        else self._compile(value)
                    for value in search_criteria
                ]
            )

        else:

            structure = search_criteria

        return structure

    def _compile(self, value: str | int | bool):
        if isinstance(value, str):
            if value.startswith("@"):
                value = value.replace("@", "self.")
                value = eval(value)

        return value
    
    def merge_data(self, add_data: pd.DataFrame, column_name: str) -> pd.DataFrame:
        add_data.iacele.keep_integers()
        add_data.iacele.keep_floats()

        return pd.merge(
            left= self.df,
            left_on= column_name,
            right= add_data,
            right_on= 'id',
            how= "left"
        )

    def keep_integers(self) -> None:
        int_columns_to_keep = (
            self.df
            .dtypes
            .reset_index(
                name='dtype'
            )
            .pipe(
                lambda df: (
                    df[df["dtype"] == 'int64']
                )
            )
            ['index']
            .to_list()
        )
        
        for column in int_columns_to_keep:
            self.df[column] = self.df[column].astype("Int64")

        return self.df

    def keep_floats(self) -> None:
        int_columns_to_keep = (
            self.df
            .dtypes
            .reset_index(
                name='dtype'
            )
            .pipe(
                lambda df: (
                    df[df["dtype"] == 'float64']
                )
            )
            ['index']
            .to_list()
        )

        for column in int_columns_to_keep:
            self.df[column] = self.df[column].astype("Float64")

        return self.df
