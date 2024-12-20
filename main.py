from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.backend.origins import allowed_origins
from app.constants.routes import api_routes
from app.constants.tags import tags
from app.routes import (
    account,
    authentication,
    odoo,
    sales,
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

# Rutas de estructura base de la aplicación
app.include_router(authentication.router, prefix= api_routes.authentication, tags= [tags.authentication])
app.include_router(account.router, prefix= api_routes.account, tags= [tags.account])

# Rutas a incluir
app.include_router(odoo.router, prefix= api_routes.odoo, tags= [tags.odoo])
app.include_router(sales.router, prefix= api_routes.odoo, tags= [tags.sales])
