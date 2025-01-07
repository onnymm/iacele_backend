from fastapi import APIRouter, status, Query, Depends
from app.security import get_current_user
from app.models import UserInDB, BaseDataRequest
from app.database import db_connection
from app.core.sales import get_stats
from app.dependencies.common import criteria_from_endpoint
from app.dependencies.data_for_table import get_data_for_table
from app.types import DataResponse, CriteriaStructure
from typing import Callable
from app.models.data_view import DataViewResponse

router = APIRouter()

@router.get(
    "/commissions",
    status_code= status.HTTP_200_OK,
    name= "Mis comisiones",
    response_model= DataViewResponse,
)
async def _show_commisions(
    params: BaseDataRequest = Query(),
    user: UserInDB = Depends(get_current_user),
    build_criteria: Callable[[CriteriaStructure], CriteriaStructure] = Depends(criteria_from_endpoint),
) -> DataResponse:

    return get_data_for_table(
        "commissions",
        params = params,
        search= params.search,
        search_criteria= build_criteria(
            [('salesperson_id', '=', user.odoo_id)]
        ),
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

    return record

@router.get(
    "/stats",
    status_code= status.HTTP_200_OK,
    name= "Resumen",
)
async def _get_stats(user: UserInDB = Depends(get_current_user)):

    return get_stats(user.odoo_id)
