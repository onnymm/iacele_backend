from app.core import iacele
from lylac.utils import ComputeContext

# ----------------------------- CAMPOS COMPUTADOS -----------------------------

@iacele.core.register_computed_field(
    'carpentry.project',
    'total_time',
    'Tiempo total del proyecto',
    'duration',
)
def _carpentry_project__total_time(
    ctx: ComputeContext,
):

    # Obtención de la suma de la duración de todas las actividades
    field = ctx.agg('activity_ids.duration', 'sum')

    return field

@iacele.core.register_computed_field(
    'carpentry.project',
    'done_activities',
    'Actividades completadas',
    'integer',
)
def _carpentry_project__done_activities(
    ctx: ComputeContext,
):

    # Obtención del conteo de las actividades completadas
    field = ctx.agg('activity_ids', 'count', [('done', '=', True)])

    return field

@iacele.core.register_computed_field(
    'carpentry.project',
    'remaining_time',
    'Tiempo restante estimado',
    'duration',
)
def _carpentry_project__remaining_time(
    ctx: ComputeContext,
):

    # Obtención de la suma de la duración de las actividades no completadas
    field = ctx.agg('activity_ids.duration', 'sum', [('done', '=', False)])

    return field

@iacele.core.register_computed_field(
    'carpentry.project',
    'remaining_activities',
    'Actividades restantes',
    'integer',
)
def _carpentry_project__remaining_activities(
    ctx: ComputeContext,
):

    # Obtención del conteo de las actividades no completadas
    field = ctx.agg('activity_ids', 'count', [('done', '=', False)])

    return field
