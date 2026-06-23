from .._core import Lylac
from .._constants import PRESET_PROFILE_FIELDS

def me(ctx: Lylac.ExecutionContext):

    # Obtención de los datos del usuario de la sesión
    [ user_data ] = ctx.read(
        'base.users',
        ctx.uid,
        PRESET_PROFILE_FIELDS,
    )

    return user_data
