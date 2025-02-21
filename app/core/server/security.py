from app.utils.ip import local_ip
from app import settings

# Orígenes autorizados
allowed_origins = [
    f"http://{local_ip}:{settings._backend.REACT_PORT}",
    f"http://{local_ip}:{settings._backend.ALT_REACT_PORT}",
    f"localhost:{settings._backend.REACT_PORT}",
    f"localhost:{settings._backend.ALT_REACT_PORT}",
]