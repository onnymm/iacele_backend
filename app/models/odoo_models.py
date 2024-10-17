from pydantic import BaseModel
from odoo_api_manager import OdooAPIManager
from app.models.base import BaseDataRequest

class ModelFields(BaseDataRequest):
    model: OdooAPIManager.odoo_models
