from lylac import Lylac
from lylac.utils import ModelRecordData
from app._database import db
from app.orm import ORM
from app.types import CUSTOM_MODELS

class Tree():

    def __init__(
        self,
        instance: Lylac[CUSTOM_MODELS],
    ) -> None:

        self._main = instance

    def read(
        self,
        user_id,
        model_name: str,
        record_ids: int,
    ):

        # Obtención de la ID del modelo
        model_id = self._get_model_id(user_id, model_name)

        # Lectura de los campos
        fields: list[ModelRecordData.BaseModelField] = self._main.search_read(
            user_id,
            'base.model.field',
            [('model_id', '=', model_id)],
            [
                'name',
                'label',
                'ttype',
                'help_info',
                ('related_model_id.model', 'model'),
                'selection_ids',
                'readonly',
                'is_computed',
            ],
        )

        # Se obtienen los datos de las IDs de selección en caso de haberlas
        self._get_selection_fields_data(user_id, fields)

        data = self._main.read(user_id, model_name, record_ids)

        for record in data:

            # Iteración por cada campo
            for field in fields:
                # Si el campo es de tipo one2many o many2many
                if (field['ttype'] == 'one2many' or field['ttype'] == 'many2many'):
                    # Obtención del nombre del campo
                    field_name = field['name']
                    # Obtención del nombre del modelo relacionado
                    related_model_name = field['model']
                    # Se sobreescriben las IDs en el campo del registro
                    record[field_name] = self._main.read(
                        user_id,
                        related_model_name,
                        record[field_name],
                        ['name']
                    )

        return {
            'records': data,
            'fields': fields,
        }

    def _get_selection_fields_data(
        self,
        user_id: int,
        fields: list[ModelRecordData.BaseModelField],
    ) -> None:

        # Iteración por cada registro de campo
        for field in fields:
            # Si el campo contiene valores en IDs de selección...
            if field['selection_ids']:
                # Se obtiene la ID del campo
                field_id = field['id']
                # Se sobreescriben las IDs de selección por su información con nombre y etiqueta
                field['selection_ids'] = (
                        self._main.search_read(
                        user_id,
                        'base.model.field.selection',
                        [('field_id', '=', field_id)],
                        ['name', 'label'],
                    )
                )

    def _get_model_id(
            self,
        user_id: int,
        model_name: str
    ) -> int:

        # Obtención de la ID encontrada
        [ model_id ] = self._main.search(
            user_id,
            'base.model',
            [('model', '=', model_name)],
        )

        return model_id

class Form():

    def __init__(
        self,
        instance: Lylac[CUSTOM_MODELS],
    ) -> None:

        self._main = instance

    def read(
        self,
        user_id,
        model_name: str,
        record_id: int,
    ):

        # Obtención de la ID del modelo
        model_id = self._get_model_id(user_id, model_name)

        # Lectura de los campos
        fields: list[ModelRecordData.BaseModelField] = self._main.search_read(
            user_id,
            'base.model.field',
            [('model_id', '=', model_id)],
            [
                'name',
                'label',
                'ttype',
                'help_info',
                ('related_model_id.model', 'model'),
                'selection_ids',
                'readonly',
                'is_computed',
            ],
        )

        # Se obtienen los datos de las IDs de selección en caso de haberlas
        self._get_selection_fields_data(user_id, fields)

        # Si la ID es diferente de 0
        if record_id != 0:

            # Lectura del registro
            [ record ] = self._main.read(user_id, model_name, record_id)

        else:
            record = {}

        # Iteración por cada campo
        for field in fields:
            # Si el campo es de tipo one2many o many2many
            if (field['ttype'] == 'one2many' or field['ttype'] == 'many2many') and record_id != 0:
                # Obtención del nombre del campo
                field_name = field['name']
                # Obtención del nombre del modelo relacionado
                related_model_name = field['model']
                # Se sobreescriben las IDs en el campo del registro
                record[field_name] = self._main.read(
                    user_id,
                    related_model_name,
                    record[field_name],
                    ['name']
                )

        return {
            'record': record,
            'fields': fields,
        }

    def _get_selection_fields_data(
        self,
        user_id: int,
        fields: list[ModelRecordData.BaseModelField],
    ) -> None:

        # Iteración por cada registro de campo
        for field in fields:
            # Si el campo contiene valores en IDs de selección...
            if field['selection_ids']:
                # Se obtiene la ID del campo
                field_id = field['id']
                # Se sobreescriben las IDs de selección por su información con nombre y etiqueta
                field['selection_ids'] = (
                        self._main.search_read(
                        user_id,
                        'base.model.field.selection',
                        [('field_id', '=', field_id)],
                        ['name', 'label'],
                    )
                )

    def _get_model_id(
            self,
        user_id: int,
        model_name: str
    ) -> int:

        # Obtención de la ID encontrada
        [ model_id ] = self._main.search(
            user_id,
            'base.model',
            [('model', '=', model_name)],
        )

        return model_id

class IACele():

    def __init__(self) -> None:
        instance = db
        self.core = instance
        self.form = Form(instance)
        self.tree = Tree(instance)
        self.orm = ORM()

iacele = IACele()
