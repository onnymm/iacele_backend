import pandas as pd
import numpy as np
from typing import overload

class Transformation():
    
    # Funciones para uso en apply
    @overload
    def _apply_get_many2one_values(value: bool) -> bool:
        ...
    @overload
    def _apply_get_many2one_values(value: list) -> str:
        ...

    def _apply_get_many2one_values(value: bool | list):
        """
        ## Extracción de valores many2one
        Este método interno extrae el nombre del valor many2one provisto
        desde un Pandas.Series. Retorna el valor por sí mismo si éste es un
        booleano (False) o el índice 1 si contiene una lista, que por
        defecto siempre es de 2 valores dentro
        """


        if isinstance(value, bool):
            return value
        
        elif isinstance(value, list):
            if len(value) == 2:
                return value[1]
            else:
                raise IndexError("Los valores de tipo many2one deben ser estrictamente listas de 2 valores.")
        
        else:
            raise TypeError("Los valores tipo many2one sólo pueden ser listas o booleanos.")

    @overload
    def _apply_get_generic_values(value: np.number) -> str:
        ...
    @overload
    def _apply_get_generic_values(value: bool) -> str:
        ...
    @overload
    def _apply_get_generic_values(value: str) -> str:
        ...
    @overload
    def _apply_get_generic_values(value: int) -> int:
        ...
    @overload
    def _apply_get_generic_values(value: object) -> str:
        ...

    def _apply_get_generic_values(value: np.number | bool | str | int | object) -> str:
        """
        ## Extracción y/o transformación de valores genéricos
        Este método interno extrae el valor provisto
        desde un Pandas.Series. Retorna un valor transformado o el valor por sí
        mismo dependiendo del caso, esto, con fines de ordenamiento adecuado
        del objeto Pandas.Series al que se le aplicará este método.
        """
        # Si el valor es np.nan se retorna una cadena vacía para evitar la
        #       propagación del tipo de valor flotante por todo el objeto
        if value is np.nan:
            return ""
        
        # Se transforma el valor para evitar un ordenamiento anormal con otros
        #       tipos de valores como 0.
        elif isinstance(value, bool):
            return '1' if value else ''
        
        elif isinstance(value, np.number) or isinstance(value, str) or isinstance(value, object) or isinstance(value, object):
            return value
        
        else:
            raise TypeError(f"El valor {type(value)} no está admitido en este método.")
        
    apply_get_values = {
        'many2one': _apply_get_many2one_values,
        'char': _apply_get_generic_values,
        'float': _apply_get_generic_values,
        'integer': _apply_get_generic_values,
        'monetary': _apply_get_generic_values,
    }
    """
    ## Funciones de extracción de valores
    Este es un mapa de funciones para extracción de valores que transforma
    los datos de un Pandas.Series dependiendo del tipo de valor que se
    indica.

    Uso:
    >>> df['new_column'] = apply_get_values[df['user_id'], 'many2one']
    """

    def get_values_from_series(self, series: pd.Series, value_type: str) -> pd.Series:
        """
        ## Obtención de valores útiles de un Pandas.Series
        Este método extrae los valores útiles de un Pandas.Series en base a su
        tipo y naturaleza. Para usar este método también es necesario indicar
        el tipo de campo del que se tomaron los valores.

        Uso:
        >>> get_values_from_series(df['some_field_name'], 'many2one')

        Los tipos de campos son:
        - `'char'`
        - `'integer'`
        - `'float'`
        - `'many2one'`
        """
        return series.apply(self.apply_get_values[value_type])
