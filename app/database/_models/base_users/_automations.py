from ...._core import Lylac
from ...._core import iacele

@iacele.api.automations.register(
    'update',
    'base.users',
)
def _base_users__notify_update(ctx: Lylac.AutomationContext):

    # Iteración por cada registro actualizado
    for record in ctx.records:
        # Se realiza notificación de cambio
        ctx.notify('profile.update', record['id'])
