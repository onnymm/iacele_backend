from collections import defaultdict
from fastapi import WebSocket
from lylac import Notifier
import asyncio

class WebsocketManager:
    _connections: defaultdict[int, set[WebSocket]]

    def __init__(
        self,
    ) -> None:

        # Inicialización de objeto de conexiones
        self._connections = defaultdict(set)

    async def connect(
        self,
        uid: int,
        websocket: WebSocket,
    ) -> None:

        # Se acepta la conexión de websocket
        await websocket.accept()
        # Se añade el websocket a la lista de conexiones del usuario
        self._connections[uid].add(websocket)

    async def remove(
        self,
        uid: int,
        websocket: WebSocket,
    ) -> None:

        # Se descarta el websocket de la lista de conexiones del usuario
        self._connections[uid].discard(websocket)

        # Si la lista de conexiones del usuario está vacía...
        if not self._connections[uid]:
            # Se elimina ésta
            del self._connections[uid]

    async def notify(
        self,
        uid: int,
        payload: dict,
    ) -> None:

        # Obtención de la lista de conexiones del usuario
        user_connections = self._connections.get(uid, set())

        # Iteración por cada conexión de la lista de conexiones
        for websocket in user_connections:
            # Envío de 
            await websocket.send_json(payload)

    def schedule_notify(
        self,
        uid: int,
        payload: dict,
    ) -> None:

        # Obtención del loop de la ejecución actual
        # Esto debe estar ejecutándose en un endpoint de FastAPI
        loop = asyncio.get_running_loop()
        # Ejecución de función asíncrona
        loop.create_task( self.notify(uid, payload) )

class WebsocketNotifier(Notifier):

    def __init__(
        self,
        uid: int,
    ) -> None:

        # Asignación de valores
        self._uid = uid
        # Inicialización de lista de notificaciones a enviar después de commit
        self._post_commit_notifications = []

    def send(
        self,
        notification,
    ) -> None:

        # Construcción del objeto de mensaje
        message = {
            'event': notification.event,
            'payload': notification.payload,
        }

        # Si el objetivo de la notificación es el usuario actual...
        if notification.target == 'current_user':
            # Se realiza la notificación por el administrador de websockets
            ws_manager.schedule_notify(
                self._uid,
                message,
            )

        # Si el objetivo es una lista de IDs...
        else:
            # Iteración por cada ID de la lista
            for uid in notification.target:
                ws_manager.schedule_notify(
                    uid,
                    message,
                )

ws_manager = WebsocketManager()
