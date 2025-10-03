from ._base import (
    _RequiresActionName,
    _RequiredModelName,
    _RequiresRecordID,
)

class Server:

    class Action(
        _RequiresActionName,
        _RequiresRecordID,
        _RequiredModelName,
    ):
        """
        ### Acción de servidor

        Parámetros para la ejecución de una acción de servidor.
        - `model_name`: Nombre del modelo en la base de datos.
        - `record_id`: ID del registro.
        - `action`: Nombre de la acción de servidor.
        """
        ...
