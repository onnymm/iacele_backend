from ._types import _Base
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.types import (
    Integer,
    String,
)

class Users(_Base):

    __tablename__ = "users"
    user: Mapped[str] = mapped_column(String(24), nullable= False, unique= True)
    name: Mapped[str] = mapped_column(String(60), nullable= False)
    odoo_id: Mapped[int] = mapped_column(Integer, nullable= True)
    password: Mapped[str] = mapped_column(String(60), nullable= False)
