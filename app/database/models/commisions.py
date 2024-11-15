from ._types import _Base, State, SaleTeamCode, BusinessModel, WarehouseCode, Money
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.types import (
    Integer,
    String,
    Float,
    Date,
    Enum as SQLEnum
)

class Commissions(_Base):

    __tablename__ = "commissions"

    invoice_line_id: Mapped[int] = mapped_column(primary_key= True)
    invoice_doc_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[int] = mapped_column(String(20))
    invoice_date: Mapped[Date] = mapped_column(Date)
    state: Mapped[State] = mapped_column(SQLEnum(State))
    partner_id: Mapped[int] = mapped_column(Integer)
    partner_name: Mapped[str] = mapped_column(String(100), nullable=True)
    salesperson_id: Mapped[int] = mapped_column(Integer, nullable=True)
    salesperson_name: Mapped[str] = mapped_column(String(100))
    sale_team_code: Mapped[SaleTeamCode] = mapped_column(SQLEnum(SaleTeamCode))
    business_model: Mapped[SaleTeamCode] = mapped_column(SQLEnum(BusinessModel))
    warehouse_code: Mapped[SaleTeamCode] = mapped_column(SQLEnum(WarehouseCode))
    product_id: Mapped[int] = mapped_column(Integer)
    product_name: Mapped[str] = mapped_column(String(100))
    internal_reference: Mapped[str] = mapped_column(String(16), nullable=True)
    quantity: Mapped[float] = mapped_column(Float)
    price_unit: Mapped[float] = mapped_column(Money)
    discount: Mapped[float] = mapped_column(Float)
    price_subtotal: Mapped[float] = mapped_column(Money)
    line_comission: Mapped[float] = mapped_column(Money)
