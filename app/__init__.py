from odoo_api_manager import OdooAPIManager
from .settings.settings import settings
from .security.auth import hash_password

from .database import db_connection

odoo = OdooAPIManager()
