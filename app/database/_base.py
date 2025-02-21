from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import (
    Integer,
    DateTime,
)

class Base(DeclarativeBase):
    """
    Clase base para la declaración de la base de datos.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    create_date: Mapped[DateTime] = mapped_column(DateTime, default= datetime.now)
    write_date: Mapped[DateTime] = mapped_column(DateTime, default= datetime.now, onupdate= datetime.now)
