from lylac.utils import (
    ActionContext,
    AutomationContext,
    ModelRecordData,
)
from app.core import iacele

# -------------------------------- ACCIONES ------------------------------------

@iacele.core.register_action(
    'base.users',
    'activate',
)
def _activate(
    ctx: ActionContext[ModelRecordData.BaseUsers],
) -> None:

    # Obtencón de la ID del usuario
    user_id = ctx.data['id']

    # Activación del usuario
    ctx.update(
        'base.users',
        user_id,
        {'active': True},
    )

@iacele.core.register_action(
    'base.users',
    'deactivate',
)
def _deactivate(
    ctx: ActionContext[ModelRecordData.BaseUsers],
) -> None:

    # Obtencón de la ID del usuario
    user_id = ctx.data['id']

    # Desactivación del usuario
    ctx.update(
        'base.users',
        user_id,
        {'active': False},
    )

@iacele.core.register_action(
    'base.users',
    'reset_password',
)
def _reset_password(
    ctx: ActionContext[ModelRecordData.BaseUsers],
) -> None:

    # Obtención de la ID del usuario
    user_id = ctx.data['id']

    # Se restablece la contraseña del usuario
    ctx.reset_password(user_id)

@iacele.core.register_action(
    'base.users',
    'sync_off',
)
def _sync_off(
    ctx: ActionContext[ModelRecordData.BaseUsers],
) -> None:

    # Obtencón de la ID del usuario
    user_id = ctx.data['id']

    # Desactivación del usuario
    ctx.update(
        'base.users',
        user_id,
        {'sync': False},
    )

@iacele.core.register_action(
    'base.users',
    'sync_on',
)
def _sync_on(
    ctx: ActionContext[ModelRecordData.BaseUsers],
) -> None:

    # Obtencón de la ID del usuario
    user_id = ctx.data['id']

    # Desactivación del usuario
    ctx.update(
        'base.users',
        user_id,
        {'sync': True},
    )

# ---------------------------- AUTOMATIZACIONES -------------------------------

@iacele.core.register_automation(
    'base.users',
    'create',
)
def _base_users__add_base_user_role(
    ctx: AutomationContext.Individual,
) -> None:

    # Obtención de la ID del usuario
    user_id = ctx.data['id']

    # Actualización de su rol
    ctx.update(
        'base.users',
        user_id,
        {
            'role_ids': [
                (
                    'add',
                    [2]
                )
            ]
        }
    )
