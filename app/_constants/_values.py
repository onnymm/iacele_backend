from datetime import timedelta
from datetime import timezone

# Zona horaria local
LOCAL_TZ = timezone(timedelta(hours= -7))

# Campos predeterminados a leer en perfil de usuario
PRESET_PROFILE_FIELDS = [
    'name',
    'active',
    'login',
    'profile_picture',
    (
        'role_ids',
        [
            'name',
            'label',
            (
                'group_ids',
                ['name'],
            )
        ],
    )
]

class LOCATION:
    CSL = 'csl'
    SJC = 'sjc'
