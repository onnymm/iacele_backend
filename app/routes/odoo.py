from fastapi import APIRouter, status, Query
from odoo_api_manager import OdooAPIManager
from app.models.odoo_models import ModelFields
from app.utils.common import paginate, get_fields_info

# Manager para el API de Odoo
odoo = OdooAPIManager()

# Ruteador
router = APIRouter()

@router.get(
    "/model_fields",
    status_code= status.HTTP_200_OK
)
async def _get_model_fields(params: ModelFields = Query()):
    """
    ## Consulta de campos de un modelo de Odoo
    Esta función muestra los campos del modelo de Odoo provisto, para poder ser
    mostrados en una tabla en el frontend de iaCele.
    """
    data = odoo.data.model_fields(params.model)
    (start_index, end_index) = paginate(params.page, params.items_per_page)

    return {
        'data': (
            data
            .iloc[start_index: end_index]
            .iacele.to_backend_response()
        ),
        'fields': get_fields_info(data),
        'count': len(data),
    }
