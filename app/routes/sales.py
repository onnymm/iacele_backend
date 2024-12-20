from app.models.data_view import DataViewParameters, ResponseCommissionsData
from fastapi import APIRouter, status, Query, Depends
from app.security import get_current_user
from app.models import UserInDB, BaseDataRequest
from app.database import db_connection
from app.core.sales import get_stats
from app.dependencies.common import criteria_from_endpoint
from app.dependencies.data_for_table import get_data_for_table

router = APIRouter()

@router.get(
    "/commissions",
    status_code= status.HTTP_200_OK,
    name= "Mis comisiones",
    # response_model= Union[ResponseCommissionsData, list]
)
async def _show_commisions(params: BaseDataRequest = Query(), user: UserInDB = Depends(get_current_user), build_criteria = Depends(criteria_from_endpoint)):

    search_criteria = build_criteria([('salesperson_id', '=', user.odoo_id)])

    return get_data_for_table(
        "commissions",
        params = params,
        search_criteria= search_criteria
    )

@router.get(
    "/commission_record",
    status_code= status.HTTP_200_OK,
    name= "Detalle de comisiones",
)
async def _commision_record(id: int = Query(), user: UserInDB = Depends(get_current_user)):

    search_criteria = [
        "&",
            ("salesperson_id", "=", user.odoo_id),
            ("id", "=", id)
    ]

    record = db_connection.search_read(
        "commissions",
        search_criteria,
        output_format= "dict"
    )

    print(record)

    return record

@router.get(
    "/stats",
    status_code= status.HTTP_200_OK,
    name= "Resumen",
)
async def _get_stats(user: UserInDB = Depends(get_current_user)):

    return get_stats(user.odoo_id)
