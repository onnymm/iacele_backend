from typing import Optional
from typing import TypeVar
from pydantic import BaseModel
from pydantic import BaseModel
from lylac import CriteriaStructure

_T = TypeVar('_T')

_ScalarOrList = _T | list[_T]

_FieldName = str

ExpandedRecords = tuple[_FieldName | _T]

_AliasedField = tuple[_T, str]

_SupportsAlias = _T | _AliasedField[_T]

_FlatOrNested = _SupportsAlias[_FieldName] | _SupportsAlias[ExpandedRecords[_T]]

FieldsSelectionLevel4 = list[_SupportsAlias[_FieldName]]

FieldsSelectionLevel3 = list[_FlatOrNested[FieldsSelectionLevel4]]

FieldsSelectionLevel2 = list[_FlatOrNested[FieldsSelectionLevel3]]

FieldsSelectionLevel1 = list[_FlatOrNested[FieldsSelectionLevel2]]

class _SupportsSelectableFieldsLevel_3:
    fields: FieldsSelectionLevel3

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
    record_ids: _ScalarOrList[int]

class _RequiresRecordID(BaseModel):
    record_ids: int

class _SupportsSelectableFields(BaseModel):
    fields: FieldsSelectionLevel1 = []

class _SupportsSorting(BaseModel):
    sortby: Optional[_ScalarOrList[str]] = None
    ascending: Optional[_ScalarOrList[bool]] = None
