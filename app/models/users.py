from pydantic import BaseModel
from datetime import datetime

class BaseRecord(BaseModel):
    user: str | None = None
    name: str | None = None
    odoo_id: int | None = None

class BaseUser(BaseModel):
    user: str
    name: str
    odoo_id: int

class UserNewData(BaseModel):
    user: str | None = None
    name: str | None = None
    odoo_id: int | None = None

class UserData(BaseUser):
    password: str

class UserInDB(UserData, BaseRecord):
    pass
