from typing import Optional
from fastapi import Body
from pydantic import BaseModel
from lylac._module_types import CriteriaStructure
from app.types import (
    FieldMetadata,
    SelectionValue,
    BACKEND_MODELS,
)

class _HasSegmentation(BaseModel):
    offset: Optional[int] = Body(
        default= None,
        description= '- Desfase de índice de resultados.',
    )
    limit: Optional[int] = Body(
        default= None,
        description= '- Límite de cantidad de resultados a retornar.',
    )

class _HasSelectableFields(BaseModel):
    fields: list[str] = Body(
        default=[],
        description="- Array de nombres de campo del modelo.",
        json_schema_extra={'format': 'Fields'},
    )

class _RequiresActionName(BaseModel):
    action: str = Body(
        description= '- Nombre de la acción de servidor.'
    )

class _RequiresItemsPerPage(BaseModel):
    items_per_page: int = Body(
        description= '- Cantidad máxima de registros por página.',
    )

class _RequiredModelName(BaseModel):
    model_name: BACKEND_MODELS = Body(
        description= '- Nombre del modelo en la base de datos.',
        json_schema_extra= {'format': 'ModelName'},
    )

class _RequiresPageNumber(BaseModel):
    page: int = Body(
        description= '- Número de página',
    )

class _RequiresRecordData(BaseModel):
    data: dict | list[dict] = Body(
        description= '- Objeto de datos de los registros a modificar.',
    )

class _RequiresRecordsData(BaseModel):
    data: dict | list[dict] = Body(
        description= '- Objeto o array de objetos de datos de los registros a crear.',
    )

class _RequiresRecordID(BaseModel):
    record_id: int = Body(
        description= '- ID del registro.',
    )

class _RequiresRecordIDs(BaseModel):
    record_ids: int | list[int] = Body(
        description= '- IDs de registros',
    )

class _SupportsFiltering(BaseModel):
    search_criteria: CriteriaStructure = Body(
        default= [],
        json_schema_extra= {'format': 'CriteriaStructure'},
        description= '- Criterio de búsqueda para filtrar resultados',
    )

class _SupportsSorting(BaseModel):
    sortby: Optional[str | list[str]] = Body(
        default= None,
        description= '- Campo usado para ordenar los resultados.',
    )
    ascending: Optional[bool | list[bool]] = Body(
        default= None,
        description= '- Ordenamiento ascendente',
    )

class _HasRecordData(BaseModel):
    record: dict = Body(
        description= '- Datos del registro.',
    )

class _HasFieldsMetadata(BaseModel):
    fields: list[FieldMetadata[SelectionValue]] = Body(
        description= '- Metadatos de los campos del modelo.'
    )

class _HasRecordsData(BaseModel):
    records: list[dict] = Body(
        description= '- Datos de los registros.',
    )

class _Count(BaseModel):
    count: int = Body(
        description= '- Datos de los registros.',
    )

class _ModelLabel(BaseModel):
    model_label: str = Body(
        description= '- Etiqueta del modelo.'
    )
