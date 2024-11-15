from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enum import Enum
from sqlalchemy.types import (
    Integer,
    Float,
    DateTime,
    TypeDecorator,
)

class _Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    create_date: Mapped[DateTime] = mapped_column(DateTime, default= datetime.now)
    write_date: Mapped[DateTime] = mapped_column(DateTime, default= datetime.now, onupdate=datetime.now)

class db_enum(Enum):

    def __str__(self):
        return self.value

class State(db_enum):
    draft = "draft"
    sent = "sent"
    posted = "posted"
    cancel = "cancel"

class SaleTeamCode(db_enum):
    a1_piso = "a1_piso"
    a2_piso = "a2_piso"
    a1_ce = "a1_ce"
    a2_ce = "a2_ce"

    def __str__(self):
        return self.value

class BusinessModel(db_enum):
    piso = "piso"
    ce = "ce"

class WarehouseCode(db_enum):
    a1 = "a1"
    a2 = "a2"

class Money(TypeDecorator):
    impl = Float

    cache_ok = True 

    def process_bind_param(self, value, dialect):
        return round(float(value), 2) if value is not None else None
    
    def process_result_value(self, value, dialect):
        return round(float(value), 2) if value is not None else None
