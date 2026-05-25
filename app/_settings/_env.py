from .._core import env_

class CONFIG:
    CRYPT_KEY = env_.variable('CRYPT_KEY')
