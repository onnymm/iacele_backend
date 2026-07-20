from collections import defaultdict
from fastapi import WebSocket
from lylac import Notifier
import asyncio

class WebsocketManager:

    def __init__(
        self,
    ) -> None:

        # Inicialización de objeto de conexiones
        self._connections = defaultdict[int, set[WebSocket]](set)

    async def connect(
        self,
        uid: int,
        websocket: WebSocket,
    ) -> None:

        await websocket.accept()
        self._connections[uid].add(websocket)

    async def disconnect(
        self,
        uid: int,
        websocket: WebSocket,
    ) -> None:

        self._connections[uid].discard(websocket)

        if not self._connections[uid]:
            del self._connections[uid]

    async def notify(
        self,
        uid: int,
        payload: dict,
    ) -> None:

        for websocket in self._connections.get(uid, []):
            await websocket.send_json(payload)

    def schedule_notify(
        self,
        uid: int,
        payload: dict,
    ) -> None:

        loop = asyncio.get_running_loop()
        loop.create_task(
            self.notify(uid, payload)
        )

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
        
        # Construcción del objeto de payload
        payload = {
            'name': notification.name,
            'payload': notification.payload,
        }

        # Si el objetivo de la notificación es el usuario actual...
        if notification.target == 'current_user':
            # Se realiza la notificación por el administrador de websockets
            ws_manager.notify(
                self._uid,
                payload,
            )

        # Si el objetivo es una lista de IDs...
        else:
            # Iteración por cada ID de la lista
            for uid in notification.target:
                ws_manager.schedule_notify(
                    uid,
                    payload,
                )

ws_manager = WebsocketManager()
