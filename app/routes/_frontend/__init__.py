from fastapi import APIRouter
from app.constants import TAG
from . import (
    _form,
    _list,
)

router = APIRouter(
    prefix= '/frontend',
    tags= [TAG.FRONTEND],
)

router.include_router(_list.router)
router.include_router(_form.router)
