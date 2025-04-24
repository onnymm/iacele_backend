from .base_users import *

server_actions = {
    'base.users': {
        'activate_user': activate_user,
        'deactivate_user': deactivate_user,
        'reset_password': reset_password,
    }
}
