import pandas as pd
from app import db_connection, odoo
from app.core.actions.utils import find_symmetric_diff
from app.models.actions import Action
from app.security.auth import hash_password
from app.settings.settings import settings
from .base import IACele

@IACele.register_action('base.users')
def activate_user(params: Action) -> None:
    db_connection.update(
        'base.users',
        params.record_ids,
        {'active': True}
    )

@IACele.register_action('base.users')
def deactivate_user(params: Action) -> None:
    db_connection.update(
        'base.users',
        params.record_ids,
        {'active': False}
    )

@IACele.register_action('base.users')
def reset_password(params: Action) -> None:
    db_connection.update(
        'base.users',
        params.record_ids,
        {'password': hash_password(settings.base.NEW_USER_PASSWORD)}
    )

@IACele.register_action('base.users')
def create(params: Action) -> None:
    data = odoo.read('res.users', params.record_ids, ['name', 'login'], output= 'dict')
    return [
        {
            'user': record['login'],
            'name': record['name'],
            'odoo_id': record['id'],
            'password': hash_password(settings.base.NEW_USER_PASSWORD),
            'active': True,
        } for record in data
    ]

@IACele.register_task('base.users')
def update_users():

    def wrapped_create(record_ids: int | list[int]):
        action = Action(table= 'base.users', action= 'create', record_ids= record_ids, data= {})
        return create(action)

    def wrapped_deactivate_user(record_ids: int | list[int]):
        action = Action(table= 'base.users', action= 'deactivate_user', record_ids= record_ids, data= {})
        return deactivate_user(action)

    users_api = odoo.search_read('res.users', [], ['name', 'login'])
    users_db: pd.DataFrame = db_connection.search_read('base.users', fields=['odoo_id'], output_format= 'dataframe')

    find_symmetric_diff(users_db, users_api, 'odoo_id', 'id', wrapped_create, wrapped_deactivate_user)
