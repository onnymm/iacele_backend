from app.types import DBTable
from fastapi import Body
from pydantic import BaseModel

class Action(BaseModel):
    table: DBTable = Body(...)
    action: str = Body(...)
    record_ids: int | list[int] = Body(...)
    data: dict = Body({})

class Task(BaseModel): 
    table: DBTable = Body(...)
    task: str = Body(...)
