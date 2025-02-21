from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Date,
    Float,
    Integer,
    String,
    Text,
    Enum as SQLEnum
)
from app.database._base import Base
from app.database._types import (
    BusinessModel,
    ModuleOrigin,
    WarehouseCode,
)

class CommissionsLine(Base):

    __tablename__ = 'commissions.line'

    # ID de línea de factura
    invoice_line_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # ID de factura
    invoice_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Fecha de factura
    invoice_date: Mapped[Date] = mapped_column(Date)
    # Folio de factura
    name: Mapped[int] = mapped_column(String(20))
    # Origen de factura
    invoice_origin: Mapped[int] = mapped_column(String(100), nullable= True)

    # ID de la vendedora en Odoo
    salesperson_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Modelo de negocio
    business_model: Mapped[BusinessModel] = mapped_column(SQLEnum(BusinessModel), nullable=True)
    # Almacén
    warehouse: Mapped[WarehouseCode] = mapped_column(SQLEnum(WarehouseCode), nullable= True)
    # Orden de origen
    origin_module: Mapped[ModuleOrigin] = mapped_column(SQLEnum(ModuleOrigin), nullable= True)

    # Nombre del cliente
    partner_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Nombre del cliente
    partner_name: Mapped[str] = mapped_column(String(160), nullable= True)
    # ID del producto
    product_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Código del producto
    internal_reference: Mapped[str] = mapped_column(String(16), nullable= True)
    # Descripción del producto
    product_name: Mapped[str] = mapped_column(String(160), nullable= True)
    # Cantidad del producto
    quantity: Mapped[float] = mapped_column(Float, nullable= True)
    # Precio unitario del producto
    price_unit: Mapped[float] = mapped_column(Float, nullable= True)
    # Precio subtotal del producto
    price_subtotal: Mapped[float] = mapped_column(Float, nullable= True)

    # ID de compra
    purchase_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Folio de la compra
    purchase_name: Mapped[str] = mapped_column(String(120), nullable= True)
    # ID de proveedor
    vendor_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Nombre del proveedor
    vendor_name: Mapped[int] = mapped_column(String(160), nullable= True)
    # Fecha de la compra
    purchase_date: Mapped[Date] = mapped_column(Date, nullable= True)
    # Costo unitario
    product_cost: Mapped[float] = mapped_column(Float, nullable= True)
    # Costo subtotal
    cost_subtotal: Mapped[float] = mapped_column(Float, nullable= True)
    # Descuento
    discount: Mapped[float] = mapped_column(Float, nullable= True)

    # Porcentaje de comisión del cliente
    partner_commission: Mapped[float] = mapped_column(Float, nullable= True)
    # Costo de la comisión del cliente
    partner_commission_cost: Mapped[float] = mapped_column(Float, nullable= True)

    # Utilidad
    utility_subtotal: Mapped[float] = mapped_column(Float, nullable= True)
    # Porcentaje de utilidad
    total_utility_pct: Mapped[float] = mapped_column(Float, nullable= True)
    # Margen
    margin: Mapped[float] = mapped_column(Float, nullable= True)

    # Costo subtotal después de comisión del cliente
    cost_subtotal_after_partner_commission: Mapped[float] = mapped_column(Float, nullable= True)
    # Utilidad después de comisión del cliente
    utility_subtotal_after_partner_commission: Mapped[float] = mapped_column(Float, nullable= True)
    # Porcentaje de utilidad después de comisión del cliente
    utility_subtotal_after_partner_commission_pct: Mapped[float] = mapped_column(Float, nullable= True)
    # Margen de contribución después de comisión del cliente
    margin_after_partner_commission_pct: Mapped[float] = mapped_column(Float, nullable= True)

    # Comentarios de corrección
    notes: Mapped[str] = mapped_column(Text, nullable= True)
