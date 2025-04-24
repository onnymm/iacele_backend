from app.types import DBTable
from fastapi import Body
from pydantic import BaseModel

class Action(BaseModel):
    record_ids: int | list[int] = Body(...)
    table: DBTable = Body(...)
    action: str = Body(...)
