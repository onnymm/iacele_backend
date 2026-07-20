from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from .._constants import ENDPOINT_NAME
from .._constants import QUERY_PARAMS
from .._constants import ROOT_PATH
from .._constants import ROUTER_PREFIX
from .._constants import TAG
from .._core import iacele
from .._core import ws_manager
from .._security import authenticate_user

# Inicialización de router de websockets
router = APIRouter(
    prefix= ROUTER_PREFIX.WEBSOCKET,
    tags= [TAG.WEBSOCKETS],
)

@router.websocket(
    ROOT_PATH,
    name= ENDPOINT_NAME.WEBSOCKET,
)
async def _websocket(
    websocket: WebSocket,
):

    # Obtención del token de autenticación
    token = websocket.query_params[QUERY_PARAMS.TOKEN]
    # Obtención de la UUID de sesión del usuario
    session_uuid = authenticate_user(token)
    # Autenticación del usuario
    user_id = iacele.authenticate_user(session_uuid)
    # Se registra la conexión del websocket
    await ws_manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(user_id, websocket)
