from ...._core import iacele
from ...._core import Lylac

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'start_time',
    'Hora de entrada',
    'time',
)
def _assistance_registry_day__start_time(
    ctx: Lylac.ComputeContext,
):

    # Obtención de campo agregado
    start_time__datetime = ctx.agg(
        'event_ids',
        'registry_time',
        'min',
        [('status', '=', 'check_in')],
    )

    # Conversión de tipo de dato
    start_time = ctx.cast(start_time__datetime, 'time')

    return start_time

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'end_time',
    'Hora de salida',
    'time',
)
def _assistance_registry_day__end_time(
    ctx: Lylac.ComputeContext,
):

    # Obtención de campo agregado
    end_time__datetime = ctx.agg(
        'event_ids',
        'registry_time',
        'max',
        [('status', '=', 'check_out')],
    )

    # Conversión de tipo de dato
    end_time = ctx.cast(end_time__datetime, 'time')

    return end_time

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'lunch_time',
    'Tiempo en comida',
    'duration',
)
def _assistance_registry_day__lunch_time(
    ctx: Lylac.ComputeContext,
):

    # Declaración de función de casteo de valor de fecha y hora de registro a formato de duración
    registry_time_to_duration_ttype: Lylac.ComputeFieldFn = lambda portal_ctx: (
        portal_ctx.cast(
            # Casteo a 'time' primero
            portal_ctx.cast(
                'registry_time',
                'time',
            ),
            # Casteo a 'duration'
            'duration',
        )
    )

    # Obtención de suma de valores de registro de hora fin de comida
    break_in_registry_time_sum = ctx.agg(
        'event_ids',
        registry_time_to_duration_ttype,
        'sum',
        [('status', '=', 'break_in')],
    )

    # Obtención de suma de valores de registro de hora inicio de comida
    break_out_registry_time_sum = ctx.agg(
        'event_ids',
        registry_time_to_duration_ttype,
        'sum',
        [('status', '=', 'break_out')],
    )

    # Obtención de conteo en inicios de hora de comida
    break_out_count = ctx.agg(
        'event_ids',
        'id',
        'count',
        [('status', '=', 'break_out')]
    )

    # Obtención de conteo en fines de hora de comida
    break_in_count = ctx.agg(
        'event_ids',
        'id',
        'count',
        [('status', '=', 'break_in')]
    )

    # Evaluación de si existe la misma cantidad en inicios y fines de comida
    same_break_in_and_out = ( break_out_count == break_in_count )

    # Obtención de duración en tiempo de comida
    precomputed_lunch_time = break_in_registry_time_sum - break_out_registry_time_sum
    # Obtencion de total en tiempo de comida
    lunch_time = ctx.case(
        (
            same_break_in_and_out,
            precomputed_lunch_time,
        ),
        default= None
    )

    return lunch_time

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'weekday',
    'Día de la semana',
    'char',
)
def _assistance_registry_day__weekday(
    ctx: Lylac.ComputeContext,
):

    # Obtención de la instancia de campo computada
    weekday = ctx.weekday('date')

    return weekday

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'allowed_start',
    'Inicio de jornada laboral permitido',
    'time',
)
def _assistance_registry_day__allowed_start(
    ctx: Lylac.ComputeContext,
):

    # Obtención de ID de desfase
    offset_id = ctx['offset_id.id']
    # Obtención hora de inicio de horario del día
    day_schedule_start_time = ctx['schedule_id.start_time']
    # Obtención de desfase de inicio de desfase vinculado
    linked_offset_start = ctx['offset_id.start_offset']

    # Evaluación de si existe desfase para el empleado en el día
    offset_exists = offset_id != None

    # Suma de inicio de horario laboral y desfase de tiempo del empleado
    precomputed_allowed_start = day_schedule_start_time + linked_offset_start

    # Obtención de cálculo
    allowed_start = ctx.case(
        (offset_exists, precomputed_allowed_start),
        default= day_schedule_start_time,
    )

    return allowed_start

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'allowed_end',
    'Fin de jornada laboral permitido',
    'time',
)
def _assistance_registry_day__allowed_end(
    ctx: Lylac.ComputeContext,
):

    # Obtención de ID de desfase
    offset_id = ctx['offset_id.id']
    # Obtención hora de inicio de horario del día
    day_schedule_end_time = ctx['schedule_id.end_time']
    # Obtención de desfase de inicio de desfase vinculado
    linked_offset_end = ctx['offset_id.end_offset']

    # Evaluación de si existe desfase para el empleado en el día
    offset_exists = offset_id != None

    # Suma de inicio de horario laboral y desfase de tiempo del empleado
    precomputed_allowed_end = day_schedule_end_time + linked_offset_end

    # Obtención de cálculo
    allowed_end = ctx.case(
        (offset_exists, precomputed_allowed_end),
        default= day_schedule_end_time,
    )

    return allowed_end

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'late_start',
    'Tiempo en entrada tardía',
    'duration',
)
def _assistance_registry_day__late_start(
    ctx: Lylac.ComputeContext,
):

    # Obtención de hora de inicio de jornada laboral
    start_time = ctx['start_time']
    # Obtención de hora de inicio permitida
    allowed_start = ctx['allowed_start']
    # Declaración de valor cero
    zero_value = '00:00:00'

    # Obtención de diferencia entre tiempo de entrada y tiempo permitido
    time_difference = start_time - allowed_start

    # Evaluación de si la diferencia de tiempo es menor a 0
    gt_zero = time_difference >= zero_value

    # Declaración de valor de minutos de entrada tardía
    late_start = ctx.case(
        (gt_zero, time_difference),
        default= zero_value,
    )

    return late_start

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'early_end',
    'Tiempo de salida anticipada',
    'duration',
)
def _assistance_registry_day__early_end(
    ctx: Lylac.ComputeContext,
):

    # Obtención de hora de inicio de jornada laboral
    end_time = ctx['end_time']
    # Obtención de hora de inicio permitida
    allowed_end = ctx['allowed_end']
    # Declaración de valor cero
    zero_value = '00:00:00'

    # Obtención de diferencia entre tiempo de entrada y tiempo permitido
    time_difference = allowed_end - end_time

    # Evaluación de si la diferencia de tiempo es menor a 0
    gt_zero = time_difference >= zero_value

    # Declaración de valor de minutos de entrada tardía
    late_start = ctx.case(
        (gt_zero, time_difference),
        default= zero_value,
    )

    return late_start

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'is_complete',
    'El registro de día está completado',
    'boolean',
)
def _assistance_registry_day__is_complete(
    ctx: Lylac.ComputeContext,
):

    # Obtención de la hora de inicio de jornada laboral
    start_time = ctx['start_time']
    # Obtención del tiempo en comida
    lunch_time = ctx['lunch_time']
    # Obtención de la hora de fin de jornada laboral
    end_time = ctx['end_time']

    # Evaluación de si todos los campos contienen datos válidos
    is_complete = ctx.and_(
        start_time != None,
        lunch_time != None,
        end_time != None,
    )

    return is_complete

@iacele.api.compute.register_field(
    'assistance.registry.day',
    'has_valid_events',
    'Contiene eventos válidos',
    'boolean',
)
def _assistance_registry_day__has_valid_events(
    ctx: Lylac.ComputeContext,
):

    # Obtención de conteo de eventos que sean diferentes a indefinido o nulo
    valid_events_count = ctx.agg(
        'event_ids',
        'id',
        'count',
        [('status', 'not in', ['null', 'undefined'])],
    )

    # Evaluación de si el conteo es mayor a 0
    has_valid_events = valid_events_count > 0

    return has_valid_events
