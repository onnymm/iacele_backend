from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele

class _ScheduleWeek(Template.Record):
    data_name: TType.Char

@iacele.api.automations.register(
    'create',
    'schedule.week',
    [('data_name', 'char', lambda ctx: ctx.concat('schedule_week.', ctx['weekday']) )],
)
def _schedule_week__create_model_data(ctx: Lylac.AutomationContext[_ScheduleWeek]):

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de ID de registro
        record_id = record['id']
        # Obtención del nombre de datos computado
        data_name = record['data_name']

        # Creación de registro de datos
        ctx.create(
            'base.model.data',
            {
                'res_id': record_id,
                'model_name': 'schedule.week',
                'name': data_name,
            },
        )
