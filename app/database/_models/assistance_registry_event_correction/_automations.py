from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele
from typing import Literal

class _AssistanceRegistryEvent(Template.Record):
    event_id: TType.Integer
    status: TType.Selection[Literal['check_in', 'break_out', 'break_in', 'check_out', 'null']]
    registry_time: TType.Datetime

@iacele.api.automations.register(
    'create',
    'assistance.registry.event.correction',
    [('event_id.id', 'event_id'), 'status', 'registry_time'],
)
def _assistance_registry_event_correction__consume(ctx: Lylac.AutomationContext[_AssistanceRegistryEvent]):

    # Iteración por cada registro creado
    for record in ctx.records:

        # Actualización del evento original
        ctx.update(
            'assistance.registry.event',
            record['event_id'],
            {
                'status_correction': record['status'],
                'registry_time_correction': record['registry_time'],
            }
        )
