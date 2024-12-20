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

    business_model: Mapped[SaleTeamCode] = mapped_column(SQLEnum(BusinessModel), nullable=True)
    warehouse: Mapped[SaleTeamCode] = mapped_column(Integer, nullable= True)
    invoice_doc_id: Mapped[int] = mapped_column(Integer)
    invoice_name: Mapped[int] = mapped_column(String(20))
    invoice_date: Mapped[Date] = mapped_column(Date)
    invoice_origin: Mapped[int] = mapped_column(String(100), nullable= True)
    partner_name: Mapped[str] = mapped_column(String(160), nullable= True)
    salesperson_id: Mapped[int] = mapped_column(Integer, nullable= True)
    internal_reference: Mapped[str] = mapped_column(String(16), nullable= True)
    product_name: Mapped[str] = mapped_column(String(160))
    quantity: Mapped[float] = mapped_column(Float)
    price_unit: Mapped[float] = mapped_column(Float)
    price_subtotal: Mapped[float] = mapped_column(Float)
    purchase_name: Mapped[int] = mapped_column(String(120), nullable= True)
    vendor_name: Mapped[str] = mapped_column(String(100), nullable= True)
    product_cost: Mapped[float] = mapped_column(Float, nullable= True)
    cost_subtotal: Mapped[float] = mapped_column(Float, nullable= True)
    subtotal_commission: Mapped[float] = mapped_column(Float, nullable= True)
    subtotal_commission_pct: Mapped[float] = mapped_column(Float, nullable= True)
    subtotal_contribution_pct: Mapped[float] = mapped_column(Float, nullable= True)
    customer_commission_pct: Mapped[float] = mapped_column(Float, nullable= True)
    customer_commission: Mapped[float] = mapped_column(Float, nullable= True)
    product_total_cost: Mapped[float] = mapped_column(Float, nullable= True)
    product_total_commission: Mapped[float] = mapped_column(Float, nullable= True)
    total_utility_pct: Mapped[float] = mapped_column(Float, nullable= True)
    total_contribution_pct: Mapped[float] = mapped_column(Float, nullable= True)
