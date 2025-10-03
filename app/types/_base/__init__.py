from typing import Union
from lylac._module_types import ModelName
from ._custom_models import CUSTOM_MODELS
from ._generics import _T

BACKEND_MODELS = Union[ModelName, CUSTOM_MODELS]
