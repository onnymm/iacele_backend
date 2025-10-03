from app.orm._base import Base_ORM

class Account():

    _USER_FIELDS = [
        'id',
        'name',
        'login',
        'active',
        'sync',
        'role_ids',
        'profile_picture',
    ]

    def __init__(
        self,
        instance: Base_ORM
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

    def get_user_context(
        self,
        user_id: int,
    ):

        # Obtención de los datos del usuario
        [ user_data ] = self._main._db.read(
            self._main._db._ROOT_USER,
            'base.users',
            user_id,
            self._USER_FIELDS,
        )

        # Obtención de las IDs de grupos
        group_ids = self._main._db.get_value(
            self._main._db._ROOT_USER,
            'base.users.role',
            user_data['role_ids'],
            'group_ids',
        )

        # Obtención de los nombres de grupos
        groups = self._main._db.read(
            self._main._db._ROOT_USER,
            'base.model.access.groups',
            group_ids,
            ['name'],
        )

        user_data['groups'] = groups

        return user_data
