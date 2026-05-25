from typing import Literal
from pydantic import BaseModel

class TokenData(BaseModel):
    """
    Token de autenticación de usuario.
    """
    access_token: str
    token_type: Literal['bearer']
