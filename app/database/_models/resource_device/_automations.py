from lylac import Preset
from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele

class _ResourceDevice(Template.Record):
    data_name: TType.Char

@iacele.api.automations.register(
    'create',
    'resource.device',
    [
        ('data_name', 'char', lambda ctx: ctx.concat('resource_device.', ctx['location_id.short_name']))
    ],
)
def _resource_device__create_resource_id(ctx: Lylac.AutomationContext[_ResourceDevice]):

    # Inicialización de lista de datos a crear
    data_to_create: list[Preset.BaseModelData] = []
    # Iteración por cada registro de empleado creado
    for record in ctx.records:
        # Construcción de datos
        new_record: Preset.BaseModelData = {
            'res_id': record['id'],
            'name': record['data_name'],
            'model_name': 'resource.device',
        }
        # Se añaden éstos a lista de datos a crear
        data_to_create.append(new_record)

    # Creación de datos
    ctx.create('base.model.data', data_to_create)
