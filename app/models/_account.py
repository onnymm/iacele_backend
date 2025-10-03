from ._base import _BaseRecord

class _Group(_BaseRecord):
    """
    ### Grupo de acceso
    Grupo de acceso del usuario.

    - `id`: ID del grupo.
    - `name`: Nombre del grupo.
    """
    ...

class SessionUser(_BaseRecord):
    """
    ### Usuario de la sesión
    Datos del usuario de la sesión activa.

    - `login`: Nombre de usuario para inicio de sesión.
    - `active`: El usuario está activo.
    - `sync`: La sincronización del usuario está activa.
    - `role_ids`: IDs de roles de usuario.
    - `groups`: Grupos de acceso del usuario.
    """
    login: str
    active: bool
    sync: bool
    role_ids: list[int]
    groups: list[_Group]
    profile_picture: str | None
