from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele

class _AssistanceRegistryEvent(Template.Record):
    date: TType.Date
    employee_id: TType.Integer

@iacele.api.automations.register(
    'create',
    'assistance.registry.event',
    [
        ('employee_id.id', 'employee_id'),
        ('date', 'date', lambda ctx: ctx.cast( ctx.cast('original_registry_time', 'date'), 'char' )),
    ]
)
def _assistance_registry_event__create_day_record(ctx: Lylac.AutomationContext[_AssistanceRegistryEvent]):

    # Iteración por cada registro de evento creado
    for record in ctx.records:
        # Obtención de la ID del registro
        record_id = record['id']
        # Obtención de la fecha del evento
        event_date = record['date']
        # Obtención de la ID del empleado
        employee_id = record['employee_id']

        # Búsqueda de registro de día existente
        found_results = ctx.search(
            'assistance.registry.day',
            [
                '&',
                    ('date', '=', event_date),
                    ('employee_id.id', '=', employee_id),
            ],
        )

        # Si fueron encontrados...
        if found_results:
            # Obtención de la ID del registro de día
            [ day_id ] = found_results
        # Si no fueron encontrados resultados...
        else:
            [ day_id ] = ctx.create(
                'assistance.registry.day',
                {
                    'employee_id': employee_id,
                    'date': event_date,
                },
            )

        # Actualización de ID de día en el registro de evento
        ctx.update(
            'assistance.registry.event',
            record_id,
            {'day_id': day_id},
        )
