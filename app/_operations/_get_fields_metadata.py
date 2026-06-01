from .._core import Lylac
from .._api.models import Metadata
from .._settings import PARAMETERS

def operation_get_fields_metadata(
    ctx: Lylac.ExecutionContext,
    params: Metadata.Fields,
):

    # Lectura de campos
    fields_metadata = ctx.search_read(
        'base.model.field',
        [('model_id.model', '=', params.model_name)],
        PARAMETERS.FIELDS_TO_READ.FIELDS_METADATA,
    )

    return fields_metadata
