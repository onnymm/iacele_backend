from fastapi import APIRouter, status
from app.constants import tags
from app.core import tasks

router = APIRouter(
    prefix= '/tasks',
    tags= [tags.tasks],
)

@router.post(
    '/update_users',
    status_code= status.HTTP_200_OK,
    name= 'Actualición de usuarios en Odoo',
)
async def _update_users() -> bool:
    """
    ## Actualización de usuarios de Odoo en iaCele
    Esta tarea actualiza los usuarios de Odoo, registrando nuevos usuarios en
    iaCele o desactivando los faltantes en Odoo.
    """

    # Ejecución de la tarea
    tasks.update_users()

    # Retorno de finalización de proceso
    return True
