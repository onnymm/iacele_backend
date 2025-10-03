from app.orm._base import Base_ORM

class Form():

    def __init__(
        self,
        instance: Base_ORM
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

    def get(
        self,
        user_id: int,
        model_name: str,
        record_id: int,
    ):

        # Obtención de los datos de los campos
        fields = self._main._get_fields_info(model_name)

        # Si la ID es diferente de 0...
        if record_id != 0:

            # Lectura del registro
            [ record ] = self._main._db.read(
                user_id,
                model_name,
                record_id,
            )

        # Si la ID es igual a 0...
        else:
            # Se utiliza un diccionario vacío
            record = {}

        # Obtención de los campos relacionados
        related_fields = self._main._get_related_fields(fields)

        # Obtención de datos de registros referenciados
        self._main._get_related_records([record], related_fields)

        return {
            'record': record,
            'fields': fields,
        }
