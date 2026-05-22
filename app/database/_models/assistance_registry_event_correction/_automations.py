from lylac import CriteriaStructure
from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele
from ...._typing.models import APIStatus

class _AssistanceRegistryEventCorrection(Template.Record):
    employee_id: TType.Integer
    registry_time: TType.Datetime
    status: TType.Selection[APIStatus]

@iacele.api.automations.register(
    'create',
    'assistance.registry.event.correction',
    [
        ('employee_id.id', 'employee_id'),
        'registry_time',
        'status',
    ],
)
def _assistance_registry_event_correction__automation(ctx: Lylac.AutomationContext[_AssistanceRegistryEventCorrection]):

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de ID de empleado
        employee_id = record['employee_id']
        # Obtención de fecha y hora de registro
        registry_time = record['registry_time']
        # Obtención de tipo de registro
        status = record['status']
        # Creación de filtro
        search_criteria: CriteriaStructure = [
            '&',
                ('employee_id.id', '=', employee_id),
                ('original_registry_time', '=', registry_time),
        ]
        # Búsqueda de registros encontrados
        found_results = ctx.search('assistance.registry.event', search_criteria)
        # Si fue encontrado un resultado...
        if found_results:
            # Obtención de ID de registro a modificar
            [ record_to_modify ] = found_results
            # Modificación de registro
            ctx.update(
                'assistance.registry.event',
                record_to_modify,
                {
                    'registry_time_correction': registry_time,
                    'status_correction': status,
                },
            )

        # Si no fueron encontrados resultados...
        else:
            ctx.create(
                'assistance.registry.event',
                {
                    'employee_id': employee_id,
                    'original_registry_time': registry_time,
                    'original_status': status,
                    'from_api': False,
                },
            )
