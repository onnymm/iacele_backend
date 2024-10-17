from pydantic import BaseModel

class BaseDataRequest(BaseModel):
    page: int
    items_per_page: int
