from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele
from ...._typing import Weekday

class _AssistanceRegistryDay(Template.Record):
    employee_id: TType.Integer
    weekday: TType.Selection[Weekday]

@iacele.api.automations.register(
    'create',
    'assistance.registry.day',
    [
        ('employee_id.id', 'employee_id'),
        ('weekday', 'char', lambda ctx: ctx.weekday('date')),
    ],
)
def _assistance_registry_day__add_schedule(ctx: Lylac.AutomationContext[_AssistanceRegistryDay]):

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de la ID del registro
        record_id = record['id']
        # Obtención de la ID del empleado
        employee_id = record['employee_id']
        # Obtención del valor de día de la semana
        weekday_value = record['weekday']
        # Actualización del registro
        ctx.update(
            'assistance.registry.day',
            record_id,
            {'schedule_id': ctx.get_resource_id(f'schedule_week.{weekday_value}')}
        )

        # Búsqueda de desfase para el empleado en el día
        found_results = ctx.search(
            'schedule.week.offset',
            [
                '&',
                    ('employee_id.id', '=', employee_id),
                    ('weekday', '=', weekday_value),
            ],
        )
        # Si fueron encontrados resultados...
        if found_results:
            # Obtención de la ID de desfase
            [ offset_id ] = found_results
            # Actualización del registro
            ctx.update(
                'assistance.registry.day',
                record_id,
                {'offset_id': offset_id}
            )
