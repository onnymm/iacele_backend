from ...._core import iacele
from ...._core import Lylac

@iacele.api.compute.register_field(
    'assistance.registry.event',
    'registry_time',
    'Fecha y hora de registro',
    'datetime',
)
def _assistance_registry_event__registry_time(
    ctx: Lylac.ComputeContext,
):

    # Obtención de instancia de campo de corrección de fecha y hora de registro
    registry_time_correction = ctx['registry_time_correction']
    # Obtención de instancia de campo de fecha y hora de registro original
    original_registry_time = ctx['original_registry_time']

    # Cómputo de fecha y hora de registro definitivo
    registry_time = ctx.case(
        # Si la corrección no es nula, se usa ésta
        (registry_time_correction != None, registry_time_correction),
        # Por defecto se usa la hora original
        default= original_registry_time
    )

    return registry_time

@iacele.api.compute.register_field(
    'assistance.registry.event',
    'status',
    'Tipo de registro',
    'datetime',
)
def _assistance_registry_event__status(
    ctx: Lylac.ComputeContext,
):

    # Obtención de instancia de campo de corrección de tipo de registro
    status_correction = ctx['status_correction']
    # Obtención de instancia de campo de tipo de registro original
    original_status = ctx['original_status']

    # Cómputo de tipo de registro definitivo
    status = ctx.case(
        # Si la corrección no es nula, se usa ésta
        (status_correction != None, status_correction),
        # Por defecto se usa la hora original
        default= original_status
    )

    return status

@iacele.api.compute.register_field(
    'assistance.registry.event',
    'is_correction',
    'Es corrección',
    'boolean'
)
def _assistance_registry_event__is_correction(
    ctx: Lylac.ComputeContext,
):

    # Obtención de instancia de corección de fecha y hora de registro
    registry_time_correction = ctx['registry_time_correction']
    # Obtención de valor de si el registro proviene desde la API de HikVision
    from_api = ctx['from_api']

    # Evaluación de si el registro es una corrección
    is_correction = ctx.or_(
        registry_time_correction != None,
        from_api == False,
    )

    return is_correction
