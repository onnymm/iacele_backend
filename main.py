from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares import CamelCaseMiddleware
from app.core.server import allowed_origins
from app.routes import (
    account,
    authentication,
    crud,
    sales,
    tasks,
)

# App del servidor 
app = FastAPI()

# Control de middlewares para permitir las solicitudes desde el servidor frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins= allowed_origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)
app.add_middleware(CamelCaseMiddleware)

# Rutas de estructura base de la aplicación
app.include_router(authentication.router)

# Usable por el frontend
app.include_router(account.router)
app.include_router(sales.router)

# Ruta para transacciones de datos comunes
app.include_router(crud.router)

# Tareas
app.include_router(tasks.router)
