from typing import TypedDict, Callable
import pandas as pd
from dml_manager import CriteriaStructure

# Función de transformación de datos de pandas.DataFrame
class DataTransformationCallback(TypedDict):
    search_criteria: CriteriaStructure
    callback: Callable[[pd.DataFrame], list[dict]]

# Mapa de funciones de transformación de datos de pandas.DataFrame
TransformCallbacksCollection = dict[str, DataTransformationCallback]
