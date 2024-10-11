from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.origins import allowed_origins
from app.routes import odoo
from app.constants.routes import api_routes
from app.constants.tags import tags

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

# Rutas a incluir
app.include_router(odoo.router, prefix= api_routes.odoo, tags= [tags.odoo])
