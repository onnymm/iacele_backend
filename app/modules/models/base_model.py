from app.core import iacele
from lylac.utils import AutomationContext, ModelRecordData

@iacele.core.register_automation(
    'base.model',
    'create',
    ['id', 'name', 'label']
)
def _base_model__add_preset_permissions(
    ctx: AutomationContext.Individual
) -> None:

    # Obtención de los valores
    model_id = ctx.data['id']
    name = ctx.data['name']
    label = ctx.data['label']

    # Creación de los datos de permisos
    user_permission = {
        'name': f'{name}_user',
        'label': f'{label} / Usuario',
        'model_id': model_id,
        'perm_read': True,
    }
    admin_permission = {
        'name': f'{name}_admin',
        'label': f'{label} / Administrador',
        'model_id': model_id,
        'perm_create': True,
        'perm_read': True,
        'perm_update': True,
        'perm_delete': True,
    }

    # Se añade el permiso de usuario
    ctx.update(
        'base.model.access.groups',
        1,
        { 'permission_ids': [ ( 'create', user_permission, ) ] }
    )

    # Se añade el permiso de administrador
    ctx.update(
        'base.model.access.groups',
        2,
        { 'permission_ids': [ ( 'create', admin_permission, ) ] }
    )
