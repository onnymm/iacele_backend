from fastapi import APIRouter, status, Query, Body, Depends
from app.security.auth import hash_password, get_current_user, authenticate_user
from app.database import db_connection
from app.models.users import UserNewData, UserData, UserInDB
from app.utils.data_transformation import remove_nonetypes

router = APIRouter()

@router.post(
    "/",
    status_code= status.HTTP_201_CREATED,
    name= "Registro",
)
async def _register(user: UserData = Body()):
    """
    ## Registro de nuevo usuario
    Este endpoint realiza el registro de un nuevo usuario en la aplicación.
    """

    # Hash de la contraseña
    user.password = hash_password(user.password)

    # Registro del usuario en la base de datos
    db_connection.create("users", user.model_dump())

    # Respuesta para el API
    return {"message": "Usuario creado con éxito"}

@router.get(
    "/",
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
    [ data ] = db_connection.read("users", [user.id], fields= fields, output_format="dict")

    # Retorno de la información
    return data

@router.patch(
    "/",
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
    db_connection.update("users", [user.id], {**data})

    # Retorno de respuesta si la modificación se realizó con éxito
    return True

@router.delete(
    "/",
    status_code= status.HTTP_200_OK,
    name= "Eliminar cuenta",
)
async def _delete(password: str = Body(), user: UserInDB = Depends(get_current_user)):
    """
    ## Eliminación de usuario
    Este endpoint elimina al usuario actual. Se requiere ingresar la contraseña nuevamente.
    """

    # Si el usuario es autenticado correctamente se elimina la cuenta
    if authenticate_user(user.user, password):
        db_connection.delete("users", [user.id])

        # Retorno de respuesta si la modificación se realizó con éxito
        return True
