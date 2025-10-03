from typing import Optional
from lylac._module_types import CriteriaStructure
from app.orm._base import Base_ORM

class List():

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
        page: int,
        items_per_page: int,
        search_criteria: CriteriaStructure = [],
        sortby: Optional[str | list[str]] = None,
        ascending: Optional[bool | list[bool]] = None,
    ):

        # Cálculo del desfase
        offset = self._calculate_offset(page, items_per_page)

        # Obtención de lista de registros
        records = self._main._db.search_read(
            user_id,
            model_name,
            search_criteria,
            offset= offset,
            limit= items_per_page,
            sortby= sortby,
            ascending= ascending,
        )

        # Obtención de los datos de los campos
        fields = self._main._get_fields_info(model_name)

        # Obtención de los campos relacionados
        related_fields = self._main._get_related_fields(fields)

        # Obtención de datos de registros referenciados
        self._main._get_related_records(records, related_fields)

        # Obtención de cantidad total de registros
        count = self._main._db.search_count(
            self._main._db._ROOT_USER,
            model_name,
            search_criteria,
        )

        # Obtención de la etiqueta del modelo
        model_id = self._main._get_model_id(model_name)
        model_label = self._main._db.get_value(
            self._main._db._ROOT_USER,
            'base.model',
            model_id,
            'label',
        )

        return {
            'records': records,
            'fields': fields,
            'count': count,
            'model_label': model_label,
        }

    def _calculate_offset(
        self,
        page: int,
        items_per_page: int,
    ) -> int:

        # Cálculo del desfase
        offset = page * items_per_page

        return offset
