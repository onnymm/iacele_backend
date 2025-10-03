from ._base import (
    _RequiresItemsPerPage,
    _RequiredModelName,
    _RequiresPageNumber,
    _RequiresRecordID,
    _SupportsFiltering,
    _SupportsSorting,

    _Count,
    _HasFieldsMetadata,
    _HasRecordData,
    _HasRecordsData,
    _ModelLabel,
)

class Frontend:

    class List:

        class ListRequest(
            _SupportsSorting,
            _SupportsFiltering,
            _RequiresItemsPerPage,
            _RequiresPageNumber,
            _RequiredModelName,
        ):
            ...

        class ListResponse(
            _HasRecordsData,
            _HasFieldsMetadata,
            _Count,
            _ModelLabel,
        ):
            ...

    class Form:

        class FormRequest(
            _RequiresRecordID,
            _RequiredModelName,
        ):
            ...

        class FormResponse(
            _HasFieldsMetadata,
            _HasRecordData,
        ):
            ...
