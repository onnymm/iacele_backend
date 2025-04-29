from fastapi import APIRouter, status, Depends
from app.models.actions import Action, Task
from app.models import UserInDB
from app.security import get_current_user
from app.core.actions.base import IACele

router = APIRouter(
    prefix= '/server',
    tags= ['Servidor'],
)

@router.post(
    '/action',
    name= 'Ejecutar acción',
    status_code= status.HTTP_200_OK,
)
async def _action(
    action: Action,
    _: UserInDB = Depends(get_current_user),
) -> bool:

    IACele.execute_action(action)

    return True

@router.post(
    '/task',
    name= 'Ejecutar tarea',
    status_code= status.HTTP_200_OK,
)
async def _task(
    task: Task,
    _: UserInDB = Depends(get_current_user),
) -> bool:

    IACele.execute_task(task)

    return True
