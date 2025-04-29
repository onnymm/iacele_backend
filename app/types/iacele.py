from app.models.crud import DBTable
from typing import Callable

RecordAction = Callable[[DBTable, str, int | list[int], dict], bool]
ModelAction = Callable[[DBTable, str], bool]

Actions = dict[DBTable, dict[str, RecordAction]]
Tasks = dict[DBTable, dict[str, ModelAction]]

WrappedAction = Callable[[int | list[int]], list[int]]
