from ._attributes import _RequiresModelName
from ._attributes import _RequiresRecordID
from ._attributes import _SupportsSelectableFields

class Frontend:

    class Form(
        _RequiresModelName,
        _RequiresRecordID,
        _SupportsSelectableFields,
    ):
        ...
