from ._base import (
    _HasSegmentation,
    _HasSelectableFields,
    _RequiredModelName,
    _RequiresRecordData,
    _RequiresRecordsData,
    _RequiresRecordIDs,
    _SupportsFiltering,
    _SupportsSorting,
)

class CRUD:

    class Create(
        _RequiredModelName,
        _RequiresRecordsData,
    ):
        """
        ### Creación
        Parámetros para creación de registro(s)

        - `model_name`: Nombre del modelo en la base de datos.
        - `data`: Diccionario o lista de diccionarios de datos de los registros a crear.
        """
        ...

    class Search(
        _HasSegmentation,
        _SupportsFiltering,
        _RequiredModelName,
    ):
        """
        ### Búsqueda
        Parámetros para búsqueda de registros.

        - `model_name`: Nombre del modelo en la base de datos.
        - `search_criteria`: Criterio de búsqueda para filtrar resultados.
        - `offset`: Desfase de índice de resultados.
        - `limit`: Límite de resultados obtenidos.
        """
        ...

    class Read(
        _SupportsSorting,
        _HasSelectableFields,
        _RequiresRecordIDs,
        _RequiredModelName,
    ):
        """
        ### Lectura
        Parámetros para lectura de registros.

        - `model_name`: Nombre del modelo en la base de datos.
        - `record_ids`: IDs de registros a leer.
        - `fields`: Campos del modelo a leer.
        - `sortby`: Campo a usar para ordenar los resultados.
        - `ascending`: Ordenamiento ascendente o no.
        """
        ...

    class SearchRead(
        _HasSegmentation,
        _SupportsSorting,
        _HasSelectableFields,
        _SupportsFiltering,
        _RequiredModelName,
    ):
        """
        ### Búsqueda y lectura
        Párámetros para búsqueda y lectura de registros

        - `model_name`: Nombre del modelo en la base de datos.
        - `search_criteria`: Criterio de búsqueda para filtrar resultados.
        - `fields`: Campos del modelo a leer.
        - `sortby`: Campo a usar para ordenar los resultados.
        - `ascending`: Ordenamiento ascendente o no.
        - `offset`: Desfase de índice de resultados.
        - `limit`: Límite de resultados obtenidos.
        """
        ...

    class Update(
        _RequiresRecordData,
        _RequiresRecordIDs,
        _RequiredModelName,
    ):
        """
        ### Modificación
        Parámetros para modificación de registros.

        - `model_name`: Nombre del modelo en la base de datos.
        - `record_ids`: IDs de registros a leer.
        - `data`: Diccionario o lista de diccionarios de datos de los registros a crear.
        """
        ...

    class Delete(
        _RequiresRecordIDs,
        _RequiredModelName,
    ):
        """
        ### Eliminación
        Parámetros para eliminación de registros.

        - `model_name`: Nombre del modelo en la base de datos.
        - `record_ids`: IDs de registros a leer.
        """
        ...
