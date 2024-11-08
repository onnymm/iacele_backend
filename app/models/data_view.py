from pydantic import BaseModel, Field
from typing import Literal
from datetime import date

class DataViewParameters(BaseModel):
    """
    ## Parámetros de vista de datos
    Estructura de datos para visualización de datos de una o más tablas SQL.
    Los parámetros disponibles son los siguientes:
    - `page`: Página del conjunto de registros a mostrar. Esto va en función del
    número de registros por página (`items_per_page`).
    - `items_per_page`: Número de registros a mostrar por página.
    - `search_criteria`: Búsqueda por algún criterio para filtrar registros.
    - `sortby`: Ordenar por algún campo de los registros.
    - `ascending`: Ordenamiento ascendente o descendente, en función del campo
    a usar para ordenar en el parámetro `sortby`.
    - `search`: Búsqueda por coincidencias de texto.
    """
    page: int = Field(
        default= 0,
        ge= 0,
        description= "Página del conjunto de registros a mostrar. Esto va en función del número de registros por página (`items_per_page`)."
    )
    items_per_page: int = Field(
        default= 40,
        ge= 0,
        description= "Número de registros a mostrar por página."
    )
    search_criteria: str = Field(
        default= "",
        description= "Búsqueda por algún criterio para filtrar registros."
    )
    sortby: str | None = Field(
        default= None,
        pattern= "[a-z_]",
        description= "Ordenar por algún campo de los registros."
    )
    ascending: bool | None = Field(
        default= None,
        description= "Ordenamiento ascendente o descendente, en función del campo a usar para ordenar en el parámetro `sortby`."
    )
    search: str | None = Field(
        default= None
    )

class _CommisionsBaseData(BaseModel):
    invoice_line_id: int
    invoice_order_id: int
    name: str
    invoice_date: date
    state: str
    partner_id: int
    partner_name: str
    salesperson_id: int
    salesperson_name: str
    sale_team_code: str
    bussiness_model: str
    warehouse_code: str
    product_id: int
    product_name: str
    product_default_code: str | None
    product_quantity: float
    product_price_unit: float
    product_discount: float
    price_subtotal: float
    line_commision: float

class FieldsInfo(BaseModel):
    name: str
    ttype: Literal["char", "float", "int", "date", "datetime", "selection", "monetary"]

class ResponseCommissionsData(BaseModel):
    data: list[_CommisionsBaseData]
    fields: list[FieldsInfo]
    count: int
