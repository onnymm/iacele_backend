from ...._core import Lylac
from ...._core import iacele
from lylac import NewRecord
from lylac import Preset
from lylac import Template
from lylac import TType

class _LocationWarehouse(Template.Record):
    data_name: TType.Char

@iacele.api.automations.register(
    'create',
    'location.warehouse',
    [('data_name', 'char', lambda ctx: ctx.concat('location_warehouse.', ctx['location_number']) )],
)
def _location_warehouse__register_model_data(ctx: Lylac.AutomationContext[_LocationWarehouse]) -> None:

    # Inicialización de datos a crear
    data_to_create: list[dict] = []

    # Iteración por cada registro creado
    for record in ctx.records:
        # Construcción de registro a crear
        record_to_create: NewRecord[Preset.BaseModelData] = {
            'res_id': record['id'],
            'name': record['data_name'],
            'model_name': 'location.warehouse',
        }
        # Se añade el registro a la lista de registros a crear
        data_to_create.append(record_to_create)

    # Creación de registros
    ctx.create(
        'base.model.data',
        data_to_create,
    )
