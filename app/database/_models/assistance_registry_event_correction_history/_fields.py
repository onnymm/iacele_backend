from ...._core import iacele
from ...._core import Lylac

@iacele.api.compute.register_field(
    'assistance.registry.event.correction.history',
    'display_name',
    'Nombre a mostrar',
    'char',
)
def _assistance_registry_event__registry_time(
    ctx: Lylac.ComputeContext,
):

    status = ctx.case(
        (ctx['new_status'] == 'check_in', 'Entrada'),
        (ctx['new_status'] == 'break_out', 'Inicio de comida'),
        (ctx['new_status'] == 'break_in', 'Fin de comida'),
        (ctx['new_status'] == 'check_out', 'Fin de comida'),
        (ctx['new_status'] == 'undefined', 'Indefinido'),
        (ctx['new_status'] == 'null', 'Anulado'),
        default= '',
    )

    casted_registry_time = ctx.cast(ctx['new_registry_time'], 'char')

    status_not_empty = ctx['new_status'] != None
    registry_time_not_empty = ctx['new_registry_time'] != None

    both_corrections_not_empty = ctx.and_(status_not_empty, registry_time_not_empty)

    correction_detail = ctx.case(
        (both_corrections_not_empty, ctx.concat(status, ', ', casted_registry_time)),
        (status_not_empty, status),
        default= casted_registry_time,
    )

    move_type = ctx.case(
        (ctx['move_type'] == 'undo', 'Deshacer cambios'),
        (ctx['move_type'] == 'correction', ctx.concat('Corrección: (', correction_detail, ')')),
    )

    user_name = ctx['create_uid.name']

    correction_time = ctx.func.substring(ctx.cast(ctx['create_date'], 'char'), 1, 19)

    display_name = ctx.concat('[', move_type, '] ', user_name, ' - ', correction_time)

    return display_name
