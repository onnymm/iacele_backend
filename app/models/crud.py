from typing import (
    TypedDict,
    Union,
)
from pydantic import BaseModel
from fastapi import (
    Body,
    Query,
)
from dml_manager import CriteriaStructure
from app.types import DBTable
from pydantic.alias_generators import to_camel

_RecordValue = Union[int, float, str, bool, list[int], None]
_Record = dict[str, _RecordValue]
_Records = list[_Record]

class _SearchReadRecords(TypedDict):
    data: _Records
    count: int

class _PostRequestData(BaseModel):
    table_name: DBTable = Body()

class _Create(_PostRequestData):
    data: _Record | list[_Record]

class _GetRequestData(BaseModel):
    table_name: DBTable = Query()

class _Read(_GetRequestData):
    record_ids: int | list[int] = Query()
    fields: list[str] = Query([])
    sortby: str | list[str] = Query(None)
    ascending: bool | list[bool] = Query(True)

class _SearchRead(_PostRequestData):
    search_criteria: CriteriaStructure = Body([])
    fields: list[str] = Body([])
    offset: int | None = Body(None)
    limit: int | None = Body(None)
    sortby: str | list[str] = Body(None)
    ascending: bool | list[bool] = Body(True)

class _Update(_PostRequestData):
    record_id: int = Body()
    data_to_write: dict = Body()

class _Delete(_GetRequestData):
    record_ids: int | list[int]

# Modelos para endpoints

class crud():
    create = _Create
    read = _Read
    search_read = _SearchRead
    update = _Update
    delete = _Delete

class response():
    records = _Records
    search_read = _SearchReadRecords
