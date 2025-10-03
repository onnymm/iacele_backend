from typing import (
    Generic,
    TypedDict,
    Union,
)
from lylac._module_types import (
    ModelName,
    TType,
)
from ._base import (
    CUSTOM_MODELS,
    _T,
)

BACKEND_MODELS = Union[ModelName, CUSTOM_MODELS]

class SelectionValue(TypedDict):
    id: int
    name: str
    label: str

class FieldMetadata(TypedDict, Generic[_T]):
    id: int
    name: str
    label: str
    ttype: TType
    help_info: str | None
    model: BACKEND_MODELS | None
    selection_ids: list[_T]
    readonly: bool
    is_computed: bool
