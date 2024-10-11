from app.utils.ip import local_ip
from app.constants.clients import react_port, alt_react_port

# Orígenes autorizados
allowed_origins = [
    f"http://{local_ip}:{react_port}",
    f"http://{local_ip}:{alt_react_port}",
    f"localhost:{react_port}",
    f"localhost:{alt_react_port}",
]
