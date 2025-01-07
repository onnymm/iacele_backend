from pydantic import BaseModel

class BaseDataRequest(BaseModel):
    page: int
    items_per_page: int
    sortby: str | list[str] | None = None
    ascending: bool | list[bool] = True
    search: str | None = '{"text":"","method":[]}'

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'page': 0,
                    'items_per_page': 40,
                    'search': '{"text":"" ,"method":[]}'
                }
            ]
        }
    }
