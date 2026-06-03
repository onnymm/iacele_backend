from ._attributes import _RequiresModelName
from ._attributes import _RequiresRecordData
from ._attributes import _RequiresRecordsData
from ._attributes import _SupportsSegmentation
from ._attributes import _SupportsFiltering
from ._attributes import _RequiresRecordIDs
from ._attributes import _SupportsSelectableFields
from ._attributes import _SupportsSorting

class CRUD:

    class Create(
        _RequiresModelName,
        _RequiresRecordsData,
    ):
        ...

    class Search(
        _RequiresModelName,
        _SupportsFiltering,
        _SupportsSegmentation,
    ):
        ...

    class Read(
        _RequiresModelName,
        _RequiresRecordIDs,
        _SupportsSelectableFields,
        _SupportsSorting,
    ):
        ...

    class SearchRead(
        _RequiresModelName,
        _SupportsFiltering,
        _SupportsSelectableFields,
        _SupportsSegmentation,
        _SupportsSorting,
    ):
        ...

    class SearchCount(
        _RequiresModelName,
        _SupportsFiltering,
    ):
        ...

    class Update(
        _RequiresModelName,
        _RequiresRecordIDs,
        _RequiresRecordData,
    ):
        ...

    class Delete(
        _RequiresModelName,
        _RequiresRecordIDs,
    ):
        ...
