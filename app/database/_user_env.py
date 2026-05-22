from .._src import Lylac
from .._core import iacele

@iacele.api.env.register_value('location_id')
def _location_id(ctx: Lylac.ExecutionContext):

    # Obtención del registro con campo computado
    [ record ] = ctx.search_read('hr.employee', [('user_id.id', '=', ctx.uid)], ['location_id.id'])
    # Extracción del valor de ID de ubicación
    location_id = record['location_id.id']

    return location_id
