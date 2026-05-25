ROOT_PATH = '/'

class AUTH:
    ALGORYTHM = 'HS256'
    TOKEN_TYPE = 'bearer'

class ROUTER_PREFIX:
    TOKEN = '/token'
    CRUD = '/crud'
    SERVER = '/server'

class ENDPOINT_PATH:
    class AUTH:
        TOKEN = ROOT_PATH
    class CRUD:
        CREATE = '/create'
        SEARCH = '/search'
        READ = '/read'
        SEARCH_READ = '/search_read'
        UPDATE = '/update'
        DELETE = '/delete'
    class SERVER:
        ACTION = '/action'
        TASK = '/task'

class ENDPOINT_NAME:
    class AUTH:
        TOKEN = 'Obtención de token'
    class CRUD:
        CREATE = 'Creación de registros'
        SEARCH = 'Búsqueda de registros'
        READ = 'Lectura de registros'
        SEARCH_READ = 'Búsqueda y lectura de registros'
        UPDATE = 'Modificación de registros'
        DELETE = 'Eliminación de registros'
    class SERVER:
        ACTION = 'Acción de registro'
        TASK = 'Tarea de servidor'

class TAG:
    AUTH = 'Autenticación'
    CRUD = 'Transacciones CRUD'
    SERVER = 'Procesos de servidor'

SESSION_UUID = 'uuid'
