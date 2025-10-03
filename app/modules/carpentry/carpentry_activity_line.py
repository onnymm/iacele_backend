from app.core import iacele
from lylac.utils import (
    ActionContext,
    ComputeContext,
)

# ----------------------------- CAMPOS COMPUTADOS -----------------------------

@iacele.core.register_computed_field(
    'carpentry.activity.line',
    'end_date',
    'Fin',
    'datetime',
)
def _carpentry_activity_line__end_date(
    ctx: ComputeContext,
):

    # Obtención del valor
    field = ctx['start_date'] + ctx['duration']

    return field

# ------------------------------- ACCIONES ------------------------------------

@iacele.core.register_action(
    'carpentry.activity.line',
    'mark_as_done',
)
def _carpentry_activity_line__mark_as_done(
    ctx: ActionContext,
):

    # Obtención de la ID del registro
    record_id = ctx.data['id']

    # Se actualiza el estado del registro
    ctx.update('carpentry.activity.line', record_id, {'done': True})

@iacele.core.register_action(
    'carpentry.activity.line',
    'mark_as_undone',
)
def _carpentry_activity_line__mark_as_undone(
    ctx: ActionContext
):

    # Obtención de la ID del registro
    record_id = ctx.data['id']

    # Se actualiza el estado del registro
    ctx.update('carpentry.activity.line', record_id, {'done': False})
