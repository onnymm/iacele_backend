ROOT_PATH = '/'

class AUTH:
    ALGORYTHM = 'HS256'
    TOKEN_TYPE = 'bearer'

class ROUTER_PREFIX:
    TOKEN = '/token'
    ACCOUNT = '/account'
    CRUD = '/crud'
    FRONTEND = '/frontend'
    METADATA = '/metadata'
    SERVER = '/server'

class ENDPOINT_PATH:
    class AUTH:
        TOKEN = ROOT_PATH
    class ACCOUNT:
        ME = '/me'
    class METADATA:
        FIELDS = '/fields'
    class CRUD:
        CREATE = '/create'
        SEARCH = '/search'
        READ = '/read'
        SEARCH_READ = '/search_read'
        SEARCH_COUNT = '/search_count'
        UPDATE = '/update'
        DELETE = '/delete'
    class FRONTEND:
        TREE = '/tree'
        FORM = '/form'
    class SERVER:
        ACTION = '/action'
        TASK = '/task'

class ENDPOINT_NAME:
    class AUTH:
        TOKEN = 'Obtención de token'
    class ACCOUNT:
        ME = 'Mi usuario'
    class CRUD:
        CREATE = 'Creación de registros'
        SEARCH = 'Búsqueda de registros'
        READ = 'Lectura de registros'
        SEARCH_READ = 'Búsqueda y lectura de registros'
        SEARCH_COUNT = 'Conteo de búsqueda de registros'
        UPDATE = 'Modificación de registros'
        DELETE = 'Eliminación de registros'
    class FRONTEND:
        TREE = 'Búsqueda y lectura para vista de árbol'
        FORM = 'Lectura para vista de formulario'
    class METADATA:
        FIELDS = 'Metadatos de campos'
    class SERVER:
        ACTION = 'Acción de registro'
        TASK = 'Tarea de servidor'

class TAG:
    AUTH = 'Autenticación'
    ACCOUNT = 'Cuenta'
    FRONTEND = 'Frontend'
    METADATA = 'Metadatos'
    CRUD = 'Transacciones CRUD'
    SERVER = 'Procesos de servidor'

SESSION_UUID = 'uuid'
