from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel
from lylac import CriteriaStructure

_FieldAlias = tuple[str, str]

class _RequiresModelName(BaseModel):
    model_name: str

class _RequiresRecordData(BaseModel):
    data: dict

class _RequiresRecordsData(BaseModel):
    data: dict | list[dict]

class _SupportsSegmentation(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None

class _SupportsFiltering(BaseModel):
    search_criteria: CriteriaStructure = []

class _RequiresName(BaseModel):
    name: str

class _RequiresRecordID(BaseModel):
    record_id: int

class _RequiresRecordIDs(BaseModel):
    record_ids: int | list[int]

class _SupportsSelectableFields(BaseModel):
    fields: list[str | _FieldAlias] = []

class _SupportsSorting(BaseModel):
    sortby: Optional[str | list[str]] = None
    ascending: Optional[bool | list[bool]] = None
