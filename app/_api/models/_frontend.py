from ._attributes import _RequiresModelName
from ._attributes import _RequiresRecordIDs
from ._attributes import _SupportsSelectableFields

class Frontend:

    class Form(
        _RequiresModelName,
        _RequiresRecordIDs,
        _SupportsSelectableFields,
    ):
        ...
