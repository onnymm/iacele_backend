from pydantic import BaseModel

class BaseDataRequest(BaseModel):
    page: int
    items_per_page: int
    sortby: str | list[str] | None = None
    ascending: bool | list[bool] = True
