from fastapi import FastAPI
from app import iacele
from app._routes import auth
from app._routes import crud
from app._routes import server

# Inicialización final de la base de datos
iacele.populate_if_first_initialization()

# Inicialización de la app
app = FastAPI()

# Adición de routers
app.include_router(auth.router)
app.include_router(crud.router)
app.include_router(server.router)
