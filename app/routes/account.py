from fastapi import APIRouter, status, Query, Body, Depends
from fastapi.exceptions import HTTPException
from app.constants.tags import tags
from app.security.auth import hash_password, get_current_user, authenticate_user
from app.database import db_connection
from app.models.users import UserNewData, UserInDB, ChangePassword
from app.utils.data_transformation import remove_nonetypes

router = APIRouter(
    prefix= '/account',
    tags= [tags.account],
)

@router.get(
    "/me",
    status_code= status.HTTP_200_OK,
    name= "Mi cuenta"
)
async def _get(user: UserInDB = Depends(get_current_user)):
    """
    ## Mi cuenta
    Este endpoint muestra la información del usuario actual.
    """

    # Campos a retornar
    fields = ['id', 'user', 'name', 'odoo_id', 'create_date', 'write_date']

    # Obtención del usuario
    [ data ] = db_connection.read('base.users', [user.id], fields= fields, output_format="dict")

    # Retorno de la información
    return data

@router.patch(
    "/me",
    status_code= status.HTTP_200_OK,
    name= "Modificar datos",
)
async def _update(changes_data: UserNewData = Body(), user: UserInDB = Depends(get_current_user)):
    """
    ## Modificación de datos del usuario actual
    Este endpoint realiza modificación de datos del usuario actual.
    """

    # Remoción de todos los atributos indefinidos
    data = remove_nonetypes( changes_data.model_dump() )

    # Modificación del usuario actual
    db_connection.update('base.users', [user.id], {**data})

    # Retorno de respuesta si la modificación se realizó con éxito
    return True

@router.patch(
    '/change_password',
    status_code= status.HTTP_200_OK,
    name= 'Cambiar contraseña',
)
async def _change_password(
    data: ChangePassword,
    user: UserInDB = Depends(get_current_user)
):
    """
    ## Cambiar contraseña
    Este endpoint cambia la contraseña del usuario actual autenticado

    ----
    ### Parámetros
    - `current_password`: Contraseña actual del usuario para confirmar que
    es éste quien solicita el cambio de contraseña.
    - `new_password`: Nueva contraseña del usuario.
    """

    # Si la contraseña actual es correcta...
    if authenticate_user(user.user, data.current_password):
        # Se cambia la contraseña en la base de datos
        db_connection.update('base.users', user.id, {'password': hash_password(data.new_password)})
        # Retorno de confirmación de cambios
        return True
    # Si la contraseña actual no es correcta
    else:
        # Se retorna un error 401
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Contraseña actual incorrecta",
        )
