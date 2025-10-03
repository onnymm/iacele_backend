from fastapi import (
    APIRouter,
    status,
    Depends,
)
from pydantic import BaseModel
from app.constants import TAG
from app.core import iacele
from app.security import authenticate_user

class TreeRead(BaseModel):
    model_name: str
    record_ids: list[int]

router = APIRouter(
    prefix= '/frontend',
    tags= [TAG.FRONTEND],
)

@router.post(
    '/tree',
    name= 'Obtención de datos para árbol',
    status_code= status.HTTP_200_OK,
    deprecated= True,
)
async def _tree(
    params: TreeRead,
    user_id: int = Depends(authenticate_user),
):

    return iacele.tree.read(user_id, params.model_name, params.record_ids)
