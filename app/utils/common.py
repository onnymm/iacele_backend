from typing import Tuple
from app.core.odoo_manager import odoo, odoo_models
import pandas as pd

def paginate(page: int, items_per_page: int) -> Tuple[int, int]:
    start_index = items_per_page * page
    end_index = start_index + items_per_page

    return start_index, end_index

def get_fields_info(
    data: pd.DataFrame,
):

    # Obtención del tipo de campos en Odoo
    fields: pd.DataFrame = odoo.data.model_fields("ir.model.fields", ["name", "ttype"], list(data.columns))

    # Conversión a lista de diccionarios
    fields_info = fields.iacele.to_backend_response()

    # Retorno de los datos
    return fields_info
