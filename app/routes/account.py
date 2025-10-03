from fastapi import (
    APIRouter,
    status,
    Depends,
)
from app.constants import TAG
from app.core import iacele
from app.security import authenticate_user
from app.models import SessionUser

router = APIRouter(
    prefix= '/account',
    tags= [TAG.ACCOUNT],
)

@router.get(
    '/me',
    status_code= status.HTTP_200_OK,
    name= 'Mi cuenta',
)
async def _me(
    user_id: int = Depends(authenticate_user),
) -> SessionUser:
    """
    ### Mi cuenta
    Obtención de los datos del usuario de la sesión activa.
    """

    # Lectura del usuario
    user_data = iacele.orm.account.get_user_context(user_id)

    return user_data
