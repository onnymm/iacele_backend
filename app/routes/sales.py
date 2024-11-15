from app.models.data_view import DataViewParameters, ResponseCommissionsData
from fastapi import APIRouter, status, Query, Body, Depends
from app.security import get_current_user
from app.models import UserInDB, BaseDataRequest
from app.database import db_connection
from app.utils.common import paginate
from typing import Annotated, Union
from app.api.callbacks import get_commisions

router = APIRouter()

@router.get(
    "/commissions",
    status_code= status.HTTP_200_OK,
    name= "Mis comisiones",
    response_model= Union[ResponseCommissionsData, list]
)
async def _show_commisions(params: BaseDataRequest = Query(), user: UserInDB = Depends(get_current_user)):

    ( index_start, index_end ) = paginate(params.page, params.items_per_page)

    data = db_connection.search_read("commissions", [('salesperson_id', '=', user.odoo_id)], offset= index_start, limit= index_end, output_format= "dict")

    return data
