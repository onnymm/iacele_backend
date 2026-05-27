from .._core import env_

class CONFIG:
    CRYPT_KEY = env_.variable('CRYPT_KEY')
    FRONTEND_URL = env_.variable('FRONTEND_URL')
