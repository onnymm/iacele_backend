from fastapi import APIRouter, status, Depends
from app.models.actions import Action
from app.models import UserInDB
from app.security import get_current_user
from app.core.actions import server_actions


router = APIRouter(
    prefix= '/actions',
    tags= ['Acciones'],
)

@router.post(
    '/execute',
    name= 'Ejecutar acción',
    status_code= status.HTTP_200_OK,
)
async def _execute(
    action: Action,
    _: UserInDB = Depends(get_current_user),
) -> bool:

    server_actions[action.table][action.action](action.record_ids)

    return True
