from dml_manager import DMLManager
from app.database._base import Base
from .models import *

db_connection = DMLManager('env', Base, 'dict')
