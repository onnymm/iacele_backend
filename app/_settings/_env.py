import json
from .._core import env_

class CONFIG:
    CRYPT_KEY = env_.variable('CRYPT_KEY')
    FRONTEND_URLS = env_.variable('FRONTEND_URLS', json.loads)
