from app.orm._base import Base_ORM
from app.orm._modules import List, Account, Form
from app.types import (
    BACKEND_MODELS,
    SelectionValue,
    FieldMetadata,
)
from lylac import Lylac
from app._database import db

class ORM(Base_ORM):
    _db: Lylac[BACKEND_MODELS]
    list_: List

    def __init__(
        self,
    ) -> None:

        self._db = db
        self.list_ = List(self)
        self.form = Form(self)
        self.account = Account(self)

    def _get_related_fields(
        self,
        fields: list[dict],
    ) -> list[tuple[str, str]]:

        # Inicialización de campos referenciados
        related_fields: list[tuple[str, str]] = []

        # Iteración por cada campo
        for field in fields:
            # Obtención del tipo del campo
            ttype = field['ttype']
            # Si el campo es one2many o many2many
            if ttype in ['one2many', 'many2many']:
                # Obtención del nombre del campo
                field_name = field['name']
                # Obtención del nombre del modelo relacionado
                related_model_name = field['model']
                # Se añaden los datos
                related_fields.append( (field_name, related_model_name,) )

        return related_fields

    def _get_related_records(
        self,
        records,
        related_fields,
    ) -> None:

        # Iteración por cada campo relacionado
        for ( field_name, related_model_name ) in related_fields:
            # Iteración por cada registro
            for record in records:
                if len(record) == 0:
                    return None
                # Obtención de los datos de los registros referenciados
                record[field_name] = self._db.read(
                    self._db._ROOT_USER,
                    related_model_name,
                    record[field_name],
                    ['name']
                )

    def _get_fields_info(
        self,
        model_name: str,
    ) -> list[FieldMetadata[SelectionValue]]:

        # Obtención de la ID del modelo
        model_id = self._get_model_id(model_name)

        # Obtención de los campos
        raw_fields: list[FieldMetadata[int]] = self._db.search_read(
            self._db._ROOT_USER,
            'base.model.field',
            [('model_id', '=', model_id)],
            self._FIELD_ATTS,
        )

        # Obtención de los valores de selección
        fields = self._get_selection_values(raw_fields)

        return fields

    def _get_selection_values(
        self,
        fields: list[FieldMetadata[int]],
    ) -> list[FieldMetadata[SelectionValue]]:

        # Iteración por cada registro de campo
        for field in fields:
            # Si el campo contiene valores de IDs de selección...
            if field['selection_ids']:
                # Se obtiene la ID del campo
                field_id = field['id']
                # Se sobreescriben las IDs de selección por su información con nombre y etiqueta
                field['selection_ids'] = (
                    self._db.search_read(
                        self._db._ROOT_USER,
                        'base.model.field.selection',
                        [('field_id', '=', field_id)],
                        ['name', 'label']
                    )
                )

        return fields

    def _get_model_id(
        self,
        model_name: str,
    ) -> int:

        # Obtención de la ID del modelo
        [ model_id ] = self._db.search(
            self._db._ROOT_USER,
            'base.model',
            [('model', '=', model_name)],
        )

        return model_id
