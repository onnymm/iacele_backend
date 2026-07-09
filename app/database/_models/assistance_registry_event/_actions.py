from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele

@iacele.api.actions.register(
    'assistance.registry.event',
    'undo_corrections',
)
def _assistance_registry_event__undo_corrections(ctx: Lylac.ActionContext):

    # Se actualiza el registro
    ctx.update(
        'assistance.registry.event',
        ctx.record_id,
        {
            'status_correction': None,
            'registry_time_correction': None,
            # Generación de historial
            'correction_history_ids': {
                'create': [
                    {
                        'move_type': 'undo',
                    },
                ],
            },
        },
    )
