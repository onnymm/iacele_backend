from lylac import Preset
from lylac import Template
from lylac import TType
from ...._core import Lylac
from ...._core import iacele

class _HREmployee(Template.Record):
    name: TType.Char

@iacele.api.automations.register(
    'create',
    'hr.employee',
    [
        ('name', 'char', lambda ctx: ctx.concat('hr_employee.', ctx['odoo_id'])),
    ]
)
def _hr_employee__create_resource_id(ctx: Lylac.AutomationContext[_HREmployee]):

    # Inicialización de lista de datos a crear
    data_to_create: list[dict] = []
    # Iteración por cada registro de empleado creado
    for record in ctx.records:
        # Construcción de datos
        new_record: Preset.BaseModelData = {
            'res_id': record['id'],
            'name': record['name'],
            'model_name': 'hr.employee',
        }
        # Se añaden éstos a lista de datos a crear
        data_to_create.append(new_record)

    # Creación de datos
    ctx.create('base.model.data', data_to_create)
