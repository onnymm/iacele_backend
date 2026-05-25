from ._attributes import _RequiresModelName
from ._attributes import _RequiresRecordID
from ._attributes import _RequiresName

class Server:

    class Action(
        _RequiresModelName,
        _RequiresRecordID,
        _RequiresName,
    ):
        ...

    class Tast(
        _RequiresName,
    ):
        ...
