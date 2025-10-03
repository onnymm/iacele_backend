from app.constants import TAG

OPENAPI_TAGS = [
    {
        'name': TAG.AUTH,
        'description': 'Autenticación del usuario.',
    },
    {
        'name': TAG.ACCOUNT,
        'description': 'Datos del usuario de la sesión actual activa.',
    },
    {
        'name': TAG.CRUD,
        'description': 'Métodos de transacción básicos CRUD usados para cualquier necesidad básica.',
    },
    {
        'name': TAG.FRONTEND,
        'description': 'Endpoints para obtención de datos para visualizar en un formato específico.'
    },
    {
        'name': TAG.SERVER,
        'description': 'Funciones de servidor.'
    },
]
