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
    'selection',
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
    'has_corrections',
    'Tiene correcciones',
    'boolean'
)
def _assistance_registry_event__is_correction(
    ctx: Lylac.ComputeContext,
):

    # Obtención de instancia de corección de fecha y hora de registro
    registry_time_correction = ctx['registry_time_correction']
    # Obtención de instancia de corrección de tipo de registro
    status_correction = ctx['status_correction']

    # Evaluación de si el registro es una corrección
    is_correction = ctx.or_(
        registry_time_correction != None,
        status_correction != None,
    )

    return is_correction

@iacele.api.compute.register_field(
    'assistance.registry.event',
    'display_name',
    'Nombre a mostrar',
    'char',
)
def _assistance_registry_event__display_name(
    ctx: Lylac.ComputeContext,
):

    # Obtención del valor de tipo de registro efectivo
    status = ctx['status']

    name = ctx['employee_id.name']

    # Cómputo de etiqueta
    label = ctx.case(
        (status == 'check_in', 'Entrada'),
        (status == 'break_out', 'Inicio de comida'),
        (status == 'break_in', 'Fin de comida'),
        (status == 'check_out', 'Salida'),
        (status == 'undefined', 'Indefinido'),
        (status == 'null', 'Anulado'),
    )

    # Obtención de hora de registro
    time = ctx.cast('registry_time', 'time')

    # Cómputo de nombre a mostrar
    display_name = ctx.concat(label, ' (', name, ') [', time, ']')

    return display_name
