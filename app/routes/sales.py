from app.models.data_view import DataViewParameters, ResponseCommissionsData
from fastapi import APIRouter, status, Query
from typing import Annotated
from app.api.callbacks import get_commisions

router = APIRouter()

@router.get(
    "/commisions",
    status_code=status.HTTP_200_OK,
    name= "Comisiones",
    response_model=ResponseCommissionsData
)
async def _show_data(params: Annotated[DataViewParameters, Query()]):
    """
    ## Visualización de comisiones
    Este endpoint muestra la vista de comisiones de alguna vendedora, para
    mostrarse en una vista de tabla o de kanban.

    ----
    ### Parámetros de vista de datos

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
    ----
    ## Campos disponibles
    - `'fact_line_id'`: ID de línea de factura.
    - `'fact_doc_id'`: ID de factuta.
    - `'name'`: Folio de factura.
    - `'invoice_date'`: Fecha de factura.
    - `'state'`: Estado de la factura.
    - `'partner_id_x'`: ID del cliente.
    - `'partner_name_x'`: Nombre del cliente.
    - `'salesperson_id'`: ID de la vendedora.
    - `'salesperson_name'`: Nombre de la vendedora.
    - `'sale_team_description'`: Nombre del equipo de ventas.
    - `'business_model'`: Modelo de negocio.
    - `'warehouse'`: Clave del almacén.
    - `'product_id_pp'`: ID del producto.
    - `'product_name_y'`: Nombre del producto.
    - `'prod_codigo'`: Código del producto.
    - `'quantity'`: Cantidad del producto.
    - `'price_unit'`: Precio unitario del producto.
    - `'discount'`: Descuento del producto.
    - `'price_subtotal'`: Subtotal de la línea de factura.
    - `'utilidad_partida_$'`: Utilidad de la línea de factura.
    """
    search = None
    if params.search:
        search = eval(params.search)

    return get_commisions(
        params.page,
        params.items_per_page,
        search_criteria= params.search_criteria,
        sortby= params.sortby,
        ascending= params.ascending,
        search= search
    )
