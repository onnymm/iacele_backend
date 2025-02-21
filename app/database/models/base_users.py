from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Boolean,
    Integer,
    String,
)
from app.database._base import Base

class BaseUsers(Base):

    __tablename__ = 'base.users'

    user: Mapped[str] = mapped_column(String(40), nullable= False, unique= True)
    name: Mapped[str] = mapped_column(String(60), nullable= False)
    odoo_id: Mapped[int] = mapped_column(Integer, nullable= True)
    password: Mapped[str] = mapped_column(String(60), nullable= False)
    active: Mapped[str] = mapped_column(Boolean, default= True)
