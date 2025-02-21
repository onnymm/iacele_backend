from fastapi import Body
from pydantic import BaseModel
from datetime import datetime

class BaseRecord(BaseModel):
    user: str | None = None
    name: str | None = None
    odoo_id: int | None = None

class BaseUser(BaseModel):
    user: str
    name: str
    odoo_id: int

class UserNewData(BaseModel):
    user: str | None = None
    name: str | None = None
    odoo_id: int | None = None

class UserData(BaseUser):
    password: str

class UserInDB(UserData, BaseRecord):
    """
    Formato de usuario en la base de datos:
    - `id` `str`: ID del usuario.
    - `user` `str`: Nombre de usuario.
    - `name` `str`: Nombre completo del usuario.
    - `odoo_id` `int`: ID del usuario en Odoo.
    - `password` `str`: Contraseña hasheada del usuario.
    """
    id: int

class NewUserTemplate(BaseModel):
    odoo_id: int = Body()

class ChangePassword(BaseModel):
    """
    Formato de información recibida para cambiar contraseña:
    - `current_password` `str`: Contraseña actual.
    - `new_password` `str`: Nueva contraseña.
    """
    current_password: str = Body()
    new_password: str = Body()

class AlreadyRegistered(BaseModel):
    detail: str = 'El usuario ya existe en la base de datos de iaCele.'
