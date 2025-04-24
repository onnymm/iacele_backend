from app import db_connection
from app.security.auth import hash_password
from app.settings.settings import settings

def activate_user(id: int | list[int]) -> None:
    db_connection.update('base.users', id, {'active': True})

def deactivate_user(id: int | list[int]) -> None:
    db_connection.update('base.users', id, {'active': False})

def reset_password(id: int | list[int]) -> None:
    db_connection.update('base.users', id, {'password': hash_password(settings.base.NEW_USER_PASSWORD)})
