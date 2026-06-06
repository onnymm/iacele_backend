from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import iacele
from app._routes import auth
from app._routes import account
from app._routes import crud
from app._routes import frontend
from app._routes import metadata
from app._routes import server
from app._settings import CONFIG

# Inicialización final de la base de datos
iacele.populate_if_first_initialization()

# Inicialización de la app
app = FastAPI()

# Adición de routers
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(crud.router)
app.include_router(frontend.router)
app.include_router(metadata.router)
app.include_router(server.router)

# Control de middlewares para permitir las solicitudes desde el servidor frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins= CONFIG.FRONTEND_URLS,
    allow_credentials= True,
    allow_methods= ['*'],
    allow_headers= ['*'],
)
