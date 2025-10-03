from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from lylac.errors import InvalidPasswordError
from app.core import LOCAL_FRONTEND
from app.data import OPENAPI_TAGS
from app.routes import (
    auth,
    account,
    crud,
    frontend,
    _frontend,
    server,
)

app = FastAPI(
    title= 'iaCele',
    version= 'v0.1.0',
    description= 'Backend de la aplicación de iaCele.',
    openapi_tags= OPENAPI_TAGS
)

@app.exception_handler(PermissionError)
async def permission_handler(_: Request, __: PermissionError):

    raise HTTPException(
        status_code= status.HTTP_403_FORBIDDEN,
        detail= 'No cuentas con los permisos para realizar esta acción.',
    )

@app.exception_handler(InvalidPasswordError)
async def wrong_password_handler(_: Request, __: InvalidPasswordError):

    raise HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= 'Usuario o contraseña incorrecta.',
    )

# Control de middlewares para permitir las solicitudes desde el servidor frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins= [LOCAL_FRONTEND],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(crud.router)
app.include_router(frontend.router)
app.include_router(_frontend.router)
app.include_router(server.router)
