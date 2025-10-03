from lylac import Lylac
from app.types import (
    FieldMetadata,
    SelectionValue,
)

class Base_ORM():
    _db: Lylac

    _FIELD_ATTS = [
        'name',
        'label',
        'ttype',
        'help_info',
        ('related_model_id.model', 'model'),
        'selection_ids',
        'readonly',
        'is_computed',
    ]

    def _get_related_fields(
        self,
        fields: list[dict],
    ) -> list[tuple[str, str]]:
        """
        ### Campos relacionados
        Obtención de la selección de los campos de tipo `one2many` y `many2many` junto
        con su campo relacionado en el modelo relacionado.
        """
        ...

    def _get_related_records(
        self,
        records,
        related_fields,
    ):
        """
        ### Relacionados
        Obtención de los registros relacionados desde los campos relacionados.
        """
        ...

    def _get_fields_info(
        self,
        model_name: str,
    ) -> list[FieldMetadata[SelectionValue]]:
        """
        ### Metadatos de campos
        Obtención de los metadatos de campos para uso en renderización del frontend.
        """
        ...

    def _get_selection_values(
        self,
        fields: list[FieldMetadata[int]],
    ) -> list[FieldMetadata[SelectionValue]]:
        """
        ### Valores de selección
        Obtención de los valores de selección de los campos de tipo `selection`.
        """
        ...

    def _get_model_id(
        self,
        model_name: str,
    ) -> int:
        """
        ### ID de modelo
        Obtención de la ID del modelo provisto.
        """
        ...
